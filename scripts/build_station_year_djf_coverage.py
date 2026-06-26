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

from eop012_config import PROJECT_ROOT, PSQL

METHODOLOGY_VERSION = "eop012-ecwt-method-v0.2.0"
SESSION_WORK_MEM = "256MB"


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


def build_sql(
    run_id: str,
    code_commit: str,
    min_year: int,
    max_year: int,
    complete_threshold: float,
    snapshot_mode: str,
) -> str:
    start = utc_now().isoformat(timespec="seconds")
    if snapshot_mode not in {"current", "historical"}:
        raise ValueError("snapshot_mode must be current or historical")
    target_table = (
        "weather.station_year_djf_coverage_current"
        if snapshot_mode == "current"
        else "weather.station_year_djf_coverage"
    )
    prepare_target_sql = (
        "truncate table weather.station_year_djf_coverage_current;"
        if snapshot_mode == "current"
        else f"delete from weather.station_year_djf_coverage where calculation_run_id = {sql_literal(run_id)};"
    )
    params = {
        "source": "weather.station_year_hourly_summary plus weather.noaa_hourly_load_file",
        "min_year": min_year,
        "max_year": max_year,
        "complete_threshold": complete_threshold,
        "session_work_mem": SESSION_WORK_MEM,
        "snapshot_mode": snapshot_mode,
        "target_table": target_table,
        "coverage_status_rule": "complete if station-local DJF coverage_ratio >= threshold, partial if valid_djf_hours > 0, otherwise empty",
    }
    return f"""
\\set ON_ERROR_STOP on
begin;
set local work_mem = {sql_literal(SESSION_WORK_MEM)};

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

do $$
begin
    if exists (
        select 1
        from weather.noaa_hourly_load_file
        where file_status = 'loaded'
          and source_year between {min_year} and {max_year}
    )
    and not exists (
        select 1
        from weather.station_year_hourly_summary
        where source_year between {min_year} and {max_year}
    ) then
        raise exception 'weather.station_year_hourly_summary is empty for loaded NOAA files; run scripts/backfill_station_year_hourly_summary.py first';
    end if;
end $$;

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
create index if not exists ix_station_year_djf_coverage_run_station_year
    on weather.station_year_djf_coverage (calculation_run_id, station_id, source_year);
create index if not exists ix_station_year_djf_coverage_status
    on weather.station_year_djf_coverage (calculation_run_id, coverage_status);
create index if not exists ix_noaa_hourly_load_file_status_year_station
    on weather.noaa_hourly_load_file (file_status, source_year, station_id);

create table if not exists weather.station_year_djf_coverage_current (
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
    unique (station_id, source_year),
    constraint station_year_djf_coverage_current_status_check
        check (coverage_status in ('complete', 'partial', 'empty'))
);
create index if not exists ix_station_year_djf_coverage_current_run_station_year
    on weather.station_year_djf_coverage_current (calculation_run_id, station_id, source_year);
create index if not exists ix_station_year_djf_coverage_current_status
    on weather.station_year_djf_coverage_current (calculation_run_id, coverage_status);

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
    'Built station-year DJF coverage from maintained NOAA hourly station-year summaries.'
)
on conflict (calculation_run_id) do update set
    run_finished_at_utc = excluded.run_finished_at_utc,
    run_status = excluded.run_status,
    parameters_json = excluded.parameters_json,
    notes = excluded.notes;

{prepare_target_sql}

with years as (
    select generate_series({min_year}, {max_year})::integer as source_year
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
hourly_summary as (
    select
        station_id,
        source_year,
        valid_djf_hours
    from weather.station_year_hourly_summary
    where source_year between {min_year} and {max_year}
),
station_year_scope as (
    select station_id, source_year from file_stats
    union
    select station_id, source_year from hourly_summary
),
station_year_offsets as (
    select
        sys.station_id,
        sys.source_year,
        coalesce(
            st.local_standard_utc_offset_hours,
            greatest(-12, least(14, round(st.longitude / 15.0)::integer)),
            0
        ) as local_standard_utc_offset_hours
    from station_year_scope sys
    join weather.station st
      on st.station_id = sys.station_id
    join years y
      on y.source_year = sys.source_year
),
expected as (
    select
        syo.station_id,
        syo.source_year,
        make_timestamptz(syo.source_year, 1, 1, 0, 0, 0.0, 'UTC')
            - make_interval(hours => syo.local_standard_utc_offset_hours) as period_start_utc,
        make_timestamptz(syo.source_year + 1, 1, 1, 0, 0, 0.0, 'UTC')
            - make_interval(hours => syo.local_standard_utc_offset_hours)
            - interval '1 hour' as period_end_utc,
        count(*) filter (
            where extract(month from gs.hour_utc + make_interval(hours => syo.local_standard_utc_offset_hours)) in (12, 1, 2)
        )::bigint as expected_djf_hours
    from station_year_offsets syo
    cross join lateral generate_series(
        make_timestamptz(syo.source_year, 1, 1, 0, 0, 0.0, 'UTC')
            - make_interval(hours => syo.local_standard_utc_offset_hours),
        make_timestamptz(syo.source_year + 1, 1, 1, 0, 0, 0.0, 'UTC')
            - make_interval(hours => syo.local_standard_utc_offset_hours)
            - interval '1 hour',
        interval '1 hour'
    ) as gs(hour_utc)
    group by syo.station_id, syo.source_year, syo.local_standard_utc_offset_hours
),
coverage as (
    select
        sys.station_id,
        sys.source_year,
        e.period_start_utc,
        e.period_end_utc,
        e.expected_djf_hours,
        coalesce(h.valid_djf_hours, 0)::bigint as valid_djf_hours,
        greatest(e.expected_djf_hours - coalesce(h.valid_djf_hours, 0), 0)::bigint as missing_hour_count,
        coalesce(fs.loaded_file_count, 0)::bigint as loaded_file_count,
        coalesce(fs.invalid_temp_row_count, 0)::bigint as invalid_temp_row_count,
        coalesce(fs.rejected_source_row_count, 0)::bigint as rejected_source_row_count,
        coalesce(fs.rejected_plausibility_row_count, 0)::bigint as rejected_plausibility_row_count,
        coalesce(fs.duplicate_hour_count, 0)::bigint as duplicate_hour_count,
        (coalesce(h.valid_djf_hours, 0)::numeric / nullif(e.expected_djf_hours, 0)) as coverage_ratio
    from station_year_scope sys
    join expected e
      on e.station_id = sys.station_id
     and e.source_year = sys.source_year
    left join file_stats fs
      on fs.station_id = sys.station_id
     and fs.source_year = sys.source_year
    left join hourly_summary h
      on h.station_id = sys.station_id
     and h.source_year = sys.source_year
)
insert into {target_table} (
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
    'Coverage built from maintained station-local weather.station_year_hourly_summary rows. SOURCE=7 rows are rejected by the current loader default.' as notes
from coverage
;

commit;
"""


def report_counts(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    run_id: str,
    user: str | None,
    coverage_table: str,
) -> OrderedDict[str, str]:
    queries = OrderedDict(
        [
            (
                "coverage rows for this run",
                f"select count(*) from {coverage_table} where calculation_run_id = {sql_literal(run_id)};",
            ),
            (
                "complete station-years",
                f"select count(*) from {coverage_table} where calculation_run_id = {sql_literal(run_id)} and coverage_status = 'complete';",
            ),
            (
                "partial station-years",
                f"select count(*) from {coverage_table} where calculation_run_id = {sql_literal(run_id)} and coverage_status = 'partial';",
            ),
            (
                "empty station-years",
                f"select count(*) from {coverage_table} where calculation_run_id = {sql_literal(run_id)} and coverage_status = 'empty';",
            ),
            (
                "valid DJF hours represented",
                f"select coalesce(sum(valid_djf_hours),0) from {coverage_table} where calculation_run_id = {sql_literal(run_id)};",
            ),
            (
                "rejected source rows represented",
                f"select coalesce(sum(rejected_source_row_count),0) from {coverage_table} where calculation_run_id = {sql_literal(run_id)};",
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
    snapshot_mode: str,
    coverage_table: str,
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
        f"- Snapshot mode: `{snapshot_mode}`",
        f"- Coverage table: `{coverage_table}`",
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
            "- This is station-year coverage for the currently loaded canonical station-local DJF table, not final plant ECWT.",
            "- Valid-hour counts are read from `weather.station_year_hourly_summary`, which is maintained by the NOAA DJF loader and can be backfilled from `weather.hourly_djf` for existing rows.",
            "- Expected-hour counts use each station's `local_standard_utc_offset_hours`; UTC timestamps remain the storage key.",
            "- `current` snapshot mode replaces the compact operational coverage table; `historical` mode appends a milestone snapshot to the full audit table.",
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
    parser.add_argument(
        "--snapshot-mode",
        choices=["current", "historical"],
        default="current",
        help="Write compact replaceable current coverage for batch loops, or append a historical milestone snapshot.",
    )
    args = parser.parse_args()

    code_commit = git_commit_label(args.project_root)
    run_id = f"station_year_djf_coverage_{utc_now().strftime('%Y%m%dT%H%M%SZ')}"
    coverage_table = (
        "weather.station_year_djf_coverage_current"
        if args.snapshot_mode == "current"
        else "weather.station_year_djf_coverage"
    )
    sql = build_sql(run_id, code_commit, args.min_year, args.max_year, args.complete_threshold, args.snapshot_mode)
    run(psql_cmd(args.psql, args.host, args.port, args.dbname, args.user), input_text=sql)

    db_counts = report_counts(args.psql, args.host, args.port, args.dbname, run_id, args.user, coverage_table)
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
        from {coverage_table}
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
        args.snapshot_mode,
        coverage_table,
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
