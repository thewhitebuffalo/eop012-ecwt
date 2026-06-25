#!/usr/bin/env python3
"""Build read-only QA outputs for provisional plant-to-station selections."""

from __future__ import annotations

import argparse
import csv
import io
import json
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from eop012_config import PROJECT_ROOT, PSQL


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def sql_literal(value: object) -> str:
    if value is None:
        return "null"
    text = str(value)
    return "'" + text.replace("'", "''") + "'"


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        cmd,
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


def latest_strict_readiness_run_id(psql: Path, host: str, port: int, dbname: str, user: str | None) -> str:
    run_id = psql_scalar(
        psql,
        host,
        port,
        dbname,
        """
        select calculation_run_id
        from audit.calculation_run
        where calculation_run_id like 'plant_ecwt_readiness_%'
          and run_status = 'succeeded'
          and coalesce((parameters_json->>'min_coverage_ratio')::numeric, 0) >= 0.95
        order by run_started_at_utc desc
        limit 1
        """,
        user,
    )
    if not run_id:
        raise RuntimeError("No succeeded strict plant_ecwt_readiness run found.")
    return run_id


def fetch_run_params(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    run_id: str,
    user: str | None,
) -> dict[str, object]:
    params_text = psql_scalar(
        psql,
        host,
        port,
        dbname,
        f"""
        select coalesce(parameters_json::text, '{{}}')
        from audit.calculation_run
        where calculation_run_id = {sql_literal(run_id)}
        """,
        user,
    )
    if not params_text:
        raise RuntimeError(f"Calculation run not found: {run_id}")
    return json.loads(params_text)


def build_candidate_sql(readiness_run_id: str) -> str:
    return f"""
with readiness_run as (
    select
        calculation_run_id as readiness_run_id,
        parameters_json->>'plant_ecwt_run_id' as plant_ecwt_run_id,
        parameters_json->>'min_valid_hours' as readiness_min_valid_hours,
        parameters_json->>'min_coverage_ratio' as readiness_min_coverage_ratio,
        parameters_json->>'coverage_denominator' as readiness_coverage_denominator,
        parameters_json->>'coverage_min_year' as readiness_coverage_min_year,
        parameters_json->>'coverage_max_year' as readiness_coverage_max_year
    from audit.calculation_run
    where calculation_run_id = {sql_literal(readiness_run_id)}
),
plant_run as (
    select
        cr.calculation_run_id as plant_ecwt_run_id,
        cr.parameters_json->>'candidate_run_id' as candidate_run_id,
        cr.parameters_json->>'station_ecwt_run_id' as station_ecwt_run_id
    from audit.calculation_run cr
    join readiness_run rr on rr.plant_ecwt_run_id = cr.calculation_run_id
)
select
    rr.readiness_run_id,
    rr.plant_ecwt_run_id,
    pr.candidate_run_id,
    pr.station_ecwt_run_id,
    rr.readiness_min_valid_hours,
    rr.readiness_min_coverage_ratio,
    rr.readiness_coverage_denominator,
    rr.readiness_coverage_min_year,
    rr.readiness_coverage_max_year,
    r.plant_ecwt_readiness_id,
    r.plant_ecwt_id,
    r.plant_id,
    r.readiness_status,
    r.reason_code as readiness_reason_code,
    r.valid_hour_count as readiness_valid_hour_count,
    r.expected_hour_count as readiness_expected_hour_count,
    r.coverage_ratio as readiness_coverage_ratio,
    r.min_valid_hour_threshold,
    r.min_coverage_ratio_threshold,
    r.selected_station_id,
    pe.station_selection_id,
    pe.valid_hour_count as plant_ecwt_valid_hour_count,
    pe.expected_hour_count as plant_ecwt_expected_hour_count,
    pe.missing_hour_count as plant_ecwt_missing_hour_count,
    pe.duplicate_hour_count as plant_ecwt_duplicate_hour_count,
    pe.percentile_target,
    pe.ecwt_c,
    pe.ecwt_f,
    pe.discrete_rank,
    pe.ecwt_discrete_c,
    pe.ecwt_discrete_f,
    pe.governing_ecwt_f,
    pe.result_status as plant_ecwt_result_status,
    p.eia_plant_code,
    p.plant_name,
    p.utility_id,
    p.utility_name,
    p.city as plant_city,
    p.state as plant_state,
    p.county as plant_county,
    p.latitude as plant_latitude,
    p.longitude as plant_longitude,
    p.nerc_region,
    p.balancing_authority_code,
    p.balancing_authority_name,
    p.sector_name,
    seg.station_id as segment_station_id,
    seg.segment_start_utc,
    seg.segment_end_utc,
    seg.reason_code as segment_reason_code,
    sc.distance_km as selected_distance_km,
    sc.elevation_delta_m as selected_elevation_delta_m,
    sc.valid_djf_hours as selected_candidate_valid_djf_hours,
    sc.expected_djf_hours as selected_candidate_expected_djf_hours,
    sc.coverage_ratio as selected_candidate_coverage_ratio,
    sc.rank_order as selected_rank_order,
    sc.candidate_status as selected_candidate_status,
    sc.reason_code as selected_candidate_reason_code,
    st.station_name as selected_station_name,
    st.latitude as selected_station_latitude,
    st.longitude as selected_station_longitude,
    st.elevation_m as selected_station_elevation_m,
    st.state as selected_station_state,
    st.country as selected_station_country,
    st.first_observation_utc as selected_station_first_observation_utc,
    st.last_observation_utc as selected_station_last_observation_utc
from readiness_run rr
join plant_run pr on true
join calc.plant_ecwt_readiness r
  on r.calculation_run_id = rr.readiness_run_id
 and r.readiness_status = 'publication_candidate'
join calc.plant_ecwt pe
  on pe.plant_ecwt_id = r.plant_ecwt_id
join asset.plant p
  on p.plant_id = r.plant_id
left join link.station_selection_segment seg
  on seg.station_selection_id = pe.station_selection_id
left join link.station_candidate sc
  on sc.calculation_run_id = pr.candidate_run_id
 and sc.plant_id = r.plant_id
 and sc.station_id = r.selected_station_id
left join weather.station st
  on st.station_id = r.selected_station_id
order by p.state nulls last, p.eia_plant_code, p.plant_name
"""


def to_float(value: str | None) -> float | None:
    if value is None or value == "":
        return None
    return float(value)


def to_int(value: str | None) -> int | None:
    if value is None or value == "":
        return None
    return int(float(value))


def timestamp_year(value: str | None) -> int | None:
    if value is None or len(value) < 4:
        return None
    try:
        return int(value[:4])
    except ValueError:
        return None


def format_number(value: str | int | float | None, digits: int = 3) -> str:
    if value is None or value == "":
        return ""
    if isinstance(value, str):
        try:
            number = float(value)
        except ValueError:
            return value
    else:
        number = float(value)
    if number.is_integer():
        return f"{int(number):,}"
    return f"{number:,.{digits}f}"


def format_ratio(value: str | int | float | None) -> str:
    if value is None or value == "":
        return ""
    return f"{float(value):.4f}"


def format_temp(value: str | int | float | None) -> str:
    if value is None or value == "":
        return ""
    return f"{float(value):.1f}"


def compute_risk_flags(row: dict[str, str], thresholds: argparse.Namespace) -> list[str]:
    flags: list[str] = []

    selected_station_id = row.get("selected_station_id", "")
    segment_station_id = row.get("segment_station_id", "")
    if not selected_station_id:
        flags.append("missing_selected_station")
    if not segment_station_id:
        flags.append("missing_selection_segment")
    if selected_station_id and segment_station_id and selected_station_id != segment_station_id:
        flags.append("selection_segment_station_mismatch")

    if not row.get("selected_candidate_status"):
        flags.append("missing_selected_candidate_link")

    distance = to_float(row.get("selected_distance_km"))
    if distance is not None:
        if distance > thresholds.high_distance_km:
            flags.append(f"distance_gt_{int(thresholds.high_distance_km)}km")
        elif distance > thresholds.distance_review_km:
            flags.append(f"distance_gt_{int(thresholds.distance_review_km)}km")

    rank_order = to_int(row.get("selected_rank_order"))
    if rank_order is not None:
        if rank_order > 3:
            flags.append("selected_rank_gt_3")
        elif rank_order > 1:
            flags.append("selected_rank_gt_1")

    station_country = (row.get("selected_station_country") or "").upper()
    if not station_country:
        flags.append("station_country_missing")
    elif station_country != "US":
        flags.append("station_country_not_us")

    plant_state = (row.get("plant_state") or "").upper()
    station_state = (row.get("selected_station_state") or "").upper()
    if not station_state:
        flags.append("station_state_missing")
    elif plant_state and station_state != plant_state and station_country == "US":
        flags.append("plant_station_state_mismatch")

    coverage = to_float(row.get("readiness_coverage_ratio"))
    if coverage is not None and coverage < thresholds.near_threshold_coverage:
        label = str(thresholds.near_threshold_coverage).replace(".", "_")
        flags.append(f"coverage_below_{label}")

    last_year = timestamp_year(row.get("selected_station_last_observation_utc"))
    if last_year is not None and last_year < thresholds.old_station_last_year:
        flags.append(f"station_last_observation_before_{thresholds.old_station_last_year}")

    ecwt_f = to_float(row.get("governing_ecwt_f"))
    if ecwt_f is not None:
        if ecwt_f > thresholds.warm_ecwt_f:
            flags.append(f"warm_ecwt_gt_{int(thresholds.warm_ecwt_f)}f")
        if plant_state != "HI" and ecwt_f > thresholds.warm_mainland_ecwt_f:
            flags.append(f"warm_mainland_ecwt_gt_{int(thresholds.warm_mainland_ecwt_f)}f")

    shared_count = to_int(row.get("selected_station_strict_candidate_count"))
    if shared_count is not None:
        if shared_count > thresholds.high_shared_station_count:
            flags.append(f"shared_station_gt_{thresholds.high_shared_station_count}_plants")
        elif shared_count > thresholds.shared_station_review_count:
            flags.append(f"shared_station_gt_{thresholds.shared_station_review_count}_plants")

    return flags


def add_qa_flags(rows: list[dict[str, str]], thresholds: argparse.Namespace) -> None:
    station_counts = Counter(row.get("selected_station_id", "") for row in rows if row.get("selected_station_id"))
    for row in rows:
        shared_count = station_counts.get(row.get("selected_station_id", ""), 0)
        row["selected_station_strict_candidate_count"] = str(shared_count)
        flags = compute_risk_flags(row, thresholds)
        row["risk_flags"] = ";".join(flags)
        row["risk_flag_count"] = str(len(flags))


def sort_numeric(rows: list[dict[str, str]], key: str, reverse: bool = True) -> list[dict[str, str]]:
    return sorted(
        rows,
        key=lambda row: to_float(row.get(key)) if to_float(row.get(key)) is not None else float("-inf"),
        reverse=reverse,
    )


def md_table(rows: list[dict[str, str]], columns: list[tuple[str, str]], limit: int = 15) -> list[str]:
    if not rows:
        return ["_None._"]
    limited = rows[:limit]
    lines = [
        "| " + " | ".join(header for header, _ in columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in limited:
        cells = []
        for _, key in columns:
            value = row.get(key, "")
            cells.append(str(value).replace("\n", " ").replace("|", "\\|"))
        lines.append("| " + " | ".join(cells) + " |")
    if len(rows) > limit:
        omitted_cells = ["..."] + [f"{len(rows) - limit} more rows omitted"] + [""] * max(0, len(columns) - 2)
        lines.append("| " + " | ".join(omitted_cells) + " |")
    return lines


def compact_row(row: dict[str, str]) -> dict[str, str]:
    return {
        "Plant": f"{row.get('eia_plant_code', '')} {row.get('plant_name', '')}".strip(),
        "Plant State": row.get("plant_state", ""),
        "Station": f"{row.get('selected_station_id', '')} {row.get('selected_station_name', '')}".strip(),
        "Station State": row.get("selected_station_state", ""),
        "Country": row.get("selected_station_country", ""),
        "Distance km": format_number(row.get("selected_distance_km"), 1),
        "Rank": row.get("selected_rank_order", ""),
        "Coverage": format_ratio(row.get("readiness_coverage_ratio")),
        "ECWT F": format_temp(row.get("governing_ecwt_f")),
        "Shared Plants": row.get("selected_station_strict_candidate_count", ""),
        "Last Obs": (row.get("selected_station_last_observation_utc") or "")[:10],
        "Flags": row.get("risk_flags", ""),
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "qa_run_id",
        "readiness_run_id",
        "plant_ecwt_run_id",
        "candidate_run_id",
        "station_ecwt_run_id",
        "plant_ecwt_readiness_id",
        "plant_ecwt_id",
        "plant_id",
        "eia_plant_code",
        "plant_name",
        "utility_id",
        "utility_name",
        "plant_city",
        "plant_state",
        "plant_county",
        "plant_latitude",
        "plant_longitude",
        "nerc_region",
        "balancing_authority_code",
        "balancing_authority_name",
        "sector_name",
        "readiness_status",
        "readiness_reason_code",
        "readiness_valid_hour_count",
        "readiness_expected_hour_count",
        "readiness_coverage_ratio",
        "min_valid_hour_threshold",
        "min_coverage_ratio_threshold",
        "station_selection_id",
        "selected_station_id",
        "selected_station_name",
        "selected_station_state",
        "selected_station_country",
        "selected_station_latitude",
        "selected_station_longitude",
        "selected_station_elevation_m",
        "selected_station_first_observation_utc",
        "selected_station_last_observation_utc",
        "selected_distance_km",
        "selected_elevation_delta_m",
        "selected_rank_order",
        "selected_candidate_status",
        "selected_candidate_reason_code",
        "selected_candidate_valid_djf_hours",
        "selected_candidate_expected_djf_hours",
        "selected_candidate_coverage_ratio",
        "selected_station_strict_candidate_count",
        "segment_station_id",
        "segment_start_utc",
        "segment_end_utc",
        "segment_reason_code",
        "plant_ecwt_valid_hour_count",
        "plant_ecwt_expected_hour_count",
        "plant_ecwt_missing_hour_count",
        "plant_ecwt_duplicate_hour_count",
        "percentile_target",
        "ecwt_c",
        "ecwt_f",
        "discrete_rank",
        "ecwt_discrete_c",
        "ecwt_discrete_f",
        "governing_ecwt_f",
        "plant_ecwt_result_status",
        "risk_flags",
        "risk_flag_count",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def render_report(
    path: Path,
    csv_path: Path,
    qa_run_id: str,
    generated_at: str,
    code_commit: str,
    readiness_run_id: str,
    params: dict[str, object],
    rows: list[dict[str, str]],
    thresholds: argparse.Namespace,
) -> None:
    total = len(rows)
    flagged_rows = [row for row in rows if to_int(row.get("risk_flag_count")) and to_int(row.get("risk_flag_count")) > 0]
    flag_counts = Counter()
    for row in flagged_rows:
        for flag in row["risk_flags"].split(";"):
            if flag:
                flag_counts[flag] += 1

    distinct_stations = len({row["selected_station_id"] for row in rows if row.get("selected_station_id")})
    max_distance = max((to_float(row.get("selected_distance_km")) or 0.0 for row in rows), default=0.0)
    max_shared = max((to_int(row.get("selected_station_strict_candidate_count")) or 0 for row in rows), default=0)
    rank_outliers = [row for row in rows if (to_int(row.get("selected_rank_order")) or 0) > 1]
    non_us = [row for row in rows if (row.get("selected_station_country") or "").upper() not in ("", "US")]
    state_mismatch = [
        row
        for row in rows
        if row.get("plant_state")
        and row.get("selected_station_state")
        and (row.get("selected_station_country") or "").upper() == "US"
        and row["plant_state"] != row["selected_station_state"]
    ]
    old_station = [
        row
        for row in rows
        if (timestamp_year(row.get("selected_station_last_observation_utc")) or 9999) < thresholds.old_station_last_year
    ]
    warm_mainland = [
        row
        for row in rows
        if (row.get("plant_state") or "").upper() != "HI"
        and (to_float(row.get("governing_ecwt_f")) or -9999.0) > thresholds.warm_mainland_ecwt_f
    ]
    near_threshold = [
        row for row in rows if (to_float(row.get("readiness_coverage_ratio")) or 9999.0) < thresholds.near_threshold_coverage
    ]

    by_station: dict[str, dict[str, str]] = {}
    for row in rows:
        station_id = row.get("selected_station_id", "")
        if not station_id:
            continue
        if station_id not in by_station:
            by_station[station_id] = {
                "Station": f"{station_id} {row.get('selected_station_name', '')}".strip(),
                "State": row.get("selected_station_state", ""),
                "Country": row.get("selected_station_country", ""),
                "Strict Candidate Plants": row.get("selected_station_strict_candidate_count", ""),
                "Min Coverage": format_ratio(row.get("readiness_coverage_ratio")),
                "Max Distance km": format_number(row.get("selected_distance_km"), 1),
                "ECWT F": format_temp(row.get("governing_ecwt_f")),
            }
        else:
            current = by_station[station_id]
            current_min_cov = to_float(current["Min Coverage"]) or 9999.0
            current_max_dist = to_float(current["Max Distance km"].replace(",", "")) or 0.0
            row_cov = to_float(row.get("readiness_coverage_ratio")) or 9999.0
            row_dist = to_float(row.get("selected_distance_km")) or 0.0
            if row_cov < current_min_cov:
                current["Min Coverage"] = format_ratio(row.get("readiness_coverage_ratio"))
            if row_dist > current_max_dist:
                current["Max Distance km"] = format_number(row.get("selected_distance_km"), 1)

    station_rows = sorted(
        by_station.values(),
        key=lambda row: (to_int(row.get("Strict Candidate Plants")) or 0, to_float(row.get("Max Distance km").replace(",", "")) or 0),
        reverse=True,
    )

    flag_rows = [
        {"Flag": flag, "Rows": f"{count:,}", "Share": f"{(count / total * 100):.1f}%"}
        for flag, count in flag_counts.most_common()
    ]

    detail_cols = [
        ("Plant", "Plant"),
        ("Plant State", "Plant State"),
        ("Station", "Station"),
        ("Station State", "Station State"),
        ("Country", "Country"),
        ("Distance km", "Distance km"),
        ("Rank", "Rank"),
        ("Coverage", "Coverage"),
        ("ECWT F", "ECWT F"),
        ("Flags", "Flags"),
    ]

    lines = [
        "# Station Selection QA for Strict Plant ECWT Candidates",
        "",
        "## Technical Summary",
        "",
        (
            f"This read-only QA pass reviewed `{total:,}` strict plant ECWT publication candidates "
            f"from readiness run `{readiness_run_id}`. The script found `{flagged_rows and len(flagged_rows) or 0:,}` "
            "rows with at least one review flag. Flags are not rejection decisions; they identify selected "
            "plant-to-station assignments that should be reviewed before any compliance-facing release."
        ),
        "",
        (
            f"The strict candidates use `{distinct_stations:,}` distinct selected NOAA stations. "
            f"The maximum selected station distance is `{max_distance:.1f}` km, and the largest single-station "
            f"concentration is `{max_shared:,}` strict candidate plants."
        ),
        "",
        "## Scope and Source Runs",
        "",
        f"- QA run: `{qa_run_id}`",
        f"- Generated at UTC: `{generated_at}`",
        f"- Code commit: `{code_commit}`",
        f"- Readiness run: `{readiness_run_id}`",
        f"- Plant ECWT run: `{params.get('plant_ecwt_run_id', '')}`",
        f"- Strict readiness threshold: `{params.get('min_valid_hours', '')}` valid hours and coverage ratio >= `{params.get('min_coverage_ratio', '')}`",
        f"- Coverage denominator: `{params.get('coverage_denominator', '')}`",
        f"- Detailed CSV: `{csv_path.name}`",
        "",
        "## QA Flag Definitions",
        "",
        f"- Distance review: selected station is more than `{thresholds.distance_review_km:g}` km from the plant.",
        f"- High distance review: selected station is more than `{thresholds.high_distance_km:g}` km from the plant.",
        "- Rank review: selected station was not the rank-1 candidate, or was worse than rank 3.",
        "- Cross-border/state review: selected station country is not US, station country/state is missing, or US station state differs from plant state.",
        f"- Coverage review: strict candidate coverage is below `{thresholds.near_threshold_coverage:g}` even though it passes the publication gate.",
        f"- Old station review: selected station metadata ends before `{thresholds.old_station_last_year}`.",
        f"- Warm ECWT review: governing ECWT is above `{thresholds.warm_ecwt_f:g}` F, or mainland governing ECWT is above `{thresholds.warm_mainland_ecwt_f:g}` F.",
        f"- Shared station review: one selected station governs more than `{thresholds.shared_station_review_count}` strict candidate plants.",
        "",
        "## Aggregate Counts",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| Strict publication candidates reviewed | {total:,} |",
        f"| Distinct selected stations | {distinct_stations:,} |",
        f"| Rows with at least one QA flag | {len(flagged_rows):,} |",
        f"| Selected station assignments with rank > 1 | {len(rank_outliers):,} |",
        f"| Non-US selected stations | {len(non_us):,} |",
        f"| US plant/station state mismatches | {len(state_mismatch):,} |",
        f"| Selected stations with last observation before {thresholds.old_station_last_year} | {len(old_station):,} |",
        f"| Mainland warm ECWT rows > {thresholds.warm_mainland_ecwt_f:g} F | {len(warm_mainland):,} |",
        f"| Near-threshold coverage rows below {thresholds.near_threshold_coverage:g} | {len(near_threshold):,} |",
        "",
        "## Risk Flag Counts",
        "",
    ]

    lines.extend(md_table(flag_rows, [("Flag", "Flag"), ("Rows", "Rows"), ("Share", "Share")], limit=30))

    lines.extend(
        [
            "",
            "## Top Selected Stations by Plant Count",
            "",
        ]
    )
    lines.extend(
        md_table(
            station_rows,
            [
                ("Station", "Station"),
                ("State", "State"),
                ("Country", "Country"),
                ("Strict Candidate Plants", "Strict Candidate Plants"),
                ("Max Distance km", "Max Distance km"),
                ("Min Coverage", "Min Coverage"),
                ("ECWT F", "ECWT F"),
            ],
            limit=20,
        )
    )

    lines.extend(["", "## Farthest Selected Station Assignments", ""])
    farthest = [compact_row(row) for row in sort_numeric(rows, "selected_distance_km")[:20]]
    lines.extend(md_table(farthest, detail_cols, limit=20))

    lines.extend(["", "## Candidate Rank Outliers", ""])
    rank_rows = [compact_row(row) for row in sorted(rank_outliers, key=lambda r: to_int(r.get("selected_rank_order")) or 0, reverse=True)]
    lines.extend(md_table(rank_rows, detail_cols, limit=20))

    lines.extend(["", "## Cross-Border or Non-US Station Assignments", ""])
    lines.extend(md_table([compact_row(row) for row in non_us], detail_cols, limit=20))

    lines.extend(["", "## US Plant/Station State Mismatches", ""])
    lines.extend(md_table([compact_row(row) for row in state_mismatch], detail_cols, limit=20))

    lines.extend(["", f"## Selected Stations Ending Before {thresholds.old_station_last_year}", ""])
    old_rows = [compact_row(row) for row in sorted(old_station, key=lambda r: r.get("selected_station_last_observation_utc") or "")]
    lines.extend(
        md_table(
            old_rows,
            [
                ("Plant", "Plant"),
                ("Plant State", "Plant State"),
                ("Station", "Station"),
                ("Station State", "Station State"),
                ("Country", "Country"),
                ("Last Obs", "Last Obs"),
                ("Coverage", "Coverage"),
                ("ECWT F", "ECWT F"),
                ("Flags", "Flags"),
            ],
            limit=20,
        )
    )

    lines.extend(["", "## Warm Mainland ECWT Rows", ""])
    warm_rows = [compact_row(row) for row in sort_numeric(warm_mainland, "governing_ecwt_f")]
    lines.extend(md_table(warm_rows, detail_cols, limit=20))

    lines.extend(["", "## Near-Threshold Coverage Rows", ""])
    near_rows = [compact_row(row) for row in sort_numeric(near_threshold, "readiness_coverage_ratio", reverse=False)]
    lines.extend(md_table(near_rows, detail_cols, limit=20))

    lines.extend(
        [
            "",
            "## Method Notes",
            "",
            "- This script does not write to the database.",
            "- Selected station IDs come from `calc.plant_ecwt_readiness.selected_station_id` and are cross-checked against `link.station_selection_segment`.",
            "- Candidate rank, distance, elevation delta, and candidate coverage come from `link.station_candidate` for the candidate run embedded in the plant ECWT run parameters.",
            "- Station metadata comes from `weather.station`, and plant metadata comes from `asset.plant`.",
            "- Shared station counts are computed only across the strict publication-candidate cohort in this QA run.",
            "",
            "## Recommended Next Steps",
            "",
            "1. Review all rows with distance, cross-border/state, old-station, or warm-mainland flags before marking any ECWT output as compliance-ready.",
            "2. Decide whether to encode review dispositions in a database table, likely a new audited station-selection review table rather than editing provisional algorithmic rows.",
            "3. After review policy is defined, rebuild a release-candidate export that includes both ECWT values and station-selection review status.",
        ]
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--psql", type=Path, default=PSQL)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5436)
    parser.add_argument("--dbname", default="eop012")
    parser.add_argument("--user")
    parser.add_argument("--readiness-run-id")
    parser.add_argument("--distance-review-km", type=float, default=50.0)
    parser.add_argument("--high-distance-km", type=float, default=75.0)
    parser.add_argument("--near-threshold-coverage", type=float, default=0.97)
    parser.add_argument("--shared-station-review-count", type=int, default=10)
    parser.add_argument("--high-shared-station-count", type=int, default=25)
    parser.add_argument("--old-station-last-year", type=int, default=2010)
    parser.add_argument("--warm-mainland-ecwt-f", type=float, default=32.0)
    parser.add_argument("--warm-ecwt-f", type=float, default=35.0)
    args = parser.parse_args()

    timestamp = utc_now().strftime("%Y%m%dT%H%M%SZ")
    qa_run_id = f"station_selection_qa_{timestamp}"
    readiness_run_id = args.readiness_run_id or latest_strict_readiness_run_id(
        args.psql, args.host, args.port, args.dbname, args.user
    )
    params = fetch_run_params(args.psql, args.host, args.port, args.dbname, readiness_run_id, args.user)
    code_commit = git_commit_label(args.project_root)
    rows = psql_csv_query(args.psql, args.host, args.port, args.dbname, build_candidate_sql(readiness_run_id), args.user)
    for row in rows:
        row["qa_run_id"] = qa_run_id
    add_qa_flags(rows, args)

    docs_dir = args.project_root / "docs"
    csv_path = docs_dir / f"{qa_run_id}.csv"
    report_path = docs_dir / f"{qa_run_id}_report.md"
    write_csv(csv_path, rows)
    render_report(
        report_path,
        csv_path,
        qa_run_id,
        utc_now().isoformat(timespec="seconds"),
        code_commit,
        readiness_run_id,
        params,
        rows,
        args,
    )

    print(f"qa_run_id={qa_run_id}")
    print(f"readiness_run_id={readiness_run_id}")
    print(f"strict_candidate_rows={len(rows)}")
    print(f"csv_path={csv_path}")
    print(f"report_path={report_path}")


if __name__ == "__main__":
    main()
