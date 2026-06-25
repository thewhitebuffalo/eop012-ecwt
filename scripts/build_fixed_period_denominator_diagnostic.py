#!/usr/bin/env python3
"""Compare fixed-period and station-active-window coverage gates for blocked plants."""

from __future__ import annotations

import argparse
import calendar
import csv
import io
import json
import subprocess
from collections import Counter, OrderedDict, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable

from eop012_config import PROJECT_ROOT, PSQL


METHODOLOGY_VERSION = "eop012-ecwt-method-v0.1.0"
OPERABLE_STATUSES = ("OP", "SB", "OA", "OS")


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


def psql_execute(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    sql: str,
) -> None:
    run(psql_cmd(psql, host, port, dbname, user) + ["-c", sql])


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def git_commit_label(project_root: Path) -> str:
    try:
        return run(["git", "-C", str(project_root), "rev-parse", "HEAD"]).stdout.strip()
    except Exception:
        return "UNCOMMITTED_WORKTREE"


def register_calculation_run(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    run_id: str,
    code_commit: str,
    run_started_at: datetime,
    parameters: dict[str, object],
) -> None:
    psql_execute(
        psql,
        host,
        port,
        dbname,
        user,
        f"""
        insert into audit.calculation_run (
            calculation_run_id,
            methodology_version,
            code_commit,
            run_started_at_utc,
            run_finished_at_utc,
            run_status,
            parameters_json,
            notes
        )
        values (
            {sql_literal(run_id)},
            {sql_literal(METHODOLOGY_VERSION)},
            {sql_literal(code_commit)},
            {sql_literal(run_started_at.isoformat())}::timestamptz,
            now(),
            'succeeded',
            {sql_literal(json.dumps(parameters, sort_keys=True))}::jsonb,
            'Generated fixed-period denominator diagnostic comparing fixed-period and station-active-window coverage gates.'
        )
        on conflict (calculation_run_id) do update set
            code_commit = excluded.code_commit,
            run_started_at_utc = excluded.run_started_at_utc,
            run_finished_at_utc = excluded.run_finished_at_utc,
            run_status = excluded.run_status,
            parameters_json = excluded.parameters_json,
            notes = excluded.notes;
        """,
    )


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


def latest_readiness_run_id(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    plant_ecwt_run_id: str,
) -> str:
    return psql_scalar(
        psql,
        host,
        port,
        dbname,
        user,
        f"""
        select calculation_run_id
        from audit.calculation_run
        where calculation_run_id like 'plant_ecwt_readiness_fixed_period_%'
          and run_status = 'succeeded'
          and parameters_json ->> 'plant_ecwt_run_id' = {sql_literal(plant_ecwt_run_id)}
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


def blocked_plants_query(plant_ecwt_run_id: str, plant_scope: str) -> str:
    status_list = ", ".join(sql_literal(status) for status in OPERABLE_STATUSES)
    scope_filter = "fs.plant_id is not null" if plant_scope == "first-operable" else "true"
    return f"""
    with first_scope as (
        select
            ('eia860:2024:plant:' || eia_plant_code)::text as plant_id,
            count(*)::integer as first_operable_generator_count,
            round(coalesce(sum(nameplate_capacity_mw), 0), 3)::text as first_operable_nameplate_mw
        from asset.generator
        where status in ({status_list})
        group by ('eia860:2024:plant:' || eia_plant_code)::text
    )
    select
        pe.plant_id,
        p.eia_plant_code,
        p.plant_name,
        p.state as plant_state,
        p.county as plant_county,
        round(p.latitude, 6)::text as plant_latitude,
        round(p.longitude, 6)::text as plant_longitude,
        p.nerc_region,
        p.balancing_authority_code,
        p.sector_name,
        coalesce(fs.first_operable_generator_count, 0)::text as first_operable_generator_count,
        coalesce(fs.first_operable_nameplate_mw, '0.000') as first_operable_nameplate_mw
    from calc.plant_ecwt pe
    join asset.plant p using (plant_id)
    left join first_scope fs using (plant_id)
    where pe.calculation_run_id = {sql_literal(plant_ecwt_run_id)}
      and pe.result_status = 'blocked'
      and {scope_filter}
    order by p.state, p.eia_plant_code::integer nulls last, p.plant_name
    """


def candidate_rows_query(
    plant_ecwt_run_id: str,
    candidate_run_id: str,
    station_ecwt_run_id: str,
    plant_scope: str,
) -> str:
    status_list = ", ".join(sql_literal(status) for status in OPERABLE_STATUSES)
    scope_filter = "fs.plant_id is not null" if plant_scope == "first-operable" else "true"
    return f"""
    with first_scope as (
        select distinct ('eia860:2024:plant:' || eia_plant_code)::text as plant_id
        from asset.generator
        where status in ({status_list})
    ),
    blocked_plants as (
        select pe.plant_id
        from calc.plant_ecwt pe
        left join first_scope fs using (plant_id)
        where pe.calculation_run_id = {sql_literal(plant_ecwt_run_id)}
          and pe.result_status = 'blocked'
          and {scope_filter}
    )
    select
        sc.plant_id,
        sc.station_id,
        st.station_name,
        st.state as station_state,
        st.country as station_country,
        to_char(st.first_observation_utc at time zone 'UTC', 'YYYY-MM-DD"T"HH24:MI:SS"Z"')
            as first_observation_utc,
        to_char(st.last_observation_utc at time zone 'UTC', 'YYYY-MM-DD"T"HH24:MI:SS"Z"')
            as last_observation_utc,
        extract(epoch from st.first_observation_utc)::text as first_observation_epoch,
        extract(epoch from st.last_observation_utc)::text as last_observation_epoch,
        round(sc.distance_km, 3)::text as distance_km,
        sc.distance_km::text as distance_km_num,
        sc.rank_order::text as rank_order,
        se.station_ecwt_id,
        se.result_status as station_ecwt_status,
        coalesce(se.valid_hour_count, 0)::text as station_ecwt_valid_hour_count,
        round(se.ecwt_f, 3)::text as station_ecwt_f
    from link.station_candidate sc
    join blocked_plants bp using (plant_id)
    join weather.station st using (station_id)
    left join calc.station_ecwt se
      on se.station_id = sc.station_id
     and se.calculation_run_id = {sql_literal(station_ecwt_run_id)}
    where sc.calculation_run_id = {sql_literal(candidate_run_id)}
      and sc.candidate_status = 'candidate'
    order by sc.plant_id, sc.rank_order nulls last, sc.distance_km nulls last, sc.station_id
    """


def coverage_rows_query(coverage_run_id: str, coverage_table: str, min_year: int, max_year: int) -> str:
    if coverage_table not in {"weather.station_year_djf_coverage", "weather.station_year_djf_coverage_current"}:
        raise ValueError(f"Unsupported coverage table: {coverage_table}")
    return f"""
    select
        station_id,
        source_year::text as source_year,
        expected_djf_hours::text as expected_djf_hours,
        valid_djf_hours::text as valid_djf_hours,
        duplicate_hour_count::text as duplicate_hour_count,
        loaded_file_count::text as loaded_file_count,
        coverage_status
    from {coverage_table}
    where calculation_run_id = {sql_literal(coverage_run_id)}
      and source_year between {min_year} and {max_year}
    """


def dt_from_epoch(raw: str | None) -> datetime | None:
    if not raw:
        return None
    return datetime.fromtimestamp(float(raw), timezone.utc)


def int_value(raw: object, default: int = 0) -> int:
    if raw in (None, ""):
        return default
    return int(float(str(raw)))


def float_value(raw: object, default: float = 0.0) -> float:
    if raw in (None, ""):
        return default
    return float(str(raw))


def fmt_int(value: int | None) -> str:
    return "" if value is None else str(value)


def fmt_float(value: float | None, digits: int = 6) -> str:
    return "" if value is None else f"{value:.{digits}f}"


def expected_djf_hours_by_year(min_year: int, max_year: int) -> dict[int, int]:
    return {year: (31 + (29 if calendar.isleap(year) else 28) + 31) * 24 for year in range(min_year, max_year + 1)}


def active_expected_by_year(
    first_obs: datetime | None,
    last_obs: datetime | None,
    min_year: int,
    max_year: int,
) -> dict[int, int]:
    fixed_start = datetime(min_year, 1, 1, tzinfo=timezone.utc)
    fixed_end = datetime(max_year + 1, 1, 1, tzinfo=timezone.utc)
    active_start = first_obs or fixed_start
    active_end = (last_obs + timedelta(hours=1)) if last_obs else fixed_end
    by_year: dict[int, int] = {}
    for year in range(min_year, max_year + 1):
        total = 0.0
        segments = (
            (datetime(year, 1, 1, tzinfo=timezone.utc), datetime(year, 3, 1, tzinfo=timezone.utc)),
            (datetime(year, 12, 1, tzinfo=timezone.utc), datetime(year + 1, 1, 1, tzinfo=timezone.utc)),
        )
        for seg_start, seg_end in segments:
            left = max(seg_start, active_start)
            right = min(seg_end, active_end)
            if right > left:
                total += (right - left).total_seconds() / 3600.0
        by_year[year] = int(round(total))
    return by_year


def build_station_metrics(
    candidates: list[dict[str, str]],
    coverage_rows: list[dict[str, str]],
    min_year: int,
    max_year: int,
) -> dict[str, dict[str, object]]:
    expected_by_year = expected_djf_hours_by_year(min_year, max_year)
    coverage: dict[tuple[str, int], dict[str, str]] = {}
    for row in coverage_rows:
        coverage[(row["station_id"], int(row["source_year"]))] = row

    station_info: dict[str, dict[str, str]] = {}
    for row in candidates:
        station_info.setdefault(row["station_id"], row)

    fixed_expected = sum(expected_by_year.values())
    metrics: dict[str, dict[str, object]] = {}
    for station_id, info in station_info.items():
        first_obs = dt_from_epoch(info.get("first_observation_epoch"))
        last_obs = dt_from_epoch(info.get("last_observation_epoch"))
        active_expected = active_expected_by_year(first_obs, last_obs, min_year, max_year)

        fixed_valid = 0
        fixed_duplicate = 0
        loaded_years = 0
        complete_years = 0
        first_loaded: int | None = None
        last_loaded: int | None = None
        active_valid = 0
        active_loaded_years = 0
        active_complete_years = 0
        year_data: dict[int, tuple[int, bool, bool]] = {}
        for year in range(min_year, max_year + 1):
            cov = coverage.get((station_id, year))
            valid = int_value(cov.get("valid_djf_hours") if cov else None)
            fixed_valid += valid
            fixed_duplicate += int_value(cov.get("duplicate_hour_count") if cov else None)
            loaded = int_value(cov.get("loaded_file_count") if cov else None) > 0
            complete = bool(cov and cov.get("coverage_status") == "complete")
            year_data[year] = (valid, loaded, complete)
            if loaded:
                loaded_years += 1
                first_loaded = year if first_loaded is None else min(first_loaded, year)
                last_loaded = year if last_loaded is None else max(last_loaded, year)
            if complete:
                complete_years += 1
            if active_expected[year] > 0:
                active_valid += valid
                if loaded:
                    active_loaded_years += 1
                if complete:
                    active_complete_years += 1

        active_expected_total = sum(active_expected.values())
        active_years = sum(1 for hours in active_expected.values() if hours > 0)
        active_overfilled = max(active_valid - active_expected_total, 0)

        loaded_window_start = datetime(first_loaded, 1, 1, tzinfo=timezone.utc) if first_loaded else None
        loaded_window_end = datetime(last_loaded, 12, 31, 23, tzinfo=timezone.utc) if last_loaded else None
        normalized_first_candidates = [dt for dt in (first_obs, loaded_window_start) if dt is not None]
        normalized_last_candidates = [dt for dt in (last_obs, loaded_window_end) if dt is not None]
        normalized_first = min(normalized_first_candidates) if normalized_first_candidates else None
        normalized_last = max(normalized_last_candidates) if normalized_last_candidates else None
        normalized_active_expected = active_expected_by_year(normalized_first, normalized_last, min_year, max_year)
        normalized_active_valid = 0
        normalized_active_loaded_years = 0
        normalized_active_complete_years = 0
        for year, (valid, loaded, complete) in year_data.items():
            if normalized_active_expected[year] > 0:
                normalized_active_valid += valid
                if loaded:
                    normalized_active_loaded_years += 1
                if complete:
                    normalized_active_complete_years += 1
        normalized_active_expected_total = sum(normalized_active_expected.values())
        normalized_active_years = sum(1 for hours in normalized_active_expected.values() if hours > 0)
        normalized_active_overfilled = max(normalized_active_valid - normalized_active_expected_total, 0)
        metrics[station_id] = {
            "fixed_expected_djf_hours": fixed_expected,
            "fixed_valid_djf_hours": fixed_valid,
            "fixed_missing_djf_hours": max(fixed_expected - fixed_valid, 0),
            "fixed_duplicate_hour_count": fixed_duplicate,
            "loaded_station_year_count": loaded_years,
            "complete_station_year_count": complete_years,
            "first_loaded_year": first_loaded,
            "last_loaded_year": last_loaded,
            "fixed_coverage_ratio": fixed_valid / fixed_expected if fixed_expected else None,
            "active_expected_djf_hours": active_expected_total,
            "active_valid_djf_hours": active_valid,
            "active_missing_djf_hours": max(active_expected_total - active_valid, 0),
            "active_overfilled_hour_count": active_overfilled,
            "active_djf_year_count": active_years,
            "active_loaded_station_year_count": active_loaded_years,
            "active_complete_station_year_count": active_complete_years,
            "active_coverage_ratio": active_valid / active_expected_total if active_expected_total else None,
            "active_loaded_year_ratio": active_loaded_years / active_years if active_years else None,
            "loaded_window_first_year": first_loaded,
            "loaded_window_last_year": last_loaded,
            "normalized_active_first_utc": normalized_first.isoformat().replace("+00:00", "Z") if normalized_first else "",
            "normalized_active_last_utc": normalized_last.isoformat().replace("+00:00", "Z") if normalized_last else "",
            "normalized_active_expected_djf_hours": normalized_active_expected_total,
            "normalized_active_valid_djf_hours": normalized_active_valid,
            "normalized_active_missing_djf_hours": max(normalized_active_expected_total - normalized_active_valid, 0),
            "normalized_active_overfilled_hour_count": normalized_active_overfilled,
            "normalized_active_djf_year_count": normalized_active_years,
            "normalized_active_loaded_station_year_count": normalized_active_loaded_years,
            "normalized_active_complete_station_year_count": normalized_active_complete_years,
            "normalized_active_coverage_ratio": (
                normalized_active_valid / normalized_active_expected_total if normalized_active_expected_total else None
            ),
            "normalized_active_loaded_year_ratio": (
                normalized_active_loaded_years / normalized_active_years if normalized_active_years else None
            ),
        }
    return metrics


def candidate_eval(row: dict[str, str], metrics: dict[str, object], min_ratio: float, min_loaded_years: int) -> dict[str, object]:
    has_provisional = (
        bool(row.get("station_ecwt_id"))
        and row.get("station_ecwt_status") == "provisional"
        and int_value(row.get("station_ecwt_valid_hour_count")) > 0
    )
    fixed_ratio = metrics.get("fixed_coverage_ratio")
    active_ratio = metrics.get("active_coverage_ratio")
    normalized_active_ratio = metrics.get("normalized_active_coverage_ratio")
    loaded_years = int(metrics.get("loaded_station_year_count") or 0)
    active_loaded_year_ratio = metrics.get("active_loaded_year_ratio")
    normalized_active_loaded_year_ratio = metrics.get("normalized_active_loaded_year_ratio")
    eval_row: dict[str, object] = dict(row)
    eval_row.update(metrics)
    eval_row["has_station_ecwt_row"] = bool(row.get("station_ecwt_id"))
    eval_row["has_provisional_station_ecwt"] = has_provisional
    eval_row["fixed_eligible"] = bool(has_provisional and fixed_ratio is not None and fixed_ratio >= min_ratio and loaded_years >= min_loaded_years)
    eval_row["active_coverage_eligible"] = bool(has_provisional and active_ratio is not None and active_ratio >= min_ratio)
    eval_row["active_coverage_absolute_loaded_eligible"] = bool(
        has_provisional and active_ratio is not None and active_ratio >= min_ratio and loaded_years >= min_loaded_years
    )
    eval_row["active_window_eligible"] = bool(
        has_provisional
        and active_ratio is not None
        and active_ratio >= min_ratio
        and active_loaded_year_ratio is not None
        and active_loaded_year_ratio >= min_ratio
    )
    eval_row["normalized_active_coverage_eligible"] = bool(
        has_provisional and normalized_active_ratio is not None and normalized_active_ratio >= min_ratio
    )
    eval_row["normalized_active_coverage_absolute_loaded_eligible"] = bool(
        has_provisional
        and normalized_active_ratio is not None
        and normalized_active_ratio >= min_ratio
        and loaded_years >= min_loaded_years
    )
    eval_row["normalized_active_window_eligible"] = bool(
        has_provisional
        and normalized_active_ratio is not None
        and normalized_active_ratio >= min_ratio
        and normalized_active_loaded_year_ratio is not None
        and normalized_active_loaded_year_ratio >= min_ratio
    )
    return eval_row


def sort_key_fixed(candidate: dict[str, object]) -> tuple[object, ...]:
    return (
        not bool(candidate["fixed_eligible"]),
        -(float(candidate.get("fixed_coverage_ratio") or 0.0)),
        -(int(candidate.get("loaded_station_year_count") or 0)),
        int_value(candidate.get("rank_order"), 999999),
        float_value(candidate.get("distance_km_num"), 1e12),
        str(candidate.get("station_id") or ""),
    )


def sort_key_active(candidate: dict[str, object]) -> tuple[object, ...]:
    return (
        not bool(candidate["active_window_eligible"]),
        not bool(candidate["active_coverage_eligible"]),
        -(float(candidate.get("active_coverage_ratio") or 0.0)),
        -(float(candidate.get("active_loaded_year_ratio") or 0.0)),
        -(float(candidate.get("fixed_coverage_ratio") or 0.0)),
        int_value(candidate.get("rank_order"), 999999),
        float_value(candidate.get("distance_km_num"), 1e12),
        str(candidate.get("station_id") or ""),
    )


def sort_key_normalized_active(candidate: dict[str, object]) -> tuple[object, ...]:
    return (
        not bool(candidate["normalized_active_window_eligible"]),
        not bool(candidate["normalized_active_coverage_eligible"]),
        -(float(candidate.get("normalized_active_coverage_ratio") or 0.0)),
        -(float(candidate.get("normalized_active_loaded_year_ratio") or 0.0)),
        -(float(candidate.get("fixed_coverage_ratio") or 0.0)),
        int_value(candidate.get("rank_order"), 999999),
        float_value(candidate.get("distance_km_num"), 1e12),
        str(candidate.get("station_id") or ""),
    )


def build_detail_rows(
    blocked_plants: list[dict[str, str]],
    candidates: list[dict[str, str]],
    station_metrics: dict[str, dict[str, object]],
    min_ratio: float,
    min_loaded_years: int,
) -> list[dict[str, str]]:
    candidates_by_plant: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in candidates:
        metrics = station_metrics.get(row["station_id"], {})
        candidates_by_plant[row["plant_id"]].append(candidate_eval(row, metrics, min_ratio, min_loaded_years))

    details: list[dict[str, str]] = []
    for plant in blocked_plants:
        plant_candidates = candidates_by_plant.get(plant["plant_id"], [])
        provisional = [row for row in plant_candidates if row["has_provisional_station_ecwt"]]
        best_fixed = sorted(provisional, key=sort_key_fixed)[0] if provisional else {}
        best_active = sorted(provisional, key=sort_key_active)[0] if provisional else {}
        best_normalized_active = sorted(provisional, key=sort_key_normalized_active)[0] if provisional else {}

        candidate_count = len(plant_candidates)
        station_ecwt_count = sum(1 for row in plant_candidates if row["has_station_ecwt_row"])
        provisional_count = len(provisional)
        fixed_eligible_count = sum(1 for row in plant_candidates if row["fixed_eligible"])
        active_coverage_count = sum(1 for row in plant_candidates if row["active_coverage_eligible"])
        active_abs_count = sum(1 for row in plant_candidates if row["active_coverage_absolute_loaded_eligible"])
        active_window_count = sum(1 for row in plant_candidates if row["active_window_eligible"])
        normalized_active_coverage_count = sum(
            1 for row in plant_candidates if row["normalized_active_coverage_eligible"]
        )
        normalized_active_abs_count = sum(
            1 for row in plant_candidates if row["normalized_active_coverage_absolute_loaded_eligible"]
        )
        normalized_active_window_count = sum(
            1 for row in plant_candidates if row["normalized_active_window_eligible"]
        )
        best_fixed_ratio = max((float(row.get("fixed_coverage_ratio") or 0) for row in plant_candidates), default=0.0)
        best_loaded_years = max((int(row.get("loaded_station_year_count") or 0) for row in plant_candidates), default=0)
        best_fixed_valid = max((int(row.get("fixed_valid_djf_hours") or 0) for row in plant_candidates), default=0)
        best_active_ratio = max((float(row.get("active_coverage_ratio") or 0) for row in plant_candidates), default=0.0)
        best_active_loaded_ratio = max((float(row.get("active_loaded_year_ratio") or 0) for row in plant_candidates), default=0.0)
        best_normalized_active_ratio = max(
            (float(row.get("normalized_active_coverage_ratio") or 0) for row in plant_candidates),
            default=0.0,
        )
        best_normalized_active_loaded_ratio = max(
            (float(row.get("normalized_active_loaded_year_ratio") or 0) for row in plant_candidates),
            default=0.0,
        )

        if fixed_eligible_count:
            current_class = "unexpected_blocked_has_eligible_candidate"
        elif candidate_count == 0:
            current_class = "no_station_candidates"
        elif provisional_count == 0:
            current_class = "no_candidate_with_provisional_station_ecwt"
        elif best_loaded_years < min_loaded_years and best_fixed_ratio < min_ratio:
            current_class = "fixed_coverage_and_loaded_years_below_threshold"
        elif best_loaded_years < min_loaded_years:
            current_class = "fixed_loaded_years_below_threshold"
        elif best_fixed_ratio < min_ratio:
            current_class = "fixed_coverage_below_threshold"
        else:
            current_class = "other_no_eligible_candidate"

        if candidate_count == 0:
            active_class = "no_station_candidates"
        elif provisional_count == 0:
            active_class = "no_candidate_with_provisional_station_ecwt"
        elif active_window_count:
            active_class = "would_pass_active_window_coverage_and_active_year_ratio"
        elif active_abs_count:
            active_class = "would_pass_active_window_coverage_plus_20_loaded_years"
        elif active_coverage_count:
            active_class = "would_pass_active_window_coverage_only"
        else:
            active_class = "still_fails_active_window_coverage"

        if candidate_count == 0:
            normalized_active_class = "no_station_candidates"
        elif provisional_count == 0:
            normalized_active_class = "no_candidate_with_provisional_station_ecwt"
        elif normalized_active_window_count:
            normalized_active_class = "would_pass_normalized_active_window_coverage_and_active_year_ratio"
        elif normalized_active_abs_count:
            normalized_active_class = "would_pass_normalized_active_window_coverage_plus_20_loaded_years"
        elif normalized_active_coverage_count:
            normalized_active_class = "would_pass_normalized_active_window_coverage_only"
        else:
            normalized_active_class = "still_fails_normalized_active_window_coverage"

        detail = {
            **plant,
            "current_blocker_class": current_class,
            "active_window_class": active_class,
            "normalized_active_window_class": normalized_active_class,
            "candidate_count": str(candidate_count),
            "candidate_with_station_ecwt_row_count": str(station_ecwt_count),
            "candidate_with_provisional_station_ecwt_count": str(provisional_count),
            "fixed_eligible_candidate_count": str(fixed_eligible_count),
            "active_coverage_eligible_candidate_count": str(active_coverage_count),
            "active_coverage_absolute_loaded_eligible_candidate_count": str(active_abs_count),
            "active_window_eligible_candidate_count": str(active_window_count),
            "normalized_active_coverage_eligible_candidate_count": str(normalized_active_coverage_count),
            "normalized_active_coverage_absolute_loaded_eligible_candidate_count": str(normalized_active_abs_count),
            "normalized_active_window_eligible_candidate_count": str(normalized_active_window_count),
            "best_fixed_coverage_ratio": fmt_float(best_fixed_ratio),
            "best_loaded_station_year_count": str(best_loaded_years),
            "best_fixed_valid_djf_hours": str(best_fixed_valid),
            "best_active_coverage_ratio": fmt_float(best_active_ratio),
            "best_active_loaded_year_ratio": fmt_float(best_active_loaded_ratio),
            "best_normalized_active_coverage_ratio": fmt_float(best_normalized_active_ratio),
            "best_normalized_active_loaded_year_ratio": fmt_float(best_normalized_active_loaded_ratio),
        }
        add_candidate_fields(detail, "best_fixed", best_fixed)
        add_candidate_fields(detail, "best_active", best_active)
        add_candidate_fields(detail, "best_normalized_active", best_normalized_active)
        details.append(detail)
    return details


def add_candidate_fields(detail: dict[str, str], prefix: str, candidate: dict[str, object]) -> None:
    fields = {
        "station_id": "station_id",
        "station_name": "station_name",
        "station_state": "station_state",
        "station_country": "station_country",
        "distance_km": "distance_km",
        "rank_order": "rank_order",
        "station_ecwt_status": "station_ecwt_status",
        "station_ecwt_valid_hour_count": "station_ecwt_valid_hour_count",
        "station_ecwt_f": "station_ecwt_f",
        "station_first_observation_utc": "first_observation_utc",
        "station_last_observation_utc": "last_observation_utc",
    }
    for out_suffix, source_field in fields.items():
        detail[f"{prefix}_{out_suffix}"] = str(candidate.get(source_field) or "")

    metric_fields = (
        "fixed_coverage_ratio",
        "loaded_station_year_count",
        "fixed_valid_djf_hours",
        "fixed_expected_djf_hours",
        "first_loaded_year",
        "last_loaded_year",
        "active_expected_djf_hours",
        "active_valid_djf_hours",
        "active_missing_djf_hours",
        "active_overfilled_hour_count",
        "active_djf_year_count",
        "active_loaded_station_year_count",
        "active_coverage_ratio",
        "active_loaded_year_ratio",
        "loaded_window_first_year",
        "loaded_window_last_year",
        "normalized_active_first_utc",
        "normalized_active_last_utc",
        "normalized_active_expected_djf_hours",
        "normalized_active_valid_djf_hours",
        "normalized_active_missing_djf_hours",
        "normalized_active_overfilled_hour_count",
        "normalized_active_djf_year_count",
        "normalized_active_loaded_station_year_count",
        "normalized_active_coverage_ratio",
        "normalized_active_loaded_year_ratio",
    )
    for field in metric_fields:
        value = candidate.get(field)
        if isinstance(value, float):
            detail[f"{prefix}_{field}"] = fmt_float(value)
        elif value is None:
            detail[f"{prefix}_{field}"] = ""
        else:
            detail[f"{prefix}_{field}"] = str(value)


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
    readiness_run_id: str,
    candidate_run_id: str,
    station_ecwt_run_id: str,
    coverage_run_id: str,
    coverage_table: str,
    fixed_min_year: int,
    fixed_max_year: int,
    fixed_min_coverage_ratio: float,
    fixed_min_loaded_years: int,
    plant_scope: str,
    detail_csv: Path,
    rows: list[dict[str, str]],
) -> None:
    current_counts = Counter(row["current_blocker_class"] for row in rows)
    active_counts = Counter(row["active_window_class"] for row in rows)
    normalized_active_counts = Counter(row["normalized_active_window_class"] for row in rows)
    state_counts = Counter(row["plant_state"] or "(blank)" for row in rows)

    active_coverage_any = sum(1 for row in rows if int_value(row["active_coverage_eligible_candidate_count"]) > 0)
    active_abs_loaded_any = sum(
        1 for row in rows if int_value(row["active_coverage_absolute_loaded_eligible_candidate_count"]) > 0
    )
    active_window_any = sum(1 for row in rows if int_value(row["active_window_eligible_candidate_count"]) > 0)
    normalized_active_coverage_any = sum(
        1 for row in rows if int_value(row["normalized_active_coverage_eligible_candidate_count"]) > 0
    )
    normalized_active_abs_loaded_any = sum(
        1 for row in rows if int_value(row["normalized_active_coverage_absolute_loaded_eligible_candidate_count"]) > 0
    )
    normalized_active_window_any = sum(
        1 for row in rows if int_value(row["normalized_active_window_eligible_candidate_count"]) > 0
    )
    active_overfilled = sum(1 for row in rows if int_value(row["best_active_active_overfilled_hour_count"]) > 0)
    active_ratio_over_1 = sum(1 for row in rows if float_value(row["best_active_active_coverage_ratio"]) > 1.0)
    active_ratio_over_105 = sum(1 for row in rows if float_value(row["best_active_active_coverage_ratio"]) > 1.05)
    max_active_ratio = max((float_value(row["best_active_active_coverage_ratio"]) for row in rows), default=0.0)
    normalized_active_overfilled = sum(
        1 for row in rows if int_value(row["best_normalized_active_normalized_active_overfilled_hour_count"]) > 0
    )
    normalized_active_ratio_over_1 = sum(
        1 for row in rows if float_value(row["best_normalized_active_normalized_active_coverage_ratio"]) > 1.0
    )
    normalized_active_ratio_over_105 = sum(
        1 for row in rows if float_value(row["best_normalized_active_normalized_active_coverage_ratio"]) > 1.05
    )
    max_normalized_active_ratio = max(
        (float_value(row["best_normalized_active_normalized_active_coverage_ratio"]) for row in rows),
        default=0.0,
    )

    current_rows = [{"class": key, "rows": f"{value:,}"} for key, value in current_counts.most_common()]
    active_rows = [{"class": key, "rows": f"{value:,}"} for key, value in active_counts.most_common()]
    normalized_active_rows = [
        {"class": key, "rows": f"{value:,}"} for key, value in normalized_active_counts.most_common()
    ]
    state_rows = [{"plant_state": key, "rows": f"{value:,}"} for key, value in state_counts.most_common(20)]
    overfill_examples = sorted(
        (row for row in rows if int_value(row["best_active_active_overfilled_hour_count"]) > 0),
        key=lambda row: float_value(row["best_active_active_coverage_ratio"]),
        reverse=True,
    )[:20]
    still_fails_examples = sorted(
        (row for row in rows if row["active_window_class"] == "still_fails_active_window_coverage"),
        key=lambda row: float_value(row["best_active_coverage_ratio"]),
        reverse=True,
    )[:20]
    normalized_still_fails_examples = sorted(
        (
            row
            for row in rows
            if row["normalized_active_window_class"] == "still_fails_normalized_active_window_coverage"
        ),
        key=lambda row: float_value(row["best_normalized_active_coverage_ratio"]),
        reverse=True,
    )[:20]

    lines = [
        "# Fixed-Period Denominator Diagnostic",
        "",
        f"Generated UTC: {utc_now().isoformat(timespec='seconds')}",
        "",
        "## Run",
        "",
        f"- Diagnostic run ID: `{run_id}`",
        f"- Code commit: `{code_commit}`",
        f"- Plant scope: `{plant_scope}`",
        f"- Plant ECWT run ID: `{plant_ecwt_run_id}`",
        f"- Readiness run ID: `{readiness_run_id or '(not found)'}`",
        f"- Candidate run ID: `{candidate_run_id}`",
        f"- Station ECWT run ID: `{station_ecwt_run_id}`",
        f"- Station-year coverage run ID: `{coverage_run_id}`",
        f"- Station-year coverage table: `{coverage_table}`",
        f"- Fixed period: `{fixed_min_year}-{fixed_max_year}`",
        f"- Fixed minimum coverage ratio: `{fixed_min_coverage_ratio}`",
        f"- Fixed minimum loaded station-years: `{fixed_min_loaded_years}`",
        f"- Detail CSV: `{detail_csv.name}`",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| Blocked plant rows in scope | {len(rows):,} |",
        f"| Active-window coverage pass, any candidate | {active_coverage_any:,} |",
        f"| Active-window coverage plus 20 loaded fixed years pass, any candidate | {active_abs_loaded_any:,} |",
        f"| Active-window coverage plus active-loaded-year-ratio pass, any candidate | {active_window_any:,} |",
        f"| Normalized active-window coverage pass, any candidate | {normalized_active_coverage_any:,} |",
        f"| Normalized active-window coverage plus 20 loaded fixed years pass, any candidate | {normalized_active_abs_loaded_any:,} |",
        f"| Normalized active-window coverage plus active-loaded-year-ratio pass, any candidate | {normalized_active_window_any:,} |",
        f"| Best active-window candidate has valid hours beyond active expected hours | {active_overfilled:,} |",
        f"| Best active-window coverage ratio > 1.00 | {active_ratio_over_1:,} |",
        f"| Best active-window coverage ratio > 1.05 | {active_ratio_over_105:,} |",
        f"| Maximum best active-window coverage ratio | {max_active_ratio:.3f} |",
        f"| Best normalized active-window candidate has valid hours beyond normalized expected hours | {normalized_active_overfilled:,} |",
        f"| Best normalized active-window coverage ratio > 1.00 | {normalized_active_ratio_over_1:,} |",
        f"| Best normalized active-window coverage ratio > 1.05 | {normalized_active_ratio_over_105:,} |",
        f"| Maximum best normalized active-window coverage ratio | {max_normalized_active_ratio:.3f} |",
        "",
        "## Current Fixed-Period Blocker Classes",
        "",
    ]
    render_table(lines, ["Class", "Rows"], current_rows, ["class", "rows"])
    lines.extend(["", "## Raw Active-Window Sensitivity Classes", ""])
    render_table(lines, ["Class", "Rows"], active_rows, ["class", "rows"])
    lines.extend(["", "## Normalized Active-Window Sensitivity Classes", ""])
    render_table(lines, ["Class", "Rows"], normalized_active_rows, ["class", "rows"])
    lines.extend(["", "## Top Blocked Plant States", ""])
    render_table(lines, ["Plant State", "Rows"], state_rows, ["plant_state", "rows"])
    lines.extend(["", "## Active-Window Overfill Examples", ""])
    render_table(
        lines,
        ["Plant", "State", "Station", "Active Ratio", "Active Valid", "Active Expected", "Overfilled Hours", "First Obs", "Last Obs"],
        overfill_examples,
        [
            "plant_name",
            "plant_state",
            "best_active_station_id",
            "best_active_active_coverage_ratio",
            "best_active_active_valid_djf_hours",
            "best_active_active_expected_djf_hours",
            "best_active_active_overfilled_hour_count",
            "best_active_station_first_observation_utc",
            "best_active_station_last_observation_utc",
        ],
    )
    lines.extend(["", "## Still Fails Active-Window Coverage Examples", ""])
    render_table(
        lines,
        ["Plant", "State", "Station", "Active Ratio", "Fixed Ratio", "Active Loaded Year Ratio", "Distance km", "Rank"],
        still_fails_examples,
        [
            "plant_name",
            "plant_state",
            "best_active_station_id",
            "best_active_active_coverage_ratio",
            "best_active_fixed_coverage_ratio",
            "best_active_active_loaded_year_ratio",
            "best_active_distance_km",
            "best_active_rank_order",
        ],
    )
    lines.extend(["", "## Still Fails Normalized Active-Window Coverage Examples", ""])
    render_table(
        lines,
        ["Plant", "State", "Station", "Normalized Ratio", "Fixed Ratio", "Normalized Loaded Year Ratio", "Distance km", "Rank"],
        normalized_still_fails_examples,
        [
            "plant_name",
            "plant_state",
            "best_normalized_active_station_id",
            "best_normalized_active_normalized_active_coverage_ratio",
            "best_normalized_active_fixed_coverage_ratio",
            "best_normalized_active_normalized_active_loaded_year_ratio",
            "best_normalized_active_distance_km",
            "best_normalized_active_rank_order",
        ],
    )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- The current fixed-period gate uses the full 2000-2025 DJF denominator for station eligibility, plus a 20 loaded station-year minimum.",
            "- The raw active-window sensitivity uses NOAA station first/last observation metadata to shrink the expected-hour denominator before testing coverage.",
            f"- The normalized active-window sensitivity expands each station window to the union of NOAA station metadata bounds and full loaded station-years observed in `{coverage_table}`.",
            "- A large active-window pass count means the full fixed-period denominator is the dominant blocker for many plants.",
            "- Raw active-window ratios above 1.00 are a warning sign, not a pass recommendation: they mean the loaded annual file contributes more valid DJF hours than the station metadata active window expects.",
            "- Normalized active-window overfill counts should be zero or near zero; nonzero values would indicate the normalization rule still understates actual loaded observations.",
            "- This diagnostic supports a methodology decision. It does not change publication readiness or plant ECWT selection by itself.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    run_started_at = utc_now()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--psql", type=Path, default=PSQL)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5436)
    parser.add_argument("--dbname", default="eop012")
    parser.add_argument("--user")
    parser.add_argument("--plant-ecwt-run-id")
    parser.add_argument("--plant-scope", choices=["first-operable", "all-plants"], default="first-operable")
    args = parser.parse_args()

    plant_ecwt_run_id = args.plant_ecwt_run_id or latest_fixed_plant_ecwt_run_id(
        args.psql, args.host, args.port, args.dbname, args.user
    )
    if not plant_ecwt_run_id:
        raise RuntimeError("No fixed-period plant ECWT run found.")

    params = fetch_json_params(args.psql, args.host, args.port, args.dbname, args.user, plant_ecwt_run_id)
    candidate_run_id = str(params["candidate_run_id"])
    station_ecwt_run_id = str(params["station_ecwt_run_id"])
    coverage_run_id = str(params["coverage_run_id"])
    coverage_table = str(params.get("coverage_table") or "weather.station_year_djf_coverage")
    fixed_min_year = int(params["fixed_min_year"])
    fixed_max_year = int(params["fixed_max_year"])
    fixed_min_coverage_ratio = float(params["fixed_min_coverage_ratio"])
    fixed_min_loaded_years = int(params["fixed_min_loaded_years"])
    readiness_run_id = latest_readiness_run_id(args.psql, args.host, args.port, args.dbname, args.user, plant_ecwt_run_id)

    blocked_plants = psql_csv_query(
        args.psql,
        args.host,
        args.port,
        args.dbname,
        args.user,
        blocked_plants_query(plant_ecwt_run_id, args.plant_scope),
    )
    candidates = psql_csv_query(
        args.psql,
        args.host,
        args.port,
        args.dbname,
        args.user,
        candidate_rows_query(plant_ecwt_run_id, candidate_run_id, station_ecwt_run_id, args.plant_scope),
    )
    coverage_rows = psql_csv_query(
        args.psql,
        args.host,
        args.port,
        args.dbname,
        args.user,
        coverage_rows_query(coverage_run_id, coverage_table, fixed_min_year, fixed_max_year),
    )
    station_metrics = build_station_metrics(candidates, coverage_rows, fixed_min_year, fixed_max_year)
    rows = build_detail_rows(
        blocked_plants,
        candidates,
        station_metrics,
        fixed_min_coverage_ratio,
        fixed_min_loaded_years,
    )

    run_id = f"fixed_period_denominator_diagnostic_{args.plant_scope}_{utc_now().strftime('%Y%m%dT%H%M%SZ')}"
    code_commit = git_commit_label(args.project_root)
    docs_dir = args.project_root / "docs"
    detail_csv = docs_dir / f"{run_id}.csv"
    report_path = docs_dir / f"{run_id}_report.md"
    fieldnames = list(rows[0].keys()) if rows else []
    write_csv(detail_csv, fieldnames, rows)
    render_report(
        report_path,
        run_id,
        code_commit,
        plant_ecwt_run_id,
        readiness_run_id,
        candidate_run_id,
        station_ecwt_run_id,
        coverage_run_id,
        coverage_table,
        fixed_min_year,
        fixed_max_year,
        fixed_min_coverage_ratio,
        fixed_min_loaded_years,
        args.plant_scope,
        detail_csv,
        rows,
    )
    register_calculation_run(
        args.psql,
        args.host,
        args.port,
        args.dbname,
        args.user,
        run_id,
        code_commit,
        run_started_at,
        {
            "plant_scope": args.plant_scope,
            "plant_ecwt_run_id": plant_ecwt_run_id,
            "readiness_run_id": readiness_run_id,
            "candidate_run_id": candidate_run_id,
            "station_ecwt_run_id": station_ecwt_run_id,
            "coverage_run_id": coverage_run_id,
            "coverage_table": coverage_table,
            "fixed_min_year": fixed_min_year,
            "fixed_max_year": fixed_max_year,
            "fixed_min_coverage_ratio": fixed_min_coverage_ratio,
            "fixed_min_loaded_years": fixed_min_loaded_years,
            "blocked_rows": len(rows),
            "candidate_rows": len(candidates),
            "coverage_rows": len(coverage_rows),
            "detail_csv": str(detail_csv),
            "report_path": str(report_path),
        },
    )
    print(
        json.dumps(
            OrderedDict(
                [
                    ("run_id", run_id),
                    ("plant_scope", args.plant_scope),
                    ("plant_ecwt_run_id", plant_ecwt_run_id),
                    ("coverage_table", coverage_table),
                    ("blocked_rows", len(rows)),
                    ("candidate_rows", len(candidates)),
                    ("coverage_rows", len(coverage_rows)),
                    ("detail_csv", str(detail_csv)),
                    ("report_path", str(report_path)),
                ]
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
