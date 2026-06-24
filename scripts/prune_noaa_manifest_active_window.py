#!/usr/bin/env python3
"""Skip NOAA backfill manifest rows outside a station's active DJF window."""

from __future__ import annotations

import argparse
import csv
import io
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from eop012_config import PROJECT_ROOT, PSQL

METHODOLOGY_VERSION = "eop012-ecwt-method-v0.1.0"


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


def git_commit_label(project_root: Path) -> str:
    try:
        return run(["git", "-C", str(project_root), "rev-parse", "HEAD"]).stdout.strip()
    except Exception:
        return "UNCOMMITTED_WORKTREE"


def latest_manifest_run_id(psql: Path, host: str, port: int, dbname: str, user: str | None) -> str:
    run_id = psql_scalar(
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
    if not run_id:
        raise RuntimeError("No succeeded noaa_backfill_manifest calculation run found.")
    return run_id


def no_djf_overlap_condition() -> str:
    return """
    st.first_observation_utc is not null
    and st.last_observation_utc is not null
    and not (
        (
            st.first_observation_utc < make_timestamptz(m.source_year, 3, 1, 0, 0, 0, 'UTC')
            and st.last_observation_utc >= make_timestamptz(m.source_year, 1, 1, 0, 0, 0, 'UTC')
        )
        or (
            st.first_observation_utc < make_timestamptz(m.source_year + 1, 1, 1, 0, 0, 0, 'UTC')
            and st.last_observation_utc >= make_timestamptz(m.source_year, 12, 1, 0, 0, 0, 'UTC')
        )
    )
    """


def summary_rows(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    manifest_run_id: str,
) -> list[dict[str, str]]:
    condition = no_djf_overlap_condition()
    return psql_csv_query(
        psql,
        host,
        port,
        dbname,
        user,
        f"""
        with candidates as (
            select
                m.station_id,
                m.source_year,
                m.station_candidate_plant_links,
                m.batch_number,
                m.priority_rank,
                st.station_name,
                st.state,
                st.country,
                st.first_observation_utc,
                st.last_observation_utc,
                {condition} as no_djf_active_overlap
            from weather.noaa_raw_backfill_manifest m
            join weather.station st using (station_id)
            where m.calculation_run_id = {sql_literal(manifest_run_id)}
              and m.manifest_status = 'planned'
        )
        select
            count(*)::text as planned_rows,
            count(*) filter (where no_djf_active_overlap)::text as rows_to_skip,
            count(distinct station_id) filter (where no_djf_active_overlap)::text as stations_to_skip,
            count(*) filter (where station_id like '999999-%')::text as planned_999999_rows,
            count(*) filter (where station_id like '999999-%' and no_djf_active_overlap)::text as rows_999999_to_skip,
            coalesce(sum(station_candidate_plant_links) filter (where no_djf_active_overlap), 0)::text as affected_candidate_links
        from candidates
        """,
    )


def sample_rows(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    manifest_run_id: str,
    limit: int,
) -> list[dict[str, str]]:
    condition = no_djf_overlap_condition()
    return psql_csv_query(
        psql,
        host,
        port,
        dbname,
        user,
        f"""
        select
            m.station_id,
            m.source_year::text as source_year,
            st.station_name,
            st.state,
            st.country,
            st.first_observation_utc::text as first_observation_utc,
            st.last_observation_utc::text as last_observation_utc,
            m.station_candidate_plant_links::text as station_candidate_plant_links,
            m.batch_number::text as batch_number,
            m.priority_rank::text as priority_rank
        from weather.noaa_raw_backfill_manifest m
        join weather.station st using (station_id)
        where m.calculation_run_id = {sql_literal(manifest_run_id)}
          and m.manifest_status = 'planned'
          and {condition}
        order by m.station_candidate_plant_links desc, m.priority_rank, m.station_id, m.source_year
        limit {int(limit)}
        """,
    )


def status_rows(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    manifest_run_id: str,
) -> list[dict[str, str]]:
    return psql_csv_query(
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


def update_sql(run_id: str, manifest_run_id: str, code_commit: str, dry_run: bool, params: dict[str, object]) -> str:
    condition = no_djf_overlap_condition()
    started = utc_now().isoformat(timespec="seconds")
    if dry_run:
        update_stmt = "-- Dry run; no manifest rows updated."
    else:
        update_stmt = f"""
        update weather.noaa_raw_backfill_manifest m
        set
            manifest_status = 'skipped',
            notes = concat_ws(
                '; ',
                nullif(m.notes, ''),
                'Skipped by active-window prune: station has no Jan-Feb or Dec observation overlap for source year.'
            )
        from weather.station st
        where st.station_id = m.station_id
          and m.calculation_run_id = {sql_literal(manifest_run_id)}
          and m.manifest_status = 'planned'
          and {condition};
        """
    return f"""
    begin;

    {update_stmt}

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
        {sql_literal(started)},
        now(),
        'succeeded',
        {sql_literal(json.dumps(params, sort_keys=True))}::jsonb,
        'Pruned planned NOAA backfill manifest rows outside station active DJF observation windows.'
    )
    on conflict (calculation_run_id) do update set
        run_finished_at_utc = excluded.run_finished_at_utc,
        run_status = excluded.run_status,
        parameters_json = excluded.parameters_json,
        notes = excluded.notes;

    commit;
    """


def render_report(
    report_path: Path,
    run_id: str,
    manifest_run_id: str,
    dry_run: bool,
    before_summary: dict[str, str],
    after_status: list[dict[str, str]],
    sample: list[dict[str, str]],
) -> None:
    lines = [
        "# NOAA Backfill Manifest Active-Window Prune Report",
        "",
        f"Generated UTC: {utc_now().isoformat(timespec='seconds')}",
        "",
        "## Run",
        "",
        f"- Calculation run ID: `{run_id}`",
        f"- Manifest run ID: `{manifest_run_id}`",
        f"- Dry run: `{dry_run}`",
        f"- Methodology version: `{METHODOLOGY_VERSION}`",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| Planned rows before prune | {before_summary['planned_rows']} |",
        f"| Rows with no station active DJF overlap | {before_summary['rows_to_skip']} |",
        f"| Distinct stations affected | {before_summary['stations_to_skip']} |",
        f"| Planned `999999-*` rows before prune | {before_summary['planned_999999_rows']} |",
        f"| `999999-*` rows skipped by active window | {before_summary['rows_999999_to_skip']} |",
        f"| Candidate plant links represented by skipped rows | {before_summary['affected_candidate_links']} |",
        "",
        "## Manifest Status After Prune",
        "",
        "| Status | Rows |",
        "| --- | ---: |",
    ]
    for row in after_status:
        lines.append(f"| `{row['manifest_status']}` | {row['rows']} |")
    lines.extend(
        [
            "",
            "## Sample Skipped Rows",
            "",
            "| Station | Year | Name | State | First Observation | Last Observation | Candidate Links | Batch | Rank |",
            "| --- | ---: | --- | --- | --- | --- | ---: | ---: | ---: |",
        ]
    )
    if sample:
        for row in sample:
            lines.append(
                "| "
                f"`{row['station_id']}` | "
                f"{row['source_year']} | "
                f"{row['station_name']} | "
                f"{row['state']} | "
                f"{row['first_observation_utc']} | "
                f"{row['last_observation_utc']} | "
                f"{row['station_candidate_plant_links']} | "
                f"{row['batch_number']} | "
                f"{row['priority_rank']} |"
            )
    else:
        lines.append("| No rows matched. |  |  |  |  |  |  |  |  |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- A row is skipped only when station metadata proves there is no overlap with January-February or December for that source year.",
            "- `999999-*` station IDs are not globally invalid. NOAA Global Hourly contains valid WBAN-only station files using the `999999` USAF placeholder.",
            "- This prune prevents known out-of-active-window station-years from consuming public AWS requests while preserving valid `999999-*` stations.",
        ]
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--psql", type=Path, default=PSQL)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5436)
    parser.add_argument("--dbname", default="eop012")
    parser.add_argument("--user")
    parser.add_argument("--manifest-run-id")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--sample-limit", type=int, default=25)
    args = parser.parse_args()

    manifest_run_id = args.manifest_run_id or latest_manifest_run_id(
        args.psql, args.host, args.port, args.dbname, args.user
    )
    run_id = f"noaa_manifest_active_window_prune_{utc_now().strftime('%Y%m%dT%H%M%SZ')}"
    code_commit = git_commit_label(args.project_root)
    before = summary_rows(args.psql, args.host, args.port, args.dbname, args.user, manifest_run_id)[0]
    sample = sample_rows(args.psql, args.host, args.port, args.dbname, args.user, manifest_run_id, args.sample_limit)
    params = {
        "manifest_run_id": manifest_run_id,
        "dry_run": args.dry_run,
        "sample_limit": args.sample_limit,
        "rows_to_skip": int(before["rows_to_skip"]),
        "prune_rule": "skip planned rows where station active window has no Jan-Feb or Dec overlap for source year",
    }
    run(
        psql_cmd(args.psql, args.host, args.port, args.dbname, args.user),
        input_text=update_sql(run_id, manifest_run_id, code_commit, args.dry_run, params),
    )
    after = status_rows(args.psql, args.host, args.port, args.dbname, args.user, manifest_run_id)
    report_path = args.project_root / "docs" / f"{run_id}_report.md"
    render_report(report_path, run_id, manifest_run_id, args.dry_run, before, after, sample)
    print(
        json.dumps(
            {
                "run_id": run_id,
                "manifest_run_id": manifest_run_id,
                "dry_run": args.dry_run,
                "rows_to_skip": int(before["rows_to_skip"]),
                "stations_to_skip": int(before["stations_to_skip"]),
                "rows_999999_to_skip": int(before["rows_999999_to_skip"]),
                "report_path": str(report_path),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
