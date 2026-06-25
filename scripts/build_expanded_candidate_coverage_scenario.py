#!/usr/bin/env python3
"""Audit whether broader station-candidate search can remediate coverage gaps."""

from __future__ import annotations

import argparse
import csv
import io
import json
import math
import subprocess
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import median
from typing import Iterable

from eop012_config import PROJECT_ROOT, PSQL, STAGING_ROOT


METHODOLOGY_VERSION = "eop012-ecwt-method-v0.1.0"
SOURCE_FAMILY = "expanded_candidate_coverage_scenario"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def sql_literal(value: object) -> str:
    if value is None:
        return "null"
    text = str(value)
    return "'" + text.replace("'", "''") + "'"


def sql_list(values: Iterable[str]) -> str:
    items = list(dict.fromkeys(values))
    if not items:
        return "null"
    return ", ".join(sql_literal(item) for item in items)


def pg_csv_value(value: object) -> object:
    if value is None:
        return r"\N"
    text = str(value)
    return r"\N" if text == "" else text


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


def psql_cmd(psql: Path, host: str, port: int, dbname: str, user: str | None = None) -> list[str]:
    cmd = [str(psql), "-h", host, "-p", str(port)]
    if user:
        cmd.extend(["-U", user])
    cmd.extend(["-d", dbname, "-v", "ON_ERROR_STOP=1"])
    return cmd


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


def psql_scalar(psql: Path, host: str, port: int, dbname: str, user: str | None, query: str) -> str:
    result = run(psql_cmd(psql, host, port, dbname, user) + ["-At", "-c", query])
    return result.stdout.strip()


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: pg_csv_value(row.get(field)) for field in fieldnames})


def git_commit_label(project_root: Path) -> str:
    try:
        head = run(["git", "-C", str(project_root), "rev-parse", "HEAD"]).stdout.strip()
        dirty = run(["git", "-C", str(project_root), "status", "--porcelain"]).stdout.strip()
        return f"{head}-dirty" if dirty else head
    except Exception:
        return "UNKNOWN_GIT_COMMIT"


def latest_successful_run_id(
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
        where calculation_run_id like {sql_literal(prefix + '%')}
          and run_status = 'succeeded'
        order by run_finished_at_utc desc nulls last, calculation_run_id desc
        limit 1;
        """,
    )
    if not run_id:
        raise RuntimeError(f"No succeeded calculation run found with prefix {prefix!r}.")
    return run_id


def parse_ts(value: str | None) -> datetime | None:
    if not value:
        return None
    text = value.strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def int_value(value: object, default: int = 0) -> int:
    if value in (None, ""):
        return default
    return int(float(str(value)))


def float_value(value: object, default: float = 0.0) -> float:
    if value in (None, ""):
        return default
    return float(str(value))


def fmt_float(value: float | None, digits: int = 6) -> str:
    return "" if value is None else f"{value:.{digits}f}"


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius_km = 6371.0088
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    return 2 * radius_km * math.asin(math.sqrt(a))


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
        for seg_start, seg_end in (
            (datetime(year, 1, 1, tzinfo=timezone.utc), datetime(year, 3, 1, tzinfo=timezone.utc)),
            (datetime(year, 12, 1, tzinfo=timezone.utc), datetime(year + 1, 1, 1, tzinfo=timezone.utc)),
        ):
            left = max(seg_start, active_start)
            right = min(seg_end, active_end)
            if right > left:
                total += (right - left).total_seconds() / 3600.0
        by_year[year] = int(round(total))
    return by_year


def fetch_priority_rows(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    priority_run_id: str,
    max_gap_hours: int,
) -> list[dict[str, str]]:
    return psql_csv_query(
        psql,
        host,
        port,
        dbname,
        user,
        f"""
        select
            p.priority_run_id,
            p.priority_rank::text,
            p.priority_bucket,
            p.plant_id,
            p.eia_plant_code,
            p.plant_name,
            p.plant_state,
            p.plant_county,
            p.nerc_region,
            p.balancing_authority_code,
            p.sector_name,
            a.latitude::text as plant_latitude,
            a.longitude::text as plant_longitude,
            p.valid_hour_gap_to_threshold::text,
            p.candidate_count::text,
            p.normalized_active_coverage_eligible_candidate_count::text,
            p.best_station_id as current_station_id,
            p.best_station_name as current_station_name,
            p.best_station_state as current_station_state,
            p.best_station_country as current_station_country,
            p.best_distance_km::text as current_distance_km,
            p.best_rank_order::text as current_rank_order,
            p.normalized_expected_djf_hours::text as current_normalized_expected_djf_hours,
            p.normalized_valid_djf_hours::text as current_normalized_valid_djf_hours,
            p.normalized_coverage_ratio::text as current_normalized_coverage_ratio,
            p.normalized_loaded_year_ratio::text as current_normalized_loaded_year_ratio
        from calc.coverage_blocker_priority p
        join asset.plant a on a.plant_id = p.plant_id
        where p.priority_run_id = {sql_literal(priority_run_id)}
          and p.valid_hour_gap_to_threshold <= {int(max_gap_hours)}
          and a.latitude is not null
          and a.longitude is not null
        order by p.priority_rank
        """,
    )


def fetch_station_ecwt_rows(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    station_ecwt_run_id: str,
) -> dict[str, dict[str, str]]:
    rows = psql_csv_query(
        psql,
        host,
        port,
        dbname,
        user,
        f"""
        select
            station_id,
            valid_hour_count::text,
            expected_hour_count::text,
            missing_hour_count::text,
            ecwt_f::text,
            ecwt_discrete_f::text,
            result_status
        from calc.station_ecwt
        where calculation_run_id = {sql_literal(station_ecwt_run_id)}
        """,
    )
    return {row["station_id"]: row for row in rows}


def fetch_station_rows(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    station_ecwt_run_id: str,
) -> list[dict[str, str]]:
    return psql_csv_query(
        psql,
        host,
        port,
        dbname,
        user,
        f"""
        select
            s.station_id,
            s.station_name,
            s.state as station_state,
            s.country as station_country,
            s.latitude::text,
            s.longitude::text,
            s.elevation_m::text,
            s.first_observation_utc::text,
            s.last_observation_utc::text
        from weather.station s
        join calc.station_ecwt se
          on se.station_id = s.station_id
         and se.calculation_run_id = {sql_literal(station_ecwt_run_id)}
         and se.result_status = 'provisional'
        where s.latitude is not null
          and s.longitude is not null
        """,
    )


def fetch_coverage_rows(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    coverage_run_id: str,
    station_ids: list[str],
    min_year: int,
    max_year: int,
) -> dict[str, dict[int, dict[str, str]]]:
    rows = psql_csv_query(
        psql,
        host,
        port,
        dbname,
        user,
        f"""
        select
            station_id,
            source_year::text,
            valid_djf_hours::text,
            loaded_file_count::text,
            coverage_status
        from weather.station_year_djf_coverage
        where calculation_run_id = {sql_literal(coverage_run_id)}
          and station_id in ({sql_list(station_ids)})
          and source_year between {int(min_year)} and {int(max_year)}
        """,
    )
    by_station: dict[str, dict[int, dict[str, str]]] = defaultdict(dict)
    for row in rows:
        by_station[row["station_id"]][int(row["source_year"])] = row
    return by_station


def build_station_metrics(
    station_rows: list[dict[str, str]],
    coverage_rows: dict[str, dict[int, dict[str, str]]],
    station_ecwt: dict[str, dict[str, str]],
    min_year: int,
    max_year: int,
    min_coverage_ratio: float,
    min_loaded_year_ratio: float,
) -> list[dict[str, object]]:
    metrics: list[dict[str, object]] = []
    for station in station_rows:
        station_id = station["station_id"]
        first_obs = parse_ts(station.get("first_observation_utc"))
        last_obs = parse_ts(station.get("last_observation_utc"))
        station_coverage = coverage_rows.get(station_id, {})
        loaded_year_values = [
            year for year, row in station_coverage.items() if int_value(row.get("loaded_file_count")) > 0
        ]
        first_loaded_year = min(loaded_year_values) if loaded_year_values else None
        last_loaded_year = max(loaded_year_values) if loaded_year_values else None
        loaded_start = datetime(first_loaded_year, 1, 1, tzinfo=timezone.utc) if first_loaded_year else None
        loaded_end = datetime(last_loaded_year, 12, 31, 23, tzinfo=timezone.utc) if last_loaded_year else None
        normalized_first = min([dt for dt in (first_obs, loaded_start) if dt is not None], default=None)
        normalized_last = max([dt for dt in (last_obs, loaded_end) if dt is not None], default=None)
        expected_by_year = active_expected_by_year(normalized_first, normalized_last, min_year, max_year)
        expected = sum(expected_by_year.values())
        valid = 0
        active_years = 0
        loaded_years = 0
        for year, expected_hours in expected_by_year.items():
            if expected_hours <= 0:
                continue
            active_years += 1
            coverage = station_coverage.get(year)
            if coverage:
                valid += int_value(coverage.get("valid_djf_hours"))
                if int_value(coverage.get("loaded_file_count")) > 0:
                    loaded_years += 1
        coverage_ratio = valid / expected if expected else 0.0
        loaded_year_ratio = loaded_years / active_years if active_years else 0.0
        ecwt = station_ecwt.get(station_id, {})
        metrics.append(
            {
                "station_id": station_id,
                "station_name": station.get("station_name", ""),
                "station_state": station.get("station_state", ""),
                "station_country": station.get("station_country", ""),
                "latitude": float_value(station.get("latitude")),
                "longitude": float_value(station.get("longitude")),
                "first_loaded_year": first_loaded_year,
                "last_loaded_year": last_loaded_year,
                "normalized_expected_djf_hours": expected,
                "normalized_valid_djf_hours": valid,
                "normalized_missing_djf_hours": max(expected - valid, 0),
                "normalized_coverage_ratio": coverage_ratio,
                "normalized_loaded_year_ratio": loaded_year_ratio,
                "active_years": active_years,
                "loaded_years": loaded_years,
                "coverage_pass": coverage_ratio >= min_coverage_ratio,
                "window_pass": coverage_ratio >= min_coverage_ratio and loaded_year_ratio >= min_loaded_year_ratio,
                "station_ecwt_valid_hour_count": int_value(ecwt.get("valid_hour_count")),
                "station_ecwt_f": float_value(ecwt.get("ecwt_f")) if ecwt.get("ecwt_f") else None,
                "station_ecwt_discrete_f": float_value(ecwt.get("ecwt_discrete_f")) if ecwt.get("ecwt_discrete_f") else None,
                "station_ecwt_status": ecwt.get("result_status", ""),
            }
        )
    return metrics


def station_grid(stations: list[dict[str, object]]) -> dict[tuple[int, int], list[dict[str, object]]]:
    grid: dict[tuple[int, int], list[dict[str, object]]] = defaultdict(list)
    for station in stations:
        grid[(math.floor(float(station["latitude"])), math.floor(float(station["longitude"])))].append(station)
    return grid


def nearby_stations(
    plant_lat: float,
    plant_lon: float,
    grid: dict[tuple[int, int], list[dict[str, object]]],
    radius_km: float,
) -> list[tuple[float, dict[str, object]]]:
    lat_delta = radius_km / 111.0
    cos_lat = max(0.15, abs(math.cos(math.radians(plant_lat))))
    lon_delta = radius_km / (111.0 * cos_lat)
    found: list[tuple[float, dict[str, object]]] = []
    for lat_bin in range(math.floor(plant_lat - lat_delta), math.floor(plant_lat + lat_delta) + 1):
        for lon_bin in range(math.floor(plant_lon - lon_delta), math.floor(plant_lon + lon_delta) + 1):
            for station in grid.get((lat_bin, lon_bin), []):
                distance = haversine_km(plant_lat, plant_lon, float(station["latitude"]), float(station["longitude"]))
                if distance <= radius_km:
                    found.append((distance, station))
    found.sort(key=lambda item: item[0])
    return found


PLANT_FIELDS = [
    "scenario_run_id",
    "priority_run_id",
    "coverage_run_id",
    "station_ecwt_run_id",
    "plant_id",
    "eia_plant_code",
    "plant_name",
    "plant_state",
    "plant_county",
    "nerc_region",
    "balancing_authority_code",
    "sector_name",
    "plant_latitude",
    "plant_longitude",
    "priority_rank",
    "priority_bucket",
    "valid_hour_gap_to_threshold",
    "current_station_id",
    "current_station_name",
    "current_station_state",
    "current_station_country",
    "current_distance_km",
    "current_rank_order",
    "current_normalized_coverage_ratio",
    "current_normalized_loaded_year_ratio",
    "current_candidate_count",
    "current_eligible_candidate_count",
    "search_radius_km",
    "stations_searched_within_radius",
    "passing_station_count_within_radius",
    "nearest_pass_radius_bucket_km",
    "nearest_pass_rank_order_within_radius",
    "nearest_pass_station_id",
    "nearest_pass_station_name",
    "nearest_pass_station_state",
    "nearest_pass_station_country",
    "nearest_pass_distance_km",
    "nearest_pass_normalized_expected_djf_hours",
    "nearest_pass_normalized_valid_djf_hours",
    "nearest_pass_normalized_missing_djf_hours",
    "nearest_pass_normalized_coverage_ratio",
    "nearest_pass_normalized_loaded_year_ratio",
    "nearest_pass_loaded_years",
    "nearest_pass_active_years",
    "nearest_pass_station_ecwt_valid_hour_count",
    "nearest_pass_station_ecwt_f",
    "nearest_pass_station_ecwt_discrete_f",
    "scenario_status",
    "notes",
]


RADIUS_FIELDS = [
    "scenario_run_id",
    "priority_run_id",
    "coverage_run_id",
    "station_ecwt_run_id",
    "radius_km",
    "plant_count",
    "plants_with_passing_station",
    "plants_without_passing_station",
    "pass_rate",
    "min_nearest_pass_distance_km",
    "median_nearest_pass_distance_km",
    "max_nearest_pass_distance_km",
    "median_nearest_pass_rank_order",
]


STATE_FIELDS = [
    "scenario_run_id",
    "priority_run_id",
    "coverage_run_id",
    "station_ecwt_run_id",
    "plant_state",
    "plant_count",
    "plants_with_passing_station_within_search_radius",
    "nearest_pass_radius_buckets",
    "median_nearest_pass_distance_km",
    "max_nearest_pass_distance_km",
]


def build_rows(
    run_id: str,
    priority_run_id: str,
    coverage_run_id: str,
    station_ecwt_run_id: str,
    plants: list[dict[str, str]],
    station_metrics: list[dict[str, object]],
    radii: list[float],
) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    max_radius = max(radii)
    grid = station_grid(station_metrics)
    plant_rows: list[dict[str, object]] = []

    for plant in plants:
        plant_lat = float_value(plant["plant_latitude"])
        plant_lon = float_value(plant["plant_longitude"])
        nearby = nearby_stations(plant_lat, plant_lon, grid, max_radius)
        passing = [(idx, distance, station) for idx, (distance, station) in enumerate(nearby, start=1) if station["window_pass"]]
        nearest = passing[0] if passing else None
        pass_radius = None
        if nearest:
            pass_radius = next((radius for radius in radii if nearest[1] <= radius), None)
        passing_count = len(passing)
        if nearest:
            rank, distance, station = nearest
            status = "expanded_candidate_passes_coverage_gate"
            notes = "Nearest passing station within expanded scenario search radius; not applied to official station selection."
        else:
            rank, distance, station = None, None, {}
            status = "no_passing_station_within_search_radius"
            notes = "No station with provisional station ECWT and normalized active-window coverage pass within expanded scenario search radius."

        plant_rows.append(
            {
                "scenario_run_id": run_id,
                "priority_run_id": priority_run_id,
                "coverage_run_id": coverage_run_id,
                "station_ecwt_run_id": station_ecwt_run_id,
                "plant_id": plant["plant_id"],
                "eia_plant_code": plant.get("eia_plant_code", ""),
                "plant_name": plant.get("plant_name", ""),
                "plant_state": plant.get("plant_state", ""),
                "plant_county": plant.get("plant_county", ""),
                "nerc_region": plant.get("nerc_region", ""),
                "balancing_authority_code": plant.get("balancing_authority_code", ""),
                "sector_name": plant.get("sector_name", ""),
                "plant_latitude": plant.get("plant_latitude", ""),
                "plant_longitude": plant.get("plant_longitude", ""),
                "priority_rank": plant.get("priority_rank", ""),
                "priority_bucket": plant.get("priority_bucket", ""),
                "valid_hour_gap_to_threshold": plant.get("valid_hour_gap_to_threshold", ""),
                "current_station_id": plant.get("current_station_id", ""),
                "current_station_name": plant.get("current_station_name", ""),
                "current_station_state": plant.get("current_station_state", ""),
                "current_station_country": plant.get("current_station_country", ""),
                "current_distance_km": plant.get("current_distance_km", ""),
                "current_rank_order": plant.get("current_rank_order", ""),
                "current_normalized_coverage_ratio": plant.get("current_normalized_coverage_ratio", ""),
                "current_normalized_loaded_year_ratio": plant.get("current_normalized_loaded_year_ratio", ""),
                "current_candidate_count": plant.get("candidate_count", ""),
                "current_eligible_candidate_count": plant.get("normalized_active_coverage_eligible_candidate_count", ""),
                "search_radius_km": fmt_float(max_radius, 3),
                "stations_searched_within_radius": len(nearby),
                "passing_station_count_within_radius": passing_count,
                "nearest_pass_radius_bucket_km": fmt_float(pass_radius, 3) if pass_radius is not None else "",
                "nearest_pass_rank_order_within_radius": rank or "",
                "nearest_pass_station_id": station.get("station_id", ""),
                "nearest_pass_station_name": station.get("station_name", ""),
                "nearest_pass_station_state": station.get("station_state", ""),
                "nearest_pass_station_country": station.get("station_country", ""),
                "nearest_pass_distance_km": fmt_float(distance, 3) if distance is not None else "",
                "nearest_pass_normalized_expected_djf_hours": station.get("normalized_expected_djf_hours", ""),
                "nearest_pass_normalized_valid_djf_hours": station.get("normalized_valid_djf_hours", ""),
                "nearest_pass_normalized_missing_djf_hours": station.get("normalized_missing_djf_hours", ""),
                "nearest_pass_normalized_coverage_ratio": fmt_float(station.get("normalized_coverage_ratio"), 6)
                if station
                else "",
                "nearest_pass_normalized_loaded_year_ratio": fmt_float(station.get("normalized_loaded_year_ratio"), 6)
                if station
                else "",
                "nearest_pass_loaded_years": station.get("loaded_years", ""),
                "nearest_pass_active_years": station.get("active_years", ""),
                "nearest_pass_station_ecwt_valid_hour_count": station.get("station_ecwt_valid_hour_count", ""),
                "nearest_pass_station_ecwt_f": fmt_float(station.get("station_ecwt_f"), 3) if station else "",
                "nearest_pass_station_ecwt_discrete_f": fmt_float(station.get("station_ecwt_discrete_f"), 3)
                if station
                else "",
                "scenario_status": status,
                "notes": notes,
            }
        )

    radius_rows: list[dict[str, object]] = []
    for radius in radii:
        passing_at_radius = [
            row
            for row in plant_rows
            if row["nearest_pass_distance_km"] not in ("", None)
            and float_value(row["nearest_pass_distance_km"]) <= radius
        ]
        distances = [float_value(row["nearest_pass_distance_km"]) for row in passing_at_radius]
        ranks = [int_value(row["nearest_pass_rank_order_within_radius"]) for row in passing_at_radius]
        radius_rows.append(
            {
                "scenario_run_id": run_id,
                "priority_run_id": priority_run_id,
                "coverage_run_id": coverage_run_id,
                "station_ecwt_run_id": station_ecwt_run_id,
                "radius_km": fmt_float(radius, 3),
                "plant_count": len(plant_rows),
                "plants_with_passing_station": len(passing_at_radius),
                "plants_without_passing_station": len(plant_rows) - len(passing_at_radius),
                "pass_rate": fmt_float(len(passing_at_radius) / len(plant_rows) if plant_rows else 0.0, 6),
                "min_nearest_pass_distance_km": fmt_float(min(distances), 3) if distances else "",
                "median_nearest_pass_distance_km": fmt_float(median(distances), 3) if distances else "",
                "max_nearest_pass_distance_km": fmt_float(max(distances), 3) if distances else "",
                "median_nearest_pass_rank_order": fmt_float(median(ranks), 1) if ranks else "",
            }
        )

    by_state: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in plant_rows:
        by_state[str(row["plant_state"] or "")].append(row)
    state_rows: list[dict[str, object]] = []
    for state, rows in by_state.items():
        passing = [row for row in rows if row["scenario_status"] == "expanded_candidate_passes_coverage_gate"]
        distances = [float_value(row["nearest_pass_distance_km"]) for row in passing]
        buckets = Counter(str(row["nearest_pass_radius_bucket_km"]) for row in passing if row["nearest_pass_radius_bucket_km"])
        state_rows.append(
            {
                "scenario_run_id": run_id,
                "priority_run_id": priority_run_id,
                "coverage_run_id": coverage_run_id,
                "station_ecwt_run_id": station_ecwt_run_id,
                "plant_state": state,
                "plant_count": len(rows),
                "plants_with_passing_station_within_search_radius": len(passing),
                "nearest_pass_radius_buckets": ";".join(f"{bucket}:{count}" for bucket, count in buckets.most_common()),
                "median_nearest_pass_distance_km": fmt_float(median(distances), 3) if distances else "",
                "max_nearest_pass_distance_km": fmt_float(max(distances), 3) if distances else "",
            }
        )
    state_rows.sort(key=lambda row: (-int_value(row["plant_count"]), row["plant_state"]))
    return plant_rows, radius_rows, state_rows


def copy_sql(table: str, columns: list[str], path: Path) -> str:
    return f"\\copy {table} ({', '.join(columns)}) from '{path}' with (format csv, header true, null '\\N')"


def temp_table_sql(table: str, columns: list[str]) -> str:
    return "create temp table " + table + " (\n" + ",\n".join(f"    {column} text" for column in columns) + "\n);"


def qident(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def text_null(field: str) -> str:
    return f"nullif({qident(field)}, '')"


def cast_null(field: str, cast_type: str) -> str:
    return f"nullif({qident(field)}, '')::{cast_type}"


def build_load_sql(
    run_id: str,
    code_commit: str,
    started_at: str,
    params: dict[str, object],
    plant_csv: Path,
    radius_csv: Path,
    state_csv: Path,
) -> str:
    return f"""
\\set ON_ERROR_STOP on
begin;

create table if not exists calc.expanded_candidate_coverage_scenario_plant (
    scenario_run_id text not null references audit.calculation_run(calculation_run_id),
    priority_run_id text not null references audit.calculation_run(calculation_run_id),
    coverage_run_id text not null references audit.calculation_run(calculation_run_id),
    station_ecwt_run_id text not null references audit.calculation_run(calculation_run_id),
    plant_id text not null references asset.plant(plant_id),
    eia_plant_code text,
    plant_name text,
    plant_state text,
    plant_county text,
    nerc_region text,
    balancing_authority_code text,
    sector_name text,
    plant_latitude numeric,
    plant_longitude numeric,
    priority_rank integer,
    priority_bucket text,
    valid_hour_gap_to_threshold bigint,
    current_station_id text,
    current_station_name text,
    current_station_state text,
    current_station_country text,
    current_distance_km numeric,
    current_rank_order integer,
    current_normalized_coverage_ratio numeric,
    current_normalized_loaded_year_ratio numeric,
    current_candidate_count integer,
    current_eligible_candidate_count integer,
    search_radius_km numeric,
    stations_searched_within_radius bigint,
    passing_station_count_within_radius bigint,
    nearest_pass_radius_bucket_km numeric,
    nearest_pass_rank_order_within_radius integer,
    nearest_pass_station_id text,
    nearest_pass_station_name text,
    nearest_pass_station_state text,
    nearest_pass_station_country text,
    nearest_pass_distance_km numeric,
    nearest_pass_normalized_expected_djf_hours bigint,
    nearest_pass_normalized_valid_djf_hours bigint,
    nearest_pass_normalized_missing_djf_hours bigint,
    nearest_pass_normalized_coverage_ratio numeric,
    nearest_pass_normalized_loaded_year_ratio numeric,
    nearest_pass_loaded_years integer,
    nearest_pass_active_years integer,
    nearest_pass_station_ecwt_valid_hour_count bigint,
    nearest_pass_station_ecwt_f numeric,
    nearest_pass_station_ecwt_discrete_f numeric,
    scenario_status text,
    notes text,
    created_at_utc timestamptz not null default now(),
    primary key (scenario_run_id, plant_id)
);
create index if not exists ix_expanded_candidate_scenario_plant_status
    on calc.expanded_candidate_coverage_scenario_plant (scenario_run_id, scenario_status, nearest_pass_radius_bucket_km);
create index if not exists ix_expanded_candidate_scenario_plant_station
    on calc.expanded_candidate_coverage_scenario_plant (scenario_run_id, nearest_pass_station_id);

create table if not exists calc.expanded_candidate_coverage_scenario_radius_summary (
    scenario_run_id text not null references audit.calculation_run(calculation_run_id),
    priority_run_id text not null references audit.calculation_run(calculation_run_id),
    coverage_run_id text not null references audit.calculation_run(calculation_run_id),
    station_ecwt_run_id text not null references audit.calculation_run(calculation_run_id),
    radius_km numeric not null,
    plant_count bigint,
    plants_with_passing_station bigint,
    plants_without_passing_station bigint,
    pass_rate numeric,
    min_nearest_pass_distance_km numeric,
    median_nearest_pass_distance_km numeric,
    max_nearest_pass_distance_km numeric,
    median_nearest_pass_rank_order numeric,
    created_at_utc timestamptz not null default now(),
    primary key (scenario_run_id, radius_km)
);

create table if not exists calc.expanded_candidate_coverage_scenario_state_summary (
    scenario_run_id text not null references audit.calculation_run(calculation_run_id),
    priority_run_id text not null references audit.calculation_run(calculation_run_id),
    coverage_run_id text not null references audit.calculation_run(calculation_run_id),
    station_ecwt_run_id text not null references audit.calculation_run(calculation_run_id),
    plant_state text not null,
    plant_count bigint,
    plants_with_passing_station_within_search_radius bigint,
    nearest_pass_radius_buckets text,
    median_nearest_pass_distance_km numeric,
    max_nearest_pass_distance_km numeric,
    created_at_utc timestamptz not null default now(),
    primary key (scenario_run_id, plant_state)
);

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
    'Audited whether broader station-candidate search would find ECWT-ready normalized active-window coverage candidates for near-threshold plant blockers.'
)
on conflict (calculation_run_id) do update set
    code_commit = excluded.code_commit,
    run_started_at_utc = excluded.run_started_at_utc,
    run_finished_at_utc = excluded.run_finished_at_utc,
    run_status = excluded.run_status,
    parameters_json = excluded.parameters_json,
    notes = excluded.notes;

{temp_table_sql("tmp_expanded_candidate_plant", PLANT_FIELDS)}
{copy_sql("tmp_expanded_candidate_plant", PLANT_FIELDS, plant_csv)}
{temp_table_sql("tmp_expanded_candidate_radius", RADIUS_FIELDS)}
{copy_sql("tmp_expanded_candidate_radius", RADIUS_FIELDS, radius_csv)}
{temp_table_sql("tmp_expanded_candidate_state", STATE_FIELDS)}
{copy_sql("tmp_expanded_candidate_state", STATE_FIELDS, state_csv)}

delete from calc.expanded_candidate_coverage_scenario_plant where scenario_run_id = {sql_literal(run_id)};
delete from calc.expanded_candidate_coverage_scenario_radius_summary where scenario_run_id = {sql_literal(run_id)};
delete from calc.expanded_candidate_coverage_scenario_state_summary where scenario_run_id = {sql_literal(run_id)};

insert into calc.expanded_candidate_coverage_scenario_plant (
    scenario_run_id,
    priority_run_id,
    coverage_run_id,
    station_ecwt_run_id,
    plant_id,
    eia_plant_code,
    plant_name,
    plant_state,
    plant_county,
    nerc_region,
    balancing_authority_code,
    sector_name,
    plant_latitude,
    plant_longitude,
    priority_rank,
    priority_bucket,
    valid_hour_gap_to_threshold,
    current_station_id,
    current_station_name,
    current_station_state,
    current_station_country,
    current_distance_km,
    current_rank_order,
    current_normalized_coverage_ratio,
    current_normalized_loaded_year_ratio,
    current_candidate_count,
    current_eligible_candidate_count,
    search_radius_km,
    stations_searched_within_radius,
    passing_station_count_within_radius,
    nearest_pass_radius_bucket_km,
    nearest_pass_rank_order_within_radius,
    nearest_pass_station_id,
    nearest_pass_station_name,
    nearest_pass_station_state,
    nearest_pass_station_country,
    nearest_pass_distance_km,
    nearest_pass_normalized_expected_djf_hours,
    nearest_pass_normalized_valid_djf_hours,
    nearest_pass_normalized_missing_djf_hours,
    nearest_pass_normalized_coverage_ratio,
    nearest_pass_normalized_loaded_year_ratio,
    nearest_pass_loaded_years,
    nearest_pass_active_years,
    nearest_pass_station_ecwt_valid_hour_count,
    nearest_pass_station_ecwt_f,
    nearest_pass_station_ecwt_discrete_f,
    scenario_status,
    notes
)
select
    {text_null("scenario_run_id")},
    {text_null("priority_run_id")},
    {text_null("coverage_run_id")},
    {text_null("station_ecwt_run_id")},
    {text_null("plant_id")},
    {text_null("eia_plant_code")},
    {text_null("plant_name")},
    {text_null("plant_state")},
    {text_null("plant_county")},
    {text_null("nerc_region")},
    {text_null("balancing_authority_code")},
    {text_null("sector_name")},
    {cast_null("plant_latitude", "numeric")},
    {cast_null("plant_longitude", "numeric")},
    {cast_null("priority_rank", "integer")},
    {text_null("priority_bucket")},
    {cast_null("valid_hour_gap_to_threshold", "bigint")},
    {text_null("current_station_id")},
    {text_null("current_station_name")},
    {text_null("current_station_state")},
    {text_null("current_station_country")},
    {cast_null("current_distance_km", "numeric")},
    {cast_null("current_rank_order", "integer")},
    {cast_null("current_normalized_coverage_ratio", "numeric")},
    {cast_null("current_normalized_loaded_year_ratio", "numeric")},
    {cast_null("current_candidate_count", "integer")},
    {cast_null("current_eligible_candidate_count", "integer")},
    {cast_null("search_radius_km", "numeric")},
    {cast_null("stations_searched_within_radius", "bigint")},
    {cast_null("passing_station_count_within_radius", "bigint")},
    {cast_null("nearest_pass_radius_bucket_km", "numeric")},
    {cast_null("nearest_pass_rank_order_within_radius", "integer")},
    {text_null("nearest_pass_station_id")},
    {text_null("nearest_pass_station_name")},
    {text_null("nearest_pass_station_state")},
    {text_null("nearest_pass_station_country")},
    {cast_null("nearest_pass_distance_km", "numeric")},
    {cast_null("nearest_pass_normalized_expected_djf_hours", "bigint")},
    {cast_null("nearest_pass_normalized_valid_djf_hours", "bigint")},
    {cast_null("nearest_pass_normalized_missing_djf_hours", "bigint")},
    {cast_null("nearest_pass_normalized_coverage_ratio", "numeric")},
    {cast_null("nearest_pass_normalized_loaded_year_ratio", "numeric")},
    {cast_null("nearest_pass_loaded_years", "integer")},
    {cast_null("nearest_pass_active_years", "integer")},
    {cast_null("nearest_pass_station_ecwt_valid_hour_count", "bigint")},
    {cast_null("nearest_pass_station_ecwt_f", "numeric")},
    {cast_null("nearest_pass_station_ecwt_discrete_f", "numeric")},
    {text_null("scenario_status")},
    {text_null("notes")}
from tmp_expanded_candidate_plant;

insert into calc.expanded_candidate_coverage_scenario_radius_summary (
    scenario_run_id,
    priority_run_id,
    coverage_run_id,
    station_ecwt_run_id,
    radius_km,
    plant_count,
    plants_with_passing_station,
    plants_without_passing_station,
    pass_rate,
    min_nearest_pass_distance_km,
    median_nearest_pass_distance_km,
    max_nearest_pass_distance_km,
    median_nearest_pass_rank_order
)
select
    {text_null("scenario_run_id")},
    {text_null("priority_run_id")},
    {text_null("coverage_run_id")},
    {text_null("station_ecwt_run_id")},
    {cast_null("radius_km", "numeric")},
    {cast_null("plant_count", "bigint")},
    {cast_null("plants_with_passing_station", "bigint")},
    {cast_null("plants_without_passing_station", "bigint")},
    {cast_null("pass_rate", "numeric")},
    {cast_null("min_nearest_pass_distance_km", "numeric")},
    {cast_null("median_nearest_pass_distance_km", "numeric")},
    {cast_null("max_nearest_pass_distance_km", "numeric")},
    {cast_null("median_nearest_pass_rank_order", "numeric")}
from tmp_expanded_candidate_radius;

insert into calc.expanded_candidate_coverage_scenario_state_summary (
    scenario_run_id,
    priority_run_id,
    coverage_run_id,
    station_ecwt_run_id,
    plant_state,
    plant_count,
    plants_with_passing_station_within_search_radius,
    nearest_pass_radius_buckets,
    median_nearest_pass_distance_km,
    max_nearest_pass_distance_km
)
select
    {text_null("scenario_run_id")},
    {text_null("priority_run_id")},
    {text_null("coverage_run_id")},
    {text_null("station_ecwt_run_id")},
    {text_null("plant_state")},
    {cast_null("plant_count", "bigint")},
    {cast_null("plants_with_passing_station_within_search_radius", "bigint")},
    {text_null("nearest_pass_radius_buckets")},
    {cast_null("median_nearest_pass_distance_km", "numeric")},
    {cast_null("max_nearest_pass_distance_km", "numeric")}
from tmp_expanded_candidate_state;

commit;
"""


def render_table(lines: list[str], headers: list[str], rows: list[dict[str, object]], fields: list[str], limit: int | None = None) -> None:
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join("---" for _ in headers) + " |")
    selected = rows if limit is None else rows[:limit]
    for row in selected:
        lines.append("| " + " | ".join(str(row.get(field, "")) for field in fields) + " |")
    if limit is not None and len(rows) > limit:
        lines.append(f"| ... | {len(rows) - limit:,} more rows omitted | | | | | | | | |")


def render_report(
    run_id: str,
    params: dict[str, object],
    plant_rows: list[dict[str, object]],
    radius_rows: list[dict[str, object]],
    state_rows: list[dict[str, object]],
    docs_dir: Path,
) -> None:
    status_counts = Counter(row["scenario_status"] for row in plant_rows)
    pass_rows = [row for row in plant_rows if row["scenario_status"] == "expanded_candidate_passes_coverage_gate"]
    rank_values = [int_value(row["nearest_pass_rank_order_within_radius"]) for row in pass_rows]
    bucket_counts = Counter(str(row["nearest_pass_radius_bucket_km"]) for row in pass_rows if row["nearest_pass_radius_bucket_km"])
    top_states = [
        {
            "state": row["plant_state"],
            "plants": row["plant_count"],
            "passing": row["plants_with_passing_station_within_search_radius"],
            "buckets": row["nearest_pass_radius_buckets"],
            "median_distance": row["median_nearest_pass_distance_km"],
            "max_distance": row["max_nearest_pass_distance_km"],
        }
        for row in state_rows[:20]
    ]
    example_rows = sorted(
        pass_rows,
        key=lambda row: (float_value(row["nearest_pass_distance_km"]), int_value(row["priority_rank"])),
    )[:20]
    examples = [
        {
            "plant": row["eia_plant_code"],
            "state": row["plant_state"],
            "current": row["current_station_id"],
            "pass_station": row["nearest_pass_station_id"],
            "distance": row["nearest_pass_distance_km"],
            "rank": row["nearest_pass_rank_order_within_radius"],
            "coverage": row["nearest_pass_normalized_coverage_ratio"],
            "ecwt_f": row["nearest_pass_station_ecwt_f"],
        }
        for row in example_rows
    ]
    radius_display = [
        {
            "radius": row["radius_km"],
            "plants": row["plant_count"],
            "passing": row["plants_with_passing_station"],
            "not_passing": row["plants_without_passing_station"],
            "pass_rate": row["pass_rate"],
            "median_distance": row["median_nearest_pass_distance_km"],
            "median_rank": row["median_nearest_pass_rank_order"],
        }
        for row in radius_rows
    ]

    lines = [
        "# Expanded Candidate Coverage Scenario",
        "",
        f"- Scenario run ID: `{run_id}`",
        f"- Priority run ID: `{params['priority_run_id']}`",
        f"- Coverage run ID: `{params['coverage_run_id']}`",
        f"- Station ECWT run ID: `{params['station_ecwt_run_id']}`",
        f"- Search radii km: `{params['radii_km']}`",
        f"- Minimum normalized coverage ratio: `{params['min_coverage_ratio']}`",
        f"- Minimum normalized loaded-year ratio: `{params['min_loaded_year_ratio']}`",
        f"- Plant CSV: `{run_id}_plants.csv`",
        f"- Radius summary CSV: `{run_id}_radius_summary.csv`",
        f"- State summary CSV: `{run_id}_state_summary.csv`",
        "",
        "## Headline",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Near-threshold plants audited | {len(plant_rows):,} |",
        f"| Plants with passing expanded station within max radius | {len(pass_rows):,} |",
        f"| Plants without passing expanded station within max radius | {status_counts.get('no_passing_station_within_search_radius', 0):,} |",
        f"| Median nearest passing station rank among loaded stations | {median(rank_values):.1f} |" if rank_values else "| Median nearest passing station rank among loaded stations |  |",
        "",
        "## Radius Summary",
        "",
    ]
    render_table(
        lines,
        ["Radius km", "Plants", "Passing", "Not Passing", "Pass Rate", "Median Distance km", "Median Rank"],
        radius_display,
        ["radius", "plants", "passing", "not_passing", "pass_rate", "median_distance", "median_rank"],
    )
    lines.extend(["", "## Nearest Passing Radius Buckets", "", "| Bucket km | Plants |", "| --- | ---: |"])
    for bucket, count in sorted(bucket_counts.items(), key=lambda item: float_value(item[0])):
        lines.append(f"| {bucket} | {count:,} |")
    lines.extend(["", "## Top States", ""])
    render_table(
        lines,
        ["State", "Plants", "Passing", "Buckets", "Median Distance km", "Max Distance km"],
        top_states,
        ["state", "plants", "passing", "buckets", "median_distance", "max_distance"],
    )
    lines.extend(["", "## Nearest Passing Examples", ""])
    render_table(
        lines,
        ["Plant", "State", "Current Station", "Pass Station", "Distance km", "Rank", "Coverage", "ECWT F"],
        examples,
        ["plant", "state", "current", "pass_station", "distance", "rank", "coverage", "ecwt_f"],
    )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- This is a scenario audit only. It does not alter `link.station_candidate`, station selection, readiness, or plant ECWT results.",
            "- The scenario searches loaded stations with provisional station ECWT rows and requires normalized active-window coverage ratio and loaded-year ratio to meet the configured thresholds.",
            "- A pass means an ECWT-ready station exists within the searched radius under the coverage policy. It does not prove the station is meteorologically acceptable for the plant.",
            "- If this scenario is adopted, the real pipeline change is candidate expansion plus station-selection policy review, followed by a full plant ECWT/readiness rebuild.",
        ]
    )
    (docs_dir / f"{run_id}_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_radii(raw: str) -> list[float]:
    radii = sorted({float(item.strip()) for item in raw.split(",") if item.strip()})
    if not radii:
        raise ValueError("At least one radius is required.")
    return radii


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--staging-root", type=Path, default=STAGING_ROOT)
    parser.add_argument("--docs-dir", type=Path, default=PROJECT_ROOT / "docs")
    parser.add_argument("--psql", type=Path, default=PSQL)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5436)
    parser.add_argument("--dbname", default="eop012")
    parser.add_argument("--user", default=None)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--priority-run-id", default=None)
    parser.add_argument("--coverage-run-id", default=None)
    parser.add_argument("--station-ecwt-run-id", default=None)
    parser.add_argument("--max-gap-hours", type=int, default=168)
    parser.add_argument("--min-year", type=int, default=2000)
    parser.add_argument("--max-year", type=int, default=2025)
    parser.add_argument("--radii-km", default="50,75,100,150,250,500,1000")
    parser.add_argument("--min-coverage-ratio", type=float, default=0.95)
    parser.add_argument("--min-loaded-year-ratio", type=float, default=0.95)
    args = parser.parse_args()

    if not args.psql.exists():
        raise FileNotFoundError(args.psql)
    if args.min_year > args.max_year:
        raise ValueError("--min-year must be <= --max-year")
    radii = parse_radii(args.radii_km)

    priority_run_id = args.priority_run_id or latest_successful_run_id(
        args.psql, args.host, args.port, args.dbname, args.user, "normalized_active_window_blocker_priority_"
    )
    coverage_run_id = args.coverage_run_id or latest_successful_run_id(
        args.psql, args.host, args.port, args.dbname, args.user, "station_year_djf_coverage_"
    )
    station_ecwt_run_id = args.station_ecwt_run_id or latest_successful_run_id(
        args.psql, args.host, args.port, args.dbname, args.user, "station_ecwt_loaded_"
    )

    code_commit = git_commit_label(args.project_root)
    run_timestamp = utc_now().strftime("%Y%m%dT%H%M%SZ")
    run_id = args.run_id or f"expanded_candidate_coverage_scenario_{run_timestamp}"
    staging_dir = args.staging_root / run_id
    staging_dir.mkdir(parents=True, exist_ok=True)
    args.docs_dir.mkdir(parents=True, exist_ok=True)

    plants = fetch_priority_rows(args.psql, args.host, args.port, args.dbname, args.user, priority_run_id, args.max_gap_hours)
    station_ecwt = fetch_station_ecwt_rows(args.psql, args.host, args.port, args.dbname, args.user, station_ecwt_run_id)
    stations = fetch_station_rows(args.psql, args.host, args.port, args.dbname, args.user, station_ecwt_run_id)
    coverage = fetch_coverage_rows(
        args.psql,
        args.host,
        args.port,
        args.dbname,
        args.user,
        coverage_run_id,
        [row["station_id"] for row in stations],
        args.min_year,
        args.max_year,
    )
    station_metrics = build_station_metrics(
        stations,
        coverage,
        station_ecwt,
        args.min_year,
        args.max_year,
        args.min_coverage_ratio,
        args.min_loaded_year_ratio,
    )
    plant_rows, radius_rows, state_rows = build_rows(
        run_id,
        priority_run_id,
        coverage_run_id,
        station_ecwt_run_id,
        plants,
        station_metrics,
        radii,
    )

    plant_staging = staging_dir / f"{run_id}_plants.csv"
    radius_staging = staging_dir / f"{run_id}_radius_summary.csv"
    state_staging = staging_dir / f"{run_id}_state_summary.csv"
    plant_doc = args.docs_dir / f"{run_id}_plants.csv"
    radius_doc = args.docs_dir / f"{run_id}_radius_summary.csv"
    state_doc = args.docs_dir / f"{run_id}_state_summary.csv"
    write_csv(plant_staging, PLANT_FIELDS, plant_rows)
    write_csv(radius_staging, RADIUS_FIELDS, radius_rows)
    write_csv(state_staging, STATE_FIELDS, state_rows)
    write_csv(plant_doc, PLANT_FIELDS, plant_rows)
    write_csv(radius_doc, RADIUS_FIELDS, radius_rows)
    write_csv(state_doc, STATE_FIELDS, state_rows)

    params = {
        "source_family": SOURCE_FAMILY,
        "priority_run_id": priority_run_id,
        "coverage_run_id": coverage_run_id,
        "station_ecwt_run_id": station_ecwt_run_id,
        "max_gap_hours": args.max_gap_hours,
        "min_year": args.min_year,
        "max_year": args.max_year,
        "radii_km": radii,
        "min_coverage_ratio": args.min_coverage_ratio,
        "min_loaded_year_ratio": args.min_loaded_year_ratio,
        "plant_rows": len(plant_rows),
        "station_metric_rows": len(station_metrics),
    }
    started_at = utc_now().isoformat(timespec="seconds")
    sql = build_load_sql(run_id, code_commit, started_at, params, plant_staging, radius_staging, state_staging)
    run(psql_cmd(args.psql, args.host, args.port, args.dbname, args.user), input_text=sql)
    render_report(run_id, params, plant_rows, radius_rows, state_rows, args.docs_dir)

    pass_count = sum(1 for row in plant_rows if row["scenario_status"] == "expanded_candidate_passes_coverage_gate")
    print(f"run_id={run_id}")
    print(f"plant_rows={len(plant_rows)}")
    print(f"station_metric_rows={len(station_metrics)}")
    print(f"plants_with_passing_station_within_max_radius={pass_count}")
    print(f"plants_without_passing_station_within_max_radius={len(plant_rows) - pass_count}")
    print(f"report={args.docs_dir / f'{run_id}_report.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
