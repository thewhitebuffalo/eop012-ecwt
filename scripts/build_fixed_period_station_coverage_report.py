#!/usr/bin/env python3
"""Compare strict plant ECWT candidates against a fixed-period station coverage gate."""

from __future__ import annotations

import argparse
import csv
import io
import json
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from eop012_config import PROJECT_ROOT, PSQL


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def sql_literal(value: object) -> str:
    if value is None:
        return "null"
    text = str(value)
    return "'" + text.replace("'", "''") + "'"


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        cmd,
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


def latest_strict_readiness_run_id(psql: Path, host: str, port: int, dbname: str, user: str | None) -> str:
    run_id = psql_scalar(
        psql,
        host,
        port,
        dbname,
        """
        select calculation_run_id
        from audit.calculation_run
        where calculation_run_id like 'plant_ecwt_readiness_%'
          and run_status = 'succeeded'
          and coalesce((parameters_json->>'min_coverage_ratio')::numeric, 0) >= 0.95
        order by run_started_at_utc desc
        limit 1
        """,
        user,
    )
    if not run_id:
        raise RuntimeError("No succeeded strict plant_ecwt_readiness run found.")
    return run_id


def fetch_run_params(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    run_id: str,
    user: str | None,
) -> dict[str, object]:
    params_text = psql_scalar(
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
    if not params_text:
        raise RuntimeError(f"Calculation run not found: {run_id}")
    return json.loads(params_text)


def build_sql(readiness_run_id: str, min_year: int, max_year: int) -> str:
    return f"""
with readiness_run as (
    select
        calculation_run_id as readiness_run_id,
        parameters_json->>'plant_ecwt_run_id' as plant_ecwt_run_id,
        parameters_json->>'min_valid_hours' as active_min_valid_hours,
        parameters_json->>'min_coverage_ratio' as active_min_coverage_ratio,
        parameters_json->>'coverage_denominator' as active_coverage_denominator
    from audit.calculation_run
    where calculation_run_id = {sql_literal(readiness_run_id)}
),
plant_run as (
    select
        cr.calculation_run_id as plant_ecwt_run_id,
        cr.parameters_json->>'candidate_run_id' as candidate_run_id,
        cr.parameters_json->>'station_ecwt_run_id' as station_ecwt_run_id
    from audit.calculation_run cr
    join readiness_run rr on rr.plant_ecwt_run_id = cr.calculation_run_id
),
station_ecwt_run as (
    select
        cr.calculation_run_id as station_ecwt_run_id,
        cr.parameters_json->>'coverage_run_id' as coverage_run_id
    from audit.calculation_run cr
    join plant_run pr on pr.station_ecwt_run_id = cr.calculation_run_id
),
years as (
    select generate_series({min_year}, {max_year})::integer as source_year
),
expected_by_year as (
    select
        y.source_year,
        count(*) filter (
            where extract(month from gs.hour_utc at time zone 'UTC') in (12, 1, 2)
        )::bigint as expected_djf_hours
    from years y
    cross join lateral generate_series(
        make_timestamptz(y.source_year, 1, 1, 0, 0, 0, 'UTC'),
        make_timestamptz(y.source_year, 12, 31, 23, 0, 0, 'UTC'),
        interval '1 hour'
    ) as gs(hour_utc)
    group by y.source_year
),
strict_candidates as (
    select
        rr.readiness_run_id,
        rr.plant_ecwt_run_id,
        pr.candidate_run_id,
        pr.station_ecwt_run_id,
        ser.coverage_run_id,
        rr.active_min_valid_hours,
        rr.active_min_coverage_ratio,
        rr.active_coverage_denominator,
        r.plant_ecwt_readiness_id,
        r.plant_ecwt_id,
        r.plant_id,
        r.selected_station_id,
        r.valid_hour_count as active_valid_hour_count,
        r.expected_hour_count as active_expected_hour_count,
        r.coverage_ratio as active_coverage_ratio,
        pe.governing_ecwt_f,
        pe.station_selection_id,
        p.eia_plant_code,
        p.plant_name,
        p.utility_name,
        p.city as plant_city,
        p.state as plant_state,
        p.county as plant_county,
        p.latitude as plant_latitude,
        p.longitude as plant_longitude,
        p.nerc_region,
        p.balancing_authority_code,
        p.sector_name,
        st.station_name as selected_station_name,
        st.state as selected_station_state,
        st.country as selected_station_country,
        st.latitude as selected_station_latitude,
        st.longitude as selected_station_longitude,
        st.elevation_m as selected_station_elevation_m,
        st.first_observation_utc as selected_station_first_observation_utc,
        st.last_observation_utc as selected_station_last_observation_utc,
        sc.distance_km as selected_distance_km,
        sc.rank_order as selected_rank_order
    from readiness_run rr
    join plant_run pr on true
    join station_ecwt_run ser on true
    join calc.plant_ecwt_readiness r
      on r.calculation_run_id = rr.readiness_run_id
     and r.readiness_status = 'publication_candidate'
    join calc.plant_ecwt pe
      on pe.plant_ecwt_id = r.plant_ecwt_id
    join asset.plant p
      on p.plant_id = r.plant_id
    left join weather.station st
      on st.station_id = r.selected_station_id
    left join link.station_candidate sc
      on sc.calculation_run_id = pr.candidate_run_id
     and sc.plant_id = r.plant_id
     and sc.station_id = r.selected_station_id
),
fixed_coverage as (
    select
        s.plant_id,
        s.selected_station_id,
        sum(e.expected_djf_hours)::bigint as fixed_expected_djf_hours,
        coalesce(sum(c.valid_djf_hours), 0)::bigint as fixed_valid_djf_hours,
        greatest(sum(e.expected_djf_hours) - coalesce(sum(c.valid_djf_hours), 0), 0)::bigint as fixed_missing_djf_hours,
        count(*)::integer as fixed_period_years,
        count(c.*) filter (where c.loaded_file_count > 0)::integer as loaded_station_year_count,
        count(c.*) filter (where c.valid_djf_hours > 0)::integer as nonzero_station_year_count,
        count(c.*) filter (where c.coverage_status = 'complete')::integer as complete_station_year_count,
        min(c.source_year) filter (where c.loaded_file_count > 0) as first_loaded_year,
        max(c.source_year) filter (where c.loaded_file_count > 0) as last_loaded_year,
        coalesce(sum(c.duplicate_hour_count), 0)::bigint as fixed_duplicate_hour_count,
        coalesce(sum(c.rejected_source_row_count), 0)::bigint as fixed_rejected_source_row_count,
        coalesce(sum(c.rejected_plausibility_row_count), 0)::bigint as fixed_rejected_plausibility_row_count
    from strict_candidates s
    cross join expected_by_year e
    left join weather.station_year_djf_coverage c
      on c.calculation_run_id = s.coverage_run_id
     and c.station_id = s.selected_station_id
     and c.source_year = e.source_year
    group by s.plant_id, s.selected_station_id
)
select
    s.*,
    {min_year}::integer as fixed_min_year,
    {max_year}::integer as fixed_max_year,
    f.fixed_period_years,
    f.fixed_expected_djf_hours,
    f.fixed_valid_djf_hours,
    f.fixed_missing_djf_hours,
    f.fixed_valid_djf_hours::numeric / nullif(f.fixed_expected_djf_hours, 0) as fixed_coverage_ratio,
    f.loaded_station_year_count,
    f.nonzero_station_year_count,
    f.complete_station_year_count,
    f.first_loaded_year,
    f.last_loaded_year,
    f.fixed_duplicate_hour_count,
    f.fixed_rejected_source_row_count,
    f.fixed_rejected_plausibility_row_count,
    (s.active_coverage_ratio - (f.fixed_valid_djf_hours::numeric / nullif(f.fixed_expected_djf_hours, 0))) as active_minus_fixed_coverage_ratio
from strict_candidates s
join fixed_coverage f
  on f.plant_id = s.plant_id
 and f.selected_station_id = s.selected_station_id
order by fixed_coverage_ratio desc nulls last, plant_state nulls last, eia_plant_code, plant_name
"""


def to_float(value: str | None) -> float | None:
    if value is None or value == "":
        return None
    return float(value)


def to_int(value: str | None) -> int | None:
    if value is None or value == "":
        return None
    return int(float(value))


def timestamp_year(value: str | None) -> int | None:
    if value is None or len(value) < 4:
        return None
    try:
        return int(value[:4])
    except ValueError:
        return None


def fmt_num(value: str | int | float | None, digits: int = 3) -> str:
    if value is None or value == "":
        return ""
    number = float(value)
    if number.is_integer():
        return f"{int(number):,}"
    return f"{number:,.{digits}f}"


def fmt_ratio(value: str | int | float | None) -> str:
    if value is None or value == "":
        return ""
    return f"{float(value):.4f}"


def fmt_temp(value: str | int | float | None) -> str:
    if value is None or value == "":
        return ""
    return f"{float(value):.1f}"


def add_status(rows: list[dict[str, str]], min_coverage_ratio: float, min_loaded_years: int) -> None:
    for row in rows:
        fixed_ratio = to_float(row.get("fixed_coverage_ratio")) or 0.0
        loaded_years = to_int(row.get("loaded_station_year_count")) or 0
        flags = []
        if fixed_ratio >= min_coverage_ratio and loaded_years >= min_loaded_years:
            status = "fixed_period_pass"
        elif fixed_ratio >= min_coverage_ratio:
            status = "fixed_period_coverage_pass_insufficient_years"
            flags.append(f"loaded_years_lt_{min_loaded_years}")
        elif fixed_ratio >= 0.90:
            status = "fixed_period_near_pass"
            flags.append(f"fixed_coverage_below_{str(min_coverage_ratio).replace('.', '_')}")
        else:
            status = "fixed_period_low_coverage"
            flags.append("fixed_coverage_below_0_90")
        if loaded_years < min_loaded_years and f"loaded_years_lt_{min_loaded_years}" not in flags:
            flags.append(f"loaded_years_lt_{min_loaded_years}")
        if (to_int(row.get("last_loaded_year")) or 0) < int(row.get("fixed_max_year") or 0):
            flags.append("no_loaded_file_in_final_fixed_year")
        last_obs_year = timestamp_year(row.get("selected_station_last_observation_utc"))
        if last_obs_year is not None and last_obs_year < 2010:
            flags.append("station_last_observation_before_2010")
        row["fixed_period_status"] = status
        row["fixed_period_flags"] = ";".join(flags)
        row["fixed_period_flag_count"] = str(len(flags))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise RuntimeError("No rows to write.")
    fieldnames = [
        "diagnostic_run_id",
        "readiness_run_id",
        "plant_ecwt_run_id",
        "candidate_run_id",
        "station_ecwt_run_id",
        "coverage_run_id",
        "plant_id",
        "eia_plant_code",
        "plant_name",
        "utility_name",
        "plant_city",
        "plant_state",
        "plant_county",
        "plant_latitude",
        "plant_longitude",
        "nerc_region",
        "balancing_authority_code",
        "sector_name",
        "plant_ecwt_readiness_id",
        "plant_ecwt_id",
        "station_selection_id",
        "selected_station_id",
        "selected_station_name",
        "selected_station_state",
        "selected_station_country",
        "selected_station_latitude",
        "selected_station_longitude",
        "selected_station_elevation_m",
        "selected_station_first_observation_utc",
        "selected_station_last_observation_utc",
        "selected_distance_km",
        "selected_rank_order",
        "governing_ecwt_f",
        "active_coverage_denominator",
        "active_min_valid_hours",
        "active_min_coverage_ratio",
        "active_valid_hour_count",
        "active_expected_hour_count",
        "active_coverage_ratio",
        "fixed_min_year",
        "fixed_max_year",
        "fixed_period_years",
        "fixed_expected_djf_hours",
        "fixed_valid_djf_hours",
        "fixed_missing_djf_hours",
        "fixed_coverage_ratio",
        "active_minus_fixed_coverage_ratio",
        "loaded_station_year_count",
        "nonzero_station_year_count",
        "complete_station_year_count",
        "first_loaded_year",
        "last_loaded_year",
        "fixed_duplicate_hour_count",
        "fixed_rejected_source_row_count",
        "fixed_rejected_plausibility_row_count",
        "fixed_period_status",
        "fixed_period_flags",
        "fixed_period_flag_count",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def compact_row(row: dict[str, str]) -> dict[str, str]:
    return {
        "Plant": f"{row.get('eia_plant_code', '')} {row.get('plant_name', '')}".strip(),
        "State": row.get("plant_state", ""),
        "Station": f"{row.get('selected_station_id', '')} {row.get('selected_station_name', '')}".strip(),
        "Active Coverage": fmt_ratio(row.get("active_coverage_ratio")),
        "Fixed Coverage": fmt_ratio(row.get("fixed_coverage_ratio")),
        "Loaded Years": row.get("loaded_station_year_count", ""),
        "Years": f"{row.get('first_loaded_year', '')}-{row.get('last_loaded_year', '')}",
        "Distance km": fmt_num(row.get("selected_distance_km"), 1),
        "ECWT F": fmt_temp(row.get("governing_ecwt_f")),
        "Status": row.get("fixed_period_status", ""),
    }


def md_table(rows: list[dict[str, str]], columns: list[tuple[str, str]], limit: int = 20) -> list[str]:
    if not rows:
        return ["_None._"]
    lines = [
        "| " + " | ".join(header for header, _ in columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows[:limit]:
        cells = [str(row.get(key, "")).replace("\n", " ").replace("|", "\\|") for _, key in columns]
        lines.append("| " + " | ".join(cells) + " |")
    if len(rows) > limit:
        omitted_cells = ["..."] + [f"{len(rows) - limit} more rows omitted"] + [""] * max(0, len(columns) - 2)
        lines.append("| " + " | ".join(omitted_cells) + " |")
    return lines


def render_report(
    path: Path,
    csv_path: Path,
    diagnostic_run_id: str,
    generated_at: str,
    code_commit: str,
    readiness_run_id: str,
    readiness_params: dict[str, object],
    rows: list[dict[str, str]],
    fixed_min_year: int,
    fixed_max_year: int,
    min_coverage_ratio: float,
    min_loaded_years: int,
) -> None:
    total = len(rows)
    status_counts = Counter(row["fixed_period_status"] for row in rows)
    median_ratio = sorted(to_float(row["fixed_coverage_ratio"]) or 0.0 for row in rows)[total // 2]
    median_loaded_years = sorted(to_int(row["loaded_station_year_count"]) or 0 for row in rows)[total // 2]
    max_ratio = max(to_float(row["fixed_coverage_ratio"]) or 0.0 for row in rows)
    min_ratio = min(to_float(row["fixed_coverage_ratio"]) or 0.0 for row in rows)
    expected_hours = rows[0].get("fixed_expected_djf_hours", "") if rows else ""
    coverage_run_id = rows[0].get("coverage_run_id", "") if rows else ""

    status_rows = [
        {
            "Status": status,
            "Rows": f"{count:,}",
            "Share": f"{(count / total * 100):.1f}%",
        }
        for status, count in status_counts.most_common()
    ]
    pass_rows = [row for row in rows if row["fixed_period_status"] == "fixed_period_pass"]
    near_rows = [row for row in rows if row["fixed_period_status"] == "fixed_period_near_pass"]
    worst_rows = sorted(rows, key=lambda row: to_float(row["fixed_coverage_ratio"]) or 0.0)
    biggest_drop_rows = sorted(rows, key=lambda row: to_float(row["active_minus_fixed_coverage_ratio"]) or 0.0, reverse=True)
    old_station_rows = [
        row
        for row in rows
        if (timestamp_year(row.get("selected_station_last_observation_utc")) or 9999) < 2010
    ]

    cols = [
        ("Plant", "Plant"),
        ("State", "State"),
        ("Station", "Station"),
        ("Active Coverage", "Active Coverage"),
        ("Fixed Coverage", "Fixed Coverage"),
        ("Loaded Years", "Loaded Years"),
        ("Years", "Years"),
        ("Distance km", "Distance km"),
        ("ECWT F", "ECWT F"),
        ("Status", "Status"),
    ]

    lines = [
        "# Fixed-Period Coverage Diagnostic for Strict Plant ECWT Candidates",
        "",
        "## Technical Summary",
        "",
        (
            f"The current strict readiness run has `{total:,}` publication candidates under the active-window denominator. "
            f"When the same selected stations are tested against a fixed `{fixed_min_year}-{fixed_max_year}` DJF denominator, "
            f"only `{status_counts.get('fixed_period_pass', 0):,}` rows pass coverage >= `{min_coverage_ratio:g}`. "
            f"`{status_counts.get('fixed_period_near_pass', 0):,}` more rows are between `0.90` and `{min_coverage_ratio:g}`."
        ),
        "",
        (
            f"The median fixed-period coverage ratio is `{median_ratio:.4f}` with a median of `{median_loaded_years}` "
            f"loaded station-years out of `{fixed_max_year - fixed_min_year + 1}`. This means the current strict "
            "publication-candidate label should remain provisional until the readiness denominator policy is corrected."
        ),
        "",
        "## Scope and Source Runs",
        "",
        f"- Diagnostic run: `{diagnostic_run_id}`",
        f"- Generated at UTC: `{generated_at}`",
        f"- Code commit: `{code_commit}`",
        f"- Readiness run: `{readiness_run_id}`",
        f"- Plant ECWT run: `{readiness_params.get('plant_ecwt_run_id', '')}`",
        f"- Station-year coverage run: `{coverage_run_id}`",
        f"- Active-window denominator from readiness run: `{readiness_params.get('coverage_denominator', '')}`",
        f"- Fixed denominator: `{fixed_min_year}-{fixed_max_year}` DJF hours, `{expected_hours}` hours per selected station.",
        f"- Fixed pass gate used in this diagnostic: coverage ratio >= `{min_coverage_ratio:g}` and at least `{min_loaded_years}` loaded station-years.",
        f"- Detailed CSV: `{csv_path.name}`",
        "",
        "## Fixed-Period Status Counts",
        "",
    ]
    lines.extend(md_table(status_rows, [("Status", "Status"), ("Rows", "Rows"), ("Share", "Share")], limit=10))

    lines.extend(
        [
            "",
            "## Coverage Distribution",
            "",
            "| Metric | Value |",
            "| --- | ---: |",
            f"| Minimum fixed-period coverage | {min_ratio:.4f} |",
            f"| Median fixed-period coverage | {median_ratio:.4f} |",
            f"| Maximum fixed-period coverage | {max_ratio:.4f} |",
            f"| Median loaded station-years | {median_loaded_years} |",
            f"| Rows with selected station metadata ending before 2010 | {len(old_station_rows):,} |",
            "",
            "## Rows Passing Fixed-Period Gate",
            "",
        ]
    )
    lines.extend(md_table([compact_row(row) for row in pass_rows], cols, limit=20))

    lines.extend(["", "## Rows Near Fixed-Period Gate", ""])
    lines.extend(md_table([compact_row(row) for row in near_rows], cols, limit=20))

    lines.extend(["", "## Lowest Fixed-Period Coverage Rows", ""])
    lines.extend(md_table([compact_row(row) for row in worst_rows], cols, limit=20))

    lines.extend(["", "## Largest Active-to-Fixed Coverage Drops", ""])
    lines.extend(md_table([compact_row(row) for row in biggest_drop_rows], cols, limit=20))

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "The active-window denominator answers a narrow parser question: how complete are the loaded rows during the station's represented active period. It does not answer whether the selected station has adequate coverage across the intended ECWT analysis period.",
            "",
            "For a compliance-facing national plant ECWT release, the fixed-period diagnostic is the more conservative publication-control view. The current `publication_candidate` cohort is therefore best treated as a provisional math output, not a release-ready compliance dataset.",
            "",
            "## Recommended Next Steps",
            "",
            "1. Replace or supplement the current readiness gate with a fixed-period coverage gate before release-candidate export.",
            "2. Decide the required fixed analysis period and minimum loaded-year rule from the EOP-012/EPRI method notes, then encode it in `calc.plant_ecwt_readiness` or a successor release-readiness table.",
            "3. Re-run station selection after applying the fixed-period rule, because many plants may need a different station than the current active-window winner.",
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
    parser.add_argument("--readiness-run-id")
    parser.add_argument("--fixed-min-year", type=int, default=2000)
    parser.add_argument("--fixed-max-year", type=int, default=2025)
    parser.add_argument("--min-coverage-ratio", type=float, default=0.95)
    parser.add_argument("--min-loaded-years", type=int, default=20)
    args = parser.parse_args()

    timestamp = utc_now().strftime("%Y%m%dT%H%M%SZ")
    diagnostic_run_id = f"fixed_period_station_coverage_{timestamp}"
    readiness_run_id = args.readiness_run_id or latest_strict_readiness_run_id(
        args.psql, args.host, args.port, args.dbname, args.user
    )
    readiness_params = fetch_run_params(args.psql, args.host, args.port, args.dbname, readiness_run_id, args.user)
    code_commit = git_commit_label(args.project_root)
    rows = psql_csv_query(
        args.psql,
        args.host,
        args.port,
        args.dbname,
        build_sql(readiness_run_id, args.fixed_min_year, args.fixed_max_year),
        args.user,
    )
    for row in rows:
        row["diagnostic_run_id"] = diagnostic_run_id
    add_status(rows, args.min_coverage_ratio, args.min_loaded_years)

    docs_dir = args.project_root / "docs"
    csv_path = docs_dir / f"{diagnostic_run_id}.csv"
    report_path = docs_dir / f"{diagnostic_run_id}_report.md"
    write_csv(csv_path, rows)
    render_report(
        report_path,
        csv_path,
        diagnostic_run_id,
        utc_now().isoformat(timespec="seconds"),
        code_commit,
        readiness_run_id,
        readiness_params,
        rows,
        args.fixed_min_year,
        args.fixed_max_year,
        args.min_coverage_ratio,
        args.min_loaded_years,
    )

    status_counts = Counter(row["fixed_period_status"] for row in rows)
    print(f"diagnostic_run_id={diagnostic_run_id}")
    print(f"readiness_run_id={readiness_run_id}")
    print(f"strict_candidate_rows={len(rows)}")
    for status, count in status_counts.most_common():
        print(f"{status}={count}")
    print(f"csv_path={csv_path}")
    print(f"report_path={report_path}")


if __name__ == "__main__":
    main()
