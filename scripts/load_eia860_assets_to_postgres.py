#!/usr/bin/env python3
"""Load EIA-860 asset inventory extracts into the audited EOP012 Postgres DB."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import zipfile
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


PROJECT_ROOT = Path("/Users/Shared/EOP012/rebuild")
RAW_ZIP = Path("/Users/Shared/EOP012/EIA_860_raw_downloads/intake/eia8602024.zip")
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed" / "eia8602024"
STAGING_ROOT = Path("/Volumes/NOAA_CACHE/EOP012/staging")
PSQL = Path("/opt/homebrew/opt/postgresql@16/bin/psql")

METHODOLOGY_VERSION = "eop012-ecwt-method-v0.1.0"
SOURCE_YEAR = 2024
SOURCE_RELEASE = "eia8602024"
EIA_URL = "https://www.eia.gov/electricity/data/eia860/xls/eia8602024.zip"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def slug(value: str) -> str:
    text = re.sub(r"[^0-9A-Za-z]+", "_", value.strip().lower()).strip("_")
    return text or "unknown"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: pg_csv_value(row.get(field)) for field in fieldnames})


def pg_csv_value(value: object) -> object:
    if value is None:
        return r"\N"
    if isinstance(value, float) and math.isnan(value):
        return r"\N"
    text = str(value)
    return r"\N" if text == "" else text


def parse_numeric(value: str) -> str | None:
    if value is None:
        return None
    text = str(value).strip().replace(",", "")
    if not text:
        return None
    try:
        float(text)
    except ValueError:
        return None
    return text


def sql_literal(value: object) -> str:
    if value is None:
        return "null"
    text = str(value)
    return "'" + text.replace("'", "''") + "'"


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
        result = run(["git", "-c", f"safe.directory={project_root}", "-C", str(project_root), "rev-parse", "HEAD"])
        return result.stdout.strip()
    except Exception:
        return "UNCOMMITTED_WORKTREE"


def source_files_from_zip(zip_path: Path) -> list[dict[str, object]]:
    source_rows: list[dict[str, object]] = []
    zip_stat = zip_path.stat()
    source_rows.append(
        {
            "source_file_id": "eia860_2024_zip",
            "source_family": "eia860",
            "source_url": EIA_URL,
            "local_path": str(zip_path),
            "file_name": zip_path.name,
            "size_bytes": zip_stat.st_size,
            "sha256": sha256_file(zip_path),
            "retrieved_at_utc": None,
            "source_year": SOURCE_YEAR,
            "source_release": SOURCE_RELEASE,
            "notes": "Official EIA-860 2024 final annual ZIP. Download date recorded in raw-intake README as 2026-06-23.",
        }
    )

    wanted = {
        "1___Utility_Y2024.xlsx": "eia860_2024_utility_xlsx",
        "2___Plant_Y2024.xlsx": "eia860_2024_plant_xlsx",
        "3_1_Generator_Y2024.xlsx": "eia860_2024_generator_xlsx",
        "LayoutY2024.xlsx": "eia860_2024_layout_xlsx",
    }
    with zipfile.ZipFile(zip_path) as zf:
        for info in zf.infolist():
            file_name = Path(info.filename).name
            if file_name not in wanted:
                continue
            data = zf.read(info.filename)
            source_rows.append(
                {
                    "source_file_id": wanted[file_name],
                    "source_family": "eia860",
                    "source_url": EIA_URL,
                    "local_path": f"{zip_path}!/{info.filename}",
                    "file_name": file_name,
                    "size_bytes": info.file_size,
                    "sha256": sha256_bytes(data),
                    "retrieved_at_utc": None,
                    "source_year": SOURCE_YEAR,
                    "source_release": SOURCE_RELEASE,
                    "notes": "Member file inside official EIA-860 2024 final annual ZIP.",
                }
            )
    return source_rows


def map_utility_rows(utility_rows: list[dict[str, str]], plant_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    utilities: OrderedDict[str, dict[str, object]] = OrderedDict()

    for row in utility_rows:
        utility_id = row.get("utility_id", "").strip()
        if not utility_id:
            continue
        utilities[utility_id] = {
            "utility_id": utility_id,
            "utility_name": row.get("utility_name", "").strip(),
            "entity_type": row.get("entity_type", "").strip() or None,
            "source_file_id": "eia860_2024_utility_xlsx",
            "source_year": SOURCE_YEAR,
        }

    for row in plant_rows:
        utility_id = row.get("utility_id", "").strip()
        if not utility_id or utility_id in utilities:
            continue
        utilities[utility_id] = {
            "utility_id": utility_id,
            "utility_name": row.get("utility_name", "").strip(),
            "entity_type": None,
            "source_file_id": "eia860_2024_plant_xlsx",
            "source_year": SOURCE_YEAR,
        }

    return list(utilities.values())


def map_plant_rows(plant_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    mapped: list[dict[str, object]] = []
    for row in plant_rows:
        plant_code = row.get("plant_code", "").strip()
        if not plant_code:
            continue
        mapped.append(
            {
                "plant_id": f"eia860:{SOURCE_YEAR}:plant:{plant_code}",
                "eia_plant_code": plant_code,
                "plant_name": row.get("plant_name", "").strip(),
                "utility_id": row.get("utility_id", "").strip() or None,
                "utility_name": row.get("utility_name", "").strip() or None,
                "street_address": row.get("street_address", "").strip() or None,
                "city": row.get("city", "").strip() or None,
                "state": row.get("state", "").strip() or None,
                "zip": row.get("zip", "").strip() or None,
                "county": row.get("county", "").strip() or None,
                "latitude": parse_numeric(row.get("latitude", "")),
                "longitude": parse_numeric(row.get("longitude", "")),
                "nerc_region": row.get("nerc_region", "").strip() or None,
                "balancing_authority_code": row.get("balancing_authority_code", "").strip() or None,
                "balancing_authority_name": row.get("balancing_authority_name", "").strip() or None,
                "sector_name": row.get("sector_name", "").strip() or None,
                "source_file_id": "eia860_2024_plant_xlsx",
                "source_year": SOURCE_YEAR,
            }
        )
    return mapped


def generator_sheet_name(path: Path) -> str:
    name = path.stem.replace("generator_", "")
    return {
        "operable": "Operable",
        "proposed": "Proposed",
        "retired_and_canceled": "Retired and Canceled",
    }.get(name, name)


def map_generator_rows(processed_dir: Path) -> list[dict[str, object]]:
    mapped: list[dict[str, object]] = []
    for path in [
        processed_dir / "generator_operable.csv",
        processed_dir / "generator_proposed.csv",
        processed_dir / "generator_retired_and_canceled.csv",
    ]:
        sheet = generator_sheet_name(path)
        sheet_slug = slug(sheet)
        for row in read_csv(path):
            plant_code = row.get("plant_code", "").strip()
            generator_id = row.get("generator_id", "").strip()
            if not plant_code or not generator_id:
                continue
            mapped.append(
                {
                    "generator_id_internal": f"eia860:{SOURCE_YEAR}:generator:{sheet_slug}:{plant_code}:{generator_id}",
                    "eia_plant_code": plant_code,
                    "generator_id": generator_id,
                    "utility_id": row.get("utility_id", "").strip() or None,
                    "utility_name": row.get("utility_name", "").strip() or None,
                    "plant_name": row.get("plant_name", "").strip() or None,
                    "state": row.get("state", "").strip() or None,
                    "county": row.get("county", "").strip() or None,
                    "technology": row.get("technology", "").strip() or None,
                    "prime_mover": row.get("prime_mover", "").strip() or None,
                    "unit_code": row.get("unit_code", "").strip() or None,
                    "ownership": row.get("ownership", "").strip() or None,
                    "nameplate_capacity_mw": parse_numeric(row.get("nameplate_capacity_mw", "")),
                    "summer_capacity_mw": parse_numeric(row.get("summer_capacity_mw", "")),
                    "winter_capacity_mw": parse_numeric(row.get("winter_capacity_mw", "")),
                    "status": row.get("status", "").strip(),
                    "generator_sheet": sheet,
                    "source_file_id": "eia860_2024_generator_xlsx",
                    "source_year": SOURCE_YEAR,
                }
            )
    return mapped


def build_exceptions(
    run_id: str,
    plant_rows: list[dict[str, object]],
    generator_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    exceptions: list[dict[str, object]] = []
    plant_codes = {str(row["eia_plant_code"]) for row in plant_rows}

    for row in plant_rows:
        if row.get("latitude") is None or row.get("longitude") is None:
            plant_code = str(row["eia_plant_code"])
            exceptions.append(
                {
                    "exception_id": f"{run_id}:plant_missing_coordinates:{plant_code}",
                    "calculation_run_id": run_id,
                    "entity_type": "plant",
                    "entity_id": str(row["plant_id"]),
                    "severity": "warning",
                    "reason_code": "plant_missing_coordinates",
                    "message": f"EIA plant {plant_code} ({row.get('plant_name')}) has missing or non-numeric latitude/longitude.",
                    "resolution_status": "open",
                    "notes": "Plant cannot be included in automated station matching until coordinates are resolved.",
                }
            )

    for row in generator_rows:
        plant_code = str(row["eia_plant_code"])
        if plant_code not in plant_codes:
            exceptions.append(
                {
                    "exception_id": f"{run_id}:generator_missing_plant:{plant_code}:{row['generator_id']}",
                    "calculation_run_id": run_id,
                    "entity_type": "generator",
                    "entity_id": str(row["generator_id_internal"]),
                    "severity": "error",
                    "reason_code": "generator_plant_code_not_in_plant_table",
                    "message": f"EIA generator {row['generator_id']} references plant code {plant_code}, but that plant code is absent from the EIA plant table.",
                    "resolution_status": "open",
                    "notes": "This generator cannot inherit a plant-level ECWT until the plant anomaly is resolved.",
                }
            )

    return exceptions


def copy_command(table: str, columns: list[str], path: Path) -> str:
    joined_cols = ", ".join(columns)
    return f"\\copy {table} ({joined_cols}) from '{path}' with (format csv, header true, null '\\N')"


def render_values_insert(table: str, columns: list[str], rows: list[dict[str, object]], conflict: str) -> str:
    values = []
    for row in rows:
        values.append("(" + ", ".join(sql_literal(row.get(col)) for col in columns) + ")")
    return f"insert into {table} ({', '.join(columns)}) values\n" + ",\n".join(values) + f"\n{conflict};\n"


def build_load_sql(
    staging_dir: Path,
    run_id: str,
    code_commit: str,
    source_rows: list[dict[str, object]],
) -> str:
    utility_cols = ["utility_id", "utility_name", "entity_type", "source_file_id", "source_year"]
    plant_cols = [
        "plant_id",
        "eia_plant_code",
        "plant_name",
        "utility_id",
        "utility_name",
        "street_address",
        "city",
        "state",
        "zip",
        "county",
        "latitude",
        "longitude",
        "nerc_region",
        "balancing_authority_code",
        "balancing_authority_name",
        "sector_name",
        "source_file_id",
        "source_year",
    ]
    generator_cols = [
        "generator_id_internal",
        "eia_plant_code",
        "generator_id",
        "utility_id",
        "utility_name",
        "plant_name",
        "state",
        "county",
        "technology",
        "prime_mover",
        "unit_code",
        "ownership",
        "nameplate_capacity_mw",
        "summer_capacity_mw",
        "winter_capacity_mw",
        "status",
        "generator_sheet",
        "source_file_id",
        "source_year",
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

    start = utc_now().isoformat(timespec="seconds")
    sql = [
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
            source_rows,
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
    '{{"source_release":"{SOURCE_RELEASE}","source_year":{SOURCE_YEAR}}}'::jsonb,
    'Loaded EIA-860 2024 asset universe into audit and asset schemas.'
)
on conflict (calculation_run_id) do update set
    run_finished_at_utc = excluded.run_finished_at_utc,
    run_status = excluded.run_status,
    parameters_json = excluded.parameters_json,
    notes = excluded.notes;
""",
        """
create temp table stg_utility (
    utility_id text,
    utility_name text,
    entity_type text,
    source_file_id text,
    source_year integer
) on commit drop;
""",
        copy_command("stg_utility", utility_cols, staging_dir / "utility_mapped.csv"),
        """
insert into asset.utility (utility_id, utility_name, entity_type, source_file_id, source_year)
select utility_id, utility_name, entity_type, source_file_id, source_year
from stg_utility
where utility_id is not null
on conflict (utility_id) do update set
    utility_name = excluded.utility_name,
    entity_type = excluded.entity_type,
    source_file_id = excluded.source_file_id,
    source_year = excluded.source_year;
""",
        """
create temp table stg_plant (
    plant_id text,
    eia_plant_code text,
    plant_name text,
    utility_id text,
    utility_name text,
    street_address text,
    city text,
    state text,
    zip text,
    county text,
    latitude numeric,
    longitude numeric,
    nerc_region text,
    balancing_authority_code text,
    balancing_authority_name text,
    sector_name text,
    source_file_id text,
    source_year integer
) on commit drop;
""",
        copy_command("stg_plant", plant_cols, staging_dir / "plant_mapped.csv"),
        """
insert into asset.plant (
    plant_id,
    eia_plant_code,
    plant_name,
    utility_id,
    utility_name,
    street_address,
    city,
    state,
    zip,
    county,
    latitude,
    longitude,
    nerc_region,
    balancing_authority_code,
    balancing_authority_name,
    sector_name,
    source_file_id,
    source_year
)
select
    plant_id,
    eia_plant_code,
    plant_name,
    utility_id,
    utility_name,
    street_address,
    city,
    state,
    zip,
    county,
    latitude,
    longitude,
    nerc_region,
    balancing_authority_code,
    balancing_authority_name,
    sector_name,
    source_file_id,
    source_year
from stg_plant
on conflict (eia_plant_code) do update set
    plant_id = excluded.plant_id,
    plant_name = excluded.plant_name,
    utility_id = excluded.utility_id,
    utility_name = excluded.utility_name,
    street_address = excluded.street_address,
    city = excluded.city,
    state = excluded.state,
    zip = excluded.zip,
    county = excluded.county,
    latitude = excluded.latitude,
    longitude = excluded.longitude,
    nerc_region = excluded.nerc_region,
    balancing_authority_code = excluded.balancing_authority_code,
    balancing_authority_name = excluded.balancing_authority_name,
    sector_name = excluded.sector_name,
    source_file_id = excluded.source_file_id,
    source_year = excluded.source_year;
""",
        """
create temp table stg_generator (
    generator_id_internal text,
    eia_plant_code text,
    generator_id text,
    utility_id text,
    utility_name text,
    plant_name text,
    state text,
    county text,
    technology text,
    prime_mover text,
    unit_code text,
    ownership text,
    nameplate_capacity_mw numeric,
    summer_capacity_mw numeric,
    winter_capacity_mw numeric,
    status text,
    generator_sheet text,
    source_file_id text,
    source_year integer
) on commit drop;
""",
        copy_command("stg_generator", generator_cols, staging_dir / "generator_mapped.csv"),
        """
insert into asset.generator (
    generator_id_internal,
    eia_plant_code,
    generator_id,
    utility_id,
    utility_name,
    plant_name,
    state,
    county,
    technology,
    prime_mover,
    unit_code,
    ownership,
    nameplate_capacity_mw,
    summer_capacity_mw,
    winter_capacity_mw,
    status,
    generator_sheet,
    source_file_id,
    source_year
)
select
    generator_id_internal,
    eia_plant_code,
    generator_id,
    utility_id,
    utility_name,
    plant_name,
    state,
    county,
    technology,
    prime_mover,
    unit_code,
    ownership,
    nameplate_capacity_mw,
    summer_capacity_mw,
    winter_capacity_mw,
    status,
    generator_sheet,
    source_file_id,
    source_year
from stg_generator
on conflict (eia_plant_code, generator_id, generator_sheet, source_year) do update set
    generator_id_internal = excluded.generator_id_internal,
    utility_id = excluded.utility_id,
    utility_name = excluded.utility_name,
    plant_name = excluded.plant_name,
    state = excluded.state,
    county = excluded.county,
    technology = excluded.technology,
    prime_mover = excluded.prime_mover,
    unit_code = excluded.unit_code,
    ownership = excluded.ownership,
    nameplate_capacity_mw = excluded.nameplate_capacity_mw,
    summer_capacity_mw = excluded.summer_capacity_mw,
    winter_capacity_mw = excluded.winter_capacity_mw,
    status = excluded.status,
    source_file_id = excluded.source_file_id,
    source_year = excluded.source_year;
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
        copy_command("stg_exception", exception_cols, staging_dir / "exceptions_mapped.csv"),
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
    return "\n".join(sql)


def psql_query(psql: Path, host: str, port: int, dbname: str, sql: str) -> str:
    result = run([str(psql), "-h", host, "-p", str(port), "-d", dbname, "-At", "-c", sql])
    return result.stdout.strip()


def render_report(
    path: Path,
    run_id: str,
    code_commit: str,
    source_rows: list[dict[str, object]],
    mapped_counts: dict[str, int],
    db_counts: dict[str, str],
    exceptions: list[dict[str, object]],
    host: str,
    port: int,
    dbname: str,
) -> None:
    now = utc_now().isoformat(timespec="seconds")
    lines = [
        "# EIA-860 Database Load Report",
        "",
        f"Generated UTC: {now}",
        "",
        "## Database",
        "",
        f"- Host: `{host}`",
        f"- Port: `{port}`",
        f"- Database: `{dbname}`",
        "- Cluster path: `/Volumes/NOAA_CACHE/EOP012/postgres16`",
        "",
        "## Run",
        "",
        f"- Calculation run ID: `{run_id}`",
        f"- Methodology version: `{METHODOLOGY_VERSION}`",
        f"- Code commit: `{code_commit}`",
        f"- Source release: `{SOURCE_RELEASE}`",
        "",
        "## Source Files",
        "",
        "| Source file ID | File | Size bytes | SHA-256 |",
        "| --- | --- | ---: | --- |",
    ]
    for row in source_rows:
        lines.append(
            f"| `{row['source_file_id']}` | `{row['file_name']}` | {row['size_bytes']} | `{row['sha256']}` |"
        )
    lines.extend(
        [
            "",
            "## Mapped Row Counts",
            "",
            "| Mapped table | Rows |",
            "| --- | ---: |",
        ]
    )
    for key, value in mapped_counts.items():
        lines.append(f"| `{key}` | {value} |")
    lines.extend(
        [
            "",
            "## Database Row Counts",
            "",
            "| Database relation | Rows |",
            "| --- | ---: |",
        ]
    )
    for key, value in db_counts.items():
        lines.append(f"| `{key}` | {value} |")
    reason_counts: OrderedDict[str, int] = OrderedDict()
    for exc in exceptions:
        reason = str(exc["reason_code"])
        reason_counts[reason] = reason_counts.get(reason, 0) + 1
    lines.extend(
        [
            "",
            "## Exceptions Loaded",
            "",
            "| Reason code | Count |",
            "| --- | ---: |",
        ]
    )
    for reason, count in reason_counts.items():
        lines.append(f"| `{reason}` | {count} |")
    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- The database contains the EIA-860 2024 final asset universe only; NOAA station matching has not been loaded yet.",
            "- The known generator anomaly is plant code `68815`, which appears in the generator file but not the plant file.",
            "- Plants with missing coordinates are loaded but cannot enter automated NOAA station matching until resolved.",
            "",
        ]
    )
    if code_commit == "UNCOMMITTED_WORKTREE":
        lines.insert(
            -3,
            "- The current repository has not been committed yet, so `code_commit` is `UNCOMMITTED_WORKTREE`.",
        )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--zip", type=Path, default=RAW_ZIP)
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED_DIR)
    parser.add_argument("--staging-root", type=Path, default=STAGING_ROOT)
    parser.add_argument("--psql", type=Path, default=PSQL)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5436)
    parser.add_argument("--dbname", default="eop012")
    args = parser.parse_args()

    required = [
        args.processed_dir / "utility.csv",
        args.processed_dir / "plant.csv",
        args.processed_dir / "generator_operable.csv",
        args.processed_dir / "generator_proposed.csv",
        args.processed_dir / "generator_retired_and_canceled.csv",
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing processed input files: " + ", ".join(missing))
    if not args.zip.exists():
        raise FileNotFoundError(args.zip)
    if not args.psql.exists():
        raise FileNotFoundError(args.psql)

    run_timestamp = utc_now().strftime("%Y%m%dT%H%M%SZ")
    run_id = f"eia860_2024_asset_load_{run_timestamp}"
    staging_dir = args.staging_root / run_id
    staging_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_files_from_zip(args.zip)
    utility_src = read_csv(args.processed_dir / "utility.csv")
    plant_src = read_csv(args.processed_dir / "plant.csv")
    utility_rows = map_utility_rows(utility_src, plant_src)
    plant_rows = map_plant_rows(plant_src)
    generator_rows = map_generator_rows(args.processed_dir)
    exceptions = build_exceptions(run_id, plant_rows, generator_rows)
    code_commit = git_commit_label(args.project_root)

    write_csv(
        staging_dir / "utility_mapped.csv",
        ["utility_id", "utility_name", "entity_type", "source_file_id", "source_year"],
        utility_rows,
    )
    write_csv(
        staging_dir / "plant_mapped.csv",
        [
            "plant_id",
            "eia_plant_code",
            "plant_name",
            "utility_id",
            "utility_name",
            "street_address",
            "city",
            "state",
            "zip",
            "county",
            "latitude",
            "longitude",
            "nerc_region",
            "balancing_authority_code",
            "balancing_authority_name",
            "sector_name",
            "source_file_id",
            "source_year",
        ],
        plant_rows,
    )
    write_csv(
        staging_dir / "generator_mapped.csv",
        [
            "generator_id_internal",
            "eia_plant_code",
            "generator_id",
            "utility_id",
            "utility_name",
            "plant_name",
            "state",
            "county",
            "technology",
            "prime_mover",
            "unit_code",
            "ownership",
            "nameplate_capacity_mw",
            "summer_capacity_mw",
            "winter_capacity_mw",
            "status",
            "generator_sheet",
            "source_file_id",
            "source_year",
        ],
        generator_rows,
    )
    write_csv(
        staging_dir / "exceptions_mapped.csv",
        [
            "exception_id",
            "calculation_run_id",
            "entity_type",
            "entity_id",
            "severity",
            "reason_code",
            "message",
            "resolution_status",
            "notes",
        ],
        exceptions,
    )

    load_sql = build_load_sql(staging_dir, run_id, code_commit, source_rows)
    sql_path = staging_dir / "load.sql"
    sql_path.write_text(load_sql, encoding="utf-8")
    run([str(args.psql), "-h", args.host, "-p", str(args.port), "-d", args.dbname, "-v", "ON_ERROR_STOP=1", "-f", str(sql_path)])

    db_counts = OrderedDict(
        [
            ("audit.source_file", psql_query(args.psql, args.host, args.port, args.dbname, "select count(*) from audit.source_file;")),
            ("audit.calculation_run", psql_query(args.psql, args.host, args.port, args.dbname, "select count(*) from audit.calculation_run;")),
            ("asset.utility", psql_query(args.psql, args.host, args.port, args.dbname, "select count(*) from asset.utility;")),
            ("asset.plant", psql_query(args.psql, args.host, args.port, args.dbname, "select count(*) from asset.plant;")),
            ("asset.generator", psql_query(args.psql, args.host, args.port, args.dbname, "select count(*) from asset.generator;")),
            ("audit.exception_log", psql_query(args.psql, args.host, args.port, args.dbname, "select count(*) from audit.exception_log;")),
        ]
    )
    mapped_counts = OrderedDict(
        [
            ("utility", len(utility_rows)),
            ("plant", len(plant_rows)),
            ("generator", len(generator_rows)),
            ("exceptions", len(exceptions)),
        ]
    )

    report_path = args.project_root / "docs" / "eia860_db_load_report.md"
    render_report(
        report_path,
        run_id,
        code_commit,
        source_rows,
        mapped_counts,
        db_counts,
        exceptions,
        args.host,
        args.port,
        args.dbname,
    )

    print(
        json.dumps(
            {
                "run_id": run_id,
                "staging_dir": str(staging_dir),
                "report_path": str(report_path),
                "mapped_counts": mapped_counts,
                "db_counts": db_counts,
                "exception_count": len(exceptions),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
