#!/usr/bin/env python3
"""Build station-year DJF coverage from canonical loaded NOAA hourly data."""

from __future__ import annotations

import argparse
import csv
import io
import json
import subprocess
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path("/Users/Shared/EOP012/rebuild")
PSQL = Path("/opt/homebrew/opt/postgresql@16/bin/psql")
METHODOLOGY_VERSION = "eop012-ecwt-method-v0.1.0"


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


def build_sql(run_id: str, code_commit: str, min_year: int, max_year: int, complete_threshold: float) -> str:
    start = utc_now().isoformat(timespec="seconds")
    params = {
        "source": "weather.hourly_djf plus weather.noaa_hourly_load_file",
        "min_year": min_year,
        "max_year": max_year,
        "complete_threshold": complete_threshold,
        "coverage_status_rule": "complete if coverage_ratio >= threshold, partial if valid_djf_hours > 0, otherwise empty",
    }
    return f"""
\\set ON_ERROR_STOP on
begin;

create table if not exists weather.station_year_djf_coverage (
    station_year_djf_coverage_id text primary key,
    station_id text not null references weather.station(station_id),
    source_year integer not null,
    calculation_run_id text not null references audit.calculation_run(calculation_run_id),
    period_start_utc timestamptz not null,
    period_end_utc timestamptz not null,
    expected_djf_hours bigint not null,
    valid_djf_hours bigint not null,
    missing_hour_count bigint not null,
    loaded_file_count bigint not null,
    invalid_temp_row_count bigint not null,
    rejected_source_row_count bigint not null,
    rejected_plausibility_row_count bigint not null,
    duplicate_hour_count bigint not null,
    coverage_ratio numeric,
    coverage_status text not null,
    notes text,
    created_at_utc timestamptz not null default now(),
    unique (station_id, source_year, calculation_run_id),
    constraint station_year_djf_coverage_status_check
        check (coverage_status in ('complete', 'partial', 'empty'))
);
create index if not exists ix_station_year_djf_coverage_station_year
    on weather.station_year_djf_coverage (station_id, source_year);
create index if not exists ix_station_year_djf_coverage_status
    on weather.station_year_djf_coverage (calculation_run_id, coverage_status);

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
    'Built station-year DJF coverage from hardened canonical NOAA hourly rows.'
)
on conflict (calculation_run_id) do update set
    run_finished_at_utc = excluded.run_finished_at_utc,
    run_status = excluded.run_status,
    parameters_json = excluded.parameters_json,
    notes = excluded.notes;

with years as (
    select generate_series({min_year}, {max_year})::integer as source_year
),
expected as (
    select
        y.source_year,
        make_timestamptz(y.source_year, 1, 1, 0, 0, 0, 'UTC') as period_start_utc,
        make_timestamptz(y.source_year, 12, 31, 23, 0, 0, 'UTC') as period_end_utc,
        count(*) filter (where extract(month from gs.hour_utc at time zone 'UTC') in (12, 1, 2))::bigint as expected_djf_hours
    from years y
    cross join lateral generate_series(
        make_timestamptz(y.source_year, 1, 1, 0, 0, 0, 'UTC'),
        make_timestamptz(y.source_year, 12, 31, 23, 0, 0, 'UTC'),
        interval '1 hour'
    ) as gs(hour_utc)
    group by y.source_year
),
file_stats as (
    select
        station_id,
        source_year,
        count(*)::bigint as loaded_file_count,
        coalesce(sum(invalid_temp_rows), 0)::bigint as invalid_temp_row_count,
        coalesce(sum(rejected_source_rows), 0)::bigint as rejected_source_row_count,
        coalesce(sum(rejected_plausibility_rows), 0)::bigint as rejected_plausibility_row_count,
        coalesce(sum(duplicate_hour_count), 0)::bigint as duplicate_hour_count
    from weather.noaa_hourly_load_file
    where file_status = 'loaded'
      and source_year between {min_year} and {max_year}
    group by station_id, source_year
),
hourly as (
    select
        station_id,
        extract(year from hour_ending_utc at time zone 'UTC')::integer as source_year,
        count(*)::bigint as valid_djf_hours
    from weather.hourly_djf
    where extract(month from hour_ending_utc at time zone 'UTC') in (12, 1, 2)
      and extract(year from hour_ending_utc at time zone 'UTC')::integer between {min_year} and {max_year}
    group by station_id, extract(year from hour_ending_utc at time zone 'UTC')::integer
),
coverage as (
    select
        fs.station_id,
        fs.source_year,
        e.period_start_utc,
        e.period_end_utc,
        e.expected_djf_hours,
        coalesce(h.valid_djf_hours, 0)::bigint as valid_djf_hours,
        greatest(e.expected_djf_hours - coalesce(h.valid_djf_hours, 0), 0)::bigint as missing_hour_count,
        fs.loaded_file_count,
        fs.invalid_temp_row_count,
        fs.rejected_source_row_count,
        fs.rejected_plausibility_row_count,
        fs.duplicate_hour_count,
        (coalesce(h.valid_djf_hours, 0)::numeric / nullif(e.expected_djf_hours, 0)) as coverage_ratio
    from file_stats fs
    join expected e using (source_year)
    left join hourly h
      on h.station_id = fs.station_id
     and h.source_year = fs.source_year
)
insert into weather.station_year_djf_coverage (
    station_year_djf_coverage_id,
    station_id,
    source_year,
    calculation_run_id,
    period_start_utc,
    period_end_utc,
    expected_djf_hours,
    valid_djf_hours,
    missing_hour_count,
    loaded_file_count,
    invalid_temp_row_count,
    rejected_source_row_count,
    rejected_plausibility_row_count,
    duplicate_hour_count,
    coverage_ratio,
    coverage_status,
    notes
)
select
    {sql_literal(run_id)} || ':station:' || station_id || ':year:' || source_year as station_year_djf_coverage_id,
    station_id,
    source_year,
    {sql_literal(run_id)} as calculation_run_id,
    period_start_utc,
    period_end_utc,
    expected_djf_hours,
    valid_djf_hours,
    missing_hour_count,
    loaded_file_count,
    invalid_temp_row_count,
    rejected_source_row_count,
    rejected_plausibility_row_count,
    duplicate_hour_count,
    coverage_ratio,
    case
        when valid_djf_hours = 0 then 'empty'
        when coverage_ratio >= {complete_threshold} then 'complete'
        else 'partial'
    end as coverage_status,
    'Coverage built from hardened canonical NOAA DJF rows. SOURCE=7 rows are rejected by the current loader default.' as notes
from coverage
on conflict (station_id, source_year, calculation_run_id) do update set
    expected_djf_hours = excluded.expected_djf_hours,
    valid_djf_hours = excluded.valid_djf_hours,
    missing_hour_count = excluded.missing_hour_count,
    loaded_file_count = excluded.loaded_file_count,
    invalid_temp_row_count = excluded.invalid_temp_row_count,
    rejected_source_row_count = excluded.rejected_source_row_count,
    rejected_plausibility_row_count = excluded.rejected_plausibility_row_count,
    duplicate_hour_count = excluded.duplicate_hour_count,
    coverage_ratio = excluded.coverage_ratio,
    coverage_status = excluded.coverage_status,
    notes = excluded.notes;

commit;
"""


def report_counts(psql: Path, host: str, port: int, dbname: str, run_id: str, user: str | None) -> OrderedDict[str, str]:
    queries = OrderedDict(
        [
            (
                "coverage rows for this run",
                f"select count(*) from weather.station_year_djf_coverage where calculation_run_id = {sql_literal(run_id)};",
            ),
            (
                "complete station-years",
                f"select count(*) from weather.station_year_djf_coverage where calculation_run_id = {sql_literal(run_id)} and coverage_status = 'complete';",
            ),
            (
                "partial station-years",
                f"select count(*) from weather.station_year_djf_coverage where calculation_run_id = {sql_literal(run_id)} and coverage_status = 'partial';",
            ),
            (
                "empty station-years",
                f"select count(*) from weather.station_year_djf_coverage where calculation_run_id = {sql_literal(run_id)} and coverage_status = 'empty';",
            ),
            (
                "valid DJF hours represented",
                f"select coalesce(sum(valid_djf_hours),0) from weather.station_year_djf_coverage where calculation_run_id = {sql_literal(run_id)};",
            ),
            (
                "rejected source rows represented",
                f"select coalesce(sum(rejected_source_row_count),0) from weather.station_year_djf_coverage where calculation_run_id = {sql_literal(run_id)};",
            ),
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
    complete_threshold: float,
    db_counts: OrderedDict[str, str],
    by_year: list[dict[str, str]],
    host: str,
    port: int,
    dbname: str,
) -> None:
    lines = [
        "# Station-Year DJF Coverage Report",
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
        f"- Complete threshold: `{complete_threshold}`",
        "",
        "## Summary",
        "",
        "| Relation or Check | Rows / Value |",
        "| --- | ---: |",
    ]
    for label, count in db_counts.items():
        lines.append(f"| `{label}` | {count} |")
    lines.extend(["", "## Coverage By Year", "", "| Year | Complete | Partial | Empty | Valid DJF Hours |", "| ---: | ---: | ---: | ---: | ---: |"])
    for row in by_year:
        lines.append(
            f"| {row['source_year']} | {row['complete']} | {row['partial']} | {row['empty']} | {row['valid_djf_hours']} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- This is station-year coverage for the currently loaded canonical DJF table, not final plant ECWT.",
            "- `complete` means `coverage_ratio >= complete_threshold`; this run uses the configured threshold above.",
            "- Coverage will change as more NOAA files are downloaded and loaded.",
            "",
        ]
    )
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
    parser.add_argument("--complete-threshold", type=float, default=0.95)
    args = parser.parse_args()

    code_commit = git_commit_label(args.project_root)
    run_id = f"station_year_djf_coverage_{utc_now().strftime('%Y%m%dT%H%M%SZ')}"
    sql = build_sql(run_id, code_commit, args.min_year, args.max_year, args.complete_threshold)
    run(psql_cmd(args.psql, args.host, args.port, args.dbname, args.user), input_text=sql)

    db_counts = report_counts(args.psql, args.host, args.port, args.dbname, run_id, args.user)
    by_year = psql_csv_query(
        args.psql,
        args.host,
        args.port,
        args.dbname,
        f"""
        select
            source_year,
            count(*) filter (where coverage_status = 'complete') as complete,
            count(*) filter (where coverage_status = 'partial') as partial,
            count(*) filter (where coverage_status = 'empty') as empty,
            coalesce(sum(valid_djf_hours), 0) as valid_djf_hours
        from weather.station_year_djf_coverage
        where calculation_run_id = {sql_literal(run_id)}
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
        args.complete_threshold,
        db_counts,
        by_year,
        args.host,
        args.port,
        args.dbname,
    )
    print(
        json.dumps(
            {
                "run_id": run_id,
                "report_path": str(report_path),
                "db_counts": db_counts,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
