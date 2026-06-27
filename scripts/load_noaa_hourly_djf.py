#!/usr/bin/env python3
"""Load available NOAA Global Hourly CSV files into weather.hourly_djf.

This is a batch loader. It intentionally loads DJF observations only, because
that is the weather slice needed for ECWT and avoids inflating the working DB
with non-winter observations before the ECWT method is validated.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import io
import json
import math
import subprocess
from collections import OrderedDict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable

from eop012_config import PROJECT_ROOT, PSQL, STAGING_ROOT

DEFAULT_STAGING_ROOT = STAGING_ROOT

METHODOLOGY_VERSION = "eop012-ecwt-method-v0.2.0"
SOURCE_FAMILY = "noaa_global_hourly_djf_load"
DJF_MONTHS = {12, 1, 2}
SHEF_MIN_TEMP_C = -50.0


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def sql_literal(value: object) -> str:
    if value is None:
        return "null"
    text = str(value)
    return "'" + text.replace("'", "''") + "'"


def pg_csv_value(value: object) -> object:
    if value is None:
        return r"\N"
    if isinstance(value, float) and math.isnan(value):
        return r"\N"
    text = str(value)
    return r"\N" if text == "" else text


def run(cmd: list[str], *, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        cmd,
        input=input_text,
        text=True,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        raise RuntimeError(
            "Command failed with exit code "
            f"{result.returncode}: {' '.join(cmd)}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    return result


def psql_cmd(psql: Path, host: str, port: int, dbname: str, user: str | None = None) -> list[str]:
    cmd = [str(psql), "-h", host, "-p", str(port)]
    if user:
        cmd.extend(["-U", user])
    cmd.extend(["-d", dbname, "-v", "ON_ERROR_STOP=1"])
    return cmd


def psql_csv_query(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    query: str,
    user: str | None = None,
) -> list[dict[str, str]]:
    result = run(
        psql_cmd(psql, host, port, dbname, user)
        + ["-c", f"\\copy ({query}) to stdout with (format csv, header true)"]
    )
    return list(csv.DictReader(io.StringIO(result.stdout)))


def psql_scalar(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    query: str,
    user: str | None = None,
) -> str:
    result = run(psql_cmd(psql, host, port, dbname, user) + ["-At", "-c", query])
    return result.stdout.strip()


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: pg_csv_value(row.get(field)) for field in fieldnames})


def git_commit_label(project_root: Path) -> str:
    try:
        result = run(["git", "-C", str(project_root), "rev-parse", "HEAD"])
        return result.stdout.strip()
    except Exception:
        return "UNCOMMITTED_WORKTREE"


def copy_command(table: str, columns: list[str], path: Path) -> str:
    return f"\\copy {table} ({', '.join(columns)}) from '{path}' with (format csv, header true, null '\\N')"


def ensure_load_schema(psql: Path, host: str, port: int, dbname: str, user: str | None) -> None:
    sql = """
do $$
begin
    if not exists (
        select 1
        from pg_type t
        join pg_namespace n on n.oid = t.typnamespace
        where n.nspname = 'weather'
          and t.typname = 'source_channel'
    ) then
        create type weather.source_channel as enum (
            'noaa_global_hourly_aws',
            'noaa_lcd_cdo',
            'asos_iem',
            'noaa_isd_local_cache'
        );
    end if;
end $$;

alter table weather.station
    add column if not exists local_standard_utc_offset_hours integer;
update weather.station
set local_standard_utc_offset_hours = greatest(-12, least(14, round(longitude / 15.0)::integer))
where local_standard_utc_offset_hours is null
  and longitude is not null;
alter table weather.hourly_djf
    add column if not exists obs_timestamp timestamptz,
    add column if not exists source_channel weather.source_channel,
    add column if not exists source_code text,
    add column if not exists report_type text;
create table if not exists weather.noaa_hourly_load_file (
    load_file_id text primary key,
    calculation_run_id text not null references audit.calculation_run(calculation_run_id),
    station_id text not null references weather.station(station_id),
    source_year integer not null,
    raw_station_id text not null,
    local_path text not null,
    source_file_id text references audit.source_file(source_file_id),
    source_basis text not null,
    file_size_bytes bigint,
    file_status text not null,
    rows_seen bigint not null default 0,
    djf_rows_seen bigint not null default 0,
    rejected_source_rows bigint not null default 0,
    valid_temp_rows bigint not null default 0,
    invalid_temp_rows bigint not null default 0,
    rejected_plausibility_rows bigint not null default 0,
    duplicate_hour_count bigint not null default 0,
    loaded_hour_count bigint not null default 0,
    min_hour_ending_utc timestamptz,
    max_hour_ending_utc timestamptz,
    error_message text,
    notes text,
    created_at_utc timestamptz not null default now(),
    unique (station_id, source_year, local_path),
    constraint noaa_hourly_load_file_status_check
        check (file_status in ('loaded', 'failed', 'skipped'))
);
create index if not exists ix_noaa_hourly_load_file_status
    on weather.noaa_hourly_load_file (calculation_run_id, file_status);
create index if not exists ix_noaa_hourly_load_file_station_year
    on weather.noaa_hourly_load_file (station_id, source_year);
create index if not exists ix_noaa_hourly_load_file_status_year_station
    on weather.noaa_hourly_load_file (file_status, source_year, station_id);
create table if not exists weather.station_year_hourly_summary (
    station_id text not null references weather.station(station_id),
    source_year integer not null,
    valid_djf_hours bigint not null,
    min_hour_ending_utc timestamptz,
    max_hour_ending_utc timestamptz,
    refreshed_at_utc timestamptz not null default now(),
    source_basis text not null,
    primary key (station_id, source_year)
);
create index if not exists ix_station_year_hourly_summary_year
    on weather.station_year_hourly_summary (source_year);
alter table weather.noaa_hourly_load_file
    add column if not exists rejected_source_rows bigint not null default 0;
alter table weather.noaa_hourly_load_file
    add column if not exists rejected_plausibility_rows bigint not null default 0;
"""
    run(psql_cmd(psql, host, port, dbname, user), input_text=sql)


def station_year_values(target_station_years: list[tuple[str, int]]) -> str:
    return ",\n        ".join(
        f"({sql_literal(station_id)}, {int(source_year)})" for station_id, source_year in target_station_years
    )


def candidate_files_query(
    source: str,
    limit_files: int | None,
    include_loaded: bool,
    target_station_years: list[tuple[str, int]] | None = None,
) -> str:
    source_predicates = ["true"]
    if source == "downloaded":
        source_predicates.append("ranked.source_basis = 'download_attempt'")
    elif source == "inventory":
        source_predicates.append("ranked.source_basis = 'inventory'")

    target_cte = ""
    target_join = ""
    if target_station_years:
        target_cte = f"""
,
target_station_years(station_id, source_year) as (
    values
        {station_year_values(target_station_years)}
)
"""
        target_join = """
join target_station_years target
  on target.station_id = ranked.station_id
 and target.source_year = ranked.source_year
"""

    loaded_filter = ""
    if not include_loaded:
        loaded_filter = """
        and not exists (
            select 1
            from weather.noaa_hourly_load_file lf
            where lf.station_id = ranked.station_id
              and lf.source_year = ranked.source_year
              and lf.local_path = ranked.local_path
              and lf.file_status = 'loaded'
        )
        """
    limit_clause = "" if limit_files is None else f"limit {int(limit_files)}"
    return f"""
with source_files as (
    select
        station_id,
        source_year,
        raw_station_id,
        local_path,
        source_file_id,
        file_size_bytes,
        'inventory'::text as source_basis,
        2 as source_priority
    from weather.noaa_raw_file_inventory
    where file_status = 'available'
      and local_path is not null

    union all

    select
        station_id,
        source_year,
        raw_station_id,
        target_path as local_path,
        source_file_id,
        file_size_bytes,
        'download_attempt'::text as source_basis,
        1 as source_priority
    from weather.noaa_raw_download_attempt
    where download_status in ('downloaded', 'skipped_existing')
      and target_path is not null
),
ranked as (
    select distinct on (station_id, source_year, local_path)
        station_id,
        source_year,
        raw_station_id,
        local_path,
        source_file_id,
        file_size_bytes,
        source_basis,
        source_priority
    from source_files
    order by station_id, source_year, local_path, source_priority
)
{target_cte},
filtered as (
    select ranked.*
    from ranked
    {target_join}
    where {' and '.join(source_predicates)}
)
select
    ranked.station_id,
    ranked.source_year::text as source_year,
    ranked.raw_station_id,
    ranked.local_path,
    ranked.source_file_id,
    ranked.file_size_bytes::text as file_size_bytes,
    ranked.source_basis,
    coalesce(
        st.local_standard_utc_offset_hours,
        greatest(-12, least(14, round(st.longitude / 15.0)::integer)),
        0
    )::text as local_standard_utc_offset_hours
from filtered ranked
join weather.station st
  on st.station_id = ranked.station_id
where true
  {loaded_filter}
order by source_year desc, source_priority, station_id, local_path
{limit_clause}
"""


def read_target_station_years(path: Path | None, gap_cause: str | None) -> list[tuple[str, int]]:
    if path is None:
        return []
    if not path.exists():
        raise FileNotFoundError(path)
    targets: list[tuple[str, int]] = []
    seen: set[tuple[str, int]] = set()
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {"station_id", "source_year"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{path} is missing required columns: {', '.join(sorted(missing))}")
        if gap_cause and "gap_cause" not in set(reader.fieldnames or []):
            raise ValueError(f"{path} is missing gap_cause column required by --station-year-gap-cause")
        for row in reader:
            if gap_cause and row.get("gap_cause") != gap_cause:
                continue
            station_id = (row.get("station_id") or "").strip()
            source_year_text = (row.get("source_year") or "").strip()
            if not station_id or not source_year_text:
                continue
            key = (station_id, int(source_year_text))
            if key in seen:
                continue
            seen.add(key)
            targets.append(key)
    return targets


def open_text(path: Path):
    if path.name.lower().endswith(".gz"):
        return gzip.open(path, "rt", newline="", encoding="utf-8", errors="replace")
    return path.open("r", newline="", encoding="utf-8", errors="replace")


def parse_noaa_datetime(text: str) -> datetime | None:
    if not text:
        return None
    try:
        dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def canonical_hour(dt: datetime) -> datetime:
    return dt.replace(minute=0, second=0, microsecond=0)


def parse_int(value: object, default: int = 0) -> int:
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return default


def local_hour_from_utc(hour_ending_utc: datetime, offset_hours: int) -> datetime:
    return (hour_ending_utc + timedelta(hours=offset_hours)).replace(tzinfo=None)


def parse_tmp(tmp: str) -> tuple[float | None, str | None]:
    if not tmp:
        return None, None
    parts = tmp.split(",")
    if len(parts) < 2:
        return None, None
    value_text = parts[0]
    quality = parts[1]
    if value_text in {"+9999", "-9999", "9999"} or quality == "9":
        return None, quality
    try:
        return int(value_text) / 10.0, quality
    except ValueError:
        return None, quality


def parse_code_set(values: list[str] | None) -> set[str]:
    codes: set[str] = set()
    for value in values or []:
        for code in value.split(","):
            cleaned = code.strip()
            if cleaned:
                codes.add(cleaned)
    return codes


def observation_score(row: dict[str, str], dt: datetime, tmp_quality: str | None) -> tuple[int, int, int, int]:
    quality_rank = {"1": 0, "5": 1, "0": 2}.get(tmp_quality or "", 5)
    report_type = (row.get("REPORT_TYPE") or "").strip()
    report_rank = 0 if report_type.startswith("FM") else 1
    source_rank = {"4": 0, "6": 2, "7": 10}.get((row.get("SOURCE") or "").strip(), 3)
    minute_rank = abs(dt.minute - 56)
    return quality_rank, report_rank, source_rank, minute_rank


def parse_file(
    row: dict[str, str],
    run_id: str,
    reject_source_codes: set[str],
    min_temp_c: float,
    max_temp_c: float,
) -> tuple[list[dict[str, object]], dict[str, object]]:
    path = Path(row["local_path"])
    station_id = row["station_id"]
    source_year = int(row["source_year"])
    local_offset_hours = parse_int(row.get("local_standard_utc_offset_hours"), 0)
    raw_station_id = row["raw_station_id"]
    source_file_id = row.get("source_file_id") or None
    file_size_bytes = int(row["file_size_bytes"]) if row.get("file_size_bytes") else None
    load_file_id = f"{run_id}:station:{station_id}:year:{source_year}:file:{path.name}"
    stats: dict[str, object] = {
        "load_file_id": load_file_id,
        "calculation_run_id": run_id,
        "station_id": station_id,
        "source_year": source_year,
        "raw_station_id": raw_station_id,
        "local_path": str(path),
        "source_file_id": source_file_id,
        "source_basis": row["source_basis"],
        "file_size_bytes": file_size_bytes,
        "file_status": "loaded",
        "rows_seen": 0,
        "djf_rows_seen": 0,
        "rejected_source_rows": 0,
        "valid_temp_rows": 0,
        "invalid_temp_rows": 0,
        "rejected_plausibility_rows": 0,
        "duplicate_hour_count": 0,
        "loaded_hour_count": 0,
        "min_hour_ending_utc": None,
        "max_hour_ending_utc": None,
        "error_message": None,
        "notes": "DJF rows loaded from NOAA Global Hourly CSV using station-local standard-time month filtering and canonical UTC station-hours.",
    }
    best_by_hour: dict[datetime, dict[str, object]] = {}
    best_score_by_hour: dict[datetime, tuple[int, int, int, int]] = {}

    try:
        with open_text(path) as f:
            reader = csv.DictReader(f)
            for raw in reader:
                stats["rows_seen"] = int(stats["rows_seen"]) + 1
                dt = parse_noaa_datetime(raw.get("DATE", ""))
                if dt is None:
                    continue
                hour = canonical_hour(dt)
                local_hour = local_hour_from_utc(hour, local_offset_hours)
                if local_hour.month not in DJF_MONTHS:
                    continue
                stats["djf_rows_seen"] = int(stats["djf_rows_seen"]) + 1

                noaa_source = (raw.get("SOURCE") or "").strip()
                if noaa_source in reject_source_codes:
                    stats["rejected_source_rows"] = int(stats["rejected_source_rows"]) + 1
                    continue

                temp_c, tmp_quality = parse_tmp(raw.get("TMP", ""))
                if temp_c is None:
                    stats["invalid_temp_rows"] = int(stats["invalid_temp_rows"]) + 1
                    continue
                report_type = (raw.get("REPORT_TYPE") or "").strip()
                if temp_c < min_temp_c or temp_c > max_temp_c or (report_type == "SHEF" and temp_c < SHEF_MIN_TEMP_C):
                    stats["rejected_plausibility_rows"] = int(stats["rejected_plausibility_rows"]) + 1
                    continue
                stats["valid_temp_rows"] = int(stats["valid_temp_rows"]) + 1

                quality_flags = "|".join(
                    [
                        f"tmp_quality:{tmp_quality or ''}",
                        f"report_type:{report_type}",
                        f"source:{noaa_source}",
                        f"qc:{raw.get('QUALITY_CONTROL') or ''}",
                        f"local_standard_utc_offset_hours:{local_offset_hours}",
                    ]
                )
                record = {
                    "station_id": station_id,
                    "hour_ending_utc": hour.isoformat(timespec="seconds"),
                    "hour_local": local_hour.isoformat(timespec="seconds"),
                    "obs_timestamp": dt.isoformat(timespec="seconds"),
                    "dry_bulb_c": f"{temp_c:.3f}",
                    "dry_bulb_f": f"{(temp_c * 9.0 / 5.0) + 32.0:.3f}",
                    "source_file_id": source_file_id,
                    "source_channel": (
                        "noaa_global_hourly_aws"
                        if row["source_basis"] == "download_attempt"
                        else "noaa_isd_local_cache"
                    ),
                    "source_code": noaa_source,
                    "report_type": report_type,
                    "quality_flags_text": quality_flags,
                    "calculation_run_id": run_id,
                }
                score = observation_score(raw, dt, tmp_quality)
                if hour in best_by_hour:
                    stats["duplicate_hour_count"] = int(stats["duplicate_hour_count"]) + 1
                    if score >= best_score_by_hour[hour]:
                        continue
                best_by_hour[hour] = record
                best_score_by_hour[hour] = score
    except Exception as exc:
        stats["file_status"] = "failed"
        stats["error_message"] = str(exc)
        stats["notes"] = "File failed during NOAA Global Hourly DJF parsing."
        return [], stats

    loaded_rows = [best_by_hour[hour] for hour in sorted(best_by_hour)]
    stats["loaded_hour_count"] = len(loaded_rows)
    if loaded_rows:
        stats["min_hour_ending_utc"] = loaded_rows[0]["hour_ending_utc"]
        stats["max_hour_ending_utc"] = loaded_rows[-1]["hour_ending_utc"]
    return loaded_rows, stats


def render_values_insert(table: str, columns: list[str], rows: list[dict[str, object]], conflict: str) -> str:
    values = []
    for row in rows:
        values.append("(" + ", ".join(sql_literal(row.get(col)) for col in columns) + ")")
    return f"insert into {table} ({', '.join(columns)}) values\n" + ",\n".join(values) + f"\n{conflict};\n"


def build_load_sql(
    staging_dir: Path,
    run_id: str,
    code_commit: str,
    params: dict[str, object],
) -> str:
    start = utc_now().isoformat(timespec="seconds")
    hourly_cols = [
        "station_id",
        "hour_ending_utc",
        "hour_local",
        "obs_timestamp",
        "dry_bulb_c",
        "dry_bulb_f",
        "source_file_id",
        "source_channel",
        "source_code",
        "report_type",
        "quality_flags_text",
        "calculation_run_id",
    ]
    file_cols = [
        "load_file_id",
        "calculation_run_id",
        "station_id",
        "source_year",
        "raw_station_id",
        "local_path",
        "source_file_id",
        "source_basis",
        "file_size_bytes",
        "file_status",
        "rows_seen",
        "djf_rows_seen",
        "rejected_source_rows",
        "valid_temp_rows",
        "invalid_temp_rows",
        "rejected_plausibility_rows",
        "duplicate_hour_count",
        "loaded_hour_count",
        "min_hour_ending_utc",
        "max_hour_ending_utc",
        "error_message",
        "notes",
    ]
    return "\n".join(
        [
            "\\set ON_ERROR_STOP on",
            "begin;",
            render_values_insert(
                "audit.methodology_version",
                ["methodology_version", "methodology_name", "effective_at_utc", "source_standard", "notes"],
                [
                    {
                        "methodology_version": METHODOLOGY_VERSION,
                        "methodology_name": "EOP012 ECWT national calculation methodology",
                        "effective_at_utc": start,
                        "source_standard": "NERC EOP-012-3; EPRI 3002030362 guidance",
                        "notes": "Initial auditable methodology version for asset loading, station matching, raw file inventory, coverage auditing, NOAA DJF hourly loading, and ECWT calculation.",
                    }
                ],
                "on conflict (methodology_version) do update set notes = excluded.notes",
            ),
            f"""
insert into audit.calculation_run (
    calculation_run_id,
    methodology_version,
    code_commit,
    run_started_at_utc,
    run_finished_at_utc,
    run_status,
    parameters_json,
    notes
) values (
    {sql_literal(run_id)},
    {sql_literal(METHODOLOGY_VERSION)},
    {sql_literal(code_commit)},
    {sql_literal(start)},
    now(),
    'succeeded',
    {sql_literal(json.dumps(params, sort_keys=True))}::jsonb,
    'Loaded NOAA Global Hourly DJF observations into weather.hourly_djf.'
)
on conflict (calculation_run_id) do update set
    run_finished_at_utc = excluded.run_finished_at_utc,
    run_status = excluded.run_status,
    parameters_json = excluded.parameters_json,
    notes = excluded.notes;
""",
            """
create temp table stg_hourly_djf (
    station_id text,
    hour_ending_utc timestamptz,
    hour_local timestamp,
    obs_timestamp timestamptz,
    dry_bulb_c numeric,
    dry_bulb_f numeric,
    source_file_id text,
    source_channel weather.source_channel,
    source_code text,
    report_type text,
    quality_flags_text text,
    calculation_run_id text
) on commit drop;
""",
            copy_command("stg_hourly_djf", hourly_cols, staging_dir / "hourly_djf.csv"),
            """
create temp table stg_hourly_rebuild_audit as
select
    staged.station_id,
    staged.hour_ending_utc,
    existing.station_id is null as needs_insert,
    existing.station_id is not null
      and existing.hour_local is distinct from staged.hour_local as needs_hour_local_update,
    existing.station_id is not null
      and (
          existing.dry_bulb_c is distinct from staged.dry_bulb_c
          or existing.dry_bulb_f is distinct from staged.dry_bulb_f
      ) as payload_differs,
    existing.station_id is not null
      and (
          existing.source_file_id is distinct from staged.source_file_id
          or existing.obs_timestamp is distinct from staged.obs_timestamp
          or existing.source_channel is distinct from staged.source_channel
          or existing.source_code is distinct from staged.source_code
          or existing.report_type is distinct from staged.report_type
          or existing.quality_flags is distinct from array_remove(string_to_array(staged.quality_flags_text, '|'), '')
      ) as metadata_differs
from stg_hourly_djf staged
left join weather.hourly_djf existing
  on existing.station_id = staged.station_id
 and existing.hour_ending_utc = staged.hour_ending_utc;
""",
            f"""
update audit.calculation_run
set parameters_json = parameters_json || jsonb_build_object(
    'hourly_needs_insert_count', (select count(*) from stg_hourly_rebuild_audit where needs_insert),
    'hourly_needs_hour_local_update_count', (select count(*) from stg_hourly_rebuild_audit where needs_hour_local_update),
    'hourly_existing_payload_diff_count', (select count(*) from stg_hourly_rebuild_audit where payload_differs),
    'hourly_existing_metadata_diff_count', (select count(*) from stg_hourly_rebuild_audit where metadata_differs)
)
where calculation_run_id = {sql_literal(run_id)};
""",
            """
insert into weather.hourly_djf (
    station_id,
    hour_ending_utc,
    hour_local,
    obs_timestamp,
    dry_bulb_c,
    dry_bulb_f,
    source_file_id,
    source_channel,
    source_code,
    report_type,
    quality_flags,
    calculation_run_id
)
select
    staged.station_id,
    staged.hour_ending_utc,
    staged.hour_local,
    staged.obs_timestamp,
    staged.dry_bulb_c,
    staged.dry_bulb_f,
    staged.source_file_id,
    staged.source_channel,
    staged.source_code,
    staged.report_type,
    array_remove(string_to_array(staged.quality_flags_text, '|'), ''),
    staged.calculation_run_id
from stg_hourly_djf staged
join stg_hourly_rebuild_audit audit
  on audit.station_id = staged.station_id
 and audit.hour_ending_utc = staged.hour_ending_utc
where audit.needs_insert
on conflict (station_id, hour_ending_utc) do nothing;
""",
            """
update weather.hourly_djf existing
set
    hour_local = staged.hour_local,
    obs_timestamp = staged.obs_timestamp,
    dry_bulb_c = staged.dry_bulb_c,
    dry_bulb_f = staged.dry_bulb_f,
    source_file_id = staged.source_file_id,
    source_channel = staged.source_channel,
    source_code = staged.source_code,
    report_type = staged.report_type,
    quality_flags = array_remove(string_to_array(staged.quality_flags_text, '|'), ''),
    calculation_run_id = staged.calculation_run_id
from stg_hourly_djf staged
join stg_hourly_rebuild_audit audit
  on audit.station_id = staged.station_id
 and audit.hour_ending_utc = staged.hour_ending_utc
where existing.station_id = staged.station_id
  and existing.hour_ending_utc = staged.hour_ending_utc
  and (audit.payload_differs or audit.metadata_differs);
""",
            """
create temp table stg_noaa_hourly_load_file (
    load_file_id text,
    calculation_run_id text,
    station_id text,
    source_year integer,
    raw_station_id text,
    local_path text,
    source_file_id text,
    source_basis text,
    file_size_bytes bigint,
    file_status text,
    rows_seen bigint,
    djf_rows_seen bigint,
    rejected_source_rows bigint,
    valid_temp_rows bigint,
    invalid_temp_rows bigint,
    rejected_plausibility_rows bigint,
    duplicate_hour_count bigint,
    loaded_hour_count bigint,
    min_hour_ending_utc timestamptz,
    max_hour_ending_utc timestamptz,
    error_message text,
    notes text
) on commit drop;
""",
            copy_command("stg_noaa_hourly_load_file", file_cols, staging_dir / "noaa_hourly_load_file.csv"),
            """
insert into weather.noaa_hourly_load_file (
    load_file_id,
    calculation_run_id,
    station_id,
    source_year,
    raw_station_id,
    local_path,
    source_file_id,
    source_basis,
    file_size_bytes,
    file_status,
    rows_seen,
    djf_rows_seen,
    rejected_source_rows,
    valid_temp_rows,
    invalid_temp_rows,
    rejected_plausibility_rows,
    duplicate_hour_count,
    loaded_hour_count,
    min_hour_ending_utc,
    max_hour_ending_utc,
    error_message,
    notes
)
select
    load_file_id,
    calculation_run_id,
    station_id,
    source_year,
    raw_station_id,
    local_path,
    source_file_id,
    source_basis,
    file_size_bytes,
    file_status,
    rows_seen,
    djf_rows_seen,
    rejected_source_rows,
    valid_temp_rows,
    invalid_temp_rows,
    rejected_plausibility_rows,
    duplicate_hour_count,
    loaded_hour_count,
    min_hour_ending_utc,
    max_hour_ending_utc,
    error_message,
    notes
from stg_noaa_hourly_load_file
on conflict (station_id, source_year, local_path) do update set
    calculation_run_id = excluded.calculation_run_id,
    raw_station_id = excluded.raw_station_id,
    source_file_id = excluded.source_file_id,
    source_basis = excluded.source_basis,
    file_size_bytes = excluded.file_size_bytes,
    file_status = excluded.file_status,
    rows_seen = excluded.rows_seen,
    djf_rows_seen = excluded.djf_rows_seen,
    rejected_source_rows = excluded.rejected_source_rows,
    valid_temp_rows = excluded.valid_temp_rows,
    invalid_temp_rows = excluded.invalid_temp_rows,
    rejected_plausibility_rows = excluded.rejected_plausibility_rows,
    duplicate_hour_count = excluded.duplicate_hour_count,
    loaded_hour_count = excluded.loaded_hour_count,
    min_hour_ending_utc = excluded.min_hour_ending_utc,
    max_hour_ending_utc = excluded.max_hour_ending_utc,
    error_message = excluded.error_message,
    notes = excluded.notes;
""",
            "" if params.get("skip_summary_refresh") else """
create temp table stg_touched_station_year as
select distinct
    station_id,
    extract(year from hour_local)::integer as source_year
from stg_hourly_djf
where hour_local is not null
union
select distinct station_id, source_year
from stg_noaa_hourly_load_file
where file_status = 'loaded';
""",
            "" if params.get("skip_summary_refresh") else """
insert into weather.station_year_hourly_summary (
    station_id,
    source_year,
    valid_djf_hours,
    min_hour_ending_utc,
    max_hour_ending_utc,
    refreshed_at_utc,
    source_basis
)
select
    touched.station_id,
    touched.source_year,
    count(hourly.hour_ending_utc)::bigint as valid_djf_hours,
    min(hourly.hour_ending_utc) as min_hour_ending_utc,
    max(hourly.hour_ending_utc) as max_hour_ending_utc,
    now() as refreshed_at_utc,
    'weather.hourly_djf canonical station-local DJF rows refreshed by load_noaa_hourly_djf.py' as source_basis
from stg_touched_station_year touched
join weather.station station
  on station.station_id = touched.station_id
left join weather.hourly_djf hourly
  on hourly.station_id = touched.station_id
 and (
      (
          hourly.hour_ending_utc >= (
              make_timestamp(touched.source_year, 1, 1, 0, 0, 0)
              - make_interval(hours => coalesce(station.local_standard_utc_offset_hours, 0))
          ) at time zone 'UTC'
          and hourly.hour_ending_utc < (
              make_timestamp(touched.source_year, 3, 1, 0, 0, 0)
              - make_interval(hours => coalesce(station.local_standard_utc_offset_hours, 0))
          ) at time zone 'UTC'
      )
      or (
          hourly.hour_ending_utc >= (
              make_timestamp(touched.source_year, 12, 1, 0, 0, 0)
              - make_interval(hours => coalesce(station.local_standard_utc_offset_hours, 0))
          ) at time zone 'UTC'
          and hourly.hour_ending_utc < (
              make_timestamp(touched.source_year + 1, 1, 1, 0, 0, 0)
              - make_interval(hours => coalesce(station.local_standard_utc_offset_hours, 0))
          ) at time zone 'UTC'
      )
 )
group by touched.station_id, touched.source_year
on conflict (station_id, source_year) do update set
    valid_djf_hours = excluded.valid_djf_hours,
    min_hour_ending_utc = excluded.min_hour_ending_utc,
    max_hour_ending_utc = excluded.max_hour_ending_utc,
    refreshed_at_utc = excluded.refreshed_at_utc,
    source_basis = excluded.source_basis;
""",
            "commit;",
        ]
    )


def report_counts(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    run_id: str,
    exact_db_counts: bool,
) -> OrderedDict[str, str]:
    queries = OrderedDict()
    if exact_db_counts:
        queries["weather.hourly_djf total"] = "select count(*) from weather.hourly_djf;"
        queries["weather.hourly_djf rows for this run"] = (
            f"select count(*) from weather.hourly_djf where calculation_run_id = {sql_literal(run_id)};"
        )
    else:
        queries["weather.hourly_djf estimated total"] = (
            "select coalesce(reltuples::bigint, 0) from pg_class where oid = 'weather.hourly_djf'::regclass;"
        )
        queries["weather.hourly_djf rows for this run (file audit)"] = (
            f"select coalesce(sum(loaded_hour_count),0) from weather.noaa_hourly_load_file "
            f"where calculation_run_id = {sql_literal(run_id)};"
        )
    queries.update(
        OrderedDict(
            [
                (
                    "loaded files for this run",
                    f"select count(*) from weather.noaa_hourly_load_file where calculation_run_id = {sql_literal(run_id)} and file_status = 'loaded';",
                ),
                (
                    "failed files for this run",
                    f"select count(*) from weather.noaa_hourly_load_file where calculation_run_id = {sql_literal(run_id)} and file_status = 'failed';",
                ),
                (
                    "loaded hour count for this run",
                    f"select coalesce(sum(loaded_hour_count),0) from weather.noaa_hourly_load_file where calculation_run_id = {sql_literal(run_id)};",
                ),
                (
                    "invalid temp rows for this run",
                    f"select coalesce(sum(invalid_temp_rows),0) from weather.noaa_hourly_load_file where calculation_run_id = {sql_literal(run_id)};",
                ),
                (
                    "rejected source rows for this run",
                    f"select coalesce(sum(rejected_source_rows),0) from weather.noaa_hourly_load_file where calculation_run_id = {sql_literal(run_id)};",
                ),
                (
                    "rejected plausibility rows for this run",
                    f"select coalesce(sum(rejected_plausibility_rows),0) from weather.noaa_hourly_load_file where calculation_run_id = {sql_literal(run_id)};",
                ),
                (
                    "duplicate hour count for this run",
                    f"select coalesce(sum(duplicate_hour_count),0) from weather.noaa_hourly_load_file where calculation_run_id = {sql_literal(run_id)};",
                ),
                ("audit.calculation_run", "select count(*) from audit.calculation_run;"),
            ]
        )
    )
    results: OrderedDict[str, str] = OrderedDict()
    for label, query in queries.items():
        results[label] = psql_scalar(psql, host, port, dbname, query, user)
    return results


def render_report(
    path: Path,
    run_id: str,
    code_commit: str,
    params: dict[str, object],
    file_rows: list[dict[str, str]],
    file_stats: list[dict[str, object]],
    hourly_rows_count: int,
    db_counts: OrderedDict[str, str],
    host: str,
    port: int,
    dbname: str,
) -> None:
    loaded_files = sum(1 for row in file_stats if row["file_status"] == "loaded")
    failed_files = sum(1 for row in file_stats if row["file_status"] == "failed")
    total_bytes = sum(int(row.get("file_size_bytes") or 0) for row in file_stats)
    total_seen = sum(int(row["rows_seen"]) for row in file_stats)
    total_djf_seen = sum(int(row["djf_rows_seen"]) for row in file_stats)
    total_rejected_source = sum(int(row["rejected_source_rows"]) for row in file_stats)
    total_valid = sum(int(row["valid_temp_rows"]) for row in file_stats)
    total_invalid = sum(int(row["invalid_temp_rows"]) for row in file_stats)
    total_rejected_plausibility = sum(int(row["rejected_plausibility_rows"]) for row in file_stats)
    total_dupes = sum(int(row["duplicate_hour_count"]) for row in file_stats)
    years = sorted({int(row["source_year"]) for row in file_rows})
    lines = [
        "# NOAA DJF Hourly Load Report",
        "",
        f"Generated UTC: {utc_now().isoformat(timespec='seconds')}",
        "",
        "## Database",
        "",
        f"- Host: `{host}`",
        f"- Port: `{port}`",
        f"- Database: `{dbname}`",
        "",
        "## Run",
        "",
        f"- Calculation run ID: `{run_id}`",
        f"- Methodology version: `{METHODOLOGY_VERSION}`",
        f"- Code commit: `{code_commit}`",
        f"- Source selector: `{params['source']}`",
        f"- Limit files: `{params['limit_files']}`",
        f"- Rejected NOAA source codes: `{params['reject_source_codes']}`",
        f"- Plausible temperature range C: `{params['min_temp_c']}` to `{params['max_temp_c']}`",
        f"- Timestamp policy: `{params['timestamp_policy']}`",
        f"- Years represented: `{years[0] if years else None}-{years[-1] if years else None}`",
        "",
        "## Results",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| Candidate files selected | {len(file_rows)} |",
        f"| Loaded files | {loaded_files} |",
        f"| Failed files | {failed_files} |",
        f"| Source bytes parsed | {total_bytes} |",
        f"| Raw rows seen | {total_seen} |",
        f"| DJF rows seen | {total_djf_seen} |",
        f"| Rejected source-code rows | {total_rejected_source} |",
        f"| Valid DJF temperature rows | {total_valid} |",
        f"| Invalid DJF temperature rows | {total_invalid} |",
        f"| Rejected plausibility rows | {total_rejected_plausibility} |",
        f"| Duplicate station-hour observations | {total_dupes} |",
        f"| Canonical hourly rows staged | {hourly_rows_count} |",
        "",
        "## Database Row Counts",
        "",
        "| Relation or Check | Rows / Value |",
        "| --- | ---: |",
    ]
    for label, count in db_counts.items():
        lines.append(f"| `{label}` | {count} |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- This loader populates `weather.hourly_djf`, not the final ECWT tables.",
            "- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.",
            "- Configured rejected NOAA source codes are excluded before TMP interpretation.",
            "- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.",
            "- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.",
            "- The timestamp policy for this run is: DJF month filtering uses station-local standard time derived from station longitude; canonical storage remains UTC.",
            "- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.",
        ]
    )
    if not file_rows:
        lines.append("- No candidate files were selected, so this run is an auditable no-op and loaded zero weather rows.")
    lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--staging-root", type=Path, default=DEFAULT_STAGING_ROOT)
    parser.add_argument("--psql", type=Path, default=PSQL)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5436)
    parser.add_argument("--dbname", default="eop012")
    parser.add_argument("--user", default=None)
    parser.add_argument("--source", choices=["all", "downloaded", "inventory"], default="all")
    parser.add_argument("--limit-files", type=int, default=25)
    parser.add_argument("--include-loaded", action="store_true")
    parser.add_argument(
        "--station-year-csv",
        type=Path,
        help="Optional CSV with station_id and source_year columns used to restrict candidate files.",
    )
    parser.add_argument(
        "--station-year-gap-cause",
        help="Optional gap_cause value used to filter --station-year-csv rows before loading.",
    )
    parser.add_argument(
        "--reject-source-code",
        action="append",
        default=["7"],
        help="NOAA SOURCE code to reject before TMP interpretation. Repeat or pass comma-separated values.",
    )
    parser.add_argument("--min-temp-c", type=float, default=-65.0)
    parser.add_argument("--max-temp-c", type=float, default=40.0)
    parser.add_argument(
        "--exact-db-counts",
        action="store_true",
        help="Run expensive exact weather.hourly_djf count(*) validations in the report.",
    )
    parser.add_argument(
        "--skip-summary-refresh",
        action="store_true",
        help="Defer weather.station_year_hourly_summary refresh; useful for bulk reloads that run a full summary backfill afterward.",
    )
    args = parser.parse_args()

    if not args.psql.exists():
        raise FileNotFoundError(args.psql)
    if args.min_temp_c >= args.max_temp_c:
        raise ValueError("--min-temp-c must be lower than --max-temp-c")

    ensure_load_schema(args.psql, args.host, args.port, args.dbname, args.user)
    reject_source_codes = parse_code_set(args.reject_source_code)
    target_station_years = read_target_station_years(args.station_year_csv, args.station_year_gap_cause)

    code_commit = git_commit_label(args.project_root)
    run_timestamp = utc_now().strftime("%Y%m%dT%H%M%S%fZ")
    run_id = f"noaa_hourly_djf_load_{run_timestamp}"
    staging_dir = args.staging_root / run_id
    staging_dir.mkdir(parents=True, exist_ok=True)

    file_rows = psql_csv_query(
        args.psql,
        args.host,
        args.port,
        args.dbname,
        candidate_files_query(args.source, args.limit_files, args.include_loaded, target_station_years),
        args.user,
    )

    hourly_rows: list[dict[str, object]] = []
    file_stats: list[dict[str, object]] = []
    for row in file_rows:
        parsed_rows, stats = parse_file(row, run_id, reject_source_codes, args.min_temp_c, args.max_temp_c)
        hourly_rows.extend(parsed_rows)
        file_stats.append(stats)

    hourly_cols = [
        "station_id",
        "hour_ending_utc",
        "hour_local",
        "dry_bulb_c",
        "dry_bulb_f",
        "source_file_id",
        "quality_flags_text",
        "calculation_run_id",
    ]
    file_cols = [
        "load_file_id",
        "calculation_run_id",
        "station_id",
        "source_year",
        "raw_station_id",
        "local_path",
        "source_file_id",
        "source_basis",
        "file_size_bytes",
        "file_status",
        "rows_seen",
        "djf_rows_seen",
        "rejected_source_rows",
        "valid_temp_rows",
        "invalid_temp_rows",
        "rejected_plausibility_rows",
        "duplicate_hour_count",
        "loaded_hour_count",
        "min_hour_ending_utc",
        "max_hour_ending_utc",
        "error_message",
        "notes",
    ]
    write_csv(staging_dir / "hourly_djf.csv", hourly_cols, hourly_rows)
    write_csv(staging_dir / "noaa_hourly_load_file.csv", file_cols, file_stats)

    params = {
        "source_family": SOURCE_FAMILY,
        "source": args.source,
        "limit_files": args.limit_files,
        "include_loaded": args.include_loaded,
        "station_year_csv": str(args.station_year_csv) if args.station_year_csv else None,
        "station_year_gap_cause": args.station_year_gap_cause,
        "target_station_year_count": len(target_station_years),
        "reject_source_codes": sorted(reject_source_codes),
        "min_temp_c": args.min_temp_c,
        "max_temp_c": args.max_temp_c,
        "file_count": len(file_rows),
        "hourly_rows_staged": len(hourly_rows),
        "skip_summary_refresh": args.skip_summary_refresh,
        "tmp_units": "NOAA TMP tenths of degrees C converted to C and F",
        "timestamp_policy": (
            "DJF month filtering uses station-local standard time derived from weather.station.local_standard_utc_offset_hours; "
            "canonical hour_ending_utc remains the NOAA observation timestamp floored to the UTC hour"
        ),
        "no_candidate_files_selected": not bool(file_rows),
    }
    load_sql = build_load_sql(staging_dir, run_id, code_commit, params)
    sql_path = staging_dir / "load.sql"
    sql_path.write_text(load_sql, encoding="utf-8")
    run(psql_cmd(args.psql, args.host, args.port, args.dbname, args.user) + ["-f", str(sql_path)])

    db_counts = report_counts(
        args.psql,
        args.host,
        args.port,
        args.dbname,
        args.user,
        run_id,
        args.exact_db_counts,
    )
    report_path = args.project_root / "docs" / f"{run_id}_report.md"
    render_report(
        report_path,
        run_id,
        code_commit,
        params,
        file_rows,
        file_stats,
        len(hourly_rows),
        db_counts,
        args.host,
        args.port,
        args.dbname,
    )

    print(
        json.dumps(
            {
                "run_id": run_id,
                "staging_dir": str(staging_dir),
                "report_path": str(report_path),
                "files_selected": len(file_rows),
                "hourly_rows_staged": len(hourly_rows),
                "loaded_files": sum(1 for row in file_stats if row["file_status"] == "loaded"),
                "failed_files": sum(1 for row in file_stats if row["file_status"] == "failed"),
                "db_counts": db_counts,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
