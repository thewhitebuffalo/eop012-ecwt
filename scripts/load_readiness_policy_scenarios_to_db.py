#!/usr/bin/env python3
"""Load first-operable readiness policy scenario artifacts into Postgres."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path

from eop012_config import PROJECT_ROOT, PSQL


METHODOLOGY_VERSION = "eop012-ecwt-method-v0.1.0"

MATRIX_FIELDS = [
    "scenario_id",
    "scenario_label",
    "policy_suitability",
    "total_first_operable_scope",
    "current_fixed_candidates_retained",
    "fixed_period_blockers_promoted",
    "total_scenario_candidates",
    "remaining_blocked",
    "promoted_candidate_overfill_rows",
    "promoted_candidate_coverage_ratio_gt_1_rows",
    "source",
    "notes",
]

CANDIDATE_FIELDS = [
    "scenario_id",
    "scenario_label",
    "policy_suitability",
    "candidate_source",
    "plant_id",
    "eia_plant_code",
    "plant_name",
    "plant_state",
    "plant_county",
    "sector_name",
    "first_scope_generator_count",
    "first_scope_nameplate_mw",
    "selected_station_id",
    "selected_station_name",
    "selected_station_state",
    "selected_station_country",
    "selected_station_distance_km",
    "selected_station_rank_order",
    "ecwt_f",
    "valid_hour_count",
    "expected_hour_count",
    "coverage_ratio",
    "overfilled_hour_count",
    "fixed_coverage_ratio",
    "fixed_loaded_station_year_count",
    "source_blocker_class",
    "source_active_window_class",
    "source_normalized_active_window_class",
    "notes",
]


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
    return list(csv.DictReader(result.stdout.splitlines()))


def git_commit_label(project_root: Path) -> str:
    try:
        return run(["git", "-C", str(project_root), "rev-parse", "HEAD"]).stdout.strip()
    except Exception:
        return "UNCOMMITTED_WORKTREE"


def latest_file(docs_dir: Path, pattern: str) -> Path:
    matches = sorted(docs_dir.glob(pattern))
    if not matches:
        raise FileNotFoundError(f"No files matched {docs_dir / pattern}")
    return matches[-1]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def csv_row_count(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def verify_headers(path: Path, expected: list[str]) -> None:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        header = next(reader)
    if header != expected:
        raise ValueError(f"Unexpected header in {path}: {header}")


def source_row(path: Path, family: str, source_release: str) -> dict[str, object]:
    digest = sha256_file(path)
    return {
        "source_file_id": f"{family}:{digest}",
        "source_family": family,
        "source_url": None,
        "local_path": str(path),
        "file_name": path.name,
        "size_bytes": path.stat().st_size,
        "sha256": digest,
        "retrieved_at_utc": datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat(),
        "source_year": None,
        "source_release": source_release,
        "notes": "Generated EOP012 policy scenario artifact loaded into Postgres.",
    }


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


def nullif_cast(field: str, cast_type: str) -> str:
    return f"nullif({qident(field)}, '')::{cast_type}"


def build_load_sql(
    run_id: str,
    code_commit: str,
    matrix_csv: Path,
    candidates_csv: Path,
    matrix_source: dict[str, object],
    candidates_source: dict[str, object],
    started_at: str,
    params: dict[str, object],
) -> str:
    return f"""
\\set ON_ERROR_STOP on
begin;

create table if not exists calc.readiness_policy_scenario (
    scenario_run_id text not null references audit.calculation_run(calculation_run_id),
    scenario_id text not null,
    scenario_label text not null,
    policy_suitability text not null,
    total_first_operable_scope bigint not null,
    current_fixed_candidates_retained bigint not null,
    fixed_period_blockers_promoted bigint not null,
    total_scenario_candidates bigint not null,
    remaining_blocked bigint not null,
    promoted_candidate_overfill_rows bigint not null,
    promoted_candidate_coverage_ratio_gt_1_rows bigint not null,
    source text,
    notes text,
    created_at_utc timestamptz not null default now(),
    primary key (scenario_run_id, scenario_id)
);

create table if not exists calc.readiness_policy_scenario_candidate (
    scenario_candidate_id text primary key,
    scenario_run_id text not null references audit.calculation_run(calculation_run_id),
    scenario_id text not null,
    scenario_label text not null,
    policy_suitability text not null,
    candidate_source text not null,
    plant_id text not null references asset.plant(plant_id),
    eia_plant_code text,
    plant_name text,
    plant_state text,
    plant_county text,
    sector_name text,
    first_scope_generator_count bigint,
    first_scope_nameplate_mw numeric,
    selected_station_id text references weather.station(station_id),
    selected_station_name text,
    selected_station_state text,
    selected_station_country text,
    selected_station_distance_km numeric,
    selected_station_rank_order integer,
    ecwt_f numeric,
    valid_hour_count bigint,
    expected_hour_count bigint,
    coverage_ratio numeric,
    overfilled_hour_count bigint,
    fixed_coverage_ratio numeric,
    fixed_loaded_station_year_count integer,
    source_blocker_class text,
    source_active_window_class text,
    source_normalized_active_window_class text,
    notes text,
    created_at_utc timestamptz not null default now(),
    unique (scenario_run_id, scenario_id, plant_id)
);

create index if not exists ix_readiness_policy_scenario_candidate_run_scenario
    on calc.readiness_policy_scenario_candidate (scenario_run_id, scenario_id);
create index if not exists ix_readiness_policy_scenario_candidate_station
    on calc.readiness_policy_scenario_candidate (selected_station_id);
create index if not exists ix_readiness_policy_scenario_candidate_state
    on calc.readiness_policy_scenario_candidate (plant_state);

insert into audit.source_file (
    source_file_id, source_family, source_url, local_path, file_name, size_bytes,
    sha256, retrieved_at_utc, source_year, source_release, notes
) values
(
    {sql_literal(matrix_source["source_file_id"])},
    {sql_literal(matrix_source["source_family"])},
    null,
    {sql_literal(matrix_source["local_path"])},
    {sql_literal(matrix_source["file_name"])},
    {matrix_source["size_bytes"]},
    {sql_literal(matrix_source["sha256"])},
    {sql_literal(matrix_source["retrieved_at_utc"])},
    null,
    {sql_literal(matrix_source["source_release"])},
    {sql_literal(matrix_source["notes"])}
),
(
    {sql_literal(candidates_source["source_file_id"])},
    {sql_literal(candidates_source["source_family"])},
    null,
    {sql_literal(candidates_source["local_path"])},
    {sql_literal(candidates_source["file_name"])},
    {candidates_source["size_bytes"]},
    {sql_literal(candidates_source["sha256"])},
    {sql_literal(candidates_source["retrieved_at_utc"])},
    null,
    {sql_literal(candidates_source["source_release"])},
    {sql_literal(candidates_source["notes"])}
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
    'Loaded first-operable readiness policy scenario artifacts into calc tables.'
)
on conflict (calculation_run_id) do update set
    run_finished_at_utc = excluded.run_finished_at_utc,
    run_status = excluded.run_status,
    parameters_json = excluded.parameters_json,
    notes = excluded.notes;

{temp_table_sql("tmp_policy_scenario_matrix", MATRIX_FIELDS)}
{copy_sql("tmp_policy_scenario_matrix", MATRIX_FIELDS, matrix_csv)}

{temp_table_sql("tmp_policy_scenario_candidate", CANDIDATE_FIELDS)}
{copy_sql("tmp_policy_scenario_candidate", CANDIDATE_FIELDS, candidates_csv)}

delete from calc.readiness_policy_scenario_candidate
where scenario_run_id = {sql_literal(run_id)};

delete from calc.readiness_policy_scenario
where scenario_run_id = {sql_literal(run_id)};

insert into calc.readiness_policy_scenario (
    scenario_run_id,
    scenario_id,
    scenario_label,
    policy_suitability,
    total_first_operable_scope,
    current_fixed_candidates_retained,
    fixed_period_blockers_promoted,
    total_scenario_candidates,
    remaining_blocked,
    promoted_candidate_overfill_rows,
    promoted_candidate_coverage_ratio_gt_1_rows,
    source,
    notes
)
select
    {sql_literal(run_id)},
    scenario_id,
    scenario_label,
    policy_suitability,
    {nullif_cast("total_first_operable_scope", "bigint")},
    {nullif_cast("current_fixed_candidates_retained", "bigint")},
    {nullif_cast("fixed_period_blockers_promoted", "bigint")},
    {nullif_cast("total_scenario_candidates", "bigint")},
    {nullif_cast("remaining_blocked", "bigint")},
    {nullif_cast("promoted_candidate_overfill_rows", "bigint")},
    {nullif_cast("promoted_candidate_coverage_ratio_gt_1_rows", "bigint")},
    source,
    notes
from tmp_policy_scenario_matrix;

insert into calc.readiness_policy_scenario_candidate (
    scenario_candidate_id,
    scenario_run_id,
    scenario_id,
    scenario_label,
    policy_suitability,
    candidate_source,
    plant_id,
    eia_plant_code,
    plant_name,
    plant_state,
    plant_county,
    sector_name,
    first_scope_generator_count,
    first_scope_nameplate_mw,
    selected_station_id,
    selected_station_name,
    selected_station_state,
    selected_station_country,
    selected_station_distance_km,
    selected_station_rank_order,
    ecwt_f,
    valid_hour_count,
    expected_hour_count,
    coverage_ratio,
    overfilled_hour_count,
    fixed_coverage_ratio,
    fixed_loaded_station_year_count,
    source_blocker_class,
    source_active_window_class,
    source_normalized_active_window_class,
    notes
)
select
    {sql_literal(run_id)} || ':' || scenario_id || ':plant:' || plant_id,
    {sql_literal(run_id)},
    scenario_id,
    scenario_label,
    policy_suitability,
    candidate_source,
    plant_id,
    nullif(eia_plant_code, ''),
    nullif(plant_name, ''),
    nullif(plant_state, ''),
    nullif(plant_county, ''),
    nullif(sector_name, ''),
    nullif(first_scope_generator_count, '')::bigint,
    nullif(first_scope_nameplate_mw, '')::numeric,
    nullif(nullif(selected_station_id, ''), '\\N'),
    nullif(nullif(selected_station_name, ''), '\\N'),
    nullif(nullif(selected_station_state, ''), '\\N'),
    nullif(nullif(selected_station_country, ''), '\\N'),
    nullif(selected_station_distance_km, '')::numeric,
    nullif(selected_station_rank_order, '')::integer,
    nullif(ecwt_f, '')::numeric,
    nullif(valid_hour_count, '')::bigint,
    nullif(expected_hour_count, '')::bigint,
    nullif(coverage_ratio, '')::numeric,
    coalesce(nullif(overfilled_hour_count, '')::bigint, 0),
    nullif(fixed_coverage_ratio, '')::numeric,
    nullif(fixed_loaded_station_year_count, '')::integer,
    nullif(source_blocker_class, ''),
    nullif(source_active_window_class, ''),
    nullif(source_normalized_active_window_class, ''),
    notes
from tmp_policy_scenario_candidate;

commit;
"""


def render_report(
    path: Path,
    run_id: str,
    code_commit: str,
    matrix_csv: Path,
    candidates_csv: Path,
    matrix_source: dict[str, object],
    candidates_source: dict[str, object],
    matrix_rows: list[dict[str, str]],
    candidate_summary_rows: list[dict[str, str]],
    db_counts: OrderedDict[str, str],
    host: str,
    port: int,
    dbname: str,
) -> None:
    lines = [
        "# Readiness Policy Scenario DB Load Report",
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
        f"- Matrix CSV: `{matrix_csv.name}`",
        f"- Matrix SHA-256: `{matrix_source['sha256']}`",
        f"- Candidate CSV: `{candidates_csv.name}`",
        f"- Candidate SHA-256: `{candidates_source['sha256']}`",
        "",
        "## Loaded DB Counts",
        "",
        "| Relation or check | Rows |",
        "| --- | ---: |",
    ]
    for label, count in db_counts.items():
        lines.append(f"| `{label}` | {count} |")
    lines.extend(["", "## Scenario Matrix", "", "| Scenario | Candidates | Promoted | Blocked | Overfill |", "| --- | ---: | ---: | ---: | ---: |"])
    for row in matrix_rows:
        lines.append(
            "| "
            f"`{row['scenario_id']}` | "
            f"{row['total_scenario_candidates']} | "
            f"{row['fixed_period_blockers_promoted']} | "
            f"{row['remaining_blocked']} | "
            f"{row['promoted_candidate_overfill_rows']} |"
        )
    lines.extend(["", "## Candidate Rows By Scenario", "", "| Scenario | Rows |", "| --- | ---: |"])
    for row in candidate_summary_rows:
        lines.append(f"| `{row['scenario_id']}` | {row['rows']} |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- The scenario artifacts are now queryable in `calc.readiness_policy_scenario` and `calc.readiness_policy_scenario_candidate`.",
            "- This load does not replace `calc.plant_ecwt_readiness`; the conservative fixed-period readiness run remains intact.",
            "- Source CSV hashes are recorded in `audit.source_file` and in the calculation-run parameters.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--psql", type=Path, default=PSQL)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5436)
    parser.add_argument("--dbname", default="eop012")
    parser.add_argument("--user")
    parser.add_argument("--matrix-csv", type=Path)
    parser.add_argument("--candidates-csv", type=Path)
    args = parser.parse_args()

    docs_dir = args.project_root / "docs"
    matrix_csv = args.matrix_csv or latest_file(docs_dir, "readiness_policy_scenarios_first_operable_*_matrix.csv")
    candidates_csv = args.candidates_csv or latest_file(docs_dir, "readiness_policy_scenarios_first_operable_*_candidates.csv")
    verify_headers(matrix_csv, MATRIX_FIELDS)
    verify_headers(candidates_csv, CANDIDATE_FIELDS)
    run_id = f"readiness_policy_scenarios_db_load_{utc_now().strftime('%Y%m%dT%H%M%SZ')}"
    code_commit = git_commit_label(args.project_root)
    started_at = utc_now().isoformat(timespec="seconds")
    matrix_source = source_row(matrix_csv, "eop012_readiness_policy_scenario_matrix", run_id)
    candidates_source = source_row(candidates_csv, "eop012_readiness_policy_scenario_candidates", run_id)
    params = {
        "matrix_csv": str(matrix_csv),
        "matrix_source_file_id": matrix_source["source_file_id"],
        "matrix_sha256": matrix_source["sha256"],
        "matrix_rows": csv_row_count(matrix_csv),
        "candidates_csv": str(candidates_csv),
        "candidates_source_file_id": candidates_source["source_file_id"],
        "candidates_sha256": candidates_source["sha256"],
        "candidate_rows": csv_row_count(candidates_csv),
        "target_tables": ["calc.readiness_policy_scenario", "calc.readiness_policy_scenario_candidate"],
    }
    run(
        psql_cmd(args.psql, args.host, args.port, args.dbname, args.user),
        input_text=build_load_sql(
            run_id,
            code_commit,
            matrix_csv,
            candidates_csv,
            matrix_source,
            candidates_source,
            started_at,
            params,
        ),
    )

    db_counts = OrderedDict(
        [
            (
                "calc.readiness_policy_scenario",
                psql_scalar(
                    args.psql,
                    args.host,
                    args.port,
                    args.dbname,
                    args.user,
                    f"select count(*) from calc.readiness_policy_scenario where scenario_run_id = {sql_literal(run_id)};",
                ),
            ),
            (
                "calc.readiness_policy_scenario_candidate",
                psql_scalar(
                    args.psql,
                    args.host,
                    args.port,
                    args.dbname,
                    args.user,
                    f"select count(*) from calc.readiness_policy_scenario_candidate where scenario_run_id = {sql_literal(run_id)};",
                ),
            ),
            (
                "audit.source_file rows",
                psql_scalar(
                    args.psql,
                    args.host,
                    args.port,
                    args.dbname,
                    args.user,
                    "select count(*) from audit.source_file "
                    f"where source_file_id in ({sql_literal(matrix_source['source_file_id'])}, {sql_literal(candidates_source['source_file_id'])});",
                ),
            ),
        ]
    )
    matrix_rows = psql_csv_query(
        args.psql,
        args.host,
        args.port,
        args.dbname,
        args.user,
        f"""
        select
            scenario_id,
            total_scenario_candidates::text as total_scenario_candidates,
            fixed_period_blockers_promoted::text as fixed_period_blockers_promoted,
            remaining_blocked::text as remaining_blocked,
            promoted_candidate_overfill_rows::text as promoted_candidate_overfill_rows
        from calc.readiness_policy_scenario
        where scenario_run_id = {sql_literal(run_id)}
        order by scenario_id
        """,
    )
    candidate_summary = psql_csv_query(
        args.psql,
        args.host,
        args.port,
        args.dbname,
        args.user,
        f"""
        select scenario_id, count(*)::text as rows
        from calc.readiness_policy_scenario_candidate
        where scenario_run_id = {sql_literal(run_id)}
        group by scenario_id
        order by scenario_id
        """,
    )
    report_path = docs_dir / f"{run_id}_report.md"
    render_report(
        report_path,
        run_id,
        code_commit,
        matrix_csv,
        candidates_csv,
        matrix_source,
        candidates_source,
        matrix_rows,
        candidate_summary,
        db_counts,
        args.host,
        args.port,
        args.dbname,
    )
    print(
        json.dumps(
            OrderedDict(
                [
                    ("run_id", run_id),
                    ("matrix_csv", str(matrix_csv)),
                    ("candidates_csv", str(candidates_csv)),
                    ("db_counts", db_counts),
                    ("report_path", str(report_path)),
                ]
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
