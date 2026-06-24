#!/usr/bin/env python3
"""Build provisional station ECWT from canonical loaded DJF weather."""

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


def psql_csv_query(psql: Path, host: str, port: int, dbname: str, query: str, user: str | None = None) -> list[dict[str, str]]:
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


def latest_coverage_run_id(psql: Path, host: str, port: int, dbname: str, user: str | None) -> str:
    run_id = psql_scalar(
        psql,
        host,
        port,
        dbname,
        """
        select calculation_run_id
        from audit.calculation_run
        where calculation_run_id like 'station_year_djf_coverage_%'
          and run_status = 'succeeded'
        order by run_started_at_utc desc
        limit 1
        """,
        user,
    )
    if not run_id:
        raise RuntimeError("No succeeded station_year_djf_coverage run found.")
    return run_id


def build_sql(run_id: str, coverage_run_id: str, code_commit: str, percentile_target: float) -> str:
    start = utc_now().isoformat(timespec="seconds")
    params = {
        "source": "weather.hourly_djf",
        "coverage_run_id": coverage_run_id,
        "percentile_target": percentile_target,
        "status": "provisional until station selection and full NOAA coverage are complete",
    }
    return f"""
\\set ON_ERROR_STOP on
begin;

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
    'Built provisional station ECWT from currently loaded canonical NOAA DJF rows.'
)
on conflict (calculation_run_id) do update set
    run_finished_at_utc = excluded.run_finished_at_utc,
    run_status = excluded.run_status,
    parameters_json = excluded.parameters_json,
    notes = excluded.notes;

with coverage as (
    select
        station_id,
        coalesce(sum(expected_djf_hours), 0)::bigint as expected_hour_count,
        coalesce(sum(valid_djf_hours), 0)::bigint as coverage_valid_hour_count,
        coalesce(sum(missing_hour_count), 0)::bigint as missing_hour_count,
        coalesce(sum(duplicate_hour_count), 0)::bigint as duplicate_hour_count
    from weather.station_year_djf_coverage
    where calculation_run_id = {sql_literal(coverage_run_id)}
    group by station_id
),
stats as (
    select
        station_id,
        count(*)::bigint as valid_hour_count,
        max(hour_ending_utc) as calculation_cutoff_utc,
        percentile_cont({percentile_target}) within group (order by dry_bulb_c) as ecwt_c,
        percentile_cont({percentile_target}) within group (order by dry_bulb_f) as ecwt_f,
        greatest(ceil({percentile_target} * count(*))::integer, 1) as discrete_rank
    from weather.hourly_djf
    group by station_id
),
ranked as (
    select
        station_id,
        dry_bulb_c,
        dry_bulb_f,
        row_number() over (partition by station_id order by dry_bulb_c, hour_ending_utc) as cold_rank
    from weather.hourly_djf
),
discrete as (
    select
        r.station_id,
        r.dry_bulb_c as ecwt_discrete_c,
        r.dry_bulb_f as ecwt_discrete_f
    from ranked r
    join stats s
      on s.station_id = r.station_id
     and s.discrete_rank = r.cold_rank
),
station_scope as (
    select station_id from coverage
    union
    select station_id from stats
)
insert into calc.station_ecwt (
    station_ecwt_id,
    station_id,
    calculation_run_id,
    methodology_version,
    calculation_cutoff_utc,
    valid_hour_count,
    expected_hour_count,
    missing_hour_count,
    duplicate_hour_count,
    percentile_target,
    ecwt_c,
    ecwt_f,
    discrete_rank,
    ecwt_discrete_c,
    ecwt_discrete_f,
    result_status
)
select
    {sql_literal(run_id)} || ':station:' || ss.station_id as station_ecwt_id,
    ss.station_id,
    {sql_literal(run_id)} as calculation_run_id,
    {sql_literal(METHODOLOGY_VERSION)} as methodology_version,
    coalesce(s.calculation_cutoff_utc, now()) as calculation_cutoff_utc,
    coalesce(s.valid_hour_count, 0) as valid_hour_count,
    coalesce(c.expected_hour_count, 0) as expected_hour_count,
    coalesce(c.missing_hour_count, 0) as missing_hour_count,
    coalesce(c.duplicate_hour_count, 0) as duplicate_hour_count,
    {percentile_target} as percentile_target,
    s.ecwt_c,
    s.ecwt_f,
    s.discrete_rank,
    d.ecwt_discrete_c,
    d.ecwt_discrete_f,
    case when coalesce(s.valid_hour_count, 0) = 0 then 'blocked' else 'provisional' end as result_status
from station_scope ss
left join stats s using (station_id)
left join coverage c using (station_id)
left join discrete d using (station_id)
on conflict (station_ecwt_id) do update set
    calculation_cutoff_utc = excluded.calculation_cutoff_utc,
    valid_hour_count = excluded.valid_hour_count,
    expected_hour_count = excluded.expected_hour_count,
    missing_hour_count = excluded.missing_hour_count,
    duplicate_hour_count = excluded.duplicate_hour_count,
    percentile_target = excluded.percentile_target,
    ecwt_c = excluded.ecwt_c,
    ecwt_f = excluded.ecwt_f,
    discrete_rank = excluded.discrete_rank,
    ecwt_discrete_c = excluded.ecwt_discrete_c,
    ecwt_discrete_f = excluded.ecwt_discrete_f,
    result_status = excluded.result_status;

commit;
"""


def report_counts(psql: Path, host: str, port: int, dbname: str, run_id: str, user: str | None) -> OrderedDict[str, str]:
    queries = OrderedDict(
        [
            ("station ECWT rows for this run", f"select count(*) from calc.station_ecwt where calculation_run_id = {sql_literal(run_id)};"),
            ("provisional rows", f"select count(*) from calc.station_ecwt where calculation_run_id = {sql_literal(run_id)} and result_status = 'provisional';"),
            ("blocked rows", f"select count(*) from calc.station_ecwt where calculation_run_id = {sql_literal(run_id)} and result_status = 'blocked';"),
            ("minimum ECWT F", f"select coalesce(round(min(ecwt_f), 3)::text, '') from calc.station_ecwt where calculation_run_id = {sql_literal(run_id)};"),
            ("maximum ECWT F", f"select coalesce(round(max(ecwt_f), 3)::text, '') from calc.station_ecwt where calculation_run_id = {sql_literal(run_id)};"),
        ]
    )
    rows = OrderedDict()
    for label, query in queries.items():
        rows[label] = psql_scalar(psql, host, port, dbname, query, user)
    return rows


def render_report(
    path: Path,
    run_id: str,
    coverage_run_id: str,
    code_commit: str,
    percentile_target: float,
    db_counts: OrderedDict[str, str],
    coldest: list[dict[str, str]],
    host: str,
    port: int,
    dbname: str,
) -> None:
    lines = [
        "# Provisional Station ECWT Report",
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
        f"- Coverage run ID: `{coverage_run_id}`",
        f"- Methodology version: `{METHODOLOGY_VERSION}`",
        f"- Code commit: `{code_commit}`",
        f"- Percentile target: `{percentile_target}`",
        "",
        "## Summary",
        "",
        "| Relation or Check | Rows / Value |",
        "| --- | ---: |",
    ]
    for label, count in db_counts.items():
        lines.append(f"| `{label}` | {count} |")
    lines.extend(["", "## Coldest Provisional Station ECWT Values", "", "| Station | Valid Hours | ECWT F | Discrete ECWT F | Status |", "| --- | ---: | ---: | ---: | --- |"])
    for row in coldest:
        lines.append(
            f"| `{row['station_id']}` | {row['valid_hour_count']} | {row['ecwt_f']} | {row['ecwt_discrete_f']} | {row['result_status']} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- These are station-level provisional ECWT values from the currently loaded canonical DJF table.",
            "- They are not final plant ECWT values. Plant station selection, complete coverage, and final QA must still be completed.",
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
    parser.add_argument("--coverage-run-id", default=None)
    parser.add_argument("--percentile-target", type=float, default=0.002)
    args = parser.parse_args()

    coverage_run_id = args.coverage_run_id or latest_coverage_run_id(args.psql, args.host, args.port, args.dbname, args.user)
    code_commit = git_commit_label(args.project_root)
    run_id = f"station_ecwt_loaded_{utc_now().strftime('%Y%m%dT%H%M%SZ')}"
    sql = build_sql(run_id, coverage_run_id, code_commit, args.percentile_target)
    run(psql_cmd(args.psql, args.host, args.port, args.dbname, args.user), input_text=sql)

    db_counts = report_counts(args.psql, args.host, args.port, args.dbname, run_id, args.user)
    coldest = psql_csv_query(
        args.psql,
        args.host,
        args.port,
        args.dbname,
        f"""
        select
            station_id,
            valid_hour_count,
            round(ecwt_f, 3) as ecwt_f,
            round(ecwt_discrete_f, 3) as ecwt_discrete_f,
            result_status
        from calc.station_ecwt
        where calculation_run_id = {sql_literal(run_id)}
          and ecwt_f is not null
        order by ecwt_f asc
        limit 20
        """,
        args.user,
    )
    report_path = args.project_root / "docs" / f"{run_id}_report.md"
    render_report(
        report_path,
        run_id,
        coverage_run_id,
        code_commit,
        args.percentile_target,
        db_counts,
        coldest,
        args.host,
        args.port,
        args.dbname,
    )
    print(json.dumps({"run_id": run_id, "report_path": str(report_path), "db_counts": db_counts}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
