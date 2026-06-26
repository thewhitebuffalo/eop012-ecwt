#!/usr/bin/env python3
"""Audit station-year root causes for near-threshold normalized coverage blockers."""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
import subprocess
from collections import Counter, OrderedDict, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from eop012_config import PROJECT_ROOT, PSQL


METHODOLOGY_VERSION = "eop012-ecwt-method-v0.2.0"
DEFAULT_MAX_GAP_HOURS = 168

STATION_YEAR_FIELDS = [
    "gap_audit_run_id",
    "priority_run_id",
    "coverage_run_id",
    "inventory_run_id",
    "station_id",
    "station_name",
    "station_state",
    "station_country",
    "source_year",
    "impacted_plant_count",
    "priority_buckets",
    "min_priority_rank",
    "max_priority_rank",
    "min_plant_gap_hours",
    "max_plant_gap_hours",
    "station_gap_to_threshold",
    "normalized_expected_djf_hours",
    "valid_djf_hours",
    "missing_to_normalized_expected_hours",
    "coverage_ratio",
    "coverage_status",
    "loaded_file_count",
    "invalid_temp_row_count",
    "rejected_source_row_count",
    "rejected_plausibility_row_count",
    "duplicate_hour_count",
    "raw_file_status",
    "raw_file_path",
    "raw_file_size_bytes",
    "latest_download_status",
    "latest_http_status",
    "latest_download_run_id",
    "latest_download_error",
    "notes",
]

STATION_SUMMARY_FIELDS = [
    "gap_audit_run_id",
    "priority_run_id",
    "coverage_run_id",
    "inventory_run_id",
    "station_id",
    "station_name",
    "station_state",
    "station_country",
    "impacted_plant_count",
    "priority_buckets",
    "min_plant_gap_hours",
    "max_plant_gap_hours",
    "station_gap_to_threshold",
    "normalized_expected_djf_hours",
    "normalized_valid_djf_hours",
    "missing_to_normalized_expected_hours",
    "missing_station_year_count",
    "raw_file_missing_year_count",
    "partial_coverage_year_count",
    "empty_coverage_year_count",
    "latest_aws_404_year_count",
    "latest_retryable_failure_year_count",
    "invalid_temp_row_count",
    "rejected_source_row_count",
    "rejected_plausibility_row_count",
    "duplicate_hour_count",
    "top_missing_years",
    "top_plant_states",
]


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def sql_literal(value: object) -> str:
    if value is None:
        return "null"
    return "'" + str(value).replace("'", "''") + "'"


def sql_list(values: list[object]) -> str:
    return ", ".join(sql_literal(value) for value in values)


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


def psql_cmd(psql: Path, host: str, port: int, dbname: str, user: str | None) -> list[str]:
    cmd = [str(psql), "-h", host, "-p", str(port)]
    if user:
        cmd.extend(["-U", user])
    cmd.extend(["-d", dbname, "-v", "ON_ERROR_STOP=1"])
    return cmd


def psql_scalar(psql: Path, host: str, port: int, dbname: str, user: str | None, query: str) -> str:
    result = run(psql_cmd(psql, host, port, dbname, user) + ["-At", "-c", query])
    return result.stdout.strip()


def psql_csv_query(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    query: str,
) -> list[dict[str, str]]:
    result = run(
        psql_cmd(psql, host, port, dbname, user)
        + ["-c", f"\\copy ({query}) to stdout with (format csv, header true)"]
    )
    return list(csv.DictReader(result.stdout.splitlines()))


def git_commit_label(project_root: Path) -> str:
    try:
        return run(["git", "-C", str(project_root), "rev-parse", "HEAD"]).stdout.strip()
    except Exception:
        return "UNCOMMITTED_WORKTREE"


def latest_run_id(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    prefix: str,
) -> str:
    run_id = psql_scalar(
        psql,
        host,
        port,
        dbname,
        user,
        f"""
        select calculation_run_id
        from audit.calculation_run
        where calculation_run_id like {sql_literal(prefix + '%')}
          and run_status = 'succeeded'
        order by run_started_at_utc desc
        limit 1
        """,
    )
    if not run_id:
        raise RuntimeError(f"No succeeded calculation run found with prefix {prefix!r}.")
    return run_id


def to_int(value: object) -> int | None:
    if value is None or value == "":
        return None
    return int(float(str(value)))


def to_float(value: object) -> float | None:
    if value is None or value == "":
        return None
    return float(str(value))


def fmt_float(value: float | None, digits: int = 6) -> str:
    if value is None:
        return ""
    return f"{value:.{digits}f}"


def parse_ts(value: str | None) -> datetime | None:
    if not value:
        return None
    text = value.strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def overlap_hours(start: datetime | None, end: datetime | None, left: datetime, right: datetime) -> int:
    if start is None or end is None:
        return 0
    lo = max(start, left)
    hi = min(end, right)
    if hi <= lo:
        return 0
    return int((hi - lo).total_seconds() // 3600)


def normalized_expected_hours(row: dict[str, str], source_year: int) -> int:
    start = parse_ts(row.get("normalized_active_first_utc"))
    end = parse_ts(row.get("normalized_active_last_utc"))
    if start is None or end is None:
        return 0
    jan_start = datetime(source_year, 1, 1, tzinfo=timezone.utc)
    mar_start = datetime(source_year, 3, 1, tzinfo=timezone.utc)
    dec_start = datetime(source_year, 12, 1, tzinfo=timezone.utc)
    next_jan = datetime(source_year + 1, 1, 1, tzinfo=timezone.utc)
    return overlap_hours(start, end, jan_start, mar_start) + overlap_hours(start, end, dec_start, next_jan)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: "" if row.get(field) is None else row.get(field, "") for field in fieldnames})


def fetch_priority_rows(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    priority_run_id: str,
    max_gap_hours: int,
) -> list[dict[str, str]]:
    return psql_csv_query(
        psql,
        host,
        port,
        dbname,
        user,
        f"""
        select
            p.*,
            coalesce(st.station_name, p.best_station_name) as station_name,
            coalesce(st.state, p.best_station_state) as station_state,
            coalesce(st.country, p.best_station_country) as station_country
        from calc.coverage_blocker_priority p
        left join weather.station st
          on st.station_id = p.best_station_id
        where p.priority_run_id = {sql_literal(priority_run_id)}
          and p.valid_hour_gap_to_threshold <= {max_gap_hours}
        order by p.priority_rank
        """,
    )


def fetch_coverage_rows(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    coverage_run_id: str,
    station_ids: list[str],
) -> dict[tuple[str, int], dict[str, str]]:
    rows = psql_csv_query(
        psql,
        host,
        port,
        dbname,
        user,
        f"""
        select *
        from weather.station_year_djf_coverage
        where calculation_run_id = {sql_literal(coverage_run_id)}
          and station_id in ({sql_list(station_ids)})
        """,
    )
    return {(row["station_id"], int(row["source_year"])): row for row in rows}


def fetch_inventory_rows(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    inventory_run_id: str,
    station_ids: list[str],
) -> dict[tuple[str, int], dict[str, str]]:
    rows = psql_csv_query(
        psql,
        host,
        port,
        dbname,
        user,
        f"""
        select *
        from weather.noaa_raw_file_inventory
        where calculation_run_id = {sql_literal(inventory_run_id)}
          and station_id in ({sql_list(station_ids)})
        """,
    )
    return {(row["station_id"], int(row["source_year"])): row for row in rows}


def fetch_latest_attempt_rows(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    station_ids: list[str],
) -> dict[tuple[str, int], dict[str, str]]:
    rows = psql_csv_query(
        psql,
        host,
        port,
        dbname,
        user,
        f"""
        select distinct on (station_id, source_year)
            station_id,
            source_year,
            calculation_run_id,
            http_status::text as http_status,
            download_status,
            error_message
        from weather.noaa_raw_download_attempt
        where station_id in ({sql_list(station_ids)})
        order by station_id, source_year, attempted_at_utc desc
        """,
    )
    return {(row["station_id"], int(row["source_year"])): row for row in rows}


def year_range(priority_rows: list[dict[str, str]]) -> range:
    years: list[int] = []
    for row in priority_rows:
        for field in ("first_loaded_year", "last_loaded_year"):
            value = to_int(row.get(field))
            if value is not None:
                years.append(value)
    if not years:
        return range(2000, 2026)
    return range(max(min(years), 1900), min(max(years), 2100) + 1)


def summarize_station_priority_rows(rows: list[dict[str, str]]) -> dict[str, object]:
    gaps = [to_int(row.get("valid_hour_gap_to_threshold")) for row in rows]
    gaps = [gap for gap in gaps if gap is not None]
    ranks = [to_int(row.get("priority_rank")) for row in rows]
    ranks = [rank for rank in ranks if rank is not None]
    buckets = Counter(row.get("priority_bucket", "") for row in rows)
    station_gap = max(gaps) if gaps else None
    return {
        "impacted_plant_count": len(rows),
        "priority_buckets": ";".join(f"{bucket}:{count}" for bucket, count in buckets.most_common() if bucket),
        "min_priority_rank": min(ranks) if ranks else "",
        "max_priority_rank": max(ranks) if ranks else "",
        "min_plant_gap_hours": min(gaps) if gaps else "",
        "max_plant_gap_hours": max(gaps) if gaps else "",
        "station_gap_to_threshold": station_gap if station_gap is not None else "",
    }


def build_station_year_rows(
    run_id: str,
    priority_run_id: str,
    coverage_run_id: str,
    inventory_run_id: str,
    priority_rows: list[dict[str, str]],
    coverage: dict[tuple[str, int], dict[str, str]],
    inventory: dict[tuple[str, int], dict[str, str]],
    attempts: dict[tuple[str, int], dict[str, str]],
) -> list[dict[str, object]]:
    by_station: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in priority_rows:
        station_id = row.get("best_station_id")
        if station_id:
            by_station[station_id].append(row)
    rows: list[dict[str, object]] = []
    for station_id, group in by_station.items():
        station_meta = group[0]
        summary = summarize_station_priority_rows(group)
        for source_year in year_range(group):
            expected_values = [normalized_expected_hours(row, source_year) for row in group]
            expected = max(expected_values) if expected_values else 0
            if expected <= 0:
                continue
            cov = coverage.get((station_id, source_year), {})
            valid = to_int(cov.get("valid_djf_hours")) or 0
            missing_to_expected = max(expected - valid, 0)
            if missing_to_expected <= 0:
                continue
            inv = inventory.get((station_id, source_year), {})
            attempt = attempts.get((station_id, source_year), {})
            coverage_ratio = valid / expected if expected else None
            rows.append(
                {
                    "gap_audit_run_id": run_id,
                    "priority_run_id": priority_run_id,
                    "coverage_run_id": coverage_run_id,
                    "inventory_run_id": inventory_run_id,
                    "station_id": station_id,
                    "station_name": station_meta.get("station_name") or station_meta.get("best_station_name", ""),
                    "station_state": station_meta.get("station_state") or station_meta.get("best_station_state", ""),
                    "station_country": station_meta.get("station_country") or station_meta.get("best_station_country", ""),
                    "source_year": source_year,
                    "impacted_plant_count": summary["impacted_plant_count"],
                    "priority_buckets": summary["priority_buckets"],
                    "min_priority_rank": summary["min_priority_rank"],
                    "max_priority_rank": summary["max_priority_rank"],
                    "min_plant_gap_hours": summary["min_plant_gap_hours"],
                    "max_plant_gap_hours": summary["max_plant_gap_hours"],
                    "station_gap_to_threshold": summary["station_gap_to_threshold"],
                    "normalized_expected_djf_hours": expected,
                    "valid_djf_hours": valid,
                    "missing_to_normalized_expected_hours": missing_to_expected,
                    "coverage_ratio": fmt_float(coverage_ratio, 6),
                    "coverage_status": cov.get("coverage_status", "missing_coverage_row"),
                    "loaded_file_count": cov.get("loaded_file_count", "0"),
                    "invalid_temp_row_count": cov.get("invalid_temp_row_count", "0"),
                    "rejected_source_row_count": cov.get("rejected_source_row_count", "0"),
                    "rejected_plausibility_row_count": cov.get("rejected_plausibility_row_count", "0"),
                    "duplicate_hour_count": cov.get("duplicate_hour_count", "0"),
                    "raw_file_status": inv.get("file_status", ""),
                    "raw_file_path": inv.get("local_path", ""),
                    "raw_file_size_bytes": inv.get("file_size_bytes", ""),
                    "latest_download_status": attempt.get("download_status", ""),
                    "latest_http_status": attempt.get("http_status", ""),
                    "latest_download_run_id": attempt.get("calculation_run_id", ""),
                    "latest_download_error": (attempt.get("error_message") or "")[:300],
                    "notes": "Station-year has fewer valid DJF hours than the normalized active-window expected denominator.",
                }
            )
    rows.sort(
        key=lambda row: (
            -int(row["impacted_plant_count"]),
            int(row["station_gap_to_threshold"] or 999999999),
            -int(row["missing_to_normalized_expected_hours"]),
            str(row["station_id"]),
            int(row["source_year"]),
        )
    )
    return rows


def build_station_summary(rows: list[dict[str, object]], priority_rows: list[dict[str, str]], run_id: str) -> list[dict[str, object]]:
    plant_states: dict[str, Counter[str]] = defaultdict(Counter)
    for row in priority_rows:
        station_id = row.get("best_station_id")
        if station_id:
            plant_states[station_id][row.get("plant_state") or "(blank)"] += 1
    by_station: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_station[str(row["station_id"])].append(row)
    summaries: list[dict[str, object]] = []
    for station_id, group in by_station.items():
        first = group[0]
        missing_hours = [to_int(row.get("missing_to_normalized_expected_hours")) or 0 for row in group]
        invalids = [to_int(row.get("invalid_temp_row_count")) or 0 for row in group]
        rejected = [to_int(row.get("rejected_source_row_count")) or 0 for row in group]
        plaus = [to_int(row.get("rejected_plausibility_row_count")) or 0 for row in group]
        dupes = [to_int(row.get("duplicate_hour_count")) or 0 for row in group]
        missing_years = sorted(
            group,
            key=lambda row: (-int(row["missing_to_normalized_expected_hours"]), int(row["source_year"])),
        )
        top_missing_years = ";".join(
            f"{row['source_year']}:{row['missing_to_normalized_expected_hours']}h" for row in missing_years[:8]
        )
        latest_404 = sum(1 for row in group if str(row.get("latest_download_status")) == "missing_on_aws")
        retryable = sum(
            1
            for row in group
            if str(row.get("latest_download_status")) in {"failed_http", "failed_exception"}
        )
        summaries.append(
            {
                "gap_audit_run_id": run_id,
                "priority_run_id": first["priority_run_id"],
                "coverage_run_id": first["coverage_run_id"],
                "inventory_run_id": first["inventory_run_id"],
                "station_id": station_id,
                "station_name": first.get("station_name", ""),
                "station_state": first.get("station_state", ""),
                "station_country": first.get("station_country", ""),
                "impacted_plant_count": first["impacted_plant_count"],
                "priority_buckets": first["priority_buckets"],
                "min_plant_gap_hours": first["min_plant_gap_hours"],
                "max_plant_gap_hours": first["max_plant_gap_hours"],
                "station_gap_to_threshold": first["station_gap_to_threshold"],
                "normalized_expected_djf_hours": sum(to_int(row.get("normalized_expected_djf_hours")) or 0 for row in group),
                "normalized_valid_djf_hours": sum(to_int(row.get("valid_djf_hours")) or 0 for row in group),
                "missing_to_normalized_expected_hours": sum(missing_hours),
                "missing_station_year_count": len(group),
                "raw_file_missing_year_count": sum(1 for row in group if row.get("raw_file_status") == "missing"),
                "partial_coverage_year_count": sum(1 for row in group if row.get("coverage_status") == "partial"),
                "empty_coverage_year_count": sum(1 for row in group if row.get("coverage_status") == "empty"),
                "latest_aws_404_year_count": latest_404,
                "latest_retryable_failure_year_count": retryable,
                "invalid_temp_row_count": sum(invalids),
                "rejected_source_row_count": sum(rejected),
                "rejected_plausibility_row_count": sum(plaus),
                "duplicate_hour_count": sum(dupes),
                "top_missing_years": top_missing_years,
                "top_plant_states": ";".join(
                    f"{state}:{count}" for state, count in plant_states[station_id].most_common(8)
                ),
            }
        )
    summaries.sort(
        key=lambda row: (
            -int(row["impacted_plant_count"]),
            int(row["station_gap_to_threshold"] or 999999999),
            -int(row["missing_to_normalized_expected_hours"]),
            row["station_id"],
        )
    )
    return summaries


def qident(name: str) -> str:
    if not name.replace("_", "").isalnum() or name[0].isdigit():
        raise ValueError(f"Unsafe SQL identifier: {name}")
    return name


def temp_table_sql(table_name: str, fields: list[str]) -> str:
    cols = ",\n        ".join(f"{qident(field)} text" for field in fields)
    return f"create temp table {table_name} (\n        {cols}\n    ) on commit drop;"


def copy_sql(table_name: str, fields: list[str], path: Path) -> str:
    cols = ", ".join(qident(field) for field in fields)
    return f"\\copy {table_name} ({cols}) from {sql_literal(path)} with (format csv, header true, null '')"


def nullif_cast(field: str, cast_type: str) -> str:
    return f"nullif({qident(field)}, '')::{cast_type}"


def text_null(field: str) -> str:
    return f"nullif({qident(field)}, '')"


def build_load_sql(
    run_id: str,
    code_commit: str,
    started_at: str,
    params: dict[str, object],
    station_year_csv: Path,
    station_summary_csv: Path,
) -> str:
    return f"""
\\set ON_ERROR_STOP on
begin;

create table if not exists calc.coverage_blocker_station_year_gap (
    gap_row_id text primary key,
    gap_audit_run_id text not null references audit.calculation_run(calculation_run_id),
    priority_run_id text not null references audit.calculation_run(calculation_run_id),
    coverage_run_id text not null references audit.calculation_run(calculation_run_id),
    inventory_run_id text not null references audit.calculation_run(calculation_run_id),
    station_id text not null references weather.station(station_id),
    station_name text,
    station_state text,
    station_country text,
    source_year integer not null,
    impacted_plant_count bigint not null,
    priority_buckets text,
    min_priority_rank integer,
    max_priority_rank integer,
    min_plant_gap_hours bigint,
    max_plant_gap_hours bigint,
    station_gap_to_threshold bigint,
    normalized_expected_djf_hours bigint,
    valid_djf_hours bigint,
    missing_to_normalized_expected_hours bigint,
    coverage_ratio numeric,
    coverage_status text,
    loaded_file_count bigint,
    invalid_temp_row_count bigint,
    rejected_source_row_count bigint,
    rejected_plausibility_row_count bigint,
    duplicate_hour_count bigint,
    raw_file_status text,
    raw_file_path text,
    raw_file_size_bytes bigint,
    latest_download_status text,
    latest_http_status integer,
    latest_download_run_id text,
    latest_download_error text,
    notes text,
    created_at_utc timestamptz not null default now(),
    unique (gap_audit_run_id, station_id, source_year)
);
create index if not exists ix_coverage_blocker_station_year_gap_station
    on calc.coverage_blocker_station_year_gap (gap_audit_run_id, station_id, source_year);
create index if not exists ix_coverage_blocker_station_year_gap_status
    on calc.coverage_blocker_station_year_gap (gap_audit_run_id, coverage_status, raw_file_status);

create table if not exists calc.coverage_blocker_station_gap_summary (
    gap_audit_run_id text not null references audit.calculation_run(calculation_run_id),
    priority_run_id text not null references audit.calculation_run(calculation_run_id),
    coverage_run_id text not null references audit.calculation_run(calculation_run_id),
    inventory_run_id text not null references audit.calculation_run(calculation_run_id),
    station_id text not null references weather.station(station_id),
    station_name text,
    station_state text,
    station_country text,
    impacted_plant_count bigint not null,
    priority_buckets text,
    min_plant_gap_hours bigint,
    max_plant_gap_hours bigint,
    station_gap_to_threshold bigint,
    normalized_expected_djf_hours bigint,
    normalized_valid_djf_hours bigint,
    missing_to_normalized_expected_hours bigint,
    missing_station_year_count bigint,
    raw_file_missing_year_count bigint,
    partial_coverage_year_count bigint,
    empty_coverage_year_count bigint,
    latest_aws_404_year_count bigint,
    latest_retryable_failure_year_count bigint,
    invalid_temp_row_count bigint,
    rejected_source_row_count bigint,
    rejected_plausibility_row_count bigint,
    duplicate_hour_count bigint,
    top_missing_years text,
    top_plant_states text,
    created_at_utc timestamptz not null default now(),
    primary key (gap_audit_run_id, station_id)
);

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
    {sql_literal(started_at)},
    now(),
    'succeeded',
    {sql_literal(json.dumps(params, sort_keys=True))}::jsonb,
    'Audited station-year missing-hour root causes for near-threshold normalized coverage blockers.'
)
on conflict (calculation_run_id) do update set
    run_finished_at_utc = excluded.run_finished_at_utc,
    run_status = excluded.run_status,
    parameters_json = excluded.parameters_json,
    notes = excluded.notes;

{temp_table_sql("tmp_station_year_gap", STATION_YEAR_FIELDS)}
{copy_sql("tmp_station_year_gap", STATION_YEAR_FIELDS, station_year_csv)}
{temp_table_sql("tmp_station_gap_summary", STATION_SUMMARY_FIELDS)}
{copy_sql("tmp_station_gap_summary", STATION_SUMMARY_FIELDS, station_summary_csv)}

delete from calc.coverage_blocker_station_year_gap where gap_audit_run_id = {sql_literal(run_id)};
delete from calc.coverage_blocker_station_gap_summary where gap_audit_run_id = {sql_literal(run_id)};

insert into calc.coverage_blocker_station_year_gap (
    gap_row_id,
    gap_audit_run_id,
    priority_run_id,
    coverage_run_id,
    inventory_run_id,
    station_id,
    station_name,
    station_state,
    station_country,
    source_year,
    impacted_plant_count,
    priority_buckets,
    min_priority_rank,
    max_priority_rank,
    min_plant_gap_hours,
    max_plant_gap_hours,
    station_gap_to_threshold,
    normalized_expected_djf_hours,
    valid_djf_hours,
    missing_to_normalized_expected_hours,
    coverage_ratio,
    coverage_status,
    loaded_file_count,
    invalid_temp_row_count,
    rejected_source_row_count,
    rejected_plausibility_row_count,
    duplicate_hour_count,
    raw_file_status,
    raw_file_path,
    raw_file_size_bytes,
    latest_download_status,
    latest_http_status,
    latest_download_run_id,
    latest_download_error,
    notes
)
select
    gap_audit_run_id || ':station:' || station_id || ':year:' || source_year,
    gap_audit_run_id,
    priority_run_id,
    coverage_run_id,
    inventory_run_id,
    station_id,
    {text_null("station_name")},
    {text_null("station_state")},
    {text_null("station_country")},
    {nullif_cast("source_year", "integer")},
    {nullif_cast("impacted_plant_count", "bigint")},
    {text_null("priority_buckets")},
    {nullif_cast("min_priority_rank", "integer")},
    {nullif_cast("max_priority_rank", "integer")},
    {nullif_cast("min_plant_gap_hours", "bigint")},
    {nullif_cast("max_plant_gap_hours", "bigint")},
    {nullif_cast("station_gap_to_threshold", "bigint")},
    {nullif_cast("normalized_expected_djf_hours", "bigint")},
    {nullif_cast("valid_djf_hours", "bigint")},
    {nullif_cast("missing_to_normalized_expected_hours", "bigint")},
    {nullif_cast("coverage_ratio", "numeric")},
    {text_null("coverage_status")},
    {nullif_cast("loaded_file_count", "bigint")},
    {nullif_cast("invalid_temp_row_count", "bigint")},
    {nullif_cast("rejected_source_row_count", "bigint")},
    {nullif_cast("rejected_plausibility_row_count", "bigint")},
    {nullif_cast("duplicate_hour_count", "bigint")},
    {text_null("raw_file_status")},
    {text_null("raw_file_path")},
    {nullif_cast("raw_file_size_bytes", "bigint")},
    {text_null("latest_download_status")},
    {nullif_cast("latest_http_status", "integer")},
    {text_null("latest_download_run_id")},
    {text_null("latest_download_error")},
    {text_null("notes")}
from tmp_station_year_gap;

insert into calc.coverage_blocker_station_gap_summary (
    gap_audit_run_id,
    priority_run_id,
    coverage_run_id,
    inventory_run_id,
    station_id,
    station_name,
    station_state,
    station_country,
    impacted_plant_count,
    priority_buckets,
    min_plant_gap_hours,
    max_plant_gap_hours,
    station_gap_to_threshold,
    normalized_expected_djf_hours,
    normalized_valid_djf_hours,
    missing_to_normalized_expected_hours,
    missing_station_year_count,
    raw_file_missing_year_count,
    partial_coverage_year_count,
    empty_coverage_year_count,
    latest_aws_404_year_count,
    latest_retryable_failure_year_count,
    invalid_temp_row_count,
    rejected_source_row_count,
    rejected_plausibility_row_count,
    duplicate_hour_count,
    top_missing_years,
    top_plant_states
)
select
    gap_audit_run_id,
    priority_run_id,
    coverage_run_id,
    inventory_run_id,
    station_id,
    {text_null("station_name")},
    {text_null("station_state")},
    {text_null("station_country")},
    {nullif_cast("impacted_plant_count", "bigint")},
    {text_null("priority_buckets")},
    {nullif_cast("min_plant_gap_hours", "bigint")},
    {nullif_cast("max_plant_gap_hours", "bigint")},
    {nullif_cast("station_gap_to_threshold", "bigint")},
    {nullif_cast("normalized_expected_djf_hours", "bigint")},
    {nullif_cast("normalized_valid_djf_hours", "bigint")},
    {nullif_cast("missing_to_normalized_expected_hours", "bigint")},
    {nullif_cast("missing_station_year_count", "bigint")},
    {nullif_cast("raw_file_missing_year_count", "bigint")},
    {nullif_cast("partial_coverage_year_count", "bigint")},
    {nullif_cast("empty_coverage_year_count", "bigint")},
    {nullif_cast("latest_aws_404_year_count", "bigint")},
    {nullif_cast("latest_retryable_failure_year_count", "bigint")},
    {nullif_cast("invalid_temp_row_count", "bigint")},
    {nullif_cast("rejected_source_row_count", "bigint")},
    {nullif_cast("rejected_plausibility_row_count", "bigint")},
    {nullif_cast("duplicate_hour_count", "bigint")},
    {text_null("top_missing_years")},
    {text_null("top_plant_states")}
from tmp_station_gap_summary;

commit;
"""


def md_table(rows: list[dict[str, object]], fields: list[str], headers: list[str], limit: int | None = None) -> list[str]:
    shown = rows if limit is None else rows[:limit]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in shown:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("|", "\\|") for field in fields) + " |")
    if limit is not None and len(rows) > limit:
        lines.append("| ... | " + f"{len(rows) - limit} more rows omitted" + " |" * (len(fields) - 1))
    return lines


def render_report(
    path: Path,
    run_id: str,
    code_commit: str,
    priority_run_id: str,
    coverage_run_id: str,
    inventory_run_id: str,
    max_gap_hours: int,
    station_year_rows: list[dict[str, object]],
    station_summary_rows: list[dict[str, object]],
    station_year_csv: Path,
    station_summary_csv: Path,
    db_counts: OrderedDict[str, str],
) -> None:
    coverage_counts = Counter(str(row.get("coverage_status") or "(blank)") for row in station_year_rows)
    raw_counts = Counter(str(row.get("raw_file_status") or "(blank)") for row in station_year_rows)
    download_counts = Counter(str(row.get("latest_download_status") or "(blank)") for row in station_year_rows)
    lines = [
        "# Near-Threshold Station-Year Gap Audit",
        "",
        f"Generated UTC: {utc_now().isoformat(timespec='seconds')}",
        "",
        "## Run",
        "",
        f"- Gap audit run ID: `{run_id}`",
        f"- Priority run ID: `{priority_run_id}`",
        f"- Station-year coverage run ID: `{coverage_run_id}`",
        f"- Raw inventory run ID: `{inventory_run_id}`",
        f"- Code commit: `{code_commit}`",
        f"- Max plant gap hours included: `{max_gap_hours}`",
        f"- Station-year CSV: `{station_year_csv.name}`",
        f"- Station summary CSV: `{station_summary_csv.name}`",
        "",
        "## Loaded DB Counts",
        "",
    ]
    lines.extend(md_table([{"check": key, "rows": value} for key, value in db_counts.items()], ["check", "rows"], ["Check", "Rows"]))
    lines.extend(["", "## Station-Year Status Counts", ""])
    lines.extend(md_table([{"status": key, "rows": value} for key, value in coverage_counts.most_common()], ["status", "rows"], ["Coverage Status", "Rows"]))
    lines.extend(["", "## Raw File Status Counts", ""])
    lines.extend(md_table([{"status": key, "rows": value} for key, value in raw_counts.most_common()], ["status", "rows"], ["Raw File Status", "Rows"]))
    lines.extend(["", "## Latest Download Status Counts", ""])
    lines.extend(md_table([{"status": key, "rows": value} for key, value in download_counts.most_common()], ["status", "rows"], ["Latest Download Status", "Rows"]))
    lines.extend(["", "## Top Stations By Impacted Plants", ""])
    lines.extend(
        md_table(
            station_summary_rows,
            [
                "station_id",
                "station_name",
                "impacted_plant_count",
                "station_gap_to_threshold",
                "missing_station_year_count",
                "missing_to_normalized_expected_hours",
                "raw_file_missing_year_count",
                "top_missing_years",
            ],
            [
                "Station",
                "Name",
                "Plants",
                "Gap Hours",
                "Missing Years",
                "Missing Hours",
                "Raw Missing Years",
                "Top Missing Years",
            ],
            limit=20,
        )
    )
    top_years = sorted(
        station_year_rows,
        key=lambda row: (
            -int(row["impacted_plant_count"]),
            -int(row["missing_to_normalized_expected_hours"]),
            str(row["station_id"]),
            int(row["source_year"]),
        ),
    )
    lines.extend(["", "## Top Station-Year Gaps", ""])
    lines.extend(
        md_table(
            top_years,
            [
                "station_id",
                "source_year",
                "impacted_plant_count",
                "missing_to_normalized_expected_hours",
                "valid_djf_hours",
                "normalized_expected_djf_hours",
                "coverage_status",
                "raw_file_status",
                "latest_download_status",
            ],
            ["Station", "Year", "Plants", "Missing Hours", "Valid", "Expected", "Coverage", "Raw File", "Download"],
            limit=30,
        )
    )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- This audit is restricted to plants whose best normalized-active candidate is within the configured valid-hour gap threshold.",
            "- Rows are station-years where the normalized active-window denominator expects DJF hours but the loaded canonical coverage has fewer valid hours.",
            "- If raw files are available and coverage is partial, the issue is likely source sparsity, parsing rejection, or source-observation gaps rather than a missing AWS object.",
            "- If raw files are missing with prior `missing_on_aws`, the public AWS object has already been tested and should not be blindly retried.",
            "- This diagnostic does not alter plant readiness or release status.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--psql", type=Path, default=PSQL)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5436)
    parser.add_argument("--dbname", default="eop012")
    parser.add_argument("--user")
    parser.add_argument("--priority-run-id")
    parser.add_argument("--coverage-run-id")
    parser.add_argument("--inventory-run-id")
    parser.add_argument("--max-gap-hours", type=int, default=DEFAULT_MAX_GAP_HOURS)
    args = parser.parse_args()

    priority_run_id = args.priority_run_id or latest_run_id(
        args.psql, args.host, args.port, args.dbname, args.user, "normalized_active_window_blocker_priority_"
    )
    coverage_run_id = args.coverage_run_id or latest_run_id(
        args.psql, args.host, args.port, args.dbname, args.user, "station_year_djf_coverage_"
    )
    inventory_run_id = args.inventory_run_id or latest_run_id(
        args.psql, args.host, args.port, args.dbname, args.user, "noaa_raw_file_inventory_"
    )
    run_id = f"near_threshold_station_year_gap_audit_{utc_now().strftime('%Y%m%dT%H%M%SZ')}"
    code_commit = git_commit_label(args.project_root)
    started_at = utc_now().isoformat(timespec="seconds")

    priority_rows = fetch_priority_rows(
        args.psql, args.host, args.port, args.dbname, args.user, priority_run_id, args.max_gap_hours
    )
    if not priority_rows:
        raise RuntimeError("No priority rows matched the near-threshold gap filter.")
    station_ids = sorted({row["best_station_id"] for row in priority_rows if row.get("best_station_id")})
    coverage = fetch_coverage_rows(args.psql, args.host, args.port, args.dbname, args.user, coverage_run_id, station_ids)
    inventory = fetch_inventory_rows(args.psql, args.host, args.port, args.dbname, args.user, inventory_run_id, station_ids)
    attempts = fetch_latest_attempt_rows(args.psql, args.host, args.port, args.dbname, args.user, station_ids)

    station_year_rows = build_station_year_rows(
        run_id, priority_run_id, coverage_run_id, inventory_run_id, priority_rows, coverage, inventory, attempts
    )
    station_summary_rows = build_station_summary(station_year_rows, priority_rows, run_id)

    docs_dir = args.project_root / "docs"
    station_year_csv = docs_dir / f"{run_id}_station_years.csv"
    station_summary_csv = docs_dir / f"{run_id}_stations.csv"
    write_csv(station_year_csv, STATION_YEAR_FIELDS, station_year_rows)
    write_csv(station_summary_csv, STATION_SUMMARY_FIELDS, station_summary_rows)

    params = {
        "priority_run_id": priority_run_id,
        "coverage_run_id": coverage_run_id,
        "inventory_run_id": inventory_run_id,
        "max_gap_hours": args.max_gap_hours,
        "priority_rows": len(priority_rows),
        "station_count": len(station_ids),
        "station_year_gap_rows": len(station_year_rows),
        "station_summary_rows": len(station_summary_rows),
    }
    run(
        psql_cmd(args.psql, args.host, args.port, args.dbname, args.user),
        input_text=build_load_sql(run_id, code_commit, started_at, params, station_year_csv, station_summary_csv),
    )

    db_counts = OrderedDict(
        [
            (
                "calc.coverage_blocker_station_year_gap",
                psql_scalar(
                    args.psql,
                    args.host,
                    args.port,
                    args.dbname,
                    args.user,
                    f"select count(*) from calc.coverage_blocker_station_year_gap where gap_audit_run_id = {sql_literal(run_id)};",
                ),
            ),
            (
                "calc.coverage_blocker_station_gap_summary",
                psql_scalar(
                    args.psql,
                    args.host,
                    args.port,
                    args.dbname,
                    args.user,
                    f"select count(*) from calc.coverage_blocker_station_gap_summary where gap_audit_run_id = {sql_literal(run_id)};",
                ),
            ),
        ]
    )
    report_path = docs_dir / f"{run_id}_report.md"
    render_report(
        report_path,
        run_id,
        code_commit,
        priority_run_id,
        coverage_run_id,
        inventory_run_id,
        args.max_gap_hours,
        station_year_rows,
        station_summary_rows,
        station_year_csv,
        station_summary_csv,
        db_counts,
    )
    print(
        json.dumps(
            OrderedDict(
                [
                    ("run_id", run_id),
                    ("priority_run_id", priority_run_id),
                    ("coverage_run_id", coverage_run_id),
                    ("inventory_run_id", inventory_run_id),
                    ("max_gap_hours", args.max_gap_hours),
                    ("priority_rows", len(priority_rows)),
                    ("station_count", len(station_ids)),
                    ("station_year_gap_rows", len(station_year_rows)),
                    ("station_summary_rows", len(station_summary_rows)),
                    ("db_counts", db_counts),
                    ("station_year_csv", str(station_year_csv)),
                    ("station_summary_csv", str(station_summary_csv)),
                    ("report_path", str(report_path)),
                ]
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
