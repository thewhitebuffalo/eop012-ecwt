#!/usr/bin/env python3
"""Classify provisional plant ECWT rows for publication readiness."""

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


def psql_scalar(psql: Path, host: str, port: int, dbname: str, query: str, user: str | None = None) -> str:
    result = run(psql_cmd(psql, host, port, dbname, user) + ["-At", "-c", query])
    return result.stdout.strip()


def psql_csv_query(psql: Path, host: str, port: int, dbname: str, query: str, user: str | None = None) -> list[dict[str, str]]:
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


def latest_plant_ecwt_run_id(psql: Path, host: str, port: int, dbname: str, user: str | None) -> str:
    run_id = psql_scalar(
        psql,
        host,
        port,
        dbname,
        """
        select calculation_run_id
        from audit.calculation_run
        where calculation_run_id like 'plant_ecwt_provisional_%'
          and run_status = 'succeeded'
        order by run_started_at_utc desc
        limit 1
        """,
        user,
    )
    if not run_id:
        raise RuntimeError("No succeeded plant_ecwt_provisional run found.")
    return run_id


def build_sql(
    run_id: str,
    plant_ecwt_run_id: str,
    code_commit: str,
    min_valid_hours: int,
    min_coverage_ratio: float,
) -> str:
    start = utc_now().isoformat(timespec="seconds")
    params = {
        "plant_ecwt_run_id": plant_ecwt_run_id,
        "min_valid_hours": min_valid_hours,
        "min_coverage_ratio": min_coverage_ratio,
        "readiness_rule": "publication_candidate requires provisional plant ECWT, valid hours >= threshold, and coverage ratio >= threshold",
    }
    return f"""
\\set ON_ERROR_STOP on
begin;

-- Serialize readiness writers. Parallel strict/diagnostic runs can otherwise
-- deadlock while writing shared audit and readiness indexes.
select pg_advisory_xact_lock(12012, 9510);

create table if not exists calc.plant_ecwt_readiness (
    plant_ecwt_readiness_id text primary key,
    plant_ecwt_id text not null references calc.plant_ecwt(plant_ecwt_id),
    plant_id text not null references asset.plant(plant_id),
    calculation_run_id text not null references audit.calculation_run(calculation_run_id),
    methodology_version text not null references audit.methodology_version(methodology_version),
    selected_station_id text references weather.station(station_id),
    valid_hour_count bigint not null,
    expected_hour_count bigint not null,
    coverage_ratio numeric,
    min_valid_hour_threshold bigint not null,
    min_coverage_ratio_threshold numeric not null,
    readiness_status text not null,
    reason_code text not null,
    notes text,
    created_at_utc timestamptz not null default now(),
    constraint plant_ecwt_readiness_status_check
        check (readiness_status in ('publication_candidate', 'provisional_low_coverage', 'blocked'))
);
create index if not exists ix_plant_ecwt_readiness_run_status
    on calc.plant_ecwt_readiness (calculation_run_id, readiness_status);

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
    'Classified provisional plant ECWT rows for publication readiness.'
)
on conflict (calculation_run_id) do update set
    run_finished_at_utc = excluded.run_finished_at_utc,
    run_status = excluded.run_status,
    parameters_json = excluded.parameters_json,
    notes = excluded.notes;

insert into calc.plant_ecwt_readiness (
    plant_ecwt_readiness_id,
    plant_ecwt_id,
    plant_id,
    calculation_run_id,
    methodology_version,
    selected_station_id,
    valid_hour_count,
    expected_hour_count,
    coverage_ratio,
    min_valid_hour_threshold,
    min_coverage_ratio_threshold,
    readiness_status,
    reason_code,
    notes
)
select
    {sql_literal(run_id)} || ':plant:' || pe.plant_id as plant_ecwt_readiness_id,
    pe.plant_ecwt_id,
    pe.plant_id,
    {sql_literal(run_id)} as calculation_run_id,
    {sql_literal(METHODOLOGY_VERSION)} as methodology_version,
    seg.station_id as selected_station_id,
    pe.valid_hour_count,
    pe.expected_hour_count,
    (pe.valid_hour_count::numeric / nullif(pe.expected_hour_count, 0)) as coverage_ratio,
    {min_valid_hours}::bigint as min_valid_hour_threshold,
    {min_coverage_ratio}::numeric as min_coverage_ratio_threshold,
    case
        when pe.result_status = 'blocked' then 'blocked'
        when pe.valid_hour_count >= {min_valid_hours}
         and (pe.valid_hour_count::numeric / nullif(pe.expected_hour_count, 0)) >= {min_coverage_ratio}
            then 'publication_candidate'
        else 'provisional_low_coverage'
    end as readiness_status,
    case
        when pe.result_status = 'blocked' then 'no_candidate_station_with_provisional_ecwt'
        when pe.valid_hour_count < {min_valid_hours} then 'valid_hours_below_threshold'
        when (pe.valid_hour_count::numeric / nullif(pe.expected_hour_count, 0)) < {min_coverage_ratio} then 'coverage_ratio_below_threshold'
        else 'passes_current_publication_gate'
    end as reason_code,
    'Readiness classification for provisional plant ECWT. Thresholds are conservative working gates and may change before publication.' as notes
from calc.plant_ecwt pe
left join link.station_selection_segment seg
  on seg.station_selection_id = pe.station_selection_id
where pe.calculation_run_id = {sql_literal(plant_ecwt_run_id)}
on conflict (plant_ecwt_readiness_id) do update set
    selected_station_id = excluded.selected_station_id,
    valid_hour_count = excluded.valid_hour_count,
    expected_hour_count = excluded.expected_hour_count,
    coverage_ratio = excluded.coverage_ratio,
    min_valid_hour_threshold = excluded.min_valid_hour_threshold,
    min_coverage_ratio_threshold = excluded.min_coverage_ratio_threshold,
    readiness_status = excluded.readiness_status,
    reason_code = excluded.reason_code,
    notes = excluded.notes;

commit;
"""


def report_counts(psql: Path, host: str, port: int, dbname: str, run_id: str, user: str | None) -> OrderedDict[str, str]:
    queries = OrderedDict(
        [
            ("readiness rows", f"select count(*) from calc.plant_ecwt_readiness where calculation_run_id = {sql_literal(run_id)};"),
            ("publication candidates", f"select count(*) from calc.plant_ecwt_readiness where calculation_run_id = {sql_literal(run_id)} and readiness_status = 'publication_candidate';"),
            ("provisional low coverage", f"select count(*) from calc.plant_ecwt_readiness where calculation_run_id = {sql_literal(run_id)} and readiness_status = 'provisional_low_coverage';"),
            ("blocked", f"select count(*) from calc.plant_ecwt_readiness where calculation_run_id = {sql_literal(run_id)} and readiness_status = 'blocked';"),
            ("minimum coverage ratio", f"select coalesce(round(min(coverage_ratio), 4)::text, '') from calc.plant_ecwt_readiness where calculation_run_id = {sql_literal(run_id)} and coverage_ratio is not null;"),
            ("median coverage ratio", f"select coalesce(round(percentile_cont(0.5) within group (order by coverage_ratio)::numeric, 4)::text, '') from calc.plant_ecwt_readiness where calculation_run_id = {sql_literal(run_id)} and coverage_ratio is not null;"),
        ]
    )
    rows = OrderedDict()
    for label, query in queries.items():
        rows[label] = psql_scalar(psql, host, port, dbname, query, user)
    return rows


def render_report(
    path: Path,
    run_id: str,
    plant_ecwt_run_id: str,
    code_commit: str,
    min_valid_hours: int,
    min_coverage_ratio: float,
    db_counts: OrderedDict[str, str],
    by_reason: list[dict[str, str]],
    host: str,
    port: int,
    dbname: str,
) -> None:
    lines = [
        "# Plant ECWT Readiness Report",
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
        f"- Plant ECWT run ID: `{plant_ecwt_run_id}`",
        f"- Methodology version: `{METHODOLOGY_VERSION}`",
        f"- Code commit: `{code_commit}`",
        f"- Minimum valid hours: `{min_valid_hours}`",
        f"- Minimum coverage ratio: `{min_coverage_ratio}`",
        "",
        "## Summary",
        "",
        "| Relation or Check | Rows / Value |",
        "| --- | ---: |",
    ]
    for label, count in db_counts.items():
        lines.append(f"| `{label}` | {count} |")
    lines.extend(["", "## By Reason", "", "| Readiness | Reason | Rows |", "| --- | --- | ---: |"])
    for row in by_reason:
        lines.append(f"| `{row['readiness_status']}` | `{row['reason_code']}` | {row['rows']} |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- This is a working publication-readiness gate for provisional plant ECWT rows.",
            "- `publication_candidate` is not the same as final accepted compliance output; it means the row passes the current coverage thresholds.",
            "- Rows that fail this gate should stay out of a published compliance dataset until more weather coverage or manual review is available.",
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
    parser.add_argument("--plant-ecwt-run-id", default=None)
    parser.add_argument("--min-valid-hours", type=int, default=2000)
    parser.add_argument("--min-coverage-ratio", type=float, default=0.95)
    args = parser.parse_args()

    plant_ecwt_run_id = args.plant_ecwt_run_id or latest_plant_ecwt_run_id(
        args.psql, args.host, args.port, args.dbname, args.user
    )
    code_commit = git_commit_label(args.project_root)
    run_id = f"plant_ecwt_readiness_{utc_now().strftime('%Y%m%dT%H%M%SZ')}"
    run(
        psql_cmd(args.psql, args.host, args.port, args.dbname, args.user),
        input_text=build_sql(run_id, plant_ecwt_run_id, code_commit, args.min_valid_hours, args.min_coverage_ratio),
    )

    db_counts = report_counts(args.psql, args.host, args.port, args.dbname, run_id, args.user)
    by_reason = psql_csv_query(
        args.psql,
        args.host,
        args.port,
        args.dbname,
        f"""
        select readiness_status, reason_code, count(*) as rows
        from calc.plant_ecwt_readiness
        where calculation_run_id = {sql_literal(run_id)}
        group by readiness_status, reason_code
        order by readiness_status, reason_code
        """,
        args.user,
    )
    report_path = args.project_root / "docs" / f"{run_id}_report.md"
    render_report(
        report_path,
        run_id,
        plant_ecwt_run_id,
        code_commit,
        args.min_valid_hours,
        args.min_coverage_ratio,
        db_counts,
        by_reason,
        args.host,
        args.port,
        args.dbname,
    )
    print(json.dumps({"run_id": run_id, "report_path": str(report_path), "db_counts": db_counts}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
