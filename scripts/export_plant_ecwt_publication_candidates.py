#!/usr/bin/env python3
"""Export strict plant ECWT publication candidates as a reviewable CSV preview."""

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

METHODOLOGY_VERSION = "eop012-ecwt-method-v0.2.0"
FIRST_SCOPE_STATUSES = ("OP", "SB", "OA", "OS")


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def sql_literal(value: object) -> str:
    if value is None:
        return "null"
    return "'" + str(value).replace("'", "''") + "'"


def sql_list(values: Iterable[object]) -> str:
    return ", ".join(sql_literal(value) for value in values)


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


def psql_scalar(psql: Path, host: str, port: int, dbname: str, user: str | None, query: str) -> str:
    result = run(psql_cmd(psql, host, port, dbname, user) + ["-At", "-c", query])
    return result.stdout.strip()


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: pg_csv_value(row.get(field)) for field in fieldnames})


def git_commit_label(project_root: Path) -> str:
    try:
        return run(["git", "-C", str(project_root), "rev-parse", "HEAD"]).stdout.strip()
    except Exception:
        return "UNCOMMITTED_WORKTREE"


def latest_strict_readiness_run_id(psql: Path, host: str, port: int, dbname: str, user: str | None) -> str:
    run_id = psql_scalar(
        psql,
        host,
        port,
        dbname,
        user,
        """
        select r.calculation_run_id
        from calc.plant_ecwt_readiness r
        join audit.calculation_run cr
          on cr.calculation_run_id = r.calculation_run_id
        where cr.run_status = 'succeeded'
          and r.min_coverage_ratio_threshold = 0.95
        group by r.calculation_run_id, cr.run_started_at_utc
        order by cr.run_started_at_utc desc
        limit 1
        """,
    )
    if not run_id:
        raise RuntimeError("No strict plant_ecwt_readiness run found.")
    return run_id


def export_rows(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    readiness_run_id: str,
    release_id: str,
    plant_scope: str,
) -> list[dict[str, str]]:
    first_scope_statuses_sql = sql_list(FIRST_SCOPE_STATUSES)
    scope_filter = ""
    if plant_scope == "first-operable":
        scope_filter = "and pscope.in_first_scope"
    return psql_csv_query(
        psql,
        host,
        port,
        dbname,
        user,
        f"""
        with plant_generator_scope as (
            select
                p.plant_id,
                coalesce(string_agg(distinct g.status, ',' order by g.status), '') as generator_statuses,
                count(g.*)::text as total_generator_count,
                coalesce(round(sum(g.nameplate_capacity_mw), 3), 0)::text as total_nameplate_mw,
                count(g.*) filter (where g.status in ({first_scope_statuses_sql}))::text as first_scope_generator_count,
                coalesce(round(sum(g.nameplate_capacity_mw) filter (where g.status in ({first_scope_statuses_sql})), 3), 0)::text
                    as first_scope_nameplate_mw,
                coalesce(bool_or(g.status in ({first_scope_statuses_sql})), false) as in_first_scope
            from asset.plant p
            left join asset.generator g
              on g.eia_plant_code = p.eia_plant_code
            group by p.plant_id
        )
        select
            {sql_literal(release_id)} as release_id,
            {sql_literal(plant_scope)} as plant_scope,
            r.calculation_run_id as readiness_run_id,
            pe.calculation_run_id as plant_ecwt_run_id,
            pe.methodology_version,
            cr.code_commit,
            p.plant_id,
            p.eia_plant_code,
            p.plant_name,
            p.utility_id,
            p.utility_name,
            p.state as plant_state,
            p.county as plant_county,
            round(p.latitude, 6)::text as plant_latitude,
            round(p.longitude, 6)::text as plant_longitude,
            p.nerc_region,
            p.balancing_authority_code,
            p.balancing_authority_name,
            p.sector_name,
            pscope.generator_statuses,
            pscope.total_generator_count,
            pscope.total_nameplate_mw,
            pscope.first_scope_generator_count,
            pscope.first_scope_nameplate_mw,
            r.selected_station_id,
            st.station_name as selected_station_name,
            st.state as selected_station_state,
            st.country as selected_station_country,
            round(st.latitude, 6)::text as selected_station_latitude,
            round(st.longitude, 6)::text as selected_station_longitude,
            round(st.elevation_m, 3)::text as selected_station_elevation_m,
            st.first_observation_utc::text as selected_station_first_observation_utc,
            st.last_observation_utc::text as selected_station_last_observation_utc,
            round(r.selected_station_distance_km, 3)::text as selected_station_distance_km,
            round(r.selected_station_elevation_delta_m, 3)::text as selected_station_elevation_delta_m,
            round(pe.ecwt_f, 1)::text as ecwt_f,
            round(pe.ecwt_discrete_f, 1)::text as ecwt_discrete_f,
            round(pe.governing_ecwt_f, 1)::text as governing_ecwt_f,
            pe.valid_hour_count::text as valid_hour_count,
            pe.expected_hour_count::text as expected_hour_count,
            pe.missing_hour_count::text as missing_hour_count,
            pe.duplicate_hour_count::text as duplicate_hour_count,
            round(r.coverage_ratio, 6)::text as coverage_ratio,
            'fixed_period_station_local_djf_2000_to_calculation_cutoff'::text as coverage_basis,
            pe.percentile_target::text as percentile_target,
            pe.calculation_cutoff_utc::text as calculation_cutoff_utc,
            r.min_valid_hour_threshold::text as min_valid_hour_threshold,
            round(r.min_coverage_ratio_threshold, 6)::text as min_coverage_ratio_threshold,
            'rounded_to_0.1_f_due_to_noaa_tmp_tenths_c_source_resolution'::text as ecwt_precision_basis,
            'Analytical plant-level ECWT preview; not a Generator Owner EOP-012 compliance filing input without station representativeness review and source QA acceptance.'::text as publication_caveat,
            r.readiness_status,
            r.reason_code,
            pe.result_status,
            pe.created_at_utc::text as plant_ecwt_created_at_utc,
            r.created_at_utc::text as readiness_created_at_utc
        from calc.plant_ecwt_readiness r
        join calc.plant_ecwt pe
          on pe.plant_ecwt_id = r.plant_ecwt_id
        join audit.calculation_run cr
          on cr.calculation_run_id = r.calculation_run_id
        join asset.plant p
          on p.plant_id = r.plant_id
        join plant_generator_scope pscope
          on pscope.plant_id = r.plant_id
        left join weather.station st
          on st.station_id = r.selected_station_id
        where r.calculation_run_id = {sql_literal(readiness_run_id)}
          and r.readiness_status = 'publication_candidate'
          {scope_filter}
        order by p.state, p.eia_plant_code::integer nulls last, p.plant_name
        """,
    )


def readiness_summary(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    readiness_run_id: str,
) -> list[dict[str, str]]:
    return psql_csv_query(
        psql,
        host,
        port,
        dbname,
        user,
        f"""
        select readiness_status, reason_code, count(*)::text as rows
        from calc.plant_ecwt_readiness
        where calculation_run_id = {sql_literal(readiness_run_id)}
        group by readiness_status, reason_code
        order by readiness_status, reason_code
        """,
    )


def render_table(lines: list[str], headers: list[str], rows: list[dict[str, object]], fields: list[str]) -> None:
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join("---" for _ in headers) + " |")
    if not rows:
        lines.append("| " + " | ".join("" for _ in headers) + " |")
        return
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")) for field in fields) + " |")


def render_report(
    report_path: Path,
    run_id: str,
    release_id: str,
    code_commit: str,
    readiness_run_id: str,
    plant_scope: str,
    csv_path: Path,
    rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
) -> None:
    by_state = Counter(row["plant_state"] or "" for row in rows)
    state_rows = [{"state": state or "(blank)", "rows": count} for state, count in by_state.most_common()]
    coldest_rows = sorted(rows, key=lambda r: float(r["ecwt_f"]))[:20]
    warmest_rows = sorted(rows, key=lambda r: float(r["ecwt_f"]), reverse=True)[:20]
    lines = [
        "# Plant ECWT Strict Publication Candidate Export Report",
        "",
        f"Generated UTC: {utc_now().isoformat(timespec='seconds')}",
        "",
        "## Run",
        "",
        f"- Export run ID: `{run_id}`",
        f"- Release ID: `{release_id}`",
        f"- Code commit: `{code_commit}`",
        f"- Strict readiness run ID: `{readiness_run_id}`",
        f"- Plant scope: `{plant_scope}`",
        f"- CSV preview: `{csv_path.name}`",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| Exported strict publication candidates | {len(rows)} |",
        f"| Distinct plant states | {len(by_state)} |",
        f"| Distinct selected stations | {len(set(row['selected_station_id'] for row in rows))} |",
        "",
        "## Full Readiness Run Counts",
        "",
    ]
    render_table(lines, ["Readiness", "Reason", "Rows"], summary_rows, ["readiness_status", "reason_code", "rows"])
    lines.extend(["", "## Exported Candidates By State", ""])
    render_table(lines, ["State", "Rows"], state_rows, ["state", "rows"])
    lines.extend(["", "## Coldest Exported Plant ECWT Values", ""])
    render_table(
        lines,
        ["Plant", "State", "Station", "ECWT F", "Coverage"],
        coldest_rows,
        ["plant_name", "plant_state", "selected_station_id", "ecwt_f", "coverage_ratio"],
    )
    lines.extend(["", "## Warmest Exported Plant ECWT Values", ""])
    render_table(
        lines,
        ["Plant", "State", "Station", "ECWT F", "Coverage"],
        warmest_rows,
        ["plant_name", "plant_state", "selected_station_id", "ecwt_f", "coverage_ratio"],
    )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- This is a preview export of rows that passed the current strict publication gate, not a final compliance release.",
            "- The CSV intentionally excludes provisional low-coverage and blocked rows.",
            "- ECWT values are rounded to 0.1 F to avoid false precision relative to NOAA TMP tenths-C source resolution.",
            "- `coverage_basis` and `publication_caveat` are exported with each row so fixed-period denominator and review limits travel with the CSV.",
            "- `first-operable` scope means plants with at least one `OP`, `SB`, `OA`, or `OS` generator status.",
            "- Raw NOAA files and the Postgres database are not included in Git; source lineage and run IDs are retained for reproducibility.",
            "- Before a national release, QA must close out plausibility rejects, warm station ECWT outliers, and station-selection review.",
        ]
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--psql", type=Path, default=PSQL)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5436)
    parser.add_argument("--dbname", default="eop012")
    parser.add_argument("--user")
    parser.add_argument("--readiness-run-id")
    parser.add_argument("--release-id")
    parser.add_argument(
        "--plant-scope",
        choices=("all-plants", "first-operable"),
        default="all-plants",
        help="Filter publication candidates by plant/generator scope.",
    )
    args = parser.parse_args()

    readiness_run_id = args.readiness_run_id or latest_strict_readiness_run_id(
        args.psql, args.host, args.port, args.dbname, args.user
    )
    scope_slug = "" if args.plant_scope == "all-plants" else f"{args.plant_scope.replace('-', '_')}_"
    run_id = f"plant_ecwt_publication_candidates_{scope_slug}{utc_now().strftime('%Y%m%dT%H%M%SZ')}"
    release_id = args.release_id or f"preview-{run_id}"
    code_commit = git_commit_label(args.project_root)
    rows = export_rows(
        args.psql,
        args.host,
        args.port,
        args.dbname,
        args.user,
        readiness_run_id,
        release_id,
        args.plant_scope,
    )
    docs_dir = args.project_root / "docs"
    csv_path = docs_dir / f"{run_id}.csv"
    fieldnames = [
        "release_id",
        "plant_scope",
        "readiness_run_id",
        "plant_ecwt_run_id",
        "methodology_version",
        "code_commit",
        "plant_id",
        "eia_plant_code",
        "plant_name",
        "utility_id",
        "utility_name",
        "plant_state",
        "plant_county",
        "plant_latitude",
        "plant_longitude",
        "nerc_region",
        "balancing_authority_code",
        "balancing_authority_name",
        "sector_name",
        "generator_statuses",
        "total_generator_count",
        "total_nameplate_mw",
        "first_scope_generator_count",
        "first_scope_nameplate_mw",
        "selected_station_id",
        "selected_station_name",
        "selected_station_state",
        "selected_station_country",
        "selected_station_latitude",
        "selected_station_longitude",
        "selected_station_elevation_m",
        "selected_station_first_observation_utc",
        "selected_station_last_observation_utc",
        "selected_station_distance_km",
        "selected_station_elevation_delta_m",
        "ecwt_f",
        "ecwt_discrete_f",
        "governing_ecwt_f",
        "valid_hour_count",
        "expected_hour_count",
        "missing_hour_count",
        "duplicate_hour_count",
        "coverage_ratio",
        "coverage_basis",
        "percentile_target",
        "calculation_cutoff_utc",
        "min_valid_hour_threshold",
        "min_coverage_ratio_threshold",
        "ecwt_precision_basis",
        "publication_caveat",
        "readiness_status",
        "reason_code",
        "result_status",
        "plant_ecwt_created_at_utc",
        "readiness_created_at_utc",
    ]
    write_csv(csv_path, fieldnames, rows)
    summary = readiness_summary(args.psql, args.host, args.port, args.dbname, args.user, readiness_run_id)
    report_path = docs_dir / f"{run_id}_report.md"
    render_report(report_path, run_id, release_id, code_commit, readiness_run_id, args.plant_scope, csv_path, rows, summary)
    print(
        json.dumps(
            OrderedDict(
                [
                    ("run_id", run_id),
                    ("release_id", release_id),
                    ("readiness_run_id", readiness_run_id),
                    ("plant_scope", args.plant_scope),
                    ("rows_exported", len(rows)),
                    ("csv_path", str(csv_path)),
                    ("report_path", str(report_path)),
                ]
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
