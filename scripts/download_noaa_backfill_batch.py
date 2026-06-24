#!/usr/bin/env python3
"""Download one NOAA Global Hourly backfill manifest batch."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import os
import subprocess
import time
import urllib.error
import urllib.request
from collections import Counter, OrderedDict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from eop012_config import PROJECT_ROOT, PSQL, STAGING_ROOT

DEFAULT_STAGING_ROOT = STAGING_ROOT

METHODOLOGY_VERSION = "eop012-ecwt-method-v0.1.0"
SOURCE_FAMILY = "noaa_global_hourly_csv"
USER_AGENT = "eop012-ecwt-audit/0.1"


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


def git_commit_label(project_root: Path) -> str:
    try:
        result = run(["git", "-C", str(project_root), "rev-parse", "HEAD"])
        return result.stdout.strip()
    except Exception:
        return "UNCOMMITTED_WORKTREE"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def latest_manifest_run_id(psql: Path, host: str, port: int, dbname: str, user: str | None) -> str:
    run_id = psql_scalar(
        psql,
        host,
        port,
        dbname,
        """
        select calculation_run_id
        from audit.calculation_run
        where calculation_run_id like 'noaa_backfill_manifest_%'
          and run_status = 'succeeded'
        order by run_started_at_utc desc
        limit 1
        """,
        user,
    )
    if not run_id:
        raise RuntimeError("No succeeded noaa_backfill_manifest calculation run found.")
    return run_id


def manifest_batch_rows(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    manifest_run_id: str,
    batch_number: int,
    limit: int | None,
    include_non_planned: bool,
) -> list[dict[str, str]]:
    status_clause = "" if include_non_planned else "and manifest_status = 'planned'"
    limit_clause = "" if limit is None else f"limit {int(limit)}"
    return psql_csv_query(
        psql,
        host,
        port,
        dbname,
        f"""
        select
            manifest_id,
            calculation_run_id as manifest_run_id,
            inventory_run_id,
            station_id,
            source_year::text as source_year,
            raw_station_id,
            download_url,
            target_path,
            priority_rank::text as priority_rank,
            batch_number::text as batch_number,
            station_candidate_plant_links::text as station_candidate_plant_links
        from weather.noaa_raw_backfill_manifest
        where calculation_run_id = {sql_literal(manifest_run_id)}
          and batch_number = {batch_number}
          {status_clause}
        order by priority_rank
        {limit_clause}
        """,
        user,
    )


def source_file_id(source_year: int, raw_station_id: str, digest: str) -> str:
    return f"noaa_global_hourly_csv_{source_year}_{raw_station_id}_{digest[:16]}"


def download_one(row: dict[str, str], run_id: str, overwrite: bool, timeout: int, dry_run: bool) -> tuple[dict[str, object], dict[str, object] | None]:
    attempted = utc_now()
    target_path = Path(row["target_path"])
    source_year = int(row["source_year"])
    raw_station_id = row["raw_station_id"]
    source_row: dict[str, object] | None = None
    attempt: dict[str, object] = {
        "attempt_id": f"{run_id}:manifest:{row['manifest_id']}",
        "manifest_id": row["manifest_id"],
        "manifest_run_id": row["manifest_run_id"],
        "calculation_run_id": run_id,
        "station_id": row["station_id"],
        "source_year": source_year,
        "raw_station_id": raw_station_id,
        "download_url": row["download_url"],
        "target_path": str(target_path),
        "attempted_at_utc": attempted.isoformat(timespec="seconds"),
        "finished_at_utc": None,
        "http_status": None,
        "download_status": None,
        "file_size_bytes": None,
        "file_sha256": None,
        "source_file_id": None,
        "error_message": None,
        "notes": None,
    }
    try:
        if dry_run:
            attempt["download_status"] = "dry_run"
            attempt["finished_at_utc"] = utc_now().isoformat(timespec="seconds")
            attempt["notes"] = "Dry run; download not attempted."
            return attempt, None

        target_path.parent.mkdir(parents=True, exist_ok=True)
        if target_path.exists() and not overwrite:
            digest = sha256_file(target_path)
            size = target_path.stat().st_size
            sfid = source_file_id(source_year, raw_station_id, digest)
            attempt.update(
                {
                    "download_status": "skipped_existing",
                    "file_size_bytes": size,
                    "file_sha256": digest,
                    "source_file_id": sfid,
                    "finished_at_utc": utc_now().isoformat(timespec="seconds"),
                    "notes": "Target file already existed; no overwrite performed.",
                }
            )
            source_row = build_source_row(sfid, row, target_path, size, digest, attempt["finished_at_utc"], "Existing local file observed by downloader without overwrite.")
            return attempt, source_row

        temp_path = target_path.with_name(target_path.name + f".{os.getpid()}.part")
        if temp_path.exists():
            temp_path.unlink()
        request = urllib.request.Request(row["download_url"], headers={"User-Agent": USER_AGENT})
        digest_obj = hashlib.sha256()
        total = 0
        http_status: int | None = None
        with urllib.request.urlopen(request, timeout=timeout) as response:
            http_status = getattr(response, "status", None)
            with temp_path.open("wb") as f:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    f.write(chunk)
                    digest_obj.update(chunk)
                    total += len(chunk)
        digest = digest_obj.hexdigest()
        temp_path.replace(target_path)
        finished = utc_now().isoformat(timespec="seconds")
        sfid = source_file_id(source_year, raw_station_id, digest)
        attempt.update(
            {
                "http_status": http_status,
                "download_status": "downloaded",
                "file_size_bytes": total,
                "file_sha256": digest,
                "source_file_id": sfid,
                "finished_at_utc": finished,
                "notes": "Downloaded to temporary part file and atomically moved into target path.",
            }
        )
        source_row = build_source_row(sfid, row, target_path, total, digest, finished, "NOAA Global Hourly CSV downloaded by EOP012 backfill downloader.")
        return attempt, source_row
    except urllib.error.HTTPError as exc:
        cleanup_part(target_path)
        attempt.update(
            {
                "http_status": exc.code,
                "download_status": "failed_http",
                "finished_at_utc": utc_now().isoformat(timespec="seconds"),
                "error_message": str(exc)[:2000],
                "notes": "HTTP error from NOAA public endpoint.",
            }
        )
        return attempt, None
    except Exception as exc:
        cleanup_part(target_path)
        attempt.update(
            {
                "download_status": "failed_exception",
                "finished_at_utc": utc_now().isoformat(timespec="seconds"),
                "error_message": repr(exc)[:2000],
                "notes": "Downloader exception.",
            }
        )
        return attempt, None


def cleanup_part(target_path: Path) -> None:
    parent = target_path.parent
    if not parent.exists():
        return
    for part in parent.glob(target_path.name + ".*.part"):
        try:
            part.unlink()
        except OSError:
            pass


def build_source_row(
    sfid: str,
    row: dict[str, str],
    target_path: Path,
    size: int,
    digest: str,
    retrieved_at: object,
    notes: str,
) -> dict[str, object]:
    return {
        "source_file_id": sfid,
        "source_family": SOURCE_FAMILY,
        "source_url": row["download_url"],
        "local_path": str(target_path),
        "file_name": target_path.name,
        "size_bytes": size,
        "sha256": digest,
        "retrieved_at_utc": retrieved_at,
        "source_year": int(row["source_year"]),
        "source_release": "noaa_global_hourly_access_csv",
        "notes": notes,
    }


def run_downloads(
    rows: list[dict[str, str]],
    run_id: str,
    overwrite: bool,
    timeout: int,
    max_workers: int,
    dry_run: bool,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    attempts: list[dict[str, object]] = []
    source_rows_by_id: OrderedDict[str, dict[str, object]] = OrderedDict()
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(download_one, row, run_id, overwrite, timeout, dry_run) for row in rows]
        for future in as_completed(futures):
            attempt, source_row = future.result()
            attempts.append(attempt)
            if source_row:
                source_rows_by_id[str(source_row["source_file_id"])] = source_row
    attempts.sort(key=lambda item: str(item["manifest_id"]))
    return attempts, list(source_rows_by_id.values())


def render_values_insert(table: str, columns: list[str], rows: list[dict[str, object]], conflict: str) -> str:
    if not rows:
        return f"-- no rows for {table}\n"
    values = []
    for row in rows:
        values.append("(" + ", ".join(sql_literal(row.get(col)) for col in columns) + ")")
    return f"insert into {table} ({', '.join(columns)}) values\n" + ",\n".join(values) + f"\n{conflict};\n"


def copy_command(table: str, columns: list[str], path: Path) -> str:
    return f"\\copy {table} ({', '.join(columns)}) from '{path}' with (format csv, header true, null '\\N')"


def build_load_sql(
    staging_dir: Path,
    run_id: str,
    manifest_run_id: str,
    code_commit: str,
    params: dict[str, object],
    has_source_rows: bool,
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
    attempt_cols = [
        "attempt_id",
        "manifest_id",
        "manifest_run_id",
        "calculation_run_id",
        "station_id",
        "source_year",
        "raw_station_id",
        "download_url",
        "target_path",
        "attempted_at_utc",
        "finished_at_utc",
        "http_status",
        "download_status",
        "file_size_bytes",
        "file_sha256",
        "source_file_id",
        "error_message",
        "notes",
    ]
    source_load = ""
    if has_source_rows:
        source_load = "\n".join(
            [
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
            ]
        )
    return "\n".join(
        [
            "\\set ON_ERROR_STOP on",
            "begin;",
            """
create table if not exists weather.noaa_raw_download_attempt (
    attempt_id text primary key,
    manifest_id text not null references weather.noaa_raw_backfill_manifest(manifest_id),
    manifest_run_id text not null references audit.calculation_run(calculation_run_id),
    calculation_run_id text not null references audit.calculation_run(calculation_run_id),
    station_id text not null references weather.station(station_id),
    source_year integer not null,
    raw_station_id text not null,
    download_url text not null,
    target_path text not null,
    attempted_at_utc timestamptz not null,
    finished_at_utc timestamptz,
    http_status integer,
    download_status text not null,
    file_size_bytes bigint,
    file_sha256 text,
    source_file_id text references audit.source_file(source_file_id),
    error_message text,
    notes text,
    created_at_utc timestamptz not null default now(),
    unique (manifest_id, calculation_run_id),
    constraint noaa_raw_download_attempt_status_check
        check (download_status in ('downloaded', 'skipped_existing', 'failed_http', 'failed_exception', 'dry_run')),
    constraint noaa_raw_download_attempt_sha256_len
        check (file_sha256 is null or length(file_sha256) = 64)
);
""",
            """
create index if not exists ix_noaa_raw_download_attempt_status
    on weather.noaa_raw_download_attempt (calculation_run_id, download_status);
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
                        "notes": "Initial auditable methodology version for asset loading, station matching, raw file inventory, backfill planning, download attempts, coverage auditing, and ECWT calculation.",
                    }
                ],
                "on conflict (methodology_version) do update set notes = excluded.notes",
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
    'Downloaded or attempted one NOAA Global Hourly backfill manifest batch.'
)
on conflict (calculation_run_id) do update set
    run_finished_at_utc = excluded.run_finished_at_utc,
    run_status = excluded.run_status,
    parameters_json = excluded.parameters_json,
    notes = excluded.notes;
""",
            source_load,
            """
create temp table stg_download_attempt (
    attempt_id text,
    manifest_id text,
    manifest_run_id text,
    calculation_run_id text,
    station_id text,
    source_year integer,
    raw_station_id text,
    download_url text,
    target_path text,
    attempted_at_utc timestamptz,
    finished_at_utc timestamptz,
    http_status integer,
    download_status text,
    file_size_bytes bigint,
    file_sha256 text,
    source_file_id text,
    error_message text,
    notes text
) on commit drop;
""",
            copy_command("stg_download_attempt", attempt_cols, staging_dir / "download_attempts.csv"),
            """
insert into weather.noaa_raw_download_attempt (
    attempt_id,
    manifest_id,
    manifest_run_id,
    calculation_run_id,
    station_id,
    source_year,
    raw_station_id,
    download_url,
    target_path,
    attempted_at_utc,
    finished_at_utc,
    http_status,
    download_status,
    file_size_bytes,
    file_sha256,
    source_file_id,
    error_message,
    notes
)
select
    attempt_id,
    manifest_id,
    manifest_run_id,
    calculation_run_id,
    station_id,
    source_year,
    raw_station_id,
    download_url,
    target_path,
    attempted_at_utc,
    finished_at_utc,
    http_status,
    download_status,
    file_size_bytes,
    file_sha256,
    source_file_id,
    error_message,
    notes
from stg_download_attempt
on conflict (manifest_id, calculation_run_id) do update set
    http_status = excluded.http_status,
    download_status = excluded.download_status,
    file_size_bytes = excluded.file_size_bytes,
    file_sha256 = excluded.file_sha256,
    source_file_id = excluded.source_file_id,
    error_message = excluded.error_message,
    notes = excluded.notes,
    finished_at_utc = excluded.finished_at_utc;
""",
            f"""
update weather.noaa_raw_backfill_manifest manifest
set manifest_status = case
    when attempt.download_status in ('downloaded', 'skipped_existing') then 'downloaded'
    when attempt.download_status = 'dry_run' then manifest.manifest_status
    when attempt.download_status in ('failed_http', 'failed_exception') then 'failed'
    else manifest.manifest_status
end,
notes = 'Latest download attempt run: {run_id}; status: ' || attempt.download_status
from stg_download_attempt attempt
where manifest.manifest_id = attempt.manifest_id
  and manifest.calculation_run_id = {sql_literal(manifest_run_id)};
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
    manifest_run_id: str,
    batch_number: int,
) -> OrderedDict[str, str]:
    queries = OrderedDict(
        [
            (
                "download attempts for this run",
                f"select count(*) from weather.noaa_raw_download_attempt where calculation_run_id = {sql_literal(run_id)};",
            ),
            (
                "downloaded",
                f"select count(*) from weather.noaa_raw_download_attempt where calculation_run_id = {sql_literal(run_id)} and download_status = 'downloaded';",
            ),
            (
                "skipped_existing",
                f"select count(*) from weather.noaa_raw_download_attempt where calculation_run_id = {sql_literal(run_id)} and download_status = 'skipped_existing';",
            ),
            (
                "failed_http",
                f"select count(*) from weather.noaa_raw_download_attempt where calculation_run_id = {sql_literal(run_id)} and download_status = 'failed_http';",
            ),
            (
                "failed_exception",
                f"select count(*) from weather.noaa_raw_download_attempt where calculation_run_id = {sql_literal(run_id)} and download_status = 'failed_exception';",
            ),
            (
                "downloaded bytes",
                f"select coalesce(sum(file_size_bytes),0) from weather.noaa_raw_download_attempt where calculation_run_id = {sql_literal(run_id)} and download_status in ('downloaded','skipped_existing');",
            ),
            (
                "remaining planned rows in batch",
                f"select count(*) from weather.noaa_raw_backfill_manifest where calculation_run_id = {sql_literal(manifest_run_id)} and batch_number = {batch_number} and manifest_status = 'planned';",
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
    manifest_run_id: str,
    code_commit: str,
    batch_number: int,
    max_workers: int,
    overwrite: bool,
    dry_run: bool,
    attempts: list[dict[str, object]],
    db_counts: OrderedDict[str, str],
    host: str,
    port: int,
    dbname: str,
) -> None:
    status_counts = Counter(str(attempt["download_status"]) for attempt in attempts)
    total_bytes = sum(int(attempt["file_size_bytes"] or 0) for attempt in attempts)
    failures = [attempt for attempt in attempts if str(attempt["download_status"]).startswith("failed")]
    lines = [
        "# NOAA Backfill Batch Download Report",
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
        f"- Manifest run ID: `{manifest_run_id}`",
        f"- Manifest batch number: `{batch_number}`",
        f"- Methodology version: `{METHODOLOGY_VERSION}`",
        f"- Code commit: `{code_commit}`",
        f"- Max workers: `{max_workers}`",
        f"- Overwrite enabled: `{overwrite}`",
        f"- Dry run: `{dry_run}`",
        "",
        "## Results",
        "",
        "| Status | Count |",
        "| --- | ---: |",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"| `{status}` | {count} |")
    lines.extend(
        [
            f"| `total_bytes_downloaded_or_observed` | {total_bytes} |",
            "",
            "## Database Row Counts",
            "",
            "| Relation or Check | Rows / Value |",
            "| --- | ---: |",
        ]
    )
    for label, count in db_counts.items():
        lines.append(f"| `{label}` | {count} |")
    lines.extend(
        [
            "",
            "## Failure Sample",
            "",
        ]
    )
    if not failures:
        lines.append("No failures recorded.")
    else:
        lines.extend(["| Status | HTTP | Station | Year | URL | Error |", "| --- | ---: | --- | ---: | --- | --- |"])
        for attempt in failures[:20]:
            lines.append(
                "| "
                f"`{attempt['download_status']}` | "
                f"{attempt['http_status'] or ''} | "
                f"`{attempt['station_id']}` | "
                f"{attempt['source_year']} | "
                f"`{attempt['download_url']}` | "
                f"{str(attempt['error_message'] or '')[:160]} |"
            )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Files are written through temporary `.part` files and moved into place only after the stream completes.",
            "- Existing files are not overwritten unless `--overwrite` is explicitly supplied.",
            "- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.",
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
    parser.add_argument("--manifest-run-id", default=None)
    parser.add_argument("--batch-number", type=int, default=1)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--max-workers", type=int, default=4)
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--include-non-planned", action="store_true")
    args = parser.parse_args()

    if not args.psql.exists():
        raise FileNotFoundError(args.psql)
    if args.batch_number <= 0:
        raise ValueError("--batch-number must be positive")
    if args.max_workers <= 0:
        raise ValueError("--max-workers must be positive")
    if args.limit is not None and args.limit <= 0:
        raise ValueError("--limit must be positive when supplied")

    manifest_run_id = args.manifest_run_id or latest_manifest_run_id(
        args.psql, args.host, args.port, args.dbname, args.user
    )
    rows = manifest_batch_rows(
        args.psql,
        args.host,
        args.port,
        args.dbname,
        args.user,
        manifest_run_id,
        args.batch_number,
        args.limit,
        args.include_non_planned,
    )
    if not rows:
        raise RuntimeError(f"No eligible manifest rows found for {manifest_run_id} batch {args.batch_number}.")

    code_commit = git_commit_label(args.project_root)
    run_timestamp = utc_now().strftime("%Y%m%dT%H%M%SZ")
    run_id = f"noaa_backfill_download_batch{args.batch_number}_{run_timestamp}"
    staging_dir = args.staging_root / run_id
    staging_dir.mkdir(parents=True, exist_ok=True)

    started = time.monotonic()
    attempts, source_rows = run_downloads(
        rows,
        run_id,
        args.overwrite,
        args.timeout,
        args.max_workers,
        args.dry_run,
    )
    elapsed_seconds = time.monotonic() - started

    attempt_cols = [
        "attempt_id",
        "manifest_id",
        "manifest_run_id",
        "calculation_run_id",
        "station_id",
        "source_year",
        "raw_station_id",
        "download_url",
        "target_path",
        "attempted_at_utc",
        "finished_at_utc",
        "http_status",
        "download_status",
        "file_size_bytes",
        "file_sha256",
        "source_file_id",
        "error_message",
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
    write_csv(staging_dir / "download_attempts.csv", attempt_cols, attempts)
    if source_rows:
        write_csv(staging_dir / "source_files.csv", source_cols, source_rows)

    status_counts = Counter(str(attempt["download_status"]) for attempt in attempts)
    params = {
        "manifest_run_id": manifest_run_id,
        "batch_number": args.batch_number,
        "limit": args.limit,
        "max_workers": args.max_workers,
        "timeout_seconds": args.timeout,
        "overwrite": args.overwrite,
        "dry_run": args.dry_run,
        "include_non_planned": args.include_non_planned,
        "attempt_rows": len(attempts),
        "elapsed_seconds": round(elapsed_seconds, 3),
        "status_counts": dict(status_counts),
    }
    load_sql = build_load_sql(staging_dir, run_id, manifest_run_id, code_commit, params, bool(source_rows))
    sql_path = staging_dir / "load.sql"
    sql_path.write_text(load_sql, encoding="utf-8")
    run(psql_cmd(args.psql, args.host, args.port, args.dbname, args.user) + ["-f", str(sql_path)])

    db_counts = report_counts(args.psql, args.host, args.port, args.dbname, args.user, run_id, manifest_run_id, args.batch_number)
    report_path = args.project_root / "docs" / f"noaa_backfill_download_batch{args.batch_number}_report.md"
    render_report(
        report_path,
        run_id,
        manifest_run_id,
        code_commit,
        args.batch_number,
        args.max_workers,
        args.overwrite,
        args.dry_run,
        attempts,
        db_counts,
        args.host,
        args.port,
        args.dbname,
    )

    print(
        json.dumps(
            {
                "run_id": run_id,
                "manifest_run_id": manifest_run_id,
                "batch_number": args.batch_number,
                "staging_dir": str(staging_dir),
                "report_path": str(report_path),
                "attempt_rows": len(attempts),
                "source_file_rows": len(source_rows),
                "elapsed_seconds": round(elapsed_seconds, 3),
                "status_counts": dict(status_counts),
                "db_counts": db_counts,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
