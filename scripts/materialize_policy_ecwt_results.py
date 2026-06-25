#!/usr/bin/env python3
"""Materialize a policy scenario into one plant-level ECWT result set."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from collections import Counter, OrderedDict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from eop012_config import PROJECT_ROOT, PSQL


METHODOLOGY_VERSION = "eop012-ecwt-method-v0.1.0"
DEFAULT_POLICY_ID = "normalized_active_window_loaded_year"

RESULT_FIELDS = [
    "policy_result_run_id",
    "plant_scope",
    "policy_id",
    "policy_label",
    "policy_suitability",
    "source_scenario_run_id",
    "source_denominator_run_id",
    "plant_id",
    "eia_plant_code",
    "plant_name",
    "plant_state",
    "plant_county",
    "sector_name",
    "first_scope_generator_count",
    "first_scope_nameplate_mw",
    "readiness_status",
    "reason_code",
    "candidate_source",
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


def git_commit_label(project_root: Path) -> str:
    try:
        head = run(["git", "-C", str(project_root), "rev-parse", "HEAD"]).stdout.strip()
        dirty = run(["git", "-C", str(project_root), "status", "--porcelain"]).stdout.strip()
        return f"{head}-dirty" if dirty else head
    except Exception:
        return "UNKNOWN_GIT_COMMIT"


def latest_file(docs_dir: Path, pattern: str) -> Path:
    matches = sorted(docs_dir.glob(pattern))
    if not matches:
        raise FileNotFoundError(f"No files matched {docs_dir / pattern}")
    return matches[-1]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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
        "notes": "Generated EOP012 policy materialization source artifact.",
    }


def run_id_from_name(path: Path, suffix: str) -> str:
    name = path.name
    if not name.endswith(suffix):
        return path.stem
    return name[: -len(suffix)]


def blocker_reason(row: dict[str, str]) -> str:
    blocker_class = row.get("normalized_active_window_class", "")
    if blocker_class == "no_station_candidates":
        return "no_station_candidates"
    if blocker_class == "no_candidate_with_provisional_station_ecwt":
        return "no_candidate_with_provisional_station_ecwt"
    if blocker_class == "still_fails_normalized_active_window_coverage":
        return "normalized_active_window_coverage_below_threshold"
    return "not_promoted_under_policy"


def candidate_reason(row: dict[str, str]) -> str:
    source = row.get("candidate_source", "")
    if source == "current_fixed_period_publication_candidate":
        return "passes_current_fixed_period_gate"
    return "passes_normalized_active_window_policy"


def candidate_result_row(
    run_id: str,
    plant_scope: str,
    policy_id: str,
    scenario_run_id: str,
    denominator_run_id: str,
    row: dict[str, str],
) -> dict[str, object]:
    return {
        "policy_result_run_id": run_id,
        "plant_scope": plant_scope,
        "policy_id": policy_id,
        "policy_label": row.get("scenario_label", ""),
        "policy_suitability": row.get("policy_suitability", ""),
        "source_scenario_run_id": scenario_run_id,
        "source_denominator_run_id": denominator_run_id,
        "plant_id": row.get("plant_id", ""),
        "eia_plant_code": row.get("eia_plant_code", ""),
        "plant_name": row.get("plant_name", ""),
        "plant_state": row.get("plant_state", ""),
        "plant_county": row.get("plant_county", ""),
        "sector_name": row.get("sector_name", ""),
        "first_scope_generator_count": row.get("first_scope_generator_count", ""),
        "first_scope_nameplate_mw": row.get("first_scope_nameplate_mw", ""),
        "readiness_status": "publication_candidate",
        "reason_code": candidate_reason(row),
        "candidate_source": row.get("candidate_source", ""),
        "selected_station_id": row.get("selected_station_id", ""),
        "selected_station_name": row.get("selected_station_name", ""),
        "selected_station_state": row.get("selected_station_state", ""),
        "selected_station_country": row.get("selected_station_country", ""),
        "selected_station_distance_km": row.get("selected_station_distance_km", ""),
        "selected_station_rank_order": row.get("selected_station_rank_order", ""),
        "ecwt_f": row.get("ecwt_f", ""),
        "valid_hour_count": row.get("valid_hour_count", ""),
        "expected_hour_count": row.get("expected_hour_count", ""),
        "coverage_ratio": row.get("coverage_ratio", ""),
        "overfilled_hour_count": row.get("overfilled_hour_count", ""),
        "fixed_coverage_ratio": row.get("fixed_coverage_ratio", ""),
        "fixed_loaded_station_year_count": row.get("fixed_loaded_station_year_count", ""),
        "source_blocker_class": row.get("source_blocker_class", ""),
        "source_active_window_class": row.get("source_active_window_class", ""),
        "source_normalized_active_window_class": row.get("source_normalized_active_window_class", ""),
        "notes": row.get("notes", ""),
    }


def blocker_result_row(
    run_id: str,
    plant_scope: str,
    policy_id: str,
    scenario_run_id: str,
    denominator_run_id: str,
    row: dict[str, str],
) -> dict[str, object]:
    return {
        "policy_result_run_id": run_id,
        "plant_scope": plant_scope,
        "policy_id": policy_id,
        "policy_label": "Normalized active-window loaded-year gate",
        "policy_suitability": "candidate_policy_option",
        "source_scenario_run_id": scenario_run_id,
        "source_denominator_run_id": denominator_run_id,
        "plant_id": row.get("plant_id", ""),
        "eia_plant_code": row.get("eia_plant_code", ""),
        "plant_name": row.get("plant_name", ""),
        "plant_state": row.get("plant_state", ""),
        "plant_county": row.get("plant_county", ""),
        "sector_name": row.get("sector_name", ""),
        "first_scope_generator_count": row.get("first_operable_generator_count", ""),
        "first_scope_nameplate_mw": row.get("first_operable_nameplate_mw", ""),
        "readiness_status": "blocked",
        "reason_code": blocker_reason(row),
        "candidate_source": "unpromoted_fixed_period_blocker",
        "selected_station_id": row.get("best_normalized_active_station_id", ""),
        "selected_station_name": row.get("best_normalized_active_station_name", ""),
        "selected_station_state": row.get("best_normalized_active_station_state", ""),
        "selected_station_country": row.get("best_normalized_active_station_country", ""),
        "selected_station_distance_km": row.get("best_normalized_active_distance_km", ""),
        "selected_station_rank_order": row.get("best_normalized_active_rank_order", ""),
        "ecwt_f": row.get("best_normalized_active_station_ecwt_f", ""),
        "valid_hour_count": row.get("best_normalized_active_normalized_active_valid_djf_hours", ""),
        "expected_hour_count": row.get("best_normalized_active_normalized_active_expected_djf_hours", ""),
        "coverage_ratio": row.get("best_normalized_active_normalized_active_coverage_ratio", ""),
        "overfilled_hour_count": row.get("best_normalized_active_normalized_active_overfilled_hour_count", ""),
        "fixed_coverage_ratio": row.get("best_normalized_active_fixed_coverage_ratio", ""),
        "fixed_loaded_station_year_count": row.get("best_normalized_active_loaded_station_year_count", ""),
        "source_blocker_class": row.get("current_blocker_class", ""),
        "source_active_window_class": row.get("active_window_class", ""),
        "source_normalized_active_window_class": row.get("normalized_active_window_class", ""),
        "notes": "Blocked under normalized active-window loaded-year policy materialization.",
    }


def build_result_rows(
    run_id: str,
    plant_scope: str,
    policy_id: str,
    scenario_rows: list[dict[str, str]],
    denominator_rows: list[dict[str, str]],
    scenario_run_id: str,
    denominator_run_id: str,
) -> list[dict[str, object]]:
    selected = [row for row in scenario_rows if row.get("scenario_id") == policy_id]
    if not selected:
        raise RuntimeError(f"No scenario candidate rows found for policy {policy_id}.")
    selected_counts = Counter(row.get("plant_id", "") for row in selected)
    duplicate_selected = sorted(plant_id for plant_id, count in selected_counts.items() if plant_id and count > 1)
    if duplicate_selected:
        sample = ", ".join(duplicate_selected[:10])
        raise RuntimeError(f"Scenario policy {policy_id} has duplicate plant rows: {sample}")
    denominator_counts = Counter(row.get("plant_id", "") for row in denominator_rows)
    duplicate_denominator = sorted(plant_id for plant_id, count in denominator_counts.items() if plant_id and count > 1)
    if duplicate_denominator:
        sample = ", ".join(duplicate_denominator[:10])
        raise RuntimeError(f"Denominator diagnostic has duplicate plant rows: {sample}")
    result_rows = [
        candidate_result_row(run_id, plant_scope, policy_id, scenario_run_id, denominator_run_id, row)
        for row in selected
    ]
    candidate_ids = {str(row["plant_id"]) for row in result_rows}
    blocker_rows = [
        row
        for row in denominator_rows
        if row.get("plant_id") not in candidate_ids
    ]
    result_rows.extend(
        blocker_result_row(run_id, plant_scope, policy_id, scenario_run_id, denominator_run_id, row)
        for row in blocker_rows
    )
    result_rows.sort(key=lambda row: (str(row.get("plant_state", "")), int(str(row.get("eia_plant_code") or "999999999")), str(row.get("plant_name", ""))))
    return result_rows


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
    return f"nullif(nullif({qident(field)}, ''), '\\N')::{cast_type}"


def text_null(field: str) -> str:
    return f"nullif(nullif({qident(field)}, ''), '\\N')"


def build_load_sql(
    run_id: str,
    code_commit: str,
    result_csv: Path,
    scenario_source: dict[str, object],
    denominator_source: dict[str, object],
    result_source: dict[str, object],
    started_at: str,
    params: dict[str, object],
) -> str:
    return f"""
\\set ON_ERROR_STOP on
begin;

create table if not exists calc.plant_ecwt_policy_result (
    policy_result_id text primary key,
    policy_result_run_id text not null references audit.calculation_run(calculation_run_id),
    plant_scope text not null,
    policy_id text not null,
    policy_label text,
    policy_suitability text,
    source_scenario_run_id text,
    source_denominator_run_id text,
    plant_id text not null references asset.plant(plant_id),
    eia_plant_code text,
    plant_name text,
    plant_state text,
    plant_county text,
    sector_name text,
    first_scope_generator_count bigint,
    first_scope_nameplate_mw numeric,
    readiness_status text not null,
    reason_code text not null,
    candidate_source text,
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
    unique (policy_result_run_id, plant_id)
);
create index if not exists ix_plant_ecwt_policy_result_run_status
    on calc.plant_ecwt_policy_result (policy_result_run_id, readiness_status);
create index if not exists ix_plant_ecwt_policy_result_station
    on calc.plant_ecwt_policy_result (policy_result_run_id, selected_station_id);
create index if not exists ix_plant_ecwt_policy_result_state
    on calc.plant_ecwt_policy_result (policy_result_run_id, plant_state);

insert into audit.source_file (
    source_file_id, source_family, source_url, local_path, file_name, size_bytes,
    sha256, retrieved_at_utc, source_year, source_release, notes
) values
(
    {sql_literal(scenario_source["source_file_id"])},
    {sql_literal(scenario_source["source_family"])},
    null,
    {sql_literal(scenario_source["local_path"])},
    {sql_literal(scenario_source["file_name"])},
    {scenario_source["size_bytes"]},
    {sql_literal(scenario_source["sha256"])},
    {sql_literal(scenario_source["retrieved_at_utc"])},
    null,
    {sql_literal(scenario_source["source_release"])},
    {sql_literal(scenario_source["notes"])}
),
(
    {sql_literal(denominator_source["source_file_id"])},
    {sql_literal(denominator_source["source_family"])},
    null,
    {sql_literal(denominator_source["local_path"])},
    {sql_literal(denominator_source["file_name"])},
    {denominator_source["size_bytes"]},
    {sql_literal(denominator_source["sha256"])},
    {sql_literal(denominator_source["retrieved_at_utc"])},
    null,
    {sql_literal(denominator_source["source_release"])},
    {sql_literal(denominator_source["notes"])}
),
(
    {sql_literal(result_source["source_file_id"])},
    {sql_literal(result_source["source_family"])},
    null,
    {sql_literal(result_source["local_path"])},
    {sql_literal(result_source["file_name"])},
    {result_source["size_bytes"]},
    {sql_literal(result_source["sha256"])},
    {sql_literal(result_source["retrieved_at_utc"])},
    null,
    {sql_literal(result_source["source_release"])},
    {sql_literal(result_source["notes"])}
)
on conflict (source_file_id) do update set
    local_path = excluded.local_path,
    size_bytes = excluded.size_bytes,
    sha256 = excluded.sha256,
    retrieved_at_utc = excluded.retrieved_at_utc,
    source_release = excluded.source_release,
    notes = excluded.notes;

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
    'Initial auditable methodology version for asset loading, station matching, raw file inventory, backfill planning, download attempts, coverage auditing, and ECWT calculation.'
)
on conflict (methodology_version) do update set notes = excluded.notes;

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
    'Materialized policy scenario into plant-level ECWT result rows.'
)
on conflict (calculation_run_id) do update set
    run_finished_at_utc = excluded.run_finished_at_utc,
    run_status = excluded.run_status,
    parameters_json = excluded.parameters_json,
    notes = excluded.notes;

{temp_table_sql("tmp_policy_result", RESULT_FIELDS)}
{copy_sql("tmp_policy_result", RESULT_FIELDS, result_csv)}

delete from calc.plant_ecwt_policy_result
where policy_result_run_id = {sql_literal(run_id)};

insert into calc.plant_ecwt_policy_result (
    policy_result_id,
    policy_result_run_id,
    plant_scope,
    policy_id,
    policy_label,
    policy_suitability,
    source_scenario_run_id,
    source_denominator_run_id,
    plant_id,
    eia_plant_code,
    plant_name,
    plant_state,
    plant_county,
    sector_name,
    first_scope_generator_count,
    first_scope_nameplate_mw,
    readiness_status,
    reason_code,
    candidate_source,
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
    {sql_literal(run_id)} || ':plant:' || plant_id,
    {sql_literal(run_id)},
    plant_scope,
    policy_id,
    {text_null("policy_label")},
    {text_null("policy_suitability")},
    {text_null("source_scenario_run_id")},
    {text_null("source_denominator_run_id")},
    plant_id,
    {text_null("eia_plant_code")},
    {text_null("plant_name")},
    {text_null("plant_state")},
    {text_null("plant_county")},
    {text_null("sector_name")},
    {nullif_cast("first_scope_generator_count", "bigint")},
    {nullif_cast("first_scope_nameplate_mw", "numeric")},
    readiness_status,
    reason_code,
    {text_null("candidate_source")},
    {text_null("selected_station_id")},
    {text_null("selected_station_name")},
    {text_null("selected_station_state")},
    {text_null("selected_station_country")},
    {nullif_cast("selected_station_distance_km", "numeric")},
    {nullif_cast("selected_station_rank_order", "integer")},
    {nullif_cast("ecwt_f", "numeric")},
    {nullif_cast("valid_hour_count", "bigint")},
    {nullif_cast("expected_hour_count", "bigint")},
    {nullif_cast("coverage_ratio", "numeric")},
    coalesce({nullif_cast("overfilled_hour_count", "bigint")}, 0),
    {nullif_cast("fixed_coverage_ratio", "numeric")},
    {nullif_cast("fixed_loaded_station_year_count", "integer")},
    {text_null("source_blocker_class")},
    {text_null("source_active_window_class")},
    {text_null("source_normalized_active_window_class")},
    {text_null("notes")}
from tmp_policy_result;

commit;
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
    plant_scope: str,
    policy_id: str,
    scenario_csv: Path,
    denominator_csv: Path,
    result_csv: Path,
    rows: list[dict[str, object]],
    db_counts: OrderedDict[str, str],
) -> None:
    status_counts = Counter(str(row["readiness_status"]) for row in rows)
    reason_counts = Counter(str(row["reason_code"]) for row in rows)
    state_counts = Counter(str(row.get("plant_state") or "(blank)") for row in rows if row["readiness_status"] == "publication_candidate")
    blocked_rows = [row for row in rows if row["readiness_status"] == "blocked"]
    lines = [
        "# Plant ECWT Policy Result Materialization",
        "",
        f"Generated UTC: {utc_now().isoformat(timespec='seconds')}",
        "",
        "## Run",
        "",
        f"- Policy result run ID: `{run_id}`",
        f"- Code commit: `{code_commit}`",
        f"- Plant scope: `{plant_scope}`",
        f"- Policy ID: `{policy_id}`",
        f"- Scenario candidate CSV: `{scenario_csv.name}`",
        f"- Denominator diagnostic CSV: `{denominator_csv.name}`",
        f"- Result CSV: `{result_csv.name}`",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| Plant rows materialized | {len(rows):,} |",
        f"| Publication candidates | {status_counts['publication_candidate']:,} |",
        f"| Blocked rows | {status_counts['blocked']:,} |",
        "",
        "## Loaded DB Counts",
        "",
        "| Check | Rows |",
        "| --- | ---: |",
    ]
    for key, value in db_counts.items():
        lines.append(f"| {key} | {value} |")
    lines.extend(["", "## Reason Counts", ""])
    render_table(
        lines,
        ["Reason", "Rows"],
        [{"reason": key, "rows": f"{value:,}"} for key, value in reason_counts.most_common()],
        ["reason", "rows"],
    )
    lines.extend(["", "## Candidate Rows By State", ""])
    render_table(
        lines,
        ["State", "Rows"],
        [{"state": key, "rows": f"{value:,}"} for key, value in state_counts.most_common(20)],
        ["state", "rows"],
    )
    lines.extend(["", "## Blocked Rows", ""])
    render_table(
        lines,
        ["Plant", "State", "Reason", "Best Station", "Coverage", "ECWT F"],
        blocked_rows[:50],
        ["plant_name", "plant_state", "reason_code", "selected_station_id", "coverage_ratio", "ecwt_f"],
    )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- This table materializes a policy scenario into one row per plant in scope.",
            "- `publication_candidate` rows are ECWT-ready under the selected policy, but still require final methodology approval before compliance publication.",
            "- `blocked` rows remain in the table so national-scope coverage is explicit and auditable.",
            "- The conservative fixed-period readiness table is not overwritten.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--psql", type=Path, default=PSQL)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5436)
    parser.add_argument("--dbname", default="eop012")
    parser.add_argument("--user")
    parser.add_argument("--plant-scope", choices=["all-plants", "first-operable"], default="all-plants")
    parser.add_argument("--policy-id", default=DEFAULT_POLICY_ID)
    parser.add_argument("--scenario-candidates-csv", type=Path)
    parser.add_argument("--denominator-csv", type=Path)
    args = parser.parse_args()

    started_at = utc_now().isoformat()
    docs_dir = args.project_root / "docs"
    scope_slug = args.plant_scope.replace("-", "_")
    scenario_csv = args.scenario_candidates_csv or latest_file(
        docs_dir, f"readiness_policy_scenarios_{scope_slug}_*_candidates.csv"
    )
    denominator_csv = args.denominator_csv or latest_file(
        docs_dir, f"fixed_period_denominator_diagnostic_{args.plant_scope}_*.csv"
    )
    scenario_run_id = run_id_from_name(scenario_csv, "_candidates.csv")
    denominator_run_id = run_id_from_name(denominator_csv, ".csv")
    scenario_rows = read_csv(scenario_csv)
    denominator_rows = read_csv(denominator_csv)

    run_id = f"plant_ecwt_policy_result_{scope_slug}_{args.policy_id}_{utc_now().strftime('%Y%m%dT%H%M%SZ')}"
    result_rows = build_result_rows(
        run_id,
        args.plant_scope,
        args.policy_id,
        scenario_rows,
        denominator_rows,
        scenario_run_id,
        denominator_run_id,
    )
    expected_scope_count = psql_scalar(
        args.psql,
        args.host,
        args.port,
        args.dbname,
        args.user,
        "select count(*) from asset.plant;" if args.plant_scope == "all-plants" else """
        select count(distinct ('eia860:2024:plant:' || eia_plant_code)::text)
        from asset.generator
        where status in ('OP','SB','OA','OS');
        """,
    )
    if str(len(result_rows)) != str(expected_scope_count):
        raise RuntimeError(
            f"Materialized row count {len(result_rows)} does not match expected {args.plant_scope} count {expected_scope_count}."
        )

    code_commit = git_commit_label(args.project_root)
    result_csv = docs_dir / f"{run_id}.csv"
    report_path = docs_dir / f"{run_id}_report.md"
    write_csv(result_csv, RESULT_FIELDS, result_rows)

    scenario_source = source_row(scenario_csv, "eop012_readiness_policy_scenario_candidates", run_id)
    denominator_source = source_row(denominator_csv, "eop012_fixed_period_denominator_diagnostic", run_id)
    result_source = source_row(result_csv, "eop012_plant_ecwt_policy_result", run_id)
    params = {
        "plant_scope": args.plant_scope,
        "policy_id": args.policy_id,
        "scenario_candidates_csv": str(scenario_csv),
        "denominator_csv": str(denominator_csv),
        "result_csv": str(result_csv),
        "scenario_sha256": scenario_source["sha256"],
        "denominator_sha256": denominator_source["sha256"],
        "result_sha256": result_source["sha256"],
        "row_count": len(result_rows),
    }
    sql = build_load_sql(
        run_id,
        code_commit,
        result_csv,
        scenario_source,
        denominator_source,
        result_source,
        started_at,
        params,
    )
    run(psql_cmd(args.psql, args.host, args.port, args.dbname, args.user), input_text=sql)
    db_counts = OrderedDict(
        [
            (
                "calc.plant_ecwt_policy_result",
                psql_scalar(
                    args.psql,
                    args.host,
                    args.port,
                    args.dbname,
                    args.user,
                    f"select count(*) from calc.plant_ecwt_policy_result where policy_result_run_id = {sql_literal(run_id)};",
                ),
            ),
            (
                "publication candidates",
                psql_scalar(
                    args.psql,
                    args.host,
                    args.port,
                    args.dbname,
                    args.user,
                    f"""
                    select count(*) from calc.plant_ecwt_policy_result
                    where policy_result_run_id = {sql_literal(run_id)}
                      and readiness_status = 'publication_candidate';
                    """,
                ),
            ),
            (
                "blocked rows",
                psql_scalar(
                    args.psql,
                    args.host,
                    args.port,
                    args.dbname,
                    args.user,
                    f"""
                    select count(*) from calc.plant_ecwt_policy_result
                    where policy_result_run_id = {sql_literal(run_id)}
                      and readiness_status = 'blocked';
                    """,
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
                    f"""
                    select count(*)
                    from audit.source_file
                    where source_file_id in (
                        {sql_literal(scenario_source['source_file_id'])},
                        {sql_literal(denominator_source['source_file_id'])},
                        {sql_literal(result_source['source_file_id'])}
                    );
                    """,
                ),
            ),
        ]
    )
    render_report(
        report_path,
        run_id,
        code_commit,
        args.plant_scope,
        args.policy_id,
        scenario_csv,
        denominator_csv,
        result_csv,
        result_rows,
        db_counts,
    )
    print(
        json.dumps(
            OrderedDict(
                [
                    ("run_id", run_id),
                    ("plant_scope", args.plant_scope),
                    ("policy_id", args.policy_id),
                    ("rows", len(result_rows)),
                    ("db_counts", db_counts),
                    ("result_csv", str(result_csv)),
                    ("report_path", str(report_path)),
                ]
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
