#!/usr/bin/env python3
"""Export the current scoped plant ECWT dataset with secondary-fill rows included."""

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


DEFAULT_POLICY_PREFIX = "plant_ecwt_policy_result_all_plants_fixed_period_current_gate_"
DEFAULT_SECONDARY_PREFIX = "secondary_station_fill_ecwt_"
DEFAULT_STATION_ECWT_PREFIX = "station_ecwt_loaded_"

EXPORT_FIELDS = [
    "release_id",
    "publication_scope",
    "method_source",
    "policy_result_run_id",
    "secondary_fill_run_id",
    "station_ecwt_run_id",
    "plant_id",
    "eia_plant_code",
    "plant_name",
    "utility_id",
    "utility_name",
    "plant_state",
    "plant_county",
    "plant_latitude",
    "plant_longitude",
    "nerc_region",
    "balancing_authority_code",
    "balancing_authority_name",
    "sector_name",
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
    "ecwt_f",
    "ecwt_discrete_f",
    "valid_hour_count",
    "expected_hour_count",
    "missing_hour_count",
    "coverage_ratio",
    "coverage_basis",
    "percentile_target",
    "ecwt_precision_basis",
    "selected_station_representativeness_basis",
    "publication_caveat",
    "readiness_status",
    "reason_code",
    "notes",
]

EXCLUSION_FIELDS = [
    "release_id",
    "policy_result_run_id",
    "exclusion_reason",
    "plant_id",
    "eia_plant_code",
    "plant_name",
    "utility_id",
    "utility_name",
    "plant_state",
    "plant_county",
    "street_address",
    "city",
    "zip",
    "plant_latitude",
    "plant_longitude",
    "readiness_status",
    "reason_code",
    "notes",
]


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def sql_literal(value: object) -> str:
    if value is None:
        return "null"
    return "'" + str(value).replace("'", "''") + "'"


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(cmd, text=True, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
            writer.writerow({field: row.get(field, "") for field in fieldnames})


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
        limit 1
        """,
    )
    if not run_id:
        raise RuntimeError(f"No succeeded calculation run found with prefix {prefix!r}.")
    return run_id


def export_query(
    release_id: str,
    policy_result_run_id: str,
    secondary_fill_run_id: str,
    station_ecwt_run_id: str,
) -> str:
    return f"""
    with base_policy as (
        select
            {sql_literal(release_id)}::text as release_id,
            'non_ak_no_station_excluded'::text as publication_scope,
            'policy_result'::text as method_source,
            pr.policy_result_run_id,
            null::text as secondary_fill_run_id,
            {sql_literal(station_ecwt_run_id)}::text as station_ecwt_run_id,
            pr.plant_id,
            pr.eia_plant_code,
            pr.plant_name,
            p.utility_id,
            p.utility_name,
            pr.plant_state,
            pr.plant_county,
            round(p.latitude, 6)::text as plant_latitude,
            round(p.longitude, 6)::text as plant_longitude,
            p.nerc_region,
            p.balancing_authority_code,
            p.balancing_authority_name,
            pr.sector_name,
            pr.selected_station_id as primary_station_id,
            pr.selected_station_name as primary_station_name,
            pr.selected_station_state as primary_station_state,
            pr.selected_station_country as primary_station_country,
            round(pr.selected_station_distance_km, 3)::text as primary_station_distance_km,
            pr.selected_station_rank_order::text as primary_station_rank_order,
            null::text as fallback_station_id,
            null::text as fallback_station_name,
            null::text as fallback_station_state,
            null::text as fallback_station_country,
            null::text as fallback_station_distance_km,
            null::text as fallback_station_rank_order,
            round(pr.ecwt_f, 1)::text as ecwt_f,
            round(se.ecwt_discrete_f, 1)::text as ecwt_discrete_f,
            pr.valid_hour_count::text as valid_hour_count,
            pr.expected_hour_count::text as expected_hour_count,
            greatest(pr.expected_hour_count - pr.valid_hour_count, 0)::text as missing_hour_count,
            round(pr.coverage_ratio, 6)::text as coverage_ratio,
            'fixed_period_station_local_djf_2000_to_calculation_cutoff'::text as coverage_basis,
            '0.002'::text as percentile_target,
            'rounded_to_0.1_f_due_to_noaa_tmp_tenths_c_source_resolution'::text as ecwt_precision_basis,
            'automated_gate_distance_100km_elevation_300m_fixed_coverage_0.95'::text
                as selected_station_representativeness_basis,
            'Analytical plant-level ECWT output; not a Generator Owner EOP-012 compliance filing input without station representativeness review and source QA acceptance.'::text
                as publication_caveat,
            pr.readiness_status,
            pr.reason_code,
            pr.notes
        from calc.plant_ecwt_policy_result pr
        join asset.plant p using (plant_id)
        left join calc.station_ecwt se
          on se.calculation_run_id = {sql_literal(station_ecwt_run_id)}
         and se.station_id = pr.selected_station_id
        where pr.policy_result_run_id = {sql_literal(policy_result_run_id)}
          and pr.plant_state <> 'AK'
          and pr.readiness_status = 'publication_candidate'
    ),
    secondary_fill as (
        select
            {sql_literal(release_id)}::text as release_id,
            'non_ak_no_station_excluded'::text as publication_scope,
            'secondary_station_fill'::text as method_source,
            sf.policy_result_run_id,
            sf.secondary_fill_run_id,
            sf.station_ecwt_run_id,
            sf.plant_id,
            sf.eia_plant_code,
            sf.plant_name,
            p.utility_id,
            p.utility_name,
            sf.plant_state,
            sf.plant_county,
            round(p.latitude, 6)::text as plant_latitude,
            round(p.longitude, 6)::text as plant_longitude,
            p.nerc_region,
            p.balancing_authority_code,
            p.balancing_authority_name,
            sf.sector_name,
            sf.primary_station_id,
            sf.primary_station_name,
            sf.primary_station_state,
            sf.primary_station_country,
            round(sf.primary_station_distance_km, 3)::text as primary_station_distance_km,
            sf.primary_station_rank_order::text as primary_station_rank_order,
            sf.fallback_station_id,
            sf.fallback_station_name,
            sf.fallback_station_state,
            sf.fallback_station_country,
            round(sf.fallback_station_distance_km, 3)::text as fallback_station_distance_km,
            sf.fallback_station_rank_order::text as fallback_station_rank_order,
            round(sf.composite_ecwt_f, 1)::text as ecwt_f,
            round(sf.composite_ecwt_discrete_f, 1)::text as ecwt_discrete_f,
            sf.composite_valid_hour_count::text as valid_hour_count,
            sf.generated_expected_hour_count::text as expected_hour_count,
            greatest(sf.generated_expected_hour_count - sf.composite_valid_hour_count, 0)::text as missing_hour_count,
            round(sf.composite_coverage_ratio, 6)::text as coverage_ratio,
            'fixed_period_station_local_djf_composite_2000_to_calculation_cutoff'::text as coverage_basis,
            sf.percentile_target::text as percentile_target,
            'rounded_to_0.1_f_due_to_noaa_tmp_tenths_c_source_resolution'::text as ecwt_precision_basis,
            'documented_secondary_station_fill_with_primary_station_retained'::text
                as selected_station_representativeness_basis,
            'Analytical plant-level ECWT output; secondary-fill rows require review of station representativeness, missing-hour treatment, and source QA before compliance use.'::text
                as publication_caveat,
            'publication_candidate'::text as readiness_status,
            'passes_secondary_station_fill'::text as reason_code,
            sf.notes
        from calc.plant_ecwt_secondary_fill sf
        join asset.plant p using (plant_id)
        where sf.secondary_fill_run_id = {sql_literal(secondary_fill_run_id)}
          and sf.fill_status = 'passes_composite_fill'
    )
    select *
    from (
        select *
        from base_policy
        union all
        select *
        from secondary_fill
    ) scoped_rows
    order by plant_state, eia_plant_code::integer nulls last, plant_name
    """


def exclusion_query(release_id: str, policy_result_run_id: str) -> str:
    return f"""
    select
        {sql_literal(release_id)}::text as release_id,
        pr.policy_result_run_id,
        case
            when pr.plant_state = 'AK' then 'alaska_excluded_by_scope'
            when pr.reason_code = 'no_station_candidates' then 'no_station_edge_case_excluded'
            else 'not_in_current_scope'
        end as exclusion_reason,
        pr.plant_id,
        pr.eia_plant_code,
        pr.plant_name,
        p.utility_id,
        p.utility_name,
        pr.plant_state,
        pr.plant_county,
        p.street_address,
        p.city,
        p.zip,
        round(p.latitude, 6)::text as plant_latitude,
        round(p.longitude, 6)::text as plant_longitude,
        pr.readiness_status,
        pr.reason_code,
        case
            when pr.plant_state = 'AK' then 'Excluded from current publication scope by user direction.'
            when pr.reason_code = 'no_station_candidates' then 'Excluded as nonphysical, unsited, unlocatable, or not first-operable under current review.'
            else pr.notes
        end as notes
    from calc.plant_ecwt_policy_result pr
    join asset.plant p using (plant_id)
    where pr.policy_result_run_id = {sql_literal(policy_result_run_id)}
      and (
        pr.plant_state = 'AK'
        or (
            pr.plant_state <> 'AK'
            and pr.readiness_status = 'blocked'
            and pr.reason_code = 'no_station_candidates'
        )
      )
    order by exclusion_reason, pr.plant_state, pr.eia_plant_code::integer nulls last, pr.plant_name
    """


def render_report(
    path: Path,
    release_id: str,
    policy_result_run_id: str,
    secondary_fill_run_id: str,
    station_ecwt_run_id: str,
    export_rows: list[dict[str, str]],
    exclusion_rows: list[dict[str, str]],
    export_csv: Path,
    exclusions_csv: Path,
) -> None:
    method_counts = Counter(row["method_source"] for row in export_rows)
    exclusion_counts = Counter(row["exclusion_reason"] for row in exclusion_rows)
    state_counts = Counter(row["plant_state"] for row in export_rows)
    lines = [
        "# Scoped Plant ECWT Dataset Export",
        "",
        f"- Release ID: `{release_id}`",
        f"- Policy result run ID: `{policy_result_run_id}`",
        f"- Secondary fill run ID: `{secondary_fill_run_id}`",
        f"- Station ECWT run ID: `{station_ecwt_run_id}`",
        f"- Dataset CSV: `{export_csv}`",
        f"- Exclusions CSV: `{exclusions_csv}`",
        "",
        "## Scope",
        "",
        "This export includes non-Alaska plant rows that are publication-ready under the fixed-period current gate, plus rows made publication-ready by the documented secondary-station fill method. It excludes Alaska and the reviewed no-station edge cases from the current publication denominator.",
        "",
        "ECWT values are rounded to 0.1 F because the NOAA Global Hourly TMP source field is stored in tenths of a degree C. Each exported row carries `coverage_basis`, `ecwt_precision_basis`, `selected_station_representativeness_basis`, and `publication_caveat` fields so downstream users see the audit caveats in the CSV itself.",
        "",
        "## Row Counts",
        "",
        "| Category | Rows |",
        "| --- | ---: |",
        f"| Exported scoped ready rows | {len(export_rows)} |",
        f"| Excluded rows | {len(exclusion_rows)} |",
        "",
        "## Export Method Counts",
        "",
        "| Method Source | Rows |",
        "| --- | ---: |",
    ]
    for method, count in sorted(method_counts.items()):
        lines.append(f"| `{method}` | {count} |")
    lines.extend(
        [
            "",
            "## Exclusion Counts",
            "",
            "| Exclusion Reason | Rows |",
            "| --- | ---: |",
        ]
    )
    for reason, count in sorted(exclusion_counts.items()):
        lines.append(f"| `{reason}` | {count} |")
    lines.extend(
        [
            "",
            "## Largest State Counts In Export",
            "",
            "| State | Rows |",
            "| --- | ---: |",
        ]
    )
    for state, count in state_counts.most_common(12):
        lines.append(f"| `{state}` | {count} |")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--psql", type=Path, default=PSQL)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5436)
    parser.add_argument("--dbname", default="eop012")
    parser.add_argument("--user", default=None)
    parser.add_argument("--policy-result-run-id")
    parser.add_argument("--secondary-fill-run-id")
    parser.add_argument("--station-ecwt-run-id")
    args = parser.parse_args()

    now = utc_now()
    release_id = f"scoped_plant_ecwt_release_{now.strftime('%Y%m%dT%H%M%SZ')}"
    policy_result_run_id = args.policy_result_run_id or latest_successful_run_id(
        args.psql, args.host, args.port, args.dbname, args.user, DEFAULT_POLICY_PREFIX
    )
    secondary_fill_run_id = args.secondary_fill_run_id or latest_successful_run_id(
        args.psql, args.host, args.port, args.dbname, args.user, DEFAULT_SECONDARY_PREFIX
    )
    station_ecwt_run_id = args.station_ecwt_run_id or latest_successful_run_id(
        args.psql, args.host, args.port, args.dbname, args.user, DEFAULT_STATION_ECWT_PREFIX
    )

    rows = psql_csv_query(
        args.psql,
        args.host,
        args.port,
        args.dbname,
        args.user,
        export_query(release_id, policy_result_run_id, secondary_fill_run_id, station_ecwt_run_id),
    )
    exclusions = psql_csv_query(
        args.psql,
        args.host,
        args.port,
        args.dbname,
        args.user,
        exclusion_query(release_id, policy_result_run_id),
    )
    if not rows:
        raise RuntimeError("Scoped export produced zero rows.")

    processed_dir = args.project_root / "data" / "processed"
    docs_dir = args.project_root / "docs"
    export_csv = processed_dir / f"{release_id}.csv"
    exclusions_csv = processed_dir / f"{release_id}_exclusions.csv"
    report_path = docs_dir / f"{release_id}_report.md"
    write_csv(export_csv, EXPORT_FIELDS, rows)
    write_csv(exclusions_csv, EXCLUSION_FIELDS, exclusions)
    render_report(
        report_path,
        release_id,
        policy_result_run_id,
        secondary_fill_run_id,
        station_ecwt_run_id,
        rows,
        exclusions,
        export_csv,
        exclusions_csv,
    )

    print(
        json.dumps(
            OrderedDict(
                [
                    ("release_id", release_id),
                    ("policy_result_run_id", policy_result_run_id),
                    ("secondary_fill_run_id", secondary_fill_run_id),
                    ("station_ecwt_run_id", station_ecwt_run_id),
                    ("export_rows", len(rows)),
                    ("exclusion_rows", len(exclusions)),
                    ("export_csv", str(export_csv)),
                    ("exclusions_csv", str(exclusions_csv)),
                    ("report_path", str(report_path)),
                ]
            ),
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
