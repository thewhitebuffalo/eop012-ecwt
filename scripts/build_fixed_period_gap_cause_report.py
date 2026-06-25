#!/usr/bin/env python3
"""Classify remaining fixed-period plant ECWT blockers after NOAA backfill."""

from __future__ import annotations

import argparse
import csv
import io
import json
import subprocess
from collections import Counter, OrderedDict, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from eop012_config import PROJECT_ROOT, PSQL


STATION_YEAR_FIELDS = [
    "diagnostic_run_id",
    "plant_ecwt_run_id",
    "candidate_run_id",
    "station_ecwt_run_id",
    "coverage_run_id",
    "coverage_table",
    "station_id",
    "station_name",
    "station_state",
    "station_country",
    "station_first_observation_utc",
    "station_last_observation_utc",
    "impacted_blocked_plant_count",
    "min_candidate_rank_order",
    "max_candidate_rank_order",
    "min_candidate_distance_km",
    "max_candidate_distance_km",
    "sample_blocked_plants",
    "source_year",
    "expected_djf_hours",
    "valid_djf_hours",
    "missing_djf_hours",
    "plant_weighted_missing_djf_hours",
    "coverage_ratio",
    "coverage_status",
    "loaded_file_count",
    "invalid_temp_row_count",
    "rejected_source_row_count",
    "rejected_plausibility_row_count",
    "duplicate_hour_count",
    "active_window_overlap",
    "latest_inventory_run_id",
    "latest_inventory_status",
    "latest_inventory_local_path",
    "latest_download_status",
    "latest_http_status",
    "latest_download_run_id",
    "latest_download_attempted_at_utc",
    "manifest_statuses",
    "gap_cause",
]

STATION_SUMMARY_FIELDS = [
    "diagnostic_run_id",
    "plant_ecwt_run_id",
    "station_id",
    "station_name",
    "station_state",
    "station_country",
    "station_first_observation_utc",
    "station_last_observation_utc",
    "impacted_blocked_plant_count",
    "min_candidate_rank_order",
    "min_candidate_distance_km",
    "sample_blocked_plants",
    "fixed_expected_djf_hours",
    "fixed_valid_djf_hours",
    "fixed_missing_djf_hours",
    "fixed_coverage_ratio",
    "plant_weighted_missing_djf_hours",
    "missing_station_year_count",
    "complete_loaded_year_count",
    "partial_loaded_year_count",
    "empty_loaded_year_count",
    "outside_station_metadata_window_year_count",
    "terminal_aws_missing_year_count",
    "retryable_download_failure_year_count",
    "downloaded_no_canonical_djf_year_count",
    "available_raw_not_loaded_year_count",
    "raw_inventory_missing_year_count",
    "no_download_or_manifest_evidence_year_count",
    "top_gap_years",
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


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: "" if row.get(field) is None else row.get(field, "") for field in fieldnames})


def git_commit_label(project_root: Path) -> str:
    try:
        return run(["git", "-C", str(project_root), "rev-parse", "HEAD"]).stdout.strip()
    except Exception:
        return "UNCOMMITTED_WORKTREE"


def relation_exists(psql: Path, host: str, port: int, dbname: str, user: str | None, relation_name: str) -> bool:
    exists = psql_scalar(
        psql,
        host,
        port,
        dbname,
        user,
        f"select to_regclass({sql_literal(relation_name)}) is not null;",
    )
    return exists.lower() == "t"


def coverage_row_count(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    coverage_run_id: str,
    coverage_table: str,
) -> int:
    return int(
        psql_scalar(
            psql,
            host,
            port,
            dbname,
            user,
            f"select count(*) from {coverage_table} where calculation_run_id = {sql_literal(coverage_run_id)};",
        )
        or "0"
    )


def resolve_coverage_table(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    coverage_run_id: str,
    coverage_source: str,
    preferred_table: str | None,
) -> str:
    valid_tables = {
        "weather.station_year_djf_coverage",
        "weather.station_year_djf_coverage_current",
    }
    if coverage_source == "history":
        return "weather.station_year_djf_coverage"
    if coverage_source == "current":
        return "weather.station_year_djf_coverage_current"
    if preferred_table in valid_tables and relation_exists(psql, host, port, dbname, user, preferred_table):
        if coverage_row_count(psql, host, port, dbname, user, coverage_run_id, preferred_table) > 0:
            return preferred_table
    current_table = "weather.station_year_djf_coverage_current"
    if relation_exists(psql, host, port, dbname, user, current_table) and coverage_row_count(
        psql, host, port, dbname, user, coverage_run_id, current_table
    ) > 0:
        return current_table
    return "weather.station_year_djf_coverage"


def latest_fixed_plant_ecwt_run_id(psql: Path, host: str, port: int, dbname: str, user: str | None) -> str:
    return psql_scalar(
        psql,
        host,
        port,
        dbname,
        user,
        """
        select calculation_run_id
        from audit.calculation_run
        where calculation_run_id like 'plant_ecwt_provisional_fixed_period_%'
          and run_status = 'succeeded'
        order by run_started_at_utc desc
        limit 1
        """,
    )


def latest_manifest_run_id(psql: Path, host: str, port: int, dbname: str, user: str | None) -> str:
    return psql_scalar(
        psql,
        host,
        port,
        dbname,
        user,
        """
        select calculation_run_id
        from audit.calculation_run
        where calculation_run_id like 'noaa_backfill_manifest_%'
          and run_status = 'succeeded'
        order by run_started_at_utc desc
        limit 1
        """,
    )


def fetch_json_params(psql: Path, host: str, port: int, dbname: str, user: str | None, run_id: str) -> dict[str, object]:
    raw = psql_scalar(
        psql,
        host,
        port,
        dbname,
        user,
        f"""
        select parameters_json::text
        from audit.calculation_run
        where calculation_run_id = {sql_literal(run_id)}
        """,
    )
    if not raw:
        raise RuntimeError(f"No audit.calculation_run row found for {run_id}")
    return json.loads(raw)


def to_int(value: object) -> int:
    if value in (None, ""):
        return 0
    return int(float(str(value)))


def to_float(value: object) -> float:
    if value in (None, ""):
        return 0.0
    return float(str(value))


def fmt_int(value: int | float) -> str:
    return f"{int(value):,}"


def fmt_float(value: float, digits: int = 6) -> str:
    return f"{value:.{digits}f}"


def nullable_int(value: object) -> int | None:
    if value in (None, ""):
        return None
    return int(float(str(value)))


def nullable_float(value: object) -> float | None:
    if value in (None, ""):
        return None
    return float(str(value))


def read_best_station_rows(blocker_csv: Path) -> list[dict[str, object]]:
    if not blocker_csv.exists():
        raise FileNotFoundError(blocker_csv)
    with blocker_csv.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    required = {
        "best_coverage_station_id",
        "best_coverage_distance_km",
        "best_coverage_rank_order",
        "plant_name",
        "plant_state",
        "eia_plant_code",
    }
    missing = required - set(rows[0].keys() if rows else [])
    if missing:
        raise ValueError(f"{blocker_csv} is missing required columns: {', '.join(sorted(missing))}")

    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        station_id = row.get("best_coverage_station_id") or ""
        if station_id:
            grouped[station_id].append(row)

    best_rows: list[dict[str, object]] = []
    for station_id, station_rows in grouped.items():
        ranks = [value for value in (nullable_int(row.get("best_coverage_rank_order")) for row in station_rows) if value]
        distances = [
            value for value in (nullable_float(row.get("best_coverage_distance_km")) for row in station_rows) if value is not None
        ]
        sample = sorted(
            station_rows,
            key=lambda row: (
                row.get("plant_state") or "",
                nullable_int(row.get("eia_plant_code")) or 10**12,
                row.get("plant_name") or "",
            ),
        )[:8]
        best_rows.append(
            {
                "station_id": station_id,
                "impacted_blocked_plant_count": len(station_rows),
                "min_candidate_rank_order": min(ranks) if ranks else None,
                "max_candidate_rank_order": max(ranks) if ranks else None,
                "min_candidate_distance_km": fmt_float(min(distances), 3) if distances else "",
                "max_candidate_distance_km": fmt_float(max(distances), 3) if distances else "",
                "sample_blocked_plants": " | ".join(row.get("plant_name") or "" for row in sample),
            }
        )
    best_rows.sort(key=lambda row: str(row["station_id"]))
    return best_rows


def best_station_values(best_station_rows: list[dict[str, object]]) -> str:
    if not best_station_rows:
        raise ValueError("No best station rows available for gap-cause diagnostic.")
    values = []
    for row in best_station_rows:
        values.append(
            "("
            + ", ".join(
                [
                    sql_literal(row["station_id"]),
                    str(int(row["impacted_blocked_plant_count"])),
                    "null" if row["min_candidate_rank_order"] is None else str(int(row["min_candidate_rank_order"])),
                    "null" if row["max_candidate_rank_order"] is None else str(int(row["max_candidate_rank_order"])),
                    sql_literal(row["min_candidate_distance_km"]),
                    sql_literal(row["max_candidate_distance_km"]),
                    sql_literal(row["sample_blocked_plants"]),
                ]
            )
            + ")"
        )
    return ",\n        ".join(values)


def gap_query(
    diagnostic_run_id: str,
    plant_ecwt_run_id: str,
    candidate_run_id: str,
    station_ecwt_run_id: str,
    coverage_run_id: str,
    coverage_table: str,
    fixed_min_year: int,
    fixed_max_year: int,
) -> str:
    if coverage_table not in {"weather.station_year_djf_coverage", "weather.station_year_djf_coverage_current"}:
        raise ValueError(f"Unexpected coverage table: {coverage_table}")
    return f"""
with fixed_years as (
    select generate_series({fixed_min_year}, {fixed_max_year})::integer as source_year
),
fixed_expected_by_year as (
    select
        y.source_year,
        count(*) filter (
            where extract(month from gs.hour_utc at time zone 'UTC') in (12, 1, 2)
        )::bigint as expected_djf_hours
    from fixed_years y
    cross join lateral generate_series(
        make_timestamptz(y.source_year, 1, 1, 0, 0, 0, 'UTC'),
        make_timestamptz(y.source_year, 12, 31, 23, 0, 0, 'UTC'),
        interval '1 hour'
    ) as gs(hour_utc)
    group by y.source_year
),
station_fixed_coverage as (
    select
        se.station_id,
        coalesce(sum(c.valid_djf_hours), 0)::bigint as fixed_valid_djf_hours,
        sum(e.expected_djf_hours)::bigint as fixed_expected_djf_hours,
        coalesce(sum(c.valid_djf_hours), 0)::numeric / nullif(sum(e.expected_djf_hours), 0)
            as fixed_coverage_ratio,
        count(c.*) filter (where c.loaded_file_count > 0)::integer as loaded_station_year_count
    from calc.station_ecwt se
    cross join fixed_expected_by_year e
    left join {coverage_table} c
      on c.calculation_run_id = {sql_literal(coverage_run_id)}
     and c.station_id = se.station_id
     and c.source_year = e.source_year
    where se.calculation_run_id = {sql_literal(station_ecwt_run_id)}
      and se.result_status = 'provisional'
      and se.valid_hour_count > 0
    group by se.station_id
),
blocked_plants as (
    select
        pe.plant_id,
        p.eia_plant_code,
        p.plant_name,
        p.state as plant_state
    from calc.plant_ecwt pe
    join asset.plant p using (plant_id)
    where pe.calculation_run_id = {sql_literal(plant_ecwt_run_id)}
      and pe.result_status = 'blocked'
),
candidate_eval as (
    select
        bp.plant_id,
        bp.eia_plant_code,
        bp.plant_name,
        bp.plant_state,
        sc.station_id,
        sc.distance_km,
        sc.rank_order,
        (
            se.station_ecwt_id is not null
            and se.result_status = 'provisional'
            and se.valid_hour_count > 0
        ) as has_provisional_station_ecwt,
        sf.fixed_coverage_ratio,
        sf.loaded_station_year_count,
        sf.fixed_valid_djf_hours
    from blocked_plants bp
    join link.station_candidate sc
      on sc.plant_id = bp.plant_id
    left join calc.station_ecwt se
      on se.station_id = sc.station_id
     and se.calculation_run_id = {sql_literal(station_ecwt_run_id)}
    left join station_fixed_coverage sf
      on sf.station_id = sc.station_id
    where sc.calculation_run_id = {sql_literal(candidate_run_id)}
      and sc.candidate_status = 'candidate'
),
best_candidate as (
    select *
    from (
        select
            ce.*,
            row_number() over (
                partition by ce.plant_id
                order by
                    ce.fixed_coverage_ratio desc nulls last,
                    ce.loaded_station_year_count desc nulls last,
                    ce.rank_order asc nulls last,
                    ce.distance_km asc nulls last,
                    ce.station_id
            ) as rn
        from candidate_eval ce
        where ce.has_provisional_station_ecwt
    ) ranked
    where rn = 1
),
best_station as (
    select
        station_id,
        count(*)::integer as impacted_blocked_plant_count,
        min(rank_order)::integer as min_candidate_rank_order,
        max(rank_order)::integer as max_candidate_rank_order,
        round(min(distance_km), 3)::text as min_candidate_distance_km,
        round(max(distance_km), 3)::text as max_candidate_distance_km
    from best_candidate
    group by station_id
),
station_plant_sample as (
    select
        station_id,
        string_agg(plant_name, ' | ' order by plant_state, eia_plant_code::integer nulls last, plant_name) as sample_blocked_plants
    from (
        select
            station_id,
            plant_name,
            plant_state,
            eia_plant_code,
            row_number() over (
                partition by station_id
                order by plant_state, eia_plant_code::integer nulls last, plant_name
            ) as rn
        from best_candidate
    ) sampled
    where rn <= 8
    group by station_id
),
latest_attempt as (
    select distinct on (station_id, source_year)
        station_id,
        source_year,
        download_status,
        http_status,
        calculation_run_id,
        attempted_at_utc
    from weather.noaa_raw_download_attempt
    order by station_id, source_year, attempted_at_utc desc nulls last, calculation_run_id desc
),
latest_inventory as (
    select distinct on (station_id, source_year)
        station_id,
        source_year,
        calculation_run_id,
        file_status,
        local_path
    from weather.noaa_raw_file_inventory
    order by station_id, source_year, created_at_utc desc, calculation_run_id desc
),
manifest_agg as (
    select
        station_id,
        source_year,
        string_agg(distinct manifest_status, ',' order by manifest_status) as manifest_statuses
    from weather.noaa_raw_backfill_manifest
    group by station_id, source_year
),
station_years as (
    select
        {sql_literal(diagnostic_run_id)} as diagnostic_run_id,
        {sql_literal(plant_ecwt_run_id)} as plant_ecwt_run_id,
        {sql_literal(candidate_run_id)} as candidate_run_id,
        {sql_literal(station_ecwt_run_id)} as station_ecwt_run_id,
        {sql_literal(coverage_run_id)} as coverage_run_id,
        {sql_literal(coverage_table)} as coverage_table,
        bs.station_id,
        st.station_name,
        st.state as station_state,
        st.country as station_country,
        st.first_observation_utc::text as station_first_observation_utc,
        st.last_observation_utc::text as station_last_observation_utc,
        bs.impacted_blocked_plant_count::text as impacted_blocked_plant_count,
        bs.min_candidate_rank_order::text as min_candidate_rank_order,
        bs.max_candidate_rank_order::text as max_candidate_rank_order,
        bs.min_candidate_distance_km,
        bs.max_candidate_distance_km,
        sps.sample_blocked_plants,
        y.source_year,
        e.expected_djf_hours,
        coalesce(c.valid_djf_hours, 0)::bigint as valid_djf_hours,
        greatest(e.expected_djf_hours - coalesce(c.valid_djf_hours, 0), 0)::bigint as missing_djf_hours,
        (
            greatest(e.expected_djf_hours - coalesce(c.valid_djf_hours, 0), 0)
            * bs.impacted_blocked_plant_count
        )::bigint as plant_weighted_missing_djf_hours,
        round(coalesce(c.coverage_ratio, 0), 6)::text as coverage_ratio,
        coalesce(c.coverage_status, 'missing') as coverage_status,
        coalesce(c.loaded_file_count, 0)::text as loaded_file_count,
        coalesce(c.invalid_temp_row_count, 0)::text as invalid_temp_row_count,
        coalesce(c.rejected_source_row_count, 0)::text as rejected_source_row_count,
        coalesce(c.rejected_plausibility_row_count, 0)::text as rejected_plausibility_row_count,
        coalesce(c.duplicate_hour_count, 0)::text as duplicate_hour_count,
        (
            st.first_observation_utc is null
            or st.last_observation_utc is null
            or (
                st.first_observation_utc < make_timestamptz(y.source_year, 3, 1, 0, 0, 0, 'UTC')
                and st.last_observation_utc >= make_timestamptz(y.source_year, 1, 1, 0, 0, 0, 'UTC')
            )
            or (
                st.first_observation_utc < make_timestamptz(y.source_year + 1, 1, 1, 0, 0, 0, 'UTC')
                and st.last_observation_utc >= make_timestamptz(y.source_year, 12, 1, 0, 0, 0, 'UTC')
            )
        ) as active_window_overlap,
        li.calculation_run_id as latest_inventory_run_id,
        li.file_status as latest_inventory_status,
        li.local_path as latest_inventory_local_path,
        la.download_status as latest_download_status,
        la.http_status::text as latest_http_status,
        la.calculation_run_id as latest_download_run_id,
        la.attempted_at_utc::text as latest_download_attempted_at_utc,
        ma.manifest_statuses
    from best_station bs
    cross join fixed_years y
    join fixed_expected_by_year e using (source_year)
    join weather.station st
      on st.station_id = bs.station_id
    left join station_plant_sample sps
      on sps.station_id = bs.station_id
    left join {coverage_table} c
      on c.calculation_run_id = {sql_literal(coverage_run_id)}
     and c.station_id = bs.station_id
     and c.source_year = y.source_year
    left join latest_attempt la
      on la.station_id = bs.station_id
     and la.source_year = y.source_year
    left join latest_inventory li
      on li.station_id = bs.station_id
     and li.source_year = y.source_year
    left join manifest_agg ma
      on ma.station_id = bs.station_id
     and ma.source_year = y.source_year
)
select
    *,
    case
        when coverage_status = 'complete' then 'complete_loaded'
        when coverage_status = 'partial' then 'partial_loaded'
        when coverage_status = 'empty' then 'empty_loaded'
        when active_window_overlap = false then 'outside_station_metadata_window'
        when latest_download_status = 'missing_on_aws'
          or manifest_statuses like '%missing%' then 'terminal_aws_missing'
        when latest_download_status in ('failed_http', 'failed_exception') then 'retryable_download_failure'
        when latest_download_status in ('downloaded', 'skipped_existing')
          or manifest_statuses like '%downloaded%' then 'downloaded_no_canonical_djf'
        when latest_inventory_status = 'available' then 'available_raw_not_loaded'
        when latest_inventory_status = 'missing' then 'raw_inventory_missing'
        else 'no_download_or_manifest_evidence'
    end as gap_cause
from station_years
order by station_id, source_year
"""


def gap_query_from_best_station_rows(
    diagnostic_run_id: str,
    plant_ecwt_run_id: str,
    candidate_run_id: str,
    station_ecwt_run_id: str,
    coverage_run_id: str,
    coverage_table: str,
    fixed_min_year: int,
    fixed_max_year: int,
    best_station_rows: list[dict[str, object]],
) -> str:
    if coverage_table not in {"weather.station_year_djf_coverage", "weather.station_year_djf_coverage_current"}:
        raise ValueError(f"Unexpected coverage table: {coverage_table}")
    return f"""
with fixed_years as (
    select generate_series({fixed_min_year}, {fixed_max_year})::integer as source_year
),
fixed_expected_by_year as (
    select
        y.source_year,
        count(*) filter (
            where extract(month from gs.hour_utc at time zone 'UTC') in (12, 1, 2)
        )::bigint as expected_djf_hours
    from fixed_years y
    cross join lateral generate_series(
        make_timestamptz(y.source_year, 1, 1, 0, 0, 0, 'UTC'),
        make_timestamptz(y.source_year, 12, 31, 23, 0, 0, 'UTC'),
        interval '1 hour'
    ) as gs(hour_utc)
    group by y.source_year
),
best_station(
    station_id,
    impacted_blocked_plant_count,
    min_candidate_rank_order,
    max_candidate_rank_order,
    min_candidate_distance_km,
    max_candidate_distance_km,
    sample_blocked_plants
) as (
    values
        {best_station_values(best_station_rows)}
),
latest_attempt as (
    select distinct on (station_id, source_year)
        station_id,
        source_year,
        download_status,
        http_status,
        calculation_run_id,
        attempted_at_utc
    from weather.noaa_raw_download_attempt
    order by station_id, source_year, attempted_at_utc desc nulls last, calculation_run_id desc
),
latest_inventory as (
    select distinct on (station_id, source_year)
        station_id,
        source_year,
        calculation_run_id,
        file_status,
        local_path
    from weather.noaa_raw_file_inventory
    order by station_id, source_year, created_at_utc desc, calculation_run_id desc
),
manifest_agg as (
    select
        station_id,
        source_year,
        string_agg(distinct manifest_status, ',' order by manifest_status) as manifest_statuses
    from weather.noaa_raw_backfill_manifest
    group by station_id, source_year
),
station_years as (
    select
        {sql_literal(diagnostic_run_id)} as diagnostic_run_id,
        {sql_literal(plant_ecwt_run_id)} as plant_ecwt_run_id,
        {sql_literal(candidate_run_id)} as candidate_run_id,
        {sql_literal(station_ecwt_run_id)} as station_ecwt_run_id,
        {sql_literal(coverage_run_id)} as coverage_run_id,
        {sql_literal(coverage_table)} as coverage_table,
        bs.station_id,
        st.station_name,
        st.state as station_state,
        st.country as station_country,
        st.first_observation_utc::text as station_first_observation_utc,
        st.last_observation_utc::text as station_last_observation_utc,
        bs.impacted_blocked_plant_count::text as impacted_blocked_plant_count,
        bs.min_candidate_rank_order::text as min_candidate_rank_order,
        bs.max_candidate_rank_order::text as max_candidate_rank_order,
        bs.min_candidate_distance_km,
        bs.max_candidate_distance_km,
        bs.sample_blocked_plants,
        y.source_year,
        e.expected_djf_hours,
        coalesce(c.valid_djf_hours, 0)::bigint as valid_djf_hours,
        greatest(e.expected_djf_hours - coalesce(c.valid_djf_hours, 0), 0)::bigint as missing_djf_hours,
        (
            greatest(e.expected_djf_hours - coalesce(c.valid_djf_hours, 0), 0)
            * bs.impacted_blocked_plant_count
        )::bigint as plant_weighted_missing_djf_hours,
        round(coalesce(c.coverage_ratio, 0), 6)::text as coverage_ratio,
        coalesce(c.coverage_status, 'missing') as coverage_status,
        coalesce(c.loaded_file_count, 0)::text as loaded_file_count,
        coalesce(c.invalid_temp_row_count, 0)::text as invalid_temp_row_count,
        coalesce(c.rejected_source_row_count, 0)::text as rejected_source_row_count,
        coalesce(c.rejected_plausibility_row_count, 0)::text as rejected_plausibility_row_count,
        coalesce(c.duplicate_hour_count, 0)::text as duplicate_hour_count,
        (
            st.first_observation_utc is null
            or st.last_observation_utc is null
            or (
                st.first_observation_utc < make_timestamptz(y.source_year, 3, 1, 0, 0, 0, 'UTC')
                and st.last_observation_utc >= make_timestamptz(y.source_year, 1, 1, 0, 0, 0, 'UTC')
            )
            or (
                st.first_observation_utc < make_timestamptz(y.source_year + 1, 1, 1, 0, 0, 0, 'UTC')
                and st.last_observation_utc >= make_timestamptz(y.source_year, 12, 1, 0, 0, 0, 'UTC')
            )
        ) as active_window_overlap,
        li.calculation_run_id as latest_inventory_run_id,
        li.file_status as latest_inventory_status,
        li.local_path as latest_inventory_local_path,
        la.download_status as latest_download_status,
        la.http_status::text as latest_http_status,
        la.calculation_run_id as latest_download_run_id,
        la.attempted_at_utc::text as latest_download_attempted_at_utc,
        ma.manifest_statuses
    from best_station bs
    cross join fixed_years y
    join fixed_expected_by_year e using (source_year)
    join weather.station st
      on st.station_id = bs.station_id
    left join {coverage_table} c
      on c.calculation_run_id = {sql_literal(coverage_run_id)}
     and c.station_id = bs.station_id
     and c.source_year = y.source_year
    left join latest_attempt la
      on la.station_id = bs.station_id
     and la.source_year = y.source_year
    left join latest_inventory li
      on li.station_id = bs.station_id
     and li.source_year = y.source_year
    left join manifest_agg ma
      on ma.station_id = bs.station_id
     and ma.source_year = y.source_year
)
select
    *,
    case
        when coverage_status = 'complete' then 'complete_loaded'
        when coverage_status = 'partial' then 'partial_loaded'
        when coverage_status = 'empty' then 'empty_loaded'
        when active_window_overlap = false then 'outside_station_metadata_window'
        when latest_download_status = 'missing_on_aws'
          or manifest_statuses like '%missing%' then 'terminal_aws_missing'
        when latest_download_status in ('failed_http', 'failed_exception') then 'retryable_download_failure'
        when latest_download_status in ('downloaded', 'skipped_existing')
          or manifest_statuses like '%downloaded%' then 'downloaded_no_canonical_djf'
        when latest_inventory_status = 'available' then 'available_raw_not_loaded'
        when latest_inventory_status = 'missing' then 'raw_inventory_missing'
        else 'no_download_or_manifest_evidence'
    end as gap_cause
from station_years
order by station_id, source_year
"""


def manifest_counts(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    manifest_run_id: str,
) -> OrderedDict[str, int]:
    if not manifest_run_id:
        return OrderedDict()
    rows = psql_csv_query(
        psql,
        host,
        port,
        dbname,
        user,
        f"""
        select manifest_status, count(*)::text as rows
        from weather.noaa_raw_backfill_manifest
        where calculation_run_id = {sql_literal(manifest_run_id)}
        group by manifest_status
        order by manifest_status
        """,
    )
    return OrderedDict((row["manifest_status"], to_int(row["rows"])) for row in rows)


def blocked_counts(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    plant_ecwt_run_id: str,
) -> OrderedDict[str, int]:
    rows = psql_csv_query(
        psql,
        host,
        port,
        dbname,
        user,
        f"""
        select result_status, count(*)::text as rows
        from calc.plant_ecwt
        where calculation_run_id = {sql_literal(plant_ecwt_run_id)}
        group by result_status
        order by result_status
        """,
    )
    return OrderedDict((row["result_status"], to_int(row["rows"])) for row in rows)


def summarize_stations(run_id: str, plant_ecwt_run_id: str, rows: list[dict[str, str]]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["station_id"]].append(row)

    summaries: list[dict[str, object]] = []
    for station_id, station_rows in grouped.items():
        first = station_rows[0]
        missing_rows = [row for row in station_rows if to_int(row["missing_djf_hours"]) > 0]
        cause_counts = Counter(row["gap_cause"] for row in missing_rows)
        expected = sum(to_int(row["expected_djf_hours"]) for row in station_rows)
        valid = sum(to_int(row["valid_djf_hours"]) for row in station_rows)
        missing = sum(to_int(row["missing_djf_hours"]) for row in station_rows)
        weighted_missing = sum(to_int(row["plant_weighted_missing_djf_hours"]) for row in station_rows)
        top_gap_years = sorted(
            missing_rows,
            key=lambda row: (to_int(row["missing_djf_hours"]), int(row["source_year"])),
            reverse=True,
        )[:8]
        summaries.append(
            {
                "diagnostic_run_id": run_id,
                "plant_ecwt_run_id": plant_ecwt_run_id,
                "station_id": station_id,
                "station_name": first["station_name"],
                "station_state": first["station_state"],
                "station_country": first["station_country"],
                "station_first_observation_utc": first["station_first_observation_utc"],
                "station_last_observation_utc": first["station_last_observation_utc"],
                "impacted_blocked_plant_count": first["impacted_blocked_plant_count"],
                "min_candidate_rank_order": first["min_candidate_rank_order"],
                "min_candidate_distance_km": first["min_candidate_distance_km"],
                "sample_blocked_plants": first["sample_blocked_plants"],
                "fixed_expected_djf_hours": expected,
                "fixed_valid_djf_hours": valid,
                "fixed_missing_djf_hours": missing,
                "fixed_coverage_ratio": fmt_float(valid / expected if expected else 0),
                "plant_weighted_missing_djf_hours": weighted_missing,
                "missing_station_year_count": len(missing_rows),
                "complete_loaded_year_count": cause_counts["complete_loaded"],
                "partial_loaded_year_count": cause_counts["partial_loaded"],
                "empty_loaded_year_count": cause_counts["empty_loaded"],
                "outside_station_metadata_window_year_count": cause_counts["outside_station_metadata_window"],
                "terminal_aws_missing_year_count": cause_counts["terminal_aws_missing"],
                "retryable_download_failure_year_count": cause_counts["retryable_download_failure"],
                "downloaded_no_canonical_djf_year_count": cause_counts["downloaded_no_canonical_djf"],
                "available_raw_not_loaded_year_count": cause_counts["available_raw_not_loaded"],
                "raw_inventory_missing_year_count": cause_counts["raw_inventory_missing"],
                "no_download_or_manifest_evidence_year_count": cause_counts["no_download_or_manifest_evidence"],
                "top_gap_years": "; ".join(
                    f"{row['source_year']}:{row['gap_cause']}:{row['missing_djf_hours']}h" for row in top_gap_years
                ),
            }
        )
    summaries.sort(
        key=lambda row: (
            -to_int(row["plant_weighted_missing_djf_hours"]),
            -to_int(row["impacted_blocked_plant_count"]),
            row["station_id"],
        )
    )
    return summaries


def cause_summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if to_int(row["missing_djf_hours"]) > 0:
            grouped[row["gap_cause"]].append(row)
    summary = []
    for cause, cause_rows in grouped.items():
        summary.append(
            {
                "gap_cause": cause,
                "station_years": len(cause_rows),
                "stations": len({row["station_id"] for row in cause_rows}),
                "missing_djf_hours": sum(to_int(row["missing_djf_hours"]) for row in cause_rows),
                "plant_weighted_missing_djf_hours": sum(
                    to_int(row["plant_weighted_missing_djf_hours"]) for row in cause_rows
                ),
                "station_year_plant_links": sum(to_int(row["impacted_blocked_plant_count"]) for row in cause_rows),
            }
        )
    summary.sort(key=lambda row: -to_int(row["plant_weighted_missing_djf_hours"]))
    return summary


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
    plant_ecwt_run_id: str,
    candidate_run_id: str,
    station_ecwt_run_id: str,
    coverage_run_id: str,
    coverage_table: str,
    manifest_run_id: str,
    fixed_min_year: int,
    fixed_max_year: int,
    station_year_csv: Path,
    station_summary_csv: Path,
    station_year_rows: list[dict[str, str]],
    station_summaries: list[dict[str, object]],
    manifest_status_counts: OrderedDict[str, int],
    plant_status_counts: OrderedDict[str, int],
) -> None:
    causes = cause_summary(station_year_rows)
    no_best_station_count = plant_status_counts.get("blocked", 0) - sum(
        to_int(row["impacted_blocked_plant_count"]) for row in station_summaries
    )
    top_stations = [
        {
            "station": f"{row['station_id']} {row['station_name']}",
            "plants": row["impacted_blocked_plant_count"],
            "coverage": row["fixed_coverage_ratio"],
            "missing_hours": fmt_int(to_int(row["fixed_missing_djf_hours"])),
            "weighted_missing": fmt_int(to_int(row["plant_weighted_missing_djf_hours"])),
            "top_gap_years": row["top_gap_years"],
        }
        for row in station_summaries[:20]
    ]
    near_threshold = sorted(
        (
            row
            for row in station_summaries
            if to_float(row["fixed_coverage_ratio"]) >= 0.90
        ),
        key=lambda row: to_float(row["fixed_coverage_ratio"]),
        reverse=True,
    )[:20]
    near_threshold_rows = [
        {
            "station": f"{row['station_id']} {row['station_name']}",
            "plants": row["impacted_blocked_plant_count"],
            "coverage": row["fixed_coverage_ratio"],
            "missing_hours": fmt_int(to_int(row["fixed_missing_djf_hours"])),
            "top_gap_years": row["top_gap_years"],
        }
        for row in near_threshold
    ]
    manifest_rows = [{"status": status, "rows": rows} for status, rows in manifest_status_counts.items()]
    plant_rows = [{"status": status, "rows": rows} for status, rows in plant_status_counts.items()]
    cause_rows = [
        {
            "cause": row["gap_cause"],
            "station_years": fmt_int(to_int(row["station_years"])),
            "stations": fmt_int(to_int(row["stations"])),
            "missing_hours": fmt_int(to_int(row["missing_djf_hours"])),
            "weighted_missing": fmt_int(to_int(row["plant_weighted_missing_djf_hours"])),
            "plant_links": fmt_int(to_int(row["station_year_plant_links"])),
        }
        for row in causes
    ]

    lines = [
        "# Fixed-Period Gap Cause Report",
        "",
        f"Generated UTC: {utc_now().isoformat(timespec='seconds')}",
        "",
        "## Run",
        "",
        f"- Diagnostic run ID: `{run_id}`",
        f"- Code commit: `{code_commit}`",
        f"- Plant ECWT run ID: `{plant_ecwt_run_id}`",
        f"- Candidate run ID: `{candidate_run_id}`",
        f"- Station ECWT run ID: `{station_ecwt_run_id}`",
        f"- Station-year coverage run ID: `{coverage_run_id}`",
        f"- Station-year coverage table: `{coverage_table}`",
        f"- Manifest run ID used for final queue counts: `{manifest_run_id}`",
        f"- Fixed period: `{fixed_min_year}-{fixed_max_year}`",
        f"- Station-year detail CSV: `{station_year_csv.name}`",
        f"- Station summary CSV: `{station_summary_csv.name}`",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| Blocked plant rows | {fmt_int(plant_status_counts.get('blocked', 0))} |",
        f"| Blocked rows with a best provisional station candidate | {fmt_int(sum(to_int(row['impacted_blocked_plant_count']) for row in station_summaries))} |",
        f"| Blocked rows with no best station candidate | {fmt_int(no_best_station_count)} |",
        f"| Distinct best stations among blocked rows | {fmt_int(len(station_summaries))} |",
        f"| Best-station years reviewed | {fmt_int(len(station_year_rows))} |",
        f"| Best-station years with any fixed-period missing hours | {fmt_int(sum(1 for row in station_year_rows if to_int(row['missing_djf_hours']) > 0))} |",
        "",
        "## Plant ECWT Status Counts",
        "",
    ]
    render_table(lines, ["Status", "Rows"], plant_rows, ["status", "rows"])
    lines.extend(["", "## Final Manifest Status Counts", ""])
    render_table(lines, ["Status", "Rows"], manifest_rows, ["status", "rows"])
    lines.extend(["", "## Gap Causes", ""])
    render_table(
        lines,
        ["Cause", "Station-Years", "Stations", "Missing Hours", "Plant-Weighted Missing Hours", "Station-Year Plant Links"],
        cause_rows,
        ["cause", "station_years", "stations", "missing_hours", "weighted_missing", "plant_links"],
    )
    lines.extend(["", "## Top Stations By Plant-Weighted Missing Hours", ""])
    render_table(
        lines,
        ["Station", "Blocked Plants", "Coverage", "Missing Hours", "Plant-Weighted Missing Hours", "Top Gap Years"],
        top_stations,
        ["station", "plants", "coverage", "missing_hours", "weighted_missing", "top_gap_years"],
    )
    lines.extend(["", "## Nearest To Strict Coverage Threshold", ""])
    render_table(
        lines,
        ["Station", "Blocked Plants", "Coverage", "Missing Hours", "Top Gap Years"],
        near_threshold_rows,
        ["station", "plants", "coverage", "missing_hours", "top_gap_years"],
    )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `outside_station_metadata_window` means NOAA station first/last observation metadata does not overlap that source year's January-February or December DJF windows. Under the strict fixed-period denominator, those hours still count as missing.",
            "- `terminal_aws_missing` means at least one download attempt or manifest row showed a terminal NOAA AWS missing object for that station-year.",
            "- `partial_loaded` and `complete_loaded` are loaded station-years that still have missing hours against the exact fixed-period denominator; `complete_loaded` is complete by the pipeline coverage-status rule, not necessarily 100.000% complete.",
            "- `available_raw_not_loaded` means the latest raw-file inventory found a local NOAA file, but the current canonical DJF coverage has no loaded station-year row; this is a loader/source-root follow-up, not an AWS download follow-up.",
            "- `raw_inventory_missing` means the latest inventory still reports no local raw file for the station-year.",
            "- `no_download_or_manifest_evidence` should be investigated before publication because it means the current audit trail does not explain the station-year gap.",
            "- With the expanded manifest exhausted, this report is the better work queue than bulk retrying NOAA downloads.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--psql", type=Path, default=PSQL)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5436)
    parser.add_argument("--dbname", default="eop012")
    parser.add_argument("--user")
    parser.add_argument("--plant-ecwt-run-id")
    parser.add_argument("--manifest-run-id")
    parser.add_argument(
        "--blocker-csv",
        type=Path,
        help="Optional fixed-period blocker detail CSV to reuse best-station selections instead of recomputing them.",
    )
    parser.add_argument("--coverage-source", choices=["auto", "current", "history"], default="auto")
    args = parser.parse_args()

    plant_ecwt_run_id = args.plant_ecwt_run_id or latest_fixed_plant_ecwt_run_id(
        args.psql, args.host, args.port, args.dbname, args.user
    )
    if not plant_ecwt_run_id:
        raise RuntimeError("No fixed-period plant ECWT run found.")
    manifest_run_id = args.manifest_run_id or latest_manifest_run_id(
        args.psql, args.host, args.port, args.dbname, args.user
    )
    params = fetch_json_params(args.psql, args.host, args.port, args.dbname, args.user, plant_ecwt_run_id)
    candidate_run_id = str(params["candidate_run_id"])
    station_ecwt_run_id = str(params["station_ecwt_run_id"])
    coverage_run_id = str(params["coverage_run_id"])
    preferred_coverage_table = str(params.get("coverage_table") or "") if params else None
    coverage_table = resolve_coverage_table(
        args.psql,
        args.host,
        args.port,
        args.dbname,
        args.user,
        coverage_run_id,
        args.coverage_source,
        preferred_coverage_table,
    )
    fixed_min_year = int(params["fixed_min_year"])
    fixed_max_year = int(params["fixed_max_year"])

    run_id = f"fixed_period_gap_causes_{utc_now().strftime('%Y%m%dT%H%M%SZ')}"
    code_commit = git_commit_label(args.project_root)
    best_station_rows = read_best_station_rows(args.blocker_csv) if args.blocker_csv else []
    if best_station_rows:
        station_year_query = gap_query_from_best_station_rows(
            run_id,
            plant_ecwt_run_id,
            candidate_run_id,
            station_ecwt_run_id,
            coverage_run_id,
            coverage_table,
            fixed_min_year,
            fixed_max_year,
            best_station_rows,
        )
    else:
        station_year_query = gap_query(
            run_id,
            plant_ecwt_run_id,
            candidate_run_id,
            station_ecwt_run_id,
            coverage_run_id,
            coverage_table,
            fixed_min_year,
            fixed_max_year,
        )

    station_year_rows = psql_csv_query(
        args.psql,
        args.host,
        args.port,
        args.dbname,
        args.user,
        station_year_query,
    )
    station_summaries = summarize_stations(run_id, plant_ecwt_run_id, station_year_rows)
    manifest_status_counts = manifest_counts(args.psql, args.host, args.port, args.dbname, args.user, manifest_run_id)
    plant_status_counts = blocked_counts(args.psql, args.host, args.port, args.dbname, args.user, plant_ecwt_run_id)

    docs_dir = args.project_root / "docs"
    station_year_csv = docs_dir / f"{run_id}_station_years.csv"
    station_summary_csv = docs_dir / f"{run_id}_stations.csv"
    report_path = docs_dir / f"{run_id}_report.md"
    write_csv(station_year_csv, STATION_YEAR_FIELDS, station_year_rows)
    write_csv(station_summary_csv, STATION_SUMMARY_FIELDS, station_summaries)
    render_report(
        report_path,
        run_id,
        code_commit,
        plant_ecwt_run_id,
        candidate_run_id,
        station_ecwt_run_id,
        coverage_run_id,
        coverage_table,
        manifest_run_id,
        fixed_min_year,
        fixed_max_year,
        station_year_csv,
        station_summary_csv,
        station_year_rows,
        station_summaries,
        manifest_status_counts,
        plant_status_counts,
    )
    print(
        json.dumps(
            OrderedDict(
                [
                    ("run_id", run_id),
                    ("plant_ecwt_run_id", plant_ecwt_run_id),
                    ("manifest_run_id", manifest_run_id),
                    ("station_year_rows", len(station_year_rows)),
                    ("station_rows", len(station_summaries)),
                    ("station_year_csv", str(station_year_csv)),
                    ("station_summary_csv", str(station_summary_csv)),
                    ("report_path", str(report_path)),
                ]
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
