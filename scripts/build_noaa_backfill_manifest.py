#!/usr/bin/env python3
"""Build a prioritized NOAA Global Hourly raw-file backfill manifest."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import subprocess
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from eop012_config import NOAA_GLOBAL_HOURLY_ROOT, PROJECT_ROOT, PSQL, STAGING_ROOT

DEFAULT_STAGING_ROOT = STAGING_ROOT
DEFAULT_TARGET_ROOT = NOAA_GLOBAL_HOURLY_ROOT

METHODOLOGY_VERSION = "eop012-ecwt-method-v0.1.0"
SOURCE_FAMILY = "noaa_global_hourly_backfill_manifest"
DEFAULT_BASE_URL = "https://noaa-global-hourly-pds.s3.amazonaws.com"


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


def git_commit_label(project_root: Path) -> str:
    try:
        result = run(["git", "-C", str(project_root), "rev-parse", "HEAD"])
        return result.stdout.strip()
    except Exception:
        return "UNCOMMITTED_WORKTREE"


def latest_inventory_run_id(psql: Path, host: str, port: int, dbname: str, user: str | None) -> str:
    run_id = psql_scalar(
        psql,
        host,
        port,
        dbname,
        """
        select calculation_run_id
        from audit.calculation_run
        where calculation_run_id like 'noaa_raw_file_inventory_%'
          and run_status = 'succeeded'
        order by run_started_at_utc desc
        limit 1
        """,
        user,
    )
    if not run_id:
        raise RuntimeError("No succeeded noaa_raw_file_inventory calculation run found.")
    return run_id


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


def ensure_download_attempt_lookup_index(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
) -> None:
    run(
        psql_cmd(psql, host, port, dbname, user)
        + [
            "-c",
            """
            create index if not exists ix_noaa_raw_download_attempt_station_year_status
                on weather.noaa_raw_download_attempt (station_id, source_year, raw_station_id, download_status);
            """,
        ]
    )


def missing_inventory_rows(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    inventory_run_id: str,
    include_known_missing_aws: bool,
) -> list[dict[str, str]]:
    known_missing_filter = ""
    if not include_known_missing_aws and relation_exists(
        psql, host, port, dbname, user, "weather.noaa_raw_download_attempt"
    ):
        ensure_download_attempt_lookup_index(psql, host, port, dbname, user)
        known_missing_filter = """
          and not exists (
              select 1
              from weather.noaa_raw_download_attempt attempt
              where attempt.station_id = i.station_id
                and attempt.source_year = i.source_year
                and attempt.raw_station_id = i.raw_station_id
                and attempt.download_status = 'missing_on_aws'
          )
        """
    return psql_csv_query(
        psql,
        host,
        port,
        dbname,
        f"""
        with year_counts as (
            select
                source_year,
                count(*) filter (where file_status = 'available') as source_year_available_count,
                count(*) filter (where file_status = 'missing') as source_year_missing_count
            from weather.noaa_raw_file_inventory
            where calculation_run_id = {sql_literal(inventory_run_id)}
            group by source_year
        ),
        station_links as (
            select
                station_id,
                count(distinct plant_id)::integer as station_candidate_plant_links
            from link.station_candidate
            group by station_id
        )
        select
            i.station_id,
            i.source_year::text as source_year,
            i.raw_station_id,
            coalesce(sl.station_candidate_plant_links, 0)::text as station_candidate_plant_links,
            yc.source_year_available_count::text as source_year_available_count,
            yc.source_year_missing_count::text as source_year_missing_count
        from weather.noaa_raw_file_inventory i
        join weather.station st
          on st.station_id = i.station_id
        join year_counts yc
          on yc.source_year = i.source_year
        left join station_links sl
          on sl.station_id = i.station_id
        where i.calculation_run_id = {sql_literal(inventory_run_id)}
          and i.file_status = 'missing'
          and (
            st.first_observation_utc is null
            or st.last_observation_utc is null
            or (
                st.first_observation_utc < make_timestamptz(i.source_year, 3, 1, 0, 0, 0, 'UTC')
                and st.last_observation_utc >= make_timestamptz(i.source_year, 1, 1, 0, 0, 0, 'UTC')
            )
            or (
                st.first_observation_utc < make_timestamptz(i.source_year + 1, 1, 1, 0, 0, 0, 'UTC')
                and st.last_observation_utc >= make_timestamptz(i.source_year, 12, 1, 0, 0, 0, 'UTC')
            )
          )
          {known_missing_filter}
        """,
        user,
    )


def priority_tuple(row: dict[str, str]) -> tuple[int, int, int, str]:
    year = int(row["source_year"])
    available = int(row["source_year_available_count"])
    plant_links = int(row["station_candidate_plant_links"])
    zero_local_year = 1 if available == 0 else 0
    return (-zero_local_year, -year, -plant_links, row["station_id"])


def priority_reason(row: dict[str, str]) -> str:
    year = int(row["source_year"])
    available = int(row["source_year_available_count"])
    plant_links = int(row["station_candidate_plant_links"])
    if available == 0:
        return f"zero_local_files_for_year;year={year};station_candidate_plant_links={plant_links}"
    return f"partial_year_gap;year={year};station_candidate_plant_links={plant_links};available_year_files={available}"


def build_manifest_rows(
    rows: list[dict[str, str]],
    run_id: str,
    inventory_run_id: str,
    base_url: str,
    target_root: Path,
    batch_size: int,
) -> list[dict[str, object]]:
    manifest_rows: list[dict[str, object]] = []
    clean_base = base_url.rstrip("/")
    for rank, row in enumerate(sorted(rows, key=priority_tuple), start=1):
        year = int(row["source_year"])
        raw_id = row["raw_station_id"]
        target_path = target_root / str(year) / f"{raw_id}.csv"
        manifest_rows.append(
            {
                "manifest_id": f"{run_id}:station:{row['station_id']}:year:{year}",
                "inventory_run_id": inventory_run_id,
                "calculation_run_id": run_id,
                "station_id": row["station_id"],
                "source_year": year,
                "raw_station_id": raw_id,
                "download_url": f"{clean_base}/{year}/{raw_id}.csv",
                "target_path": str(target_path),
                "priority_rank": rank,
                "batch_number": ((rank - 1) // batch_size) + 1,
                "station_candidate_plant_links": int(row["station_candidate_plant_links"]),
                "source_year_available_count": int(row["source_year_available_count"]),
                "source_year_missing_count": int(row["source_year_missing_count"]),
                "manifest_status": "planned",
                "priority_reason": priority_reason(row),
                "notes": "Download not attempted by manifest build step.",
            }
        )
    return manifest_rows


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
    manifest_cols = [
        "manifest_id",
        "inventory_run_id",
        "calculation_run_id",
        "station_id",
        "source_year",
        "raw_station_id",
        "download_url",
        "target_path",
        "priority_rank",
        "batch_number",
        "station_candidate_plant_links",
        "source_year_available_count",
        "source_year_missing_count",
        "manifest_status",
        "priority_reason",
        "notes",
    ]
    return "\n".join(
        [
            "\\set ON_ERROR_STOP on",
            "begin;",
            """
create table if not exists weather.noaa_raw_backfill_manifest (
    manifest_id text primary key,
    inventory_run_id text not null references audit.calculation_run(calculation_run_id),
    calculation_run_id text not null references audit.calculation_run(calculation_run_id),
    station_id text not null references weather.station(station_id),
    source_year integer not null,
    raw_station_id text not null,
    download_url text not null,
    target_path text not null,
    priority_rank integer not null,
    batch_number integer not null,
    station_candidate_plant_links integer not null,
    source_year_available_count integer not null,
    source_year_missing_count integer not null,
    manifest_status text not null,
    priority_reason text,
    notes text,
    created_at_utc timestamptz not null default now(),
    unique (inventory_run_id, station_id, source_year, calculation_run_id),
    constraint noaa_raw_backfill_manifest_status_check
        check (manifest_status in ('planned', 'downloaded', 'skipped', 'missing', 'failed'))
);
""",
            """
create index if not exists ix_noaa_raw_backfill_manifest_batch
    on weather.noaa_raw_backfill_manifest (calculation_run_id, batch_number, priority_rank);
""",
            """
create index if not exists ix_noaa_raw_backfill_manifest_year_status
    on weather.noaa_raw_backfill_manifest (source_year, manifest_status);
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
                        "notes": "Initial auditable methodology version for asset loading, station matching, raw file inventory, backfill planning, coverage auditing, and ECWT calculation.",
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
    'Built prioritized NOAA Global Hourly raw-file backfill manifest from missing local inventory rows.'
)
on conflict (calculation_run_id) do update set
    run_finished_at_utc = excluded.run_finished_at_utc,
    run_status = excluded.run_status,
    parameters_json = excluded.parameters_json,
    notes = excluded.notes;
""",
            """
create temp table stg_noaa_raw_backfill_manifest (
    manifest_id text,
    inventory_run_id text,
    calculation_run_id text,
    station_id text,
    source_year integer,
    raw_station_id text,
    download_url text,
    target_path text,
    priority_rank integer,
    batch_number integer,
    station_candidate_plant_links integer,
    source_year_available_count integer,
    source_year_missing_count integer,
    manifest_status text,
    priority_reason text,
    notes text
) on commit drop;
""",
            copy_command("stg_noaa_raw_backfill_manifest", manifest_cols, staging_dir / "noaa_raw_backfill_manifest.csv"),
            """
insert into weather.noaa_raw_backfill_manifest (
    manifest_id,
    inventory_run_id,
    calculation_run_id,
    station_id,
    source_year,
    raw_station_id,
    download_url,
    target_path,
    priority_rank,
    batch_number,
    station_candidate_plant_links,
    source_year_available_count,
    source_year_missing_count,
    manifest_status,
    priority_reason,
    notes
)
select
    manifest_id,
    inventory_run_id,
    calculation_run_id,
    station_id,
    source_year,
    raw_station_id,
    download_url,
    target_path,
    priority_rank,
    batch_number,
    station_candidate_plant_links,
    source_year_available_count,
    source_year_missing_count,
    manifest_status,
    priority_reason,
    notes
from stg_noaa_raw_backfill_manifest
on conflict (inventory_run_id, station_id, source_year, calculation_run_id) do update set
    raw_station_id = excluded.raw_station_id,
    download_url = excluded.download_url,
    target_path = excluded.target_path,
    priority_rank = excluded.priority_rank,
    batch_number = excluded.batch_number,
    station_candidate_plant_links = excluded.station_candidate_plant_links,
    source_year_available_count = excluded.source_year_available_count,
    source_year_missing_count = excluded.source_year_missing_count,
    manifest_status = excluded.manifest_status,
    priority_reason = excluded.priority_reason,
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
                "weather.noaa_raw_backfill_manifest for this run",
                f"select count(*) from weather.noaa_raw_backfill_manifest where calculation_run_id = {sql_literal(run_id)};",
            ),
            (
                "planned manifest rows",
                f"select count(*) from weather.noaa_raw_backfill_manifest where calculation_run_id = {sql_literal(run_id)} and manifest_status = 'planned';",
            ),
            (
                "batches",
                f"select count(distinct batch_number) from weather.noaa_raw_backfill_manifest where calculation_run_id = {sql_literal(run_id)};",
            ),
            (
                "batch 1 rows",
                f"select count(*) from weather.noaa_raw_backfill_manifest where calculation_run_id = {sql_literal(run_id)} and batch_number = 1;",
            ),
            ("audit.source_file", "select count(*) from audit.source_file;"),
            ("audit.calculation_run", "select count(*) from audit.calculation_run;"),
        ]
    )
    results: OrderedDict[str, str] = OrderedDict()
    for label, query in queries.items():
        results[label] = psql_scalar(psql, host, port, dbname, query, user)
    return results


def render_report(
    path: Path,
    run_id: str,
    inventory_run_id: str,
    code_commit: str,
    source_row: dict[str, object],
    target_root: Path,
    batch_size: int,
    manifest_rows: list[dict[str, object]],
    db_counts: OrderedDict[str, str],
    host: str,
    port: int,
    dbname: str,
) -> None:
    by_year: OrderedDict[int, int] = OrderedDict()
    for row in manifest_rows:
        year = int(row["source_year"])
        by_year[year] = by_year.get(year, 0) + 1
    batch_count = math.ceil(len(manifest_rows) / batch_size) if manifest_rows else 0
    top_rows = manifest_rows[:20]
    lines = [
        "# NOAA Backfill Manifest Report",
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
        f"- Source inventory run ID: `{inventory_run_id}`",
        f"- Methodology version: `{METHODOLOGY_VERSION}`",
        f"- Code commit: `{code_commit}`",
        f"- Source file ID: `{source_row['source_file_id']}`",
        "",
        "## Manifest Scope",
        "",
        f"- Download base URL: `{source_row['source_url']}`",
        f"- Target root: `{target_root}`",
        f"- Manifest rows: `{len(manifest_rows)}`",
        f"- Batch size: `{batch_size}`",
        f"- Batch count: `{batch_count}`",
        "- Status: `planned`; no files were downloaded by this step.",
        "- Known terminal AWS 404 station-years are excluded unless `--include-known-missing-aws` is supplied.",
        "",
        "## Priority Rule",
        "",
        "Rows are sorted by:",
        "",
        "1. years with zero local candidate-station raw files first",
        "2. newer source years first",
        "3. stations linked to more candidate plants first",
        "4. station ID as a stable tie-breaker",
        "",
        "## Planned Rows By Year",
        "",
        "| Year | Planned Downloads |",
        "| --- | ---: |",
    ]
    for year, count in sorted(by_year.items()):
        lines.append(f"| {year} | {count} |")
    lines.extend(
        [
            "",
            "## First 20 Planned Downloads",
            "",
            "| Rank | Batch | Year | Station | Plant Links | URL | Target |",
            "| ---: | ---: | ---: | --- | ---: | --- | --- |",
        ]
    )
    for row in top_rows:
        lines.append(
            "| "
            f"{row['priority_rank']} | "
            f"{row['batch_number']} | "
            f"{row['source_year']} | "
            f"`{row['station_id']}` | "
            f"{row['station_candidate_plant_links']} | "
            f"`{row['download_url']}` | "
            f"`{row['target_path']}` |"
        )
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
    lines.extend(["", "## Interpretation", "", "- This is a download plan, not a download run."])
    if manifest_rows:
        lines.extend(
            [
                "- Batch 1 is intentionally limited to the first 1,000 planned files so the downloader can be tested without launching the entire backfill.",
                "- The next step should run a batch downloader that consumes this manifest and records HTTP status, bytes, hashes, and failures.",
            ]
        )
    else:
        lines.extend(
            [
                "- This manifest has zero planned rows.",
                "- Under the configured roots, DJF active-window filter, and known terminal AWS 404 exclusion, there are no remaining AWS download candidates.",
            ]
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--staging-root", type=Path, default=DEFAULT_STAGING_ROOT)
    parser.add_argument("--target-root", type=Path, default=DEFAULT_TARGET_ROOT)
    parser.add_argument("--psql", type=Path, default=PSQL)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5436)
    parser.add_argument("--dbname", default="eop012")
    parser.add_argument("--user", default=None)
    parser.add_argument("--inventory-run-id", default=None)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--batch-size", type=int, default=1000)
    parser.add_argument(
        "--include-known-missing-aws",
        action="store_true",
        help="Include station-years with prior missing_on_aws evidence. Default excludes known terminal AWS 404 objects.",
    )
    args = parser.parse_args()

    if not args.psql.exists():
        raise FileNotFoundError(args.psql)
    if args.batch_size <= 0:
        raise ValueError("--batch-size must be positive")

    inventory_run_id = args.inventory_run_id or latest_inventory_run_id(
        args.psql, args.host, args.port, args.dbname, args.user
    )
    missing_rows = missing_inventory_rows(
        args.psql,
        args.host,
        args.port,
        args.dbname,
        args.user,
        inventory_run_id,
        args.include_known_missing_aws,
    )
    code_commit = git_commit_label(args.project_root)
    run_timestamp = utc_now().strftime("%Y%m%dT%H%M%SZ")
    run_id = f"noaa_backfill_manifest_{run_timestamp}"
    staging_dir = args.staging_root / run_id
    staging_dir.mkdir(parents=True, exist_ok=True)

    manifest_rows = build_manifest_rows(
        missing_rows,
        run_id,
        inventory_run_id,
        args.base_url,
        args.target_root,
        args.batch_size,
    )
    manifest_cols = [
        "manifest_id",
        "inventory_run_id",
        "calculation_run_id",
        "station_id",
        "source_year",
        "raw_station_id",
        "download_url",
        "target_path",
        "priority_rank",
        "batch_number",
        "station_candidate_plant_links",
        "source_year_available_count",
        "source_year_missing_count",
        "manifest_status",
        "priority_reason",
        "notes",
    ]
    write_csv(staging_dir / "noaa_raw_backfill_manifest.csv", manifest_cols, manifest_rows)

    source_file_id = f"{SOURCE_FAMILY}_{sha256_text(args.base_url.rstrip('/') + '|' + str(args.target_root))[:16]}"
    source_row = {
        "source_file_id": source_file_id,
        "source_family": SOURCE_FAMILY,
        "source_url": args.base_url.rstrip("/") + "/",
        "local_path": str(args.target_root),
        "file_name": "noaa_global_hourly_backfill_manifest",
        "size_bytes": None,
        "sha256": None,
        "retrieved_at_utc": utc_now().isoformat(timespec="seconds"),
        "source_year": None,
        "source_release": "planned_backfill_urls_from_latest_raw_inventory",
        "notes": "Prioritized download URL and target-path manifest for missing NOAA Global Hourly station-year files.",
    }
    params = {
        "inventory_run_id": inventory_run_id,
        "base_url": args.base_url.rstrip("/") + "/",
        "target_root": str(args.target_root),
        "batch_size": args.batch_size,
        "include_known_missing_aws": args.include_known_missing_aws,
        "known_missing_aws_rule": "default excludes station-years with prior missing_on_aws terminal AWS 404 evidence",
        "priority_rule": [
            "zero_local_files_for_year_desc",
            "source_year_desc",
            "station_candidate_plant_links_desc",
            "station_id_asc",
        ],
        "download_attempted": False,
    }
    load_sql = build_load_sql(staging_dir, source_row, run_id, code_commit, params)
    sql_path = staging_dir / "load.sql"
    sql_path.write_text(load_sql, encoding="utf-8")
    run(psql_cmd(args.psql, args.host, args.port, args.dbname, args.user) + ["-f", str(sql_path)])

    db_counts = report_counts(args.psql, args.host, args.port, args.dbname, args.user, run_id)
    report_path = args.project_root / "docs" / "noaa_backfill_manifest_report.md"
    render_report(
        report_path,
        run_id,
        inventory_run_id,
        code_commit,
        source_row,
        args.target_root,
        args.batch_size,
        manifest_rows,
        db_counts,
        args.host,
        args.port,
        args.dbname,
    )

    print(
        json.dumps(
            {
                "run_id": run_id,
                "inventory_run_id": inventory_run_id,
                "source_file_id": source_file_id,
                "staging_dir": str(staging_dir),
                "report_path": str(report_path),
                "manifest_rows": len(manifest_rows),
                "batch_size": args.batch_size,
                "batch_count": math.ceil(len(manifest_rows) / args.batch_size) if manifest_rows else 0,
                "first_batch_rows": min(len(manifest_rows), args.batch_size),
                "db_counts": db_counts,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
