#!/usr/bin/env python3
"""Build the plant-level exception review for the latest ECWT policy result."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import subprocess
from collections import Counter, OrderedDict, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from eop012_config import PROJECT_ROOT, PSQL


METHODOLOGY_VERSION = "eop012-ecwt-method-v0.1.0"
MIN_COVERAGE_RATIO = 0.95

REVIEW_FIELDS = [
    "exception_review_run_id",
    "policy_result_run_id",
    "plant_scope",
    "policy_id",
    "plant_id",
    "eia_plant_code",
    "plant_name",
    "plant_state",
    "plant_county",
    "utility_id",
    "utility_name",
    "sector_name",
    "nerc_region",
    "balancing_authority_code",
    "latitude",
    "longitude",
    "coordinate_status",
    "readiness_status",
    "reason_code",
    "resolution_category",
    "recommended_next_action",
    "station_candidate_rows",
    "distinct_candidate_stations",
    "selected_station_id",
    "selected_station_name",
    "selected_station_state",
    "selected_station_country",
    "selected_station_distance_km",
    "selected_station_rank_order",
    "ecwt_f",
    "valid_hour_count",
    "expected_hour_count",
    "required_valid_hour_count",
    "valid_hour_gap_to_threshold",
    "coverage_ratio",
    "coverage_ratio_gap_to_threshold",
    "fixed_coverage_ratio",
    "fixed_loaded_station_year_count",
    "station_coverage_year_count",
    "station_complete_year_count",
    "station_partial_year_count",
    "station_empty_year_count",
    "station_first_loaded_year",
    "station_last_loaded_year",
    "station_valid_djf_hours",
    "station_expected_djf_hours",
    "latest_downloaded_station_year_count",
    "latest_missing_on_aws_station_year_count",
    "latest_retryable_failure_station_year_count",
    "notes",
]

STATION_FIELDS = [
    "exception_review_run_id",
    "selected_station_id",
    "selected_station_name",
    "selected_station_state",
    "selected_station_country",
    "blocked_plant_count",
    "plant_states",
    "min_coverage_ratio",
    "median_coverage_ratio",
    "max_coverage_ratio",
    "total_valid_hour_gap_to_threshold",
    "max_valid_hour_gap_to_threshold",
    "latest_retryable_failure_station_year_count",
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
    return list(csv.DictReader(io.StringIO(result.stdout)))


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
    if not values:
        return None
    ordered = sorted(values)
    mid = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[mid]
    return (ordered[mid - 1] + ordered[mid]) / 2


def latest_policy_result_run_id(psql: Path, host: str, port: int, dbname: str, user: str | None) -> str:
    run_id = psql_scalar(
        psql,
        host,
        port,
        dbname,
        user,
        """
        select calculation_run_id
        from audit.calculation_run
        where calculation_run_id like 'plant_ecwt_policy_result_%'
          and run_status = 'succeeded'
        order by run_started_at_utc desc
        limit 1
        """,
    )
    if not run_id:
        raise RuntimeError("No succeeded plant_ecwt_policy_result run found.")
    return run_id


def fetch_blocked_rows(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    policy_result_run_id: str,
) -> list[dict[str, str]]:
    return psql_csv_query(
        psql,
        host,
        port,
        dbname,
        user,
        f"""
        with candidate_counts as (
            select
                plant_id,
                count(*)::text as station_candidate_rows,
                count(distinct station_id)::text as distinct_candidate_stations
            from link.station_candidate
            group by plant_id
        ),
        station_coverage as (
            select
                station_id,
                count(*)::text as station_coverage_year_count,
                count(*) filter (where coverage_status = 'complete')::text as station_complete_year_count,
                count(*) filter (where coverage_status = 'partial')::text as station_partial_year_count,
                count(*) filter (where coverage_status = 'empty')::text as station_empty_year_count,
                min(source_year)::text as station_first_loaded_year,
                max(source_year)::text as station_last_loaded_year,
                coalesce(sum(valid_djf_hours), 0)::text as station_valid_djf_hours,
                coalesce(sum(expected_djf_hours), 0)::text as station_expected_djf_hours
            from weather.station_year_djf_coverage_current
            group by station_id
        ),
        ranked_attempts as (
            select
                station_id,
                source_year,
                raw_station_id,
                download_status,
                http_status,
                row_number() over (
                    partition by station_id, source_year, raw_station_id
                    order by attempted_at_utc desc, created_at_utc desc
                ) as rn
            from weather.noaa_raw_download_attempt
        ),
        latest_attempts as (
            select *
            from ranked_attempts
            where rn = 1
        ),
        download_summary as (
            select
                station_id,
                count(*) filter (where download_status in ('downloaded', 'skipped_existing'))::text
                    as latest_downloaded_station_year_count,
                count(*) filter (where download_status = 'missing_on_aws')::text
                    as latest_missing_on_aws_station_year_count,
                count(*) filter (where download_status in ('failed_http', 'failed_exception'))::text
                    as latest_retryable_failure_station_year_count
            from latest_attempts
            group by station_id
        )
        select
            r.policy_result_run_id,
            r.plant_scope,
            r.policy_id,
            r.plant_id,
            r.eia_plant_code,
            r.plant_name,
            r.plant_state,
            r.plant_county,
            p.utility_id::text as utility_id,
            p.utility_name,
            r.sector_name,
            p.nerc_region,
            p.balancing_authority_code,
            p.latitude::text as latitude,
            p.longitude::text as longitude,
            r.readiness_status,
            r.reason_code,
            coalesce(cc.station_candidate_rows, '0') as station_candidate_rows,
            coalesce(cc.distinct_candidate_stations, '0') as distinct_candidate_stations,
            r.selected_station_id,
            r.selected_station_name,
            r.selected_station_state,
            r.selected_station_country,
            r.selected_station_distance_km::text as selected_station_distance_km,
            r.selected_station_rank_order::text as selected_station_rank_order,
            r.ecwt_f::text as ecwt_f,
            r.valid_hour_count::text as valid_hour_count,
            r.expected_hour_count::text as expected_hour_count,
            r.coverage_ratio::text as coverage_ratio,
            r.fixed_coverage_ratio::text as fixed_coverage_ratio,
            r.fixed_loaded_station_year_count::text as fixed_loaded_station_year_count,
            coalesce(sc.station_coverage_year_count, '0') as station_coverage_year_count,
            coalesce(sc.station_complete_year_count, '0') as station_complete_year_count,
            coalesce(sc.station_partial_year_count, '0') as station_partial_year_count,
            coalesce(sc.station_empty_year_count, '0') as station_empty_year_count,
            sc.station_first_loaded_year,
            sc.station_last_loaded_year,
            coalesce(sc.station_valid_djf_hours, '0') as station_valid_djf_hours,
            coalesce(sc.station_expected_djf_hours, '0') as station_expected_djf_hours,
            coalesce(ds.latest_downloaded_station_year_count, '0') as latest_downloaded_station_year_count,
            coalesce(ds.latest_missing_on_aws_station_year_count, '0') as latest_missing_on_aws_station_year_count,
            coalesce(ds.latest_retryable_failure_station_year_count, '0') as latest_retryable_failure_station_year_count
        from calc.plant_ecwt_policy_result r
        join asset.plant p using (plant_id)
        left join candidate_counts cc using (plant_id)
        left join station_coverage sc
          on sc.station_id = r.selected_station_id
        left join download_summary ds
          on ds.station_id = r.selected_station_id
        where r.policy_result_run_id = {sql_literal(policy_result_run_id)}
          and r.readiness_status = 'blocked'
        order by r.reason_code, r.plant_state, r.eia_plant_code
        """,
    )


def coordinate_status(row: dict[str, str]) -> str:
    if not row.get("latitude") or not row.get("longitude"):
        return "missing_coordinates"
    return "has_coordinates"


def classify(row: dict[str, str]) -> tuple[str, str, str]:
    reason = row.get("reason_code", "")
    coords = coordinate_status(row)
    if reason == "no_station_candidates" and coords == "missing_coordinates":
        return (
            "plant_geocode_required",
            "Resolve EIA plant coordinates or approve a non-locatable/unsited plant exception before station matching.",
            "Plant has no coordinates and no generated station-candidate rows.",
        )
    if reason == "no_station_candidates":
        return (
            "station_candidate_generation_required",
            "Re-run or review station-candidate generation for this located plant.",
            "Plant has coordinates but no selected candidate station under the current run.",
        )
    if reason == "normalized_active_window_coverage_below_threshold":
        return (
            "coverage_threshold_exception_review",
            "Review station selection, station-year coverage gaps, or approve a documented coverage-threshold exception.",
            "Best normalized active-window candidate remains below the 0.95 coverage threshold.",
        )
    return (
        "manual_exception_review",
        "Review the blocker and assign a manual resolution path.",
        "Unhandled policy blocker class.",
    )


def build_review_rows(rows: list[dict[str, str]], run_id: str, min_coverage_ratio: float) -> list[dict[str, object]]:
    review_rows: list[dict[str, object]] = []
    for row in rows:
        valid = to_int(row.get("valid_hour_count"))
        expected = to_int(row.get("expected_hour_count"))
        coverage = to_float(row.get("coverage_ratio"))
        required: int | None = None
        valid_gap: int | None = None
        ratio_gap: float | None = None
        if expected is not None and expected > 0:
            required = math.ceil(expected * min_coverage_ratio)
        if required is not None and valid is not None:
            valid_gap = max(required - valid, 0)
        if coverage is not None:
            ratio_gap = max(min_coverage_ratio - coverage, 0.0)
        category, action, note = classify(row)
        review_rows.append(
            {
                "exception_review_run_id": run_id,
                "policy_result_run_id": row.get("policy_result_run_id", ""),
                "plant_scope": row.get("plant_scope", ""),
                "policy_id": row.get("policy_id", ""),
                "plant_id": row.get("plant_id", ""),
                "eia_plant_code": row.get("eia_plant_code", ""),
                "plant_name": row.get("plant_name", ""),
                "plant_state": row.get("plant_state", ""),
                "plant_county": row.get("plant_county", ""),
                "utility_id": row.get("utility_id", ""),
                "utility_name": row.get("utility_name", ""),
                "sector_name": row.get("sector_name", ""),
                "nerc_region": row.get("nerc_region", ""),
                "balancing_authority_code": row.get("balancing_authority_code", ""),
                "latitude": row.get("latitude", ""),
                "longitude": row.get("longitude", ""),
                "coordinate_status": coordinate_status(row),
                "readiness_status": row.get("readiness_status", ""),
                "reason_code": row.get("reason_code", ""),
                "resolution_category": category,
                "recommended_next_action": action,
                "station_candidate_rows": row.get("station_candidate_rows", "0"),
                "distinct_candidate_stations": row.get("distinct_candidate_stations", "0"),
                "selected_station_id": row.get("selected_station_id", ""),
                "selected_station_name": row.get("selected_station_name", ""),
                "selected_station_state": row.get("selected_station_state", ""),
                "selected_station_country": row.get("selected_station_country", ""),
                "selected_station_distance_km": row.get("selected_station_distance_km", ""),
                "selected_station_rank_order": row.get("selected_station_rank_order", ""),
                "ecwt_f": row.get("ecwt_f", ""),
                "valid_hour_count": row.get("valid_hour_count", ""),
                "expected_hour_count": row.get("expected_hour_count", ""),
                "required_valid_hour_count": "" if required is None else required,
                "valid_hour_gap_to_threshold": "" if valid_gap is None else valid_gap,
                "coverage_ratio": row.get("coverage_ratio", ""),
                "coverage_ratio_gap_to_threshold": fmt_float(ratio_gap),
                "fixed_coverage_ratio": row.get("fixed_coverage_ratio", ""),
                "fixed_loaded_station_year_count": row.get("fixed_loaded_station_year_count", ""),
                "station_coverage_year_count": row.get("station_coverage_year_count", "0"),
                "station_complete_year_count": row.get("station_complete_year_count", "0"),
                "station_partial_year_count": row.get("station_partial_year_count", "0"),
                "station_empty_year_count": row.get("station_empty_year_count", "0"),
                "station_first_loaded_year": row.get("station_first_loaded_year", ""),
                "station_last_loaded_year": row.get("station_last_loaded_year", ""),
                "station_valid_djf_hours": row.get("station_valid_djf_hours", "0"),
                "station_expected_djf_hours": row.get("station_expected_djf_hours", "0"),
                "latest_downloaded_station_year_count": row.get("latest_downloaded_station_year_count", "0"),
                "latest_missing_on_aws_station_year_count": row.get("latest_missing_on_aws_station_year_count", "0"),
                "latest_retryable_failure_station_year_count": row.get(
                    "latest_retryable_failure_station_year_count", "0"
                ),
                "notes": note,
            }
        )
    review_rows.sort(
        key=lambda item: (
            str(item["resolution_category"]),
            str(item["plant_state"]),
            to_int(item["eia_plant_code"]) or 999999999,
        )
    )
    return review_rows


def build_station_summary(rows: list[dict[str, object]], run_id: str) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        station_id = str(row.get("selected_station_id") or "")
        if station_id:
            grouped[station_id].append(row)
    summaries: list[dict[str, object]] = []
    for station_id, group in grouped.items():
        ratios = [to_float(row.get("coverage_ratio")) for row in group]
        ratios = [value for value in ratios if value is not None]
        gaps = [to_int(row.get("valid_hour_gap_to_threshold")) for row in group]
        gaps = [value for value in gaps if value is not None]
        state_counts = Counter(str(row.get("plant_state") or "(blank)") for row in group)
        first = group[0]
        retryable = max(to_int(row.get("latest_retryable_failure_station_year_count")) or 0 for row in group)
        summaries.append(
            {
                "exception_review_run_id": run_id,
                "selected_station_id": station_id,
                "selected_station_name": first.get("selected_station_name", ""),
                "selected_station_state": first.get("selected_station_state", ""),
                "selected_station_country": first.get("selected_station_country", ""),
                "blocked_plant_count": len(group),
                "plant_states": ";".join(f"{state}:{count}" for state, count in state_counts.most_common()),
                "min_coverage_ratio": fmt_float(min(ratios), 6) if ratios else "",
                "median_coverage_ratio": fmt_float(median(ratios), 6),
                "max_coverage_ratio": fmt_float(max(ratios), 6) if ratios else "",
                "total_valid_hour_gap_to_threshold": sum(gaps),
                "max_valid_hour_gap_to_threshold": max(gaps) if gaps else "",
                "latest_retryable_failure_station_year_count": retryable,
                "notes": "Selected station for one or more remaining coverage-threshold blockers.",
            }
        )
    summaries.sort(key=lambda row: (-int(row["blocked_plant_count"]), row["selected_station_id"]))
    return summaries


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
        "notes": "Generated EOP012 plant ECWT exception review artifact.",
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


def text_null(field: str) -> str:
    return f"nullif(nullif({qident(field)}, ''), '\\N')"


def nullif_cast(field: str, cast_type: str) -> str:
    return f"nullif(nullif({qident(field)}, ''), '\\N')::{cast_type}"


def build_load_sql(
    run_id: str,
    code_commit: str,
    started_at: str,
    params: dict[str, object],
    csv_source: dict[str, object],
    review_csv: Path,
) -> str:
    return f"""
\\set ON_ERROR_STOP on
begin;

create table if not exists calc.plant_ecwt_exception_review (
    exception_review_id text primary key,
    exception_review_run_id text not null references audit.calculation_run(calculation_run_id),
    policy_result_run_id text not null references audit.calculation_run(calculation_run_id),
    plant_scope text not null,
    policy_id text not null,
    plant_id text not null references asset.plant(plant_id),
    eia_plant_code text,
    plant_name text,
    plant_state text,
    plant_county text,
    utility_id text,
    utility_name text,
    sector_name text,
    nerc_region text,
    balancing_authority_code text,
    latitude numeric,
    longitude numeric,
    coordinate_status text not null,
    readiness_status text not null,
    reason_code text not null,
    resolution_category text not null,
    recommended_next_action text not null,
    station_candidate_rows integer,
    distinct_candidate_stations integer,
    selected_station_id text references weather.station(station_id),
    selected_station_name text,
    selected_station_state text,
    selected_station_country text,
    selected_station_distance_km numeric,
    selected_station_rank_order integer,
    ecwt_f numeric,
    valid_hour_count bigint,
    expected_hour_count bigint,
    required_valid_hour_count bigint,
    valid_hour_gap_to_threshold bigint,
    coverage_ratio numeric,
    coverage_ratio_gap_to_threshold numeric,
    fixed_coverage_ratio numeric,
    fixed_loaded_station_year_count integer,
    station_coverage_year_count integer,
    station_complete_year_count integer,
    station_partial_year_count integer,
    station_empty_year_count integer,
    station_first_loaded_year integer,
    station_last_loaded_year integer,
    station_valid_djf_hours bigint,
    station_expected_djf_hours bigint,
    latest_downloaded_station_year_count integer,
    latest_missing_on_aws_station_year_count integer,
    latest_retryable_failure_station_year_count integer,
    notes text,
    created_at_utc timestamptz not null default now(),
    unique (exception_review_run_id, plant_id)
);
create index if not exists ix_plant_ecwt_exception_review_run_category
    on calc.plant_ecwt_exception_review (exception_review_run_id, resolution_category);
create index if not exists ix_plant_ecwt_exception_review_reason
    on calc.plant_ecwt_exception_review (exception_review_run_id, reason_code);
create index if not exists ix_plant_ecwt_exception_review_station
    on calc.plant_ecwt_exception_review (exception_review_run_id, selected_station_id);

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
    'Initial auditable methodology version for asset loading, station matching, raw file inventory, backfill planning, download attempts, coverage auditing, ECWT calculation, policy materialization, and exception review.'
)
on conflict (methodology_version) do update set notes = excluded.notes;

insert into audit.source_file (
    source_file_id, source_family, source_url, local_path, file_name, size_bytes,
    sha256, retrieved_at_utc, source_year, source_release, notes
) values (
    {sql_literal(csv_source["source_file_id"])},
    {sql_literal(csv_source["source_family"])},
    null,
    {sql_literal(csv_source["local_path"])},
    {sql_literal(csv_source["file_name"])},
    {csv_source["size_bytes"]},
    {sql_literal(csv_source["sha256"])},
    {sql_literal(csv_source["retrieved_at_utc"])},
    null,
    {sql_literal(csv_source["source_release"])},
    {sql_literal(csv_source["notes"])}
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
    'Built plant-level exception review rows for blocked ECWT policy results.'
)
on conflict (calculation_run_id) do update set
    run_finished_at_utc = excluded.run_finished_at_utc,
    run_status = excluded.run_status,
    parameters_json = excluded.parameters_json,
    notes = excluded.notes;

{temp_table_sql("tmp_exception_review", REVIEW_FIELDS)}
{copy_sql("tmp_exception_review", REVIEW_FIELDS, review_csv)}

delete from calc.plant_ecwt_exception_review
where exception_review_run_id = {sql_literal(run_id)};

insert into calc.plant_ecwt_exception_review (
    exception_review_id,
    exception_review_run_id,
    policy_result_run_id,
    plant_scope,
    policy_id,
    plant_id,
    eia_plant_code,
    plant_name,
    plant_state,
    plant_county,
    utility_id,
    utility_name,
    sector_name,
    nerc_region,
    balancing_authority_code,
    latitude,
    longitude,
    coordinate_status,
    readiness_status,
    reason_code,
    resolution_category,
    recommended_next_action,
    station_candidate_rows,
    distinct_candidate_stations,
    selected_station_id,
    selected_station_name,
    selected_station_state,
    selected_station_country,
    selected_station_distance_km,
    selected_station_rank_order,
    ecwt_f,
    valid_hour_count,
    expected_hour_count,
    required_valid_hour_count,
    valid_hour_gap_to_threshold,
    coverage_ratio,
    coverage_ratio_gap_to_threshold,
    fixed_coverage_ratio,
    fixed_loaded_station_year_count,
    station_coverage_year_count,
    station_complete_year_count,
    station_partial_year_count,
    station_empty_year_count,
    station_first_loaded_year,
    station_last_loaded_year,
    station_valid_djf_hours,
    station_expected_djf_hours,
    latest_downloaded_station_year_count,
    latest_missing_on_aws_station_year_count,
    latest_retryable_failure_station_year_count,
    notes
)
select
    {sql_literal(run_id)} || ':plant:' || plant_id,
    exception_review_run_id,
    policy_result_run_id,
    plant_scope,
    policy_id,
    plant_id,
    {text_null("eia_plant_code")},
    {text_null("plant_name")},
    {text_null("plant_state")},
    {text_null("plant_county")},
    {text_null("utility_id")},
    {text_null("utility_name")},
    {text_null("sector_name")},
    {text_null("nerc_region")},
    {text_null("balancing_authority_code")},
    {nullif_cast("latitude", "numeric")},
    {nullif_cast("longitude", "numeric")},
    coordinate_status,
    readiness_status,
    reason_code,
    resolution_category,
    recommended_next_action,
    {nullif_cast("station_candidate_rows", "integer")},
    {nullif_cast("distinct_candidate_stations", "integer")},
    {text_null("selected_station_id")},
    {text_null("selected_station_name")},
    {text_null("selected_station_state")},
    {text_null("selected_station_country")},
    {nullif_cast("selected_station_distance_km", "numeric")},
    {nullif_cast("selected_station_rank_order", "integer")},
    {nullif_cast("ecwt_f", "numeric")},
    {nullif_cast("valid_hour_count", "bigint")},
    {nullif_cast("expected_hour_count", "bigint")},
    {nullif_cast("required_valid_hour_count", "bigint")},
    {nullif_cast("valid_hour_gap_to_threshold", "bigint")},
    {nullif_cast("coverage_ratio", "numeric")},
    {nullif_cast("coverage_ratio_gap_to_threshold", "numeric")},
    {nullif_cast("fixed_coverage_ratio", "numeric")},
    {nullif_cast("fixed_loaded_station_year_count", "integer")},
    {nullif_cast("station_coverage_year_count", "integer")},
    {nullif_cast("station_complete_year_count", "integer")},
    {nullif_cast("station_partial_year_count", "integer")},
    {nullif_cast("station_empty_year_count", "integer")},
    {nullif_cast("station_first_loaded_year", "integer")},
    {nullif_cast("station_last_loaded_year", "integer")},
    {nullif_cast("station_valid_djf_hours", "bigint")},
    {nullif_cast("station_expected_djf_hours", "bigint")},
    {nullif_cast("latest_downloaded_station_year_count", "integer")},
    {nullif_cast("latest_missing_on_aws_station_year_count", "integer")},
    {nullif_cast("latest_retryable_failure_station_year_count", "integer")},
    {text_null("notes")}
from tmp_exception_review;

commit;
"""


def db_counts(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    run_id: str,
) -> OrderedDict[str, str]:
    queries = OrderedDict(
        [
            (
                "calc.plant_ecwt_exception_review",
                f"select count(*) from calc.plant_ecwt_exception_review where exception_review_run_id = {sql_literal(run_id)};",
            ),
            (
                "distinct plants",
                f"select count(distinct plant_id) from calc.plant_ecwt_exception_review where exception_review_run_id = {sql_literal(run_id)};",
            ),
            (
                "plant_geocode_required",
                f"""
                select count(*) from calc.plant_ecwt_exception_review
                where exception_review_run_id = {sql_literal(run_id)}
                  and resolution_category = 'plant_geocode_required';
                """,
            ),
            (
                "coverage_threshold_exception_review",
                f"""
                select count(*) from calc.plant_ecwt_exception_review
                where exception_review_run_id = {sql_literal(run_id)}
                  and resolution_category = 'coverage_threshold_exception_review';
                """,
            ),
        ]
    )
    return OrderedDict(
        (label, psql_scalar(psql, host, port, dbname, user, query)) for label, query in queries.items()
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
    path: Path,
    run_id: str,
    code_commit: str,
    policy_result_run_id: str,
    review_csv: Path,
    station_csv: Path,
    rows: list[dict[str, object]],
    station_rows: list[dict[str, object]],
    counts: OrderedDict[str, str],
) -> None:
    by_reason = Counter(str(row["reason_code"]) for row in rows)
    by_category = Counter(str(row["resolution_category"]) for row in rows)
    by_state = Counter(str(row.get("plant_state") or "(blank)") for row in rows)
    no_station_rows = [row for row in rows if row["resolution_category"] == "plant_geocode_required"]
    coverage_rows = [row for row in rows if row["resolution_category"] == "coverage_threshold_exception_review"]
    coverage_rows.sort(key=lambda row: to_int(row.get("valid_hour_gap_to_threshold")) or 999999999)
    lines = [
        "# Plant ECWT Exception Review",
        "",
        f"Generated UTC: {utc_now().isoformat(timespec='seconds')}",
        "",
        "## Run",
        "",
        f"- Exception review run ID: `{run_id}`",
        f"- Policy result run ID: `{policy_result_run_id}`",
        f"- Code commit: `{code_commit}`",
        f"- Review CSV: `{review_csv.name}`",
        f"- Station summary CSV: `{station_csv.name}`",
        "",
        "## Loaded DB Counts",
        "",
        "| Check | Rows |",
        "| --- | ---: |",
    ]
    for label, value in counts.items():
        lines.append(f"| `{label}` | {value} |")
    lines.extend(["", "## Resolution Categories", ""])
    render_table(
        lines,
        ["Category", "Rows"],
        [{"category": key, "rows": f"{value:,}"} for key, value in by_category.most_common()],
        ["category", "rows"],
    )
    lines.extend(["", "## Reason Codes", ""])
    render_table(
        lines,
        ["Reason", "Rows"],
        [{"reason": key, "rows": f"{value:,}"} for key, value in by_reason.most_common()],
        ["reason", "rows"],
    )
    lines.extend(["", "## Blocked Rows By State", ""])
    render_table(
        lines,
        ["State", "Rows"],
        [{"state": key, "rows": f"{value:,}"} for key, value in by_state.most_common()],
        ["state", "rows"],
    )
    lines.extend(["", "## Coverage Stations", ""])
    render_table(
        lines,
        ["Station", "Name", "Plants", "Median Coverage", "Total Gap Hours", "Retryable Failures"],
        station_rows,
        [
            "selected_station_id",
            "selected_station_name",
            "blocked_plant_count",
            "median_coverage_ratio",
            "total_valid_hour_gap_to_threshold",
            "latest_retryable_failure_station_year_count",
        ],
    )
    lines.extend(["", "## Coverage Threshold Blockers", ""])
    render_table(
        lines,
        ["Plant", "State", "Station", "Coverage", "Gap Hours", "Action"],
        coverage_rows,
        [
            "plant_name",
            "plant_state",
            "selected_station_id",
            "coverage_ratio",
            "valid_hour_gap_to_threshold",
            "recommended_next_action",
        ],
    )
    lines.extend(["", "## Geocode-Required Plants", ""])
    render_table(
        lines,
        ["Plant", "State", "EIA Plant Code", "Utility", "Action"],
        no_station_rows,
        ["plant_name", "plant_state", "eia_plant_code", "utility_name", "recommended_next_action"],
    )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `plant_geocode_required` rows cannot enter station matching because EIA plant latitude/longitude is blank.",
            "- `coverage_threshold_exception_review` rows already have candidate stations and no current retryable NOAA transport failure; the remaining issue is station selection, sparse source coverage, or policy exception treatment.",
            "- This review does not change the policy result table. It creates a separate exception table so blocked plants stay explicit and auditable.",
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
    parser.add_argument("--min-coverage-ratio", type=float, default=MIN_COVERAGE_RATIO)
    args = parser.parse_args()

    if not args.psql.exists():
        raise FileNotFoundError(args.psql)
    if args.min_coverage_ratio <= 0 or args.min_coverage_ratio > 1:
        raise ValueError("--min-coverage-ratio must be in the interval (0, 1].")

    started_at = utc_now().isoformat()
    docs_dir = args.project_root / "docs"
    policy_result_run_id = args.policy_result_run_id or latest_policy_result_run_id(
        args.psql, args.host, args.port, args.dbname, args.user
    )
    source_rows = fetch_blocked_rows(args.psql, args.host, args.port, args.dbname, args.user, policy_result_run_id)
    if not source_rows:
        raise RuntimeError(f"No blocked policy result rows found for {policy_result_run_id}.")

    run_id = f"plant_ecwt_exception_review_{utc_now().strftime('%Y%m%dT%H%M%SZ')}"
    review_rows = build_review_rows(source_rows, run_id, args.min_coverage_ratio)
    station_rows = build_station_summary(review_rows, run_id)
    code_commit = git_commit_label(args.project_root)

    review_csv = docs_dir / f"{run_id}.csv"
    station_csv = docs_dir / f"{run_id}_stations.csv"
    report_path = docs_dir / f"{run_id}_report.md"
    write_csv(review_csv, REVIEW_FIELDS, review_rows)
    write_csv(station_csv, STATION_FIELDS, station_rows)

    csv_source = source_row(review_csv, "eop012_plant_ecwt_exception_review", run_id)
    params = {
        "policy_result_run_id": policy_result_run_id,
        "review_csv": str(review_csv),
        "station_csv": str(station_csv),
        "min_coverage_ratio": args.min_coverage_ratio,
        "row_count": len(review_rows),
        "station_summary_row_count": len(station_rows),
        "review_sha256": csv_source["sha256"],
    }
    sql = build_load_sql(run_id, code_commit, started_at, params, csv_source, review_csv)
    run(psql_cmd(args.psql, args.host, args.port, args.dbname, args.user), input_text=sql)
    counts = db_counts(args.psql, args.host, args.port, args.dbname, args.user, run_id)
    render_report(report_path, run_id, code_commit, policy_result_run_id, review_csv, station_csv, review_rows, station_rows, counts)
    print(
        json.dumps(
            OrderedDict(
                [
                    ("run_id", run_id),
                    ("policy_result_run_id", policy_result_run_id),
                    ("rows", len(review_rows)),
                    ("station_rows", len(station_rows)),
                    ("db_counts", counts),
                    ("review_csv", str(review_csv)),
                    ("station_csv", str(station_csv)),
                    ("report_path", str(report_path)),
                ]
            ),
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
