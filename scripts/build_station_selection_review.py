#!/usr/bin/env python3
"""Seed station-selection review dispositions and release-readiness gates."""

from __future__ import annotations

import argparse
import csv
import io
import json
import subprocess
from collections import Counter, OrderedDict
from datetime import datetime, timezone
from pathlib import Path

from build_station_selection_qa_report import add_qa_flags, build_candidate_sql
from eop012_config import PROJECT_ROOT, PSQL, STAGING_ROOT

METHODOLOGY_VERSION = "eop012-ecwt-method-v0.1.0"
REVIEWER = "system_policy_seed"
REVIEW_BASIS = "automated_policy_seed"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def sql_literal(value: object) -> str:
    if value is None:
        return "null"
    text = str(value)
    return "'" + text.replace("'", "''") + "'"


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


def copy_command(table: str, columns: list[str], path: Path) -> str:
    cols = ", ".join(columns)
    return f"\\copy {table} ({cols}) from '{path}' with (format csv, header true, null '\\N')"


def git_commit_label(project_root: Path) -> str:
    try:
        result = run(["git", "-C", str(project_root), "rev-parse", "HEAD"])
        return result.stdout.strip()
    except Exception:
        return "UNCOMMITTED_WORKTREE"


def latest_fixed_readiness_run_id(psql: Path, host: str, port: int, dbname: str, user: str | None) -> str:
    run_id = psql_scalar(
        psql,
        host,
        port,
        dbname,
        """
        select calculation_run_id
        from audit.calculation_run
        where calculation_run_id like 'plant_ecwt_readiness_fixed_period_%'
          and run_status = 'succeeded'
        order by run_started_at_utc desc
        limit 1
        """,
        user,
    )
    if not run_id:
        raise RuntimeError("No succeeded fixed-period plant ECWT readiness run found.")
    return run_id


def disposition_reason(flags: list[str]) -> str:
    flag_set = set(flags)
    if not flags:
        return "accepted_no_qa_flags"
    if "station_country_not_us" in flag_set:
        return "needs_policy_cross_border_station"
    if "distance_gt_75km" in flag_set:
        return "needs_review_high_distance"
    if "selected_rank_gt_3" in flag_set:
        return "needs_review_high_candidate_rank"
    if "plant_station_state_mismatch" in flag_set:
        return "needs_review_state_mismatch"
    if "coverage_below_0_97" in flag_set:
        return "needs_review_near_threshold_coverage"
    return "needs_review_qa_flags"


def review_notes(flags: list[str]) -> str:
    if not flags:
        return "Automated seed accepted this station selection because no QA flags were present."
    return "Manual review required before release because QA flags were present: " + ";".join(flags)


def build_review_rows(qa_rows: list[dict[str, str]], run_id: str, auto_accept_clean: bool) -> list[dict[str, object]]:
    review_rows: list[dict[str, object]] = []
    for row in qa_rows:
        flags = [flag for flag in row.get("risk_flags", "").split(";") if flag]
        if not flags and auto_accept_clean:
            review_status = "accepted"
        else:
            review_status = "needs_review"
        review_id = f"{run_id}:station_selection:{row['station_selection_id']}"
        review_rows.append(
            {
                "station_selection_review_id": review_id,
                "calculation_run_id": run_id,
                "readiness_run_id": row["readiness_run_id"],
                "plant_ecwt_readiness_id": row["plant_ecwt_readiness_id"],
                "plant_ecwt_id": row["plant_ecwt_id"],
                "station_selection_id": row["station_selection_id"],
                "plant_id": row["plant_id"],
                "station_id": row["selected_station_id"],
                "review_status": review_status,
                "review_basis": REVIEW_BASIS,
                "reviewer": REVIEWER,
                "risk_flags": ";".join(flags),
                "risk_flag_count": len(flags),
                "disposition_reason": disposition_reason(flags),
                "notes": review_notes(flags),
            }
        )
    return review_rows


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: pg_csv_value(row.get(field)) for field in fieldnames})


def build_sql(
    run_id: str,
    readiness_run_id: str,
    code_commit: str,
    staging_csv: Path,
    review_cols: list[str],
    auto_accept_clean: bool,
    operation_note: str = "Seeded station-selection review dispositions and built release-readiness gate.",
) -> str:
    start = utc_now().isoformat(timespec="seconds")
    params = {
        "readiness_run_id": readiness_run_id,
        "review_basis": REVIEW_BASIS,
        "reviewer": REVIEWER,
        "auto_accept_clean": auto_accept_clean,
        "release_rule": "release_ready requires plant readiness publication_candidate and station-selection review_status accepted",
    }
    return f"""
\\set ON_ERROR_STOP on
begin;

create table if not exists link.station_selection_review (
    station_selection_review_id text primary key,
    calculation_run_id text not null references audit.calculation_run(calculation_run_id),
    readiness_run_id text not null references audit.calculation_run(calculation_run_id),
    plant_ecwt_readiness_id text not null references calc.plant_ecwt_readiness(plant_ecwt_readiness_id),
    plant_ecwt_id text not null references calc.plant_ecwt(plant_ecwt_id),
    station_selection_id text not null references link.station_selection(station_selection_id),
    plant_id text not null references asset.plant(plant_id),
    station_id text not null references weather.station(station_id),
    review_status text not null,
    review_basis text not null,
    reviewer text,
    risk_flags text,
    risk_flag_count integer not null default 0,
    disposition_reason text not null,
    notes text,
    created_at_utc timestamptz not null default now(),
    unique (calculation_run_id, station_selection_id),
    constraint station_selection_review_status_check
        check (review_status in ('accepted', 'needs_review', 'rejected')),
    constraint station_selection_review_basis_check
        check (review_basis in ('automated_policy_seed', 'manual_review', 'policy_override')),
    constraint station_selection_review_risk_count_check
        check (risk_flag_count >= 0)
);
create index if not exists ix_station_selection_review_status
    on link.station_selection_review (calculation_run_id, review_status);
create index if not exists ix_station_selection_review_readiness
    on link.station_selection_review (readiness_run_id, plant_ecwt_readiness_id);

create table if not exists publish.plant_ecwt_release_readiness (
    plant_ecwt_release_readiness_id text primary key,
    calculation_run_id text not null references audit.calculation_run(calculation_run_id),
    readiness_run_id text not null references audit.calculation_run(calculation_run_id),
    plant_ecwt_readiness_id text not null references calc.plant_ecwt_readiness(plant_ecwt_readiness_id),
    plant_ecwt_id text not null references calc.plant_ecwt(plant_ecwt_id),
    plant_id text not null references asset.plant(plant_id),
    station_selection_review_id text references link.station_selection_review(station_selection_review_id),
    release_status text not null,
    reason_code text not null,
    notes text,
    created_at_utc timestamptz not null default now(),
    unique (calculation_run_id, plant_ecwt_readiness_id),
    constraint plant_ecwt_release_readiness_status_check
        check (release_status in (
            'release_ready',
            'blocked_readiness',
            'blocked_missing_review',
            'blocked_station_review',
            'blocked_policy_rejected'
        ))
);
create index if not exists ix_plant_ecwt_release_readiness_status
    on publish.plant_ecwt_release_readiness (calculation_run_id, release_status);

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
    {sql_literal(operation_note)}
)
on conflict (calculation_run_id) do update set
    run_finished_at_utc = excluded.run_finished_at_utc,
    run_status = excluded.run_status,
    parameters_json = excluded.parameters_json,
    notes = excluded.notes;

create temp table stg_station_selection_review (
    station_selection_review_id text,
    calculation_run_id text,
    readiness_run_id text,
    plant_ecwt_readiness_id text,
    plant_ecwt_id text,
    station_selection_id text,
    plant_id text,
    station_id text,
    review_status text,
    review_basis text,
    reviewer text,
    risk_flags text,
    risk_flag_count integer,
    disposition_reason text,
    notes text
);
{copy_command("stg_station_selection_review", review_cols, staging_csv)}

insert into link.station_selection_review (
    station_selection_review_id,
    calculation_run_id,
    readiness_run_id,
    plant_ecwt_readiness_id,
    plant_ecwt_id,
    station_selection_id,
    plant_id,
    station_id,
    review_status,
    review_basis,
    reviewer,
    risk_flags,
    risk_flag_count,
    disposition_reason,
    notes
)
select
    station_selection_review_id,
    calculation_run_id,
    readiness_run_id,
    plant_ecwt_readiness_id,
    plant_ecwt_id,
    station_selection_id,
    plant_id,
    station_id,
    review_status,
    review_basis,
    reviewer,
    risk_flags,
    risk_flag_count,
    disposition_reason,
    notes
from stg_station_selection_review
on conflict (calculation_run_id, station_selection_id) do update set
    review_status = excluded.review_status,
    review_basis = excluded.review_basis,
    reviewer = excluded.reviewer,
    risk_flags = excluded.risk_flags,
    risk_flag_count = excluded.risk_flag_count,
    disposition_reason = excluded.disposition_reason,
    notes = excluded.notes;

insert into publish.plant_ecwt_release_readiness (
    plant_ecwt_release_readiness_id,
    calculation_run_id,
    readiness_run_id,
    plant_ecwt_readiness_id,
    plant_ecwt_id,
    plant_id,
    station_selection_review_id,
    release_status,
    reason_code,
    notes
)
select
    {sql_literal(run_id)} || ':plant:' || r.plant_id as plant_ecwt_release_readiness_id,
    {sql_literal(run_id)} as calculation_run_id,
    r.calculation_run_id as readiness_run_id,
    r.plant_ecwt_readiness_id,
    r.plant_ecwt_id,
    r.plant_id,
    review.station_selection_review_id,
    case
        when r.readiness_status <> 'publication_candidate' then 'blocked_readiness'
        when review.station_selection_review_id is null then 'blocked_missing_review'
        when review.review_status = 'accepted' then 'release_ready'
        when review.review_status = 'rejected' then 'blocked_policy_rejected'
        else 'blocked_station_review'
    end as release_status,
    case
        when r.readiness_status <> 'publication_candidate' then 'upstream_' || r.reason_code
        when review.station_selection_review_id is null then 'station_selection_review_missing'
        when review.review_status = 'accepted' then 'station_selection_review_accepted'
        when review.review_status = 'rejected' then review.disposition_reason
        else review.disposition_reason
    end as reason_code,
    case
        when r.readiness_status <> 'publication_candidate' then 'Plant did not pass upstream fixed-period ECWT readiness.'
        when review.station_selection_review_id is null then 'No station-selection review row was found for this publication candidate.'
        when review.review_status = 'accepted' then 'Plant ECWT row passed upstream readiness and station-selection review.'
        else 'Plant ECWT row passed upstream readiness but station-selection review is not accepted.'
    end as notes
from calc.plant_ecwt_readiness r
join calc.plant_ecwt pe
  on pe.plant_ecwt_id = r.plant_ecwt_id
left join link.station_selection_review review
  on review.calculation_run_id = {sql_literal(run_id)}
 and review.plant_ecwt_readiness_id = r.plant_ecwt_readiness_id
where r.calculation_run_id = {sql_literal(readiness_run_id)}
on conflict (calculation_run_id, plant_ecwt_readiness_id) do update set
    station_selection_review_id = excluded.station_selection_review_id,
    release_status = excluded.release_status,
    reason_code = excluded.reason_code,
    notes = excluded.notes;

commit;
"""


def count_query(run_id: str) -> str:
    return f"""
select 'station_selection_review' as section, review_status as key, count(*)::text as rows
from link.station_selection_review
where calculation_run_id = {sql_literal(run_id)}
group by review_status
union all
select 'station_selection_review_reason', disposition_reason, count(*)::text
from link.station_selection_review
where calculation_run_id = {sql_literal(run_id)}
group by disposition_reason
union all
select 'release_readiness', release_status, count(*)::text
from publish.plant_ecwt_release_readiness
where calculation_run_id = {sql_literal(run_id)}
group by release_status
union all
select 'release_readiness_reason', reason_code, count(*)::text
from publish.plant_ecwt_release_readiness
where calculation_run_id = {sql_literal(run_id)}
group by reason_code
order by section, key
"""


def md_table(rows: list[dict[str, str]], fields: list[str], headers: list[str], limit: int | None = None) -> list[str]:
    if not rows:
        return ["_None._"]
    selected = rows if limit is None else rows[:limit]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in selected:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("|", "\\|") for field in fields) + " |")
    if limit is not None and len(rows) > limit:
        lines.append("| ... | " + f"{len(rows) - limit} more rows omitted" + " |" * (len(fields) - 1))
    return lines


def render_report(
    path: Path,
    csv_path: Path,
    run_id: str,
    readiness_run_id: str,
    code_commit: str,
    review_rows: list[dict[str, object]],
    count_rows: list[dict[str, str]],
) -> None:
    review_status_counts = Counter(str(row["review_status"]) for row in review_rows)
    reason_counts = Counter(str(row["disposition_reason"]) for row in review_rows)
    flag_counts: Counter[str] = Counter()
    for row in review_rows:
        for flag in str(row.get("risk_flags") or "").split(";"):
            if flag:
                flag_counts[flag] += 1
    release_rows = [row for row in count_rows if row["section"] == "release_readiness"]
    review_rows_md = [
        {"review_status": status, "rows": f"{count:,}"}
        for status, count in review_status_counts.most_common()
    ]
    reason_rows_md = [
        {"reason": reason, "rows": f"{count:,}"}
        for reason, count in reason_counts.most_common()
    ]
    flag_rows_md = [
        {"flag": flag, "rows": f"{count:,}"}
        for flag, count in flag_counts.most_common()
    ]
    release_rows_md = [
        {"release_status": row["key"], "rows": f"{int(row['rows']):,}"}
        for row in release_rows
    ]
    lines = [
        "# Station Selection Review Seed and Release Readiness Gate",
        "",
        f"Generated UTC: {utc_now().isoformat(timespec='seconds')}",
        "",
        "## Summary",
        "",
        (
            f"This run seeded `{len(review_rows):,}` station-selection review rows for fixed-period publication candidates "
            f"from readiness run `{readiness_run_id}`. The seed is intentionally conservative: rows with any QA flag are "
            "`needs_review`, and only clean rows can be automatically accepted."
        ),
        "",
        "Release readiness now requires both upstream fixed-period ECWT readiness and an accepted station-selection review. "
        "Because the current fixed-period candidate set still has QA flags on every row, this run produces no release-ready rows.",
        "",
        "## Run",
        "",
        f"- Review run ID: `{run_id}`",
        f"- Readiness run ID: `{readiness_run_id}`",
        f"- Code commit: `{code_commit}`",
        f"- Review CSV: `{csv_path.name}`",
        "",
        "## Review Status Counts",
        "",
    ]
    lines.extend(md_table(review_rows_md, ["review_status", "rows"], ["Review Status", "Rows"]))
    lines.extend(["", "## Release Readiness Counts", ""])
    lines.extend(md_table(release_rows_md, ["release_status", "rows"], ["Release Status", "Rows"]))
    lines.extend(["", "## Review Disposition Reasons", ""])
    lines.extend(md_table(reason_rows_md, ["reason", "rows"], ["Disposition Reason", "Rows"], limit=20))
    lines.extend(["", "## QA Flag Counts", ""])
    lines.extend(md_table(flag_rows_md, ["flag", "rows"], ["QA Flag", "Rows"], limit=20))
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `link.station_selection_review` is the auditable disposition layer for plant-to-station assignments.",
            "- `publish.plant_ecwt_release_readiness` is the current release gate. It is stricter than `calc.plant_ecwt_readiness` because it blocks rows that have not been accepted by station-selection review.",
            "- This run does not make policy decisions about cross-border, high-rank, high-distance, or near-threshold stations. It records them as review work.",
            "- A future manual or policy-override run can update review dispositions to `accepted` or `rejected`, after which release readiness can be rebuilt.",
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
    parser.add_argument("--readiness-run-id")
    parser.add_argument("--no-auto-accept-clean", action="store_true")
    parser.add_argument("--distance-review-km", type=float, default=50.0)
    parser.add_argument("--high-distance-km", type=float, default=75.0)
    parser.add_argument("--near-threshold-coverage", type=float, default=0.97)
    parser.add_argument("--shared-station-review-count", type=int, default=10)
    parser.add_argument("--high-shared-station-count", type=int, default=25)
    parser.add_argument("--old-station-last-year", type=int, default=2010)
    parser.add_argument("--warm-mainland-ecwt-f", type=float, default=32.0)
    parser.add_argument("--warm-ecwt-f", type=float, default=35.0)
    args = parser.parse_args()

    readiness_run_id = args.readiness_run_id or latest_fixed_readiness_run_id(
        args.psql, args.host, args.port, args.dbname, args.user
    )
    run_id = f"station_selection_review_seed_{utc_now().strftime('%Y%m%dT%H%M%SZ')}"
    code_commit = git_commit_label(args.project_root)
    qa_rows = psql_csv_query(args.psql, args.host, args.port, args.dbname, build_candidate_sql(readiness_run_id), args.user)
    add_qa_flags(qa_rows, args)
    review_rows = build_review_rows(qa_rows, run_id, not args.no_auto_accept_clean)

    review_cols = [
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
    staging_dir = args.staging_root / run_id
    staging_dir.mkdir(parents=True, exist_ok=True)
    staging_csv = staging_dir / "station_selection_review.csv"
    docs_dir = args.project_root / "docs"
    docs_csv = docs_dir / f"{run_id}.csv"
    write_csv(staging_csv, review_cols, review_rows)
    write_csv(docs_csv, review_cols, review_rows)

    sql = build_sql(run_id, readiness_run_id, code_commit, staging_csv, review_cols, not args.no_auto_accept_clean)
    sql_path = staging_dir / "station_selection_review.sql"
    sql_path.write_text(sql, encoding="utf-8")
    run(psql_cmd(args.psql, args.host, args.port, args.dbname, args.user) + ["-f", str(sql_path)])

    count_rows = psql_csv_query(args.psql, args.host, args.port, args.dbname, count_query(run_id), args.user)
    report_path = docs_dir / f"{run_id}_report.md"
    render_report(report_path, docs_csv, run_id, readiness_run_id, code_commit, review_rows, count_rows)
    print(
        json.dumps(
            OrderedDict(
                [
                    ("run_id", run_id),
                    ("readiness_run_id", readiness_run_id),
                    ("review_rows", len(review_rows)),
                    ("review_csv", str(docs_csv)),
                    ("report_path", str(report_path)),
                    ("counts", count_rows),
                ]
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
