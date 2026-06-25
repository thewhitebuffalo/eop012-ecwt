#!/usr/bin/env python3
"""Build NOAA loaded-weather QA reports for ECWT publication review."""

from __future__ import annotations

import argparse
import csv
import io
import json
import subprocess
from collections import Counter, OrderedDict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from eop012_config import PROJECT_ROOT, PSQL
from load_noaa_hourly_djf import DJF_MONTHS, SHEF_MIN_TEMP_C, open_text, parse_noaa_datetime, parse_tmp

METHODOLOGY_VERSION = "eop012-ecwt-method-v0.1.0"
DEFAULT_MIN_TEMP_C = -65.0
DEFAULT_MAX_TEMP_C = 40.0
DEFAULT_REJECT_SOURCE_CODES = {"7"}


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


def git_commit_label(project_root: Path) -> str:
    try:
        return run(["git", "-C", str(project_root), "rev-parse", "HEAD"]).stdout.strip()
    except Exception:
        return "UNCOMMITTED_WORKTREE"


def latest_run_id(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    pattern: str,
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
        where calculation_run_id like {sql_literal(pattern)}
          and run_status = 'succeeded'
        order by run_started_at_utc desc
        limit 1
        """,
    )
    if not run_id:
        raise RuntimeError(f"No succeeded run found for pattern {pattern}.")
    return run_id


def latest_strict_readiness_run_id(psql: Path, host: str, port: int, dbname: str, user: str | None) -> str:
    run_id = psql_scalar(
        psql,
        host,
        port,
        dbname,
        user,
        """
        select r.calculation_run_id
        from calc.plant_ecwt_readiness r
        join audit.calculation_run cr
          on cr.calculation_run_id = r.calculation_run_id
        where cr.run_status = 'succeeded'
          and r.min_coverage_ratio_threshold = 0.95
        group by r.calculation_run_id, cr.run_started_at_utc
        order by cr.run_started_at_utc desc
        limit 1
        """,
    )
    if not run_id:
        raise RuntimeError("No strict plant_ecwt_readiness run found.")
    return run_id


def load_file_reject_rows(psql: Path, host: str, port: int, dbname: str, user: str | None) -> list[dict[str, str]]:
    return psql_csv_query(
        psql,
        host,
        port,
        dbname,
        user,
        """
        select
            lf.station_id,
            lf.source_year::text as source_year,
            lf.calculation_run_id,
            lf.local_path,
            lf.source_file_id,
            lf.rejected_plausibility_rows::text as rejected_plausibility_rows,
            st.station_name,
            st.state,
            st.country
        from weather.noaa_hourly_load_file lf
        left join weather.station st using (station_id)
        where lf.rejected_plausibility_rows > 0
          and lf.file_status = 'loaded'
        order by lf.rejected_plausibility_rows desc, lf.station_id, lf.source_year
        """,
    )


def plausibility_reason(temp_c: float, report_type: str, min_temp_c: float, max_temp_c: float) -> str:
    if temp_c < min_temp_c:
        return "below_min_temp_c"
    if temp_c > max_temp_c:
        return "above_max_temp_c"
    if report_type == "SHEF" and temp_c < SHEF_MIN_TEMP_C:
        return "below_shef_min_temp_c"
    return "not_rejected"


def reconstruct_plausibility_rejects(
    load_files: list[dict[str, str]],
    min_temp_c: float,
    max_temp_c: float,
    reject_source_codes: set[str],
) -> list[dict[str, object]]:
    rejects: list[dict[str, object]] = []
    for file_row in load_files:
        path = Path(file_row["local_path"])
        with open_text(path) as f:
            reader = csv.DictReader(f)
            for row_number, raw in enumerate(reader, start=2):
                dt = parse_noaa_datetime(raw.get("DATE", ""))
                if dt is None or dt.month not in DJF_MONTHS:
                    continue
                source = (raw.get("SOURCE") or "").strip()
                if source in reject_source_codes:
                    continue
                temp_c, tmp_quality = parse_tmp(raw.get("TMP", ""))
                if temp_c is None:
                    continue
                report_type = (raw.get("REPORT_TYPE") or "").strip()
                reason = plausibility_reason(temp_c, report_type, min_temp_c, max_temp_c)
                if reason == "not_rejected":
                    continue
                rejects.append(
                    {
                        "station_id": file_row["station_id"],
                        "station_name": file_row.get("station_name"),
                        "state": file_row.get("state"),
                        "country": file_row.get("country"),
                        "source_year": file_row["source_year"],
                        "calculation_run_id": file_row["calculation_run_id"],
                        "source_file_id": file_row.get("source_file_id"),
                        "local_path": str(path),
                        "csv_row_number": row_number,
                        "observation_utc": dt.isoformat(timespec="seconds"),
                        "tmp_raw": raw.get("TMP", ""),
                        "tmp_quality": tmp_quality,
                        "dry_bulb_c": f"{temp_c:.3f}",
                        "dry_bulb_f": f"{(temp_c * 9.0 / 5.0) + 32.0:.3f}",
                        "report_type": report_type,
                        "source": source,
                        "quality_control": raw.get("QUALITY_CONTROL", ""),
                        "reason_code": reason,
                    }
                )
    return rejects


def warm_station_rows(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    station_ecwt_run_id: str,
    readiness_run_id: str,
    limit: int,
) -> list[dict[str, str]]:
    return psql_csv_query(
        psql,
        host,
        port,
        dbname,
        user,
        f"""
        with selected as (
            select
                r.selected_station_id as station_id,
                count(*) filter (where r.readiness_status = 'publication_candidate') as strict_publication_candidate_plants,
                count(*) as selected_plants
            from calc.plant_ecwt_readiness r
            where r.calculation_run_id = {sql_literal(readiness_run_id)}
              and r.selected_station_id is not null
            group by r.selected_station_id
        )
        select
            se.station_id,
            coalesce(st.station_name, '') as station_name,
            coalesce(st.state, '') as state,
            coalesce(st.country, '') as country,
            st.first_observation_utc::text as first_observation_utc,
            st.last_observation_utc::text as last_observation_utc,
            se.valid_hour_count::text as valid_hour_count,
            se.expected_hour_count::text as expected_hour_count,
            se.missing_hour_count::text as missing_hour_count,
            se.duplicate_hour_count::text as duplicate_hour_count,
            round(se.ecwt_f, 3)::text as ecwt_f,
            round(se.ecwt_discrete_f, 3)::text as ecwt_discrete_f,
            se.result_status,
            coalesce(selected.selected_plants, 0)::text as selected_plants,
            coalesce(selected.strict_publication_candidate_plants, 0)::text as strict_publication_candidate_plants
        from calc.station_ecwt se
        left join weather.station st using (station_id)
        left join selected using (station_id)
        where se.calculation_run_id = {sql_literal(station_ecwt_run_id)}
          and se.result_status = 'provisional'
        order by se.ecwt_f desc nulls last, se.valid_hour_count asc, se.station_id
        limit {int(limit)}
        """,
    )


def max_station_observation_rows(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    station_ecwt_run_id: str,
    limit: int,
) -> list[dict[str, str]]:
    return psql_csv_query(
        psql,
        host,
        port,
        dbname,
        user,
        f"""
        with max_station as (
            select station_id
            from calc.station_ecwt
            where calculation_run_id = {sql_literal(station_ecwt_run_id)}
              and result_status = 'provisional'
            order by ecwt_f desc nulls last, valid_hour_count asc, station_id
            limit 1
        )
        select
            h.station_id,
            h.hour_ending_utc::text as hour_ending_utc,
            round(h.dry_bulb_c, 3)::text as dry_bulb_c,
            round(h.dry_bulb_f, 3)::text as dry_bulb_f,
            array_to_string(h.quality_flags, '|') as quality_flags,
            h.source_file_id,
            h.calculation_run_id
        from weather.hourly_djf h
        join max_station using (station_id)
        order by h.dry_bulb_f asc, h.hour_ending_utc
        limit {int(limit)}
        """,
    )


def station_low_sample_count_summary(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    station_ecwt_run_id: str,
) -> dict[str, str]:
    rows = psql_csv_query(
        psql,
        host,
        port,
        dbname,
        user,
        f"""
        select
            count(*) filter (where result_status = 'provisional')::text as provisional_station_rows,
            count(*) filter (where result_status = 'provisional' and valid_hour_count < 24)::text as provisional_lt_24_hours,
            count(*) filter (where result_status = 'provisional' and valid_hour_count < 2000)::text as provisional_lt_2000_hours,
            count(*) filter (where result_status = 'provisional' and ecwt_f >= 60)::text as provisional_ecwt_ge_60f,
            count(*) filter (where result_status = 'provisional' and ecwt_f >= 80)::text as provisional_ecwt_ge_80f
        from calc.station_ecwt
        where calculation_run_id = {sql_literal(station_ecwt_run_id)}
        """,
    )
    return rows[0]


def canonical_weather_guardrails(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    min_temp_c: float,
    max_temp_c: float,
) -> dict[str, str]:
    rows = psql_csv_query(
        psql,
        host,
        port,
        dbname,
        user,
        f"""
        select
            count(*)::text as hourly_rows,
            count(*) filter (where dry_bulb_c < {float(min_temp_c)} or dry_bulb_c > {float(max_temp_c)})::text
                as outside_absolute_window,
            count(*) filter (where 'report_type:SHEF' = any(quality_flags))::text as shef_hourly_rows,
            count(*) filter (
                where 'report_type:SHEF' = any(quality_flags)
                  and dry_bulb_c < {float(SHEF_MIN_TEMP_C)}
            )::text as shef_below_floor_rows,
            round(min(dry_bulb_c), 3)::text as min_c,
            round(max(dry_bulb_c), 3)::text as max_c,
            round(min(dry_bulb_f), 3)::text as min_f,
            round(max(dry_bulb_f), 3)::text as max_f
        from weather.hourly_djf
        """,
    )
    return rows[0]


def loader_policy_summary(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
) -> dict[str, str]:
    rows = psql_csv_query(
        psql,
        host,
        port,
        dbname,
        user,
        """
        with lf as (
            select
                lf.*,
                cr.code_commit,
                cr.run_started_at_utc
            from weather.noaa_hourly_load_file lf
            join audit.calculation_run cr using (calculation_run_id)
            where lf.file_status = 'loaded'
        ),
        sf as (
            select
                lf.*,
                source_file.sha256
            from lf
            left join audit.source_file
              on source_file.source_file_id = lf.source_file_id
        )
        select
            count(*)::text as loaded_files,
            count(distinct code_commit)::text as distinct_loader_commits,
            count(*) filter (where coalesce(sha256, '') = '')::text as loaded_files_missing_source_sha256,
            coalesce(sum(rejected_plausibility_rows), 0)::text as historical_reject_rows,
            min(run_started_at_utc)::text as first_load_run_started_at_utc,
            max(run_started_at_utc)::text as last_load_run_started_at_utc
        from sf
        """,
    )
    return rows[0]


def reject_reconciliation_rows(
    load_files: list[dict[str, str]],
    rejects: list[dict[str, object]],
) -> list[dict[str, object]]:
    by_file = Counter(
        (
            str(row["station_id"]),
            str(row["source_year"]),
            str(row["local_path"]),
        )
        for row in rejects
    )
    rows: list[dict[str, object]] = []
    for file_row in load_files:
        key = (file_row["station_id"], file_row["source_year"], file_row["local_path"])
        db_rows = int(file_row["rejected_plausibility_rows"])
        reconstructed_rows = by_file[key]
        if db_rows == reconstructed_rows:
            continue
        rows.append(
            {
                "station_id": file_row["station_id"],
                "source_year": file_row["source_year"],
                "calculation_run_id": file_row["calculation_run_id"],
                "db_rows": db_rows,
                "reconstructed_rows": reconstructed_rows,
                "reconstructed_minus_db": reconstructed_rows - db_rows,
                "local_path": file_row["local_path"],
            }
        )
    rows.sort(key=lambda row: (str(row["station_id"]), str(row["source_year"]), str(row["local_path"])))
    return rows


def render_markdown_table(lines: list[str], headers: list[str], rows: list[dict[str, object]], fields: list[str]) -> None:
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join("---" for _ in headers) + " |")
    if not rows:
        lines.append("| " + " | ".join("" for _ in headers) + " |")
        return
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")) for field in fields) + " |")


def render_report(
    report_path: Path,
    run_id: str,
    code_commit: str,
    station_ecwt_run_id: str,
    readiness_run_id: str,
    load_files: list[dict[str, str]],
    rejects: list[dict[str, object]],
    rejects_csv_path: Path,
    warm_stations: list[dict[str, str]],
    max_station_observations: list[dict[str, str]],
    low_sample_summary: dict[str, str],
    canonical_guardrails: dict[str, str],
    policy_summary: dict[str, str],
    min_temp_c: float,
    max_temp_c: float,
    reject_source_codes: set[str],
) -> None:
    db_reject_total = sum(int(row["rejected_plausibility_rows"]) for row in load_files)
    by_reason = Counter(str(row["reason_code"]) for row in rejects)
    by_station = Counter(str(row["station_id"]) for row in rejects)
    by_run = Counter(str(row["calculation_run_id"]) for row in rejects)
    reconciliation_rows = reject_reconciliation_rows(load_files, rejects)
    reconstructed_minus_db = len(rejects) - db_reject_total

    top_station_rows = [
        {"station_id": station, "rows": count}
        for station, count in by_station.most_common(15)
    ]
    top_run_rows = [
        {"calculation_run_id": calc_run, "rows": count}
        for calc_run, count in by_run.most_common(10)
    ]
    reason_rows = [{"reason_code": reason, "rows": count} for reason, count in by_reason.most_common()]

    lines = [
        "# NOAA Loaded Weather QA Report",
        "",
        f"Generated UTC: {utc_now().isoformat(timespec='seconds')}",
        "",
        "## Run",
        "",
        f"- QA report ID: `{run_id}`",
        f"- Code commit: `{code_commit}`",
        f"- Station ECWT run ID: `{station_ecwt_run_id}`",
        f"- Strict readiness run ID: `{readiness_run_id}`",
        f"- Plausibility temperature window C: `{min_temp_c}` to `{max_temp_c}`",
        f"- Rejected NOAA SOURCE codes before plausibility reconstruction: `{sorted(reject_source_codes)}`",
        f"- Plausibility reject detail CSV: `{rejects_csv_path.name}`",
        "",
        "## Plausibility Rejects",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| Loaded files with plausibility rejects | {len(load_files)} |",
        f"| DB counted plausibility rejects | {db_reject_total} |",
        f"| Reconstructed plausibility reject rows | {len(rejects)} |",
        f"| Reconstructed minus DB count | {reconstructed_minus_db} |",
        f"| Files with count mismatches | {len(reconciliation_rows)} |",
        "",
    ]
    if reconciliation_rows:
        lines.append("### Count Mismatches")
        lines.append("")
        render_markdown_table(
            lines,
            ["Station", "Year", "Load Run", "DB Rows", "Reconstructed Rows", "Delta"],
            reconciliation_rows,
            [
                "station_id",
                "source_year",
                "calculation_run_id",
                "db_rows",
                "reconstructed_rows",
                "reconstructed_minus_db",
            ],
        )
        lines.append("")
    lines.append("### By Reason")
    lines.append("")
    render_markdown_table(lines, ["Reason", "Rows"], reason_rows, ["reason_code", "rows"])
    lines.extend(["", "### Top Stations By Rejected Rows", ""])
    render_markdown_table(lines, ["Station", "Rows"], top_station_rows, ["station_id", "rows"])
    lines.extend(["", "### Top Load Runs By Rejected Rows", ""])
    render_markdown_table(lines, ["Load Run", "Rows"], top_run_rows, ["calculation_run_id", "rows"])
    lines.extend(
        [
            "",
            "## Canonical Weather Guardrails",
            "",
            "| Metric | Count |",
            "| --- | ---: |",
            f"| Canonical DJF hourly rows | {canonical_guardrails['hourly_rows']} |",
            f"| Rows outside absolute C window | {canonical_guardrails['outside_absolute_window']} |",
            f"| SHEF canonical hourly rows | {canonical_guardrails['shef_hourly_rows']} |",
            f"| SHEF rows below SHEF floor | {canonical_guardrails['shef_below_floor_rows']} |",
            f"| Minimum dry bulb C | {canonical_guardrails['min_c']} |",
            f"| Maximum dry bulb C | {canonical_guardrails['max_c']} |",
            f"| Minimum dry bulb F | {canonical_guardrails['min_f']} |",
            f"| Maximum dry bulb F | {canonical_guardrails['max_f']} |",
            "",
            "## Loader Policy Audit",
            "",
            "| Metric | Count |",
            "| --- | ---: |",
            f"| Loaded file rows | {policy_summary['loaded_files']} |",
            f"| Distinct loader commits represented | {policy_summary['distinct_loader_commits']} |",
            f"| Loaded file rows missing source SHA-256 | {policy_summary['loaded_files_missing_source_sha256']} |",
            f"| Historical plausibility reject rows | {policy_summary['historical_reject_rows']} |",
            f"| First load run started UTC | {policy_summary['first_load_run_started_at_utc']} |",
            f"| Last load run started UTC | {policy_summary['last_load_run_started_at_utc']} |",
            "",
            "## Warm Station ECWT Outliers",
            "",
            "| Metric | Count |",
            "| --- | ---: |",
            f"| Provisional station ECWT rows | {low_sample_summary['provisional_station_rows']} |",
            f"| Provisional station rows with < 24 valid hours | {low_sample_summary['provisional_lt_24_hours']} |",
            f"| Provisional station rows with < 2,000 valid hours | {low_sample_summary['provisional_lt_2000_hours']} |",
            f"| Provisional station rows with ECWT >= 60 F | {low_sample_summary['provisional_ecwt_ge_60f']} |",
            f"| Provisional station rows with ECWT >= 80 F | {low_sample_summary['provisional_ecwt_ge_80f']} |",
            "",
            "### Warmest Station ECWT Rows",
            "",
        ]
    )
    render_markdown_table(
        lines,
        [
            "Station",
            "Name",
            "State",
            "Valid Hours",
            "Expected Hours",
            "ECWT F",
            "Selected Plants",
            "Strict Candidate Plants",
        ],
        warm_stations,
        [
            "station_id",
            "station_name",
            "state",
            "valid_hour_count",
            "expected_hour_count",
            "ecwt_f",
            "selected_plants",
            "strict_publication_candidate_plants",
        ],
    )
    lines.extend(["", "### Highest-ECWT Station Observation Sample", ""])
    render_markdown_table(
        lines,
        ["Station", "Hour UTC", "Dry Bulb F", "Dry Bulb C", "Quality Flags", "Source File"],
        max_station_observations,
        ["station_id", "hour_ending_utc", "dry_bulb_f", "dry_bulb_c", "quality_flags", "source_file_id"],
    )
    if reconciliation_rows:
        reconciliation_note = (
            "- Count mismatches mean the current parser policy does not reproduce historical per-file load statistics. "
            "In this rebuild, observed mismatches should be resolved through a targeted policy refresh or explicitly documented before publication."
        )
    else:
        reconciliation_note = "- Reconstructed plausibility rejects match the database load-file counters exactly for the checked files."
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Plausibility rejects are reconstructed from source CSV files because the canonical loader currently stores reject counts by file, not row-level reject details.",
            "- Reject reconstruction is scoped to files with historical reject counts; it is a reconciliation check, not a full raw-cache scan.",
            reconciliation_note,
            "- The canonical weather guardrails test the rows actually available to ECWT. Publication should block if canonical rows violate the absolute temperature window or if SHEF rows below the SHEF floor are present.",
            "- The warmest station ECWT row is driven by a station with one valid DJF hour. The strict plant readiness gate prevents such low-hour stations from becoming publication candidates, but station-level provisional outputs still need QA flags.",
            "- The presence of warm station ECWT outliers reinforces that publication should use `calc.plant_ecwt_readiness` strict candidates, not raw provisional station or plant ECWT rows.",
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
    parser.add_argument("--station-ecwt-run-id")
    parser.add_argument("--readiness-run-id")
    parser.add_argument("--min-temp-c", type=float, default=DEFAULT_MIN_TEMP_C)
    parser.add_argument("--max-temp-c", type=float, default=DEFAULT_MAX_TEMP_C)
    parser.add_argument("--warm-station-limit", type=int, default=20)
    parser.add_argument("--max-station-observation-limit", type=int, default=20)
    args = parser.parse_args()

    station_ecwt_run_id = args.station_ecwt_run_id or latest_run_id(
        args.psql, args.host, args.port, args.dbname, args.user, "station_ecwt_loaded_%"
    )
    readiness_run_id = args.readiness_run_id or latest_strict_readiness_run_id(
        args.psql, args.host, args.port, args.dbname, args.user
    )
    run_id = f"noaa_weather_qa_{utc_now().strftime('%Y%m%dT%H%M%SZ')}"
    code_commit = git_commit_label(args.project_root)
    load_files = load_file_reject_rows(args.psql, args.host, args.port, args.dbname, args.user)
    rejects = reconstruct_plausibility_rejects(
        load_files,
        args.min_temp_c,
        args.max_temp_c,
        DEFAULT_REJECT_SOURCE_CODES,
    )
    docs_dir = args.project_root / "docs"
    rejects_csv_path = docs_dir / f"{run_id}_plausibility_rejects.csv"
    reject_fields = [
        "station_id",
        "station_name",
        "state",
        "country",
        "source_year",
        "calculation_run_id",
        "source_file_id",
        "local_path",
        "csv_row_number",
        "observation_utc",
        "tmp_raw",
        "tmp_quality",
        "dry_bulb_c",
        "dry_bulb_f",
        "report_type",
        "source",
        "quality_control",
        "reason_code",
    ]
    write_csv(rejects_csv_path, reject_fields, rejects)
    warm_stations = warm_station_rows(
        args.psql,
        args.host,
        args.port,
        args.dbname,
        args.user,
        station_ecwt_run_id,
        readiness_run_id,
        args.warm_station_limit,
    )
    max_station_observations = max_station_observation_rows(
        args.psql,
        args.host,
        args.port,
        args.dbname,
        args.user,
        station_ecwt_run_id,
        args.max_station_observation_limit,
    )
    low_sample_summary = station_low_sample_count_summary(
        args.psql, args.host, args.port, args.dbname, args.user, station_ecwt_run_id
    )
    canonical_guardrails = canonical_weather_guardrails(
        args.psql, args.host, args.port, args.dbname, args.user, args.min_temp_c, args.max_temp_c
    )
    policy_summary = loader_policy_summary(args.psql, args.host, args.port, args.dbname, args.user)
    report_path = docs_dir / f"{run_id}_report.md"
    render_report(
        report_path,
        run_id,
        code_commit,
        station_ecwt_run_id,
        readiness_run_id,
        load_files,
        rejects,
        rejects_csv_path,
        warm_stations,
        max_station_observations,
        low_sample_summary,
        canonical_guardrails,
        policy_summary,
        args.min_temp_c,
        args.max_temp_c,
        DEFAULT_REJECT_SOURCE_CODES,
    )
    print(
        json.dumps(
            OrderedDict(
                [
                    ("run_id", run_id),
                    ("report_path", str(report_path)),
                    ("plausibility_reject_csv", str(rejects_csv_path)),
                    ("loaded_files_with_rejects", len(load_files)),
                    ("reconstructed_reject_rows", len(rejects)),
                    ("station_ecwt_run_id", station_ecwt_run_id),
                    ("readiness_run_id", readiness_run_id),
                ]
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
