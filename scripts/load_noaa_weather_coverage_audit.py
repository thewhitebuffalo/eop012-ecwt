#!/usr/bin/env python3
"""Load NOAA weather coverage metrics for plant-station candidates.

This pass uses the legacy NOAA cache's precomputed station sample-hour table
(`public.ecwt_raw_station`) as a fast coverage inventory. It is retained for
historical replay only after the 2026-06-25 retirement of the old source
cluster. It does not load the full hourly weather table into the EOP012
database and it does not select final representative stations.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import subprocess
from collections import OrderedDict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable

from eop012_config import PROJECT_ROOT, PSQL, SOURCE_CLUSTER_PATH, STAGING_ROOT

DEFAULT_STAGING_ROOT = STAGING_ROOT
DEFAULT_SOURCE_CLUSTER_PATH = SOURCE_CLUSTER_PATH

METHODOLOGY_VERSION = "eop012-ecwt-method-v0.1.0"
SOURCE_FAMILY = "legacy_noaa_station_sample_hour_coverage"
SOURCE_BASIS = "legacy_ecwt_raw_station_sample_hours"


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


def git_commit_label(project_root: Path) -> str:
    try:
        result = run(["git", "-C", str(project_root), "rev-parse", "HEAD"])
        return result.stdout.strip()
    except Exception:
        return "UNCOMMITTED_WORKTREE"


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


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def expected_djf_hours(period_start_year: int, period_end_year: int) -> tuple[datetime, datetime, int]:
    start = datetime(period_start_year, 1, 1, 0, tzinfo=timezone.utc)
    end = datetime(period_end_year, 12, 31, 23, tzinfo=timezone.utc)
    count = 0
    cursor = start
    while cursor <= end:
        if cursor.month in (12, 1, 2):
            count += 1
        cursor += timedelta(hours=1)
    return start, end, count


def latest_candidate_run_id(psql: Path, host: str, port: int, dbname: str, user: str | None) -> str:
    run_id = psql_scalar(
        psql,
        host,
        port,
        dbname,
        """
        select calculation_run_id
        from audit.calculation_run
        where calculation_run_id like 'noaa_station_candidates_%'
          and run_status = 'succeeded'
        order by run_started_at_utc desc
        limit 1
        """,
        user,
    )
    if not run_id:
        raise RuntimeError("No succeeded noaa_station_candidates calculation run found.")
    return run_id


def export_candidate_station_ids(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    candidate_run_id: str,
    path: Path,
) -> int:
    query = f"""
        select distinct station_id
        from link.station_candidate
        where calculation_run_id = {sql_literal(candidate_run_id)}
        order by station_id
    """
    rows = psql_csv_query(psql, host, port, dbname, query, user)
    write_csv(path, ["station_id"], rows)
    return len(rows)


def export_legacy_coverage(
    psql: Path,
    source_host: str,
    source_port: int,
    source_dbname: str,
    source_user: str | None,
    station_ids_csv: Path,
    coverage_csv: Path,
    period_start_year: int,
    period_end_year: int,
) -> None:
    sql = f"""
\\set ON_ERROR_STOP on
create temp table stg_candidate_station_id (
    station_id text primary key
);
\\copy stg_candidate_station_id(station_id) from '{station_ids_csv}' with (format csv, header true)
copy (
    with latest_full as (
        select distinct on (station_id_canonical)
            station_id_canonical,
            sample_hours,
            percentile_temp_c,
            ecwt_raw_c,
            methodology,
            ingest_run_id,
            calculated_at_utc
        from public.ecwt_raw_station
        where period_start_year = {period_start_year}
          and period_end_year = {period_end_year}
        order by station_id_canonical, calculated_at_utc desc
    )
    select
        s.station_id,
        (l.station_id_canonical is not null) as has_full_period_row,
        coalesce(l.sample_hours, 0)::bigint as valid_djf_hours,
        l.percentile_temp_c,
        l.ecwt_raw_c,
        l.methodology as legacy_methodology,
        l.ingest_run_id,
        l.calculated_at_utc
    from stg_candidate_station_id s
    left join latest_full l
      on l.station_id_canonical = s.station_id
    order by s.station_id
) to '{coverage_csv}' with (format csv, header true);
"""
    run(psql_cmd(psql, source_host, source_port, source_dbname, source_user), input_text=sql)


def read_coverage_rows(
    coverage_csv: Path,
    run_id: str,
    period_start_utc: datetime,
    period_end_utc: datetime,
    expected_hours: int,
) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, int | float | str | None]]:
    audit_rows: list[dict[str, object]] = []
    exceptions: list[dict[str, object]] = []
    stats = {
        "station_rows": 0,
        "stations_with_full_period_row": 0,
        "stations_missing_full_period_row": 0,
        "stations_with_zero_valid_hours": 0,
        "stations_with_positive_valid_hours": 0,
        "min_valid_hours": None,
        "max_valid_hours": None,
        "max_coverage_ratio": None,
    }
    valid_values: list[int] = []
    ratio_values: list[float] = []

    with coverage_csv.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            station_id = row["station_id"]
            has_full_period = row["has_full_period_row"].lower() == "t" or row["has_full_period_row"].lower() == "true"
            valid_hours = int(row["valid_djf_hours"] or 0)
            missing_hours = max(expected_hours - valid_hours, 0)
            coverage_ratio = valid_hours / expected_hours if expected_hours else None
            stats["station_rows"] += 1
            stats["stations_with_full_period_row"] += 1 if has_full_period else 0
            stats["stations_missing_full_period_row"] += 0 if has_full_period else 1
            stats["stations_with_zero_valid_hours"] += 1 if valid_hours == 0 else 0
            stats["stations_with_positive_valid_hours"] += 1 if valid_hours > 0 else 0
            valid_values.append(valid_hours)
            if coverage_ratio is not None:
                ratio_values.append(coverage_ratio)
            audit_rows.append(
                {
                    "station_coverage_audit_id": f"{run_id}:station:{station_id}",
                    "station_id": station_id,
                    "calculation_run_id": run_id,
                    "period_start_utc": period_start_utc.isoformat(timespec="seconds"),
                    "period_end_utc": period_end_utc.isoformat(timespec="seconds"),
                    "expected_djf_hours": expected_hours,
                    "valid_djf_hours": valid_hours,
                    "missing_hour_count": missing_hours,
                    "duplicate_hour_count": 0,
                    "invalid_temp_count": 0,
                    "coverage_ratio": f"{coverage_ratio:.12f}" if coverage_ratio is not None else None,
                    "source_basis": SOURCE_BASIS,
                    "notes": (
                        "Fast coverage audit from legacy ecwt_raw_station.sample_hours. "
                        "duplicate_hour_count and invalid_temp_count are not raw-source recounts in this pass."
                    ),
                }
            )
            if not has_full_period:
                exceptions.append(
                    {
                        "exception_id": f"{run_id}:missing_full_period_coverage:{station_id}",
                        "calculation_run_id": run_id,
                        "entity_type": "station",
                        "entity_id": station_id,
                        "severity": "warning",
                        "reason_code": "station_missing_legacy_full_period_coverage_row",
                        "message": (
                            f"Station {station_id} has plant-candidate links but no full-period "
                            "legacy ecwt_raw_station row for this coverage window."
                        ),
                        "resolution_status": "open",
                        "notes": "Coverage loaded as zero pending full hourly source rebuild or validation.",
                    }
                )

    if valid_values:
        stats["min_valid_hours"] = min(valid_values)
        stats["max_valid_hours"] = max(valid_values)
    if ratio_values:
        stats["max_coverage_ratio"] = max(ratio_values)
    return audit_rows, exceptions, stats


def render_values_insert(table: str, columns: list[str], rows: list[dict[str, object]], conflict: str) -> str:
    values = []
    for row in rows:
        values.append("(" + ", ".join(sql_literal(row.get(col)) for col in columns) + ")")
    return f"insert into {table} ({', '.join(columns)}) values\n" + ",\n".join(values) + f"\n{conflict};\n"


def copy_command(table: str, columns: list[str], path: Path) -> str:
    return f"\\copy {table} ({', '.join(columns)}) from '{path}' with (format csv, header true, null '\\N')"


def build_load_sql(
    staging_dir: Path,
    source_row: dict[str, object],
    run_id: str,
    candidate_run_id: str,
    code_commit: str,
    params: dict[str, object],
) -> str:
    start = utc_now().isoformat(timespec="seconds")
    source_cols = [
        "source_file_id",
        "source_family",
        "source_url",
        "local_path",
        "file_name",
        "size_bytes",
        "sha256",
        "retrieved_at_utc",
        "source_year",
        "source_release",
        "notes",
    ]
    coverage_cols = [
        "station_coverage_audit_id",
        "station_id",
        "calculation_run_id",
        "period_start_utc",
        "period_end_utc",
        "expected_djf_hours",
        "valid_djf_hours",
        "missing_hour_count",
        "duplicate_hour_count",
        "invalid_temp_count",
        "coverage_ratio",
        "source_basis",
        "notes",
    ]
    exception_cols = [
        "exception_id",
        "calculation_run_id",
        "entity_type",
        "entity_id",
        "severity",
        "reason_code",
        "message",
        "resolution_status",
        "notes",
    ]
    return "\n".join(
        [
            "\\set ON_ERROR_STOP on",
            "begin;",
            "alter table weather.station_coverage_audit add column if not exists source_basis text;",
            "alter table weather.station_coverage_audit add column if not exists notes text;",
            render_values_insert(
                "audit.methodology_version",
                ["methodology_version", "methodology_name", "effective_at_utc", "source_standard", "notes"],
                [
                    {
                        "methodology_version": METHODOLOGY_VERSION,
                        "methodology_name": "EOP012 ECWT national calculation methodology",
                        "effective_at_utc": start,
                        "source_standard": "NERC EOP-012-3; EPRI 3002030362 guidance",
                        "notes": "Initial auditable methodology version for asset loading, station matching, coverage auditing, and ECWT calculation.",
                    }
                ],
                "on conflict (methodology_version) do update set notes = excluded.notes",
            ),
            render_values_insert(
                "audit.source_file",
                source_cols,
                [source_row],
                """on conflict (source_file_id) do update set
    source_family = excluded.source_family,
    source_url = excluded.source_url,
    local_path = excluded.local_path,
    file_name = excluded.file_name,
    size_bytes = excluded.size_bytes,
    sha256 = excluded.sha256,
    retrieved_at_utc = excluded.retrieved_at_utc,
    source_year = excluded.source_year,
    source_release = excluded.source_release,
    notes = excluded.notes""",
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
    'Loaded NOAA weather coverage audit metrics for station candidates.'
)
on conflict (calculation_run_id) do update set
    run_finished_at_utc = excluded.run_finished_at_utc,
    run_status = excluded.run_status,
    parameters_json = excluded.parameters_json,
    notes = excluded.notes;
""",
            """
create temp table stg_station_coverage (
    station_coverage_audit_id text,
    station_id text,
    calculation_run_id text,
    period_start_utc timestamptz,
    period_end_utc timestamptz,
    expected_djf_hours bigint,
    valid_djf_hours bigint,
    missing_hour_count bigint,
    duplicate_hour_count bigint,
    invalid_temp_count bigint,
    coverage_ratio numeric,
    source_basis text,
    notes text
) on commit drop;
""",
            copy_command("stg_station_coverage", coverage_cols, staging_dir / "station_coverage_audit.csv"),
            """
insert into weather.station_coverage_audit (
    station_coverage_audit_id,
    station_id,
    calculation_run_id,
    period_start_utc,
    period_end_utc,
    expected_djf_hours,
    valid_djf_hours,
    missing_hour_count,
    duplicate_hour_count,
    invalid_temp_count,
    coverage_ratio,
    source_basis,
    notes
)
select
    station_coverage_audit_id,
    station_id,
    calculation_run_id,
    period_start_utc,
    period_end_utc,
    expected_djf_hours,
    valid_djf_hours,
    missing_hour_count,
    duplicate_hour_count,
    invalid_temp_count,
    coverage_ratio,
    source_basis,
    notes
from stg_station_coverage
on conflict (station_coverage_audit_id) do update set
    expected_djf_hours = excluded.expected_djf_hours,
    valid_djf_hours = excluded.valid_djf_hours,
    missing_hour_count = excluded.missing_hour_count,
    duplicate_hour_count = excluded.duplicate_hour_count,
    invalid_temp_count = excluded.invalid_temp_count,
    coverage_ratio = excluded.coverage_ratio,
    source_basis = excluded.source_basis,
    notes = excluded.notes;
""",
            f"""
update link.station_candidate candidate
set
    valid_djf_hours = coverage.valid_djf_hours,
    expected_djf_hours = coverage.expected_djf_hours,
    coverage_ratio = coverage.coverage_ratio,
    notes = 'Coverage metrics populated by {run_id} using {SOURCE_BASIS}; representative station selection remains pending.'
from weather.station_coverage_audit coverage
where coverage.calculation_run_id = {sql_literal(run_id)}
  and candidate.calculation_run_id = {sql_literal(candidate_run_id)}
  and candidate.station_id = coverage.station_id;
""",
            """
create temp table stg_exception (
    exception_id text,
    calculation_run_id text,
    entity_type text,
    entity_id text,
    severity text,
    reason_code text,
    message text,
    resolution_status text,
    notes text
) on commit drop;
""",
            copy_command("stg_exception", exception_cols, staging_dir / "exceptions.csv"),
            """
insert into audit.exception_log (
    exception_id,
    calculation_run_id,
    entity_type,
    entity_id,
    severity,
    reason_code,
    message,
    resolution_status,
    notes
)
select
    exception_id,
    calculation_run_id,
    entity_type,
    entity_id,
    severity,
    reason_code,
    message,
    resolution_status,
    notes
from stg_exception
on conflict (exception_id) do update set
    severity = excluded.severity,
    reason_code = excluded.reason_code,
    message = excluded.message,
    resolution_status = excluded.resolution_status,
    notes = excluded.notes;
""",
            "commit;",
        ]
    )


def report_query_map(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    run_id: str,
    candidate_run_id: str,
) -> OrderedDict[str, str]:
    queries = OrderedDict(
        [
            (
                "weather.station_coverage_audit for this run",
                f"select count(*) from weather.station_coverage_audit where calculation_run_id = {sql_literal(run_id)};",
            ),
            (
                "link.station_candidate rows updated",
                f"""
                select count(*)
                from link.station_candidate
                where calculation_run_id = {sql_literal(candidate_run_id)}
                  and valid_djf_hours is not null
                  and expected_djf_hours is not null
                """,
            ),
            (
                "plants with at least one positive-coverage candidate",
                f"""
                select count(*)
                from (
                    select plant_id, max(coalesce(valid_djf_hours, 0)) as best_valid
                    from link.station_candidate
                    where calculation_run_id = {sql_literal(candidate_run_id)}
                    group by plant_id
                ) x
                where best_valid > 0
                """,
            ),
            (
                "plants with zero positive-coverage candidates",
                f"""
                select count(*)
                from (
                    select plant_id, max(coalesce(valid_djf_hours, 0)) as best_valid
                    from link.station_candidate
                    where calculation_run_id = {sql_literal(candidate_run_id)}
                    group by plant_id
                ) x
                where best_valid = 0
                """,
            ),
            (
                "max candidate coverage ratio",
                f"""
                select coalesce(round(max(coverage_ratio), 6)::text, 'null')
                from link.station_candidate
                where calculation_run_id = {sql_literal(candidate_run_id)}
                """,
            ),
            ("audit.source_file", "select count(*) from audit.source_file;"),
            ("audit.calculation_run", "select count(*) from audit.calculation_run;"),
            ("audit.exception_log", "select count(*) from audit.exception_log;"),
        ]
    )
    results: OrderedDict[str, str] = OrderedDict()
    for label, query in queries.items():
        results[label] = psql_scalar(psql, host, port, dbname, query, user)
    return results


def render_report(
    path: Path,
    run_id: str,
    candidate_run_id: str,
    code_commit: str,
    source_row: dict[str, object],
    expected_hours: int,
    period_start_utc: datetime,
    period_end_utc: datetime,
    stats: dict[str, int | float | str | None],
    db_counts: OrderedDict[str, str],
    host: str,
    port: int,
    dbname: str,
    source_host: str,
    source_port: int,
    source_dbname: str,
) -> None:
    lines = [
        "# NOAA Weather Coverage Audit Report",
        "",
        f"Generated UTC: {utc_now().isoformat(timespec='seconds')}",
        "",
        "## Target Database",
        "",
        f"- Host: `{host}`",
        f"- Port: `{port}`",
        f"- Database: `{dbname}`",
        "",
        "## Source Database",
        "",
        f"- Host: `{source_host}`",
        f"- Port: `{source_port}`",
        f"- Database: `{source_dbname}`",
        f"- Source table: `{source_row['file_name']}`",
        f"- Source basis: `{SOURCE_BASIS}`",
        f"- Local path: `{source_row['local_path']}`",
        "",
        "## Run",
        "",
        f"- Calculation run ID: `{run_id}`",
        f"- Candidate run ID enriched: `{candidate_run_id}`",
        f"- Methodology version: `{METHODOLOGY_VERSION}`",
        f"- Code commit: `{code_commit}`",
        "",
        "## Coverage Window",
        "",
        f"- Period start UTC: `{period_start_utc.isoformat(timespec='seconds')}`",
        f"- Period end UTC: `{period_end_utc.isoformat(timespec='seconds')}`",
        f"- Expected DJF hours per station: `{expected_hours}`",
        "- DJF filtering basis for this fast audit: UTC calendar months in the legacy station sample-hour inventory.",
        "",
        "## Counts",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| Candidate stations audited | {stats['station_rows']} |",
        f"| Stations with full-period legacy sample row | {stats['stations_with_full_period_row']} |",
        f"| Stations missing full-period legacy sample row | {stats['stations_missing_full_period_row']} |",
        f"| Stations with positive valid hours | {stats['stations_with_positive_valid_hours']} |",
        f"| Stations with zero valid hours | {stats['stations_with_zero_valid_hours']} |",
        f"| Minimum valid hours | {stats['min_valid_hours']} |",
        f"| Maximum valid hours | {stats['max_valid_hours']} |",
        f"| Maximum coverage ratio | {stats['max_coverage_ratio']} |",
        "",
        "## Database Row Counts",
        "",
        "| Relation or Check | Rows / Value |",
        "| --- | ---: |",
    ]
    for label, value in db_counts.items():
        lines.append(f"| `{label}` | {value} |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- This is a fast coverage audit against the legacy NOAA station sample-hour inventory, not a full raw-hour recount.",
            "- `duplicate_hour_count` and `invalid_temp_count` are stored as `0` for this pass because `ecwt_raw_station.sample_hours` only exposes accepted sample-hour totals.",
            "- The current NOAA cache is materially incomplete for a compliance-grade national ECWT run; station selection should not be finalized from this coverage pass alone.",
            "- The next required build step is a full hourly NOAA DJF rebuild or recount that can populate raw missing, duplicate, and invalid-temperature evidence.",
            "",
        ]
    )
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
    parser.add_argument("--source-host", default="127.0.0.1")
    parser.add_argument("--source-port", type=int, default=5435)
    parser.add_argument("--source-dbname", default="noaa_djf_hourly_bytower")
    parser.add_argument("--source-user", default="Athena")
    parser.add_argument("--source-cluster-path", type=Path, default=DEFAULT_SOURCE_CLUSTER_PATH)
    parser.add_argument("--candidate-run-id", default=None)
    parser.add_argument("--period-start-year", type=int, default=2000)
    parser.add_argument("--period-end-year", type=int, default=2025)
    args = parser.parse_args()

    if not args.psql.exists():
        raise FileNotFoundError(args.psql)

    candidate_run_id = args.candidate_run_id or latest_candidate_run_id(
        args.psql, args.host, args.port, args.dbname, args.user
    )
    code_commit = git_commit_label(args.project_root)
    period_start_utc, period_end_utc, expected_hours = expected_djf_hours(
        args.period_start_year, args.period_end_year
    )
    run_timestamp = utc_now().strftime("%Y%m%dT%H%M%SZ")
    run_id = f"noaa_weather_coverage_audit_{run_timestamp}"
    staging_dir = args.staging_root / run_id
    staging_dir.mkdir(parents=True, exist_ok=True)

    station_ids_csv = staging_dir / "candidate_station_ids.csv"
    distinct_station_count = export_candidate_station_ids(
        args.psql,
        args.host,
        args.port,
        args.dbname,
        args.user,
        candidate_run_id,
        station_ids_csv,
    )
    if distinct_station_count == 0:
        raise RuntimeError(f"No station candidates found for candidate run {candidate_run_id}.")

    legacy_coverage_csv = staging_dir / "legacy_station_sample_hour_coverage.csv"
    export_legacy_coverage(
        args.psql,
        args.source_host,
        args.source_port,
        args.source_dbname,
        args.source_user,
        station_ids_csv,
        legacy_coverage_csv,
        args.period_start_year,
        args.period_end_year,
    )

    coverage_rows, exception_rows, stats = read_coverage_rows(
        legacy_coverage_csv,
        run_id,
        period_start_utc,
        period_end_utc,
        expected_hours,
    )
    coverage_cols = [
        "station_coverage_audit_id",
        "station_id",
        "calculation_run_id",
        "period_start_utc",
        "period_end_utc",
        "expected_djf_hours",
        "valid_djf_hours",
        "missing_hour_count",
        "duplicate_hour_count",
        "invalid_temp_count",
        "coverage_ratio",
        "source_basis",
        "notes",
    ]
    exception_cols = [
        "exception_id",
        "calculation_run_id",
        "entity_type",
        "entity_id",
        "severity",
        "reason_code",
        "message",
        "resolution_status",
        "notes",
    ]
    write_csv(staging_dir / "station_coverage_audit.csv", coverage_cols, coverage_rows)
    write_csv(staging_dir / "exceptions.csv", exception_cols, exception_rows)

    source_summary = psql_csv_query(
        args.psql,
        args.source_host,
        args.source_port,
        args.source_dbname,
        f"""
        select
            count(*)::text as full_period_rows,
            count(distinct station_id_canonical)::text as full_period_stations,
            min(calculated_at_utc)::text as min_calculated_at_utc,
            max(calculated_at_utc)::text as max_calculated_at_utc,
            pg_total_relation_size('public.ecwt_raw_station'::regclass)::text as relation_size_bytes
        from public.ecwt_raw_station
        where period_start_year = {args.period_start_year}
          and period_end_year = {args.period_end_year}
        """,
        args.source_user,
    )[0]
    source_file_id_seed = (
        f"{SOURCE_FAMILY}|{args.source_dbname}|public.ecwt_raw_station|"
        f"{args.period_start_year}|{args.period_end_year}"
    )
    source_row = {
        "source_file_id": f"{SOURCE_FAMILY}_{sha256_text(source_file_id_seed)[:16]}",
        "source_family": SOURCE_FAMILY,
        "source_url": None,
        "local_path": str(args.source_cluster_path),
        "file_name": "public.ecwt_raw_station",
        "size_bytes": source_summary["relation_size_bytes"],
        "sha256": None,
        "retrieved_at_utc": source_summary["max_calculated_at_utc"] or None,
        "source_year": None,
        "source_release": f"legacy_full_period_{args.period_start_year}_{args.period_end_year}",
        "notes": (
            "Legacy NOAA cache station-level sample-hour table. This is a derived table from "
            "the old noaa_djf_hourly_bytower database and is used only for fast coverage triage."
        ),
    }
    params = {
        "candidate_run_id": candidate_run_id,
        "source_family": SOURCE_FAMILY,
        "source_basis": SOURCE_BASIS,
        "source_dbname": args.source_dbname,
        "source_table": "public.ecwt_raw_station",
        "period_start_year": args.period_start_year,
        "period_end_year": args.period_end_year,
        "expected_djf_hours": expected_hours,
        "duplicate_hour_count_basis": "not_recounted_from_raw_in_fast_coverage_pass",
        "invalid_temp_count_basis": "not_recounted_from_raw_in_fast_coverage_pass",
    }
    load_sql = build_load_sql(staging_dir, source_row, run_id, candidate_run_id, code_commit, params)
    sql_path = staging_dir / "load.sql"
    sql_path.write_text(load_sql, encoding="utf-8")
    run(psql_cmd(args.psql, args.host, args.port, args.dbname, args.user) + ["-f", str(sql_path)])

    db_counts = report_query_map(args.psql, args.host, args.port, args.dbname, args.user, run_id, candidate_run_id)
    report_path = args.project_root / "docs" / "noaa_weather_coverage_audit_report.md"
    render_report(
        report_path,
        run_id,
        candidate_run_id,
        code_commit,
        source_row,
        expected_hours,
        period_start_utc,
        period_end_utc,
        stats,
        db_counts,
        args.host,
        args.port,
        args.dbname,
        args.source_host,
        args.source_port,
        args.source_dbname,
    )

    print(
        json.dumps(
            {
                "run_id": run_id,
                "candidate_run_id": candidate_run_id,
                "source_file_id": source_row["source_file_id"],
                "staging_dir": str(staging_dir),
                "report_path": str(report_path),
                "expected_djf_hours": expected_hours,
                "coverage_stats": stats,
                "db_counts": db_counts,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
