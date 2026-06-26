#!/usr/bin/env python3
"""Build provisional plant ECWT from candidate stations and station ECWT."""

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


def latest_run_id(psql: Path, host: str, port: int, dbname: str, pattern: str, user: str | None) -> str:
    run_id = psql_scalar(
        psql,
        host,
        port,
        dbname,
        f"""
        select calculation_run_id
        from audit.calculation_run
        where calculation_run_id like {sql_literal(pattern)}
          and run_status = 'succeeded'
        order by run_started_at_utc desc
        limit 1
        """,
        user,
    )
    if not run_id:
        raise RuntimeError(f"No succeeded calculation run found for pattern {pattern}.")
    return run_id


def run_parameters(psql: Path, host: str, port: int, dbname: str, run_id: str, user: str | None) -> dict[str, object]:
    params = psql_scalar(
        psql,
        host,
        port,
        dbname,
        f"""
        select coalesce(parameters_json::text, '{{}}')
        from audit.calculation_run
        where calculation_run_id = {sql_literal(run_id)}
        """,
        user,
    )
    if not params:
        raise RuntimeError(f"Calculation run not found: {run_id}")
    return json.loads(params)


def relation_exists(psql: Path, host: str, port: int, dbname: str, relation_name: str, user: str | None) -> bool:
    exists = psql_scalar(
        psql,
        host,
        port,
        dbname,
        f"select to_regclass({sql_literal(relation_name)}) is not null;",
        user,
    )
    return exists.lower() == "t"


def coverage_row_count(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    coverage_run_id: str,
    coverage_table: str,
    user: str | None,
) -> int:
    return int(
        psql_scalar(
            psql,
            host,
            port,
            dbname,
            f"select count(*) from {coverage_table} where calculation_run_id = {sql_literal(coverage_run_id)};",
            user,
        )
        or "0"
    )


def resolve_coverage_table(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    coverage_run_id: str,
    coverage_source: str,
    preferred_table: str | None,
    user: str | None,
) -> str:
    valid_tables = {
        "weather.station_year_djf_coverage",
        "weather.station_year_djf_coverage_current",
    }
    if coverage_source == "history":
        return "weather.station_year_djf_coverage"
    if coverage_source == "current":
        return "weather.station_year_djf_coverage_current"
    if preferred_table in valid_tables and relation_exists(psql, host, port, dbname, preferred_table, user):
        if coverage_row_count(psql, host, port, dbname, coverage_run_id, preferred_table, user) > 0:
            return preferred_table
    current_table = "weather.station_year_djf_coverage_current"
    if relation_exists(psql, host, port, dbname, current_table, user) and coverage_row_count(
        psql, host, port, dbname, coverage_run_id, current_table, user
    ) > 0:
        return current_table
    return "weather.station_year_djf_coverage"


def build_sql(
    run_id: str,
    candidate_run_id: str,
    station_ecwt_run_id: str,
    coverage_run_id: str,
    coverage_table: str,
    code_commit: str,
    selection_coverage_policy: str,
    fixed_min_year: int,
    fixed_max_year: int,
    fixed_min_coverage_ratio: float,
    fixed_min_loaded_years: int,
) -> str:
    start = utc_now().isoformat(timespec="seconds")
    if coverage_table not in {"weather.station_year_djf_coverage", "weather.station_year_djf_coverage_current"}:
        raise ValueError("Unexpected coverage table.")
    fixed_policy = selection_coverage_policy == "fixed-period"
    if fixed_policy:
        valid_hour_expr = "coalesce(sf.fixed_valid_djf_hours, 0)"
        expected_hour_expr = "coalesce(sf.fixed_expected_djf_hours, 0)"
        missing_hour_expr = "coalesce(sf.fixed_missing_djf_hours, 0)"
        duplicate_hour_expr = "coalesce(sf.fixed_duplicate_hour_count, 0)"
        coverage_filter = (
            f"      and sf.fixed_coverage_ratio >= {fixed_min_coverage_ratio}\n"
            f"      and sf.loaded_station_year_count >= {fixed_min_loaded_years}"
        )
        coverage_span_sql = f"""
coverage_span as (
	    select
	        station_id,
	        make_timestamptz({fixed_min_year}, 1, 1, 0, 0, 0.0, 'UTC') as segment_start_utc,
	        make_timestamptz({fixed_max_year}, 12, 31, 23, 0, 0.0, 'UTC') as segment_end_utc
	    from station_fixed_coverage
	)"""
        selection_rule = (
            "For each plant, choose the lowest rank_order candidate station with provisional station ECWT "
            f"and fixed-period DJF coverage >= {fixed_min_coverage_ratio} across {fixed_min_year}-{fixed_max_year}; "
            "ties use shortest distance_km, largest fixed-period valid DJF hours, then station_id."
        )
        result_status = "provisional only when a candidate station passes fixed-period coverage eligibility, otherwise blocked"
        success_note = "Selected lowest-rank fixed-period eligible candidate station; ties use distance, fixed-period valid DJF hours, and station id."
        segment_note = "Selected from fixed-period eligible station ECWT candidates by candidate rank, distance, valid-hour count, and station id."
        blocked_basis = "No candidate station currently has provisional station ECWT and fixed-period coverage eligibility under the loaded weather set."
        blocked_note = "Blocked until more NOAA weather is downloaded/loaded or a different candidate station passes the fixed-period coverage gate."
    else:
        valid_hour_expr = "se.valid_hour_count"
        expected_hour_expr = "se.expected_hour_count"
        missing_hour_expr = "se.missing_hour_count"
        duplicate_hour_expr = "se.duplicate_hour_count"
        coverage_filter = ""
        coverage_span_sql = f"""
coverage_span as (
    select
        station_id,
	        min(period_start_utc) as segment_start_utc,
	        max(period_end_utc) as segment_end_utc
	    from {coverage_table}
	    where calculation_run_id = {sql_literal(coverage_run_id)}
	    group by station_id
	)"""
        selection_rule = (
            "For each plant, choose the lowest rank_order candidate station with provisional station ECWT; "
            "ties use shortest distance_km, largest valid_hour_count, then station_id."
        )
        result_status = "provisional unless no candidate station has provisional station ECWT, then blocked"
        success_note = "Selected lowest-rank candidate station among provisional station ECWT results; ties use distance, loaded valid DJF hours, and station id."
        segment_note = "Selected from loaded station ECWT candidates by candidate rank, distance, valid-hour count, and station id."
        blocked_basis = "No candidate station currently has provisional station ECWT under the loaded weather set."
        blocked_note = "Blocked until more NOAA weather is downloaded/loaded or candidate coverage improves."
    params = {
        "candidate_run_id": candidate_run_id,
        "station_ecwt_run_id": station_ecwt_run_id,
        "coverage_run_id": coverage_run_id,
        "coverage_table": coverage_table,
        "selection_coverage_policy": selection_coverage_policy,
        "fixed_min_year": fixed_min_year,
        "fixed_max_year": fixed_max_year,
        "fixed_min_coverage_ratio": fixed_min_coverage_ratio,
        "fixed_min_loaded_years": fixed_min_loaded_years,
        "selection_rule": selection_rule,
        "result_status": result_status,
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
    'Built provisional plant station selections and plant ECWT from latest loaded station ECWT.'
)
on conflict (calculation_run_id) do update set
    run_finished_at_utc = excluded.run_finished_at_utc,
    run_status = excluded.run_status,
    parameters_json = excluded.parameters_json,
    notes = excluded.notes;

create temp table tmp_best_plant_station as
with fixed_years as (
    select generate_series({fixed_min_year}, {fixed_max_year})::integer as source_year
),
fixed_expected_by_year as (
    select
        y.source_year,
        count(*) filter (
            where extract(month from gs.hour_utc at time zone 'UTC') in (12, 1, 2)
        )::bigint as expected_djf_hours
	    from fixed_years y
	    cross join lateral generate_series(
	        make_timestamptz(y.source_year, 1, 1, 0, 0, 0.0, 'UTC'),
	        make_timestamptz(y.source_year, 12, 31, 23, 0, 0.0, 'UTC'),
	        interval '1 hour'
	    ) as gs(hour_utc)
    group by y.source_year
),
station_fixed_coverage as (
    select
        se.station_id,
        sum(e.expected_djf_hours)::bigint as fixed_expected_djf_hours,
        coalesce(sum(c.valid_djf_hours), 0)::bigint as fixed_valid_djf_hours,
        greatest(sum(e.expected_djf_hours) - coalesce(sum(c.valid_djf_hours), 0), 0)::bigint as fixed_missing_djf_hours,
        coalesce(sum(c.duplicate_hour_count), 0)::bigint as fixed_duplicate_hour_count,
        count(c.*) filter (where c.loaded_file_count > 0)::integer as loaded_station_year_count,
        count(c.*) filter (where c.coverage_status = 'complete')::integer as complete_station_year_count,
        min(c.source_year) filter (where c.loaded_file_count > 0) as first_loaded_year,
        max(c.source_year) filter (where c.loaded_file_count > 0) as last_loaded_year,
        coalesce(sum(c.valid_djf_hours), 0)::numeric / nullif(sum(e.expected_djf_hours), 0) as fixed_coverage_ratio
    from calc.station_ecwt se
    cross join fixed_expected_by_year e
	    left join {coverage_table} c
	      on c.calculation_run_id = {sql_literal(coverage_run_id)}
	     and c.station_id = se.station_id
	     and c.source_year = e.source_year
    where se.calculation_run_id = {sql_literal(station_ecwt_run_id)}
      and se.result_status = 'provisional'
    group by se.station_id
),
candidate_scores as (
    select
        sc.plant_id,
        sc.station_id,
        sc.distance_km,
        sc.rank_order,
        se.station_ecwt_id,
        {valid_hour_expr}::bigint as valid_hour_count,
        {expected_hour_expr}::bigint as expected_hour_count,
        {missing_hour_expr}::bigint as missing_hour_count,
        {duplicate_hour_expr}::bigint as duplicate_hour_count,
        se.percentile_target,
        se.ecwt_c,
        se.ecwt_f,
        se.discrete_rank,
        se.ecwt_discrete_c,
        se.ecwt_discrete_f,
        se.calculation_cutoff_utc,
        se.result_status as station_ecwt_status,
        sf.fixed_expected_djf_hours,
        sf.fixed_valid_djf_hours,
        sf.fixed_missing_djf_hours,
        sf.fixed_coverage_ratio,
        sf.loaded_station_year_count,
        sf.complete_station_year_count,
        sf.first_loaded_year,
        sf.last_loaded_year,
        row_number() over (
            partition by sc.plant_id
            order by
                sc.rank_order asc nulls last,
                sc.distance_km asc nulls last,
                {valid_hour_expr} desc nulls last,
                sc.station_id asc
        ) as selection_rank
    from link.station_candidate sc
    join calc.station_ecwt se
      on se.station_id = sc.station_id
     and se.calculation_run_id = {sql_literal(station_ecwt_run_id)}
     and se.result_status = 'provisional'
     and se.valid_hour_count > 0
    join station_fixed_coverage sf
      on sf.station_id = sc.station_id
    where sc.calculation_run_id = {sql_literal(candidate_run_id)}
      and sc.candidate_status = 'candidate'
{coverage_filter}
),
{coverage_span_sql}
select
	    cs.*,
	    coalesce(cspan.segment_start_utc, make_timestamptz(2000, 1, 1, 0, 0, 0.0, 'UTC')) as segment_start_utc,
	    coalesce(cspan.segment_end_utc, cs.calculation_cutoff_utc) as segment_end_utc
from candidate_scores cs
left join coverage_span cspan using (station_id)
where cs.selection_rank = 1;

insert into link.station_selection (
    station_selection_id,
    plant_id,
    calculation_run_id,
    methodology_version,
    selection_status,
    decision_basis,
    reviewer,
    notes
)
select
    {sql_literal(run_id)} || ':plant:' || p.plant_id as station_selection_id,
    p.plant_id,
    {sql_literal(run_id)} as calculation_run_id,
    {sql_literal(METHODOLOGY_VERSION)} as methodology_version,
    case when b.station_id is null then 'blocked' else 'provisional' end as selection_status,
    case
        when b.station_id is null then {sql_literal(blocked_basis)}
        else {sql_literal(success_note)}
    end as decision_basis,
    null as reviewer,
    case
        when b.station_id is null then {sql_literal(blocked_note)}
        else 'Provisional algorithmic selection. May change as NOAA backfill and canonical loading continue.'
    end as notes
from asset.plant p
left join tmp_best_plant_station b using (plant_id)
on conflict (station_selection_id) do update set
    selection_status = excluded.selection_status,
    decision_basis = excluded.decision_basis,
    notes = excluded.notes;

insert into link.station_selection_segment (
    station_selection_segment_id,
    station_selection_id,
    station_id,
    segment_start_utc,
    segment_end_utc,
    reason_code,
    notes
)
select
    {sql_literal(run_id)} || ':plant:' || b.plant_id || ':station:' || b.station_id as station_selection_segment_id,
    {sql_literal(run_id)} || ':plant:' || b.plant_id as station_selection_id,
    b.station_id,
    b.segment_start_utc,
    b.segment_end_utc,
    case
        when {sql_literal(selection_coverage_policy)} = 'fixed-period' then 'provisional_fixed_period_eligible_candidate'
        else 'provisional_ranked_representative_candidate'
    end,
    {sql_literal(segment_note)}
from tmp_best_plant_station b
on conflict (station_selection_segment_id) do update set
    station_id = excluded.station_id,
    segment_start_utc = excluded.segment_start_utc,
    segment_end_utc = excluded.segment_end_utc,
    reason_code = excluded.reason_code,
    notes = excluded.notes;

insert into calc.plant_ecwt (
    plant_ecwt_id,
    plant_id,
    station_selection_id,
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
    governing_ecwt_f,
    result_status
)
select
    {sql_literal(run_id)} || ':plant:' || p.plant_id as plant_ecwt_id,
    p.plant_id,
    {sql_literal(run_id)} || ':plant:' || p.plant_id as station_selection_id,
    {sql_literal(run_id)} as calculation_run_id,
    {sql_literal(METHODOLOGY_VERSION)} as methodology_version,
    coalesce(b.calculation_cutoff_utc, now()) as calculation_cutoff_utc,
    coalesce(b.valid_hour_count, 0) as valid_hour_count,
    coalesce(b.expected_hour_count, 0) as expected_hour_count,
    coalesce(b.missing_hour_count, 0) as missing_hour_count,
    coalesce(b.duplicate_hour_count, 0) as duplicate_hour_count,
    coalesce(b.percentile_target, 0.002) as percentile_target,
    b.ecwt_c,
    b.ecwt_f,
    b.discrete_rank,
    b.ecwt_discrete_c,
    b.ecwt_discrete_f,
    b.ecwt_f as governing_ecwt_f,
    case when b.station_id is null then 'blocked' else 'provisional' end as result_status
from asset.plant p
left join tmp_best_plant_station b using (plant_id)
on conflict (plant_ecwt_id) do update set
    station_selection_id = excluded.station_selection_id,
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
    governing_ecwt_f = excluded.governing_ecwt_f,
    result_status = excluded.result_status;

commit;
"""


def report_counts(psql: Path, host: str, port: int, dbname: str, run_id: str, user: str | None) -> OrderedDict[str, str]:
    queries = OrderedDict(
        [
            ("station selections", f"select count(*) from link.station_selection where calculation_run_id = {sql_literal(run_id)};"),
            ("provisional selections", f"select count(*) from link.station_selection where calculation_run_id = {sql_literal(run_id)} and selection_status = 'provisional';"),
            ("blocked selections", f"select count(*) from link.station_selection where calculation_run_id = {sql_literal(run_id)} and selection_status = 'blocked';"),
            ("selection segments", f"select count(*) from link.station_selection_segment s join link.station_selection ss using (station_selection_id) where ss.calculation_run_id = {sql_literal(run_id)};"),
            ("plant ECWT rows", f"select count(*) from calc.plant_ecwt where calculation_run_id = {sql_literal(run_id)};"),
            ("provisional plant ECWT rows", f"select count(*) from calc.plant_ecwt where calculation_run_id = {sql_literal(run_id)} and result_status = 'provisional';"),
            ("blocked plant ECWT rows", f"select count(*) from calc.plant_ecwt where calculation_run_id = {sql_literal(run_id)} and result_status = 'blocked';"),
            ("minimum plant ECWT F", f"select coalesce(round(min(ecwt_f), 1)::text, '') from calc.plant_ecwt where calculation_run_id = {sql_literal(run_id)};"),
            ("maximum plant ECWT F", f"select coalesce(round(max(ecwt_f), 1)::text, '') from calc.plant_ecwt where calculation_run_id = {sql_literal(run_id)};"),
        ]
    )
    rows = OrderedDict()
    for label, query in queries.items():
        rows[label] = psql_scalar(psql, host, port, dbname, query, user)
    return rows


def render_report(
    path: Path,
    run_id: str,
    candidate_run_id: str,
    station_ecwt_run_id: str,
    coverage_run_id: str,
    coverage_table: str,
    selection_coverage_policy: str,
    fixed_min_year: int,
    fixed_max_year: int,
    fixed_min_coverage_ratio: float,
    fixed_min_loaded_years: int,
    code_commit: str,
    db_counts: OrderedDict[str, str],
    sample_rows: list[dict[str, str]],
    host: str,
    port: int,
    dbname: str,
) -> None:
    lines = [
        "# Provisional Plant ECWT Report",
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
        f"- Candidate run ID: `{candidate_run_id}`",
        f"- Station ECWT run ID: `{station_ecwt_run_id}`",
        f"- Coverage run ID: `{coverage_run_id}`",
        f"- Coverage table: `{coverage_table}`",
        f"- Selection coverage policy: `{selection_coverage_policy}`",
        f"- Fixed-period coverage years: `{fixed_min_year}-{fixed_max_year}`",
        f"- Fixed-period minimum coverage ratio: `{fixed_min_coverage_ratio}`",
        f"- Fixed-period minimum loaded years: `{fixed_min_loaded_years}`",
        f"- Methodology version: `{METHODOLOGY_VERSION}`",
        f"- Code commit: `{code_commit}`",
        "",
        "## Summary",
        "",
        "| Relation or Check | Rows / Value |",
        "| --- | ---: |",
    ]
    for label, count in db_counts.items():
        lines.append(f"| `{label}` | {count} |")
    lines.extend(
        [
            "",
            "## Coldest Provisional Plant ECWT Values",
            "",
            "| Plant | State | Selected Station | Valid Hours | ECWT F | Status |",
            "| --- | --- | --- | ---: | ---: | --- |",
        ]
    )
    for row in sample_rows:
        lines.append(
            f"| {row['plant_name']} | {row['state'] or ''} | `{row['station_id']}` | {row['valid_hour_count']} | {row['ecwt_f']} | {row['result_status']} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- These are provisional plant-level ECWT values from the currently loaded canonical weather set.",
            "- Selection chooses one currently usable candidate station per plant using candidate rank and distance before valid-hour count.",
            "- When `selection_coverage_policy` is `fixed-period`, candidates must also pass the fixed-period coverage gate before they are eligible for selection.",
            "- Results are blocked where no candidate station currently has provisional station ECWT.",
            "- These rows are not final compliance publication values until NOAA coverage, source QA, and station-selection review are complete.",
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
    parser.add_argument("--candidate-run-id", default=None)
    parser.add_argument("--station-ecwt-run-id", default=None)
    parser.add_argument("--coverage-run-id", default=None)
    parser.add_argument(
        "--coverage-source",
        choices=["auto", "current", "history"],
        default="auto",
        help="Coverage relation to read. Auto prefers the station ECWT run's coverage table, then compact current coverage.",
    )
    parser.add_argument("--selection-coverage-policy", choices=["active-window", "fixed-period"], default="active-window")
    parser.add_argument("--fixed-min-year", type=int, default=2000)
    parser.add_argument("--fixed-max-year", type=int, default=2025)
    parser.add_argument("--fixed-min-coverage-ratio", type=float, default=0.95)
    parser.add_argument("--fixed-min-loaded-years", type=int, default=20)
    args = parser.parse_args()

    candidate_run_id = args.candidate_run_id or latest_run_id(
        args.psql, args.host, args.port, args.dbname, "noaa_station_candidates_%", args.user
    )
    station_ecwt_run_id = args.station_ecwt_run_id or latest_run_id(
        args.psql, args.host, args.port, args.dbname, "station_ecwt_loaded_%", args.user
    )
    coverage_run_id = args.coverage_run_id
    station_params: dict[str, object] = {}
    if not coverage_run_id:
        station_params = run_parameters(args.psql, args.host, args.port, args.dbname, station_ecwt_run_id, args.user)
        coverage_run_id = str(station_params.get("coverage_run_id") or "")
    if not coverage_run_id:
        raise RuntimeError(f"Station ECWT run has no coverage_run_id parameter: {station_ecwt_run_id}")
    preferred_coverage_table = str(station_params.get("coverage_table") or "") if station_params else None
    coverage_table = resolve_coverage_table(
        args.psql,
        args.host,
        args.port,
        args.dbname,
        coverage_run_id,
        args.coverage_source,
        preferred_coverage_table,
        args.user,
    )
    code_commit = git_commit_label(args.project_root)
    if args.selection_coverage_policy == "fixed-period":
        run_id = f"plant_ecwt_provisional_fixed_period_{utc_now().strftime('%Y%m%dT%H%M%SZ')}"
    else:
        run_id = f"plant_ecwt_provisional_{utc_now().strftime('%Y%m%dT%H%M%SZ')}"
    run(
        psql_cmd(args.psql, args.host, args.port, args.dbname, args.user),
        input_text=build_sql(
            run_id,
            candidate_run_id,
            station_ecwt_run_id,
            coverage_run_id,
            coverage_table,
            code_commit,
            args.selection_coverage_policy,
            args.fixed_min_year,
            args.fixed_max_year,
            args.fixed_min_coverage_ratio,
            args.fixed_min_loaded_years,
        ),
    )

    db_counts = report_counts(args.psql, args.host, args.port, args.dbname, run_id, args.user)
    sample_rows = psql_csv_query(
        args.psql,
        args.host,
        args.port,
        args.dbname,
        f"""
        select
            p.plant_name,
            p.state,
            seg.station_id,
            pe.valid_hour_count,
            round(pe.ecwt_f, 1) as ecwt_f,
            pe.result_status
        from calc.plant_ecwt pe
        join asset.plant p using (plant_id)
        left join link.station_selection_segment seg
          on seg.station_selection_id = pe.station_selection_id
        where pe.calculation_run_id = {sql_literal(run_id)}
          and pe.ecwt_f is not null
        order by pe.ecwt_f asc, p.plant_name
        limit 20
        """,
        args.user,
    )
    report_path = args.project_root / "docs" / f"{run_id}_report.md"
    render_report(
        report_path,
        run_id,
        candidate_run_id,
        station_ecwt_run_id,
        coverage_run_id,
        coverage_table,
        args.selection_coverage_policy,
        args.fixed_min_year,
        args.fixed_max_year,
        args.fixed_min_coverage_ratio,
        args.fixed_min_loaded_years,
        code_commit,
        db_counts,
        sample_rows,
        args.host,
        args.port,
        args.dbname,
    )
    print(json.dumps({"run_id": run_id, "report_path": str(report_path), "db_counts": db_counts}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
