#!/usr/bin/env python3
"""Load NOAA ISD station metadata and nearest plant-station candidates."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import re
import shutil
import subprocess
import sys
import urllib.request
from collections import OrderedDict, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from eop012_config import PROJECT_ROOT, PSQL, STAGING_ROOT, STATION_HISTORY_CSV
from station_filters import is_land_plant_station_eligible

DEFAULT_STATION_HISTORY_URL = "https://www.ncei.noaa.gov/pub/data/noaa/isd-history.csv"
DEFAULT_STATION_HISTORY_CSV = STATION_HISTORY_CSV
DEFAULT_STAGING_ROOT = STAGING_ROOT

METHODOLOGY_VERSION = "eop012-ecwt-station-candidates-v0.3.0-adr0006"
SOURCE_FAMILY = "noaa_isd_station_history"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sql_literal(value: object) -> str:
    if value is None:
        return "null"
    text = str(value)
    return "'" + text.replace("'", "''") + "'"


def pg_csv_value(value: object) -> object:
    if value is None:
        return r"\N"
    if isinstance(value, float) and math.isnan(value):
        return r"\N"
    text = str(value)
    return r"\N" if text == "" else text


def run(cmd: list[str], *, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        input=input_text,
        text=True,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def git_commit_label(project_root: Path) -> str:
    try:
        result = run(["git", "-C", str(project_root), "rev-parse", "HEAD"])
        return result.stdout.strip()
    except Exception:
        return "UNCOMMITTED_WORKTREE"


def download_if_needed(url: str, path: Path, refresh: bool) -> bool:
    if path.exists() and not refresh:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    curl = shutil.which("curl")
    if curl:
        run(
            [
                curl,
                "-L",
                "--fail",
                "--connect-timeout",
                "20",
                "--max-time",
                "120",
                "--retry",
                "3",
                "--retry-delay",
                "2",
                "--output",
                str(path),
                url,
            ]
        )
    else:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = response.read()
        path.write_bytes(data)
    return True


def parse_date(value: str) -> str | None:
    text = (value or "").strip()
    if not text or text == "99999999":
        return None
    try:
        dt = datetime.strptime(text, "%Y%m%d").replace(tzinfo=timezone.utc)
    except ValueError:
        return None
    return dt.isoformat(timespec="seconds")


def parse_float(value: str) -> float | None:
    text = (value or "").strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def local_standard_utc_offset_hours(longitude: float | None) -> int | None:
    if longitude is None:
        return None
    return max(-12, min(14, round(longitude / 15.0)))


def station_id(usaf: str, wban: str) -> str | None:
    usaf = (usaf or "").strip()
    wban = (wban or "").strip()
    if not usaf or not wban:
        return None
    if not re.fullmatch(r"\d+", usaf) or not re.fullmatch(r"\d+", wban):
        return None
    return f"{usaf.zfill(6)}-{wban.zfill(5)}"


def parse_noaa_station_history(path: Path, source_file_id: str) -> list[dict[str, object]]:
    stations: OrderedDict[str, dict[str, object]] = OrderedDict()
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sid = station_id(row.get("USAF", ""), row.get("WBAN", ""))
            lat = parse_float(row.get("LAT", ""))
            lon = parse_float(row.get("LON", ""))
            if sid is None or lat is None or lon is None:
                continue
            if not is_land_plant_station_eligible(sid):
                continue
            if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                continue
            if lat == 0 and lon == 0:
                continue
            begin = parse_date(row.get("BEGIN", ""))
            end = parse_date(row.get("END", ""))
            if end and end < "2000-01-01T00:00:00+00:00":
                continue
            existing = stations.get(sid)
            incoming = {
                "station_id": sid,
                "station_name": (row.get("STATION NAME", "") or "").strip() or None,
                "latitude": lat,
                "longitude": lon,
                "local_standard_utc_offset_hours": local_standard_utc_offset_hours(lon),
                "elevation_m": parse_float(row.get("ELEV(M)", "")),
                "state": (row.get("STATE", "") or "").strip() or None,
                "country": (row.get("CTRY", "") or "").strip() or None,
                "first_observation_utc": begin,
                "last_observation_utc": end,
                "source_file_id": source_file_id,
            }
            if existing is None:
                stations[sid] = incoming
                continue

            # Merge duplicate station IDs. Keep the latest coordinates/name while
            # preserving the broadest observation date span.
            old_end = existing.get("last_observation_utc") or ""
            new_end = incoming.get("last_observation_utc") or ""
            if new_end >= old_end:
                for key in [
                    "station_name",
                    "latitude",
                    "longitude",
                    "local_standard_utc_offset_hours",
                    "elevation_m",
                    "state",
                    "country",
                ]:
                    existing[key] = incoming[key]
            begins = [v for v in [existing.get("first_observation_utc"), incoming.get("first_observation_utc")] if v]
            ends = [v for v in [existing.get("last_observation_utc"), incoming.get("last_observation_utc")] if v]
            existing["first_observation_utc"] = min(begins) if begins else None
            existing["last_observation_utc"] = max(ends) if ends else None
    return list(stations.values())


def psql_csv_query(psql: Path, host: str, port: int, dbname: str, query: str) -> list[dict[str, str]]:
    result = run(
        [
            str(psql),
            "-h",
            host,
            "-p",
            str(port),
            "-d",
            dbname,
            "-v",
            "ON_ERROR_STOP=1",
            "-c",
            f"\\copy ({query}) to stdout with (format csv, header true)",
        ]
    )
    return list(csv.DictReader(io.StringIO(result.stdout)))


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: pg_csv_value(row.get(field)) for field in fieldnames})


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius_km = 6371.0088
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    return 2 * radius_km * math.asin(math.sqrt(a))


def station_grid(stations: list[dict[str, object]]) -> dict[tuple[int, int], list[dict[str, object]]]:
    grid: dict[tuple[int, int], list[dict[str, object]]] = defaultdict(list)
    for station in stations:
        lat = float(station["latitude"])
        lon = float(station["longitude"])
        grid[(math.floor(lat), math.floor(lon))].append(station)
    return grid


def candidates_in_radius(
    plant: dict[str, str],
    grid: dict[tuple[int, int], list[dict[str, object]]],
    stations: list[dict[str, object]],
    radius_km: float,
) -> list[tuple[float, dict[str, object]]]:
    lat = float(plant["latitude"])
    lon = float(plant["longitude"])
    lat_delta = radius_km / 111.0
    cos_lat = max(0.15, abs(math.cos(math.radians(lat))))
    lon_delta = radius_km / (111.0 * cos_lat)
    found: list[tuple[float, dict[str, object]]] = []
    for lat_bin in range(math.floor(lat - lat_delta), math.floor(lat + lat_delta) + 1):
        for lon_bin in range(math.floor(lon - lon_delta), math.floor(lon + lon_delta) + 1):
            for station in grid.get((lat_bin, lon_bin), []):
                distance = haversine_km(lat, lon, float(station["latitude"]), float(station["longitude"]))
                if distance <= radius_km:
                    found.append((distance, station))
    return found


def generate_candidates(
    plants: list[dict[str, str]],
    stations: list[dict[str, object]],
    run_id: str,
    top_n: int,
    initial_radius_km: float,
    expanded_radius_km: float,
) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, int]]:
    grid = station_grid(stations)
    candidates: list[dict[str, object]] = []
    exceptions: list[dict[str, object]] = []
    stats = {"initial_radius": 0, "expanded_radius": 0, "global_fallback": 0, "no_candidate": 0}

    for plant in plants:
        plant_id = plant["plant_id"]
        eia_code = plant["eia_plant_code"]
        found = candidates_in_radius(plant, grid, stations, initial_radius_km)
        search_mode = "initial_radius"
        if len(found) < top_n:
            found = candidates_in_radius(plant, grid, stations, expanded_radius_km)
            search_mode = "expanded_radius"
        if len(found) < top_n:
            lat = float(plant["latitude"])
            lon = float(plant["longitude"])
            found = [
                (
                    haversine_km(lat, lon, float(station["latitude"]), float(station["longitude"])),
                    station,
                )
                for station in stations
            ]
            search_mode = "global_fallback"
        if not found:
            stats["no_candidate"] += 1
            exceptions.append(
                {
                    "exception_id": f"{run_id}:no_station_candidate:{eia_code}",
                    "calculation_run_id": run_id,
                    "entity_type": "plant",
                    "entity_id": plant_id,
                    "severity": "blocker",
                    "reason_code": "no_station_candidate",
                    "message": f"No NOAA ISD station candidate was generated for EIA plant {eia_code}.",
                    "resolution_status": "open",
                    "notes": "Station metadata candidate generation failed to find any valid station.",
                }
            )
            continue

        stats[search_mode] += 1
        found.sort(key=lambda item: item[0])
        for rank, (distance, station) in enumerate(found[:top_n], start=1):
            sid = str(station["station_id"])
            candidates.append(
                {
                    "candidate_id": f"{run_id}:candidate:{eia_code}:{rank}:{sid}",
                    "plant_id": plant_id,
                    "station_id": sid,
                    "calculation_run_id": run_id,
                    "distance_km": f"{distance:.6f}",
                    "elevation_delta_m": None,
                    "valid_djf_hours": None,
                    "expected_djf_hours": None,
                    "coverage_ratio": None,
                    "rank_order": rank,
                    "candidate_status": "candidate",
                    "reason_code": f"nearest_by_distance_{search_mode}_coverage_pending",
                    "notes": "Coverage metrics are intentionally pending until the NOAA hourly coverage audit phase.",
                }
            )

    return candidates, exceptions, stats


def copy_command(table: str, columns: list[str], path: Path) -> str:
    return f"\\copy {table} ({', '.join(columns)}) from '{path}' with (format csv, header true, null '\\N')"


def render_values_insert(table: str, columns: list[str], rows: list[dict[str, object]], conflict: str) -> str:
    values = []
    for row in rows:
        values.append("(" + ", ".join(sql_literal(row.get(col)) for col in columns) + ")")
    return f"insert into {table} ({', '.join(columns)}) values\n" + ",\n".join(values) + f"\n{conflict};\n"


def build_load_sql(
    staging_dir: Path,
    source_row: dict[str, object],
    run_id: str,
    code_commit: str,
    stats: dict[str, int],
) -> str:
    station_cols = [
        "station_id",
        "station_name",
        "latitude",
        "longitude",
        "local_standard_utc_offset_hours",
        "elevation_m",
        "state",
        "country",
        "first_observation_utc",
        "last_observation_utc",
        "source_file_id",
    ]
    candidate_cols = [
        "candidate_id",
        "plant_id",
        "station_id",
        "calculation_run_id",
        "distance_km",
        "elevation_delta_m",
        "valid_djf_hours",
        "expected_djf_hours",
        "coverage_ratio",
        "rank_order",
        "candidate_status",
        "reason_code",
        "notes",
    ]
    exception_cols = [
        "exception_id",
        "calculation_run_id",
        "entity_type",
        "entity_id",
        "severity",
        "reason_code",
        "message",
        "resolution_status",
        "notes",
    ]
    start = utc_now().isoformat(timespec="seconds")
    source_cols = [
        "source_file_id",
        "source_family",
        "source_url",
        "local_path",
        "file_name",
        "size_bytes",
        "sha256",
        "retrieved_at_utc",
        "source_year",
        "source_release",
        "notes",
    ]
    params = json.dumps(
        {
            "source_family": SOURCE_FAMILY,
            "top_n": stats.get("top_n"),
            "initial_radius_km": stats.get("initial_radius_km"),
            "expanded_radius_km": stats.get("expanded_radius_km"),
        },
        sort_keys=True,
    )

    return "\n".join(
        [
            "\\set ON_ERROR_STOP on",
            "begin;",
            render_values_insert(
                "audit.methodology_version",
                ["methodology_version", "methodology_name", "effective_at_utc", "source_standard", "notes"],
                [
                    {
                        "methodology_version": METHODOLOGY_VERSION,
                        "methodology_name": "EOP012 ECWT national calculation methodology",
                        "effective_at_utc": start,
                        "source_standard": "NERC EOP-012-3; EPRI 3002030362 guidance",
                        "notes": "Initial auditable methodology version for asset loading, station matching, and ECWT calculation.",
                    }
                ],
                "on conflict (methodology_version) do update set notes = excluded.notes",
            ),
            render_values_insert(
                "audit.source_file",
                source_cols,
                [source_row],
                """on conflict (source_file_id) do update set
    source_family = excluded.source_family,
    source_url = excluded.source_url,
    local_path = excluded.local_path,
    file_name = excluded.file_name,
    size_bytes = excluded.size_bytes,
    sha256 = excluded.sha256,
    retrieved_at_utc = excluded.retrieved_at_utc,
    source_year = excluded.source_year,
    source_release = excluded.source_release,
    notes = excluded.notes""",
            ),
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
) values (
    {sql_literal(run_id)},
    {sql_literal(METHODOLOGY_VERSION)},
    {sql_literal(code_commit)},
    {sql_literal(start)},
    now(),
    'succeeded',
    {sql_literal(params)}::jsonb,
    'Loaded NOAA ISD station metadata and generated plant-station candidates.'
)
on conflict (calculation_run_id) do update set
    run_finished_at_utc = excluded.run_finished_at_utc,
    run_status = excluded.run_status,
    parameters_json = excluded.parameters_json,
    notes = excluded.notes;
""",
            """
alter table weather.station
    add column if not exists local_standard_utc_offset_hours integer;
""",
            """
create temp table stg_station (
    station_id text,
    station_name text,
    latitude numeric,
    longitude numeric,
    local_standard_utc_offset_hours integer,
    elevation_m numeric,
    state text,
    country text,
    first_observation_utc timestamptz,
    last_observation_utc timestamptz,
    source_file_id text
) on commit drop;
""",
            copy_command("stg_station", station_cols, staging_dir / "stations.csv"),
            """
insert into weather.station (
    station_id,
    station_name,
    latitude,
    longitude,
    local_standard_utc_offset_hours,
    elevation_m,
    state,
    country,
    first_observation_utc,
    last_observation_utc,
    source_file_id
)
select
    station_id,
    station_name,
    latitude,
    longitude,
    local_standard_utc_offset_hours,
    elevation_m,
    state,
    country,
    first_observation_utc,
    last_observation_utc,
    source_file_id
from stg_station
on conflict (station_id) do update set
    station_name = excluded.station_name,
    latitude = excluded.latitude,
    longitude = excluded.longitude,
    local_standard_utc_offset_hours = excluded.local_standard_utc_offset_hours,
    elevation_m = excluded.elevation_m,
    state = excluded.state,
    country = excluded.country,
    first_observation_utc = excluded.first_observation_utc,
    last_observation_utc = excluded.last_observation_utc,
    source_file_id = excluded.source_file_id;
""",
            """
create temp table stg_candidate (
    candidate_id text,
    plant_id text,
    station_id text,
    calculation_run_id text,
    distance_km numeric,
    elevation_delta_m numeric,
    valid_djf_hours bigint,
    expected_djf_hours bigint,
    coverage_ratio numeric,
    rank_order integer,
    candidate_status text,
    reason_code text,
    notes text
) on commit drop;
""",
            copy_command("stg_candidate", candidate_cols, staging_dir / "station_candidates.csv"),
            """
insert into link.station_candidate (
    candidate_id,
    plant_id,
    station_id,
    calculation_run_id,
    distance_km,
    elevation_delta_m,
    valid_djf_hours,
    expected_djf_hours,
    coverage_ratio,
    rank_order,
    candidate_status,
    reason_code,
    notes
)
select
    candidate_id,
    plant_id,
    station_id,
    calculation_run_id,
    distance_km,
    elevation_delta_m,
    valid_djf_hours,
    expected_djf_hours,
    coverage_ratio,
    rank_order,
    candidate_status,
    reason_code,
    notes
from stg_candidate
on conflict (plant_id, station_id, calculation_run_id) do update set
    candidate_id = excluded.candidate_id,
    distance_km = excluded.distance_km,
    elevation_delta_m = excluded.elevation_delta_m,
    valid_djf_hours = excluded.valid_djf_hours,
    expected_djf_hours = excluded.expected_djf_hours,
    coverage_ratio = excluded.coverage_ratio,
    rank_order = excluded.rank_order,
    candidate_status = excluded.candidate_status,
    reason_code = excluded.reason_code,
    notes = excluded.notes;
""",
            """
create temp table stg_exception (
    exception_id text,
    calculation_run_id text,
    entity_type text,
    entity_id text,
    severity text,
    reason_code text,
    message text,
    resolution_status text,
    notes text
) on commit drop;
""",
            copy_command("stg_exception", exception_cols, staging_dir / "exceptions.csv"),
            """
insert into audit.exception_log (
    exception_id,
    calculation_run_id,
    entity_type,
    entity_id,
    severity,
    reason_code,
    message,
    resolution_status,
    notes
)
select
    exception_id,
    calculation_run_id,
    entity_type,
    entity_id,
    severity,
    reason_code,
    message,
    resolution_status,
    notes
from stg_exception
on conflict (exception_id) do update set
    severity = excluded.severity,
    reason_code = excluded.reason_code,
    message = excluded.message,
    resolution_status = excluded.resolution_status,
    notes = excluded.notes;
""",
            "commit;",
        ]
    )


def psql_query(psql: Path, host: str, port: int, dbname: str, sql: str) -> str:
    result = run([str(psql), "-h", host, "-p", str(port), "-d", dbname, "-At", "-c", sql])
    return result.stdout.strip()


def render_report(
    path: Path,
    run_id: str,
    code_commit: str,
    source_row: dict[str, object],
    parsed_station_count: int,
    plants_with_coordinates: int,
    candidate_count: int,
    stats: dict[str, int],
    db_counts: OrderedDict[str, str],
    top_n: int,
    initial_radius_km: float,
    expanded_radius_km: float,
    host: str,
    port: int,
    dbname: str,
) -> None:
    lines = [
        "# NOAA Station Candidate Report",
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
        "",
        "## Source",
        "",
        f"- Source URL: `{source_row['source_url']}`",
        f"- Local path: `{source_row['local_path']}`",
        f"- Size bytes: `{source_row['size_bytes']}`",
        f"- SHA-256: `{source_row['sha256']}`",
        "",
        "## Candidate Parameters",
        "",
        f"- Top candidates per plant: `{top_n}`",
        f"- Initial radius: `{initial_radius_km:g} km`",
        f"- Expanded radius: `{expanded_radius_km:g} km`",
        "- Coverage metrics: pending; these candidates are distance-only station metadata candidates.",
        "",
        "## Counts",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| Parsed NOAA stations loaded | {parsed_station_count} |",
        f"| Plants with valid coordinates considered | {plants_with_coordinates} |",
        f"| Station candidate rows generated | {candidate_count} |",
        f"| Plants satisfied by initial radius | {stats['initial_radius']} |",
        f"| Plants requiring expanded radius | {stats['expanded_radius']} |",
        f"| Plants requiring global fallback | {stats['global_fallback']} |",
        f"| Plants with no candidate | {stats['no_candidate']} |",
        "",
        "## Database Row Counts",
        "",
        "| Relation | Rows |",
        "| --- | ---: |",
    ]
    for relation, count in db_counts.items():
        lines.append(f"| `{relation}` | {count} |")
    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- Station IDs use NOAA ISD `USAF-WBAN` format, matching the local NOAA hourly cache format.",
            "- Candidate ranking is distance-only for this phase.",
            "- Representative station selection is not complete until hourly DJF coverage metrics are joined and reviewed.",
            "- `valid_djf_hours`, `expected_djf_hours`, and `coverage_ratio` are intentionally null in this phase.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--station-history-url", default=DEFAULT_STATION_HISTORY_URL)
    parser.add_argument("--station-history-csv", type=Path, default=DEFAULT_STATION_HISTORY_CSV)
    parser.add_argument("--refresh-station-history", action="store_true")
    parser.add_argument("--staging-root", type=Path, default=DEFAULT_STAGING_ROOT)
    parser.add_argument("--psql", type=Path, default=PSQL)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5436)
    parser.add_argument("--dbname", default="eop012")
    parser.add_argument("--top-n", type=int, default=10)
    parser.add_argument("--initial-radius-km", type=float, default=250.0)
    parser.add_argument("--expanded-radius-km", type=float, default=1000.0)
    args = parser.parse_args()

    if not args.psql.exists():
        raise FileNotFoundError(args.psql)

    downloaded = download_if_needed(args.station_history_url, args.station_history_csv, args.refresh_station_history)
    retrieved_at_utc = (
        utc_now()
        if downloaded
        else datetime.fromtimestamp(args.station_history_csv.stat().st_mtime, tz=timezone.utc)
    )
    source_hash = sha256_file(args.station_history_csv)
    source_file_id = f"noaa_isd_history_csv_{source_hash[:16]}"
    source_row = {
        "source_file_id": source_file_id,
        "source_family": SOURCE_FAMILY,
        "source_url": args.station_history_url,
        "local_path": str(args.station_history_csv),
        "file_name": args.station_history_csv.name,
        "size_bytes": args.station_history_csv.stat().st_size,
        "sha256": source_hash,
        "retrieved_at_utc": retrieved_at_utc.isoformat(timespec="seconds"),
        "source_year": None,
        "source_release": "live_noaa_isd_history_csv",
        "notes": "NOAA ISD station history CSV used for weather station metadata and candidate generation.",
    }

    stations = parse_noaa_station_history(args.station_history_csv, source_file_id)
    plants = psql_csv_query(
        args.psql,
        args.host,
        args.port,
        args.dbname,
        """
        select plant_id, eia_plant_code, plant_name, state, latitude::text as latitude, longitude::text as longitude
        from asset.plant
        where latitude is not null and longitude is not null
        order by eia_plant_code::bigint nulls last, eia_plant_code
        """,
    )
    code_commit = git_commit_label(args.project_root)
    run_timestamp = utc_now().strftime("%Y%m%dT%H%M%SZ")
    run_id = f"noaa_station_candidates_{run_timestamp}"
    staging_dir = args.staging_root / run_id
    staging_dir.mkdir(parents=True, exist_ok=True)

    candidates, exceptions, stats = generate_candidates(
        plants,
        stations,
        run_id,
        args.top_n,
        args.initial_radius_km,
        args.expanded_radius_km,
    )
    stats["top_n"] = args.top_n
    stats["initial_radius_km"] = int(args.initial_radius_km)
    stats["expanded_radius_km"] = int(args.expanded_radius_km)

    station_cols = [
        "station_id",
        "station_name",
        "latitude",
        "longitude",
        "elevation_m",
        "state",
        "country",
        "first_observation_utc",
        "last_observation_utc",
        "source_file_id",
    ]
    candidate_cols = [
        "candidate_id",
        "plant_id",
        "station_id",
        "calculation_run_id",
        "distance_km",
        "elevation_delta_m",
        "valid_djf_hours",
        "expected_djf_hours",
        "coverage_ratio",
        "rank_order",
        "candidate_status",
        "reason_code",
        "notes",
    ]
    exception_cols = [
        "exception_id",
        "calculation_run_id",
        "entity_type",
        "entity_id",
        "severity",
        "reason_code",
        "message",
        "resolution_status",
        "notes",
    ]
    write_csv(staging_dir / "stations.csv", station_cols, stations)
    write_csv(staging_dir / "station_candidates.csv", candidate_cols, candidates)
    write_csv(staging_dir / "exceptions.csv", exception_cols, exceptions)

    load_sql = build_load_sql(staging_dir, source_row, run_id, code_commit, stats)
    sql_path = staging_dir / "load.sql"
    sql_path.write_text(load_sql, encoding="utf-8")
    run([str(args.psql), "-h", args.host, "-p", str(args.port), "-d", args.dbname, "-v", "ON_ERROR_STOP=1", "-f", str(sql_path)])

    db_counts = OrderedDict(
        [
            ("weather.station", psql_query(args.psql, args.host, args.port, args.dbname, "select count(*) from weather.station;")),
            (
                "link.station_candidate for this run",
                psql_query(
                    args.psql,
                    args.host,
                    args.port,
                    args.dbname,
                    f"select count(*) from link.station_candidate where calculation_run_id = {sql_literal(run_id)};",
                ),
            ),
            (
                "plants with candidates for this run",
                psql_query(
                    args.psql,
                    args.host,
                    args.port,
                    args.dbname,
                    f"select count(distinct plant_id) from link.station_candidate where calculation_run_id = {sql_literal(run_id)};",
                ),
            ),
            ("audit.source_file", psql_query(args.psql, args.host, args.port, args.dbname, "select count(*) from audit.source_file;")),
            ("audit.calculation_run", psql_query(args.psql, args.host, args.port, args.dbname, "select count(*) from audit.calculation_run;")),
            ("audit.exception_log", psql_query(args.psql, args.host, args.port, args.dbname, "select count(*) from audit.exception_log;")),
        ]
    )

    report_path = args.project_root / "docs" / "noaa_station_candidate_report.md"
    render_report(
        report_path,
        run_id,
        code_commit,
        source_row,
        len(stations),
        len(plants),
        len(candidates),
        stats,
        db_counts,
        args.top_n,
        args.initial_radius_km,
        args.expanded_radius_km,
        args.host,
        args.port,
        args.dbname,
    )

    print(
        json.dumps(
            {
                "run_id": run_id,
                "source_file_id": source_file_id,
                "station_history_csv": str(args.station_history_csv),
                "station_history_sha256": source_hash,
                "staging_dir": str(staging_dir),
                "report_path": str(report_path),
                "stations_loaded": len(stations),
                "plants_with_coordinates": len(plants),
                "candidates_generated": len(candidates),
                "candidate_stats": stats,
                "db_counts": db_counts,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
