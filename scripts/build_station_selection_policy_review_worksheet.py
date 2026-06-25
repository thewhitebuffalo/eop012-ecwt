#!/usr/bin/env python3
"""Build a complete station-selection review worksheet from a named policy scenario."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
from collections import Counter, OrderedDict
from datetime import datetime, timezone
from pathlib import Path

from apply_station_selection_review_updates import (
    TEMPLATE_FIELDS,
    latest_review_run_id,
    psql_csv_query,
    template_query,
    write_csv,
)
from build_station_selection_policy_scenarios import qualifies, scenario_definitions
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


def scenario_by_id(scenario_id: str) -> dict[str, object]:
    for scenario in scenario_definitions():
        if scenario["scenario_id"] == scenario_id:
            return scenario
    valid = ", ".join(str(scenario["scenario_id"]) for scenario in scenario_definitions())
    raise RuntimeError(f"Unknown scenario_id {scenario_id!r}; expected one of: {valid}")


def policy_note(scenario: dict[str, object], row: dict[str, str]) -> str:
    return (
        f"Accepted by policy scenario {scenario['scenario_id']}: {scenario['description']} "
        f"Observed values: station_country={row.get('station_country', '')}, "
        f"distance_km={row.get('selected_distance_km', '')}, "
        f"rank_order={row.get('selected_rank_order', '')}, "
        f"coverage_ratio={row.get('coverage_ratio', '')}, "
        f"risk_flags={row.get('risk_flags', '') or 'none'}."
    )


def build_policy_rows(
    rows: list[dict[str, str]],
    scenario: dict[str, object],
    reviewer: str,
    accept_reason: str,
) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    for row in rows:
        out = dict(row)
        if qualifies(row, scenario):
            out["proposed_review_status"] = "accepted"
            out["proposed_review_basis"] = "policy_override"
            out["proposed_disposition_reason"] = accept_reason
            out["reviewer"] = reviewer
            out["review_notes"] = policy_note(scenario, row)
        output.append(out)
    return output


def render_report(
    path: Path,
    run_id: str,
    source_review_run_id: str,
    scenario: dict[str, object],
    code_commit: str,
    worksheet_path: Path,
    rows: list[dict[str, str]],
) -> None:
    accepted = [row for row in rows if row.get("proposed_review_status") == "accepted"]
    preserved = len(rows) - len(accepted)
    flag_counts: Counter[str] = Counter()
    state_counts: Counter[str] = Counter(row.get("plant_state") or "(blank)" for row in accepted)
    country_counts: Counter[str] = Counter(row.get("station_country") or "(blank)" for row in accepted)
    for row in accepted:
        for flag in (row.get("risk_flags") or "").split(";"):
            if flag:
                flag_counts[flag] += 1

    lines = [
        "# Station Selection Policy Review Worksheet",
        "",
        f"Generated UTC: {utc_now().isoformat(timespec='seconds')}",
        "",
        "## Run",
        "",
        f"- Worksheet run ID: `{run_id}`",
        f"- Source review run ID: `{source_review_run_id}`",
        f"- Scenario ID: `{scenario['scenario_id']}`",
        f"- Scenario name: `{scenario['scenario_name']}`",
        f"- Code commit: `{code_commit}`",
        f"- Worksheet CSV: `{worksheet_path.name}`",
        "",
        "## Policy",
        "",
        str(scenario["description"]),
        "",
        "## Counts",
        "",
        "| Metric | Rows |",
        "| --- | ---: |",
        f"| Source review rows | {len(rows):,} |",
        f"| Proposed accepted rows | {len(accepted):,} |",
        f"| Preserved as current disposition | {preserved:,} |",
        "",
        "## Accepted Rows By Plant State",
        "",
        "| Plant State | Rows |",
        "| --- | ---: |",
    ]
    for state, count in state_counts.most_common():
        lines.append(f"| `{state}` | {count:,} |")
    lines.extend(["", "## Accepted Rows By Station Country", "", "| Station Country | Rows |", "| --- | ---: |"])
    for country, count in country_counts.most_common():
        lines.append(f"| `{country}` | {count:,} |")
    lines.extend(["", "## Accepted Row QA Flags", "", "| QA Flag | Rows |", "| --- | ---: |"])
    if flag_counts:
        for flag, count in flag_counts.most_common():
            lines.append(f"| `{flag}` | {count:,} |")
    else:
        lines.append("| No QA flags | 0 |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- This file is a complete review worksheet for `scripts/apply_station_selection_review_updates.py`.",
            "- Rows not qualifying under the policy keep blank proposed fields, which preserves their current disposition.",
            "- Applying this worksheet changes only the station-selection review snapshot and derived release-readiness gate.",
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
    parser.add_argument("--scenario-id", required=True)
    parser.add_argument("--reviewer", default="codex_policy_us_ca_core")
    parser.add_argument("--accept-reason")
    args = parser.parse_args()

    scenario = scenario_by_id(args.scenario_id)
    source_review_run_id = args.source_review_run_id or latest_review_run_id(
        args.psql, args.host, args.port, args.dbname, args.user
    )
    accept_reason = args.accept_reason or f"policy_accept_{args.scenario_id}"
    code_commit = git_commit_label(args.project_root)
    rows = psql_csv_query(args.psql, args.host, args.port, args.dbname, template_query(source_review_run_id), args.user)
    output_rows = build_policy_rows(rows, scenario, args.reviewer, accept_reason)

    run_id = f"station_selection_policy_review_{args.scenario_id}_{utc_now().strftime('%Y%m%dT%H%M%SZ')}"
    docs_dir = args.project_root / "docs"
    worksheet_path = docs_dir / f"{run_id}.csv"
    report_path = docs_dir / f"{run_id}_report.md"
    write_csv(worksheet_path, TEMPLATE_FIELDS, output_rows)
    render_report(report_path, run_id, source_review_run_id, scenario, code_commit, worksheet_path, output_rows)
    print(
        json.dumps(
            OrderedDict(
                [
                    ("run_id", run_id),
                    ("source_review_run_id", source_review_run_id),
                    ("scenario_id", args.scenario_id),
                    ("rows", len(output_rows)),
                    ("proposed_accepted_rows", sum(1 for row in output_rows if row.get("proposed_review_status") == "accepted")),
                    ("worksheet_path", str(worksheet_path)),
                    ("report_path", str(report_path)),
                ]
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
