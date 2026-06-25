#!/usr/bin/env python3
"""Compare near-threshold NOAA raw files with canonical DJF hourly rows.

This audit explains whether near-threshold normalized active-window coverage
gaps are caused by absent raw NOAA hours, loader rejections, or canonical-load
loss after a raw row would otherwise pass the current loader rules.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import subprocess
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable

from eop012_config import PROJECT_ROOT, PSQL, STAGING_ROOT
from load_noaa_hourly_djf import (
    DJF_MONTHS,
    SHEF_MIN_TEMP_C,
    canonical_hour,
    observation_score,
    open_text,
    parse_code_set,
    parse_noaa_datetime,
    parse_tmp,
)


METHODOLOGY_VERSION = "eop012-ecwt-method-v0.1.0"
SOURCE_FAMILY = "near_threshold_raw_canonical_gap_audit"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def sql_literal(value: object) -> str:
    if value is None:
        return "null"
    text = str(value)
    return "'" + text.replace("'", "''") + "'"


def sql_list(values: Iterable[str]) -> str:
    items = list(dict.fromkeys(values))
    if not items:
        return "null"
    return ", ".join(sql_literal(item) for item in items)


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
    user: str | None,
    query: str,
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
    user: str | None,
    query: str,
) -> str:
    result = run(psql_cmd(psql, host, port, dbname, user) + ["-At", "-c", query])
    return result.stdout.strip()


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: pg_csv_value(row.get(field)) for field in fieldnames})


def git_commit_label(project_root: Path) -> str:
    try:
        head = run(["git", "-C", str(project_root), "rev-parse", "HEAD"]).stdout.strip()
        dirty = run(["git", "-C", str(project_root), "status", "--porcelain"]).stdout.strip()
        return f"{head}-dirty" if dirty else head
    except Exception:
        return "UNKNOWN_GIT_COMMIT"


def latest_successful_run_id(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    prefix: str,
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
        where calculation_run_id like {sql_literal(prefix + '%')}
          and run_status = 'succeeded'
        order by run_finished_at_utc desc nulls last, calculation_run_id desc
        limit 1;
        """,
    )
    if not run_id:
        raise RuntimeError(f"No succeeded calculation run found with prefix {prefix!r}.")
    return run_id


def parse_ts(value: str | None) -> datetime | None:
    if not value:
        return None
    text = value.strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def int_value(value: object, default: int = 0) -> int:
    if value in (None, ""):
        return default
    return int(float(str(value)))


def float_value(value: object, default: float = 0.0) -> float:
    if value in (None, ""):
        return default
    return float(str(value))


def fmt_float(value: float | None, digits: int = 6) -> str:
    return "" if value is None else f"{value:.{digits}f}"


def hour_text(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def ceil_hour(dt: datetime) -> datetime:
    clean = dt.replace(minute=0, second=0, microsecond=0)
    return clean if clean == dt else clean + timedelta(hours=1)


def expected_hours_for_window(row: dict[str, str], source_year: int) -> list[datetime]:
    start = parse_ts(row.get("normalized_active_first_utc"))
    end = parse_ts(row.get("normalized_active_last_utc"))
    if start is None or end is None:
        return []

    segments = (
        (datetime(source_year, 1, 1, tzinfo=timezone.utc), datetime(source_year, 3, 1, tzinfo=timezone.utc)),
        (datetime(source_year, 12, 1, tzinfo=timezone.utc), datetime(source_year + 1, 1, 1, tzinfo=timezone.utc)),
    )
    hours: list[datetime] = []
    for seg_start, seg_end in segments:
        left = max(start, seg_start)
        right = min(end, seg_end)
        cursor = ceil_hour(left)
        while cursor < right:
            hours.append(cursor)
            cursor += timedelta(hours=1)
    return hours


def fetch_gap_rows(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    gap_audit_run_id: str,
) -> list[dict[str, str]]:
    return psql_csv_query(
        psql,
        host,
        port,
        dbname,
        user,
        f"""
        select *
        from calc.coverage_blocker_station_year_gap
        where gap_audit_run_id = {sql_literal(gap_audit_run_id)}
          and missing_to_normalized_expected_hours > 0
        order by impacted_plant_count desc, station_id, source_year
        """,
    )


def fetch_priority_rows(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    priority_run_id: str,
    station_ids: list[str],
    max_gap_hours: int,
) -> list[dict[str, str]]:
    return psql_csv_query(
        psql,
        host,
        port,
        dbname,
        user,
        f"""
        select
            priority_run_id,
            priority_rank::text as priority_rank,
            priority_bucket,
            plant_id,
            best_station_id as station_id,
            normalized_active_first_utc::text as normalized_active_first_utc,
            normalized_active_last_utc::text as normalized_active_last_utc,
            normalized_expected_djf_hours::text as normalized_expected_djf_hours,
            valid_hour_gap_to_threshold::text as valid_hour_gap_to_threshold
        from calc.coverage_blocker_priority
        where priority_run_id = {sql_literal(priority_run_id)}
          and best_station_id in ({sql_list(station_ids)})
          and valid_hour_gap_to_threshold <= {int(max_gap_hours)}
        order by best_station_id, priority_rank
        """,
    )


def fetch_canonical_hours(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    station_ids: list[str],
    min_year: int,
    max_year: int,
) -> dict[tuple[str, int], set[str]]:
    rows = psql_csv_query(
        psql,
        host,
        port,
        dbname,
        user,
        f"""
        select
            station_id,
            extract(year from hour_ending_utc at time zone 'UTC')::int::text as source_year,
            to_char(hour_ending_utc at time zone 'UTC', 'YYYY-MM-DD"T"HH24:MI:SS"Z"') as hour_utc
        from weather.hourly_djf
        where station_id in ({sql_list(station_ids)})
          and extract(year from hour_ending_utc at time zone 'UTC')::int between {int(min_year)} and {int(max_year)}
          and extract(month from hour_ending_utc at time zone 'UTC')::int in (1, 2, 12)
        """,
    )
    by_key: dict[tuple[str, int], set[str]] = defaultdict(set)
    for row in rows:
        by_key[(row["station_id"], int(row["source_year"]))].add(row["hour_utc"])
    return by_key


def classify_raw_file(
    path: Path,
    reject_source_codes: set[str],
    min_temp_c: float,
    max_temp_c: float,
) -> tuple[dict[str, dict[str, object]], dict[str, int], str]:
    hours: dict[str, dict[str, object]] = {}
    stats = Counter()
    error_message = ""

    try:
        with open_text(path) as handle:
            reader = csv.DictReader(handle)
            for raw in reader:
                stats["rows_seen"] += 1
                dt = parse_noaa_datetime(raw.get("DATE", ""))
                if dt is None or dt.month not in DJF_MONTHS:
                    continue
                stats["djf_rows_seen"] += 1
                hour = hour_text(canonical_hour(dt))
                state = hours.setdefault(
                    hour,
                    {
                        "raw_rows": 0,
                        "rejected_source_rows": 0,
                        "invalid_tmp_rows": 0,
                        "rejected_plausibility_rows": 0,
                        "accepted_rows": 0,
                        "best_score": None,
                    },
                )
                state["raw_rows"] = int(state["raw_rows"]) + 1

                noaa_source = (raw.get("SOURCE") or "").strip()
                if noaa_source in reject_source_codes:
                    state["rejected_source_rows"] = int(state["rejected_source_rows"]) + 1
                    stats["rejected_source_rows"] += 1
                    continue

                temp_c, tmp_quality = parse_tmp(raw.get("TMP", ""))
                if temp_c is None:
                    state["invalid_tmp_rows"] = int(state["invalid_tmp_rows"]) + 1
                    stats["invalid_tmp_rows"] += 1
                    continue

                report_type = (raw.get("REPORT_TYPE") or "").strip()
                if temp_c < min_temp_c or temp_c > max_temp_c or (report_type == "SHEF" and temp_c < SHEF_MIN_TEMP_C):
                    state["rejected_plausibility_rows"] = int(state["rejected_plausibility_rows"]) + 1
                    stats["rejected_plausibility_rows"] += 1
                    continue

                state["accepted_rows"] = int(state["accepted_rows"]) + 1
                stats["accepted_rows"] += 1
                score = observation_score(raw, dt, tmp_quality)
                current_score = state["best_score"]
                if current_score is None or score < current_score:
                    state["best_score"] = score
    except Exception as exc:
        error_message = str(exc)[:1000]

    stats["raw_hour_observed_count"] = len(hours)
    stats["raw_accepted_hour_count"] = sum(1 for state in hours.values() if int(state["accepted_rows"]) > 0)
    return hours, dict(stats), error_message


def choose_expected_hours(
    priority_rows: list[dict[str, str]],
    source_year: int,
    gap_expected_hours: int,
) -> tuple[list[datetime], int, bool, int, str]:
    candidates: list[tuple[dict[str, str], list[datetime]]] = []
    for row in priority_rows:
        hours = expected_hours_for_window(row, source_year)
        if hours:
            candidates.append((row, hours))
    if not candidates:
        return [], 0, False, -gap_expected_hours, "no_priority_window_candidate"

    matching = [(row, hours) for row, hours in candidates if len(hours) == gap_expected_hours]
    if not matching:
        max_count = max(len(hours) for _, hours in candidates)
        matching = [(row, hours) for row, hours in candidates if len(hours) == max_count]

    matching.sort(key=lambda item: int_value(item[0].get("priority_rank"), 999999999))
    chosen = matching[0]
    chosen_hours = chosen[1]
    mismatch = len(chosen_hours) - gap_expected_hours
    notes = ""
    if mismatch:
        notes = "Expected-window hour count does not match gap-table expected count."
    elif len(matching) > 1:
        notes = "Multiple priority rows share the selected expected-window hour count; earliest priority rank used."
    return chosen_hours, len(matching), len(matching) > 1, mismatch, notes


def classify_missing_hour(raw_state: dict[str, object] | None) -> str:
    if raw_state is None:
        return "source_hour_absent"
    raw_rows = int(raw_state["raw_rows"])
    accepted = int(raw_state["accepted_rows"])
    rejected_source = int(raw_state["rejected_source_rows"])
    invalid_tmp = int(raw_state["invalid_tmp_rows"])
    plausibility = int(raw_state["rejected_plausibility_rows"])

    if accepted > 0:
        return "accepted_raw_not_in_canonical"
    if rejected_source == raw_rows:
        return "loader_rejected_source"
    if invalid_tmp > 0:
        return "loader_invalid_tmp"
    if plausibility > 0:
        return "loader_rejected_plausibility"
    return "raw_present_unclassified"


STATION_YEAR_FIELDS = [
    "raw_canonical_audit_run_id",
    "gap_audit_run_id",
    "priority_run_id",
    "coverage_run_id",
    "inventory_run_id",
    "station_id",
    "station_name",
    "station_state",
    "station_country",
    "source_year",
    "impacted_plant_count",
    "raw_file_path",
    "raw_file_size_bytes",
    "coverage_status",
    "loaded_file_count",
    "gap_table_expected_hours",
    "gap_table_valid_hours",
    "gap_table_missing_hours",
    "expected_window_hour_count",
    "canonical_present_expected_window_hours",
    "canonical_missing_expected_window_hours",
    "window_missing_minus_gap_table_missing_hours",
    "expected_window_candidate_count",
    "expected_window_ambiguous",
    "expected_window_mismatch_hours",
    "raw_djf_row_count",
    "raw_hour_observed_count",
    "raw_accepted_hour_count",
    "source_hour_absent_count",
    "loader_rejected_source_hour_count",
    "loader_invalid_tmp_hour_count",
    "loader_rejected_plausibility_hour_count",
    "accepted_raw_not_in_canonical_hour_count",
    "raw_present_unclassified_hour_count",
    "primary_root_cause",
    "raw_parse_error",
    "notes",
]


STATION_SUMMARY_FIELDS = [
    "raw_canonical_audit_run_id",
    "gap_audit_run_id",
    "station_id",
    "station_name",
    "station_state",
    "station_country",
    "station_year_count",
    "impacted_plant_count",
    "gap_table_missing_hours",
    "canonical_missing_expected_window_hours",
    "window_missing_minus_gap_table_missing_hours",
    "source_hour_absent_count",
    "loader_rejected_source_hour_count",
    "loader_invalid_tmp_hour_count",
    "loader_rejected_plausibility_hour_count",
    "accepted_raw_not_in_canonical_hour_count",
    "raw_present_unclassified_hour_count",
    "accepted_raw_not_in_canonical_year_count",
    "expected_window_mismatch_year_count",
    "top_missing_years",
    "primary_root_cause",
]


def build_station_year_rows(
    run_id: str,
    gap_rows: list[dict[str, str]],
    priority_by_station: dict[str, list[dict[str, str]]],
    canonical_hours: dict[tuple[str, int], set[str]],
    reject_source_codes: set[str],
    min_temp_c: float,
    max_temp_c: float,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    raw_cache: dict[str, tuple[dict[str, dict[str, object]], dict[str, int], str]] = {}

    for gap in gap_rows:
        station_id = gap["station_id"]
        source_year = int(gap["source_year"])
        gap_expected = int_value(gap.get("normalized_expected_djf_hours"))
        gap_missing = int_value(gap.get("missing_to_normalized_expected_hours"))
        priority_rows = priority_by_station.get(station_id, [])
        expected_hours, candidate_count, ambiguous, expected_mismatch, window_notes = choose_expected_hours(
            priority_rows,
            source_year,
            gap_expected,
        )
        expected_texts = [hour_text(hour) for hour in expected_hours]
        canonical = canonical_hours.get((station_id, source_year), set())

        path_text = gap.get("raw_file_path") or ""
        if path_text not in raw_cache:
            if path_text:
                raw_cache[path_text] = classify_raw_file(Path(path_text), reject_source_codes, min_temp_c, max_temp_c)
            else:
                raw_cache[path_text] = ({}, {}, "No raw_file_path on gap row.")
        raw_hours, raw_stats, raw_error = raw_cache[path_text]

        root_counts = Counter()
        canonical_present = 0
        for hour in expected_texts:
            if hour in canonical:
                canonical_present += 1
                continue
            root_counts[classify_missing_hour(raw_hours.get(hour))] += 1

        canonical_missing = len(expected_texts) - canonical_present
        primary_root = ""
        if root_counts:
            primary_root = root_counts.most_common(1)[0][0]
        elif canonical_missing == 0:
            primary_root = "no_expected_window_gap"

        notes = "; ".join(note for note in (window_notes, "Raw file parse failed." if raw_error else "") if note)
        rows.append(
            {
                "raw_canonical_audit_run_id": run_id,
                "gap_audit_run_id": gap["gap_audit_run_id"],
                "priority_run_id": gap["priority_run_id"],
                "coverage_run_id": gap["coverage_run_id"],
                "inventory_run_id": gap["inventory_run_id"],
                "station_id": station_id,
                "station_name": gap.get("station_name", ""),
                "station_state": gap.get("station_state", ""),
                "station_country": gap.get("station_country", ""),
                "source_year": source_year,
                "impacted_plant_count": gap.get("impacted_plant_count", ""),
                "raw_file_path": path_text,
                "raw_file_size_bytes": gap.get("raw_file_size_bytes", ""),
                "coverage_status": gap.get("coverage_status", ""),
                "loaded_file_count": gap.get("loaded_file_count", ""),
                "gap_table_expected_hours": gap_expected,
                "gap_table_valid_hours": int_value(gap.get("valid_djf_hours")),
                "gap_table_missing_hours": gap_missing,
                "expected_window_hour_count": len(expected_texts),
                "canonical_present_expected_window_hours": canonical_present,
                "canonical_missing_expected_window_hours": canonical_missing,
                "window_missing_minus_gap_table_missing_hours": canonical_missing - gap_missing,
                "expected_window_candidate_count": candidate_count,
                "expected_window_ambiguous": str(bool(ambiguous)).lower(),
                "expected_window_mismatch_hours": expected_mismatch,
                "raw_djf_row_count": raw_stats.get("djf_rows_seen", 0),
                "raw_hour_observed_count": raw_stats.get("raw_hour_observed_count", 0),
                "raw_accepted_hour_count": raw_stats.get("raw_accepted_hour_count", 0),
                "source_hour_absent_count": root_counts.get("source_hour_absent", 0),
                "loader_rejected_source_hour_count": root_counts.get("loader_rejected_source", 0),
                "loader_invalid_tmp_hour_count": root_counts.get("loader_invalid_tmp", 0),
                "loader_rejected_plausibility_hour_count": root_counts.get("loader_rejected_plausibility", 0),
                "accepted_raw_not_in_canonical_hour_count": root_counts.get("accepted_raw_not_in_canonical", 0),
                "raw_present_unclassified_hour_count": root_counts.get("raw_present_unclassified", 0),
                "primary_root_cause": primary_root,
                "raw_parse_error": raw_error,
                "notes": notes,
            }
        )

    return rows


def build_station_summary(rows: list[dict[str, object]], run_id: str) -> list[dict[str, object]]:
    by_station: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_station[str(row["station_id"])].append(row)

    summaries: list[dict[str, object]] = []
    for station_id, group in by_station.items():
        root_counts = Counter()
        for field, reason in (
            ("source_hour_absent_count", "source_hour_absent"),
            ("loader_rejected_source_hour_count", "loader_rejected_source"),
            ("loader_invalid_tmp_hour_count", "loader_invalid_tmp"),
            ("loader_rejected_plausibility_hour_count", "loader_rejected_plausibility"),
            ("accepted_raw_not_in_canonical_hour_count", "accepted_raw_not_in_canonical"),
            ("raw_present_unclassified_hour_count", "raw_present_unclassified"),
        ):
            root_counts[reason] = sum(int_value(row.get(field)) for row in group)
        primary_root = root_counts.most_common(1)[0][0] if root_counts else ""
        top_years = sorted(
            group,
            key=lambda row: (-int_value(row.get("canonical_missing_expected_window_hours")), int_value(row.get("source_year"))),
        )[:8]
        first = group[0]
        summaries.append(
            {
                "raw_canonical_audit_run_id": run_id,
                "gap_audit_run_id": first["gap_audit_run_id"],
                "station_id": station_id,
                "station_name": first.get("station_name", ""),
                "station_state": first.get("station_state", ""),
                "station_country": first.get("station_country", ""),
                "station_year_count": len(group),
                "impacted_plant_count": max(int_value(row.get("impacted_plant_count")) for row in group),
                "gap_table_missing_hours": sum(int_value(row.get("gap_table_missing_hours")) for row in group),
                "canonical_missing_expected_window_hours": sum(
                    int_value(row.get("canonical_missing_expected_window_hours")) for row in group
                ),
                "window_missing_minus_gap_table_missing_hours": sum(
                    int_value(row.get("window_missing_minus_gap_table_missing_hours")) for row in group
                ),
                "source_hour_absent_count": root_counts["source_hour_absent"],
                "loader_rejected_source_hour_count": root_counts["loader_rejected_source"],
                "loader_invalid_tmp_hour_count": root_counts["loader_invalid_tmp"],
                "loader_rejected_plausibility_hour_count": root_counts["loader_rejected_plausibility"],
                "accepted_raw_not_in_canonical_hour_count": root_counts["accepted_raw_not_in_canonical"],
                "raw_present_unclassified_hour_count": root_counts["raw_present_unclassified"],
                "accepted_raw_not_in_canonical_year_count": sum(
                    1 for row in group if int_value(row.get("accepted_raw_not_in_canonical_hour_count")) > 0
                ),
                "expected_window_mismatch_year_count": sum(
                    1 for row in group if int_value(row.get("expected_window_mismatch_hours")) != 0
                ),
                "top_missing_years": "; ".join(
                    f"{row['source_year']}:{row['canonical_missing_expected_window_hours']}h" for row in top_years
                ),
                "primary_root_cause": primary_root,
            }
        )
    summaries.sort(
        key=lambda row: (
            -int_value(row["canonical_missing_expected_window_hours"]),
            -int_value(row["impacted_plant_count"]),
            str(row["station_id"]),
        )
    )
    return summaries


def copy_sql(table: str, columns: list[str], path: Path) -> str:
    return f"\\copy {table} ({', '.join(columns)}) from '{path}' with (format csv, header true, null '\\N')"


def temp_table_sql(table: str, columns: list[str]) -> str:
    return "create temp table " + table + " (\n" + ",\n".join(f"    {column} text" for column in columns) + "\n);"


def qident(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def text_null(field: str) -> str:
    return f"nullif({qident(field)}, '')"


def int_null(field: str) -> str:
    return f"nullif({qident(field)}, '')::integer"


def bigint_null(field: str) -> str:
    return f"nullif({qident(field)}, '')::bigint"


def bool_cast(field: str) -> str:
    return f"coalesce(nullif({qident(field)}, '')::boolean, false)"


def build_load_sql(
    run_id: str,
    code_commit: str,
    started_at: str,
    params: dict[str, object],
    station_year_csv: Path,
    station_summary_csv: Path,
) -> str:
    return f"""
\\set ON_ERROR_STOP on
begin;

create table if not exists calc.coverage_blocker_raw_canonical_gap_summary (
    raw_canonical_audit_run_id text not null references audit.calculation_run(calculation_run_id),
    gap_audit_run_id text not null references audit.calculation_run(calculation_run_id),
    priority_run_id text not null references audit.calculation_run(calculation_run_id),
    coverage_run_id text not null references audit.calculation_run(calculation_run_id),
    inventory_run_id text not null references audit.calculation_run(calculation_run_id),
    station_id text not null references weather.station(station_id),
    station_name text,
    station_state text,
    station_country text,
    source_year integer not null,
    impacted_plant_count bigint,
    raw_file_path text,
    raw_file_size_bytes bigint,
    coverage_status text,
    loaded_file_count bigint,
    gap_table_expected_hours bigint,
    gap_table_valid_hours bigint,
    gap_table_missing_hours bigint,
    expected_window_hour_count bigint,
    canonical_present_expected_window_hours bigint,
    canonical_missing_expected_window_hours bigint,
    window_missing_minus_gap_table_missing_hours bigint,
    expected_window_candidate_count integer,
    expected_window_ambiguous boolean,
    expected_window_mismatch_hours bigint,
    raw_djf_row_count bigint,
    raw_hour_observed_count bigint,
    raw_accepted_hour_count bigint,
    source_hour_absent_count bigint,
    loader_rejected_source_hour_count bigint,
    loader_invalid_tmp_hour_count bigint,
    loader_rejected_plausibility_hour_count bigint,
    accepted_raw_not_in_canonical_hour_count bigint,
    raw_present_unclassified_hour_count bigint,
    primary_root_cause text,
    raw_parse_error text,
    notes text,
    created_at_utc timestamptz not null default now(),
    primary key (raw_canonical_audit_run_id, station_id, source_year)
);
create index if not exists ix_raw_canonical_gap_summary_gap_run
    on calc.coverage_blocker_raw_canonical_gap_summary (gap_audit_run_id, station_id, source_year);
create index if not exists ix_raw_canonical_gap_summary_root
    on calc.coverage_blocker_raw_canonical_gap_summary (raw_canonical_audit_run_id, primary_root_cause);

create table if not exists calc.coverage_blocker_raw_canonical_station_summary (
    raw_canonical_audit_run_id text not null references audit.calculation_run(calculation_run_id),
    gap_audit_run_id text not null references audit.calculation_run(calculation_run_id),
    station_id text not null references weather.station(station_id),
    station_name text,
    station_state text,
    station_country text,
    station_year_count bigint,
    impacted_plant_count bigint,
    gap_table_missing_hours bigint,
    canonical_missing_expected_window_hours bigint,
    window_missing_minus_gap_table_missing_hours bigint,
    source_hour_absent_count bigint,
    loader_rejected_source_hour_count bigint,
    loader_invalid_tmp_hour_count bigint,
    loader_rejected_plausibility_hour_count bigint,
    accepted_raw_not_in_canonical_hour_count bigint,
    raw_present_unclassified_hour_count bigint,
    accepted_raw_not_in_canonical_year_count bigint,
    expected_window_mismatch_year_count bigint,
    top_missing_years text,
    primary_root_cause text,
    created_at_utc timestamptz not null default now(),
    primary key (raw_canonical_audit_run_id, station_id)
);
create index if not exists ix_raw_canonical_station_summary_gap_run
    on calc.coverage_blocker_raw_canonical_station_summary (gap_audit_run_id, station_id);

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
    {sql_literal(started_at)},
    now(),
    'succeeded',
    {sql_literal(json.dumps(params, sort_keys=True))}::jsonb,
    'Compared near-threshold raw NOAA station-year files with canonical weather.hourly_djf rows and classified missing expected-window hours.'
)
on conflict (calculation_run_id) do update set
    run_finished_at_utc = excluded.run_finished_at_utc,
    run_status = excluded.run_status,
    parameters_json = excluded.parameters_json,
    notes = excluded.notes;

{temp_table_sql("tmp_raw_canonical_station_year", STATION_YEAR_FIELDS)}
{copy_sql("tmp_raw_canonical_station_year", STATION_YEAR_FIELDS, station_year_csv)}
{temp_table_sql("tmp_raw_canonical_station", STATION_SUMMARY_FIELDS)}
{copy_sql("tmp_raw_canonical_station", STATION_SUMMARY_FIELDS, station_summary_csv)}

delete from calc.coverage_blocker_raw_canonical_gap_summary
where raw_canonical_audit_run_id = {sql_literal(run_id)};
delete from calc.coverage_blocker_raw_canonical_station_summary
where raw_canonical_audit_run_id = {sql_literal(run_id)};

insert into calc.coverage_blocker_raw_canonical_gap_summary (
    raw_canonical_audit_run_id,
    gap_audit_run_id,
    priority_run_id,
    coverage_run_id,
    inventory_run_id,
    station_id,
    station_name,
    station_state,
    station_country,
    source_year,
    impacted_plant_count,
    raw_file_path,
    raw_file_size_bytes,
    coverage_status,
    loaded_file_count,
    gap_table_expected_hours,
    gap_table_valid_hours,
    gap_table_missing_hours,
    expected_window_hour_count,
    canonical_present_expected_window_hours,
    canonical_missing_expected_window_hours,
    window_missing_minus_gap_table_missing_hours,
    expected_window_candidate_count,
    expected_window_ambiguous,
    expected_window_mismatch_hours,
    raw_djf_row_count,
    raw_hour_observed_count,
    raw_accepted_hour_count,
    source_hour_absent_count,
    loader_rejected_source_hour_count,
    loader_invalid_tmp_hour_count,
    loader_rejected_plausibility_hour_count,
    accepted_raw_not_in_canonical_hour_count,
    raw_present_unclassified_hour_count,
    primary_root_cause,
    raw_parse_error,
    notes
)
select
    {text_null("raw_canonical_audit_run_id")},
    {text_null("gap_audit_run_id")},
    {text_null("priority_run_id")},
    {text_null("coverage_run_id")},
    {text_null("inventory_run_id")},
    {text_null("station_id")},
    {text_null("station_name")},
    {text_null("station_state")},
    {text_null("station_country")},
    {int_null("source_year")},
    {bigint_null("impacted_plant_count")},
    {text_null("raw_file_path")},
    {bigint_null("raw_file_size_bytes")},
    {text_null("coverage_status")},
    {bigint_null("loaded_file_count")},
    {bigint_null("gap_table_expected_hours")},
    {bigint_null("gap_table_valid_hours")},
    {bigint_null("gap_table_missing_hours")},
    {bigint_null("expected_window_hour_count")},
    {bigint_null("canonical_present_expected_window_hours")},
    {bigint_null("canonical_missing_expected_window_hours")},
    {bigint_null("window_missing_minus_gap_table_missing_hours")},
    {int_null("expected_window_candidate_count")},
    {bool_cast("expected_window_ambiguous")},
    {bigint_null("expected_window_mismatch_hours")},
    {bigint_null("raw_djf_row_count")},
    {bigint_null("raw_hour_observed_count")},
    {bigint_null("raw_accepted_hour_count")},
    {bigint_null("source_hour_absent_count")},
    {bigint_null("loader_rejected_source_hour_count")},
    {bigint_null("loader_invalid_tmp_hour_count")},
    {bigint_null("loader_rejected_plausibility_hour_count")},
    {bigint_null("accepted_raw_not_in_canonical_hour_count")},
    {bigint_null("raw_present_unclassified_hour_count")},
    {text_null("primary_root_cause")},
    {text_null("raw_parse_error")},
    {text_null("notes")}
from tmp_raw_canonical_station_year;

insert into calc.coverage_blocker_raw_canonical_station_summary (
    raw_canonical_audit_run_id,
    gap_audit_run_id,
    station_id,
    station_name,
    station_state,
    station_country,
    station_year_count,
    impacted_plant_count,
    gap_table_missing_hours,
    canonical_missing_expected_window_hours,
    window_missing_minus_gap_table_missing_hours,
    source_hour_absent_count,
    loader_rejected_source_hour_count,
    loader_invalid_tmp_hour_count,
    loader_rejected_plausibility_hour_count,
    accepted_raw_not_in_canonical_hour_count,
    raw_present_unclassified_hour_count,
    accepted_raw_not_in_canonical_year_count,
    expected_window_mismatch_year_count,
    top_missing_years,
    primary_root_cause
)
select
    {text_null("raw_canonical_audit_run_id")},
    {text_null("gap_audit_run_id")},
    {text_null("station_id")},
    {text_null("station_name")},
    {text_null("station_state")},
    {text_null("station_country")},
    {bigint_null("station_year_count")},
    {bigint_null("impacted_plant_count")},
    {bigint_null("gap_table_missing_hours")},
    {bigint_null("canonical_missing_expected_window_hours")},
    {bigint_null("window_missing_minus_gap_table_missing_hours")},
    {bigint_null("source_hour_absent_count")},
    {bigint_null("loader_rejected_source_hour_count")},
    {bigint_null("loader_invalid_tmp_hour_count")},
    {bigint_null("loader_rejected_plausibility_hour_count")},
    {bigint_null("accepted_raw_not_in_canonical_hour_count")},
    {bigint_null("raw_present_unclassified_hour_count")},
    {bigint_null("accepted_raw_not_in_canonical_year_count")},
    {bigint_null("expected_window_mismatch_year_count")},
    {text_null("top_missing_years")},
    {text_null("primary_root_cause")}
from tmp_raw_canonical_station;

commit;
"""


def render_table(lines: list[str], headers: list[str], rows: list[dict[str, object]], fields: list[str], limit: int | None = None) -> None:
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join("---" for _ in headers) + " |")
    selected = rows if limit is None else rows[:limit]
    for row in selected:
        lines.append("| " + " | ".join(str(row.get(field, "")) for field in fields) + " |")
    if limit is not None and len(rows) > limit:
        lines.append(f"| ... | {len(rows) - limit:,} more rows omitted | | | | | | | | |")


def render_report(
    run_id: str,
    params: dict[str, object],
    station_year_rows: list[dict[str, object]],
    station_rows: list[dict[str, object]],
    output_dir: Path,
) -> str:
    total_gap_missing = sum(int_value(row["gap_table_missing_hours"]) for row in station_year_rows)
    total_window_missing = sum(int_value(row["canonical_missing_expected_window_hours"]) for row in station_year_rows)
    root_counts = Counter()
    for row in station_year_rows:
        root_counts["source_hour_absent"] += int_value(row["source_hour_absent_count"])
        root_counts["loader_rejected_source"] += int_value(row["loader_rejected_source_hour_count"])
        root_counts["loader_invalid_tmp"] += int_value(row["loader_invalid_tmp_hour_count"])
        root_counts["loader_rejected_plausibility"] += int_value(row["loader_rejected_plausibility_hour_count"])
        root_counts["accepted_raw_not_in_canonical"] += int_value(row["accepted_raw_not_in_canonical_hour_count"])
        root_counts["raw_present_unclassified"] += int_value(row["raw_present_unclassified_hour_count"])

    root_rows = [{"reason": reason, "hours": f"{hours:,}"} for reason, hours in root_counts.most_common()]
    top_stations = [
        {
            "station_id": row["station_id"],
            "station_name": row["station_name"],
            "state": row["station_state"],
            "years": row["station_year_count"],
            "window_missing": f"{int_value(row['canonical_missing_expected_window_hours']):,}",
            "gap_missing": f"{int_value(row['gap_table_missing_hours']):,}",
            "primary": row["primary_root_cause"],
            "top_years": row["top_missing_years"],
        }
        for row in station_rows[:20]
    ]
    mismatch_years = sum(1 for row in station_year_rows if int_value(row["expected_window_mismatch_hours"]) != 0)
    accepted_not_loaded_years = sum(1 for row in station_year_rows if int_value(row["accepted_raw_not_in_canonical_hour_count"]) > 0)

    lines = [
        "# Near-Threshold Raw vs Canonical Gap Audit",
        "",
        f"- Raw/canonical audit run ID: `{run_id}`",
        f"- Gap audit run ID: `{params['gap_audit_run_id']}`",
        f"- Rejected NOAA source codes: `{params['reject_source_codes']}`",
        f"- Plausible temperature range C: `{params['min_temp_c']}` to `{params['max_temp_c']}`",
        f"- Station-year CSV: `{run_id}_station_years.csv`",
        f"- Station summary CSV: `{run_id}_stations.csv`",
        "",
        "## Scope",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Station-year rows audited | {len(station_year_rows):,} |",
        f"| Stations audited | {len(station_rows):,} |",
        f"| Gap-table missing hours | {total_gap_missing:,} |",
        f"| Canonical missing hours inside selected expected windows | {total_window_missing:,} |",
        f"| Window missing minus gap-table missing hours | {total_window_missing - total_gap_missing:,} |",
        f"| Station-years with expected-window count mismatch | {mismatch_years:,} |",
        f"| Station-years with accepted raw rows absent from canonical table | {accepted_not_loaded_years:,} |",
        "",
        "## Missing-Hour Classification",
        "",
    ]
    render_table(lines, ["Reason", "Hours"], root_rows, ["reason", "hours"])
    lines.extend(
        [
            "",
            "## Top Stations",
            "",
        ]
    )
    render_table(
        lines,
        ["Station", "Name", "State", "Years", "Window Missing", "Gap Missing", "Primary", "Top Years"],
        top_stations,
        ["station_id", "station_name", "state", "years", "window_missing", "gap_missing", "primary", "top_years"],
    )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `source_hour_absent` means no raw NOAA Global Hourly row exists in the local raw file for the expected canonical UTC hour.",
            "- `loader_rejected_source` means raw rows exist, but all rows for the hour use a source code rejected by the current loader configuration.",
            "- `loader_invalid_tmp` means raw rows exist after source filtering, but the NOAA `TMP` value is missing, sentinel, malformed, or quality code `9`.",
            "- `loader_rejected_plausibility` means a parsed temperature exists but is outside the configured loader plausibility range.",
            "- `accepted_raw_not_in_canonical` is the red-flag class: at least one raw row would pass the current loader rules, but `weather.hourly_djf` does not contain the expected station-hour.",
            "- A nonzero window/gap delta means the prior station-year gap table is count-based: it compares normalized active-window expected hours to full station-year valid hours, not to canonical hours clipped to that exact expected window.",
        ]
    )
    report = "\n".join(lines) + "\n"
    (output_dir / f"{run_id}_report.md").write_text(report, encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--staging-root", type=Path, default=STAGING_ROOT)
    parser.add_argument("--docs-dir", type=Path, default=PROJECT_ROOT / "docs")
    parser.add_argument("--psql", type=Path, default=PSQL)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5436)
    parser.add_argument("--dbname", default="eop012")
    parser.add_argument("--user", default=None)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--gap-audit-run-id", default=None)
    parser.add_argument("--max-gap-hours", type=int, default=168)
    parser.add_argument("--reject-source-code", action="append", default=["7"])
    parser.add_argument("--min-temp-c", type=float, default=-65.0)
    parser.add_argument("--max-temp-c", type=float, default=40.0)
    args = parser.parse_args()

    if not args.psql.exists():
        raise FileNotFoundError(args.psql)
    if args.min_temp_c >= args.max_temp_c:
        raise ValueError("--min-temp-c must be lower than --max-temp-c")

    gap_audit_run_id = args.gap_audit_run_id or latest_successful_run_id(
        args.psql,
        args.host,
        args.port,
        args.dbname,
        args.user,
        "near_threshold_station_year_gap_audit_",
    )
    gap_rows = fetch_gap_rows(args.psql, args.host, args.port, args.dbname, args.user, gap_audit_run_id)
    if not gap_rows:
        raise RuntimeError(f"No station-year gap rows found for {gap_audit_run_id}.")

    priority_run_ids = sorted({row["priority_run_id"] for row in gap_rows})
    if len(priority_run_ids) != 1:
        raise RuntimeError(f"Expected one priority run for {gap_audit_run_id}; found {priority_run_ids}.")
    priority_run_id = priority_run_ids[0]
    station_ids = sorted({row["station_id"] for row in gap_rows})
    years = [int(row["source_year"]) for row in gap_rows]

    priority_rows = fetch_priority_rows(
        args.psql,
        args.host,
        args.port,
        args.dbname,
        args.user,
        priority_run_id,
        station_ids,
        args.max_gap_hours,
    )
    priority_by_station: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in priority_rows:
        priority_by_station[row["station_id"]].append(row)

    canonical_hours = fetch_canonical_hours(
        args.psql,
        args.host,
        args.port,
        args.dbname,
        args.user,
        station_ids,
        min(years),
        max(years),
    )

    code_commit = git_commit_label(args.project_root)
    run_timestamp = utc_now().strftime("%Y%m%dT%H%M%SZ")
    run_id = args.run_id or f"near_threshold_raw_canonical_gap_audit_{run_timestamp}"
    staging_dir = args.staging_root / run_id
    staging_dir.mkdir(parents=True, exist_ok=True)
    args.docs_dir.mkdir(parents=True, exist_ok=True)

    reject_source_codes = parse_code_set(args.reject_source_code)
    station_year_rows = build_station_year_rows(
        run_id,
        gap_rows,
        priority_by_station,
        canonical_hours,
        reject_source_codes,
        args.min_temp_c,
        args.max_temp_c,
    )
    station_rows = build_station_summary(station_year_rows, run_id)

    station_year_staging = staging_dir / f"{run_id}_station_years.csv"
    station_summary_staging = staging_dir / f"{run_id}_stations.csv"
    station_year_doc = args.docs_dir / f"{run_id}_station_years.csv"
    station_summary_doc = args.docs_dir / f"{run_id}_stations.csv"
    write_csv(station_year_staging, STATION_YEAR_FIELDS, station_year_rows)
    write_csv(station_summary_staging, STATION_SUMMARY_FIELDS, station_rows)
    write_csv(station_year_doc, STATION_YEAR_FIELDS, station_year_rows)
    write_csv(station_summary_doc, STATION_SUMMARY_FIELDS, station_rows)

    params = {
        "source_family": SOURCE_FAMILY,
        "gap_audit_run_id": gap_audit_run_id,
        "priority_run_id": priority_run_id,
        "max_gap_hours": args.max_gap_hours,
        "reject_source_codes": sorted(reject_source_codes),
        "min_temp_c": args.min_temp_c,
        "max_temp_c": args.max_temp_c,
        "station_year_rows": len(station_year_rows),
        "station_count": len(station_rows),
    }
    started_at = utc_now().isoformat(timespec="seconds")
    load_sql = build_load_sql(run_id, code_commit, started_at, params, station_year_staging, station_summary_staging)
    run(psql_cmd(args.psql, args.host, args.port, args.dbname, args.user), input_text=load_sql)
    render_report(run_id, params, station_year_rows, station_rows, args.docs_dir)

    total_window_missing = sum(int_value(row["canonical_missing_expected_window_hours"]) for row in station_year_rows)
    total_gap_missing = sum(int_value(row["gap_table_missing_hours"]) for row in station_year_rows)
    print(f"run_id={run_id}")
    print(f"station_year_rows={len(station_year_rows)}")
    print(f"station_rows={len(station_rows)}")
    print(f"gap_table_missing_hours={total_gap_missing}")
    print(f"canonical_missing_expected_window_hours={total_window_missing}")
    print(f"window_missing_minus_gap_table_missing_hours={total_window_missing - total_gap_missing}")
    print(f"report={args.docs_dir / f'{run_id}_report.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
