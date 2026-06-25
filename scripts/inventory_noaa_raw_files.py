#!/usr/bin/env python3
"""Inventory local NOAA Global Hourly raw files for candidate stations."""

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

from eop012_config import NOAA_RAW_ROOTS, PROJECT_ROOT, PSQL, STAGING_ROOT

DEFAULT_STAGING_ROOT = STAGING_ROOT

METHODOLOGY_VERSION = "eop012-ecwt-method-v0.1.0"
SOURCE_FAMILY = "noaa_global_hourly_local_raw_inventory"
DEFAULT_RAW_ROOTS = NOAA_RAW_ROOTS


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


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
    query: str,
    user: str | None = None,
) -> list[dict[str, str]]:
    result = run(
        psql_cmd(psql, host, port, dbname, user)
        + ["-c", f"\\copy ({query}) to stdout with (format csv, header true)"]
    )
    return list(csv.DictReader(io.StringIO(result.stdout)))


def psql_scalar(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    query: str,
    user: str | None = None,
) -> str:
    result = run(psql_cmd(psql, host, port, dbname, user) + ["-At", "-c", query])
    return result.stdout.strip()


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: pg_csv_value(row.get(field)) for field in fieldnames})


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def dedupe_paths(paths: Iterable[Path]) -> list[Path]:
    deduped: OrderedDict[str, Path] = OrderedDict()
    for path in paths:
        expanded = path.expanduser()
        deduped.setdefault(str(expanded), expanded)
    return list(deduped.values())


def git_commit_label(project_root: Path) -> str:
    try:
        result = run(["git", "-C", str(project_root), "rev-parse", "HEAD"])
        return result.stdout.strip()
    except Exception:
        return "UNCOMMITTED_WORKTREE"


def relation_exists(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    relation_name: str,
) -> bool:
    exists = psql_scalar(
        psql,
        host,
        port,
        dbname,
        f"select to_regclass({sql_literal(relation_name)}) is not null;",
        user,
    )
    return exists.lower() in {"t", "true", "1"}


def loaded_noaa_raw_roots(psql: Path, host: str, port: int, dbname: str, user: str | None) -> list[Path]:
    if not relation_exists(psql, host, port, dbname, user, "weather.noaa_hourly_load_file"):
        return []
    rows = psql_csv_query(
        psql,
        host,
        port,
        dbname,
        """
        select
            regexp_replace(local_path, '/[0-9]{4}/[^/]+(\\.gz)?$', '') as raw_root,
            count(*)::text as loaded_file_count
        from weather.noaa_hourly_load_file
        where local_path is not null
          and local_path like '/%'
        group by 1
        order by count(*) desc, raw_root
        """,
        user,
    )
    return dedupe_paths(Path(row["raw_root"]) for row in rows if row.get("raw_root"))


def latest_candidate_run_id(psql: Path, host: str, port: int, dbname: str, user: str | None) -> str:
    run_id = psql_scalar(
        psql,
        host,
        port,
        dbname,
        """
        select calculation_run_id
        from audit.calculation_run
        where calculation_run_id like 'noaa_station_candidates_%'
          and run_status = 'succeeded'
        order by run_started_at_utc desc
        limit 1
        """,
        user,
    )
    if not run_id:
        raise RuntimeError("No succeeded noaa_station_candidates calculation run found.")
    return run_id


def candidate_station_ids(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    candidate_run_id: str,
) -> list[str]:
    rows = psql_csv_query(
        psql,
        host,
        port,
        dbname,
        f"""
        select distinct station_id
        from link.station_candidate
        where calculation_run_id = {sql_literal(candidate_run_id)}
        order by station_id
        """,
        user,
    )
    return [row["station_id"] for row in rows]


def station_to_raw_id(station_id: str) -> str:
    return station_id.replace("-", "")


def year_dir_candidates(raw_roots: list[Path], start_year: int, end_year: int) -> OrderedDict[int, list[tuple[Path, Path]]]:
    candidates: OrderedDict[int, list[tuple[Path, Path]]] = OrderedDict((year, []) for year in range(start_year, end_year + 1))
    for root in raw_roots:
        if not root.exists():
            continue
        for year in range(start_year, end_year + 1):
            year_name = str(year)
            direct = root / year_name
            if direct.is_dir():
                candidates[year].append((root, direct))
            try:
                children = [child for child in root.iterdir() if child.is_dir()]
            except OSError:
                children = []
            for child in children:
                nested = child / year_name
                if nested.is_dir():
                    candidates[year].append((root, nested))
    return candidates


def find_raw_file(raw_id: str, year_dirs: list[tuple[Path, Path]]) -> tuple[Path, Path] | tuple[None, None]:
    names = [
        f"{raw_id}.csv",
        f"{raw_id}.CSV",
        f"{raw_id}.csv.gz",
        f"{raw_id}.CSV.gz",
        f"{raw_id}.gz",
    ]
    for root, year_dir in year_dirs:
        for name in names:
            path = year_dir / name
            if path.exists() and path.is_file():
                return root, path
    return None, None


def build_inventory_rows(
    station_ids: list[str],
    year_dirs: OrderedDict[int, list[tuple[Path, Path]]],
    run_id: str,
    source_file_id: str,
) -> tuple[list[dict[str, object]], dict[str, object]]:
    rows: list[dict[str, object]] = []
    available_by_year: Counter[int] = Counter()
    missing_by_year: Counter[int] = Counter()
    available_by_root: Counter[str] = Counter()
    available_years_by_station: dict[str, set[int]] = defaultdict(set)
    total_bytes = 0

    for station_id in station_ids:
        raw_id = station_to_raw_id(station_id)
        for year, dirs in year_dirs.items():
            root, path = find_raw_file(raw_id, dirs)
            if path is None or root is None:
                missing_by_year[year] += 1
                rows.append(
                    {
                        "inventory_id": f"{run_id}:station:{station_id}:year:{year}",
                        "station_id": station_id,
                        "source_year": year,
                        "calculation_run_id": run_id,
                        "source_file_id": source_file_id,
                        "raw_station_id": raw_id,
                        "local_path": None,
                        "file_name": None,
                        "source_root": None,
                        "file_size_bytes": None,
                        "file_mtime_utc": None,
                        "file_status": "missing",
                        "notes": "No local NOAA Global Hourly raw file found in configured roots.",
                    }
                )
                continue

            stat = path.stat()
            total_bytes += stat.st_size
            available_by_year[year] += 1
            available_by_root[str(root)] += 1
            available_years_by_station[station_id].add(year)
            rows.append(
                {
                    "inventory_id": f"{run_id}:station:{station_id}:year:{year}",
                    "station_id": station_id,
                    "source_year": year,
                    "calculation_run_id": run_id,
                    "source_file_id": source_file_id,
                    "raw_station_id": raw_id,
                    "local_path": str(path),
                    "file_name": path.name,
                    "source_root": str(root),
                    "file_size_bytes": stat.st_size,
                    "file_mtime_utc": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(timespec="seconds"),
                    "file_status": "available",
                    "notes": "Local NOAA Global Hourly raw station-year file found.",
                }
            )

    years = list(year_dirs.keys())
    station_year_total = len(station_ids) * len(years)
    stations_with_all_years = sum(1 for sid in station_ids if len(available_years_by_station[sid]) == len(years))
    stations_with_any_year = sum(1 for sid in station_ids if available_years_by_station[sid])
    stats = {
        "candidate_station_count": len(station_ids),
        "year_count": len(years),
        "station_year_total": station_year_total,
        "station_year_available": sum(available_by_year.values()),
        "station_year_missing": sum(missing_by_year.values()),
        "stations_with_all_years": stations_with_all_years,
        "stations_with_any_year": stations_with_any_year,
        "stations_with_no_years": len(station_ids) - stations_with_any_year,
        "total_available_file_bytes": total_bytes,
        "available_by_year": dict(available_by_year),
        "missing_by_year": dict(missing_by_year),
        "available_by_root": dict(available_by_root),
        "year_dirs": {year: [str(path) for _, path in dirs] for year, dirs in year_dirs.items()},
    }
    return rows, stats


def year_exception_rows(run_id: str, stats: dict[str, object], station_count: int) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    available_by_year: dict[int, int] = stats["available_by_year"]  # type: ignore[assignment]
    missing_by_year: dict[int, int] = stats["missing_by_year"]  # type: ignore[assignment]
    all_years = sorted(set(available_by_year) | set(missing_by_year))
    for year in all_years:
        available = int(available_by_year.get(year, 0))
        missing = int(missing_by_year.get(year, 0))
        if missing == 0:
            continue
        severity = "blocker" if available == 0 else "warning"
        rows.append(
            {
                "exception_id": f"{run_id}:raw_file_inventory_year:{year}",
                "calculation_run_id": run_id,
                "entity_type": "source_year",
                "entity_id": str(year),
                "severity": severity,
                "reason_code": "noaa_raw_station_year_files_missing",
                "message": (
                    f"NOAA raw inventory found {available} available and {missing} missing "
                    f"candidate station-year files for {year} out of {station_count} candidate stations."
                ),
                "resolution_status": "open",
                "notes": "Missing raw files must be downloaded or excluded before a full hourly ECWT rebuild.",
            }
        )
    return rows


def render_values_insert(table: str, columns: list[str], rows: list[dict[str, object]], conflict: str) -> str:
    values = []
    for row in rows:
        values.append("(" + ", ".join(sql_literal(row.get(col)) for col in columns) + ")")
    return f"insert into {table} ({', '.join(columns)}) values\n" + ",\n".join(values) + f"\n{conflict};\n"


def copy_command(table: str, columns: list[str], path: Path) -> str:
    return f"\\copy {table} ({', '.join(columns)}) from '{path}' with (format csv, header true, null '\\N')"


def build_load_sql(
    staging_dir: Path,
    source_row: dict[str, object],
    run_id: str,
    code_commit: str,
    params: dict[str, object],
) -> str:
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
    inventory_cols = [
        "inventory_id",
        "station_id",
        "source_year",
        "calculation_run_id",
        "source_file_id",
        "raw_station_id",
        "local_path",
        "file_name",
        "source_root",
        "file_size_bytes",
        "file_mtime_utc",
        "file_status",
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
    return "\n".join(
        [
            "\\set ON_ERROR_STOP on",
            "begin;",
            """
create table if not exists weather.noaa_raw_file_inventory (
    inventory_id text primary key,
    station_id text not null references weather.station(station_id),
    source_year integer not null,
    calculation_run_id text not null references audit.calculation_run(calculation_run_id),
    source_file_id text references audit.source_file(source_file_id),
    raw_station_id text not null,
    local_path text,
    file_name text,
    source_root text,
    file_size_bytes bigint,
    file_mtime_utc timestamptz,
    file_status text not null,
    notes text,
    created_at_utc timestamptz not null default now(),
    unique (station_id, source_year, calculation_run_id),
    constraint noaa_raw_file_inventory_status_check
        check (file_status in ('available', 'missing'))
);
""",
            """
create index if not exists ix_noaa_raw_file_inventory_year_status
    on weather.noaa_raw_file_inventory (source_year, file_status);
""",
            render_values_insert(
                "audit.methodology_version",
                ["methodology_version", "methodology_name", "effective_at_utc", "source_standard", "notes"],
                [
                    {
                        "methodology_version": METHODOLOGY_VERSION,
                        "methodology_name": "EOP012 ECWT national calculation methodology",
                        "effective_at_utc": start,
                        "source_standard": "NERC EOP-012-3; EPRI 3002030362 guidance",
                        "notes": "Initial auditable methodology version for asset loading, station matching, raw file inventory, coverage auditing, and ECWT calculation.",
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
    {sql_literal(json.dumps(params, sort_keys=True))}::jsonb,
    'Inventoried local NOAA Global Hourly raw station-year files for candidate weather stations.'
)
on conflict (calculation_run_id) do update set
    run_finished_at_utc = excluded.run_finished_at_utc,
    run_status = excluded.run_status,
    parameters_json = excluded.parameters_json,
    notes = excluded.notes;
""",
            """
create temp table stg_noaa_raw_file_inventory (
    inventory_id text,
    station_id text,
    source_year integer,
    calculation_run_id text,
    source_file_id text,
    raw_station_id text,
    local_path text,
    file_name text,
    source_root text,
    file_size_bytes bigint,
    file_mtime_utc timestamptz,
    file_status text,
    notes text
) on commit drop;
""",
            copy_command("stg_noaa_raw_file_inventory", inventory_cols, staging_dir / "noaa_raw_file_inventory.csv"),
            """
insert into weather.noaa_raw_file_inventory (
    inventory_id,
    station_id,
    source_year,
    calculation_run_id,
    source_file_id,
    raw_station_id,
    local_path,
    file_name,
    source_root,
    file_size_bytes,
    file_mtime_utc,
    file_status,
    notes
)
select
    inventory_id,
    station_id,
    source_year,
    calculation_run_id,
    source_file_id,
    raw_station_id,
    local_path,
    file_name,
    source_root,
    file_size_bytes,
    file_mtime_utc,
    file_status,
    notes
from stg_noaa_raw_file_inventory
on conflict (station_id, source_year, calculation_run_id) do update set
    source_file_id = excluded.source_file_id,
    raw_station_id = excluded.raw_station_id,
    local_path = excluded.local_path,
    file_name = excluded.file_name,
    source_root = excluded.source_root,
    file_size_bytes = excluded.file_size_bytes,
    file_mtime_utc = excluded.file_mtime_utc,
    file_status = excluded.file_status,
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


def report_counts(
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
                "weather.noaa_raw_file_inventory for this run",
                f"select count(*) from weather.noaa_raw_file_inventory where calculation_run_id = {sql_literal(run_id)};",
            ),
            (
                "available station-year files",
                f"select count(*) from weather.noaa_raw_file_inventory where calculation_run_id = {sql_literal(run_id)} and file_status = 'available';",
            ),
            (
                "missing station-year files",
                f"select count(*) from weather.noaa_raw_file_inventory where calculation_run_id = {sql_literal(run_id)} and file_status = 'missing';",
            ),
            ("audit.source_file", "select count(*) from audit.source_file;"),
            ("audit.calculation_run", "select count(*) from audit.calculation_run;"),
            ("audit.exception_log", "select count(*) from audit.exception_log;"),
        ]
    )
    results: OrderedDict[str, str] = OrderedDict()
    for label, query in queries.items():
        results[label] = psql_scalar(psql, host, port, dbname, query, user)
    return results


def render_report(
    path: Path,
    run_id: str,
    candidate_run_id: str,
    code_commit: str,
    source_row: dict[str, object],
    raw_roots: list[Path],
    loaded_raw_roots: list[Path],
    auto_included_loaded_roots: list[Path],
    start_year: int,
    end_year: int,
    stats: dict[str, object],
    db_counts: OrderedDict[str, str],
    host: str,
    port: int,
    dbname: str,
) -> None:
    lines = [
        "# NOAA Raw File Inventory Report",
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
        f"- Candidate run ID inventoried: `{candidate_run_id}`",
        f"- Methodology version: `{METHODOLOGY_VERSION}`",
        f"- Code commit: `{code_commit}`",
        "",
        "## Inventory Scope",
        "",
        f"- Candidate stations: `{stats['candidate_station_count']}`",
        f"- Year range: `{start_year}-{end_year}`",
        f"- Station-year checks: `{stats['station_year_total']}`",
        f"- Source file ID: `{source_row['source_file_id']}`",
        "",
        "Configured roots, in priority order:",
        "",
    ]
    for root in raw_roots:
        lines.append(f"- `{root}`")
    if loaded_raw_roots:
        lines.extend(["", "Previously loaded NOAA roots observed in this database:", ""])
        for root in loaded_raw_roots:
            lines.append(f"- `{root}`")
    if auto_included_loaded_roots:
        lines.extend(["", "Loaded roots auto-included in this inventory:", ""])
        for root in auto_included_loaded_roots:
            lines.append(f"- `{root}`")
    lines.extend(
        [
            "",
            "## Summary",
            "",
            "| Metric | Count |",
            "| --- | ---: |",
            f"| Available station-year files | {stats['station_year_available']} |",
            f"| Missing station-year files | {stats['station_year_missing']} |",
            f"| Stations with all years available | {stats['stations_with_all_years']} |",
            f"| Stations with at least one year available | {stats['stations_with_any_year']} |",
            f"| Stations with no years available | {stats['stations_with_no_years']} |",
            f"| Total bytes for available inventoried files | {stats['total_available_file_bytes']} |",
            "",
            "## Availability By Year",
            "",
            "| Year | Available | Missing | Year Directories Found |",
            "| --- | ---: | ---: | ---: |",
        ]
    )
    available_by_year: dict[int, int] = stats["available_by_year"]  # type: ignore[assignment]
    missing_by_year: dict[int, int] = stats["missing_by_year"]  # type: ignore[assignment]
    year_dirs: dict[int, list[str]] = stats["year_dirs"]  # type: ignore[assignment]
    for year in range(start_year, end_year + 1):
        lines.append(
            f"| {year} | {available_by_year.get(year, 0)} | {missing_by_year.get(year, 0)} | {len(year_dirs.get(year, []))} |"
        )
    lines.extend(
        [
            "",
            "## Availability By Root",
            "",
            "| Root | Station-Year Files Used |",
            "| --- | ---: |",
        ]
    )
    available_by_root: dict[str, int] = stats["available_by_root"]  # type: ignore[assignment]
    for root, count in sorted(available_by_root.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| `{root}` | {count} |")
    lines.extend(
        [
            "",
            "## Database Row Counts",
            "",
            "| Relation or Check | Rows |",
            "| --- | ---: |",
        ]
    )
    for label, count in db_counts.items():
        lines.append(f"| `{label}` | {count} |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- This inventory checks local raw NOAA station-year file presence only; it does not parse hourly observations yet.",
            "- Missing years or missing station files must be downloaded before a compliance-grade full hourly rebuild can be complete.",
            "- The next parser step should process available station-year CSV files into a normalized hourly DJF staging table and produce raw missing, duplicate, and invalid-temperature counts.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--staging-root", type=Path, default=DEFAULT_STAGING_ROOT)
    parser.add_argument("--psql", type=Path, default=PSQL)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5436)
    parser.add_argument("--dbname", default="eop012")
    parser.add_argument("--user", default=None)
    parser.add_argument("--candidate-run-id", default=None)
    parser.add_argument("--start-year", type=int, default=2000)
    parser.add_argument("--end-year", type=int, default=2025)
    parser.add_argument("--raw-root", type=Path, action="append", default=None)
    parser.add_argument(
        "--no-include-loaded-roots",
        action="store_true",
        help="Do not auto-include NOAA raw roots already referenced by weather.noaa_hourly_load_file.",
    )
    args = parser.parse_args()

    if not args.psql.exists():
        raise FileNotFoundError(args.psql)

    raw_roots = dedupe_paths(args.raw_root or DEFAULT_RAW_ROOTS)
    loaded_raw_roots: list[Path] = []
    auto_included_loaded_roots: list[Path] = []
    if not args.no_include_loaded_roots:
        loaded_raw_roots = [root for root in loaded_noaa_raw_roots(args.psql, args.host, args.port, args.dbname, args.user) if root.exists()]
        configured_root_keys = {str(root) for root in raw_roots}
        auto_included_loaded_roots = [root for root in loaded_raw_roots if str(root) not in configured_root_keys]
        raw_roots = dedupe_paths([*raw_roots, *auto_included_loaded_roots])
    candidate_run_id = args.candidate_run_id or latest_candidate_run_id(
        args.psql, args.host, args.port, args.dbname, args.user
    )
    stations = candidate_station_ids(args.psql, args.host, args.port, args.dbname, args.user, candidate_run_id)
    if not stations:
        raise RuntimeError(f"No candidate stations found for {candidate_run_id}.")

    code_commit = git_commit_label(args.project_root)
    run_timestamp = utc_now().strftime("%Y%m%dT%H%M%SZ")
    run_id = f"noaa_raw_file_inventory_{run_timestamp}"
    staging_dir = args.staging_root / run_id
    staging_dir.mkdir(parents=True, exist_ok=True)

    year_dirs = year_dir_candidates(raw_roots, args.start_year, args.end_year)
    root_seed = "|".join(str(root) for root in raw_roots)
    source_file_id = f"{SOURCE_FAMILY}_{sha256_text(root_seed)[:16]}"
    rows, stats = build_inventory_rows(stations, year_dirs, run_id, source_file_id)
    exceptions = year_exception_rows(run_id, stats, len(stations))

    inventory_cols = [
        "inventory_id",
        "station_id",
        "source_year",
        "calculation_run_id",
        "source_file_id",
        "raw_station_id",
        "local_path",
        "file_name",
        "source_root",
        "file_size_bytes",
        "file_mtime_utc",
        "file_status",
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
    write_csv(staging_dir / "noaa_raw_file_inventory.csv", inventory_cols, rows)
    write_csv(staging_dir / "exceptions.csv", exception_cols, exceptions)

    source_row = {
        "source_file_id": source_file_id,
        "source_family": SOURCE_FAMILY,
        "source_url": "https://www.ncei.noaa.gov/data/global-hourly/",
        "local_path": root_seed,
        "file_name": "local_noaa_global_hourly_raw_roots",
        "size_bytes": stats["total_available_file_bytes"],
        "sha256": None,
        "retrieved_at_utc": utc_now().isoformat(timespec="seconds"),
        "source_year": None,
        "source_release": f"local_inventory_{args.start_year}_{args.end_year}",
        "notes": "Inventory of local NOAA Global Hourly station-year CSV files for EOP012 candidate weather stations.",
    }
    params = {
        "candidate_run_id": candidate_run_id,
        "source_family": SOURCE_FAMILY,
        "start_year": args.start_year,
        "end_year": args.end_year,
        "raw_roots": [str(root) for root in raw_roots],
        "include_loaded_roots": not args.no_include_loaded_roots,
        "loaded_raw_roots_seen": [str(root) for root in loaded_raw_roots],
        "auto_included_loaded_roots": [str(root) for root in auto_included_loaded_roots],
        "raw_station_id_rule": "remove hyphen from NOAA ISD USAF-WBAN station_id",
        "hashing": "file presence, size, and mtime only; full raw-file hashing deferred",
    }
    load_sql = build_load_sql(staging_dir, source_row, run_id, code_commit, params)
    sql_path = staging_dir / "load.sql"
    sql_path.write_text(load_sql, encoding="utf-8")
    run(psql_cmd(args.psql, args.host, args.port, args.dbname, args.user) + ["-f", str(sql_path)])

    db_counts = report_counts(args.psql, args.host, args.port, args.dbname, args.user, run_id)
    report_path = args.project_root / "docs" / "noaa_raw_file_inventory_report.md"
    render_report(
        report_path,
        run_id,
        candidate_run_id,
        code_commit,
        source_row,
        raw_roots,
        loaded_raw_roots,
        auto_included_loaded_roots,
        args.start_year,
        args.end_year,
        stats,
        db_counts,
        args.host,
        args.port,
        args.dbname,
    )

    print(
        json.dumps(
            {
                "run_id": run_id,
                "candidate_run_id": candidate_run_id,
                "source_file_id": source_file_id,
                "staging_dir": str(staging_dir),
                "report_path": str(report_path),
                "inventory_stats": {
                    key: value
                    for key, value in stats.items()
                    if key not in {"available_by_year", "missing_by_year", "available_by_root", "year_dirs"}
                },
                "available_by_year": stats["available_by_year"],
                "missing_by_year": stats["missing_by_year"],
                "available_by_root": stats["available_by_root"],
                "db_counts": db_counts,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
