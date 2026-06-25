#!/usr/bin/env python3
"""Audit ECWT publication scope coverage against EIA generator status."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import subprocess
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from eop012_config import PROJECT_ROOT, PSQL


METHODOLOGY_VERSION = "eop012-ecwt-method-v0.1.0"
FIRST_OPERABLE_STATUSES = ("OP", "SB", "OA", "OS")

SUMMARY_FIELDS = ["scope_audit_run_id", "metric", "value", "notes"]
GAP_FIELDS = [
    "scope_audit_run_id",
    "policy_result_run_id",
    "exception_review_run_id",
    "gap_type",
    "plant_id",
    "eia_plant_code",
    "generator_id",
    "utility_id",
    "utility_name",
    "plant_name",
    "state",
    "county",
    "technology",
    "prime_mover",
    "nameplate_capacity_mw",
    "summer_capacity_mw",
    "winter_capacity_mw",
    "status",
    "recommended_next_action",
    "notes",
]


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def sql_literal(value: object) -> str:
    if value is None:
        return "null"
    return "'" + str(value).replace("'", "''") + "'"


def sql_list(values: tuple[str, ...]) -> str:
    return ", ".join(sql_literal(value) for value in values)


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


def psql_scalar(psql: Path, host: str, port: int, dbname: str, user: str | None, query: str) -> str:
    result = run(psql_cmd(psql, host, port, dbname, user) + ["-At", "-c", query])
    return result.stdout.strip()


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


def latest_run_id(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    prefix: str,
) -> str:
    run_id = psql_scalar(
        psql,
        host,
        port,
        dbname,
        user,
        f"""
        select calculation_run_id
        from audit.calculation_run
        where calculation_run_id like {sql_literal(prefix + "%")}
          and run_status = 'succeeded'
        order by run_started_at_utc desc
        limit 1
        """,
    )
    if not run_id:
        raise RuntimeError(f"No succeeded run found with prefix {prefix!r}.")
    return run_id


def git_commit_label(project_root: Path) -> str:
    try:
        dirty = run(["git", "-C", str(project_root), "status", "--porcelain"]).stdout.strip()
        head = run(["git", "-C", str(project_root), "rev-parse", "HEAD"]).stdout.strip()
        return f"{head}-dirty" if dirty else head
    except Exception:
        return "UNKNOWN_GIT_COMMIT"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: "" if row.get(field) is None else row.get(field, "") for field in fieldnames})


def source_row(path: Path, family: str, source_release: str) -> dict[str, object]:
    digest = sha256_file(path)
    return {
        "source_file_id": f"{family}:{digest}",
        "source_family": family,
        "local_path": str(path),
        "file_name": path.name,
        "size_bytes": path.stat().st_size,
        "sha256": digest,
        "retrieved_at_utc": datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat(),
        "source_release": source_release,
        "notes": "Generated EOP012 ECWT scope-readiness audit artifact.",
    }


def summary_metrics(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    policy_result_run_id: str,
    exception_review_run_id: str,
) -> OrderedDict[str, str]:
    status_sql = sql_list(FIRST_OPERABLE_STATUSES)
    queries = OrderedDict(
        [
            ("asset.plant rows", "select count(*) from asset.plant;"),
            (
                "generator-derived first-operable plant ids",
                f"""
                select count(distinct ('eia860:2024:plant:' || eia_plant_code)::text)
                from asset.generator
                where status in ({status_sql});
                """,
            ),
            (
                "generator-derived first-operable ids with asset.plant rows",
                f"""
                with operable as (
                    select distinct ('eia860:2024:plant:' || eia_plant_code)::text as plant_id
                    from asset.generator
                    where status in ({status_sql})
                )
                select count(*)
                from operable
                join asset.plant using (plant_id);
                """,
            ),
            (
                "generator-derived first-operable ids missing asset.plant rows",
                f"""
                with operable as (
                    select distinct ('eia860:2024:plant:' || eia_plant_code)::text as plant_id
                    from asset.generator
                    where status in ({status_sql})
                )
                select count(*)
                from operable
                left join asset.plant using (plant_id)
                where asset.plant.plant_id is null;
                """,
            ),
            (
                "policy result rows",
                f"select count(*) from calc.plant_ecwt_policy_result where policy_result_run_id = {sql_literal(policy_result_run_id)};",
            ),
            (
                "policy result first-operable rows",
                f"""
                with operable as (
                    select distinct ('eia860:2024:plant:' || eia_plant_code)::text as plant_id
                    from asset.generator
                    where status in ({status_sql})
                )
                select count(*)
                from calc.plant_ecwt_policy_result r
                join operable using (plant_id)
                where r.policy_result_run_id = {sql_literal(policy_result_run_id)};
                """,
            ),
            (
                "first-operable publication candidates",
                f"""
                with operable as (
                    select distinct ('eia860:2024:plant:' || eia_plant_code)::text as plant_id
                    from asset.generator
                    where status in ({status_sql})
                )
                select count(*)
                from calc.plant_ecwt_policy_result r
                join operable using (plant_id)
                where r.policy_result_run_id = {sql_literal(policy_result_run_id)}
                  and r.readiness_status = 'publication_candidate';
                """,
            ),
            (
                "first-operable blocked rows",
                f"""
                with operable as (
                    select distinct ('eia860:2024:plant:' || eia_plant_code)::text as plant_id
                    from asset.generator
                    where status in ({status_sql})
                )
                select count(*)
                from calc.plant_ecwt_policy_result r
                join operable using (plant_id)
                where r.policy_result_run_id = {sql_literal(policy_result_run_id)}
                  and r.readiness_status = 'blocked';
                """,
            ),
            (
                "exception review plant_geocode_required",
                f"""
                select count(*)
                from calc.plant_ecwt_exception_review
                where exception_review_run_id = {sql_literal(exception_review_run_id)}
                  and resolution_category = 'plant_geocode_required';
                """,
            ),
            (
                "exception review coverage_threshold_exception_review",
                f"""
                select count(*)
                from calc.plant_ecwt_exception_review
                where exception_review_run_id = {sql_literal(exception_review_run_id)}
                  and resolution_category = 'coverage_threshold_exception_review';
                """,
            ),
        ]
    )
    return OrderedDict(
        (label, psql_scalar(psql, host, port, dbname, user, query)) for label, query in queries.items()
    )


def missing_operable_asset_rows(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    run_id: str,
    policy_result_run_id: str,
    exception_review_run_id: str,
) -> list[dict[str, object]]:
    status_sql = sql_list(FIRST_OPERABLE_STATUSES)
    rows = psql_csv_query(
        psql,
        host,
        port,
        dbname,
        user,
        f"""
        with operable_missing as (
            select
                ('eia860:2024:plant:' || g.eia_plant_code)::text as plant_id,
                g.*
            from asset.generator g
            left join asset.plant p
              on p.plant_id = ('eia860:2024:plant:' || g.eia_plant_code)::text
            where g.status in ({status_sql})
              and p.plant_id is null
        )
        select
            plant_id,
            eia_plant_code,
            generator_id,
            utility_id::text as utility_id,
            utility_name,
            plant_name,
            state,
            county,
            technology,
            prime_mover,
            nameplate_capacity_mw::text as nameplate_capacity_mw,
            summer_capacity_mw::text as summer_capacity_mw,
            winter_capacity_mw::text as winter_capacity_mw,
            status
        from operable_missing
        order by eia_plant_code, generator_id
        """,
    )
    result: list[dict[str, object]] = []
    for row in rows:
        result.append(
            {
                "scope_audit_run_id": run_id,
                "policy_result_run_id": policy_result_run_id,
                "exception_review_run_id": exception_review_run_id,
                "gap_type": "first_operable_generator_missing_asset_plant",
                "plant_id": row["plant_id"],
                "eia_plant_code": row["eia_plant_code"],
                "generator_id": row["generator_id"],
                "utility_id": row["utility_id"],
                "utility_name": row["utility_name"],
                "plant_name": row["plant_name"],
                "state": row["state"],
                "county": row["county"],
                "technology": row["technology"],
                "prime_mover": row["prime_mover"],
                "nameplate_capacity_mw": row["nameplate_capacity_mw"],
                "summer_capacity_mw": row["summer_capacity_mw"],
                "winter_capacity_mw": row["winter_capacity_mw"],
                "status": row["status"],
                "recommended_next_action": (
                    "Resolve missing plant-level EIA identity/location before including this first-operable "
                    "generator in station matching or publication denominator."
                ),
                "notes": "Generator appears in EIA-860 operable table but has no matching asset.plant row.",
            }
        )
    return result


def build_summary_rows(run_id: str, metrics: OrderedDict[str, str]) -> list[dict[str, object]]:
    notes = {
        "generator-derived first-operable ids missing asset.plant rows": (
            "These first-operable generator plant IDs cannot be station-matched until plant identity/location is resolved."
        ),
        "exception review plant_geocode_required": (
            "These are all construction-only asset.plant rows, not first-operable publication blockers."
        ),
        "exception review coverage_threshold_exception_review": (
            "These are the remaining first-operable ECWT blockers after normalized active-window policy materialization."
        ),
    }
    return [
        {
            "scope_audit_run_id": run_id,
            "metric": metric,
            "value": value,
            "notes": notes.get(metric, ""),
        }
        for metric, value in metrics.items()
    ]


def qident(name: str) -> str:
    if not name.replace("_", "").isalnum() or name[0].isdigit():
        raise ValueError(f"Unsafe SQL identifier: {name}")
    return name


def temp_table_sql(table_name: str, fields: list[str]) -> str:
    cols = ",\n        ".join(f"{qident(field)} text" for field in fields)
    return f"create temp table {table_name} (\n        {cols}\n    ) on commit drop;"


def copy_sql(table_name: str, fields: list[str], path: Path) -> str:
    cols = ", ".join(qident(field) for field in fields)
    return f"\\copy {table_name} ({cols}) from {sql_literal(path)} with (format csv, header true, null '')"


def text_null(field: str) -> str:
    return f"nullif(nullif({qident(field)}, ''), '\\N')"


def nullif_cast(field: str, cast_type: str) -> str:
    return f"nullif(nullif({qident(field)}, ''), '\\N')::{cast_type}"


def build_load_sql(
    run_id: str,
    code_commit: str,
    started_at: str,
    params: dict[str, object],
    gap_csv: Path,
    gap_source: dict[str, object],
) -> str:
    return f"""
\\set ON_ERROR_STOP on
begin;

create table if not exists calc.plant_ecwt_scope_gap (
    scope_gap_id text primary key,
    scope_audit_run_id text not null references audit.calculation_run(calculation_run_id),
    policy_result_run_id text not null references audit.calculation_run(calculation_run_id),
    exception_review_run_id text references audit.calculation_run(calculation_run_id),
    gap_type text not null,
    plant_id text not null,
    eia_plant_code text,
    generator_id text,
    utility_id text,
    utility_name text,
    plant_name text,
    state text,
    county text,
    technology text,
    prime_mover text,
    nameplate_capacity_mw numeric,
    summer_capacity_mw numeric,
    winter_capacity_mw numeric,
    status text,
    recommended_next_action text not null,
    notes text,
    created_at_utc timestamptz not null default now(),
    unique (scope_audit_run_id, plant_id, generator_id, gap_type)
);
create index if not exists ix_plant_ecwt_scope_gap_run_type
    on calc.plant_ecwt_scope_gap (scope_audit_run_id, gap_type);

insert into audit.methodology_version (
    methodology_version,
    methodology_name,
    effective_at_utc,
    source_standard,
    notes
) values (
    {sql_literal(METHODOLOGY_VERSION)},
    'EOP012 ECWT national calculation methodology',
    {sql_literal(started_at)},
    'NERC EOP-012-3; EPRI 3002030362 guidance',
    'Initial auditable methodology version for asset loading, station matching, raw file inventory, backfill planning, download attempts, coverage auditing, ECWT calculation, policy materialization, exception review, and publication scope audit.'
)
on conflict (methodology_version) do update set notes = excluded.notes;

insert into audit.source_file (
    source_file_id, source_family, source_url, local_path, file_name, size_bytes,
    sha256, retrieved_at_utc, source_year, source_release, notes
) values (
    {sql_literal(gap_source["source_file_id"])},
    {sql_literal(gap_source["source_family"])},
    null,
    {sql_literal(gap_source["local_path"])},
    {sql_literal(gap_source["file_name"])},
    {gap_source["size_bytes"]},
    {sql_literal(gap_source["sha256"])},
    {sql_literal(gap_source["retrieved_at_utc"])},
    null,
    {sql_literal(gap_source["source_release"])},
    {sql_literal(gap_source["notes"])}
)
on conflict (source_file_id) do update set
    local_path = excluded.local_path,
    size_bytes = excluded.size_bytes,
    sha256 = excluded.sha256,
    retrieved_at_utc = excluded.retrieved_at_utc,
    source_release = excluded.source_release,
    notes = excluded.notes;

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
    {sql_literal(started_at)},
    now(),
    'succeeded',
    {sql_literal(json.dumps(params, sort_keys=True))}::jsonb,
    'Audited ECWT publication scope against first-operable EIA generator plant IDs.'
)
on conflict (calculation_run_id) do update set
    run_finished_at_utc = excluded.run_finished_at_utc,
    run_status = excluded.run_status,
    parameters_json = excluded.parameters_json,
    notes = excluded.notes;

{temp_table_sql("tmp_scope_gap", GAP_FIELDS)}
{copy_sql("tmp_scope_gap", GAP_FIELDS, gap_csv)}

delete from calc.plant_ecwt_scope_gap
where scope_audit_run_id = {sql_literal(run_id)};

insert into calc.plant_ecwt_scope_gap (
    scope_gap_id,
    scope_audit_run_id,
    policy_result_run_id,
    exception_review_run_id,
    gap_type,
    plant_id,
    eia_plant_code,
    generator_id,
    utility_id,
    utility_name,
    plant_name,
    state,
    county,
    technology,
    prime_mover,
    nameplate_capacity_mw,
    summer_capacity_mw,
    winter_capacity_mw,
    status,
    recommended_next_action,
    notes
)
select
    {sql_literal(run_id)} || ':gap:' || gap_type || ':plant:' || plant_id || ':generator:' || coalesce(nullif(generator_id, ''), 'none'),
    scope_audit_run_id,
    policy_result_run_id,
    {text_null("exception_review_run_id")},
    gap_type,
    plant_id,
    {text_null("eia_plant_code")},
    {text_null("generator_id")},
    {text_null("utility_id")},
    {text_null("utility_name")},
    {text_null("plant_name")},
    {text_null("state")},
    {text_null("county")},
    {text_null("technology")},
    {text_null("prime_mover")},
    {nullif_cast("nameplate_capacity_mw", "numeric")},
    {nullif_cast("summer_capacity_mw", "numeric")},
    {nullif_cast("winter_capacity_mw", "numeric")},
    {text_null("status")},
    recommended_next_action,
    {text_null("notes")}
from tmp_scope_gap;

commit;
"""


def render_report(
    path: Path,
    run_id: str,
    code_commit: str,
    policy_result_run_id: str,
    exception_review_run_id: str,
    summary_rows: list[dict[str, object]],
    gap_rows: list[dict[str, object]],
    summary_csv: Path,
    gap_csv: Path,
) -> None:
    metrics = {str(row["metric"]): str(row["value"]) for row in summary_rows}
    lines = [
        "# Plant ECWT Scope Readiness Audit",
        "",
        f"Generated UTC: {utc_now().isoformat(timespec='seconds')}",
        "",
        "## Run",
        "",
        f"- Scope audit run ID: `{run_id}`",
        f"- Policy result run ID: `{policy_result_run_id}`",
        f"- Exception review run ID: `{exception_review_run_id}`",
        f"- Code commit: `{code_commit}`",
        f"- Summary CSV: `{summary_csv.name}`",
        f"- Scope gap CSV: `{gap_csv.name}`",
        "",
        "## Scope Counts",
        "",
        "| Metric | Value | Notes |",
        "| --- | ---: | --- |",
    ]
    for row in summary_rows:
        lines.append(f"| `{row['metric']}` | {row['value']} | {row['notes']} |")
    lines.extend(
        [
            "",
            "## First-Operable Gap Rows",
            "",
            "| EIA Plant | Generator | Utility | Status | MW | Action |",
            "| --- | --- | --- | --- | ---: | --- |",
        ]
    )
    for row in gap_rows:
        lines.append(
            "| "
            f"`{row['eia_plant_code']}` | "
            f"`{row['generator_id']}` | "
            f"{row['utility_name']} | "
            f"`{row['status']}` | "
            f"{row['nameplate_capacity_mw']} | "
            f"{row['recommended_next_action']} |"
        )
    if not gap_rows:
        lines.append("|  |  |  |  |  | No first-operable generator IDs are missing from asset.plant. |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- The all-plants policy result covers every row in `asset.plant`.",
            "- The generator-derived first-operable denominator has one extra plant ID that is absent from `asset.plant` and therefore absent from station matching and ECWT policy results.",
            "- The 28 geocode-required exception-review rows are construction-only (`CN`) asset rows with no first-operable generators; they should not be confused with active ECWT weather blockers.",
            "- After separating that missing asset row, the current first-operable policy state is 13,355 publication candidates and 15 coverage-threshold blockers.",
            "",
            "## Key Numbers",
            "",
            f"- Asset-backed first-operable policy rows: `{metrics.get('policy result first-operable rows', '')}`",
            f"- First-operable publication candidates: `{metrics.get('first-operable publication candidates', '')}`",
            f"- First-operable blocked rows: `{metrics.get('first-operable blocked rows', '')}`",
            f"- First-operable generator IDs missing asset rows: `{metrics.get('generator-derived first-operable ids missing asset.plant rows', '')}`",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--psql", type=Path, default=PSQL)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5436)
    parser.add_argument("--dbname", default="eop012")
    parser.add_argument("--user")
    parser.add_argument("--policy-result-run-id")
    parser.add_argument("--exception-review-run-id")
    args = parser.parse_args()

    if not args.psql.exists():
        raise FileNotFoundError(args.psql)

    started_at = utc_now().isoformat()
    docs_dir = args.project_root / "docs"
    policy_result_run_id = args.policy_result_run_id or latest_run_id(
        args.psql, args.host, args.port, args.dbname, args.user, "plant_ecwt_policy_result_"
    )
    exception_review_run_id = args.exception_review_run_id or latest_run_id(
        args.psql, args.host, args.port, args.dbname, args.user, "plant_ecwt_exception_review_"
    )
    run_id = f"plant_ecwt_scope_readiness_{utc_now().strftime('%Y%m%dT%H%M%SZ')}"
    code_commit = git_commit_label(args.project_root)

    metrics = summary_metrics(
        args.psql,
        args.host,
        args.port,
        args.dbname,
        args.user,
        policy_result_run_id,
        exception_review_run_id,
    )
    summary_rows = build_summary_rows(run_id, metrics)
    gap_rows = missing_operable_asset_rows(
        args.psql,
        args.host,
        args.port,
        args.dbname,
        args.user,
        run_id,
        policy_result_run_id,
        exception_review_run_id,
    )

    summary_csv = docs_dir / f"{run_id}_summary.csv"
    gap_csv = docs_dir / f"{run_id}_scope_gaps.csv"
    report_path = docs_dir / f"{run_id}_report.md"
    write_csv(summary_csv, SUMMARY_FIELDS, summary_rows)
    write_csv(gap_csv, GAP_FIELDS, gap_rows)

    gap_source = source_row(gap_csv, "eop012_plant_ecwt_scope_gap", run_id)
    params = {
        "policy_result_run_id": policy_result_run_id,
        "exception_review_run_id": exception_review_run_id,
        "first_operable_statuses": list(FIRST_OPERABLE_STATUSES),
        "summary_csv": str(summary_csv),
        "gap_csv": str(gap_csv),
        "gap_sha256": gap_source["sha256"],
        "gap_row_count": len(gap_rows),
    }
    sql = build_load_sql(run_id, code_commit, started_at, params, gap_csv, gap_source)
    run(psql_cmd(args.psql, args.host, args.port, args.dbname, args.user), input_text=sql)
    render_report(
        report_path,
        run_id,
        code_commit,
        policy_result_run_id,
        exception_review_run_id,
        summary_rows,
        gap_rows,
        summary_csv,
        gap_csv,
    )
    print(
        json.dumps(
            OrderedDict(
                [
                    ("run_id", run_id),
                    ("policy_result_run_id", policy_result_run_id),
                    ("exception_review_run_id", exception_review_run_id),
                    ("summary_rows", len(summary_rows)),
                    ("gap_rows", len(gap_rows)),
                    ("summary_csv", str(summary_csv)),
                    ("gap_csv", str(gap_csv)),
                    ("report_path", str(report_path)),
                    ("metrics", metrics),
                ]
            ),
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
