#!/usr/bin/env python3
"""Build ECWT readiness policy scenario comparison artifacts."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
from collections import Counter, OrderedDict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from eop012_config import PROJECT_ROOT


SCENARIOS = OrderedDict(
    [
        (
            "fixed_period_current_gate",
            {
                "label": "Current fixed-period publication gate",
                "source": "calc.plant_ecwt_readiness fixed-period publication candidates",
                "promotion_field": None,
                "candidate_prefix": None,
                "suitability": "current_conservative_gate",
                "notes": "Uses the current 2000-2025 fixed-period coverage and 20 loaded station-year gate.",
            },
        ),
        (
            "raw_active_window_metadata",
            {
                "label": "Raw station metadata active-window gate",
                "source": "denominator diagnostic raw active-window columns",
                "promotion_field": "active_window_eligible_candidate_count",
                "candidate_prefix": "best_active",
                "suitability": "diagnostic_only_overfill_present",
                "notes": "Uses NOAA station first/last observation metadata directly; retained as diagnostic because overfill exists.",
            },
        ),
        (
            "raw_active_window_metadata_plus_20_loaded_years",
            {
                "label": "Raw active-window gate plus 20 loaded fixed years",
                "source": "denominator diagnostic raw active-window plus absolute loaded-year columns",
                "promotion_field": "active_coverage_absolute_loaded_eligible_candidate_count",
                "candidate_prefix": "best_active",
                "suitability": "diagnostic_only_overfill_present",
                "notes": "Adds the current absolute 20 loaded station-year rule to the raw metadata active-window coverage screen.",
            },
        ),
        (
            "normalized_active_window_loaded_year",
            {
                "label": "Normalized active-window loaded-year gate",
                "source": "denominator diagnostic normalized active-window columns",
                "promotion_field": "normalized_active_window_eligible_candidate_count",
                "candidate_prefix": "best_normalized_active",
                "suitability": "diagnostic_only_not_publication_gate",
                "notes": "Expands station metadata windows to full loaded station-years; retained only as a diagnostic because it is not fixed-period publication coverage.",
            },
        ),
        (
            "normalized_active_window_loaded_year_plus_20_loaded_years",
            {
                "label": "Normalized active-window gate plus 20 loaded fixed years",
                "source": "denominator diagnostic normalized active-window plus absolute loaded-year columns",
                "promotion_field": "normalized_active_coverage_absolute_loaded_eligible_candidate_count",
                "candidate_prefix": "best_normalized_active",
                "suitability": "diagnostic_only_not_publication_gate",
                "notes": "Normalized active-window coverage screen with the current absolute 20 loaded station-year rule retained; not a publication gate.",
            },
        ),
    ]
)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(cmd, text=True, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise RuntimeError(
            "Command failed with exit code "
            f"{result.returncode}: {' '.join(cmd)}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    return result


def git_commit_label(project_root: Path) -> str:
    try:
        return run(["git", "-C", str(project_root), "rev-parse", "HEAD"]).stdout.strip()
    except Exception:
        return "UNCOMMITTED_WORKTREE"


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


def latest_file(docs_dir: Path, pattern: str) -> Path:
    matches = sorted(docs_dir.glob(pattern))
    if not matches:
        raise FileNotFoundError(f"No files matched {docs_dir / pattern}")
    return matches[-1]


def latest_strict_candidates_file(docs_dir: Path, plant_scope: str) -> Path:
    if plant_scope == "first-operable":
        return latest_file(docs_dir, "plant_ecwt_publication_candidates_first_operable_*.csv")
    matches = sorted(
        path
        for path in docs_dir.glob("plant_ecwt_publication_candidates_*.csv")
        if "first_operable" not in path.name
    )
    if not matches:
        raise FileNotFoundError("No all-plants strict publication candidate CSV found.")
    return matches[-1]


def latest_denominator_file(docs_dir: Path, plant_scope: str) -> Path:
    return latest_file(docs_dir, f"fixed_period_denominator_diagnostic_{plant_scope}_*.csv")


def validate_inputs(strict_rows: list[dict[str, str]], denominator_rows: list[dict[str, str]], plant_scope: str) -> None:
    strict_scopes = {row.get("plant_scope", "") for row in strict_rows}
    if strict_rows and strict_scopes != {plant_scope}:
        raise ValueError(f"Strict candidate CSV scope mismatch: expected {plant_scope}, found {sorted(strict_scopes)}")
    strict_ids = {row["plant_id"] for row in strict_rows}
    denominator_ids = {row["plant_id"] for row in denominator_rows}
    overlap = strict_ids & denominator_ids
    if overlap:
        sample = ", ".join(sorted(overlap)[:10])
        raise ValueError(
            "Strict candidates and denominator blockers overlap. "
            f"Check plant scope inputs before building scenarios. Sample: {sample}"
        )


def int_value(raw: object, default: int = 0) -> int:
    if raw in (None, "", r"\N"):
        return default
    return int(float(str(raw)))


def float_value(raw: object, default: float = 0.0) -> float:
    if raw in (None, "", r"\N"):
        return default
    return float(str(raw))


def scenario_promotes(row: dict[str, str], scenario: dict[str, str]) -> bool:
    field = scenario.get("promotion_field")
    return bool(field and int_value(row.get(field)) > 0)


def station_value(row: dict[str, str], prefix: str, suffix: str) -> str:
    return row.get(f"{prefix}_{suffix}", "")


def existing_candidate_row(row: dict[str, str], scenario_id: str, scenario: dict[str, str]) -> dict[str, object]:
    return {
        "scenario_id": scenario_id,
        "scenario_label": scenario["label"],
        "policy_suitability": scenario["suitability"],
        "candidate_source": "current_fixed_period_publication_candidate",
        "plant_id": row["plant_id"],
        "eia_plant_code": row["eia_plant_code"],
        "plant_name": row["plant_name"],
        "plant_state": row["plant_state"],
        "plant_county": row["plant_county"],
        "sector_name": row["sector_name"],
        "first_scope_generator_count": row["first_scope_generator_count"],
        "first_scope_nameplate_mw": row["first_scope_nameplate_mw"],
        "selected_station_id": row["selected_station_id"],
        "selected_station_name": row["selected_station_name"],
        "selected_station_state": row["selected_station_state"],
        "selected_station_country": row["selected_station_country"],
        "selected_station_distance_km": row.get("selected_station_distance_km", ""),
        "selected_station_rank_order": "",
        "ecwt_f": row["ecwt_f"],
        "valid_hour_count": row["valid_hour_count"],
        "expected_hour_count": row["expected_hour_count"],
        "coverage_ratio": row["coverage_ratio"],
        "overfilled_hour_count": "0",
        "fixed_coverage_ratio": row["coverage_ratio"],
        "fixed_loaded_station_year_count": "",
        "source_blocker_class": "",
        "source_active_window_class": "",
        "source_normalized_active_window_class": "",
        "notes": "Already passes the current fixed-period publication gate.",
    }


def promoted_candidate_row(row: dict[str, str], scenario_id: str, scenario: dict[str, str]) -> dict[str, object]:
    prefix = str(scenario["candidate_prefix"])
    if prefix == "best_active":
        coverage_prefix = "active"
    elif prefix == "best_normalized_active":
        coverage_prefix = "normalized_active"
    else:
        raise ValueError(f"Unsupported candidate prefix: {prefix}")
    return {
        "scenario_id": scenario_id,
        "scenario_label": scenario["label"],
        "policy_suitability": scenario["suitability"],
        "candidate_source": "promoted_fixed_period_blocker",
        "plant_id": row["plant_id"],
        "eia_plant_code": row["eia_plant_code"],
        "plant_name": row["plant_name"],
        "plant_state": row["plant_state"],
        "plant_county": row["plant_county"],
        "sector_name": row["sector_name"],
        "first_scope_generator_count": row["first_operable_generator_count"],
        "first_scope_nameplate_mw": row["first_operable_nameplate_mw"],
        "selected_station_id": station_value(row, prefix, "station_id"),
        "selected_station_name": station_value(row, prefix, "station_name"),
        "selected_station_state": station_value(row, prefix, "station_state"),
        "selected_station_country": station_value(row, prefix, "station_country"),
        "selected_station_distance_km": station_value(row, prefix, "distance_km"),
        "selected_station_rank_order": station_value(row, prefix, "rank_order"),
        "ecwt_f": station_value(row, prefix, "station_ecwt_f"),
        "valid_hour_count": station_value(row, prefix, f"{coverage_prefix}_valid_djf_hours"),
        "expected_hour_count": station_value(row, prefix, f"{coverage_prefix}_expected_djf_hours"),
        "coverage_ratio": station_value(row, prefix, f"{coverage_prefix}_coverage_ratio"),
        "overfilled_hour_count": station_value(row, prefix, f"{coverage_prefix}_overfilled_hour_count"),
        "fixed_coverage_ratio": station_value(row, prefix, "fixed_coverage_ratio"),
        "fixed_loaded_station_year_count": station_value(row, prefix, "loaded_station_year_count"),
        "source_blocker_class": row["current_blocker_class"],
        "source_active_window_class": row["active_window_class"],
        "source_normalized_active_window_class": row["normalized_active_window_class"],
        "notes": "Scenario promotion from fixed-period blocker; not part of the current publication gate.",
    }


def build_scenario_outputs(
    strict_rows: list[dict[str, str]],
    denominator_rows: list[dict[str, str]],
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    total_scope = len(strict_rows) + len(denominator_rows)
    matrix: list[dict[str, object]] = []
    candidates: list[dict[str, object]] = []
    strict_by_id = {row["plant_id"]: row for row in strict_rows}

    for scenario_id, scenario in SCENARIOS.items():
        promoted = [row for row in denominator_rows if scenario_promotes(row, scenario)]
        blocked = total_scope - len(strict_rows) - len(promoted)
        overfilled = 0
        ratio_gt_one = 0
        if scenario.get("candidate_prefix"):
            prefix = str(scenario["candidate_prefix"])
            if prefix == "best_active":
                ratio_field = f"{prefix}_active_coverage_ratio"
                overfill_field = f"{prefix}_active_overfilled_hour_count"
            else:
                ratio_field = f"{prefix}_normalized_active_coverage_ratio"
                overfill_field = f"{prefix}_normalized_active_overfilled_hour_count"
            overfilled = sum(1 for row in promoted if int_value(row.get(overfill_field)) > 0)
            ratio_gt_one = sum(1 for row in promoted if float_value(row.get(ratio_field)) > 1.0)

        matrix.append(
            {
                "scenario_id": scenario_id,
                "scenario_label": scenario["label"],
                "policy_suitability": scenario["suitability"],
                "total_first_operable_scope": total_scope,
                "current_fixed_candidates_retained": len(strict_rows),
                "fixed_period_blockers_promoted": len(promoted),
                "total_scenario_candidates": len(strict_rows) + len(promoted),
                "remaining_blocked": blocked,
                "promoted_candidate_overfill_rows": overfilled,
                "promoted_candidate_coverage_ratio_gt_1_rows": ratio_gt_one,
                "source": scenario["source"],
                "notes": scenario["notes"],
            }
        )

        for row in strict_rows:
            candidates.append(existing_candidate_row(row, scenario_id, scenario))
        for row in promoted:
            if row["plant_id"] in strict_by_id:
                continue
            candidates.append(promoted_candidate_row(row, scenario_id, scenario))
    return matrix, candidates


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
    strict_candidates_csv: Path,
    denominator_csv: Path,
    matrix_csv: Path,
    candidates_csv: Path,
    plant_scope: str,
    matrix_rows: list[dict[str, object]],
    candidate_rows: list[dict[str, object]],
) -> None:
    by_scenario = Counter(row["scenario_id"] for row in candidate_rows)
    normalized = next(row for row in matrix_rows if row["scenario_id"] == "normalized_active_window_loaded_year")
    raw = next(row for row in matrix_rows if row["scenario_id"] == "raw_active_window_metadata")
    fixed = next(row for row in matrix_rows if row["scenario_id"] == "fixed_period_current_gate")
    raw_overfill = int(raw["promoted_candidate_overfill_rows"])
    normalized_overfill = int(normalized["promoted_candidate_overfill_rows"])
    scenario_rows = [
        {
            "scenario_id": row["scenario_id"],
            "candidates": f"{int(row['total_scenario_candidates']):,}",
            "promoted": f"{int(row['fixed_period_blockers_promoted']):,}",
            "blocked": f"{int(row['remaining_blocked']):,}",
            "overfill": f"{int(row['promoted_candidate_overfill_rows']):,}",
            "suitability": row["policy_suitability"],
        }
        for row in matrix_rows
    ]
    lines = [
        "# ECWT Readiness Policy Scenario Comparison",
        "",
        f"Generated UTC: {utc_now().isoformat(timespec='seconds')}",
        "",
        "## Run",
        "",
        f"- Scenario run ID: `{run_id}`",
        f"- Code commit: `{code_commit}`",
        f"- Plant scope: `{plant_scope}`",
        f"- Strict fixed-period candidates CSV: `{strict_candidates_csv.name}`",
        f"- Denominator diagnostic CSV: `{denominator_csv.name}`",
        f"- Scenario matrix CSV: `{matrix_csv.name}`",
        f"- Scenario candidate detail CSV: `{candidates_csv.name}`",
        "",
        "## Scenario Matrix",
        "",
    ]
    render_table(
        lines,
        ["Scenario", "Candidates", "Promoted Blockers", "Remaining Blocked", "Overfill Rows", "Suitability"],
        scenario_rows,
        ["scenario_id", "candidates", "promoted", "blocked", "overfill", "suitability"],
    )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            f"- The current fixed-period gate has {int(fixed['total_scenario_candidates']):,} {plant_scope} publication candidates.",
            f"- The raw station metadata active-window scenario would produce {int(raw['total_scenario_candidates']):,} candidates, but it promotes {raw_overfill:,} rows with overfilled active-window denominators, so it remains diagnostic only.",
            f"- The normalized active-window loaded-year scenario would produce {int(normalized['total_scenario_candidates']):,} candidates and has {normalized_overfill:,} promoted overfill rows in this diagnostic.",
            "- Scenario candidates are not final compliance outputs; they are auditable policy alternatives for deciding the next publication gate.",
            "- The current fixed-period readiness table in Postgres is not overwritten by this script.",
            "",
            "## Candidate Detail Rows",
            "",
            "| Scenario | Rows |",
            "| --- | ---: |",
        ]
    )
    for scenario_id, count in by_scenario.items():
        lines.append(f"| `{scenario_id}` | {count:,} |")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--strict-candidates-csv", type=Path)
    parser.add_argument("--denominator-csv", type=Path)
    parser.add_argument("--plant-scope", choices=["first-operable", "all-plants"], default="first-operable")
    args = parser.parse_args()

    docs_dir = args.project_root / "docs"
    strict_candidates_csv = args.strict_candidates_csv or latest_strict_candidates_file(docs_dir, args.plant_scope)
    denominator_csv = args.denominator_csv or latest_denominator_file(docs_dir, args.plant_scope)
    expected_denominator_fragment = f"fixed_period_denominator_diagnostic_{args.plant_scope}_"
    if expected_denominator_fragment not in denominator_csv.name:
        raise ValueError(
            f"Denominator diagnostic scope mismatch: expected file containing "
            f"{expected_denominator_fragment!r}, got {denominator_csv.name!r}."
        )
    strict_rows = read_csv(strict_candidates_csv)
    denominator_rows = read_csv(denominator_csv)
    validate_inputs(strict_rows, denominator_rows, args.plant_scope)
    matrix_rows, candidate_rows = build_scenario_outputs(strict_rows, denominator_rows)

    scope_slug = args.plant_scope.replace("-", "_")
    run_id = f"readiness_policy_scenarios_{scope_slug}_{utc_now().strftime('%Y%m%dT%H%M%SZ')}"
    code_commit = git_commit_label(args.project_root)
    matrix_csv = docs_dir / f"{run_id}_matrix.csv"
    candidates_csv = docs_dir / f"{run_id}_candidates.csv"
    report_path = docs_dir / f"{run_id}_report.md"
    matrix_fields = [
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
    candidate_fields = [
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
    write_csv(matrix_csv, matrix_fields, matrix_rows)
    write_csv(candidates_csv, candidate_fields, candidate_rows)
    render_report(
        report_path,
        run_id,
        code_commit,
        strict_candidates_csv,
        denominator_csv,
        matrix_csv,
        candidates_csv,
        args.plant_scope,
        matrix_rows,
        candidate_rows,
    )
    print(
        json.dumps(
            OrderedDict(
                [
                    ("run_id", run_id),
                    ("plant_scope", args.plant_scope),
                    ("strict_candidates_csv", str(strict_candidates_csv)),
                    ("denominator_csv", str(denominator_csv)),
                    ("matrix_csv", str(matrix_csv)),
                    ("candidates_csv", str(candidates_csv)),
                    ("report_path", str(report_path)),
                    ("matrix_rows", len(matrix_rows)),
                    ("candidate_rows", len(candidate_rows)),
                ]
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
