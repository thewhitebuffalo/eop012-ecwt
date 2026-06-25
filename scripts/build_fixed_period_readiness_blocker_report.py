#!/usr/bin/env python3
"""Diagnose fixed-period plant ECWT readiness blockers."""

from __future__ import annotations

import argparse
import csv
import io
import json
import subprocess
from collections import Counter, OrderedDict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from eop012_config import PROJECT_ROOT, PSQL


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def sql_literal(value: object) -> str:
    if value is None:
        return "null"
    return "'" + str(value).replace("'", "''") + "'"


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


def psql_scalar(psql: Path, host: str, port: int, dbname: str, user: str | None, query: str) -> str:
    result = run(psql_cmd(psql, host, port, dbname, user) + ["-At", "-c", query])
    return result.stdout.strip()


def relation_exists(psql: Path, host: str, port: int, dbname: str, user: str | None, relation_name: str) -> bool:
    exists = psql_scalar(
        psql,
        host,
        port,
        dbname,
        user,
        f"select to_regclass({sql_literal(relation_name)}) is not null;",
    )
    return exists.lower() == "t"


def coverage_row_count(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    coverage_run_id: str,
    coverage_table: str,
) -> int:
    return int(
        psql_scalar(
            psql,
            host,
            port,
            dbname,
            user,
            f"select count(*) from {coverage_table} where calculation_run_id = {sql_literal(coverage_run_id)};",
        )
        or "0"
    )


def resolve_coverage_table(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    coverage_run_id: str,
    coverage_source: str,
    preferred_table: str | None,
) -> str:
    valid_tables = {
        "weather.station_year_djf_coverage",
        "weather.station_year_djf_coverage_current",
    }
    if coverage_source == "history":
        return "weather.station_year_djf_coverage"
    if coverage_source == "current":
        return "weather.station_year_djf_coverage_current"
    if preferred_table in valid_tables and relation_exists(psql, host, port, dbname, user, preferred_table):
        if coverage_row_count(psql, host, port, dbname, user, coverage_run_id, preferred_table) > 0:
            return preferred_table
    current_table = "weather.station_year_djf_coverage_current"
    if relation_exists(psql, host, port, dbname, user, current_table) and coverage_row_count(
        psql, host, port, dbname, user, coverage_run_id, current_table
    ) > 0:
        return current_table
    return "weather.station_year_djf_coverage"


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def git_commit_label(project_root: Path) -> str:
    try:
        return run(["git", "-C", str(project_root), "rev-parse", "HEAD"]).stdout.strip()
    except Exception:
        return "UNCOMMITTED_WORKTREE"


def latest_fixed_plant_ecwt_run_id(psql: Path, host: str, port: int, dbname: str, user: str | None) -> str:
    return psql_scalar(
        psql,
        host,
        port,
        dbname,
        user,
        """
        select calculation_run_id
        from audit.calculation_run
        where calculation_run_id like 'plant_ecwt_provisional_fixed_period_%'
          and run_status = 'succeeded'
        order by run_started_at_utc desc
        limit 1
        """,
    )


def fetch_json_params(psql: Path, host: str, port: int, dbname: str, user: str | None, run_id: str) -> dict[str, object]:
    raw = psql_scalar(
        psql,
        host,
        port,
        dbname,
        user,
        f"""
        select parameters_json::text
        from audit.calculation_run
        where calculation_run_id = {sql_literal(run_id)}
        """,
    )
    if not raw:
        raise RuntimeError(f"No audit.calculation_run row found for {run_id}")
    return json.loads(raw)


def blocker_query(
    plant_ecwt_run_id: str,
    candidate_run_id: str,
    station_ecwt_run_id: str,
    coverage_run_id: str,
    coverage_table: str,
    fixed_min_year: int,
    fixed_max_year: int,
    fixed_min_coverage_ratio: float,
    fixed_min_loaded_years: int,
) -> str:
    if coverage_table not in {"weather.station_year_djf_coverage", "weather.station_year_djf_coverage_current"}:
        raise ValueError(f"Unexpected coverage table: {coverage_table}")
    return f"""
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
        make_timestamptz(y.source_year, 1, 1, 0, 0, 0, 'UTC'),
        make_timestamptz(y.source_year, 12, 31, 23, 0, 0, 'UTC'),
        interval '1 hour'
    ) as gs(hour_utc)
    group by y.source_year
),
station_fixed_coverage as (
    select
        se.station_id,
        sum(e.expected_djf_hours)::bigint as fixed_expected_djf_hours,
        coalesce(sum(c.valid_djf_hours), 0)::bigint as fixed_valid_djf_hours,
        greatest(sum(e.expected_djf_hours) - coalesce(sum(c.valid_djf_hours), 0), 0)::bigint
            as fixed_missing_djf_hours,
        coalesce(sum(c.duplicate_hour_count), 0)::bigint as fixed_duplicate_hour_count,
        count(c.*) filter (where c.loaded_file_count > 0)::integer as loaded_station_year_count,
        count(c.*) filter (where c.coverage_status = 'complete')::integer as complete_station_year_count,
        min(c.source_year) filter (where c.loaded_file_count > 0) as first_loaded_year,
        max(c.source_year) filter (where c.loaded_file_count > 0) as last_loaded_year,
        coalesce(sum(c.valid_djf_hours), 0)::numeric / nullif(sum(e.expected_djf_hours), 0)
            as fixed_coverage_ratio
    from calc.station_ecwt se
    cross join fixed_expected_by_year e
    left join {coverage_table} c
      on c.calculation_run_id = {sql_literal(coverage_run_id)}
     and c.station_id = se.station_id
     and c.source_year = e.source_year
    where se.calculation_run_id = {sql_literal(station_ecwt_run_id)}
      and se.result_status = 'provisional'
      and se.valid_hour_count > 0
    group by se.station_id
),
blocked_plants as (
    select
        pe.plant_ecwt_id,
        pe.plant_id,
        pe.result_status,
        p.eia_plant_code,
        p.plant_name,
        p.state as plant_state,
        p.county as plant_county,
        round(p.latitude, 6)::text as plant_latitude,
        round(p.longitude, 6)::text as plant_longitude,
        p.nerc_region,
        p.balancing_authority_code,
        p.sector_name
    from calc.plant_ecwt pe
    join asset.plant p using (plant_id)
    where pe.calculation_run_id = {sql_literal(plant_ecwt_run_id)}
      and pe.result_status = 'blocked'
),
candidate_eval as (
    select
        sc.plant_id,
        sc.station_id,
        st.station_name,
        st.state as station_state,
        st.country as station_country,
        round(sc.distance_km, 3)::text as distance_km,
        sc.distance_km as distance_km_num,
        sc.rank_order,
        se.station_ecwt_id is not null as has_station_ecwt_row,
        se.result_status as station_ecwt_status,
        se.valid_hour_count as station_ecwt_valid_hour_count,
        round(se.ecwt_f, 3)::text as station_ecwt_f,
        sf.fixed_expected_djf_hours,
        sf.fixed_valid_djf_hours,
        sf.fixed_missing_djf_hours,
        sf.fixed_duplicate_hour_count,
        sf.loaded_station_year_count,
        sf.complete_station_year_count,
        sf.first_loaded_year,
        sf.last_loaded_year,
        sf.fixed_coverage_ratio,
        (
            se.station_ecwt_id is not null
            and se.result_status = 'provisional'
            and se.valid_hour_count > 0
        ) as has_provisional_station_ecwt,
        (
            se.station_ecwt_id is not null
            and se.result_status = 'provisional'
            and se.valid_hour_count > 0
            and sf.fixed_coverage_ratio >= {fixed_min_coverage_ratio}
            and sf.loaded_station_year_count >= {fixed_min_loaded_years}
        ) as fixed_eligible
    from link.station_candidate sc
    join weather.station st using (station_id)
    left join calc.station_ecwt se
      on se.station_id = sc.station_id
     and se.calculation_run_id = {sql_literal(station_ecwt_run_id)}
    left join station_fixed_coverage sf
      on sf.station_id = sc.station_id
    where sc.calculation_run_id = {sql_literal(candidate_run_id)}
      and sc.candidate_status = 'candidate'
),
candidate_summary as (
    select
        plant_id,
        count(*)::integer as candidate_count,
        count(*) filter (where has_station_ecwt_row)::integer as candidate_with_station_ecwt_row_count,
        count(*) filter (where has_provisional_station_ecwt)::integer as candidate_with_provisional_station_ecwt_count,
        count(*) filter (where fixed_eligible)::integer as fixed_eligible_candidate_count,
        max(coalesce(fixed_coverage_ratio, 0)) as best_fixed_coverage_ratio,
        max(coalesce(loaded_station_year_count, 0)) as best_loaded_station_year_count,
        max(coalesce(fixed_valid_djf_hours, 0)) as best_fixed_valid_djf_hours
    from candidate_eval
    group by plant_id
),
nearest_candidate as (
    select *
    from (
        select
            ce.*,
            row_number() over (
                partition by ce.plant_id
                order by ce.rank_order asc nulls last, ce.distance_km_num asc nulls last, ce.station_id
            ) as rn
        from candidate_eval ce
    ) ranked
    where rn = 1
),
best_coverage_candidate as (
    select *
    from (
        select
            ce.*,
            row_number() over (
                partition by ce.plant_id
                order by
                    ce.fixed_eligible desc,
                    ce.fixed_coverage_ratio desc nulls last,
                    ce.loaded_station_year_count desc nulls last,
                    ce.rank_order asc nulls last,
                    ce.distance_km_num asc nulls last,
                    ce.station_id
            ) as rn
        from candidate_eval ce
        where ce.has_provisional_station_ecwt
    ) ranked
    where rn = 1
)
select
    bp.plant_id,
    bp.eia_plant_code,
    bp.plant_name,
    bp.plant_state,
    bp.plant_county,
    bp.plant_latitude,
    bp.plant_longitude,
    bp.nerc_region,
    bp.balancing_authority_code,
    bp.sector_name,
    case
        when coalesce(cs.fixed_eligible_candidate_count, 0) > 0 then 'unexpected_blocked_has_eligible_candidate'
        when coalesce(cs.candidate_count, 0) = 0 then 'no_station_candidates'
        when coalesce(cs.candidate_with_provisional_station_ecwt_count, 0) = 0
            then 'no_candidate_with_provisional_station_ecwt'
        when coalesce(cs.best_loaded_station_year_count, 0) < {fixed_min_loaded_years}
         and coalesce(cs.best_fixed_coverage_ratio, 0) < {fixed_min_coverage_ratio}
            then 'fixed_coverage_and_loaded_years_below_threshold'
        when coalesce(cs.best_loaded_station_year_count, 0) < {fixed_min_loaded_years}
            then 'fixed_loaded_years_below_threshold'
        when coalesce(cs.best_fixed_coverage_ratio, 0) < {fixed_min_coverage_ratio}
            then 'fixed_coverage_below_threshold'
        else 'other_no_eligible_candidate'
    end as blocker_class,
    coalesce(cs.candidate_count, 0)::text as candidate_count,
    coalesce(cs.candidate_with_station_ecwt_row_count, 0)::text as candidate_with_station_ecwt_row_count,
    coalesce(cs.candidate_with_provisional_station_ecwt_count, 0)::text
        as candidate_with_provisional_station_ecwt_count,
    coalesce(cs.fixed_eligible_candidate_count, 0)::text as fixed_eligible_candidate_count,
    round(coalesce(cs.best_fixed_coverage_ratio, 0), 6)::text as best_fixed_coverage_ratio,
    coalesce(cs.best_loaded_station_year_count, 0)::text as best_loaded_station_year_count,
    coalesce(cs.best_fixed_valid_djf_hours, 0)::text as best_fixed_valid_djf_hours,
    nc.station_id as nearest_station_id,
    nc.station_name as nearest_station_name,
    nc.station_state as nearest_station_state,
    nc.station_country as nearest_station_country,
    nc.distance_km as nearest_distance_km,
    nc.rank_order::text as nearest_rank_order,
    nc.station_ecwt_status as nearest_station_ecwt_status,
    nc.station_ecwt_valid_hour_count::text as nearest_station_ecwt_valid_hour_count,
    round(coalesce(nc.fixed_coverage_ratio, 0), 6)::text as nearest_fixed_coverage_ratio,
    coalesce(nc.loaded_station_year_count, 0)::text as nearest_loaded_station_year_count,
    bc.station_id as best_coverage_station_id,
    bc.station_name as best_coverage_station_name,
    bc.station_state as best_coverage_station_state,
    bc.station_country as best_coverage_station_country,
    bc.distance_km as best_coverage_distance_km,
    bc.rank_order::text as best_coverage_rank_order,
    bc.station_ecwt_status as best_coverage_station_ecwt_status,
    bc.station_ecwt_valid_hour_count::text as best_coverage_station_ecwt_valid_hour_count,
    bc.station_ecwt_f as best_coverage_station_ecwt_f,
    round(coalesce(bc.fixed_coverage_ratio, 0), 6)::text as best_coverage_ratio,
    coalesce(bc.loaded_station_year_count, 0)::text as best_coverage_loaded_station_year_count,
    coalesce(bc.fixed_valid_djf_hours, 0)::text as best_coverage_fixed_valid_djf_hours,
    coalesce(bc.fixed_expected_djf_hours, 0)::text as best_coverage_fixed_expected_djf_hours,
    coalesce(bc.first_loaded_year::text, '') as best_coverage_first_loaded_year,
    coalesce(bc.last_loaded_year::text, '') as best_coverage_last_loaded_year
from blocked_plants bp
left join candidate_summary cs using (plant_id)
left join nearest_candidate nc using (plant_id)
left join best_coverage_candidate bc using (plant_id)
order by blocker_class, bp.plant_state, bp.eia_plant_code::integer nulls last, bp.plant_name
"""


def render_table(lines: list[str], headers: list[str], rows: list[dict[str, object]], fields: list[str]) -> None:
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join("---" for _ in headers) + " |")
    if not rows:
        lines.append("| " + " | ".join("" for _ in headers) + " |")
        return
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")) for field in fields) + " |")


def render_report(
    path: Path,
    run_id: str,
    code_commit: str,
    plant_ecwt_run_id: str,
    candidate_run_id: str,
    station_ecwt_run_id: str,
    coverage_run_id: str,
    coverage_table: str,
    fixed_min_year: int,
    fixed_max_year: int,
    fixed_min_coverage_ratio: float,
    fixed_min_loaded_years: int,
    detail_csv: Path,
    rows: list[dict[str, str]],
) -> None:
    blocker_counts = Counter(row["blocker_class"] for row in rows)
    state_counts = Counter(row["plant_state"] or "(blank)" for row in rows)
    station_counts = Counter(
        f"{row['best_coverage_station_id']} {row['best_coverage_station_name']}".strip()
        for row in rows
        if row.get("best_coverage_station_id")
    )
    blocker_rows = [{"blocker_class": key, "rows": value} for key, value in blocker_counts.most_common()]
    state_rows = [{"plant_state": key, "rows": value} for key, value in state_counts.most_common(20)]
    station_rows = [{"station": key, "rows": value} for key, value in station_counts.most_common(20)]
    near_threshold_rows = sorted(
        (
            row
            for row in rows
            if row.get("best_coverage_ratio")
            and float(row["best_coverage_ratio"]) >= max(0.0, fixed_min_coverage_ratio - 0.05)
        ),
        key=lambda row: float(row["best_coverage_ratio"]),
        reverse=True,
    )[:25]
    no_ecwt_rows = [row for row in rows if row["blocker_class"] == "no_candidate_with_provisional_station_ecwt"][:25]
    no_candidate_rows = [row for row in rows if row["blocker_class"] == "no_station_candidates"][:25]

    lines = [
        "# Fixed-Period Readiness Blocker Report",
        "",
        f"Generated UTC: {utc_now().isoformat(timespec='seconds')}",
        "",
        "## Run",
        "",
        f"- Diagnostic run ID: `{run_id}`",
        f"- Code commit: `{code_commit}`",
        f"- Plant ECWT run ID: `{plant_ecwt_run_id}`",
        f"- Candidate run ID: `{candidate_run_id}`",
        f"- Station ECWT run ID: `{station_ecwt_run_id}`",
        f"- Station-year coverage run ID: `{coverage_run_id}`",
        f"- Station-year coverage table: `{coverage_table}`",
        f"- Fixed period: `{fixed_min_year}-{fixed_max_year}`",
        f"- Fixed minimum coverage ratio: `{fixed_min_coverage_ratio}`",
        f"- Fixed minimum loaded station-years: `{fixed_min_loaded_years}`",
        f"- Detail CSV: `{detail_csv.name}`",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| Blocked plant rows diagnosed | {len(rows):,} |",
        f"| Distinct plant states | {len(state_counts):,} |",
        "",
        "## Blocker Classes",
        "",
    ]
    render_table(lines, ["Blocker Class", "Rows"], blocker_rows, ["blocker_class", "rows"])
    lines.extend(["", "## Top Blocked Plant States", ""])
    render_table(lines, ["Plant State", "Rows"], state_rows, ["plant_state", "rows"])
    lines.extend(["", "## Top Best-Coverage Stations Among Blocked Plants", ""])
    render_table(lines, ["Station", "Rows"], station_rows, ["station", "rows"])
    lines.extend(["", "## Near-Threshold Blocked Examples", ""])
    render_table(
        lines,
        ["Plant", "State", "Best Station", "Coverage", "Loaded Years", "Distance km", "Rank"],
        near_threshold_rows,
        [
            "plant_name",
            "plant_state",
            "best_coverage_station_id",
            "best_coverage_ratio",
            "best_coverage_loaded_station_year_count",
            "best_coverage_distance_km",
            "best_coverage_rank_order",
        ],
    )
    lines.extend(["", "## No Provisional Station ECWT Examples", ""])
    render_table(
        lines,
        ["Plant", "State", "Nearest Station", "Nearest Status", "Distance km", "Rank"],
        no_ecwt_rows,
        [
            "plant_name",
            "plant_state",
            "nearest_station_id",
            "nearest_station_ecwt_status",
            "nearest_distance_km",
            "nearest_rank_order",
        ],
    )
    lines.extend(["", "## No Station Candidate Examples", ""])
    render_table(
        lines,
        ["Plant", "State", "County", "Latitude", "Longitude", "NERC Region", "BA"],
        no_candidate_rows,
        [
            "plant_name",
            "plant_state",
            "plant_county",
            "plant_latitude",
            "plant_longitude",
            "nerc_region",
            "balancing_authority_code",
        ],
    )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `no_candidate_with_provisional_station_ecwt` means none of the plant's candidate stations has a provisional station ECWT in the selected station ECWT run.",
            "- `fixed_coverage_below_threshold` means at least one candidate has provisional station ECWT, but no candidate reaches the fixed-period coverage threshold.",
            "- `fixed_loaded_years_below_threshold` means the candidate coverage ratio can be high but the station does not satisfy the loaded-year span rule.",
            "- When the expanded NOAA AWS manifest is exhausted, do not treat all blockers as ordinary retry work; separate terminal 404 gaps, station-candidate expansion, plant geocoding gaps, and denominator-policy review.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--psql", type=Path, default=PSQL)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5436)
    parser.add_argument("--dbname", default="eop012")
    parser.add_argument("--user")
    parser.add_argument("--plant-ecwt-run-id")
    parser.add_argument("--coverage-source", choices=["auto", "current", "history"], default="auto")
    args = parser.parse_args()

    plant_ecwt_run_id = args.plant_ecwt_run_id or latest_fixed_plant_ecwt_run_id(
        args.psql, args.host, args.port, args.dbname, args.user
    )
    if not plant_ecwt_run_id:
        raise RuntimeError("No fixed-period plant ECWT run found.")
    params = fetch_json_params(args.psql, args.host, args.port, args.dbname, args.user, plant_ecwt_run_id)
    candidate_run_id = str(params["candidate_run_id"])
    station_ecwt_run_id = str(params["station_ecwt_run_id"])
    coverage_run_id = str(params["coverage_run_id"])
    preferred_coverage_table = str(params.get("coverage_table") or "") if params else None
    coverage_table = resolve_coverage_table(
        args.psql,
        args.host,
        args.port,
        args.dbname,
        args.user,
        coverage_run_id,
        args.coverage_source,
        preferred_coverage_table,
    )
    fixed_min_year = int(params["fixed_min_year"])
    fixed_max_year = int(params["fixed_max_year"])
    fixed_min_coverage_ratio = float(params["fixed_min_coverage_ratio"])
    fixed_min_loaded_years = int(params["fixed_min_loaded_years"])

    run_id = f"fixed_period_readiness_blockers_{utc_now().strftime('%Y%m%dT%H%M%SZ')}"
    code_commit = git_commit_label(args.project_root)
    rows = psql_csv_query(
        args.psql,
        args.host,
        args.port,
        args.dbname,
        args.user,
        blocker_query(
            plant_ecwt_run_id,
            candidate_run_id,
            station_ecwt_run_id,
            coverage_run_id,
            coverage_table,
            fixed_min_year,
            fixed_max_year,
            fixed_min_coverage_ratio,
            fixed_min_loaded_years,
        ),
    )
    docs_dir = args.project_root / "docs"
    detail_csv = docs_dir / f"{run_id}.csv"
    report_path = docs_dir / f"{run_id}_report.md"
    fieldnames = list(rows[0].keys()) if rows else []
    write_csv(detail_csv, fieldnames, rows)
    render_report(
        report_path,
        run_id,
        code_commit,
        plant_ecwt_run_id,
        candidate_run_id,
        station_ecwt_run_id,
        coverage_run_id,
        coverage_table,
        fixed_min_year,
        fixed_max_year,
        fixed_min_coverage_ratio,
        fixed_min_loaded_years,
        detail_csv,
        rows,
    )
    print(
        json.dumps(
            OrderedDict(
                [
                    ("run_id", run_id),
                    ("plant_ecwt_run_id", plant_ecwt_run_id),
                    ("blocked_rows", len(rows)),
                    ("detail_csv", str(detail_csv)),
                    ("report_path", str(report_path)),
                ]
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
