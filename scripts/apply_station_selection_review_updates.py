#!/usr/bin/env python3
"""Generate and apply station-selection review update worksheets."""

from __future__ import annotations

import argparse
import csv
import io
import json
import subprocess
from collections import Counter, OrderedDict
from datetime import datetime, timezone
from pathlib import Path

from build_station_selection_review import build_sql as build_review_gate_sql
from build_station_selection_review import count_query
from eop012_config import PROJECT_ROOT, PSQL, STAGING_ROOT

METHODOLOGY_VERSION = "eop012-ecwt-method-v0.1.0"
VALID_REVIEW_STATUSES = {"accepted", "needs_review", "rejected"}
VALID_REVIEW_BASES = {"manual_review", "policy_override"}

TEMPLATE_FIELDS = [
    "source_station_selection_review_id",
    "source_review_run_id",
    "readiness_run_id",
    "plant_ecwt_readiness_id",
    "plant_ecwt_id",
    "station_selection_id",
    "plant_id",
    "eia_plant_code",
    "plant_name",
    "plant_state",
    "plant_county",
    "station_id",
    "station_name",
    "station_state",
    "station_country",
    "selected_distance_km",
    "selected_rank_order",
    "coverage_ratio",
    "governing_ecwt_f",
    "current_review_status",
    "current_review_basis",
    "current_reviewer",
    "risk_flags",
    "risk_flag_count",
    "current_disposition_reason",
    "current_notes",
    "proposed_review_status",
    "proposed_review_basis",
    "proposed_disposition_reason",
    "reviewer",
    "review_notes",
]

REVIEW_FIELDS = [
    "station_selection_review_id",
    "calculation_run_id",
    "readiness_run_id",
    "plant_ecwt_readiness_id",
    "plant_ecwt_id",
    "station_selection_id",
    "plant_id",
    "station_id",
    "review_status",
    "review_basis",
    "reviewer",
    "risk_flags",
    "risk_flag_count",
    "disposition_reason",
    "notes",
]


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


def pg_csv_value(value: object) -> object:
    if value is None:
        return r"\N"
    text = str(value)
    return r"\N" if text == "" else text


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: "" if row.get(field) is None else row.get(field, "") for field in fieldnames})


def git_commit_label(project_root: Path) -> str:
    try:
        return run(["git", "-C", str(project_root), "rev-parse", "HEAD"]).stdout.strip()
    except Exception:
        return "UNCOMMITTED_WORKTREE"


def latest_review_run_id(psql: Path, host: str, port: int, dbname: str, user: str | None) -> str:
    run_id = psql_scalar(
        psql,
        host,
        port,
        dbname,
        """
        select cr.calculation_run_id
        from audit.calculation_run cr
        where cr.calculation_run_id like 'station_selection_review_%'
          and cr.run_status = 'succeeded'
          and exists (
              select 1
              from link.station_selection_review review
              where review.calculation_run_id = cr.calculation_run_id
          )
        order by cr.run_started_at_utc desc
        limit 1
        """,
        user,
    )
    if not run_id:
        raise RuntimeError("No station-selection review run found.")
    return run_id


def template_query(source_review_run_id: str) -> str:
    return f"""
with source_reviews as (
    select *
    from link.station_selection_review
    where calculation_run_id = {sql_literal(source_review_run_id)}
),
plant_run as (
    select
        sr.readiness_run_id,
        cr.parameters_json->>'plant_ecwt_run_id' as plant_ecwt_run_id
    from source_reviews sr
    join audit.calculation_run cr
      on cr.calculation_run_id = sr.readiness_run_id
    group by sr.readiness_run_id, cr.parameters_json
),
candidate_run as (
    select
        pr.readiness_run_id,
        pcr.parameters_json->>'candidate_run_id' as candidate_run_id
    from plant_run pr
    join audit.calculation_run pcr
      on pcr.calculation_run_id = pr.plant_ecwt_run_id
)
select
    sr.station_selection_review_id as source_station_selection_review_id,
    sr.calculation_run_id as source_review_run_id,
    sr.readiness_run_id,
    sr.plant_ecwt_readiness_id,
    sr.plant_ecwt_id,
    sr.station_selection_id,
    sr.plant_id,
    p.eia_plant_code,
    p.plant_name,
    p.state as plant_state,
    p.county as plant_county,
    sr.station_id,
    st.station_name,
    st.state as station_state,
    st.country as station_country,
    round(sc.distance_km, 3)::text as selected_distance_km,
    sc.rank_order::text as selected_rank_order,
    round(r.coverage_ratio, 6)::text as coverage_ratio,
    round(pe.governing_ecwt_f, 3)::text as governing_ecwt_f,
    sr.review_status as current_review_status,
    sr.review_basis as current_review_basis,
    coalesce(sr.reviewer, '') as current_reviewer,
    coalesce(sr.risk_flags, '') as risk_flags,
    sr.risk_flag_count::text as risk_flag_count,
    sr.disposition_reason as current_disposition_reason,
    coalesce(sr.notes, '') as current_notes,
    ''::text as proposed_review_status,
    ''::text as proposed_review_basis,
    ''::text as proposed_disposition_reason,
    ''::text as reviewer,
    ''::text as review_notes
from source_reviews sr
join calc.plant_ecwt_readiness r
  on r.plant_ecwt_readiness_id = sr.plant_ecwt_readiness_id
join calc.plant_ecwt pe
  on pe.plant_ecwt_id = sr.plant_ecwt_id
join asset.plant p
  on p.plant_id = sr.plant_id
join weather.station st
  on st.station_id = sr.station_id
left join candidate_run crun
  on crun.readiness_run_id = sr.readiness_run_id
left join link.station_candidate sc
  on sc.calculation_run_id = crun.candidate_run_id
 and sc.plant_id = sr.plant_id
 and sc.station_id = sr.station_id
order by p.state, p.eia_plant_code, p.plant_name
"""


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing = [field for field in TEMPLATE_FIELDS if field not in (reader.fieldnames or [])]
        if missing:
            raise RuntimeError(f"Input CSV is missing required columns: {', '.join(missing)}")
        return list(reader)


def default_disposition(status: str, basis: str, risk_flags: str, current_reason: str) -> str:
    if status == "accepted":
        if risk_flags:
            return "policy_override_accept_with_qa_flags" if basis == "policy_override" else "manual_accept_with_qa_flags"
        return "manual_accept_no_qa_flags"
    if status == "rejected":
        return "manual_reject_station_selection"
    return current_reason or "needs_review_qa_flags"


def build_review_rows(input_rows: list[dict[str, str]], run_id: str) -> tuple[list[dict[str, object]], list[str]]:
    seen: set[str] = set()
    errors: list[str] = []
    review_rows: list[dict[str, object]] = []
    for index, row in enumerate(input_rows, start=2):
        source_id = row["source_station_selection_review_id"].strip()
        if not source_id:
            errors.append(f"row {index}: source_station_selection_review_id is blank")
            continue
        if source_id in seen:
            errors.append(f"row {index}: duplicate source_station_selection_review_id {source_id}")
            continue
        seen.add(source_id)

        proposed_status = row["proposed_review_status"].strip()
        status_changed = bool(proposed_status)
        status = proposed_status or row["current_review_status"].strip()
        if status not in VALID_REVIEW_STATUSES:
            errors.append(f"row {index}: invalid review status {status!r}")
            continue

        if status_changed:
            basis = row["proposed_review_basis"].strip() or "manual_review"
            if basis not in VALID_REVIEW_BASES:
                errors.append(f"row {index}: invalid proposed_review_basis {basis!r}")
                continue
            reviewer = row["reviewer"].strip()
            notes = row["review_notes"].strip()
            if status in {"accepted", "rejected"} and not reviewer:
                errors.append(f"row {index}: reviewer is required when accepting or rejecting a row")
            if status in {"accepted", "rejected"} and not notes:
                errors.append(f"row {index}: review_notes is required when accepting or rejecting a row")
            disposition = row["proposed_disposition_reason"].strip() or default_disposition(
                status, basis, row["risk_flags"].strip(), row["current_disposition_reason"].strip()
            )
        else:
            basis = row["current_review_basis"].strip()
            reviewer = row["current_reviewer"].strip()
            notes = row["current_notes"].strip()
            disposition = row["current_disposition_reason"].strip()

        if errors and any(error.startswith(f"row {index}:") for error in errors):
            continue

        station_selection_id = row["station_selection_id"].strip()
        review_rows.append(
            {
                "station_selection_review_id": f"{run_id}:station_selection:{station_selection_id}",
                "calculation_run_id": run_id,
                "readiness_run_id": row["readiness_run_id"].strip(),
                "plant_ecwt_readiness_id": row["plant_ecwt_readiness_id"].strip(),
                "plant_ecwt_id": row["plant_ecwt_id"].strip(),
                "station_selection_id": station_selection_id,
                "plant_id": row["plant_id"].strip(),
                "station_id": row["station_id"].strip(),
                "review_status": status,
                "review_basis": basis,
                "reviewer": reviewer,
                "risk_flags": row["risk_flags"].strip(),
                "risk_flag_count": int(row["risk_flag_count"] or 0),
                "disposition_reason": disposition,
                "notes": notes,
            }
        )
    return review_rows, errors


def validate_complete_snapshot(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    source_review_run_id: str,
    input_rows: list[dict[str, str]],
) -> None:
    expected = int(
        psql_scalar(
            psql,
            host,
            port,
            dbname,
            f"select count(*) from link.station_selection_review where calculation_run_id = {sql_literal(source_review_run_id)}",
            user,
        )
    )
    if len(input_rows) != expected:
        raise RuntimeError(f"Input CSV has {len(input_rows)} rows, but source review run has {expected} rows.")
    source_ids = {row["source_station_selection_review_id"].strip() for row in input_rows}
    db_ids = {
        row["station_selection_review_id"]
        for row in psql_csv_query(
            psql,
            host,
            port,
            dbname,
            f"""
            select station_selection_review_id
            from link.station_selection_review
            where calculation_run_id = {sql_literal(source_review_run_id)}
            """,
            user,
        )
    }
    missing = sorted(db_ids - source_ids)
    extra = sorted(source_ids - db_ids)
    if missing or extra:
        raise RuntimeError(
            "Input CSV must be a complete snapshot of the source review run. "
            f"Missing IDs: {len(missing)}; extra IDs: {len(extra)}."
        )


def render_report(
    path: Path,
    run_id: str,
    source_review_run_id: str,
    input_path: Path,
    output_csv: Path,
    code_commit: str,
    review_rows: list[dict[str, object]],
    count_rows: list[dict[str, str]] | None,
    dry_run: bool,
) -> None:
    status_counts = Counter(str(row["review_status"]) for row in review_rows)
    basis_counts = Counter(str(row["review_basis"]) for row in review_rows)
    reason_counts = Counter(str(row["disposition_reason"]) for row in review_rows)
    release_counts = []
    if count_rows:
        release_counts = [row for row in count_rows if row["section"] == "release_readiness"]
    lines = [
        "# Station Selection Review Update Report",
        "",
        f"Generated UTC: {utc_now().isoformat(timespec='seconds')}",
        "",
        "## Summary",
        "",
        f"- Update run ID: `{run_id}`",
        f"- Source review run ID: `{source_review_run_id}`",
        f"- Code commit: `{code_commit}`",
        f"- Input CSV: `{input_path}`",
        f"- Output review snapshot CSV: `{output_csv.name}`",
        f"- Dry run: `{dry_run}`",
        "",
        "## Review Status Counts",
        "",
        "| Review Status | Rows |",
        "| --- | ---: |",
    ]
    for key, count in status_counts.most_common():
        lines.append(f"| `{key}` | {count:,} |")
    lines.extend(["", "## Review Basis Counts", "", "| Review Basis | Rows |", "| --- | ---: |"])
    for key, count in basis_counts.most_common():
        lines.append(f"| `{key}` | {count:,} |")
    lines.extend(["", "## Disposition Reasons", "", "| Reason | Rows |", "| --- | ---: |"])
    for key, count in reason_counts.most_common():
        lines.append(f"| `{key}` | {count:,} |")
    if release_counts:
        lines.extend(["", "## Release Readiness Counts", "", "| Release Status | Rows |", "| --- | ---: |"])
        for row in release_counts:
            lines.append(f"| `{row['key']}` | {int(row['rows']):,} |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- This tool creates a complete review snapshot. Blank proposed fields preserve the source review disposition.",
            "- Accepted rows become release-ready only after the DB write rebuilds `publish.plant_ecwt_release_readiness`.",
            "- Rejected rows remain blocked with their disposition reason.",
            "- Dry-run mode validates and summarizes the worksheet without writing to Postgres.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--staging-root", type=Path, default=STAGING_ROOT)
    parser.add_argument("--psql", type=Path, default=PSQL)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5436)
    parser.add_argument("--dbname", default="eop012")
    parser.add_argument("--user")
    parser.add_argument("--source-review-run-id")
    parser.add_argument("--write-template", type=Path)
    parser.add_argument("--input-csv", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if bool(args.write_template) == bool(args.input_csv):
        raise RuntimeError("Specify exactly one of --write-template or --input-csv.")

    source_review_run_id = args.source_review_run_id or latest_review_run_id(
        args.psql, args.host, args.port, args.dbname, args.user
    )
    code_commit = git_commit_label(args.project_root)

    if args.write_template:
        rows = psql_csv_query(args.psql, args.host, args.port, args.dbname, template_query(source_review_run_id), args.user)
        output_path = args.write_template
        if not output_path.is_absolute():
            output_path = args.project_root / output_path
        write_csv(output_path, TEMPLATE_FIELDS, rows)
        print(
            json.dumps(
                OrderedDict(
                    [
                        ("source_review_run_id", source_review_run_id),
                        ("template_rows", len(rows)),
                        ("template_path", str(output_path)),
                    ]
                ),
                indent=2,
            )
        )
        return

    input_path = args.input_csv
    if not input_path.is_absolute():
        input_path = args.project_root / input_path
    input_rows = read_csv_rows(input_path)
    validate_complete_snapshot(args.psql, args.host, args.port, args.dbname, args.user, source_review_run_id, input_rows)

    timestamp = utc_now().strftime("%Y%m%dT%H%M%SZ")
    run_id = f"station_selection_review_update_{timestamp}"
    review_rows, errors = build_review_rows(input_rows, run_id)
    if errors:
        raise RuntimeError("Review update validation failed:\n" + "\n".join(errors[:25]))

    docs_dir = args.project_root / "docs"
    output_csv = docs_dir / f"{run_id}.csv"
    write_csv(output_csv, REVIEW_FIELDS, review_rows)

    count_rows = None
    if not args.dry_run:
        staging_dir = args.staging_root / run_id
        staging_dir.mkdir(parents=True, exist_ok=True)
        staging_csv = staging_dir / "station_selection_review_update.csv"
        write_csv(staging_csv, REVIEW_FIELDS, review_rows)
        sql = build_review_gate_sql(
            run_id,
            review_rows[0]["readiness_run_id"],
            code_commit,
            staging_csv,
            REVIEW_FIELDS,
            False,
            "Applied station-selection review updates and rebuilt release-readiness gate.",
        )
        sql_path = staging_dir / "station_selection_review_update.sql"
        sql_path.write_text(sql, encoding="utf-8")
        run(psql_cmd(args.psql, args.host, args.port, args.dbname, args.user) + ["-f", str(sql_path)])
        count_rows = psql_csv_query(args.psql, args.host, args.port, args.dbname, count_query(run_id), args.user)

    report_path = docs_dir / f"{run_id}_report.md"
    render_report(report_path, run_id, source_review_run_id, input_path, output_csv, code_commit, review_rows, count_rows, args.dry_run)
    print(
        json.dumps(
            OrderedDict(
                [
                    ("run_id", run_id),
                    ("source_review_run_id", source_review_run_id),
                    ("dry_run", args.dry_run),
                    ("review_rows", len(review_rows)),
                    ("review_csv", str(output_csv)),
                    ("report_path", str(report_path)),
                    ("counts", count_rows or []),
                ]
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
