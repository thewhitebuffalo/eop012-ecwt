#!/usr/bin/env python3
"""Export station-review release-ready plant ECWT rows as an auditable CSV preview."""

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

METHODOLOGY_VERSION = "eop012-ecwt-method-v0.1.0"


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


def psql_scalar(psql: Path, host: str, port: int, dbname: str, user: str | None, query: str) -> str:
    result = run(psql_cmd(psql, host, port, dbname, user) + ["-At", "-c", query])
    return result.stdout.strip()


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: pg_csv_value(row.get(field)) for field in fieldnames})


def git_commit_label(project_root: Path) -> str:
    try:
        return run(["git", "-C", str(project_root), "rev-parse", "HEAD"]).stdout.strip()
    except Exception:
        return "UNCOMMITTED_WORKTREE"


def latest_release_gate_run_id(psql: Path, host: str, port: int, dbname: str, user: str | None) -> str:
    run_id = psql_scalar(
        psql,
        host,
        port,
        dbname,
        user,
        """
        select rr.calculation_run_id
        from publish.plant_ecwt_release_readiness rr
        join audit.calculation_run cr
          on cr.calculation_run_id = rr.calculation_run_id
        where cr.run_status = 'succeeded'
        group by rr.calculation_run_id, cr.run_started_at_utc
        order by cr.run_started_at_utc desc
        limit 1
        """,
    )
    if not run_id:
        raise RuntimeError("No plant ECWT release-readiness run found.")
    return run_id


def release_counts(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    release_gate_run_id: str,
) -> list[dict[str, str]]:
    return psql_csv_query(
        psql,
        host,
        port,
        dbname,
        user,
        f"""
        select release_status, reason_code, count(*)::text as rows
        from publish.plant_ecwt_release_readiness
        where calculation_run_id = {sql_literal(release_gate_run_id)}
        group by release_status, reason_code
        order by release_status, reason_code
        """,
    )


def export_rows(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    release_gate_run_id: str,
    release_id: str,
) -> list[dict[str, str]]:
    return psql_csv_query(
        psql,
        host,
        port,
        dbname,
        user,
        f"""
        select
            {sql_literal(release_id)} as release_id,
            rr.calculation_run_id as release_gate_run_id,
            rr.readiness_run_id,
            pe.calculation_run_id as plant_ecwt_run_id,
            review.calculation_run_id as station_review_run_id,
            pe.methodology_version,
            rr_cr.code_commit as release_gate_code_commit,
            r_cr.code_commit as readiness_code_commit,
            pe_cr.code_commit as plant_ecwt_code_commit,
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
            r.selected_station_id,
            st.station_name as selected_station_name,
            st.state as selected_station_state,
            st.country as selected_station_country,
            round(st.latitude, 6)::text as selected_station_latitude,
            round(st.longitude, 6)::text as selected_station_longitude,
            round(st.elevation_m, 3)::text as selected_station_elevation_m,
            st.first_observation_utc::text as selected_station_first_observation_utc,
            st.last_observation_utc::text as selected_station_last_observation_utc,
            round(pe.ecwt_f, 3)::text as ecwt_f,
            round(pe.ecwt_discrete_f, 3)::text as ecwt_discrete_f,
            round(pe.governing_ecwt_f, 3)::text as governing_ecwt_f,
            pe.valid_hour_count::text as valid_hour_count,
            pe.expected_hour_count::text as expected_hour_count,
            pe.missing_hour_count::text as missing_hour_count,
            pe.duplicate_hour_count::text as duplicate_hour_count,
            round(r.coverage_ratio, 6)::text as coverage_ratio,
            pe.percentile_target::text as percentile_target,
            pe.calculation_cutoff_utc::text as calculation_cutoff_utc,
            r.min_valid_hour_threshold::text as min_valid_hour_threshold,
            round(r.min_coverage_ratio_threshold, 6)::text as min_coverage_ratio_threshold,
            r.readiness_status,
            r.reason_code as readiness_reason_code,
            rr.release_status,
            rr.reason_code as release_reason_code,
            rr.notes as release_notes,
            review.review_status as station_review_status,
            review.review_basis as station_review_basis,
            review.reviewer as station_reviewer,
            review.risk_flags as station_review_risk_flags,
            review.risk_flag_count::text as station_review_risk_flag_count,
            review.disposition_reason as station_review_disposition_reason,
            review.notes as station_review_notes,
            pe.result_status,
            pe.created_at_utc::text as plant_ecwt_created_at_utc,
            r.created_at_utc::text as readiness_created_at_utc,
            rr.created_at_utc::text as release_gate_created_at_utc
        from publish.plant_ecwt_release_readiness rr
        join calc.plant_ecwt_readiness r
          on r.plant_ecwt_readiness_id = rr.plant_ecwt_readiness_id
        join calc.plant_ecwt pe
          on pe.plant_ecwt_id = rr.plant_ecwt_id
        join audit.calculation_run rr_cr
          on rr_cr.calculation_run_id = rr.calculation_run_id
        join audit.calculation_run r_cr
          on r_cr.calculation_run_id = rr.readiness_run_id
        join audit.calculation_run pe_cr
          on pe_cr.calculation_run_id = pe.calculation_run_id
        join asset.plant p
          on p.plant_id = rr.plant_id
        left join weather.station st
          on st.station_id = r.selected_station_id
        left join link.station_selection_review review
          on review.station_selection_review_id = rr.station_selection_review_id
        where rr.calculation_run_id = {sql_literal(release_gate_run_id)}
          and rr.release_status = 'release_ready'
        order by p.state, p.eia_plant_code::integer nulls last, p.plant_name
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
    release_gate_run_id: str,
    csv_path: Path,
    rows: list[dict[str, str]],
    count_rows: list[dict[str, str]],
) -> None:
    by_state = Counter(row["plant_state"] or "" for row in rows)
    by_station_country = Counter(row["selected_station_country"] or "" for row in rows)
    by_review_basis = Counter(row["station_review_basis"] or "" for row in rows)
    state_rows = [{"state": state or "(blank)", "rows": count} for state, count in by_state.most_common()]
    country_rows = [
        {"country": country or "(blank)", "rows": count} for country, count in by_station_country.most_common()
    ]
    review_basis_rows = [
        {"review_basis": basis or "(blank)", "rows": count} for basis, count in by_review_basis.most_common()
    ]
    coldest_rows = sorted(rows, key=lambda row: float(row["governing_ecwt_f"]))[:20]
    warmest_rows = sorted(rows, key=lambda row: float(row["governing_ecwt_f"]), reverse=True)[:20]
    lines = [
        "# Plant ECWT Release-Ready Export Report",
        "",
        f"Generated UTC: {utc_now().isoformat(timespec='seconds')}",
        "",
        "## Run",
        "",
        f"- Export run ID: `{run_id}`",
        f"- Release ID: `{release_id}`",
        f"- Code commit: `{code_commit}`",
        f"- Release gate run ID: `{release_gate_run_id}`",
        f"- CSV preview: `{csv_path.name}`",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| Exported release-ready rows | {len(rows):,} |",
        f"| Distinct plant states | {len(by_state):,} |",
        f"| Distinct selected stations | {len(set(row['selected_station_id'] for row in rows)):,} |",
        "",
        "## Full Release Gate Counts",
        "",
    ]
    render_table(lines, ["Release Status", "Reason", "Rows"], count_rows, ["release_status", "reason_code", "rows"])
    lines.extend(["", "## Exported Rows By Plant State", ""])
    render_table(lines, ["State", "Rows"], state_rows, ["state", "rows"])
    lines.extend(["", "## Exported Rows By Station Country", ""])
    render_table(lines, ["Country", "Rows"], country_rows, ["country", "rows"])
    lines.extend(["", "## Exported Rows By Review Basis", ""])
    render_table(lines, ["Review Basis", "Rows"], review_basis_rows, ["review_basis", "rows"])
    lines.extend(["", "## Coldest Exported Plant ECWT Values", ""])
    render_table(
        lines,
        ["Plant", "State", "Station", "Governing ECWT F", "Coverage"],
        coldest_rows,
        ["plant_name", "plant_state", "selected_station_id", "governing_ecwt_f", "coverage_ratio"],
    )
    lines.extend(["", "## Warmest Exported Plant ECWT Values", ""])
    render_table(
        lines,
        ["Plant", "State", "Station", "Governing ECWT F", "Coverage"],
        warmest_rows,
        ["plant_name", "plant_state", "selected_station_id", "governing_ecwt_f", "coverage_ratio"],
    )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- This is a preview export of rows that passed fixed-period readiness and station-selection review.",
            "- It is narrower than the publication-candidate export because it uses `publish.plant_ecwt_release_readiness`.",
            "- The CSV intentionally excludes blocked readiness rows and station-review-blocked rows.",
            "- For a national release, remaining blocked rows require additional weather coverage or explicit station-selection policy decisions.",
            "",
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
    parser.add_argument("--release-gate-run-id")
    parser.add_argument("--release-id")
    args = parser.parse_args()

    release_gate_run_id = args.release_gate_run_id or latest_release_gate_run_id(
        args.psql, args.host, args.port, args.dbname, args.user
    )
    run_id = f"plant_ecwt_release_ready_{utc_now().strftime('%Y%m%dT%H%M%SZ')}"
    release_id = args.release_id or f"preview-{run_id}"
    code_commit = git_commit_label(args.project_root)
    rows = export_rows(args.psql, args.host, args.port, args.dbname, args.user, release_gate_run_id, release_id)
    docs_dir = args.project_root / "docs"
    csv_path = docs_dir / f"{run_id}.csv"
    fieldnames = [
        "release_id",
        "release_gate_run_id",
        "readiness_run_id",
        "plant_ecwt_run_id",
        "station_review_run_id",
        "methodology_version",
        "release_gate_code_commit",
        "readiness_code_commit",
        "plant_ecwt_code_commit",
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
        "selected_station_id",
        "selected_station_name",
        "selected_station_state",
        "selected_station_country",
        "selected_station_latitude",
        "selected_station_longitude",
        "selected_station_elevation_m",
        "selected_station_first_observation_utc",
        "selected_station_last_observation_utc",
        "ecwt_f",
        "ecwt_discrete_f",
        "governing_ecwt_f",
        "valid_hour_count",
        "expected_hour_count",
        "missing_hour_count",
        "duplicate_hour_count",
        "coverage_ratio",
        "percentile_target",
        "calculation_cutoff_utc",
        "min_valid_hour_threshold",
        "min_coverage_ratio_threshold",
        "readiness_status",
        "readiness_reason_code",
        "release_status",
        "release_reason_code",
        "release_notes",
        "station_review_status",
        "station_review_basis",
        "station_reviewer",
        "station_review_risk_flags",
        "station_review_risk_flag_count",
        "station_review_disposition_reason",
        "station_review_notes",
        "result_status",
        "plant_ecwt_created_at_utc",
        "readiness_created_at_utc",
        "release_gate_created_at_utc",
    ]
    write_csv(csv_path, fieldnames, rows)
    counts = release_counts(args.psql, args.host, args.port, args.dbname, args.user, release_gate_run_id)
    report_path = docs_dir / f"{run_id}_report.md"
    render_report(report_path, run_id, release_id, code_commit, release_gate_run_id, csv_path, rows, counts)
    print(
        json.dumps(
            OrderedDict(
                [
                    ("run_id", run_id),
                    ("release_id", release_id),
                    ("release_gate_run_id", release_gate_run_id),
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
