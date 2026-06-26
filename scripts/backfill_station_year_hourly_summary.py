#!/usr/bin/env python3
"""Backfill maintained station-year DJF hourly summaries from weather.hourly_djf."""

from __future__ import annotations

import argparse
import csv
import io
import json
import subprocess
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path

from eop012_config import PROJECT_ROOT, PSQL

METHODOLOGY_VERSION = "eop012-ecwt-method-v0.2.0"
SESSION_WORK_MEM = "512MB"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def sql_literal(value: object) -> str:
    if value is None:
        return "null"
    text = str(value)
    return "'" + text.replace("'", "''") + "'"


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


def psql_scalar(psql: Path, host: str, port: int, dbname: str, query: str, user: str | None = None) -> str:
    result = run(psql_cmd(psql, host, port, dbname, user) + ["-At", "-c", query])
    return result.stdout.strip()


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


def git_commit_label(project_root: Path) -> str:
    try:
        result = run(["git", "-C", str(project_root), "rev-parse", "HEAD"])
        return result.stdout.strip()
    except Exception:
        return "UNCOMMITTED_WORKTREE"


def build_sql(run_id: str, code_commit: str, min_year: int, max_year: int) -> str:
    start = utc_now().isoformat(timespec="seconds")
    params = {
        "source": "weather.hourly_djf",
        "target": "weather.station_year_hourly_summary",
        "min_year": min_year,
        "max_year": max_year,
        "session_work_mem": SESSION_WORK_MEM,
        "purpose": "one-time station-local DJF summary backfill so coverage refreshes do not rescan the hourly fact table",
    }
    return f"""
\\set ON_ERROR_STOP on
begin;
set local work_mem = {sql_literal(SESSION_WORK_MEM)};

insert into audit.methodology_version (
    methodology_version,
    methodology_name,
    effective_at_utc,
    source_standard,
    notes
) values (
    {sql_literal(METHODOLOGY_VERSION)},
    'EOP012 ECWT national calculation methodology',
    {sql_literal(start)},
    'NERC EOP-012-3; EPRI 3002030362 guidance',
    'Auditable methodology version for EIA-860 assets, NOAA station/weather loading, coverage, and ECWT calculation.'
)
on conflict (methodology_version) do update set
    notes = excluded.notes;

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
    'Backfilled maintained station-year DJF hourly summaries from weather.hourly_djf.'
)
on conflict (calculation_run_id) do update set
    run_finished_at_utc = excluded.run_finished_at_utc,
    run_status = excluded.run_status,
    parameters_json = excluded.parameters_json,
    notes = excluded.notes;

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
    localized.station_id,
    extract(year from localized.hour_local_computed)::integer as source_year,
    count(*)::bigint as valid_djf_hours,
    min(localized.hour_ending_utc) as min_hour_ending_utc,
    max(localized.hour_ending_utc) as max_hour_ending_utc,
    now() as refreshed_at_utc,
    'weather.hourly_djf station-local DJF full-table backfill using station standard UTC offsets by backfill_station_year_hourly_summary.py' as source_basis
from (
    select
        hourly.station_id,
        hourly.hour_ending_utc,
        (hourly.hour_ending_utc at time zone 'UTC')
            + make_interval(hours => coalesce(station.local_standard_utc_offset_hours, 0)) as hour_local_computed
    from weather.hourly_djf hourly
    join weather.station station
      on station.station_id = hourly.station_id
) localized
where extract(year from localized.hour_local_computed)::integer between {min_year} and {max_year}
  and extract(month from localized.hour_local_computed) in (12, 1, 2)
group by localized.station_id, extract(year from localized.hour_local_computed)::integer
on conflict (station_id, source_year) do update set
    valid_djf_hours = excluded.valid_djf_hours,
    min_hour_ending_utc = excluded.min_hour_ending_utc,
    max_hour_ending_utc = excluded.max_hour_ending_utc,
    refreshed_at_utc = excluded.refreshed_at_utc,
    source_basis = excluded.source_basis;

analyze weather.station_year_hourly_summary;

commit;
"""


def report_counts(psql: Path, host: str, port: int, dbname: str, user: str | None) -> OrderedDict[str, str]:
    queries = OrderedDict(
        [
            ("summary station-years", "select count(*) from weather.station_year_hourly_summary;"),
            ("summary stations", "select count(distinct station_id) from weather.station_year_hourly_summary;"),
            ("summary valid DJF hours", "select coalesce(sum(valid_djf_hours),0) from weather.station_year_hourly_summary;"),
            ("minimum source year", "select coalesce(min(source_year)::text, '') from weather.station_year_hourly_summary;"),
            ("maximum source year", "select coalesce(max(source_year)::text, '') from weather.station_year_hourly_summary;"),
        ]
    )
    rows = OrderedDict()
    for label, query in queries.items():
        rows[label] = psql_scalar(psql, host, port, dbname, query, user)
    return rows


def render_report(
    path: Path,
    run_id: str,
    code_commit: str,
    min_year: int,
    max_year: int,
    db_counts: OrderedDict[str, str],
    by_year: list[dict[str, str]],
    host: str,
    port: int,
    dbname: str,
) -> None:
    lines = [
        "# Station-Year Hourly Summary Backfill Report",
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
        f"- Year range: `{min_year}-{max_year}`",
        "",
        "## Summary",
        "",
        "| Relation or Check | Rows / Value |",
        "| --- | ---: |",
    ]
    for label, count in db_counts.items():
        lines.append(f"| `{label}` | {count} |")
    lines.extend(["", "## Summary By Year", "", "| Year | Station-Years | Valid DJF Hours |", "| ---: | ---: | ---: |"])
    for row in by_year:
        lines.append(f"| {row['source_year']} | {row['station_years']} | {row['valid_djf_hours']} |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- This is an operational summary of canonical loaded DJF weather rows, not a final ECWT result.",
            "- The table lets station-year coverage refreshes read one row per station-local calendar year instead of rescanning `weather.hourly_djf`.",
            "- Future NOAA DJF loads refresh touched station-years in this table automatically.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--psql", type=Path, default=PSQL)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5436)
    parser.add_argument("--dbname", default="eop012")
    parser.add_argument("--user", default=None)
    parser.add_argument("--min-year", type=int, default=2000)
    parser.add_argument("--max-year", type=int, default=2025)
    args = parser.parse_args()

    if not args.psql.exists():
        raise FileNotFoundError(args.psql)
    if args.min_year > args.max_year:
        raise ValueError("--min-year must be <= --max-year")

    code_commit = git_commit_label(args.project_root)
    run_id = f"station_year_hourly_summary_backfill_{utc_now().strftime('%Y%m%dT%H%M%SZ')}"
    sql = build_sql(run_id, code_commit, args.min_year, args.max_year)
    run(psql_cmd(args.psql, args.host, args.port, args.dbname, args.user), input_text=sql)

    db_counts = report_counts(args.psql, args.host, args.port, args.dbname, args.user)
    by_year = psql_csv_query(
        args.psql,
        args.host,
        args.port,
        args.dbname,
        f"""
        select
            source_year,
            count(*) as station_years,
            coalesce(sum(valid_djf_hours), 0) as valid_djf_hours
        from weather.station_year_hourly_summary
        where source_year between {args.min_year} and {args.max_year}
        group by source_year
        order by source_year desc
        """,
        args.user,
    )
    report_path = args.project_root / "docs" / f"{run_id}_report.md"
    render_report(
        report_path,
        run_id,
        code_commit,
        args.min_year,
        args.max_year,
        db_counts,
        by_year,
        args.host,
        args.port,
        args.dbname,
    )
    print(json.dumps({"run_id": run_id, "report_path": str(report_path), "db_counts": db_counts}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
