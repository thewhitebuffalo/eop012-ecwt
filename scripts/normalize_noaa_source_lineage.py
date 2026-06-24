#!/usr/bin/env python3
"""Normalize NOAA Global Hourly per-file source lineage after local inventory loading.

Early rebuild inventory loads intentionally avoided hashing every raw NOAA CSV.
That left many loaded files and canonical hourly rows pointing at one coarse
local-inventory source record. This script converts those rows to per-file
SHA-256 source_file records without reparsing or changing weather values.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import subprocess
import sys
import time
from collections import Counter, OrderedDict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from eop012_config import PROJECT_ROOT, PSQL, STAGING_ROOT

METHODOLOGY_VERSION = "eop012-ecwt-method-v0.1.0"
SOURCE_FAMILY = "noaa_global_hourly_csv"
SOURCE_RELEASE = "noaa_global_hourly_access_csv"
GENERIC_SOURCE_FAMILY = "noaa_global_hourly_local_raw_inventory"
AWS_BASE_URL = "https://noaa-global-hourly-pds.s3.amazonaws.com"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def sql_literal(value: object) -> str:
    if value is None:
        return "null"
    return "'" + str(value).replace("'", "''") + "'"


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


def psql_cmd(psql: Path, host: str, port: int, dbname: str, user: str | None) -> list[str]:
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
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: pg_csv_value(row.get(field)) for field in fieldnames})


def copy_command(table: str, columns: list[str], path: Path) -> str:
    escaped_path = str(path).replace("'", "''")
    return f"\\copy {table} ({', '.join(columns)}) from '{escaped_path}' with (format csv, header true, null '\\N')"


def git_commit_label(project_root: Path) -> str:
    try:
        return run(["git", "-C", str(project_root), "rev-parse", "HEAD"]).stdout.strip()
    except Exception:
        return "UNCOMMITTED_WORKTREE"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def source_file_id(source_year: int, raw_station_id: str, digest: str) -> str:
    return f"{SOURCE_FAMILY}_{source_year}_{raw_station_id}_{digest[:16]}"


def candidate_query(limit_files: int | None, source_year: int | None) -> str:
    limit_clause = "" if limit_files is None else f"limit {int(limit_files)}"
    year_clause = "" if source_year is None else f"and lf.source_year = {int(source_year)}"
    return f"""
    select
        lf.load_file_id,
        lf.calculation_run_id as load_calculation_run_id,
        lf.station_id,
        lf.source_year::text as source_year,
        lf.raw_station_id,
        lf.local_path,
        lf.source_file_id as old_source_file_id,
        lf.file_size_bytes::text as recorded_file_size_bytes,
        lf.source_basis,
        sf.source_family as old_source_family,
        sf.sha256 as old_sha256
    from weather.noaa_hourly_load_file lf
    left join audit.source_file sf
      on sf.source_file_id = lf.source_file_id
    where lf.file_status = 'loaded'
      and lf.local_path is not null
      and (
        coalesce(sf.sha256, '') = ''
        or sf.source_family = {sql_literal(GENERIC_SOURCE_FAMILY)}
      )
      {year_clause}
    order by lf.source_year, lf.station_id, lf.local_path
    {limit_clause}
    """


def fetch_candidates(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    limit_files: int | None,
    source_year: int | None,
) -> list[dict[str, str]]:
    return psql_csv_query(psql, host, port, dbname, user, candidate_query(limit_files, source_year))


def hash_candidate(
    row: dict[str, str],
    run_id: str,
) -> tuple[dict[str, object] | None, dict[str, object] | None, dict[str, object] | None]:
    path = Path(row["local_path"])
    entity_id = row["load_file_id"]
    if not path.exists():
        return None, None, {
            "exception_id": f"{run_id}:missing_file:{hashlib.sha256(entity_id.encode()).hexdigest()[:16]}",
            "calculation_run_id": run_id,
            "entity_type": "weather.noaa_hourly_load_file",
            "entity_id": entity_id,
            "severity": "warning",
            "reason_code": "local_raw_file_missing",
            "message": f"Local NOAA CSV missing: {path}",
            "resolution_status": "open",
            "notes": "Source lineage was not normalized for this loaded file.",
        }
    size = path.stat().st_size
    digest = sha256_file(path)
    source_year = int(row["source_year"])
    raw_station_id = row["raw_station_id"]
    sfid = source_file_id(source_year, raw_station_id, digest)
    source_url = f"{AWS_BASE_URL}/{source_year}/{raw_station_id}.csv"
    mapping = {
        "lineage_id": f"{run_id}:load_file:{hashlib.sha256(entity_id.encode()).hexdigest()[:16]}",
        "calculation_run_id": run_id,
        "load_file_id": row["load_file_id"],
        "load_calculation_run_id": row["load_calculation_run_id"],
        "station_id": row["station_id"],
        "source_year": source_year,
        "raw_station_id": raw_station_id,
        "old_source_file_id": row["old_source_file_id"],
        "new_source_file_id": sfid,
        "local_path": str(path),
        "recorded_file_size_bytes": row.get("recorded_file_size_bytes") or None,
        "actual_file_size_bytes": size,
        "file_sha256": digest,
        "source_basis": row.get("source_basis"),
        "notes": "Per-file NOAA source lineage normalized from earlier local raw inventory source record.",
    }
    source_row = {
        "source_file_id": sfid,
        "source_family": SOURCE_FAMILY,
        "source_url": source_url,
        "local_path": str(path),
        "file_name": path.name,
        "size_bytes": size,
        "sha256": digest,
        "retrieved_at_utc": utc_now().isoformat(timespec="seconds"),
        "source_year": source_year,
        "source_release": SOURCE_RELEASE,
        "notes": "NOAA Global Hourly CSV observed in local raw cache by source-lineage normalizer.",
    }
    return mapping, source_row, None


def build_hash_rows(
    candidates: list[dict[str, str]],
    run_id: str,
    workers: int,
    progress_every: int,
) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    mappings: list[dict[str, object]] = []
    source_by_id: OrderedDict[str, dict[str, object]] = OrderedDict()
    exceptions: list[dict[str, object]] = []
    started = time.monotonic()
    completed = 0
    with ThreadPoolExecutor(max_workers=max(1, workers)) as executor:
        futures = [executor.submit(hash_candidate, row, run_id) for row in candidates]
        for future in as_completed(futures):
            mapping, source_row, exception_row = future.result()
            completed += 1
            if mapping is not None:
                mappings.append(mapping)
            if source_row is not None:
                source_by_id.setdefault(str(source_row["source_file_id"]), source_row)
            if exception_row is not None:
                exceptions.append(exception_row)
            if progress_every and (completed % progress_every == 0 or completed == len(candidates)):
                elapsed = max(time.monotonic() - started, 0.001)
                rate = completed / elapsed
                print(
                    f"hashed {completed}/{len(candidates)} files "
                    f"({rate:.1f} files/sec, mappings={len(mappings)}, exceptions={len(exceptions)})",
                    flush=True,
                )
    mappings.sort(key=lambda row: (int(row["source_year"]), str(row["station_id"]), str(row["local_path"])))
    return mappings, list(source_by_id.values()), exceptions


def pre_counts(psql: Path, host: str, port: int, dbname: str, user: str | None) -> dict[str, str]:
    rows = psql_csv_query(
        psql,
        host,
        port,
        dbname,
        user,
        f"""
        select
            count(*) filter (where lf.file_status = 'loaded')::text as loaded_file_rows,
            count(*) filter (
                where lf.file_status = 'loaded'
                  and (coalesce(sf.sha256, '') = '' or sf.source_family = {sql_literal(GENERIC_SOURCE_FAMILY)})
            )::text as loaded_file_rows_needing_lineage,
            count(distinct lf.local_path) filter (
                where lf.file_status = 'loaded'
                  and (coalesce(sf.sha256, '') = '' or sf.source_family = {sql_literal(GENERIC_SOURCE_FAMILY)})
            )::text as paths_needing_lineage
        from weather.noaa_hourly_load_file lf
        left join audit.source_file sf
          on sf.source_file_id = lf.source_file_id
        """,
    )[0]
    hourly = psql_csv_query(
        psql,
        host,
        port,
        dbname,
        user,
        f"""
        select
            count(*)::text as hourly_rows,
            count(*) filter (
                where coalesce(sf.sha256, '') = ''
                   or sf.source_family = {sql_literal(GENERIC_SOURCE_FAMILY)}
            )::text as hourly_rows_needing_lineage
        from weather.hourly_djf h
        left join audit.source_file sf
          on sf.source_file_id = h.source_file_id
        """,
    )[0]
    rows.update(hourly)
    return rows


def post_counts(psql: Path, host: str, port: int, dbname: str, user: str | None, run_id: str) -> dict[str, str]:
    rows = pre_counts(psql, host, port, dbname, user)
    run_rows = psql_csv_query(
        psql,
        host,
        port,
        dbname,
        user,
        f"""
        select
            count(*)::text as lineage_mapping_rows,
            count(distinct new_source_file_id)::text as distinct_new_source_files
        from audit.noaa_source_lineage_normalization
        where calculation_run_id = {sql_literal(run_id)}
        """,
    )[0]
    relink_rows = psql_csv_query(
        psql,
        host,
        port,
        dbname,
        user,
        f"""
        select
            coalesce(sum(hourly_rows_relinked), 0)::text as hourly_rows_relinked
        from audit.noaa_source_lineage_relink_batch
        where calculation_run_id = {sql_literal(run_id)}
        """,
    )[0]
    rows.update(run_rows)
    rows.update(relink_rows)
    return rows


def initialize_run_sql(
    staging_dir: Path,
    run_id: str,
    code_commit: str,
    params: dict[str, object],
    source_cols: list[str],
    mapping_cols: list[str],
    exception_cols: list[str],
) -> str:
    return "\n".join(
        [
            "\\set ON_ERROR_STOP on",
            "begin;",
            f"""
insert into audit.methodology_version (
    methodology_version,
    methodology_name,
    effective_at_utc,
    source_standard,
    notes
) values (
    {sql_literal(METHODOLOGY_VERSION)},
    'EOP012 ECWT national calculation methodology',
    now(),
    'NERC EOP-012-3; EPRI 3002030362 guidance',
    'Initial auditable methodology version for asset loading, station matching, raw file inventory, coverage auditing, and ECWT calculation.'
)
on conflict (methodology_version) do update set notes = excluded.notes;
""",
            f"""
insert into audit.calculation_run (
    calculation_run_id,
    methodology_version,
    code_commit,
    run_started_at_utc,
    run_status,
    parameters_json,
    notes
) values (
    {sql_literal(run_id)},
    {sql_literal(METHODOLOGY_VERSION)},
    {sql_literal(code_commit)},
    now(),
    'running',
    {sql_literal(json.dumps(params, sort_keys=True))}::jsonb,
    'Normalizing NOAA loaded weather source lineage from coarse local inventory source IDs to per-file SHA-256 source_file records.'
)
on conflict (calculation_run_id) do update set
    code_commit = excluded.code_commit,
    run_status = excluded.run_status,
    parameters_json = excluded.parameters_json,
    notes = excluded.notes;
""",
            """
create table if not exists audit.noaa_source_lineage_normalization (
    lineage_id text primary key,
    calculation_run_id text not null references audit.calculation_run(calculation_run_id),
    load_file_id text not null,
    load_calculation_run_id text not null references audit.calculation_run(calculation_run_id),
    station_id text not null references weather.station(station_id),
    source_year integer not null,
    raw_station_id text not null,
    old_source_file_id text references audit.source_file(source_file_id),
    new_source_file_id text not null references audit.source_file(source_file_id),
    local_path text not null,
    recorded_file_size_bytes bigint,
    actual_file_size_bytes bigint not null,
    file_sha256 text not null,
    source_basis text,
    notes text,
    created_at_utc timestamptz not null default now(),
    unique (calculation_run_id, load_file_id)
);
create index if not exists ix_noaa_source_lineage_norm_year
    on audit.noaa_source_lineage_normalization (calculation_run_id, source_year);
create index if not exists ix_noaa_source_lineage_norm_load_run
    on audit.noaa_source_lineage_normalization (load_calculation_run_id, station_id, source_year);
create table if not exists audit.noaa_source_lineage_relink_batch (
    batch_id text primary key,
    calculation_run_id text not null references audit.calculation_run(calculation_run_id),
    source_year integer not null,
    hourly_rows_relinked bigint not null,
    started_at_utc timestamptz not null,
    finished_at_utc timestamptz not null,
    notes text,
    created_at_utc timestamptz not null default now()
);
""",
            """
create temp table stg_source_file (
    source_file_id text,
    source_family text,
    source_url text,
    local_path text,
    file_name text,
    size_bytes bigint,
    sha256 text,
    retrieved_at_utc timestamptz,
    source_year integer,
    source_release text,
    notes text
) on commit drop;
""",
            copy_command("stg_source_file", source_cols, staging_dir / "source_files.csv"),
            """
insert into audit.source_file (
    source_file_id,
    source_family,
    source_url,
    local_path,
    file_name,
    size_bytes,
    sha256,
    retrieved_at_utc,
    source_year,
    source_release,
    notes
)
select
    source_file_id,
    source_family,
    source_url,
    local_path,
    file_name,
    size_bytes,
    sha256,
    retrieved_at_utc,
    source_year,
    source_release,
    notes
from stg_source_file
on conflict (source_file_id) do update set
    source_family = excluded.source_family,
    source_url = excluded.source_url,
    local_path = excluded.local_path,
    file_name = excluded.file_name,
    size_bytes = excluded.size_bytes,
    sha256 = excluded.sha256,
    retrieved_at_utc = excluded.retrieved_at_utc,
    source_year = excluded.source_year,
    source_release = excluded.source_release,
    notes = excluded.notes;
""",
            """
create temp table stg_noaa_source_lineage (
    lineage_id text,
    calculation_run_id text,
    load_file_id text,
    load_calculation_run_id text,
    station_id text,
    source_year integer,
    raw_station_id text,
    old_source_file_id text,
    new_source_file_id text,
    local_path text,
    recorded_file_size_bytes bigint,
    actual_file_size_bytes bigint,
    file_sha256 text,
    source_basis text,
    notes text
) on commit drop;
""",
            copy_command("stg_noaa_source_lineage", mapping_cols, staging_dir / "lineage_mapping.csv"),
            """
insert into audit.noaa_source_lineage_normalization (
    lineage_id,
    calculation_run_id,
    load_file_id,
    load_calculation_run_id,
    station_id,
    source_year,
    raw_station_id,
    old_source_file_id,
    new_source_file_id,
    local_path,
    recorded_file_size_bytes,
    actual_file_size_bytes,
    file_sha256,
    source_basis,
    notes
)
select
    lineage_id,
    calculation_run_id,
    load_file_id,
    load_calculation_run_id,
    station_id,
    source_year,
    raw_station_id,
    old_source_file_id,
    new_source_file_id,
    local_path,
    recorded_file_size_bytes,
    actual_file_size_bytes,
    file_sha256,
    source_basis,
    notes
from stg_noaa_source_lineage
on conflict (calculation_run_id, load_file_id) do update set
    load_calculation_run_id = excluded.load_calculation_run_id,
    station_id = excluded.station_id,
    source_year = excluded.source_year,
    raw_station_id = excluded.raw_station_id,
    old_source_file_id = excluded.old_source_file_id,
    new_source_file_id = excluded.new_source_file_id,
    local_path = excluded.local_path,
    recorded_file_size_bytes = excluded.recorded_file_size_bytes,
    actual_file_size_bytes = excluded.actual_file_size_bytes,
    file_sha256 = excluded.file_sha256,
    source_basis = excluded.source_basis,
    notes = excluded.notes;
""",
            """
update weather.noaa_hourly_load_file lf
set
    source_file_id = stg.new_source_file_id,
    file_size_bytes = stg.actual_file_size_bytes,
    notes = concat_ws(' ', nullif(lf.notes, ''), 'Source lineage normalized to per-file SHA-256 audit.source_file.')
from stg_noaa_source_lineage stg
where lf.load_file_id = stg.load_file_id
  and lf.source_file_id = stg.old_source_file_id;
""",
            """
update weather.noaa_raw_file_inventory inv
set
    source_file_id = stg.new_source_file_id,
    file_size_bytes = stg.actual_file_size_bytes,
    notes = concat_ws(' ', nullif(inv.notes, ''), 'Source lineage normalized to per-file SHA-256 audit.source_file.')
from stg_noaa_source_lineage stg
where inv.station_id = stg.station_id
  and inv.source_year = stg.source_year
  and inv.local_path = stg.local_path
  and inv.source_file_id = stg.old_source_file_id;
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


def relink_hourly_year(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    run_id: str,
    source_year: int,
) -> int:
    batch_id = f"{run_id}:year:{source_year}"
    sql = f"""
\\set ON_ERROR_STOP on
begin;
create temp table stg_relink_result (rows_relinked bigint) on commit drop;
with updated as (
    update weather.hourly_djf h
    set source_file_id = m.new_source_file_id
    from audit.noaa_source_lineage_normalization m
    where m.calculation_run_id = {sql_literal(run_id)}
      and m.source_year = {int(source_year)}
      and h.station_id = m.station_id
      and h.calculation_run_id = m.load_calculation_run_id
      and h.source_file_id = m.old_source_file_id
      and h.hour_ending_utc >= make_timestamptz({int(source_year)}, 1, 1, 0, 0, 0, 'UTC')
      and h.hour_ending_utc < make_timestamptz({int(source_year) + 1}, 1, 1, 0, 0, 0, 'UTC')
    returning 1
)
insert into stg_relink_result
select count(*) from updated;
insert into audit.noaa_source_lineage_relink_batch (
    batch_id,
    calculation_run_id,
    source_year,
    hourly_rows_relinked,
    started_at_utc,
    finished_at_utc,
    notes
)
select
    {sql_literal(batch_id)},
    {sql_literal(run_id)},
    {int(source_year)},
    rows_relinked,
    now(),
    now(),
    'Relinked existing canonical DJF hourly rows to per-file SHA-256 source_file records.'
from stg_relink_result
on conflict (batch_id) do update set
    hourly_rows_relinked = excluded.hourly_rows_relinked,
    finished_at_utc = excluded.finished_at_utc,
    notes = excluded.notes;
commit;
select hourly_rows_relinked from audit.noaa_source_lineage_relink_batch where batch_id = {sql_literal(batch_id)};
"""
    result = run(psql_cmd(psql, host, port, dbname, user) + ["-At"], input_text=sql)
    lines = [line.strip() for line in result.stdout.splitlines() if line.strip() and not line.startswith(("BEGIN", "COMMIT"))]
    return int(lines[-1]) if lines else 0


def finish_run(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    run_id: str,
    status: str,
    notes: str,
) -> None:
    run(
        psql_cmd(psql, host, port, dbname, user)
        + [
            "-c",
            f"""
            update audit.calculation_run
            set run_finished_at_utc = now(),
                run_status = {sql_literal(status)},
                notes = {sql_literal(notes)}
            where calculation_run_id = {sql_literal(run_id)}
            """,
        ]
    )


def render_report(
    report_path: Path,
    run_id: str,
    code_commit: str,
    args: argparse.Namespace,
    candidates: list[dict[str, str]],
    mappings: list[dict[str, object]],
    source_rows: list[dict[str, object]],
    exceptions: list[dict[str, object]],
    before_counts: dict[str, str],
    after_counts: dict[str, str] | None,
    relink_by_year: OrderedDict[int, int],
    mapping_csv_path: Path,
) -> None:
    by_year = Counter(int(row["source_year"]) for row in mappings)
    year_rows = [{"source_year": year, "files": count} for year, count in sorted(by_year.items())]
    lines = [
        "# NOAA Source Lineage Normalization Report",
        "",
        f"Generated UTC: {utc_now().isoformat(timespec='seconds')}",
        "",
        "## Run",
        "",
        f"- Calculation run ID: `{run_id}`",
        f"- Code commit: `{code_commit}`",
        f"- Dry run: `{args.dry_run}`",
        f"- Hourly relink skipped: `{args.skip_hourly_relink}`",
        f"- Candidate file limit: `{args.limit_files if args.limit_files is not None else 'none'}`",
        f"- Source year filter: `{args.source_year if args.source_year is not None else 'none'}`",
        f"- Mapping CSV: `{mapping_csv_path.name}`",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| Candidate loaded file rows selected | {len(candidates)} |",
        f"| Files hashed and mapped | {len(mappings)} |",
        f"| Distinct new source_file rows | {len(source_rows)} |",
        f"| Exceptions | {len(exceptions)} |",
        f"| Hourly rows relinked | {sum(relink_by_year.values())} |",
        "",
        "## Before Counts",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| Loaded file rows | {before_counts['loaded_file_rows']} |",
        f"| Loaded file rows needing lineage | {before_counts['loaded_file_rows_needing_lineage']} |",
        f"| Paths needing lineage | {before_counts['paths_needing_lineage']} |",
        f"| Canonical hourly rows | {before_counts['hourly_rows']} |",
        f"| Canonical hourly rows needing lineage | {before_counts['hourly_rows_needing_lineage']} |",
        "",
    ]
    if after_counts is not None:
        lines.extend(
            [
                "## After Counts",
                "",
                "| Metric | Count |",
                "| --- | ---: |",
                f"| Loaded file rows | {after_counts['loaded_file_rows']} |",
                f"| Loaded file rows needing lineage | {after_counts['loaded_file_rows_needing_lineage']} |",
                f"| Paths needing lineage | {after_counts['paths_needing_lineage']} |",
                f"| Canonical hourly rows | {after_counts['hourly_rows']} |",
                f"| Canonical hourly rows needing lineage | {after_counts['hourly_rows_needing_lineage']} |",
                f"| Mapping rows for this run | {after_counts['lineage_mapping_rows']} |",
                f"| Distinct new source files for this run | {after_counts['distinct_new_source_files']} |",
                f"| Hourly rows relinked for this run | {after_counts['hourly_rows_relinked']} |",
                "",
            ]
        )
    lines.extend(["## Files Hashed By Source Year", "", "| Source Year | Files |", "| ---: | ---: |"])
    if year_rows:
        for row in year_rows:
            lines.append(f"| {row['source_year']} | {row['files']} |")
    else:
        lines.append("|  |  |")
    lines.extend(["", "## Hourly Relink By Source Year", "", "| Source Year | Hourly Rows Relinked |", "| ---: | ---: |"])
    if relink_by_year:
        for year, rows in relink_by_year.items():
            lines.append(f"| {year} | {rows} |")
    else:
        lines.append("|  |  |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- This script does not change temperatures, station-hour selection, coverage, or ECWT values.",
            "- It replaces coarse local-inventory source IDs with SHA-256-backed per-file NOAA Global Hourly source records.",
            "- Relinking `weather.hourly_djf` closes the audit gap for the rows actually used by ECWT calculations.",
            "- Any remaining rows needing lineage after this run should be treated as explicit source-audit debt before a compliance-facing release.",
        ]
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--staging-root", type=Path, default=STAGING_ROOT)
    parser.add_argument("--psql", type=Path, default=PSQL)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5436)
    parser.add_argument("--dbname", default="eop012")
    parser.add_argument("--user")
    parser.add_argument("--limit-files", type=int)
    parser.add_argument("--source-year", type=int)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--progress-every", type=int, default=500)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-hourly-relink", action="store_true")
    args = parser.parse_args()

    run_id = f"noaa_source_lineage_normalization_{utc_now().strftime('%Y%m%dT%H%M%SZ')}"
    code_commit = git_commit_label(args.project_root)
    staging_dir = args.staging_root / run_id
    staging_dir.mkdir(parents=True, exist_ok=True)
    before = pre_counts(args.psql, args.host, args.port, args.dbname, args.user)
    candidates = fetch_candidates(
        args.psql,
        args.host,
        args.port,
        args.dbname,
        args.user,
        args.limit_files,
        args.source_year,
    )
    print(f"selected {len(candidates)} candidate loaded files", flush=True)
    mappings, source_rows, exceptions = build_hash_rows(
        candidates,
        run_id,
        args.workers,
        args.progress_every,
    )

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
    mapping_cols = [
        "lineage_id",
        "calculation_run_id",
        "load_file_id",
        "load_calculation_run_id",
        "station_id",
        "source_year",
        "raw_station_id",
        "old_source_file_id",
        "new_source_file_id",
        "local_path",
        "recorded_file_size_bytes",
        "actual_file_size_bytes",
        "file_sha256",
        "source_basis",
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
    write_csv(staging_dir / "source_files.csv", source_cols, source_rows)
    write_csv(staging_dir / "lineage_mapping.csv", mapping_cols, mappings)
    write_csv(staging_dir / "exceptions.csv", exception_cols, exceptions)

    docs_dir = args.project_root / "docs"
    mapping_csv_path = docs_dir / f"{run_id}_mapping.csv"
    report_path = docs_dir / f"{run_id}_report.md"
    write_csv(mapping_csv_path, mapping_cols, mappings)

    relink_by_year: OrderedDict[int, int] = OrderedDict()
    after: dict[str, str] | None = None
    if not args.dry_run:
        params = {
            "source_family": SOURCE_FAMILY,
            "generic_source_family": GENERIC_SOURCE_FAMILY,
            "limit_files": args.limit_files,
            "source_year": args.source_year,
            "workers": args.workers,
            "skip_hourly_relink": args.skip_hourly_relink,
            "candidate_rows": len(candidates),
            "mapped_rows": len(mappings),
            "exception_rows": len(exceptions),
            "operation": "register per-file source_file rows, relink loaded files, relink canonical hourly rows by source year",
        }
        sql_path = staging_dir / "initialize.sql"
        sql_path.write_text(
            initialize_run_sql(staging_dir, run_id, code_commit, params, source_cols, mapping_cols, exception_cols),
            encoding="utf-8",
        )
        try:
            run(psql_cmd(args.psql, args.host, args.port, args.dbname, args.user) + ["-f", str(sql_path)])
            if not args.skip_hourly_relink:
                years = sorted({int(row["source_year"]) for row in mappings})
                for year in years:
                    started = time.monotonic()
                    rows = relink_hourly_year(args.psql, args.host, args.port, args.dbname, args.user, run_id, year)
                    relink_by_year[year] = rows
                    print(
                        f"relinked source_year={year}: {rows} hourly rows "
                        f"in {time.monotonic() - started:.1f}s",
                        flush=True,
                    )
            finish_run(
                args.psql,
                args.host,
                args.port,
                args.dbname,
                args.user,
                run_id,
                "succeeded",
                "Normalized NOAA source lineage to per-file SHA-256 records.",
            )
        except Exception:
            try:
                finish_run(
                    args.psql,
                    args.host,
                    args.port,
                    args.dbname,
                    args.user,
                    run_id,
                    "failed",
                    "NOAA source lineage normalization failed; inspect script output and staging SQL.",
                )
            except Exception as finish_exc:
                print(f"failed to mark run failed: {finish_exc}", file=sys.stderr)
            raise
        after = post_counts(args.psql, args.host, args.port, args.dbname, args.user, run_id)

    render_report(
        report_path,
        run_id,
        code_commit,
        args,
        candidates,
        mappings,
        source_rows,
        exceptions,
        before,
        after,
        relink_by_year,
        mapping_csv_path,
    )
    print(
        json.dumps(
            OrderedDict(
                [
                    ("run_id", run_id),
                    ("dry_run", args.dry_run),
                    ("candidate_files", len(candidates)),
                    ("mapped_files", len(mappings)),
                    ("source_file_rows", len(source_rows)),
                    ("exceptions", len(exceptions)),
                    ("hourly_rows_relinked", sum(relink_by_year.values())),
                    ("mapping_csv_path", str(mapping_csv_path)),
                    ("report_path", str(report_path)),
                ]
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
