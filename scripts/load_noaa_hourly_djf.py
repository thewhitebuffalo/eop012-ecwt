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
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from eop012_config import PROJECT_ROOT, PSQL, STAGING_ROOT

DEFAULT_STAGING_ROOT = STAGING_ROOT

METHODOLOGY_VERSION = "eop012-ecwt-method-v0.1.0"
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
        writer = csv.DictWriter(f, fieldnames=fieldnames)
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
alter table weather.noaa_hourly_load_file
    add column if not exists rejected_source_rows bigint not null default 0;
alter table weather.noaa_hourly_load_file
    add column if not exists rejected_plausibility_rows bigint not null default 0;
"""
    run(psql_cmd(psql, host, port, dbname, user), input_text=sql)


def candidate_files_query(source: str, limit_files: int | None, include_loaded: bool) -> str:
    source_filter = ""
    if source == "downloaded":
        source_filter = "where source_basis = 'download_attempt'"
    elif source == "inventory":
        source_filter = "where source_basis = 'inventory'"

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
),
filtered as (
    select *
    from ranked
    {source_filter}
)
select
    station_id,
    source_year::text as source_year,
    raw_station_id,
    local_path,
    source_file_id,
    file_size_bytes::text as file_size_bytes,
    source_basis
from filtered ranked
where true
  {loaded_filter}
order by source_year desc, source_priority, station_id, local_path
{limit_clause}
"""


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
        "notes": "DJF rows loaded from NOAA Global Hourly CSV using canonical hour = observation timestamp floored to the UTC hour.",
    }
    best_by_hour: dict[datetime, dict[str, object]] = {}
    best_score_by_hour: dict[datetime, tuple[int, int, int, int]] = {}

    try:
        with open_text(path) as f:
            reader = csv.DictReader(f)
            for raw in reader:
                stats["rows_seen"] = int(stats["rows_seen"]) + 1
                dt = parse_noaa_datetime(raw.get("DATE", ""))
                if dt is None or dt.month not in DJF_MONTHS:
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

                hour = canonical_hour(dt)
                quality_flags = "|".join(
                    [
                        f"tmp_quality:{tmp_quality or ''}",
                        f"report_type:{report_type}",
                        f"source:{noaa_source}",
                        f"qc:{raw.get('QUALITY_CONTROL') or ''}",
                    ]
                )
                record = {
                    "station_id": station_id,
                    "hour_ending_utc": hour.isoformat(timespec="seconds"),
                    "hour_local": None,
                    "dry_bulb_c": f"{temp_c:.3f}",
                    "dry_bulb_f": f"{(temp_c * 9.0 / 5.0) + 32.0:.3f}",
                    "source_file_id": source_file_id,
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
    dry_bulb_c numeric,
    dry_bulb_f numeric,
    source_file_id text,
    quality_flags_text text,
    calculation_run_id text
) on commit drop;
""",
            copy_command("stg_hourly_djf", hourly_cols, staging_dir / "hourly_djf.csv"),
            """
insert into weather.hourly_djf (
    station_id,
    hour_ending_utc,
    hour_local,
    dry_bulb_c,
    dry_bulb_f,
    source_file_id,
    quality_flags,
    calculation_run_id
)
select
    station_id,
    hour_ending_utc,
    hour_local,
    dry_bulb_c,
    dry_bulb_f,
    source_file_id,
    array_remove(string_to_array(quality_flags_text, '|'), ''),
    calculation_run_id
from stg_hourly_djf
on conflict (station_id, hour_ending_utc) do update set
    hour_local = excluded.hour_local,
    dry_bulb_c = excluded.dry_bulb_c,
    dry_bulb_f = excluded.dry_bulb_f,
    source_file_id = excluded.source_file_id,
    quality_flags = excluded.quality_flags,
    calculation_run_id = excluded.calculation_run_id;
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
            "- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.",
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
    args = parser.parse_args()

    if not args.psql.exists():
        raise FileNotFoundError(args.psql)
    if args.min_temp_c >= args.max_temp_c:
        raise ValueError("--min-temp-c must be lower than --max-temp-c")

    ensure_load_schema(args.psql, args.host, args.port, args.dbname, args.user)
    reject_source_codes = parse_code_set(args.reject_source_code)

    code_commit = git_commit_label(args.project_root)
    run_timestamp = utc_now().strftime("%Y%m%dT%H%M%SZ")
    run_id = f"noaa_hourly_djf_load_{run_timestamp}"
    staging_dir = args.staging_root / run_id
    staging_dir.mkdir(parents=True, exist_ok=True)

    file_rows = psql_csv_query(
        args.psql,
        args.host,
        args.port,
        args.dbname,
        candidate_files_query(args.source, args.limit_files, args.include_loaded),
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
        "reject_source_codes": sorted(reject_source_codes),
        "min_temp_c": args.min_temp_c,
        "max_temp_c": args.max_temp_c,
        "file_count": len(file_rows),
        "hourly_rows_staged": len(hourly_rows),
        "tmp_units": "NOAA TMP tenths of degrees C converted to C and F",
        "timestamp_policy": "canonical hour = NOAA observation timestamp floored to UTC hour",
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
