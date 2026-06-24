#!/usr/bin/env python3
"""Reclassify NOAA Global Hourly HTTP 404 outcomes as missing AWS objects."""

from __future__ import annotations

import argparse
import csv
import io
import json
import subprocess
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path

from eop012_config import PROJECT_ROOT, PSQL

METHODOLOGY_VERSION = "eop012-ecwt-method-v0.1.0"
DOWNLOAD_STATUS_VALUES = ("downloaded", "skipped_existing", "missing_on_aws", "failed_http", "failed_exception", "dry_run")
MANIFEST_STATUS_VALUES = ("planned", "downloaded", "skipped", "missing", "failed")


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def sql_literal(value: object) -> str:
    if value is None:
        return "null"
    text = str(value)
    return "'" + text.replace("'", "''") + "'"


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


def git_commit_label(project_root: Path) -> str:
    try:
        result = run(["git", "-C", str(project_root), "rev-parse", "HEAD"])
        return result.stdout.strip()
    except Exception:
        return "UNCOMMITTED_WORKTREE"


def status_counts(psql: Path, host: str, port: int, dbname: str, user: str | None) -> list[dict[str, str]]:
    return psql_csv_query(
        psql,
        host,
        port,
        dbname,
        """
        select
            'download_attempt' as object_type,
            download_status as status,
            coalesce(http_status::text, '') as http_status,
            count(*)::text as rows
        from weather.noaa_raw_download_attempt
        group by download_status, http_status
        union all
        select
            'manifest' as object_type,
            manifest_status as status,
            '' as http_status,
            count(*)::text as rows
        from weather.noaa_raw_backfill_manifest
        group by manifest_status
        order by object_type, status, http_status
        """,
        user,
    )


def apply_reclassification(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    run_id: str,
    code_commit: str,
) -> OrderedDict[str, str]:
    download_status_sql = ", ".join(sql_literal(status) for status in DOWNLOAD_STATUS_VALUES)
    manifest_status_sql = ", ".join(sql_literal(status) for status in MANIFEST_STATUS_VALUES)
    params = {
        "attempt_rule": "download_status failed_http with http_status 404 becomes missing_on_aws",
        "manifest_rule": "failed manifest rows with a matching missing_on_aws attempt become missing",
    }
    sql = f"""
    begin;

    alter table weather.noaa_raw_download_attempt
        drop constraint if exists noaa_raw_download_attempt_status_check;
    alter table weather.noaa_raw_download_attempt
        add constraint noaa_raw_download_attempt_status_check
        check (download_status in ({download_status_sql}));

    alter table weather.noaa_raw_backfill_manifest
        drop constraint if exists noaa_raw_backfill_manifest_status_check;
    alter table weather.noaa_raw_backfill_manifest
        add constraint noaa_raw_backfill_manifest_status_check
        check (manifest_status in ({manifest_status_sql}));

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
        'Initial auditable methodology version for asset loading, station matching, raw file inventory, backfill planning, download attempts, coverage auditing, and ECWT calculation.'
    )
    on conflict (methodology_version) do update set notes = excluded.notes;

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
        now(),
        now(),
        'succeeded',
        {sql_literal(json.dumps(params, sort_keys=True))}::jsonb,
        'Reclassified NOAA HTTP 404 outcomes as terminal missing AWS objects instead of generic download failures.'
    )
    on conflict (calculation_run_id) do update set
        run_finished_at_utc = excluded.run_finished_at_utc,
        run_status = excluded.run_status,
        parameters_json = excluded.parameters_json,
        notes = excluded.notes;

    with changed_attempts as (
        update weather.noaa_raw_download_attempt
        set
            download_status = 'missing_on_aws',
            notes = 'NOAA public AWS endpoint returned HTTP 404 Not Found; terminal missing object, not a corrupt download.'
        where download_status = 'failed_http'
          and http_status = 404
        returning 1
    ),
    changed_manifest as (
        update weather.noaa_raw_backfill_manifest manifest
        set
            manifest_status = 'missing',
            notes = 'Latest download attempt returned HTTP 404 Not Found from NOAA public AWS endpoint; terminal missing object.'
        where manifest.manifest_status = 'failed'
          and exists (
              select 1
              from weather.noaa_raw_download_attempt attempt
              where attempt.manifest_id = manifest.manifest_id
                and attempt.download_status = 'missing_on_aws'
                and attempt.http_status = 404
          )
        returning 1
    )
    select 'download_attempt_rows_reclassified' as metric, count(*)::text as value from changed_attempts
    union all
    select 'manifest_rows_reclassified' as metric, count(*)::text as value from changed_manifest;

    commit;
    """
    result = run(psql_cmd(psql, host, port, dbname, user) + ["-At", "-F", "|", "-c", sql])
    metrics: OrderedDict[str, str] = OrderedDict()
    for line in result.stdout.splitlines():
        if "|" not in line:
            continue
        key, value = line.split("|", 1)
        metrics[key] = value
    return metrics


def render_status_table(lines: list[str], rows: list[dict[str, str]]) -> None:
    lines.extend(["| Object | Status | HTTP | Rows |", "| --- | --- | ---: | ---: |"])
    for row in rows:
        http_status = row["http_status"] or ""
        lines.append(f"| `{row['object_type']}` | `{row['status']}` | {http_status} | {row['rows']} |")


def render_report(
    path: Path,
    run_id: str,
    code_commit: str,
    host: str,
    port: int,
    dbname: str,
    before: list[dict[str, str]],
    after: list[dict[str, str]],
    metrics: OrderedDict[str, str],
) -> None:
    lines = [
        "# NOAA 404 Reclassification Report",
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
        "## Rows Changed",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
    ]
    for key, value in metrics.items():
        lines.append(f"| `{key}` | {value} |")
    lines.extend(["", "## Status Counts Before", ""])
    render_status_table(lines, before)
    lines.extend(["", "## Status Counts After", ""])
    render_status_table(lines, after)
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- NOAA HTTP 404 responses are now classified as `missing_on_aws` in `weather.noaa_raw_download_attempt`.",
            "- Matching manifest rows are now classified as `missing` instead of generic `failed`.",
            "- Non-404 HTTP errors remain `failed_http` so they can be retried separately.",
            "- This reclassification does not alter downloaded files or canonical weather rows.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--psql", type=Path, default=PSQL)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5436)
    parser.add_argument("--dbname", default="eop012")
    parser.add_argument("--user", default=None)
    args = parser.parse_args()

    if not args.psql.exists():
        raise FileNotFoundError(args.psql)

    code_commit = git_commit_label(args.project_root)
    run_id = f"noaa_404_missing_reclassification_{utc_now().strftime('%Y%m%dT%H%M%SZ')}"
    before = status_counts(args.psql, args.host, args.port, args.dbname, args.user)
    metrics = apply_reclassification(args.psql, args.host, args.port, args.dbname, args.user, run_id, code_commit)
    after = status_counts(args.psql, args.host, args.port, args.dbname, args.user)
    report_path = args.project_root / "docs" / "noaa_404_reclassification_report.md"
    render_report(report_path, run_id, code_commit, args.host, args.port, args.dbname, before, after, metrics)

    print(
        json.dumps(
            {
                "run_id": run_id,
                "report_path": str(report_path),
                "metrics": metrics,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
