#!/usr/bin/env python3
"""Prioritize remaining normalized active-window coverage blockers."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import statistics
import subprocess
from collections import Counter, OrderedDict, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from eop012_config import PROJECT_ROOT, PSQL


METHODOLOGY_VERSION = "eop012-ecwt-method-v0.1.0"
COVERAGE_POLICY = "normalized_active_window_coverage"
DEFAULT_PLANT_SCOPE = "first-operable"
TARGET_CLASS = "still_fails_normalized_active_window_coverage"

PRIORITY_FIELDS = [
    "priority_run_id",
    "diagnostic_run_id",
    "plant_scope",
    "coverage_policy",
    "priority_rank",
    "priority_bucket",
    "plant_id",
    "eia_plant_code",
    "plant_name",
    "plant_state",
    "plant_county",
    "nerc_region",
    "balancing_authority_code",
    "sector_name",
    "first_operable_generator_count",
    "first_operable_nameplate_mw",
    "current_blocker_class",
    "normalized_active_window_class",
    "candidate_count",
    "candidate_with_provisional_station_ecwt_count",
    "normalized_active_coverage_eligible_candidate_count",
    "best_station_id",
    "best_station_name",
    "best_station_state",
    "best_station_country",
    "best_distance_km",
    "best_rank_order",
    "best_station_ecwt_status",
    "best_station_ecwt_valid_hour_count",
    "best_station_ecwt_f",
    "fixed_coverage_ratio",
    "fixed_valid_djf_hours",
    "fixed_expected_djf_hours",
    "fixed_loaded_station_year_count",
    "first_loaded_year",
    "last_loaded_year",
    "normalized_active_first_utc",
    "normalized_active_last_utc",
    "normalized_expected_djf_hours",
    "normalized_valid_djf_hours",
    "normalized_missing_djf_hours",
    "normalized_overfilled_hour_count",
    "normalized_djf_year_count",
    "normalized_loaded_station_year_count",
    "normalized_coverage_ratio",
    "normalized_loaded_year_ratio",
    "valid_hour_gap_to_threshold",
    "coverage_ratio_gap_to_threshold",
    "notes",
]

STATION_SUMMARY_FIELDS = [
    "priority_run_id",
    "station_id",
    "station_name",
    "station_state",
    "station_country",
    "plant_count",
    "distinct_plant_states",
    "top_plant_states",
    "min_distance_km",
    "median_distance_km",
    "max_distance_km",
    "min_normalized_coverage_ratio",
    "median_normalized_coverage_ratio",
    "max_normalized_coverage_ratio",
    "total_valid_hour_gap_to_threshold",
    "gap_le_24h_count",
    "gap_le_168h_count",
    "gap_le_720h_count",
    "gap_le_2160h_count",
    "gap_gt_2160h_count",
]

STATE_SUMMARY_FIELDS = [
    "priority_run_id",
    "plant_state",
    "plant_count",
    "distinct_station_count",
    "total_first_operable_nameplate_mw",
    "min_normalized_coverage_ratio",
    "median_normalized_coverage_ratio",
    "max_normalized_coverage_ratio",
    "total_valid_hour_gap_to_threshold",
    "gap_le_24h_count",
    "gap_le_168h_count",
    "gap_le_720h_count",
    "gap_le_2160h_count",
    "gap_gt_2160h_count",
    "top_station_ids",
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


def latest_file(docs_dir: Path, pattern: str) -> Path:
    matches = sorted(docs_dir.glob(pattern))
    if not matches:
        raise FileNotFoundError(f"No files matched {docs_dir / pattern}")
    return matches[-1]


def git_commit_label(project_root: Path) -> str:
    try:
        return run(["git", "-C", str(project_root), "rev-parse", "HEAD"]).stdout.strip()
    except Exception:
        return "UNCOMMITTED_WORKTREE"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: "" if row.get(field) is None else row.get(field, "") for field in fieldnames})


def to_int(value: object) -> int | None:
    if value is None or value == "":
        return None
    return int(float(str(value)))


def to_float(value: object) -> float | None:
    if value is None or value == "":
        return None
    return float(str(value))


def fmt_float(value: float | None, digits: int = 6) -> str:
    if value is None:
        return ""
    return f"{value:.{digits}f}"


def median(values: list[float]) -> float | None:
    return statistics.median(values) if values else None


def percentile_gap_bucket(gap: int | None) -> str:
    if gap is None:
        return "missing_station_metric"
    if gap <= 24:
        return "gap_le_24h"
    if gap <= 168:
        return "gap_le_168h"
    if gap <= 720:
        return "gap_le_720h"
    if gap <= 2160:
        return "gap_le_2160h"
    return "gap_gt_2160h"


def bucket_order(bucket: str) -> int:
    order = {
        "gap_le_24h": 1,
        "gap_le_168h": 2,
        "gap_le_720h": 3,
        "gap_le_2160h": 4,
        "gap_gt_2160h": 5,
        "missing_station_metric": 6,
    }
    return order.get(bucket, 99)


def source_row(path: Path, source_release: str) -> dict[str, object]:
    digest = sha256_file(path)
    return {
        "source_file_id": f"eop012_normalized_coverage_blocker_diagnostic:{digest}",
        "source_family": "eop012_normalized_coverage_blocker_diagnostic",
        "local_path": str(path),
        "file_name": path.name,
        "size_bytes": path.stat().st_size,
        "sha256": digest,
        "retrieved_at_utc": datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat(),
        "source_release": source_release,
        "notes": "Generated EOP012 fixed-period denominator diagnostic used for normalized active-window blocker prioritization.",
    }


def build_priority_rows(
    diagnostic_rows: list[dict[str, str]],
    run_id: str,
    diagnostic_run_id: str,
    plant_scope: str,
    min_coverage_ratio: float,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in diagnostic_rows:
        if row.get("normalized_active_window_class") != TARGET_CLASS:
            continue
        expected = to_int(row.get("best_normalized_active_normalized_active_expected_djf_hours"))
        valid = to_int(row.get("best_normalized_active_normalized_active_valid_djf_hours"))
        coverage_ratio = to_float(row.get("best_normalized_active_normalized_active_coverage_ratio"))
        gap: int | None = None
        ratio_gap: float | None = None
        if expected is not None and valid is not None and expected > 0:
            required_valid = math.ceil(expected * min_coverage_ratio)
            gap = max(required_valid - valid, 0)
        if coverage_ratio is not None:
            ratio_gap = max(min_coverage_ratio - coverage_ratio, 0.0)
        bucket = percentile_gap_bucket(gap)
        rows.append(
            {
                "priority_run_id": run_id,
                "diagnostic_run_id": diagnostic_run_id,
                "plant_scope": plant_scope,
                "coverage_policy": COVERAGE_POLICY,
                "priority_rank": 0,
                "priority_bucket": bucket,
                "plant_id": row.get("plant_id", ""),
                "eia_plant_code": row.get("eia_plant_code", ""),
                "plant_name": row.get("plant_name", ""),
                "plant_state": row.get("plant_state", ""),
                "plant_county": row.get("plant_county", ""),
                "nerc_region": row.get("nerc_region", ""),
                "balancing_authority_code": row.get("balancing_authority_code", ""),
                "sector_name": row.get("sector_name", ""),
                "first_operable_generator_count": row.get("first_operable_generator_count", ""),
                "first_operable_nameplate_mw": row.get("first_operable_nameplate_mw", ""),
                "current_blocker_class": row.get("current_blocker_class", ""),
                "normalized_active_window_class": row.get("normalized_active_window_class", ""),
                "candidate_count": row.get("candidate_count", ""),
                "candidate_with_provisional_station_ecwt_count": row.get(
                    "candidate_with_provisional_station_ecwt_count", ""
                ),
                "normalized_active_coverage_eligible_candidate_count": row.get(
                    "normalized_active_coverage_eligible_candidate_count", ""
                ),
                "best_station_id": row.get("best_normalized_active_station_id", ""),
                "best_station_name": row.get("best_normalized_active_station_name", ""),
                "best_station_state": row.get("best_normalized_active_station_state", ""),
                "best_station_country": row.get("best_normalized_active_station_country", ""),
                "best_distance_km": row.get("best_normalized_active_distance_km", ""),
                "best_rank_order": row.get("best_normalized_active_rank_order", ""),
                "best_station_ecwt_status": row.get("best_normalized_active_station_ecwt_status", ""),
                "best_station_ecwt_valid_hour_count": row.get(
                    "best_normalized_active_station_ecwt_valid_hour_count", ""
                ),
                "best_station_ecwt_f": row.get("best_normalized_active_station_ecwt_f", ""),
                "fixed_coverage_ratio": row.get("best_normalized_active_fixed_coverage_ratio", ""),
                "fixed_valid_djf_hours": row.get("best_normalized_active_fixed_valid_djf_hours", ""),
                "fixed_expected_djf_hours": row.get("best_normalized_active_fixed_expected_djf_hours", ""),
                "fixed_loaded_station_year_count": row.get("best_normalized_active_loaded_station_year_count", ""),
                "first_loaded_year": row.get("best_normalized_active_first_loaded_year", ""),
                "last_loaded_year": row.get("best_normalized_active_last_loaded_year", ""),
                "normalized_active_first_utc": row.get("best_normalized_active_normalized_active_first_utc", ""),
                "normalized_active_last_utc": row.get("best_normalized_active_normalized_active_last_utc", ""),
                "normalized_expected_djf_hours": row.get(
                    "best_normalized_active_normalized_active_expected_djf_hours", ""
                ),
                "normalized_valid_djf_hours": row.get(
                    "best_normalized_active_normalized_active_valid_djf_hours", ""
                ),
                "normalized_missing_djf_hours": row.get(
                    "best_normalized_active_normalized_active_missing_djf_hours", ""
                ),
                "normalized_overfilled_hour_count": row.get(
                    "best_normalized_active_normalized_active_overfilled_hour_count", ""
                ),
                "normalized_djf_year_count": row.get(
                    "best_normalized_active_normalized_active_djf_year_count", ""
                ),
                "normalized_loaded_station_year_count": row.get(
                    "best_normalized_active_normalized_active_loaded_station_year_count", ""
                ),
                "normalized_coverage_ratio": row.get(
                    "best_normalized_active_normalized_active_coverage_ratio", ""
                ),
                "normalized_loaded_year_ratio": row.get(
                    "best_normalized_active_normalized_active_loaded_year_ratio", ""
                ),
                "valid_hour_gap_to_threshold": "" if gap is None else gap,
                "coverage_ratio_gap_to_threshold": fmt_float(ratio_gap),
                "notes": (
                    "Still fails normalized active-window 0.95 coverage threshold; gap is the additional "
                    "valid DJF-hour count needed at the current best normalized-active candidate station."
                ),
            }
        )
    rows.sort(
        key=lambda item: (
            bucket_order(str(item["priority_bucket"])),
            to_int(item["valid_hour_gap_to_threshold"]) if item["valid_hour_gap_to_threshold"] != "" else 999999999,
            to_float(item["coverage_ratio_gap_to_threshold"]) or 999.0,
            str(item["plant_state"]),
            str(item["best_station_id"]),
            to_int(item["eia_plant_code"]) or 999999999,
        )
    )
    for index, row in enumerate(rows, start=1):
        row["priority_rank"] = index
    return rows


def bucket_counts(rows: list[dict[str, object]]) -> Counter[str]:
    return Counter(str(row["priority_bucket"]) for row in rows)


def build_station_summary(rows: list[dict[str, object]], run_id: str) -> list[dict[str, object]]:
    groups: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        station_id = str(row.get("best_station_id") or "")
        if station_id:
            groups[station_id].append(row)
    summaries: list[dict[str, object]] = []
    for station_id, group in groups.items():
        ratios = [to_float(row.get("normalized_coverage_ratio")) for row in group]
        ratios = [value for value in ratios if value is not None]
        distances = [to_float(row.get("best_distance_km")) for row in group]
        distances = [value for value in distances if value is not None]
        gaps = [to_int(row.get("valid_hour_gap_to_threshold")) for row in group]
        gaps = [value for value in gaps if value is not None]
        state_counts = Counter(str(row.get("plant_state") or "(blank)") for row in group)
        buckets = bucket_counts(group)
        first = group[0]
        summaries.append(
            {
                "priority_run_id": run_id,
                "station_id": station_id,
                "station_name": first.get("best_station_name", ""),
                "station_state": first.get("best_station_state", ""),
                "station_country": first.get("best_station_country", ""),
                "plant_count": len(group),
                "distinct_plant_states": len(state_counts),
                "top_plant_states": ";".join(f"{state}:{count}" for state, count in state_counts.most_common(8)),
                "min_distance_km": fmt_float(min(distances), 3) if distances else "",
                "median_distance_km": fmt_float(median(distances), 3),
                "max_distance_km": fmt_float(max(distances), 3) if distances else "",
                "min_normalized_coverage_ratio": fmt_float(min(ratios), 6) if ratios else "",
                "median_normalized_coverage_ratio": fmt_float(median(ratios), 6),
                "max_normalized_coverage_ratio": fmt_float(max(ratios), 6) if ratios else "",
                "total_valid_hour_gap_to_threshold": sum(gaps),
                "gap_le_24h_count": buckets["gap_le_24h"],
                "gap_le_168h_count": buckets["gap_le_168h"],
                "gap_le_720h_count": buckets["gap_le_720h"],
                "gap_le_2160h_count": buckets["gap_le_2160h"],
                "gap_gt_2160h_count": buckets["gap_gt_2160h"],
            }
        )
    summaries.sort(key=lambda row: (-int(row["plant_count"]), int(row["total_valid_hour_gap_to_threshold"]), row["station_id"]))
    return summaries


def build_state_summary(rows: list[dict[str, object]], run_id: str) -> list[dict[str, object]]:
    groups: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        groups[str(row.get("plant_state") or "(blank)")].append(row)
    summaries: list[dict[str, object]] = []
    for state, group in groups.items():
        ratios = [to_float(row.get("normalized_coverage_ratio")) for row in group]
        ratios = [value for value in ratios if value is not None]
        gaps = [to_int(row.get("valid_hour_gap_to_threshold")) for row in group]
        gaps = [value for value in gaps if value is not None]
        mw = [to_float(row.get("first_operable_nameplate_mw")) for row in group]
        mw = [value for value in mw if value is not None]
        stations = [str(row.get("best_station_id") or "") for row in group if row.get("best_station_id")]
        station_counts = Counter(stations)
        buckets = bucket_counts(group)
        summaries.append(
            {
                "priority_run_id": run_id,
                "plant_state": state,
                "plant_count": len(group),
                "distinct_station_count": len(station_counts),
                "total_first_operable_nameplate_mw": fmt_float(sum(mw), 3),
                "min_normalized_coverage_ratio": fmt_float(min(ratios), 6) if ratios else "",
                "median_normalized_coverage_ratio": fmt_float(median(ratios), 6),
                "max_normalized_coverage_ratio": fmt_float(max(ratios), 6) if ratios else "",
                "total_valid_hour_gap_to_threshold": sum(gaps),
                "gap_le_24h_count": buckets["gap_le_24h"],
                "gap_le_168h_count": buckets["gap_le_168h"],
                "gap_le_720h_count": buckets["gap_le_720h"],
                "gap_le_2160h_count": buckets["gap_le_2160h"],
                "gap_gt_2160h_count": buckets["gap_gt_2160h"],
                "top_station_ids": ";".join(f"{station}:{count}" for station, count in station_counts.most_common(8)),
            }
        )
    summaries.sort(key=lambda row: (-int(row["plant_count"]), row["plant_state"]))
    return summaries


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


def text_null(field: str) -> str:
    return f"nullif({qident(field)}, '')"


def build_load_sql(
    run_id: str,
    code_commit: str,
    started_at: str,
    params: dict[str, object],
    diagnostic_source: dict[str, object],
    priority_csv: Path,
    station_summary_csv: Path,
    state_summary_csv: Path,
) -> str:
    return f"""
\\set ON_ERROR_STOP on
begin;

create table if not exists calc.coverage_blocker_priority (
    priority_row_id text primary key,
    priority_run_id text not null references audit.calculation_run(calculation_run_id),
    diagnostic_run_id text not null,
    plant_scope text not null,
    coverage_policy text not null,
    priority_rank integer not null,
    priority_bucket text not null,
    plant_id text not null references asset.plant(plant_id),
    eia_plant_code text,
    plant_name text,
    plant_state text,
    plant_county text,
    nerc_region text,
    balancing_authority_code text,
    sector_name text,
    first_operable_generator_count integer,
    first_operable_nameplate_mw numeric,
    current_blocker_class text,
    normalized_active_window_class text,
    candidate_count integer,
    candidate_with_provisional_station_ecwt_count integer,
    normalized_active_coverage_eligible_candidate_count integer,
    best_station_id text references weather.station(station_id),
    best_station_name text,
    best_station_state text,
    best_station_country text,
    best_distance_km numeric,
    best_rank_order integer,
    best_station_ecwt_status text,
    best_station_ecwt_valid_hour_count bigint,
    best_station_ecwt_f numeric,
    fixed_coverage_ratio numeric,
    fixed_valid_djf_hours bigint,
    fixed_expected_djf_hours bigint,
    fixed_loaded_station_year_count integer,
    first_loaded_year integer,
    last_loaded_year integer,
    normalized_active_first_utc timestamptz,
    normalized_active_last_utc timestamptz,
    normalized_expected_djf_hours bigint,
    normalized_valid_djf_hours bigint,
    normalized_missing_djf_hours bigint,
    normalized_overfilled_hour_count bigint,
    normalized_djf_year_count integer,
    normalized_loaded_station_year_count integer,
    normalized_coverage_ratio numeric,
    normalized_loaded_year_ratio numeric,
    valid_hour_gap_to_threshold bigint,
    coverage_ratio_gap_to_threshold numeric,
    notes text,
    created_at_utc timestamptz not null default now(),
    unique (priority_run_id, plant_id)
);
create index if not exists ix_coverage_blocker_priority_run_bucket
    on calc.coverage_blocker_priority (priority_run_id, priority_bucket, priority_rank);
create index if not exists ix_coverage_blocker_priority_station
    on calc.coverage_blocker_priority (priority_run_id, best_station_id);
create index if not exists ix_coverage_blocker_priority_state
    on calc.coverage_blocker_priority (priority_run_id, plant_state);

create table if not exists calc.coverage_blocker_station_summary (
    priority_run_id text not null references audit.calculation_run(calculation_run_id),
    station_id text not null references weather.station(station_id),
    station_name text,
    station_state text,
    station_country text,
    plant_count bigint not null,
    distinct_plant_states bigint not null,
    top_plant_states text,
    min_distance_km numeric,
    median_distance_km numeric,
    max_distance_km numeric,
    min_normalized_coverage_ratio numeric,
    median_normalized_coverage_ratio numeric,
    max_normalized_coverage_ratio numeric,
    total_valid_hour_gap_to_threshold bigint,
    gap_le_24h_count bigint,
    gap_le_168h_count bigint,
    gap_le_720h_count bigint,
    gap_le_2160h_count bigint,
    gap_gt_2160h_count bigint,
    created_at_utc timestamptz not null default now(),
    primary key (priority_run_id, station_id)
);

create table if not exists calc.coverage_blocker_state_summary (
    priority_run_id text not null references audit.calculation_run(calculation_run_id),
    plant_state text not null,
    plant_count bigint not null,
    distinct_station_count bigint not null,
    total_first_operable_nameplate_mw numeric,
    min_normalized_coverage_ratio numeric,
    median_normalized_coverage_ratio numeric,
    max_normalized_coverage_ratio numeric,
    total_valid_hour_gap_to_threshold bigint,
    gap_le_24h_count bigint,
    gap_le_168h_count bigint,
    gap_le_720h_count bigint,
    gap_le_2160h_count bigint,
    gap_gt_2160h_count bigint,
    top_station_ids text,
    created_at_utc timestamptz not null default now(),
    primary key (priority_run_id, plant_state)
);

insert into audit.source_file (
    source_file_id, source_family, source_url, local_path, file_name, size_bytes,
    sha256, retrieved_at_utc, source_year, source_release, notes
) values (
    {sql_literal(diagnostic_source["source_file_id"])},
    {sql_literal(diagnostic_source["source_family"])},
    null,
    {sql_literal(diagnostic_source["local_path"])},
    {sql_literal(diagnostic_source["file_name"])},
    {diagnostic_source["size_bytes"]},
    {sql_literal(diagnostic_source["sha256"])},
    {sql_literal(diagnostic_source["retrieved_at_utc"])},
    null,
    {sql_literal(diagnostic_source["source_release"])},
    {sql_literal(diagnostic_source["notes"])}
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
    'Prioritized remaining normalized active-window ECWT coverage blockers.'
)
on conflict (calculation_run_id) do update set
    run_finished_at_utc = excluded.run_finished_at_utc,
    run_status = excluded.run_status,
    parameters_json = excluded.parameters_json,
    notes = excluded.notes;

{temp_table_sql("tmp_coverage_blocker_priority", PRIORITY_FIELDS)}
{copy_sql("tmp_coverage_blocker_priority", PRIORITY_FIELDS, priority_csv)}
{temp_table_sql("tmp_coverage_blocker_station_summary", STATION_SUMMARY_FIELDS)}
{copy_sql("tmp_coverage_blocker_station_summary", STATION_SUMMARY_FIELDS, station_summary_csv)}
{temp_table_sql("tmp_coverage_blocker_state_summary", STATE_SUMMARY_FIELDS)}
{copy_sql("tmp_coverage_blocker_state_summary", STATE_SUMMARY_FIELDS, state_summary_csv)}

delete from calc.coverage_blocker_station_summary where priority_run_id = {sql_literal(run_id)};
delete from calc.coverage_blocker_state_summary where priority_run_id = {sql_literal(run_id)};
delete from calc.coverage_blocker_priority where priority_run_id = {sql_literal(run_id)};

insert into calc.coverage_blocker_priority (
    priority_row_id,
    priority_run_id,
    diagnostic_run_id,
    plant_scope,
    coverage_policy,
    priority_rank,
    priority_bucket,
    plant_id,
    eia_plant_code,
    plant_name,
    plant_state,
    plant_county,
    nerc_region,
    balancing_authority_code,
    sector_name,
    first_operable_generator_count,
    first_operable_nameplate_mw,
    current_blocker_class,
    normalized_active_window_class,
    candidate_count,
    candidate_with_provisional_station_ecwt_count,
    normalized_active_coverage_eligible_candidate_count,
    best_station_id,
    best_station_name,
    best_station_state,
    best_station_country,
    best_distance_km,
    best_rank_order,
    best_station_ecwt_status,
    best_station_ecwt_valid_hour_count,
    best_station_ecwt_f,
    fixed_coverage_ratio,
    fixed_valid_djf_hours,
    fixed_expected_djf_hours,
    fixed_loaded_station_year_count,
    first_loaded_year,
    last_loaded_year,
    normalized_active_first_utc,
    normalized_active_last_utc,
    normalized_expected_djf_hours,
    normalized_valid_djf_hours,
    normalized_missing_djf_hours,
    normalized_overfilled_hour_count,
    normalized_djf_year_count,
    normalized_loaded_station_year_count,
    normalized_coverage_ratio,
    normalized_loaded_year_ratio,
    valid_hour_gap_to_threshold,
    coverage_ratio_gap_to_threshold,
    notes
)
select
    priority_run_id || ':plant:' || plant_id,
    priority_run_id,
    diagnostic_run_id,
    plant_scope,
    coverage_policy,
    {nullif_cast("priority_rank", "integer")},
    priority_bucket,
    plant_id,
    {text_null("eia_plant_code")},
    {text_null("plant_name")},
    {text_null("plant_state")},
    {text_null("plant_county")},
    {text_null("nerc_region")},
    {text_null("balancing_authority_code")},
    {text_null("sector_name")},
    {nullif_cast("first_operable_generator_count", "integer")},
    {nullif_cast("first_operable_nameplate_mw", "numeric")},
    {text_null("current_blocker_class")},
    {text_null("normalized_active_window_class")},
    {nullif_cast("candidate_count", "integer")},
    {nullif_cast("candidate_with_provisional_station_ecwt_count", "integer")},
    {nullif_cast("normalized_active_coverage_eligible_candidate_count", "integer")},
    {text_null("best_station_id")},
    {text_null("best_station_name")},
    {text_null("best_station_state")},
    {text_null("best_station_country")},
    {nullif_cast("best_distance_km", "numeric")},
    {nullif_cast("best_rank_order", "integer")},
    {text_null("best_station_ecwt_status")},
    {nullif_cast("best_station_ecwt_valid_hour_count", "bigint")},
    {nullif_cast("best_station_ecwt_f", "numeric")},
    {nullif_cast("fixed_coverage_ratio", "numeric")},
    {nullif_cast("fixed_valid_djf_hours", "bigint")},
    {nullif_cast("fixed_expected_djf_hours", "bigint")},
    {nullif_cast("fixed_loaded_station_year_count", "integer")},
    {nullif_cast("first_loaded_year", "integer")},
    {nullif_cast("last_loaded_year", "integer")},
    nullif(normalized_active_first_utc, '')::timestamptz,
    nullif(normalized_active_last_utc, '')::timestamptz,
    {nullif_cast("normalized_expected_djf_hours", "bigint")},
    {nullif_cast("normalized_valid_djf_hours", "bigint")},
    {nullif_cast("normalized_missing_djf_hours", "bigint")},
    {nullif_cast("normalized_overfilled_hour_count", "bigint")},
    {nullif_cast("normalized_djf_year_count", "integer")},
    {nullif_cast("normalized_loaded_station_year_count", "integer")},
    {nullif_cast("normalized_coverage_ratio", "numeric")},
    {nullif_cast("normalized_loaded_year_ratio", "numeric")},
    {nullif_cast("valid_hour_gap_to_threshold", "bigint")},
    {nullif_cast("coverage_ratio_gap_to_threshold", "numeric")},
    {text_null("notes")}
from tmp_coverage_blocker_priority;

insert into calc.coverage_blocker_station_summary (
    priority_run_id,
    station_id,
    station_name,
    station_state,
    station_country,
    plant_count,
    distinct_plant_states,
    top_plant_states,
    min_distance_km,
    median_distance_km,
    max_distance_km,
    min_normalized_coverage_ratio,
    median_normalized_coverage_ratio,
    max_normalized_coverage_ratio,
    total_valid_hour_gap_to_threshold,
    gap_le_24h_count,
    gap_le_168h_count,
    gap_le_720h_count,
    gap_le_2160h_count,
    gap_gt_2160h_count
)
select
    priority_run_id,
    station_id,
    {text_null("station_name")},
    {text_null("station_state")},
    {text_null("station_country")},
    {nullif_cast("plant_count", "bigint")},
    {nullif_cast("distinct_plant_states", "bigint")},
    {text_null("top_plant_states")},
    {nullif_cast("min_distance_km", "numeric")},
    {nullif_cast("median_distance_km", "numeric")},
    {nullif_cast("max_distance_km", "numeric")},
    {nullif_cast("min_normalized_coverage_ratio", "numeric")},
    {nullif_cast("median_normalized_coverage_ratio", "numeric")},
    {nullif_cast("max_normalized_coverage_ratio", "numeric")},
    {nullif_cast("total_valid_hour_gap_to_threshold", "bigint")},
    {nullif_cast("gap_le_24h_count", "bigint")},
    {nullif_cast("gap_le_168h_count", "bigint")},
    {nullif_cast("gap_le_720h_count", "bigint")},
    {nullif_cast("gap_le_2160h_count", "bigint")},
    {nullif_cast("gap_gt_2160h_count", "bigint")}
from tmp_coverage_blocker_station_summary;

insert into calc.coverage_blocker_state_summary (
    priority_run_id,
    plant_state,
    plant_count,
    distinct_station_count,
    total_first_operable_nameplate_mw,
    min_normalized_coverage_ratio,
    median_normalized_coverage_ratio,
    max_normalized_coverage_ratio,
    total_valid_hour_gap_to_threshold,
    gap_le_24h_count,
    gap_le_168h_count,
    gap_le_720h_count,
    gap_le_2160h_count,
    gap_gt_2160h_count,
    top_station_ids
)
select
    priority_run_id,
    plant_state,
    {nullif_cast("plant_count", "bigint")},
    {nullif_cast("distinct_station_count", "bigint")},
    {nullif_cast("total_first_operable_nameplate_mw", "numeric")},
    {nullif_cast("min_normalized_coverage_ratio", "numeric")},
    {nullif_cast("median_normalized_coverage_ratio", "numeric")},
    {nullif_cast("max_normalized_coverage_ratio", "numeric")},
    {nullif_cast("total_valid_hour_gap_to_threshold", "bigint")},
    {nullif_cast("gap_le_24h_count", "bigint")},
    {nullif_cast("gap_le_168h_count", "bigint")},
    {nullif_cast("gap_le_720h_count", "bigint")},
    {nullif_cast("gap_le_2160h_count", "bigint")},
    {nullif_cast("gap_gt_2160h_count", "bigint")},
    {text_null("top_station_ids")}
from tmp_coverage_blocker_state_summary;

commit;
"""


def md_table(rows: list[dict[str, object]], fields: list[str], headers: list[str], limit: int | None = None) -> list[str]:
    shown = rows if limit is None else rows[:limit]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in shown:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("|", "\\|") for field in fields) + " |")
    if limit is not None and len(rows) > limit:
        lines.append("| ... | " + f"{len(rows) - limit} more rows omitted" + " |" * (len(fields) - 1))
    return lines


def render_report(
    path: Path,
    run_id: str,
    code_commit: str,
    diagnostic_csv: Path,
    priority_csv: Path,
    station_summary_csv: Path,
    state_summary_csv: Path,
    rows: list[dict[str, object]],
    station_summary: list[dict[str, object]],
    state_summary: list[dict[str, object]],
    min_coverage_ratio: float,
    db_counts: OrderedDict[str, str],
) -> None:
    buckets = bucket_counts(rows)
    bucket_rows = [
        {"bucket": bucket, "rows": f"{buckets[bucket]:,}"}
        for bucket in ["gap_le_24h", "gap_le_168h", "gap_le_720h", "gap_le_2160h", "gap_gt_2160h", "missing_station_metric"]
        if buckets[bucket]
    ]
    top_priority = [
        {
            "priority_rank": row["priority_rank"],
            "plant": row["plant_name"],
            "state": row["plant_state"],
            "station": row["best_station_id"],
            "ratio": row["normalized_coverage_ratio"],
            "gap_hours": row["valid_hour_gap_to_threshold"],
            "distance": row["best_distance_km"],
            "rank": row["best_rank_order"],
        }
        for row in rows[:20]
    ]
    lines = [
        "# Normalized Active-Window Coverage Blocker Priority",
        "",
        f"Generated UTC: {utc_now().isoformat(timespec='seconds')}",
        "",
        "## Run",
        "",
        f"- Priority run ID: `{run_id}`",
        f"- Methodology version: `{METHODOLOGY_VERSION}`",
        f"- Code commit: `{code_commit}`",
        f"- Source diagnostic CSV: `{diagnostic_csv.name}`",
        f"- Detail CSV: `{priority_csv.name}`",
        f"- Station summary CSV: `{station_summary_csv.name}`",
        f"- State summary CSV: `{state_summary_csv.name}`",
        f"- Normalized active-window coverage threshold: `{min_coverage_ratio}`",
        "",
        "## Loaded DB Counts",
        "",
    ]
    lines.extend(md_table([{"check": key, "rows": value} for key, value in db_counts.items()], ["check", "rows"], ["Check", "Rows"]))
    lines.extend(["", "## Gap Buckets", ""])
    lines.extend(md_table(bucket_rows, ["bucket", "rows"], ["Bucket", "Rows"]))
    lines.extend(["", "## Top Plant States", ""])
    lines.extend(
        md_table(
            state_summary,
            [
                "plant_state",
                "plant_count",
                "distinct_station_count",
                "median_normalized_coverage_ratio",
                "total_valid_hour_gap_to_threshold",
                "gap_le_168h_count",
            ],
            ["State", "Plants", "Stations", "Median Ratio", "Total Gap Hours", "Gap <= 168h"],
            limit=20,
        )
    )
    lines.extend(["", "## Top Shared Stations", ""])
    lines.extend(
        md_table(
            station_summary,
            [
                "station_id",
                "station_name",
                "station_country",
                "plant_count",
                "median_normalized_coverage_ratio",
                "total_valid_hour_gap_to_threshold",
                "top_plant_states",
            ],
            ["Station", "Name", "Country", "Plants", "Median Ratio", "Total Gap Hours", "Top States"],
            limit=20,
        )
    )
    lines.extend(["", "## First 20 Priority Rows", ""])
    lines.extend(
        md_table(
            top_priority,
            ["priority_rank", "plant", "state", "station", "ratio", "gap_hours", "distance", "rank"],
            ["Rank", "Plant", "State", "Station", "Ratio", "Gap Hours", "Distance km", "Station Rank"],
        )
    )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- This is a priority queue for the remaining first-operable plants that still fail the conservative normalized active-window coverage screen.",
            "- `valid_hour_gap_to_threshold` is the additional valid DJF-hour count needed for the best normalized-active candidate station to reach the configured coverage threshold.",
            "- Small gaps are likely the cheapest rows to audit first, but a small gap is not proof that a station assignment is publishable.",
            "- The NOAA AWS backfill queue is already exhausted under the corrected manifest; this artifact is for coverage/methodology triage, not blind bulk download.",
            "- The table does not change readiness or release status.",
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
    parser.add_argument("--diagnostic-csv", type=Path)
    parser.add_argument("--plant-scope", default=DEFAULT_PLANT_SCOPE)
    parser.add_argument("--min-coverage-ratio", type=float, default=0.95)
    args = parser.parse_args()

    docs_dir = args.project_root / "docs"
    diagnostic_csv = args.diagnostic_csv or latest_file(
        docs_dir, "fixed_period_denominator_diagnostic_first-operable_*.csv"
    )
    diagnostic_run_id = diagnostic_csv.stem
    run_id = f"normalized_active_window_blocker_priority_{utc_now().strftime('%Y%m%dT%H%M%SZ')}"
    code_commit = git_commit_label(args.project_root)
    started_at = utc_now().isoformat(timespec="seconds")
    diagnostic_source = source_row(diagnostic_csv, run_id)

    diagnostic_rows = read_csv(diagnostic_csv)
    priority_rows = build_priority_rows(
        diagnostic_rows, run_id, diagnostic_run_id, args.plant_scope, args.min_coverage_ratio
    )
    station_summary = build_station_summary(priority_rows, run_id)
    state_summary = build_state_summary(priority_rows, run_id)

    priority_csv = docs_dir / f"{run_id}_plants.csv"
    station_summary_csv = docs_dir / f"{run_id}_stations.csv"
    state_summary_csv = docs_dir / f"{run_id}_states.csv"
    write_csv(priority_csv, PRIORITY_FIELDS, priority_rows)
    write_csv(station_summary_csv, STATION_SUMMARY_FIELDS, station_summary)
    write_csv(state_summary_csv, STATE_SUMMARY_FIELDS, state_summary)

    params = {
        "diagnostic_csv": str(diagnostic_csv),
        "diagnostic_run_id": diagnostic_run_id,
        "diagnostic_source_file_id": diagnostic_source["source_file_id"],
        "diagnostic_sha256": diagnostic_source["sha256"],
        "plant_scope": args.plant_scope,
        "coverage_policy": COVERAGE_POLICY,
        "target_class": TARGET_CLASS,
        "min_coverage_ratio": args.min_coverage_ratio,
        "priority_rows": len(priority_rows),
        "station_summary_rows": len(station_summary),
        "state_summary_rows": len(state_summary),
    }
    sql = build_load_sql(
        run_id,
        code_commit,
        started_at,
        params,
        diagnostic_source,
        priority_csv,
        station_summary_csv,
        state_summary_csv,
    )
    run(psql_cmd(args.psql, args.host, args.port, args.dbname, args.user), input_text=sql)

    db_counts = OrderedDict(
        [
            (
                "calc.coverage_blocker_priority",
                psql_scalar(
                    args.psql,
                    args.host,
                    args.port,
                    args.dbname,
                    args.user,
                    f"select count(*) from calc.coverage_blocker_priority where priority_run_id = {sql_literal(run_id)};",
                ),
            ),
            (
                "calc.coverage_blocker_station_summary",
                psql_scalar(
                    args.psql,
                    args.host,
                    args.port,
                    args.dbname,
                    args.user,
                    f"select count(*) from calc.coverage_blocker_station_summary where priority_run_id = {sql_literal(run_id)};",
                ),
            ),
            (
                "calc.coverage_blocker_state_summary",
                psql_scalar(
                    args.psql,
                    args.host,
                    args.port,
                    args.dbname,
                    args.user,
                    f"select count(*) from calc.coverage_blocker_state_summary where priority_run_id = {sql_literal(run_id)};",
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
                    f"where source_file_id = {sql_literal(diagnostic_source['source_file_id'])};",
                ),
            ),
        ]
    )
    report_path = docs_dir / f"{run_id}_report.md"
    render_report(
        report_path,
        run_id,
        code_commit,
        diagnostic_csv,
        priority_csv,
        station_summary_csv,
        state_summary_csv,
        priority_rows,
        station_summary,
        state_summary,
        args.min_coverage_ratio,
        db_counts,
    )
    print(
        json.dumps(
            OrderedDict(
                [
                    ("run_id", run_id),
                    ("diagnostic_csv", str(diagnostic_csv)),
                    ("priority_rows", len(priority_rows)),
                    ("station_summary_rows", len(station_summary)),
                    ("state_summary_rows", len(state_summary)),
                    ("db_counts", db_counts),
                    ("priority_csv", str(priority_csv)),
                    ("station_summary_csv", str(station_summary_csv)),
                    ("state_summary_csv", str(state_summary_csv)),
                    ("report_path", str(report_path)),
                ]
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
