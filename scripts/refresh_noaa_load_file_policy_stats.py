#!/usr/bin/env python3
"""Refresh NOAA load-file parser statistics under the current DJF policy.

This is for targeted cleanup of historical load-file counters when the parser
policy evolved after a file was originally loaded. It does not modify
weather.hourly_djf temperature rows.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import subprocess
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from eop012_config import PROJECT_ROOT, PSQL, STAGING_ROOT
from load_noaa_hourly_djf import parse_file

METHODOLOGY_VERSION = "eop012-ecwt-method-v0.2.0"
DEFAULT_MIN_TEMP_C = -65.0
DEFAULT_MAX_TEMP_C = 40.0
DEFAULT_REJECT_SOURCE_CODES = {"7"}

STAT_FIELDS = [
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
]


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def sql_literal(value: object) -> str:
    if value is None:
        return "null"
    return "'" + str(value).replace("'", "''") + "'"


def pg_csv_value(value: object) -> object:
    if value is None:
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


def psql_cmd(psql: Path, host: str, port: int, dbname: str, user: str | None) -> list[str]:
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
    user: str | None,
    query: str,
) -> list[dict[str, str]]:
    result = run(
        psql_cmd(psql, host, port, dbname, user)
        + ["-c", f"\\copy ({query}) to stdout with (format csv, header true)"]
    )
    return list(csv.DictReader(io.StringIO(result.stdout)))


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: pg_csv_value(row.get(field)) for field in fieldnames})


def copy_command(table: str, columns: list[str], path: Path) -> str:
    escaped_path = str(path).replace("'", "''")
    return f"\\copy {table} ({', '.join(columns)}) from '{escaped_path}' with (format csv, header true, null '\\N')"


def git_commit_label(project_root: Path) -> str:
    try:
        return run(["git", "-C", str(project_root), "rev-parse", "HEAD"]).stdout.strip()
    except Exception:
        return "UNCOMMITTED_WORKTREE"


def parse_station_year(text: str) -> tuple[str, int]:
    if ":" not in text:
        raise argparse.ArgumentTypeError("station-year must look like STATION_ID:YEAR")
    station_id, year_text = text.rsplit(":", 1)
    if not station_id:
        raise argparse.ArgumentTypeError("station-year station id cannot be blank")
    try:
        year = int(year_text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("station-year year must be an integer") from exc
    return station_id, year


def candidate_query(station_years: list[tuple[str, int]]) -> str:
    filters = []
    for station_id, source_year in station_years:
        filters.append(f"(lf.station_id = {sql_literal(station_id)} and lf.source_year = {int(source_year)})")
    where_filter = " or ".join(filters)
    return f"""
    select
        lf.load_file_id,
        lf.calculation_run_id,
        lf.station_id,
        lf.source_year::text as source_year,
        lf.raw_station_id,
        lf.local_path,
        lf.source_file_id,
        lf.file_size_bytes::text as file_size_bytes,
        lf.source_basis,
        lf.rows_seen::text as rows_seen,
        lf.djf_rows_seen::text as djf_rows_seen,
        lf.rejected_source_rows::text as rejected_source_rows,
        lf.valid_temp_rows::text as valid_temp_rows,
        lf.invalid_temp_rows::text as invalid_temp_rows,
        lf.rejected_plausibility_rows::text as rejected_plausibility_rows,
        lf.duplicate_hour_count::text as duplicate_hour_count,
        lf.loaded_hour_count::text as loaded_hour_count,
        lf.min_hour_ending_utc::text as min_hour_ending_utc,
        lf.max_hour_ending_utc::text as max_hour_ending_utc,
        lf.notes
    from weather.noaa_hourly_load_file lf
    where lf.file_status = 'loaded'
      and ({where_filter})
    order by lf.station_id, lf.source_year, lf.local_path
    """


def fetch_candidates(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    station_years: list[tuple[str, int]],
) -> list[dict[str, str]]:
    return psql_csv_query(psql, host, port, dbname, user, candidate_query(station_years))


def normalize_value(value: object) -> object:
    if value is None:
        return None
    if isinstance(value, int):
        return value
    return str(value)


def build_refresh_rows(
    run_id: str,
    load_files: list[dict[str, str]],
    reject_source_codes: set[str],
    min_temp_c: float,
    max_temp_c: float,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for file_row in load_files:
        _, stats = parse_file(file_row, run_id, reject_source_codes, min_temp_c, max_temp_c)
        changed = any(str(normalize_value(stats[field]) or "") != str(file_row.get(field) or "") for field in STAT_FIELDS)
        rows.append(
            {
                "refresh_id": f"{run_id}:load_file:{file_row['load_file_id']}",
                "calculation_run_id": run_id,
                "load_file_id": file_row["load_file_id"],
                "original_calculation_run_id": file_row["calculation_run_id"],
                "station_id": file_row["station_id"],
                "source_year": int(file_row["source_year"]),
                "source_file_id": file_row.get("source_file_id"),
                "local_path": file_row["local_path"],
                "old_rows_seen": file_row["rows_seen"],
                "new_rows_seen": stats["rows_seen"],
                "old_djf_rows_seen": file_row["djf_rows_seen"],
                "new_djf_rows_seen": stats["djf_rows_seen"],
                "old_rejected_source_rows": file_row["rejected_source_rows"],
                "new_rejected_source_rows": stats["rejected_source_rows"],
                "old_valid_temp_rows": file_row["valid_temp_rows"],
                "new_valid_temp_rows": stats["valid_temp_rows"],
                "old_invalid_temp_rows": file_row["invalid_temp_rows"],
                "new_invalid_temp_rows": stats["invalid_temp_rows"],
                "old_rejected_plausibility_rows": file_row["rejected_plausibility_rows"],
                "new_rejected_plausibility_rows": stats["rejected_plausibility_rows"],
                "old_duplicate_hour_count": file_row["duplicate_hour_count"],
                "new_duplicate_hour_count": stats["duplicate_hour_count"],
                "old_loaded_hour_count": file_row["loaded_hour_count"],
                "new_loaded_hour_count": stats["loaded_hour_count"],
                "old_min_hour_ending_utc": file_row.get("min_hour_ending_utc"),
                "new_min_hour_ending_utc": stats["min_hour_ending_utc"],
                "old_max_hour_ending_utc": file_row.get("max_hour_ending_utc"),
                "new_max_hour_ending_utc": stats["max_hour_ending_utc"],
                "changed": changed,
                "notes": "Recomputed NOAA DJF load-file counters with the current parser policy; weather.hourly_djf rows were not modified.",
            }
        )
    return rows


def build_apply_sql(
    staging_dir: Path,
    run_id: str,
    code_commit: str,
    params: dict[str, object],
    refresh_cols: list[str],
) -> str:
    return "\n".join(
        [
            "\\set ON_ERROR_STOP on",
            "begin;",
            f"""
insert into audit.methodology_version (
    methodology_version,
    methodology_name,
    effective_at_utc,
    source_standard,
    notes
) values (
    {sql_literal(METHODOLOGY_VERSION)},
    'EOP012 ECWT national calculation methodology',
    now(),
    'NERC EOP-012-3; EPRI 3002030362 guidance',
    'Initial auditable methodology version for asset loading, station matching, raw file inventory, coverage auditing, and ECWT calculation.'
)
on conflict (methodology_version) do update set notes = excluded.notes;
""",
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
    now(),
    now(),
    'succeeded',
    {sql_literal(json.dumps(params, sort_keys=True))}::jsonb,
    'Refreshed targeted NOAA load-file parser counters under the current policy without modifying canonical hourly weather rows.'
)
on conflict (calculation_run_id) do update set
    code_commit = excluded.code_commit,
    run_finished_at_utc = excluded.run_finished_at_utc,
    run_status = excluded.run_status,
    parameters_json = excluded.parameters_json,
    notes = excluded.notes;
""",
            """
create table if not exists audit.noaa_load_file_policy_refresh (
    refresh_id text primary key,
    calculation_run_id text not null references audit.calculation_run(calculation_run_id),
    load_file_id text not null,
    original_calculation_run_id text not null references audit.calculation_run(calculation_run_id),
    station_id text not null references weather.station(station_id),
    source_year integer not null,
    source_file_id text references audit.source_file(source_file_id),
    local_path text not null,
    old_rows_seen bigint,
    new_rows_seen bigint,
    old_djf_rows_seen bigint,
    new_djf_rows_seen bigint,
    old_rejected_source_rows bigint,
    new_rejected_source_rows bigint,
    old_valid_temp_rows bigint,
    new_valid_temp_rows bigint,
    old_invalid_temp_rows bigint,
    new_invalid_temp_rows bigint,
    old_rejected_plausibility_rows bigint,
    new_rejected_plausibility_rows bigint,
    old_duplicate_hour_count bigint,
    new_duplicate_hour_count bigint,
    old_loaded_hour_count bigint,
    new_loaded_hour_count bigint,
    old_min_hour_ending_utc timestamptz,
    new_min_hour_ending_utc timestamptz,
    old_max_hour_ending_utc timestamptz,
    new_max_hour_ending_utc timestamptz,
    changed boolean not null,
    notes text,
    created_at_utc timestamptz not null default now(),
    unique (calculation_run_id, load_file_id)
);
""",
            """
create temp table stg_noaa_load_file_policy_refresh (
    refresh_id text,
    calculation_run_id text,
    load_file_id text,
    original_calculation_run_id text,
    station_id text,
    source_year integer,
    source_file_id text,
    local_path text,
    old_rows_seen bigint,
    new_rows_seen bigint,
    old_djf_rows_seen bigint,
    new_djf_rows_seen bigint,
    old_rejected_source_rows bigint,
    new_rejected_source_rows bigint,
    old_valid_temp_rows bigint,
    new_valid_temp_rows bigint,
    old_invalid_temp_rows bigint,
    new_invalid_temp_rows bigint,
    old_rejected_plausibility_rows bigint,
    new_rejected_plausibility_rows bigint,
    old_duplicate_hour_count bigint,
    new_duplicate_hour_count bigint,
    old_loaded_hour_count bigint,
    new_loaded_hour_count bigint,
    old_min_hour_ending_utc timestamptz,
    new_min_hour_ending_utc timestamptz,
    old_max_hour_ending_utc timestamptz,
    new_max_hour_ending_utc timestamptz,
    changed boolean,
    notes text
) on commit drop;
""",
            copy_command("stg_noaa_load_file_policy_refresh", refresh_cols, staging_dir / "policy_refresh.csv"),
            """
insert into audit.noaa_load_file_policy_refresh (
    refresh_id,
    calculation_run_id,
    load_file_id,
    original_calculation_run_id,
    station_id,
    source_year,
    source_file_id,
    local_path,
    old_rows_seen,
    new_rows_seen,
    old_djf_rows_seen,
    new_djf_rows_seen,
    old_rejected_source_rows,
    new_rejected_source_rows,
    old_valid_temp_rows,
    new_valid_temp_rows,
    old_invalid_temp_rows,
    new_invalid_temp_rows,
    old_rejected_plausibility_rows,
    new_rejected_plausibility_rows,
    old_duplicate_hour_count,
    new_duplicate_hour_count,
    old_loaded_hour_count,
    new_loaded_hour_count,
    old_min_hour_ending_utc,
    new_min_hour_ending_utc,
    old_max_hour_ending_utc,
    new_max_hour_ending_utc,
    changed,
    notes
)
select
    refresh_id,
    calculation_run_id,
    load_file_id,
    original_calculation_run_id,
    station_id,
    source_year,
    source_file_id,
    local_path,
    old_rows_seen,
    new_rows_seen,
    old_djf_rows_seen,
    new_djf_rows_seen,
    old_rejected_source_rows,
    new_rejected_source_rows,
    old_valid_temp_rows,
    new_valid_temp_rows,
    old_invalid_temp_rows,
    new_invalid_temp_rows,
    old_rejected_plausibility_rows,
    new_rejected_plausibility_rows,
    old_duplicate_hour_count,
    new_duplicate_hour_count,
    old_loaded_hour_count,
    new_loaded_hour_count,
    old_min_hour_ending_utc,
    new_min_hour_ending_utc,
    old_max_hour_ending_utc,
    new_max_hour_ending_utc,
    changed,
    notes
from stg_noaa_load_file_policy_refresh
on conflict (calculation_run_id, load_file_id) do update set
    new_rows_seen = excluded.new_rows_seen,
    new_djf_rows_seen = excluded.new_djf_rows_seen,
    new_rejected_source_rows = excluded.new_rejected_source_rows,
    new_valid_temp_rows = excluded.new_valid_temp_rows,
    new_invalid_temp_rows = excluded.new_invalid_temp_rows,
    new_rejected_plausibility_rows = excluded.new_rejected_plausibility_rows,
    new_duplicate_hour_count = excluded.new_duplicate_hour_count,
    new_loaded_hour_count = excluded.new_loaded_hour_count,
    new_min_hour_ending_utc = excluded.new_min_hour_ending_utc,
    new_max_hour_ending_utc = excluded.new_max_hour_ending_utc,
    changed = excluded.changed,
    notes = excluded.notes;
""",
            """
update weather.noaa_hourly_load_file lf
set
    rows_seen = stg.new_rows_seen,
    djf_rows_seen = stg.new_djf_rows_seen,
    rejected_source_rows = stg.new_rejected_source_rows,
    valid_temp_rows = stg.new_valid_temp_rows,
    invalid_temp_rows = stg.new_invalid_temp_rows,
    rejected_plausibility_rows = stg.new_rejected_plausibility_rows,
    duplicate_hour_count = stg.new_duplicate_hour_count,
    loaded_hour_count = stg.new_loaded_hour_count,
    min_hour_ending_utc = stg.new_min_hour_ending_utc,
    max_hour_ending_utc = stg.new_max_hour_ending_utc,
    notes = concat_ws(' ', nullif(lf.notes, ''), 'Load-file parser counters refreshed under current NOAA DJF policy; canonical hourly rows unchanged.')
from stg_noaa_load_file_policy_refresh stg
where lf.load_file_id = stg.load_file_id
  and stg.changed;
""",
            "commit;",
        ]
    )


def render_report(
    report_path: Path,
    run_id: str,
    code_commit: str,
    station_years: list[tuple[str, int]],
    refresh_rows: list[dict[str, object]],
    dry_run: bool,
    csv_path: Path,
) -> None:
    changed_rows = [row for row in refresh_rows if str(row["changed"]).lower() == "true"]
    lines = [
        "# NOAA Load-File Policy Stats Refresh Report",
        "",
        f"Generated UTC: {utc_now().isoformat(timespec='seconds')}",
        "",
        "## Run",
        "",
        f"- Calculation run ID: `{run_id}`",
        f"- Code commit: `{code_commit}`",
        f"- Dry run: `{dry_run}`",
        f"- Station-years: `{', '.join(f'{station}:{year}' for station, year in station_years)}`",
        f"- Detail CSV: `{csv_path.name}`",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| Load-file rows checked | {len(refresh_rows)} |",
        f"| Load-file rows changed | {len(changed_rows)} |",
        "",
        "## Changed Rows",
        "",
        "| Station | Year | Old Rejects | New Rejects | Old Valid | New Valid | Old Duplicates | New Duplicates | Old Loaded Hours | New Loaded Hours |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    if changed_rows:
        for row in changed_rows:
            lines.append(
                "| "
                + " | ".join(
                    [
                        str(row["station_id"]),
                        str(row["source_year"]),
                        str(row["old_rejected_plausibility_rows"]),
                        str(row["new_rejected_plausibility_rows"]),
                        str(row["old_valid_temp_rows"]),
                        str(row["new_valid_temp_rows"]),
                        str(row["old_duplicate_hour_count"]),
                        str(row["new_duplicate_hour_count"]),
                        str(row["old_loaded_hour_count"]),
                        str(row["new_loaded_hour_count"]),
                    ]
                )
                + " |"
            )
    else:
        lines.append("|  |  |  |  |  |  |  |  |  |  |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- This refresh updates only `weather.noaa_hourly_load_file` parser counters and records old/new counters in `audit.noaa_load_file_policy_refresh`.",
            "- It does not modify `weather.hourly_djf`, station coverage, station ECWT, plant ECWT, or plant readiness rows.",
            "- The targeted rows were originally loaded before the current SHEF-specific plausibility floor was added; the refreshed counters now match the current parser policy.",
        ]
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--staging-root", type=Path, default=STAGING_ROOT)
    parser.add_argument("--psql", type=Path, default=PSQL)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5436)
    parser.add_argument("--dbname", default="eop012")
    parser.add_argument("--user")
    parser.add_argument("--station-year", action="append", type=parse_station_year, required=True)
    parser.add_argument("--min-temp-c", type=float, default=DEFAULT_MIN_TEMP_C)
    parser.add_argument("--max-temp-c", type=float, default=DEFAULT_MAX_TEMP_C)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    run_id = f"noaa_load_file_policy_refresh_{utc_now().strftime('%Y%m%dT%H%M%SZ')}"
    code_commit = git_commit_label(args.project_root)
    staging_dir = args.staging_root / run_id
    staging_dir.mkdir(parents=True, exist_ok=True)
    station_years = list(args.station_year)
    load_files = fetch_candidates(args.psql, args.host, args.port, args.dbname, args.user, station_years)
    if len(load_files) != len(station_years):
        raise RuntimeError(f"Expected {len(station_years)} load-file rows, found {len(load_files)}.")
    refresh_rows = build_refresh_rows(
        run_id,
        load_files,
        DEFAULT_REJECT_SOURCE_CODES,
        args.min_temp_c,
        args.max_temp_c,
    )

    refresh_cols = [
        "refresh_id",
        "calculation_run_id",
        "load_file_id",
        "original_calculation_run_id",
        "station_id",
        "source_year",
        "source_file_id",
        "local_path",
        "old_rows_seen",
        "new_rows_seen",
        "old_djf_rows_seen",
        "new_djf_rows_seen",
        "old_rejected_source_rows",
        "new_rejected_source_rows",
        "old_valid_temp_rows",
        "new_valid_temp_rows",
        "old_invalid_temp_rows",
        "new_invalid_temp_rows",
        "old_rejected_plausibility_rows",
        "new_rejected_plausibility_rows",
        "old_duplicate_hour_count",
        "new_duplicate_hour_count",
        "old_loaded_hour_count",
        "new_loaded_hour_count",
        "old_min_hour_ending_utc",
        "new_min_hour_ending_utc",
        "old_max_hour_ending_utc",
        "new_max_hour_ending_utc",
        "changed",
        "notes",
    ]
    write_csv(staging_dir / "policy_refresh.csv", refresh_cols, refresh_rows)
    docs_dir = args.project_root / "docs"
    csv_path = docs_dir / f"{run_id}.csv"
    report_path = docs_dir / f"{run_id}_report.md"
    write_csv(csv_path, refresh_cols, refresh_rows)

    if not args.dry_run:
        params = {
            "station_years": [f"{station}:{year}" for station, year in station_years],
            "min_temp_c": args.min_temp_c,
            "max_temp_c": args.max_temp_c,
            "reject_source_codes": sorted(DEFAULT_REJECT_SOURCE_CODES),
            "operation": "refresh weather.noaa_hourly_load_file parser counters only",
        }
        sql_path = staging_dir / "apply.sql"
        sql_path.write_text(build_apply_sql(staging_dir, run_id, code_commit, params, refresh_cols), encoding="utf-8")
        run(psql_cmd(args.psql, args.host, args.port, args.dbname, args.user) + ["-f", str(sql_path)])

    render_report(report_path, run_id, code_commit, station_years, refresh_rows, args.dry_run, csv_path)
    print(
        json.dumps(
            OrderedDict(
                [
                    ("run_id", run_id),
                    ("dry_run", args.dry_run),
                    ("load_files_checked", len(refresh_rows)),
                    ("load_files_changed", sum(1 for row in refresh_rows if row["changed"])),
                    ("csv_path", str(csv_path)),
                    ("report_path", str(report_path)),
                ]
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
