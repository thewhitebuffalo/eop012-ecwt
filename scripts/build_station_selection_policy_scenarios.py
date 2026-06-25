#!/usr/bin/env python3
"""Build read-only policy scenarios for station-selection review decisions."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
from collections import Counter, OrderedDict
from datetime import datetime, timezone
from pathlib import Path

from apply_station_selection_review_updates import latest_review_run_id, psql_csv_query, template_query
from eop012_config import PROJECT_ROOT, PSQL


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


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


def git_commit_label(project_root: Path) -> str:
    try:
        return run(["git", "-C", str(project_root), "rev-parse", "HEAD"]).stdout.strip()
    except Exception:
        return "UNCOMMITTED_WORKTREE"


def to_float(value: str | None) -> float | None:
    if value is None or value == "":
        return None
    return float(value)


def to_int(value: str | None) -> int | None:
    if value is None or value == "":
        return None
    return int(float(value))


def scenario_definitions() -> list[dict[str, object]]:
    return [
        {
            "scenario_id": "current_gate",
            "scenario_name": "Current review gate",
            "description": "No station-selection review rows are accepted until a reviewer or policy run updates them.",
            "countries": [],
            "max_distance_km": None,
            "max_rank": None,
            "min_coverage_ratio": None,
            "require_same_state": False,
            "accept_none": True,
        },
        {
            "scenario_id": "us_same_state_core",
            "scenario_name": "US same-state core",
            "description": "Accept only US stations in the same state, within 50 km, rank <= 3, and coverage >= 0.97.",
            "countries": ["US"],
            "max_distance_km": 50.0,
            "max_rank": 3,
            "min_coverage_ratio": 0.97,
            "require_same_state": True,
            "accept_none": False,
        },
        {
            "scenario_id": "us_regional_core",
            "scenario_name": "US regional core",
            "description": "Accept US stations within 75 km, rank <= 3, and coverage >= 0.97; state mismatch may still need review.",
            "countries": ["US"],
            "max_distance_km": 75.0,
            "max_rank": 3,
            "min_coverage_ratio": 0.97,
            "require_same_state": False,
            "accept_none": False,
        },
        {
            "scenario_id": "us_fixed_gate_only",
            "scenario_name": "US fixed-period gate only",
            "description": "Accept US stations that pass the fixed-period coverage gate regardless of rank or distance.",
            "countries": ["US"],
            "max_distance_km": None,
            "max_rank": None,
            "min_coverage_ratio": 0.95,
            "require_same_state": False,
            "accept_none": False,
        },
        {
            "scenario_id": "us_ca_core",
            "scenario_name": "US and Canada core",
            "description": "Accept US or Canadian stations within 75 km, rank <= 3, and coverage >= 0.97.",
            "countries": ["US", "CA"],
            "max_distance_km": 75.0,
            "max_rank": 3,
            "min_coverage_ratio": 0.97,
            "require_same_state": False,
            "accept_none": False,
        },
        {
            "scenario_id": "us_ca_practical",
            "scenario_name": "US and Canada practical",
            "description": "Accept US or Canadian stations within 75 km, rank <= 10, and coverage >= 0.95.",
            "countries": ["US", "CA"],
            "max_distance_km": 75.0,
            "max_rank": 10,
            "min_coverage_ratio": 0.95,
            "require_same_state": False,
            "accept_none": False,
        },
        {
            "scenario_id": "us_ca_distance_cap_150",
            "scenario_name": "US and Canada distance cap 150 km",
            "description": "Accept US or Canadian stations within 150 km, rank <= 10, and coverage >= 0.95.",
            "countries": ["US", "CA"],
            "max_distance_km": 150.0,
            "max_rank": 10,
            "min_coverage_ratio": 0.95,
            "require_same_state": False,
            "accept_none": False,
        },
        {
            "scenario_id": "fixed_coverage_only",
            "scenario_name": "Fixed-period coverage only",
            "description": "Accept every current fixed-period candidate, ignoring station-selection QA flags.",
            "countries": ["US", "CA"],
            "max_distance_km": None,
            "max_rank": None,
            "min_coverage_ratio": 0.95,
            "require_same_state": False,
            "accept_none": False,
        },
    ]


def qualifies(row: dict[str, str], scenario: dict[str, object]) -> bool:
    if scenario.get("accept_none"):
        return False
    countries = set(scenario["countries"])
    station_country = (row.get("station_country") or "").upper()
    if countries and station_country not in countries:
        return False
    min_coverage = scenario.get("min_coverage_ratio")
    coverage = to_float(row.get("coverage_ratio")) or 0.0
    if min_coverage is not None and coverage < float(min_coverage):
        return False
    max_distance = scenario.get("max_distance_km")
    distance = to_float(row.get("selected_distance_km"))
    if max_distance is not None and (distance is None or distance > float(max_distance)):
        return False
    max_rank = scenario.get("max_rank")
    rank = to_int(row.get("selected_rank_order"))
    if max_rank is not None and (rank is None or rank > int(max_rank)):
        return False
    if scenario.get("require_same_state"):
        plant_state = (row.get("plant_state") or "").upper()
        station_state = (row.get("station_state") or "").upper()
        if not plant_state or not station_state or plant_state != station_state:
            return False
    return True


def summarize_scenario(rows: list[dict[str, str]], scenario: dict[str, object]) -> dict[str, object]:
    accepted = [row for row in rows if qualifies(row, scenario)]
    blocked = len(rows) - len(accepted)
    states = Counter(row.get("plant_state") or "(blank)" for row in accepted)
    countries = Counter(row.get("station_country") or "(blank)" for row in accepted)
    stations = {row.get("station_id") for row in accepted if row.get("station_id")}
    coverages = [to_float(row.get("coverage_ratio")) for row in accepted if to_float(row.get("coverage_ratio")) is not None]
    distances = [to_float(row.get("selected_distance_km")) for row in accepted if to_float(row.get("selected_distance_km")) is not None]
    ranks = [to_int(row.get("selected_rank_order")) for row in accepted if to_int(row.get("selected_rank_order")) is not None]
    ecwts = [to_float(row.get("governing_ecwt_f")) for row in accepted if to_float(row.get("governing_ecwt_f")) is not None]
    return {
        "scenario_id": scenario["scenario_id"],
        "scenario_name": scenario["scenario_name"],
        "description": scenario["description"],
        "accepted_rows": len(accepted),
        "blocked_rows": blocked,
        "distinct_selected_stations": len(stations),
        "plant_states": ";".join(f"{state}:{count}" for state, count in states.most_common()),
        "station_countries": ";".join(f"{country}:{count}" for country, count in countries.most_common()),
        "min_coverage_ratio": min(coverages) if coverages else "",
        "median_coverage_ratio": sorted(coverages)[len(coverages) // 2] if coverages else "",
        "max_distance_km": max(distances) if distances else "",
        "max_rank_order": max(ranks) if ranks else "",
        "min_ecwt_f": min(ecwts) if ecwts else "",
        "max_ecwt_f": max(ecwts) if ecwts else "",
    }


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def build_matrix(rows: list[dict[str, str]], scenarios: list[dict[str, object]]) -> list[dict[str, object]]:
    matrix: list[dict[str, object]] = []
    for row in rows:
        scenario_hits = [str(scenario["scenario_id"]) for scenario in scenarios if qualifies(row, scenario)]
        matrix.append(
            {
                "eia_plant_code": row.get("eia_plant_code", ""),
                "plant_name": row.get("plant_name", ""),
                "plant_state": row.get("plant_state", ""),
                "station_id": row.get("station_id", ""),
                "station_name": row.get("station_name", ""),
                "station_country": row.get("station_country", ""),
                "station_state": row.get("station_state", ""),
                "selected_distance_km": row.get("selected_distance_km", ""),
                "selected_rank_order": row.get("selected_rank_order", ""),
                "coverage_ratio": row.get("coverage_ratio", ""),
                "governing_ecwt_f": row.get("governing_ecwt_f", ""),
                "risk_flags": row.get("risk_flags", ""),
                "qualifying_scenarios": ";".join(scenario_hits),
                "qualifying_scenario_count": len(scenario_hits),
            }
        )
    return matrix


def format_value(value: object, digits: int = 3) -> str:
    if value is None or value == "":
        return ""
    if isinstance(value, str):
        return value
    number = float(value)
    if number.is_integer():
        return f"{int(number):,}"
    return f"{number:,.{digits}f}"


def md_table(rows: list[dict[str, object]], fields: list[str], headers: list[str]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(format_value(row.get(field, "")) for field in fields) + " |")
    return lines


def render_report(
    path: Path,
    run_id: str,
    source_review_run_id: str,
    code_commit: str,
    summary_path: Path,
    matrix_path: Path,
    summary_rows: list[dict[str, object]],
    matrix_rows: list[dict[str, object]],
) -> None:
    flag_counts: Counter[str] = Counter()
    for row in matrix_rows:
        for flag in str(row.get("risk_flags") or "").split(";"):
            if flag:
                flag_counts[flag] += 1
    flag_rows = [{"flag": flag, "rows": count} for flag, count in flag_counts.most_common()]
    lines = [
        "# Station Selection Policy Scenario Report",
        "",
        f"Generated UTC: {utc_now().isoformat(timespec='seconds')}",
        "",
        "## Summary",
        "",
        (
            "This read-only report evaluates named policy scenarios against the current fixed-period station-selection "
            "review queue. It does not accept or reject any station assignment."
        ),
        "",
        "## Run",
        "",
        f"- Scenario run ID: `{run_id}`",
        f"- Source review run ID: `{source_review_run_id}`",
        f"- Code commit: `{code_commit}`",
        f"- Scenario summary CSV: `{summary_path.name}`",
        f"- Row-level scenario matrix CSV: `{matrix_path.name}`",
        "",
        "## Scenario Counts",
        "",
    ]
    lines.extend(
        md_table(
            summary_rows,
            [
                "scenario_id",
                "accepted_rows",
                "blocked_rows",
                "distinct_selected_stations",
                "min_coverage_ratio",
                "max_distance_km",
                "max_rank_order",
                "min_ecwt_f",
                "max_ecwt_f",
            ],
            [
                "Scenario",
                "Accepted",
                "Blocked",
                "Stations",
                "Min Coverage",
                "Max Distance km",
                "Max Rank",
                "Min ECWT F",
                "Max ECWT F",
            ],
        )
    )
    lines.extend(["", "## QA Flag Inventory", ""])
    lines.extend(md_table(flag_rows, ["flag", "rows"], ["QA Flag", "Rows"]))
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `current_gate` matches the current release gate: no rows are accepted until review dispositions change.",
            "- `fixed_coverage_only` is the mathematical upper bound from the current fixed-period candidate cohort.",
            "- Scenarios that allow Canadian stations unlock most of the queue, but they are policy decisions, not data-quality facts.",
            "- High-rank and long-distance fallbacks dominate the remaining decision surface. Those should be accepted only if the methodology explicitly allows them.",
            "- To apply a policy, edit the review worksheet and run `scripts/apply_station_selection_review_updates.py` without `--dry-run`.",
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
    parser.add_argument("--source-review-run-id")
    args = parser.parse_args()

    source_review_run_id = args.source_review_run_id or latest_review_run_id(
        args.psql, args.host, args.port, args.dbname, args.user
    )
    run_id = f"station_selection_policy_scenarios_{utc_now().strftime('%Y%m%dT%H%M%SZ')}"
    code_commit = git_commit_label(args.project_root)
    rows = psql_csv_query(args.psql, args.host, args.port, args.dbname, template_query(source_review_run_id), args.user)
    scenarios = scenario_definitions()
    summary_rows = [summarize_scenario(rows, scenario) for scenario in scenarios]
    matrix_rows = build_matrix(rows, scenarios)

    docs_dir = args.project_root / "docs"
    summary_path = docs_dir / f"{run_id}.csv"
    matrix_path = docs_dir / f"{run_id}_matrix.csv"
    report_path = docs_dir / f"{run_id}_report.md"
    summary_fields = [
        "scenario_id",
        "scenario_name",
        "description",
        "accepted_rows",
        "blocked_rows",
        "distinct_selected_stations",
        "plant_states",
        "station_countries",
        "min_coverage_ratio",
        "median_coverage_ratio",
        "max_distance_km",
        "max_rank_order",
        "min_ecwt_f",
        "max_ecwt_f",
    ]
    matrix_fields = [
        "eia_plant_code",
        "plant_name",
        "plant_state",
        "station_id",
        "station_name",
        "station_country",
        "station_state",
        "selected_distance_km",
        "selected_rank_order",
        "coverage_ratio",
        "governing_ecwt_f",
        "risk_flags",
        "qualifying_scenarios",
        "qualifying_scenario_count",
    ]
    write_csv(summary_path, summary_fields, summary_rows)
    write_csv(matrix_path, matrix_fields, matrix_rows)
    render_report(report_path, run_id, source_review_run_id, code_commit, summary_path, matrix_path, summary_rows, matrix_rows)
    print(
        json.dumps(
            OrderedDict(
                [
                    ("run_id", run_id),
                    ("source_review_run_id", source_review_run_id),
                    ("candidate_rows", len(rows)),
                    ("scenario_rows", len(summary_rows)),
                    ("summary_path", str(summary_path)),
                    ("matrix_path", str(matrix_path)),
                    ("report_path", str(report_path)),
                ]
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
