#!/usr/bin/env python3
"""Build secondary-station fill ECWT rows for plants blocked by near-threshold coverage."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import subprocess
from collections import Counter, OrderedDict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from eop012_config import PROJECT_ROOT, PSQL


METHODOLOGY_VERSION = "eop012-ecwt-method-v0.1.0"
SOURCE_FAMILY = "secondary_station_fill_ecwt"
DEFAULT_POLICY_PREFIX = "plant_ecwt_policy_result_all_plants_normalized_active_window_loaded_year_"
DEFAULT_CANDIDATE_PREFIX = "noaa_station_candidates_"
DEFAULT_STATION_ECWT_PREFIX = "station_ecwt_loaded_"

BEST_FIELDS = [
    "secondary_fill_id",
    "secondary_fill_run_id",
    "policy_result_run_id",
    "station_candidate_run_id",
    "station_ecwt_run_id",
    "plant_id",
    "eia_plant_code",
    "plant_name",
    "plant_state",
    "plant_county",
    "sector_name",
    "street_address",
    "city",
    "zip",
    "plant_latitude",
    "plant_longitude",
    "primary_station_id",
    "primary_station_name",
    "primary_station_state",
    "primary_station_country",
    "primary_station_distance_km",
    "primary_station_rank_order",
    "fallback_station_id",
    "fallback_station_name",
    "fallback_station_state",
    "fallback_station_country",
    "fallback_station_distance_km",
    "fallback_station_rank_order",
    "fallback_station_ecwt_f",
    "fallback_station_ecwt_discrete_f",
    "policy_expected_hour_count",
    "generated_expected_hour_count",
    "required_valid_hour_count",
    "policy_primary_valid_hour_count",
    "recomputed_primary_valid_hour_count",
    "fallback_fill_hour_count",
    "fallback_overlap_valid_hour_count",
    "fallback_standalone_valid_hour_count",
    "composite_valid_hour_count",
    "policy_primary_coverage_ratio",
    "recomputed_primary_coverage_ratio",
    "composite_coverage_ratio",
    "coverage_gain_ratio",
    "primary_ecwt_f",
    "composite_ecwt_f",
    "composite_ecwt_discrete_f",
    "percentile_target",
    "candidate_count",
    "passing_candidate_count",
    "chosen_passing_distance_rank",
    "fill_status",
    "notes",
]

SCORE_FIELDS = [
    "secondary_fill_run_id",
    "policy_result_run_id",
    "station_candidate_run_id",
    "station_ecwt_run_id",
    "plant_id",
    "eia_plant_code",
    "plant_name",
    "plant_state",
    "primary_station_id",
    "primary_station_name",
    "fallback_station_id",
    "fallback_station_name",
    "fallback_station_state",
    "fallback_station_country",
    "fallback_station_distance_km",
    "fallback_station_rank_order",
    "fallback_station_ecwt_f",
    "policy_expected_hour_count",
    "generated_expected_hour_count",
    "required_valid_hour_count",
    "policy_primary_valid_hour_count",
    "recomputed_primary_valid_hour_count",
    "fallback_fill_hour_count",
    "fallback_overlap_valid_hour_count",
    "fallback_standalone_valid_hour_count",
    "composite_valid_hour_count",
    "policy_primary_coverage_ratio",
    "recomputed_primary_coverage_ratio",
    "composite_coverage_ratio",
    "coverage_gain_ratio",
    "primary_ecwt_f",
    "composite_ecwt_f",
    "composite_ecwt_discrete_f",
    "fill_status",
    "distance_rank_among_passing",
    "notes",
]


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def sql_literal(value: object) -> str:
    if value is None:
        return "null"
    return "'" + str(value).replace("'", "''") + "'"


def sql_list(values: Iterable[str]) -> str:
    items = list(dict.fromkeys(str(value) for value in values))
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
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: pg_csv_value(row.get(field)) for field in fieldnames})


def read_csv_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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
        order by run_started_at_utc desc nulls last, calculation_run_id desc
        limit 1;
        """,
    )
    if not run_id:
        raise RuntimeError(f"No succeeded calculation run found with prefix {prefix!r}.")
    return run_id


def score_query(
    run_id: str,
    policy_result_run_id: str,
    station_candidate_run_id: str,
    station_ecwt_run_id: str,
    coverage_threshold: float,
    percentile_target: float,
    include_ak: bool,
    plant_codes: list[str],
    max_candidates_per_plant: int,
) -> str:
    state_filter = "true" if include_ak else "coalesce(pr.plant_state, '') <> 'AK'"
    plant_filter = "true"
    if plant_codes:
        plant_filter = f"pr.eia_plant_code in ({sql_list(plant_codes)})"
    candidate_rank_filter = ""
    if max_candidates_per_plant > 0:
        candidate_rank_filter = f"and sc.rank_order <= {int(max_candidates_per_plant)}"

    return f"""
    with target as (
        select
            pr.policy_result_run_id,
            pr.plant_id,
            pr.eia_plant_code,
            pr.plant_name,
            pr.plant_state,
            pr.plant_county,
            pr.sector_name,
            p.street_address,
            p.city,
            p.zip,
            p.latitude as plant_latitude,
            p.longitude as plant_longitude,
            pr.selected_station_id as primary_station_id,
            pr.selected_station_name as primary_station_name,
            pr.selected_station_state as primary_station_state,
            pr.selected_station_country as primary_station_country,
            pr.selected_station_distance_km as primary_station_distance_km,
            pr.selected_station_rank_order as primary_station_rank_order,
            pr.ecwt_f as primary_ecwt_f,
            pr.valid_hour_count as policy_primary_valid_hour_count,
            pr.expected_hour_count as policy_expected_hour_count,
            pr.coverage_ratio as policy_primary_coverage_ratio
        from calc.plant_ecwt_policy_result pr
        join asset.plant p using (plant_id)
        where pr.policy_result_run_id = {sql_literal(policy_result_run_id)}
          and pr.readiness_status = 'blocked'
          and pr.reason_code = 'normalized_active_window_coverage_below_threshold'
          and pr.selected_station_id is not null
          and {state_filter}
          and {plant_filter}
    ),
    primary_year_bounds as (
        select
            t.plant_id,
            min(extract(year from h.hour_ending_utc at time zone 'UTC'))::integer as min_year,
            max(extract(year from h.hour_ending_utc at time zone 'UTC'))::integer as max_year
        from target t
        join weather.hourly_djf h
          on h.station_id = t.primary_station_id
         and h.dry_bulb_f is not null
        group by t.plant_id
    ),
    target_with_years as (
        select t.*, y.min_year, y.max_year
        from target t
        join primary_year_bounds y using (plant_id)
    ),
    source_years as (
        select plant_id, generate_series(min_year, max_year)::integer as source_year
        from target_with_years
    ),
    expected_hour as (
        select
            sy.plant_id,
            generate_series(
                make_timestamptz(sy.source_year, 1, 1, 0, 0, 0, 'UTC'),
                make_timestamptz(sy.source_year, 3, 1, 0, 0, 0, 'UTC') - interval '1 hour',
                interval '1 hour'
            ) as hour_ending_utc
        from source_years sy
        union all
        select
            sy.plant_id,
            generate_series(
                make_timestamptz(sy.source_year, 12, 1, 0, 0, 0, 'UTC'),
                make_timestamptz(sy.source_year + 1, 1, 1, 0, 0, 0, 'UTC') - interval '1 hour',
                interval '1 hour'
            ) as hour_ending_utc
        from source_years sy
    ),
    candidate as (
        select
            sc.plant_id,
            sc.station_id as fallback_station_id,
            sc.rank_order as fallback_station_rank_order,
            sc.distance_km as fallback_station_distance_km,
            st.station_name as fallback_station_name,
            st.state as fallback_station_state,
            st.country as fallback_station_country,
            se.ecwt_f as fallback_station_ecwt_f,
            se.ecwt_discrete_f as fallback_station_ecwt_discrete_f
        from target_with_years t
        join link.station_candidate sc
          on sc.plant_id = t.plant_id
         and sc.calculation_run_id = {sql_literal(station_candidate_run_id)}
         and sc.candidate_status in ('candidate', 'selected')
         and sc.station_id <> t.primary_station_id
         {candidate_rank_filter}
        join weather.station st
          on st.station_id = sc.station_id
        left join calc.station_ecwt se
          on se.station_id = sc.station_id
         and se.calculation_run_id = {sql_literal(station_ecwt_run_id)}
    ),
    score as (
        select
            {sql_literal(run_id)}::text as secondary_fill_run_id,
            {sql_literal(policy_result_run_id)}::text as policy_result_run_id,
            {sql_literal(station_candidate_run_id)}::text as station_candidate_run_id,
            {sql_literal(station_ecwt_run_id)}::text as station_ecwt_run_id,
            t.plant_id,
            t.eia_plant_code,
            t.plant_name,
            t.plant_state,
            t.plant_county,
            t.sector_name,
            t.street_address,
            t.city,
            t.zip,
            t.plant_latitude,
            t.plant_longitude,
            t.primary_station_id,
            t.primary_station_name,
            t.primary_station_state,
            t.primary_station_country,
            t.primary_station_distance_km,
            t.primary_station_rank_order,
            c.fallback_station_id,
            c.fallback_station_name,
            c.fallback_station_state,
            c.fallback_station_country,
            c.fallback_station_distance_km,
            c.fallback_station_rank_order,
            c.fallback_station_ecwt_f,
            c.fallback_station_ecwt_discrete_f,
            t.policy_expected_hour_count,
            count(*)::bigint as generated_expected_hour_count,
            ceil(count(*)::numeric * {coverage_threshold})::bigint as required_valid_hour_count,
            t.policy_primary_valid_hour_count,
            count(ph.dry_bulb_f)::bigint as recomputed_primary_valid_hour_count,
            count(fh.dry_bulb_f) filter (
                where ph.dry_bulb_f is null
                  and fh.dry_bulb_f is not null
            )::bigint as fallback_fill_hour_count,
            count(fh.dry_bulb_f) filter (
                where ph.dry_bulb_f is not null
                  and fh.dry_bulb_f is not null
            )::bigint as fallback_overlap_valid_hour_count,
            count(fh.dry_bulb_f)::bigint as fallback_standalone_valid_hour_count,
            count(coalesce(ph.dry_bulb_f, fh.dry_bulb_f))::bigint as composite_valid_hour_count,
            t.policy_primary_coverage_ratio,
            count(ph.dry_bulb_f)::numeric / nullif(count(*), 0)::numeric as recomputed_primary_coverage_ratio,
            count(coalesce(ph.dry_bulb_f, fh.dry_bulb_f))::numeric / nullif(count(*), 0)::numeric as composite_coverage_ratio,
            (
                count(coalesce(ph.dry_bulb_f, fh.dry_bulb_f))::numeric
                - count(ph.dry_bulb_f)::numeric
            ) / nullif(count(*), 0)::numeric as coverage_gain_ratio,
            t.primary_ecwt_f,
            percentile_cont({percentile_target}) within group (
                order by coalesce(ph.dry_bulb_f, fh.dry_bulb_f)::double precision
            ) filter (
                where coalesce(ph.dry_bulb_f, fh.dry_bulb_f) is not null
            )::numeric as composite_ecwt_f,
            percentile_disc({percentile_target}) within group (
                order by coalesce(ph.dry_bulb_f, fh.dry_bulb_f)
            ) filter (
                where coalesce(ph.dry_bulb_f, fh.dry_bulb_f) is not null
            )::numeric as composite_ecwt_discrete_f
        from target_with_years t
        join candidate c using (plant_id)
        join expected_hour eh using (plant_id)
        left join weather.hourly_djf ph
          on ph.station_id = t.primary_station_id
         and ph.hour_ending_utc = eh.hour_ending_utc
         and ph.dry_bulb_f is not null
        left join weather.hourly_djf fh
          on fh.station_id = c.fallback_station_id
         and fh.hour_ending_utc = eh.hour_ending_utc
         and fh.dry_bulb_f is not null
        group by
            t.plant_id,
            t.eia_plant_code,
            t.plant_name,
            t.plant_state,
            t.plant_county,
            t.sector_name,
            t.street_address,
            t.city,
            t.zip,
            t.plant_latitude,
            t.plant_longitude,
            t.primary_station_id,
            t.primary_station_name,
            t.primary_station_state,
            t.primary_station_country,
            t.primary_station_distance_km,
            t.primary_station_rank_order,
            t.primary_ecwt_f,
            t.policy_primary_valid_hour_count,
            t.policy_expected_hour_count,
            t.policy_primary_coverage_ratio,
            c.fallback_station_id,
            c.fallback_station_name,
            c.fallback_station_state,
            c.fallback_station_country,
            c.fallback_station_distance_km,
            c.fallback_station_rank_order,
            c.fallback_station_ecwt_f,
            c.fallback_station_ecwt_discrete_f
    ),
    classified as (
        select
            score.*,
            count(*) over (partition by plant_id)::integer as candidate_count,
            count(*) filter (
                where generated_expected_hour_count = policy_expected_hour_count
                  and recomputed_primary_valid_hour_count = policy_primary_valid_hour_count
                  and fallback_fill_hour_count > 0
                  and composite_valid_hour_count >= required_valid_hour_count
            ) over (partition by plant_id)::integer as passing_candidate_count,
            case
                when generated_expected_hour_count <> policy_expected_hour_count then 'blocked_denominator_mismatch'
                when recomputed_primary_valid_hour_count <> policy_primary_valid_hour_count then 'blocked_primary_count_mismatch'
                when fallback_fill_hour_count = 0 then 'blocked_no_missing_hours_filled'
                when composite_valid_hour_count >= required_valid_hour_count then 'passes_composite_fill'
                else 'blocked_composite_below_threshold'
            end as fill_status,
            case
                when generated_expected_hour_count = policy_expected_hour_count
                  and recomputed_primary_valid_hour_count = policy_primary_valid_hour_count
                  and fallback_fill_hour_count > 0
                  and composite_valid_hour_count >= required_valid_hour_count
                then row_number() over (
                    partition by plant_id,
                    (
                        generated_expected_hour_count = policy_expected_hour_count
                        and recomputed_primary_valid_hour_count = policy_primary_valid_hour_count
                        and fallback_fill_hour_count > 0
                        and composite_valid_hour_count >= required_valid_hour_count
                    )
                    order by fallback_station_distance_km nulls last, fallback_station_rank_order nulls last, fallback_station_id
                )
                else null
            end as distance_rank_among_passing
        from score
    )
    select
        secondary_fill_run_id,
        policy_result_run_id,
        station_candidate_run_id,
        station_ecwt_run_id,
        plant_id,
        eia_plant_code,
        plant_name,
        plant_state,
        plant_county,
        sector_name,
        street_address,
        city,
        zip,
        plant_latitude,
        plant_longitude,
        primary_station_id,
        primary_station_name,
        primary_station_state,
        primary_station_country,
        primary_station_distance_km,
        primary_station_rank_order,
        fallback_station_id,
        fallback_station_name,
        fallback_station_state,
        fallback_station_country,
        fallback_station_distance_km,
        fallback_station_rank_order,
        fallback_station_ecwt_f,
        fallback_station_ecwt_discrete_f,
        policy_expected_hour_count,
        generated_expected_hour_count,
        required_valid_hour_count,
        policy_primary_valid_hour_count,
        recomputed_primary_valid_hour_count,
        fallback_fill_hour_count,
        fallback_overlap_valid_hour_count,
        fallback_standalone_valid_hour_count,
        composite_valid_hour_count,
        policy_primary_coverage_ratio,
        recomputed_primary_coverage_ratio,
        composite_coverage_ratio,
        coverage_gain_ratio,
        primary_ecwt_f,
        composite_ecwt_f,
        composite_ecwt_discrete_f,
        fill_status,
        distance_rank_among_passing,
        case
            when fill_status = 'passes_composite_fill'
                then 'Composite uses primary station when valid and fills only missing primary hours from fallback station.'
            when fill_status = 'blocked_denominator_mismatch'
                then 'Generated UTC DJF expected-hour count does not match policy row expected-hour count.'
            when fill_status = 'blocked_primary_count_mismatch'
                then 'Recomputed primary valid-hour count does not match policy row valid-hour count.'
            when fill_status = 'blocked_no_missing_hours_filled'
                then 'Fallback station does not add any valid observations where the primary station is missing.'
            else 'Composite valid-hour count remains below the publication threshold.'
        end as notes
    from classified
    order by plant_state, eia_plant_code::integer, fallback_station_distance_km nulls last, fallback_station_rank_order nulls last, fallback_station_id
    """


def select_best_rows(run_id: str, score_rows: list[dict[str, str]], percentile_target: float) -> list[dict[str, object]]:
    by_plant: OrderedDict[str, list[dict[str, str]]] = OrderedDict()
    for row in score_rows:
        by_plant.setdefault(row["plant_id"], []).append(row)

    best_rows: list[dict[str, object]] = []
    for plant_id, rows in by_plant.items():
        passing = [
            row
            for row in rows
            if row["fill_status"] == "passes_composite_fill" and row.get("distance_rank_among_passing") == "1"
        ]
        if passing:
            chosen = passing[0]
        else:
            chosen = sorted(
                rows,
                key=lambda row: (
                    row["fill_status"] != "passes_composite_fill",
                    float(row["fallback_station_distance_km"] or "inf"),
                    int(float(row["fallback_station_rank_order"] or "999999")),
                    row["fallback_station_id"],
                ),
            )[0]
        best = {field: chosen.get(field, "") for field in BEST_FIELDS if field not in {"secondary_fill_id", "percentile_target", "chosen_passing_distance_rank"}}
        best["secondary_fill_id"] = f"{run_id}:plant:{plant_id}"
        best["percentile_target"] = f"{percentile_target:.6f}"
        best["chosen_passing_distance_rank"] = chosen.get("distance_rank_among_passing", "")
        best_rows.append(best)
    return best_rows


def render_report(
    path: Path,
    run_id: str,
    policy_result_run_id: str,
    station_candidate_run_id: str,
    station_ecwt_run_id: str,
    coverage_threshold: float,
    percentile_target: float,
    score_rows: list[dict[str, str]],
    best_rows: list[dict[str, object]],
    plants_csv: Path,
    scores_csv: Path,
    host: str,
    port: int,
    dbname: str,
) -> None:
    status_counts = Counter(row["fill_status"] for row in score_rows)
    best_status_counts = Counter(str(row["fill_status"]) for row in best_rows)
    lines = [
        "# Secondary Station Fill ECWT",
        "",
        f"- Calculation run ID: `{run_id}`",
        f"- Policy result run ID: `{policy_result_run_id}`",
        f"- Station candidate run ID: `{station_candidate_run_id}`",
        f"- Station ECWT run ID: `{station_ecwt_run_id}`",
        f"- Database: `{dbname}` on `{host}:{port}`",
        f"- Coverage threshold: `{coverage_threshold:.6f}`",
        f"- Percentile target: `{percentile_target:.6f}`",
        f"- Selected fallback rows: `{plants_csv}`",
        f"- Candidate score audit: `{scores_csv}`",
        "",
        "## Method",
        "",
        "The selected primary station remains the representative station. For each fallback candidate, the calculation builds the UTC DJF expected-hour set for the primary station's loaded-year window, uses the primary dry-bulb value wherever it exists, fills only missing primary hours from the fallback station, and recalculates ECWT on that composite series.",
        "",
        "The chosen fallback is the nearest candidate station that satisfies all of these checks:",
        "",
        "1. generated expected hours equal the policy-result expected hours",
        "2. recomputed primary valid hours equal the policy-result primary valid hours",
        "3. fallback adds at least one valid missing primary hour",
        "4. composite valid hours meet or exceed the coverage threshold",
        "",
        "## Selected Rows",
        "",
        "| EIA Plant | Plant | Primary Station | Fallback Station | Filled Hours | Composite Coverage | Composite ECWT F | Status |",
        "| ---: | --- | --- | --- | ---: | ---: | ---: | --- |",
    ]
    for row in best_rows:
        lines.append(
            "| {code} | {plant} | `{primary}` | `{fallback}` | {filled} | {coverage} | {ecwt} | `{status}` |".format(
                code=row.get("eia_plant_code", ""),
                plant=str(row.get("plant_name", "")).replace("|", "\\|"),
                primary=row.get("primary_station_id", ""),
                fallback=row.get("fallback_station_id", ""),
                filled=row.get("fallback_fill_hour_count", ""),
                coverage=row.get("composite_coverage_ratio", ""),
                ecwt=row.get("composite_ecwt_f", ""),
                status=row.get("fill_status", ""),
            )
        )
    lines.extend(
        [
            "",
            "## Best-Row Status Counts",
            "",
            "| Status | Plants |",
            "| --- | ---: |",
        ]
    )
    for status, count in sorted(best_status_counts.items()):
        lines.append(f"| `{status}` | {count} |")
    lines.extend(
        [
            "",
            "## Candidate Score Counts",
            "",
            "| Status | Candidate Rows |",
            "| --- | ---: |",
        ]
    )
    for status, count in sorted(status_counts.items()):
        lines.append(f"| `{status}` | {count} |")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def create_load_sql(
    run_id: str,
    started_at: datetime,
    finished_at: datetime,
    code_commit: str,
    source_file_id: str,
    plants_csv: Path,
    source_sha: str,
    policy_result_run_id: str,
    station_candidate_run_id: str,
    station_ecwt_run_id: str,
    parameters: dict[str, object],
) -> str:
    text_columns = ",\n    ".join(f"{field} text" for field in BEST_FIELDS)
    copy_fields = ", ".join(BEST_FIELDS)
    insert_fields = [
        "secondary_fill_id",
        "secondary_fill_run_id",
        "policy_result_run_id",
        "station_candidate_run_id",
        "station_ecwt_run_id",
        "source_file_id",
        "plant_id",
        "eia_plant_code",
        "plant_name",
        "plant_state",
        "plant_county",
        "sector_name",
        "street_address",
        "city",
        "zip",
        "plant_latitude",
        "plant_longitude",
        "primary_station_id",
        "primary_station_name",
        "primary_station_state",
        "primary_station_country",
        "primary_station_distance_km",
        "primary_station_rank_order",
        "fallback_station_id",
        "fallback_station_name",
        "fallback_station_state",
        "fallback_station_country",
        "fallback_station_distance_km",
        "fallback_station_rank_order",
        "fallback_station_ecwt_f",
        "fallback_station_ecwt_discrete_f",
        "policy_expected_hour_count",
        "generated_expected_hour_count",
        "required_valid_hour_count",
        "policy_primary_valid_hour_count",
        "recomputed_primary_valid_hour_count",
        "fallback_fill_hour_count",
        "fallback_overlap_valid_hour_count",
        "fallback_standalone_valid_hour_count",
        "composite_valid_hour_count",
        "policy_primary_coverage_ratio",
        "recomputed_primary_coverage_ratio",
        "composite_coverage_ratio",
        "coverage_gain_ratio",
        "primary_ecwt_f",
        "composite_ecwt_f",
        "composite_ecwt_discrete_f",
        "percentile_target",
        "candidate_count",
        "passing_candidate_count",
        "chosen_passing_distance_rank",
        "fill_status",
        "notes",
    ]
    update_assignments = ",\n        ".join(
        f"{field} = excluded.{field}" for field in insert_fields if field != "secondary_fill_id"
    )
    return f"""
begin;

insert into audit.source_file (
    source_file_id,
    source_family,
    local_path,
    file_name,
    size_bytes,
    sha256,
    retrieved_at_utc,
    source_release,
    notes
) values (
    {sql_literal(source_file_id)},
    {sql_literal(SOURCE_FAMILY)},
    {sql_literal(str(plants_csv))},
    {sql_literal(plants_csv.name)},
    {plants_csv.stat().st_size},
    {sql_literal(source_sha)},
    {sql_literal(datetime.fromtimestamp(plants_csv.stat().st_mtime, timezone.utc).isoformat())}::timestamptz,
    {sql_literal(run_id)},
    'Generated secondary-station fill ECWT selected rows.'
) on conflict (source_file_id) do update set
    local_path = excluded.local_path,
    size_bytes = excluded.size_bytes,
    sha256 = excluded.sha256,
    retrieved_at_utc = excluded.retrieved_at_utc,
    notes = excluded.notes;

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
    {sql_literal(started_at.isoformat())}::timestamptz,
    {sql_literal(finished_at.isoformat())}::timestamptz,
    'succeeded',
    {sql_literal(json.dumps(parameters, sort_keys=True))}::jsonb,
    'Secondary station fill ECWT calculation for near-threshold policy-result blockers.'
) on conflict (calculation_run_id) do update set
    code_commit = excluded.code_commit,
    run_finished_at_utc = excluded.run_finished_at_utc,
    run_status = excluded.run_status,
    parameters_json = excluded.parameters_json,
    notes = excluded.notes;

create table if not exists calc.plant_ecwt_secondary_fill (
    secondary_fill_id text primary key,
    secondary_fill_run_id text not null references audit.calculation_run(calculation_run_id),
    policy_result_run_id text not null references audit.calculation_run(calculation_run_id),
    station_candidate_run_id text not null references audit.calculation_run(calculation_run_id),
    station_ecwt_run_id text not null references audit.calculation_run(calculation_run_id),
    source_file_id text references audit.source_file(source_file_id),
    plant_id text not null references asset.plant(plant_id),
    eia_plant_code text,
    plant_name text,
    plant_state text,
    plant_county text,
    sector_name text,
    street_address text,
    city text,
    zip text,
    plant_latitude numeric,
    plant_longitude numeric,
    primary_station_id text references weather.station(station_id),
    primary_station_name text,
    primary_station_state text,
    primary_station_country text,
    primary_station_distance_km numeric,
    primary_station_rank_order integer,
    fallback_station_id text references weather.station(station_id),
    fallback_station_name text,
    fallback_station_state text,
    fallback_station_country text,
    fallback_station_distance_km numeric,
    fallback_station_rank_order integer,
    fallback_station_ecwt_f numeric,
    fallback_station_ecwt_discrete_f numeric,
    policy_expected_hour_count bigint,
    generated_expected_hour_count bigint,
    required_valid_hour_count bigint,
    policy_primary_valid_hour_count bigint,
    recomputed_primary_valid_hour_count bigint,
    fallback_fill_hour_count bigint,
    fallback_overlap_valid_hour_count bigint,
    fallback_standalone_valid_hour_count bigint,
    composite_valid_hour_count bigint,
    policy_primary_coverage_ratio numeric,
    recomputed_primary_coverage_ratio numeric,
    composite_coverage_ratio numeric,
    coverage_gain_ratio numeric,
    primary_ecwt_f numeric,
    composite_ecwt_f numeric,
    composite_ecwt_discrete_f numeric,
    percentile_target numeric not null,
    candidate_count integer,
    passing_candidate_count integer,
    chosen_passing_distance_rank integer,
    fill_status text not null,
    notes text,
    created_at_utc timestamp with time zone not null default now(),
    unique (secondary_fill_run_id, plant_id)
);

create index if not exists ix_plant_ecwt_secondary_fill_run_status
    on calc.plant_ecwt_secondary_fill (secondary_fill_run_id, fill_status);
create index if not exists ix_plant_ecwt_secondary_fill_policy_plant
    on calc.plant_ecwt_secondary_fill (policy_result_run_id, plant_id);

create temp table tmp_secondary_station_fill (
    {text_columns}
) on commit drop;

\\copy tmp_secondary_station_fill ({copy_fields}) from {sql_literal(str(plants_csv))} with (format csv, header true, null '\\N')

insert into calc.plant_ecwt_secondary_fill (
    {", ".join(insert_fields)}
) select
    secondary_fill_id,
    secondary_fill_run_id,
    policy_result_run_id,
    station_candidate_run_id,
    station_ecwt_run_id,
    {sql_literal(source_file_id)} as source_file_id,
    plant_id,
    eia_plant_code,
    plant_name,
    plant_state,
    plant_county,
    sector_name,
    street_address,
    city,
    zip,
    nullif(plant_latitude, '')::numeric,
    nullif(plant_longitude, '')::numeric,
    primary_station_id,
    primary_station_name,
    nullif(primary_station_state, ''),
    nullif(primary_station_country, ''),
    nullif(primary_station_distance_km, '')::numeric,
    nullif(primary_station_rank_order, '')::integer,
    fallback_station_id,
    fallback_station_name,
    nullif(fallback_station_state, ''),
    nullif(fallback_station_country, ''),
    nullif(fallback_station_distance_km, '')::numeric,
    nullif(fallback_station_rank_order, '')::integer,
    nullif(fallback_station_ecwt_f, '')::numeric,
    nullif(fallback_station_ecwt_discrete_f, '')::numeric,
    nullif(policy_expected_hour_count, '')::bigint,
    nullif(generated_expected_hour_count, '')::bigint,
    nullif(required_valid_hour_count, '')::bigint,
    nullif(policy_primary_valid_hour_count, '')::bigint,
    nullif(recomputed_primary_valid_hour_count, '')::bigint,
    nullif(fallback_fill_hour_count, '')::bigint,
    nullif(fallback_overlap_valid_hour_count, '')::bigint,
    nullif(fallback_standalone_valid_hour_count, '')::bigint,
    nullif(composite_valid_hour_count, '')::bigint,
    nullif(policy_primary_coverage_ratio, '')::numeric,
    nullif(recomputed_primary_coverage_ratio, '')::numeric,
    nullif(composite_coverage_ratio, '')::numeric,
    nullif(coverage_gain_ratio, '')::numeric,
    nullif(primary_ecwt_f, '')::numeric,
    nullif(composite_ecwt_f, '')::numeric,
    nullif(composite_ecwt_discrete_f, '')::numeric,
    nullif(percentile_target, '')::numeric,
    nullif(candidate_count, '')::integer,
    nullif(passing_candidate_count, '')::integer,
    nullif(chosen_passing_distance_rank, '')::integer,
    fill_status,
    notes
from tmp_secondary_station_fill
on conflict (secondary_fill_id) do update set
    {update_assignments};

commit;
"""


def load_best_rows(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    load_sql: str,
    plants_csv: Path,
) -> None:
    _ = plants_csv
    run(psql_cmd(psql, host, port, dbname, user), input_text=load_sql)


def db_counts(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    run_id: str,
) -> list[dict[str, str]]:
    return psql_csv_query(
        psql,
        host,
        port,
        dbname,
        user,
        f"""
        select fill_status, count(*) as plant_count
        from calc.plant_ecwt_secondary_fill
        where secondary_fill_run_id = {sql_literal(run_id)}
        group by fill_status
        order by fill_status
        """,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--psql", type=Path, default=PSQL)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5436)
    parser.add_argument("--dbname", default="eop012")
    parser.add_argument("--user", default=None)
    parser.add_argument("--policy-result-run-id")
    parser.add_argument("--station-candidate-run-id")
    parser.add_argument("--station-ecwt-run-id")
    parser.add_argument("--coverage-threshold", type=float, default=0.95)
    parser.add_argument("--percentile-target", type=float, default=0.002)
    parser.add_argument("--plant-code", action="append", default=[])
    parser.add_argument("--max-candidates-per-plant", type=int, default=100)
    parser.add_argument("--include-ak", action="store_true")
    parser.add_argument("--no-load", action="store_true")
    args = parser.parse_args()

    started_at = utc_now()
    timestamp = started_at.strftime("%Y%m%dT%H%M%SZ")
    run_id = f"secondary_station_fill_ecwt_{timestamp}"
    policy_result_run_id = args.policy_result_run_id or latest_successful_run_id(
        args.psql, args.host, args.port, args.dbname, args.user, DEFAULT_POLICY_PREFIX
    )
    station_candidate_run_id = args.station_candidate_run_id or latest_successful_run_id(
        args.psql, args.host, args.port, args.dbname, args.user, DEFAULT_CANDIDATE_PREFIX
    )
    station_ecwt_run_id = args.station_ecwt_run_id or latest_successful_run_id(
        args.psql, args.host, args.port, args.dbname, args.user, DEFAULT_STATION_ECWT_PREFIX
    )

    query = score_query(
        run_id,
        policy_result_run_id,
        station_candidate_run_id,
        station_ecwt_run_id,
        args.coverage_threshold,
        args.percentile_target,
        args.include_ak,
        args.plant_code,
        args.max_candidates_per_plant,
    )
    score_rows = psql_csv_query(args.psql, args.host, args.port, args.dbname, args.user, query)
    if not score_rows:
        raise RuntimeError("No target rows found for secondary-station fill analysis.")
    best_rows = select_best_rows(run_id, score_rows, args.percentile_target)

    docs_dir = args.project_root / "docs"
    plants_csv = docs_dir / f"{run_id}_plants.csv"
    scores_csv = docs_dir / f"{run_id}_candidate_scores.csv"
    report_path = docs_dir / f"{run_id}_report.md"
    write_csv(plants_csv, BEST_FIELDS, best_rows)
    write_csv(scores_csv, SCORE_FIELDS, score_rows)

    render_report(
        report_path,
        run_id,
        policy_result_run_id,
        station_candidate_run_id,
        station_ecwt_run_id,
        args.coverage_threshold,
        args.percentile_target,
        score_rows,
        best_rows,
        plants_csv,
        scores_csv,
        args.host,
        args.port,
        args.dbname,
    )

    finished_at = utc_now()
    source_sha = sha256_file(plants_csv)
    source_file_id = f"{SOURCE_FAMILY}:{source_sha[:16]}"
    parameters = OrderedDict(
        [
            ("policy_result_run_id", policy_result_run_id),
            ("station_candidate_run_id", station_candidate_run_id),
            ("station_ecwt_run_id", station_ecwt_run_id),
            ("coverage_threshold", args.coverage_threshold),
            ("percentile_target", args.percentile_target),
            ("plant_code", args.plant_code),
            ("max_candidates_per_plant", args.max_candidates_per_plant),
            ("include_ak", args.include_ak),
        ]
    )
    if not args.no_load:
        load_sql = create_load_sql(
            run_id,
            started_at,
            finished_at,
            git_commit_label(args.project_root),
            source_file_id,
            plants_csv,
            source_sha,
            policy_result_run_id,
            station_candidate_run_id,
            station_ecwt_run_id,
            parameters,
        )
        load_best_rows(args.psql, args.host, args.port, args.dbname, args.user, load_sql, plants_csv)
        counts = db_counts(args.psql, args.host, args.port, args.dbname, args.user, run_id)
    else:
        counts = []

    result = {
        "run_id": run_id,
        "policy_result_run_id": policy_result_run_id,
        "station_candidate_run_id": station_candidate_run_id,
        "station_ecwt_run_id": station_ecwt_run_id,
        "target_plants": len(best_rows),
        "candidate_scores": len(score_rows),
        "best_status_counts": dict(Counter(str(row["fill_status"]) for row in best_rows)),
        "plants_csv": str(plants_csv),
        "scores_csv": str(scores_csv),
        "report_path": str(report_path),
        "db_counts": counts,
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
