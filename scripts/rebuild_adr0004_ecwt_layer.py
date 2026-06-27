#!/usr/bin/env python3
"""Rebuild the ADR-0004 observational plant ECWT layer.

This script deliberately wires the tested stdlib helpers in ecwt_core.py to the
existing Postgres data model. It does not re-derive ECWT math.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import subprocess
import sys
from collections import Counter, OrderedDict, defaultdict
from dataclasses import asdict
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Iterable, Iterator

from ecwt_core import (
    HourObs,
    assess_adequacy,
    build_composite,
    ecwt_discrete_rank_temp,
    ecwt_percentile,
    expected_djf_hours,
    provenance_summary,
)
from eop012_config import PROJECT_ROOT, PSQL


METHODOLOGY_VERSION = "eop012-ecwt-method-v0.4.0-adr0004"
DEFAULT_CANDIDATE_PREFIX = "noaa_station_candidates_"
SOURCE_CHANNELS = (
    "noaa_global_hourly_aws",
    "noaa_lcd_cdo",
    "asos_iem",
    "noaa_isd_local_cache",
)
COVERAGE_BASIS_PREFIX = "fixed-period DJF since 2000-01-01"
PUBLICATION_CAVEAT = (
    "Analytical plant-level ECWT output; not a Generator Owner EOP-012 "
    "compliance filing input without entity-specific representativeness review "
    "and source QA acceptance."
)

RESULT_FIELDS = [
    "adr0004_result_id",
    "adr0004_run_id",
    "release_id",
    "plant_id",
    "eia_plant_code",
    "plant_name",
    "plant_state",
    "plant_county",
    "primary_station_id",
    "primary_station_distance_km",
    "primary_station_rank_order",
    "calculation_date",
    "calculation_cutoff_utc",
    "valid_hour_count",
    "expected_hour_count",
    "missing_hour_count",
    "missing_frac",
    "coverage_ratio",
    "ecwt_f",
    "ecwt_c",
    "ecwt_discrete_f",
    "ecwt_discrete_c",
    "discrete_rank",
    "tail_hour_count",
    "confidence_tier",
    "needs_review",
    "reason",
    "coverage_basis",
    "gap_calendar_basis",
    "provenance_summary_json",
    "contributing_towers_json",
    "source_channels_json",
    "cold_tail_provenance_json",
    "publication_caveat",
]

SOURCE_FIELDS = [
    "adr0004_run_id",
    "plant_id",
    "station_id",
    "role",
    "fill_priority",
    "distance_km",
    "rank_order",
    "used_hour_count",
    "filled_hour_count",
]

COLD_TAIL_FIELDS = [
    "adr0004_run_id",
    "plant_id",
    "hour_ending_utc",
    "hour_local",
    "obs_timestamp",
    "station_id",
    "dry_bulb_f",
    "source_channel",
    "source_code",
    "report_type",
    "source_file_id",
    "filled",
]

RELEASE_FIELDS = [
    "release_id",
    "adr0004_run_id",
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
    "primary_station_distance_km",
    "primary_station_rank_order",
    "ecwt_f",
    "ecwt_discrete_f",
    "confidence_tier",
    "needs_review",
    "reason",
    "valid_hour_count",
    "expected_hour_count",
    "missing_hour_count",
    "missing_frac",
    "coverage_ratio",
    "coverage_basis",
    "contributing_towers",
    "source_channels",
    "filled_hour_count",
    "cold_tail_provenance",
    "publication_caveat",
]


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def sql_literal(value: object) -> str:
    if value is None:
        return "null"
    return "'" + str(value).replace("'", "''") + "'"


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


def psql_cmd(psql: Path, host: str, port: int, dbname: str, user: str | None) -> list[str]:
    cmd = [str(psql), "-h", host, "-p", str(port)]
    if user:
        cmd.extend(["-U", user])
    cmd.extend(["-d", dbname, "-v", "ON_ERROR_STOP=1"])
    return cmd


def psql_execute(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    sql: str,
) -> None:
    run(psql_cmd(psql, host, port, dbname, user), input_text=sql)


def psql_scalar(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    query: str,
) -> str:
    return run(psql_cmd(psql, host, port, dbname, user) + ["-At", "-c", query]).stdout.strip()


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


def psql_csv_stream(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    query: str,
) -> Iterator[dict[str, str]]:
    cmd = psql_cmd(psql, host, port, dbname, user) + [
        "-c",
        f"\\copy ({query}) to stdout with (format csv, header true)",
    ]
    proc = subprocess.Popen(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert proc.stdout is not None
    reader = csv.DictReader(proc.stdout)
    for row in reader:
        yield row
    stderr = proc.stderr.read() if proc.stderr is not None else ""
    code = proc.wait()
    if code != 0:
        raise RuntimeError(f"Streaming psql query failed with exit code {code}: {stderr}")


def write_csv_header(path: Path, fieldnames: list[str]) -> csv.DictWriter:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = path.open("w", newline="", encoding="utf-8")
    writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer._eop012_handle = handle  # type: ignore[attr-defined]
    return writer


def close_writer(writer: csv.DictWriter) -> None:
    handle = getattr(writer, "_eop012_handle", None)
    if handle is not None:
        handle.close()


def writerow(writer: csv.DictWriter, row: dict[str, object]) -> None:
    writer.writerow({field: pg_csv_value(row.get(field)) for field in writer.fieldnames or []})


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
        limit 1
        """,
    )
    if not run_id:
        raise RuntimeError(f"No succeeded calculation run found with prefix {prefix!r}.")
    return run_id


def max_loaded_calc_date(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
) -> date:
    value = psql_scalar(
        psql,
        host,
        port,
        dbname,
        user,
        "select max(max_hour_ending_utc)::date from weather.station_year_hourly_summary",
    )
    if not value:
        return date.today()
    return date.fromisoformat(value)


def ensure_schema(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
) -> None:
    enum_values = ", ".join(sql_literal(value) for value in SOURCE_CHANNELS)
    sql = f"""
do $$
begin
    if not exists (
        select 1
        from pg_type t
        join pg_namespace n on n.oid = t.typnamespace
        where n.nspname = 'weather'
          and t.typname = 'source_channel'
    ) then
        create type weather.source_channel as enum ({enum_values});
    end if;
end $$;

alter table weather.hourly_djf
    add column if not exists obs_timestamp timestamptz,
    add column if not exists source_channel weather.source_channel,
    add column if not exists source_code text,
    add column if not exists report_type text;

create index if not exists ix_weather_hourly_djf_source_file
    on weather.hourly_djf (source_file_id);
create index if not exists ix_weather_hourly_djf_source_channel
    on weather.hourly_djf (source_channel);
create index if not exists ix_noaa_hourly_load_file_source_file
    on weather.noaa_hourly_load_file (source_file_id);

create table if not exists calc.plant_ecwt_adr0004_result (
    adr0004_result_id text primary key,
    adr0004_run_id text not null references audit.calculation_run(calculation_run_id),
    release_id text,
    plant_id text not null references asset.plant(plant_id),
    eia_plant_code text,
    plant_name text,
    plant_state text,
    plant_county text,
    primary_station_id text references weather.station(station_id),
    primary_station_distance_km numeric,
    primary_station_rank_order integer,
    calculation_date date not null,
    calculation_cutoff_utc timestamptz,
    valid_hour_count bigint not null,
    expected_hour_count bigint not null,
    missing_hour_count bigint not null,
    missing_frac numeric,
    coverage_ratio numeric,
    ecwt_f numeric,
    ecwt_c numeric,
    ecwt_discrete_f numeric,
    ecwt_discrete_c numeric,
    discrete_rank integer,
    tail_hour_count bigint not null default 0,
    confidence_tier text not null,
    needs_review boolean not null,
    reason text not null,
    coverage_basis text not null,
    gap_calendar_basis text not null,
    provenance_summary jsonb not null default '{{}}'::jsonb,
    contributing_towers jsonb not null default '{{}}'::jsonb,
    source_channels jsonb not null default '{{}}'::jsonb,
    cold_tail_provenance jsonb not null default '{{}}'::jsonb,
    publication_caveat text not null,
    created_at_utc timestamptz not null default now(),
    unique (adr0004_run_id, plant_id),
    constraint plant_ecwt_adr0004_confidence_tier_check
        check (confidence_tier in ('complete', 'adequate', 'provisional_review', 'blocked_no_data'))
);

create index if not exists ix_plant_ecwt_adr0004_run_tier
    on calc.plant_ecwt_adr0004_result (adr0004_run_id, confidence_tier);
create index if not exists ix_plant_ecwt_adr0004_plant
    on calc.plant_ecwt_adr0004_result (plant_id);

create table if not exists calc.plant_ecwt_adr0004_source (
    adr0004_run_id text not null references audit.calculation_run(calculation_run_id),
    plant_id text not null references asset.plant(plant_id),
    station_id text not null references weather.station(station_id),
    role text not null,
    fill_priority integer not null,
    distance_km numeric,
    rank_order integer,
    used_hour_count bigint not null default 0,
    filled_hour_count bigint not null default 0,
    created_at_utc timestamptz not null default now(),
    primary key (adr0004_run_id, plant_id, station_id, fill_priority)
);

create index if not exists ix_plant_ecwt_adr0004_source_station
    on calc.plant_ecwt_adr0004_source (adr0004_run_id, station_id);

create table if not exists calc.plant_ecwt_adr0004_cold_tail_hour (
    adr0004_run_id text not null references audit.calculation_run(calculation_run_id),
    plant_id text not null references asset.plant(plant_id),
    hour_ending_utc timestamptz not null,
    hour_local timestamp,
    obs_timestamp timestamptz,
    station_id text not null references weather.station(station_id),
    dry_bulb_f numeric not null,
    source_channel weather.source_channel,
    source_code text,
    report_type text,
    source_file_id text references audit.source_file(source_file_id),
    filled boolean not null default false,
    created_at_utc timestamptz not null default now(),
    primary key (adr0004_run_id, plant_id, hour_ending_utc, station_id)
);

create index if not exists ix_plant_ecwt_adr0004_tail_plant
    on calc.plant_ecwt_adr0004_cold_tail_hour (adr0004_run_id, plant_id);
create index if not exists ix_plant_ecwt_adr0004_tail_source
    on calc.plant_ecwt_adr0004_cold_tail_hour (adr0004_run_id, source_channel, source_code);

create table if not exists calc.plant_ecwt_adr0004_summary (
    metric text primary key,
    metric_value text not null,
    adr0004_run_id text references audit.calculation_run(calculation_run_id),
    updated_at_utc timestamptz not null default now()
);

create or replace view calc.plant_ecwt_adr0004_composite_hour as
select
    src.adr0004_run_id,
    src.plant_id,
    h.station_id,
    h.hour_ending_utc,
    h.hour_local,
    coalesce(h.obs_timestamp, h.hour_ending_utc) as obs_timestamp,
    h.dry_bulb_f,
    coalesce(h.source_channel::text, 'noaa_isd_local_cache')::weather.source_channel as source_channel,
    coalesce(h.source_code, nullif(substring(array_to_string(h.quality_flags, '|') from 'source:([^|]*)'), '')) as source_code,
    coalesce(h.report_type, nullif(substring(array_to_string(h.quality_flags, '|') from 'report_type:([^|]*)'), '')) as report_type,
    h.source_file_id,
    (src.role <> 'primary') as filled,
    src.role,
    src.fill_priority
from calc.plant_ecwt_adr0004_source src
join weather.hourly_djf h
  on h.station_id = src.station_id
 and h.dry_bulb_f is not null
where not exists (
    select 1
    from calc.plant_ecwt_adr0004_source prior_src
    join weather.hourly_djf prior_h
      on prior_h.station_id = prior_src.station_id
     and prior_h.hour_ending_utc = h.hour_ending_utc
     and prior_h.dry_bulb_f is not null
    where prior_src.adr0004_run_id = src.adr0004_run_id
      and prior_src.plant_id = src.plant_id
      and prior_src.fill_priority < src.fill_priority
);
"""
    psql_execute(psql, host, port, dbname, user, sql)


def backfill_hourly_provenance(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
) -> None:
    sql = """
with load_source as (
    select source_file_id, min(source_basis) as source_basis
    from weather.noaa_hourly_load_file
    where source_file_id is not null
    group by source_file_id
),
source_meta as (
    select
        sf.source_file_id,
        sf.source_family,
        ls.source_basis
    from audit.source_file sf
    left join load_source ls
      on ls.source_file_id = sf.source_file_id
)
update weather.hourly_djf h
set
    obs_timestamp = coalesce(h.obs_timestamp, h.hour_ending_utc),
    source_code = coalesce(
        h.source_code,
        nullif(substring(array_to_string(h.quality_flags, '|') from 'source:([^|]*)'), '')
    ),
    report_type = coalesce(
        h.report_type,
        nullif(substring(array_to_string(h.quality_flags, '|') from 'report_type:([^|]*)'), '')
    ),
    source_channel = coalesce(
        h.source_channel,
        case
            when source_meta.source_basis = 'download_attempt' then 'noaa_global_hourly_aws'::weather.source_channel
            when source_meta.source_basis = 'inventory' then 'noaa_isd_local_cache'::weather.source_channel
            when source_meta.source_family = 'noaa_global_hourly_csv' then 'noaa_global_hourly_aws'::weather.source_channel
            when source_meta.source_family = 'noaa_global_hourly_local_raw_inventory' then 'noaa_isd_local_cache'::weather.source_channel
            else null
        end
    )
from source_meta
where h.source_file_id = source_meta.source_file_id
  and (
      h.obs_timestamp is null
      or h.source_code is null
      or h.report_type is null
      or h.source_channel is null
  );

update weather.hourly_djf
set obs_timestamp = hour_ending_utc
where obs_timestamp is null;
"""
    psql_execute(psql, host, port, dbname, user, sql)


def parse_float(value: str | None) -> float | None:
    if value in (None, "", r"\N"):
        return None
    return float(str(value))


def parse_int(value: str | None) -> int | None:
    if value in (None, "", r"\N"):
        return None
    return int(float(str(value)))


def load_targets(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    station_candidate_run_id: str,
    include_ak: bool,
    limit_plants: int | None = None,
) -> list[dict[str, str]]:
    state_filter = "true" if include_ak else "coalesce(p.state, '') <> 'AK'"
    limit_clause = "" if not limit_plants else f"limit {int(limit_plants)}"
    return psql_csv_query(
        psql,
        host,
        port,
        dbname,
        user,
        f"""
        with candidate_weather as (
            select
                sc.plant_id,
                sc.station_id,
                sc.distance_km,
                sc.rank_order,
                row_number() over (
                    partition by sc.plant_id
                    order by sc.rank_order nulls last, sc.distance_km nulls last, sc.station_id
                ) as rn
            from link.station_candidate sc
            where sc.calculation_run_id = {sql_literal(station_candidate_run_id)}
              and sc.candidate_status in ('candidate', 'selected')
              and exists (
                  select 1
                  from weather.station_year_hourly_summary sy
                  where sy.station_id = sc.station_id
                    and sy.valid_djf_hours > 0
              )
        )
        select
            p.plant_id,
            p.eia_plant_code,
            p.plant_name,
            coalesce(p.utility_id, '') as utility_id,
            coalesce(p.utility_name, '') as utility_name,
            coalesce(p.state, '') as plant_state,
            coalesce(p.county, '') as plant_county,
            coalesce(round(p.latitude, 6)::text, '') as plant_latitude,
            coalesce(round(p.longitude, 6)::text, '') as plant_longitude,
            coalesce(p.nerc_region, '') as nerc_region,
            coalesce(p.balancing_authority_code, '') as balancing_authority_code,
            coalesce(p.balancing_authority_name, '') as balancing_authority_name,
            coalesce(p.sector_name, '') as sector_name,
            coalesce(cw.station_id, '') as primary_station_id,
            coalesce(round(cw.distance_km, 3)::text, '') as primary_station_distance_km,
            coalesce(cw.rank_order::text, '') as primary_station_rank_order
        from asset.plant p
        left join candidate_weather cw
          on cw.plant_id = p.plant_id
         and cw.rn = 1
        where {state_filter}
        order by p.state, p.eia_plant_code::integer nulls last, p.plant_id
        {limit_clause}
        """,
    )


def observation_query(station_ids: Iterable[str]) -> str:
    station_list = ", ".join(sql_literal(station_id) for station_id in sorted(set(station_ids)))
    return f"""
    select
        h.station_id,
        h.hour_ending_utc::text as hour_ending_utc,
        coalesce(h.hour_local::text, '') as hour_local,
        coalesce(h.obs_timestamp::text, h.hour_ending_utc::text) as obs_timestamp,
        h.dry_bulb_f::double precision::text as dry_bulb_f,
        coalesce(h.source_channel::text, 'noaa_isd_local_cache') as source_channel,
        coalesce(h.source_code, nullif(substring(array_to_string(h.quality_flags, '|') from 'source:([^|]*)'), ''), '') as source_code,
        coalesce(h.report_type, nullif(substring(array_to_string(h.quality_flags, '|') from 'report_type:([^|]*)'), ''), '') as report_type,
        coalesce(h.source_file_id, '') as source_file_id
    from weather.hourly_djf h
    where h.station_id in ({station_list})
      and h.dry_bulb_f is not null
    order by h.station_id, h.hour_ending_utc
    """


def iter_station_observations(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    station_ids: Iterable[str],
) -> Iterator[tuple[str, list[HourObs], list[dict[str, str]]]]:
    current_station: str | None = None
    obs: list[HourObs] = []
    raw_rows: list[dict[str, str]] = []
    for row in psql_csv_stream(psql, host, port, dbname, user, observation_query(station_ids)):
        station_id = row["station_id"]
        if current_station is not None and station_id != current_station:
            yield current_station, obs, raw_rows
            obs = []
            raw_rows = []
        current_station = station_id
        raw_rows.append(row)
        obs.append(
            HourObs(
                row["hour_ending_utc"],
                float(row["dry_bulb_f"]),
                station_id,
                row["source_channel"] or "noaa_isd_local_cache",
                row.get("source_code") or "",
                row.get("report_type") or "",
                row.get("source_file_id") or None,
                False,
            )
        )
    if current_station is not None:
        yield current_station, obs, raw_rows


def ecwt_c_from_f(value: float | None) -> float | None:
    if value is None or math.isnan(value):
        return None
    return round((value - 32.0) * 5.0 / 9.0, 3)


def result_base(
    run_id: str,
    release_id: str,
    plant: dict[str, str],
    calc_date: date,
    expected_hours: int,
) -> OrderedDict[str, object]:
    return OrderedDict(
        [
            ("adr0004_result_id", f"{run_id}:plant:{plant['plant_id']}"),
            ("adr0004_run_id", run_id),
            ("release_id", release_id),
            ("plant_id", plant["plant_id"]),
            ("eia_plant_code", plant["eia_plant_code"]),
            ("plant_name", plant["plant_name"]),
            ("plant_state", plant["plant_state"]),
            ("plant_county", plant["plant_county"]),
            ("primary_station_id", plant.get("primary_station_id") or None),
            ("primary_station_distance_km", plant.get("primary_station_distance_km") or None),
            ("primary_station_rank_order", plant.get("primary_station_rank_order") or None),
            ("calculation_date", calc_date.isoformat()),
            ("calculation_cutoff_utc", None),
            ("valid_hour_count", 0),
            ("expected_hour_count", expected_hours),
            ("missing_hour_count", expected_hours),
            ("missing_frac", 1.0),
            ("coverage_ratio", 0.0),
            ("ecwt_f", None),
            ("ecwt_c", None),
            ("ecwt_discrete_f", None),
            ("ecwt_discrete_c", None),
            ("discrete_rank", None),
            ("tail_hour_count", 0),
            ("confidence_tier", "blocked_no_data"),
            ("needs_review", True),
            ("reason", "no candidate station with valid observed DJF data"),
            ("coverage_basis", f"{COVERAGE_BASIS_PREFIX} through {calc_date.isoformat()}"),
            ("gap_calendar_basis", "zero observed composite hours; ECWT blocked"),
            ("provenance_summary_json", json.dumps({}, sort_keys=True)),
            ("contributing_towers_json", json.dumps({}, sort_keys=True)),
            ("source_channels_json", json.dumps({}, sort_keys=True)),
            ("cold_tail_provenance_json", json.dumps({}, sort_keys=True)),
            ("publication_caveat", PUBLICATION_CAVEAT),
        ]
    )


def release_row_from_result(row: OrderedDict[str, object], plant: dict[str, str]) -> OrderedDict[str, object]:
    return OrderedDict(
        [
            ("release_id", row["release_id"]),
            ("adr0004_run_id", row["adr0004_run_id"]),
            ("plant_id", row["plant_id"]),
            ("eia_plant_code", row["eia_plant_code"]),
            ("plant_name", row["plant_name"]),
            ("utility_id", plant.get("utility_id") or ""),
            ("utility_name", plant.get("utility_name") or ""),
            ("plant_state", row["plant_state"]),
            ("plant_county", row["plant_county"]),
            ("plant_latitude", plant.get("plant_latitude") or ""),
            ("plant_longitude", plant.get("plant_longitude") or ""),
            ("nerc_region", plant.get("nerc_region") or ""),
            ("balancing_authority_code", plant.get("balancing_authority_code") or ""),
            ("balancing_authority_name", plant.get("balancing_authority_name") or ""),
            ("sector_name", plant.get("sector_name") or ""),
            ("primary_station_id", row["primary_station_id"]),
            ("primary_station_distance_km", row["primary_station_distance_km"]),
            ("primary_station_rank_order", row["primary_station_rank_order"]),
            ("ecwt_f", row["ecwt_f"]),
            ("ecwt_discrete_f", row["ecwt_discrete_f"]),
            ("confidence_tier", row["confidence_tier"]),
            ("needs_review", row["needs_review"]),
            ("reason", row["reason"]),
            ("valid_hour_count", row["valid_hour_count"]),
            ("expected_hour_count", row["expected_hour_count"]),
            ("missing_hour_count", row["missing_hour_count"]),
            ("missing_frac", row["missing_frac"]),
            ("coverage_ratio", row["coverage_ratio"]),
            ("coverage_basis", row["coverage_basis"]),
            ("contributing_towers", row["contributing_towers_json"]),
            ("source_channels", row["source_channels_json"]),
            ("filled_hour_count", json.loads(str(row["provenance_summary_json"] or "{}")).get("filled_hours", 0)),
            ("cold_tail_provenance", row["cold_tail_provenance_json"]),
            ("publication_caveat", row["publication_caveat"]),
        ]
    )


def build_outputs(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    project_root: Path,
    run_id: str,
    release_id: str,
    station_candidate_run_id: str,
    calc_date: date,
    include_ak: bool,
    limit_plants: int | None,
) -> OrderedDict[str, object]:
    expected_hours = expected_djf_hours(calc_date)
    targets = load_targets(
        psql,
        host,
        port,
        dbname,
        user,
        station_candidate_run_id,
        include_ak,
        limit_plants,
    )
    plants_by_station: dict[str, list[dict[str, str]]] = defaultdict(list)
    blocked_plants: list[dict[str, str]] = []
    for plant in targets:
        station_id = plant.get("primary_station_id") or ""
        if station_id:
            plants_by_station[station_id].append(plant)
        else:
            blocked_plants.append(plant)

    processed_dir = project_root / "data" / "processed"
    results_csv = processed_dir / f"{run_id}_results.csv"
    sources_csv = processed_dir / f"{run_id}_sources.csv"
    cold_tail_csv = processed_dir / f"{run_id}_cold_tail_hours.csv"
    release_csv = processed_dir / f"{release_id}.csv"

    result_writer = write_csv_header(results_csv, RESULT_FIELDS)
    source_writer = write_csv_header(sources_csv, SOURCE_FIELDS)
    cold_writer = write_csv_header(cold_tail_csv, COLD_TAIL_FIELDS)
    release_writer = write_csv_header(release_csv, RELEASE_FIELDS)

    tier_counts: Counter[str] = Counter()
    result_rows = 0
    release_rows = 0
    tail_rows = 0
    stations_processed = 0
    rows_with_ecwt = 0
    station_ids = set(plants_by_station)

    try:
        for station_id, primary_obs, raw_rows in iter_station_observations(
            psql, host, port, dbname, user, station_ids
        ):
            stations_processed += 1
            composite = build_composite(primary_obs, [])
            temps = [obs.dry_bulb_f for obs in composite]
            raw_ecwt = ecwt_percentile(temps)
            raw_discrete = ecwt_discrete_rank_temp(temps)
            adequacy = assess_adequacy(temps, expected_hours)
            summary = provenance_summary(composite, raw_ecwt)
            cutoff = max((row["hour_ending_utc"] for row in raw_rows), default=None)
            tail_pairs = [
                (obs, raw)
                for obs, raw in zip(composite, raw_rows, strict=True)
                if obs.dry_bulb_f <= raw_ecwt
            ]
            discrete_rank = max(1, math.ceil(0.002 * len(temps)))
            for plant in plants_by_station[station_id]:
                row = result_base(run_id, release_id, plant, calc_date, expected_hours)
                row.update(
                    {
                        "calculation_cutoff_utc": cutoff,
                        "valid_hour_count": adequacy.n,
                        "missing_hour_count": adequacy.missing_hours,
                        "missing_frac": adequacy.missing_frac,
                        "coverage_ratio": round(adequacy.n / expected_hours, 6) if expected_hours else None,
                        "ecwt_f": adequacy.ecwt_f,
                        "ecwt_c": ecwt_c_from_f(raw_ecwt),
                        "ecwt_discrete_f": round(raw_discrete, 1),
                        "ecwt_discrete_c": ecwt_c_from_f(raw_discrete),
                        "discrete_rank": discrete_rank,
                        "tail_hour_count": len(tail_pairs),
                        "confidence_tier": adequacy.confidence_tier,
                        "needs_review": adequacy.needs_review,
                        "reason": adequacy.reason,
                        "gap_calendar_basis": (
                            "actual missing-hour timestamps remain possible cold-tail hours; review required"
                            if adequacy.confidence_tier == "provisional_review"
                            else "automated ADR-0004 missing-fraction tier; no rigid publication gate applied"
                        ),
                        "provenance_summary_json": json.dumps(summary, sort_keys=True),
                        "contributing_towers_json": json.dumps(summary["towers"], sort_keys=True),
                        "source_channels_json": json.dumps(summary["sources"], sort_keys=True),
                        "cold_tail_provenance_json": json.dumps(
                            summary["cold_tail_provenance"], sort_keys=True
                        ),
                    }
                )
                writerow(result_writer, row)
                writerow(
                    source_writer,
                    {
                        "adr0004_run_id": run_id,
                        "plant_id": plant["plant_id"],
                        "station_id": station_id,
                        "role": "primary",
                        "fill_priority": 0,
                        "distance_km": plant.get("primary_station_distance_km") or None,
                        "rank_order": plant.get("primary_station_rank_order") or None,
                        "used_hour_count": adequacy.n,
                        "filled_hour_count": 0,
                    },
                )
                for obs, raw in tail_pairs:
                    writerow(
                        cold_writer,
                        {
                            "adr0004_run_id": run_id,
                            "plant_id": plant["plant_id"],
                            "hour_ending_utc": raw["hour_ending_utc"],
                            "hour_local": raw.get("hour_local") or None,
                            "obs_timestamp": raw.get("obs_timestamp") or raw["hour_ending_utc"],
                            "station_id": obs.station_id,
                            "dry_bulb_f": round(obs.dry_bulb_f, 3),
                            "source_channel": obs.source_channel,
                            "source_code": obs.source_code,
                            "report_type": obs.report_type,
                            "source_file_id": obs.source_file_id,
                            "filled": obs.filled,
                        },
                    )
                    tail_rows += 1
                writerow(release_writer, release_row_from_result(row, plant))
                tier_counts[str(row["confidence_tier"])] += 1
                result_rows += 1
                release_rows += 1
                rows_with_ecwt += 1

        processed_plants = result_rows
        for plant in blocked_plants:
            row = result_base(run_id, release_id, plant, calc_date, expected_hours)
            writerow(result_writer, row)
            writerow(release_writer, release_row_from_result(row, plant))
            tier_counts["blocked_no_data"] += 1
            result_rows += 1
            release_rows += 1
    finally:
        close_writer(result_writer)
        close_writer(source_writer)
        close_writer(cold_writer)
        close_writer(release_writer)

    return OrderedDict(
        [
            ("run_id", run_id),
            ("release_id", release_id),
            ("station_candidate_run_id", station_candidate_run_id),
            ("calculation_date", calc_date.isoformat()),
            ("expected_djf_hours", expected_hours),
            ("target_plants", len(targets)),
            ("plants_with_station_weather", processed_plants),
            ("blocked_no_station_weather", len(blocked_plants)),
            ("stations_processed", stations_processed),
            ("result_rows", result_rows),
            ("release_rows", release_rows),
            ("rows_with_ecwt", rows_with_ecwt),
            ("cold_tail_rows", tail_rows),
            ("confidence_tier_counts", dict(sorted(tier_counts.items()))),
            ("results_csv", str(results_csv)),
            ("sources_csv", str(sources_csv)),
            ("cold_tail_csv", str(cold_tail_csv)),
            ("release_csv", str(release_csv)),
        ]
    )


def create_load_sql(
    run_id: str,
    release_id: str,
    started_at: datetime,
    code_commit: str,
    outputs: OrderedDict[str, object],
    project_root: Path,
) -> str:
    results_csv = Path(str(outputs["results_csv"]))
    sources_csv = Path(str(outputs["sources_csv"]))
    cold_tail_csv = Path(str(outputs["cold_tail_csv"]))
    release_csv = Path(str(outputs["release_csv"]))
    release_sha = sha256_file(release_csv)
    params = {
        "adr": "ADR-0004",
        "station_candidate_run_id": outputs["station_candidate_run_id"],
        "calculation_date": outputs["calculation_date"],
        "expected_djf_hours": outputs["expected_djf_hours"],
        "release_id": release_id,
    }
    result_temp = ",\n    ".join(f"{field} text" for field in RESULT_FIELDS)
    source_temp = ",\n    ".join(f"{field} text" for field in SOURCE_FIELDS)
    tail_temp = ",\n    ".join(f"{field} text" for field in COLD_TAIL_FIELDS)
    return f"""
begin;

insert into audit.methodology_version (
    methodology_version, methodology_name, effective_at_utc, source_standard, notes
) values (
    {sql_literal(METHODOLOGY_VERSION)},
    'ADR-0004 observational ECWT calculation layer',
    {sql_literal(started_at.isoformat())}::timestamptz,
    'NERC EOP-012-3 / Calculating Extreme Cold Weather Temperature',
    'Observational-only ECWT with adequacy confidence tiers and cold-tail provenance.'
) on conflict (methodology_version) do update set
    notes = excluded.notes;

insert into audit.calculation_run (
    calculation_run_id, methodology_version, code_commit, run_started_at_utc,
    run_finished_at_utc, run_status, parameters_json, notes
) values (
    {sql_literal(run_id)},
    {sql_literal(METHODOLOGY_VERSION)},
    {sql_literal(code_commit)},
    {sql_literal(started_at.isoformat())}::timestamptz,
    now(),
    'succeeded',
    {sql_literal(json.dumps(params, sort_keys=True))}::jsonb,
    'Rebuilt ADR-0004 plant ECWT layer using scripts/ecwt_core.py helpers.'
) on conflict (calculation_run_id) do update set
    code_commit = excluded.code_commit,
    run_finished_at_utc = excluded.run_finished_at_utc,
    run_status = excluded.run_status,
    parameters_json = excluded.parameters_json,
    notes = excluded.notes;

create temp table tmp_adr0004_result (
    {result_temp}
) on commit drop;
create temp table tmp_adr0004_source (
    {source_temp}
) on commit drop;
create temp table tmp_adr0004_tail (
    {tail_temp}
) on commit drop;

\\copy tmp_adr0004_result ({", ".join(RESULT_FIELDS)}) from {sql_literal(str(results_csv))} with (format csv, header true, null '\\N')
\\copy tmp_adr0004_source ({", ".join(SOURCE_FIELDS)}) from {sql_literal(str(sources_csv))} with (format csv, header true, null '\\N')
\\copy tmp_adr0004_tail ({", ".join(COLD_TAIL_FIELDS)}) from {sql_literal(str(cold_tail_csv))} with (format csv, header true, null '\\N')

insert into calc.plant_ecwt_adr0004_result (
    adr0004_result_id,
    adr0004_run_id,
    release_id,
    plant_id,
    eia_plant_code,
    plant_name,
    plant_state,
    plant_county,
    primary_station_id,
    primary_station_distance_km,
    primary_station_rank_order,
    calculation_date,
    calculation_cutoff_utc,
    valid_hour_count,
    expected_hour_count,
    missing_hour_count,
    missing_frac,
    coverage_ratio,
    ecwt_f,
    ecwt_c,
    ecwt_discrete_f,
    ecwt_discrete_c,
    discrete_rank,
    tail_hour_count,
    confidence_tier,
    needs_review,
    reason,
    coverage_basis,
    gap_calendar_basis,
    provenance_summary,
    contributing_towers,
    source_channels,
    cold_tail_provenance,
    publication_caveat
)
select
    adr0004_result_id,
    adr0004_run_id,
    release_id,
    plant_id,
    eia_plant_code,
    plant_name,
    plant_state,
    nullif(plant_county, ''),
    nullif(primary_station_id, ''),
    nullif(primary_station_distance_km, '')::numeric,
    nullif(primary_station_rank_order, '')::integer,
    calculation_date::date,
    nullif(calculation_cutoff_utc, '')::timestamptz,
    valid_hour_count::bigint,
    expected_hour_count::bigint,
    missing_hour_count::bigint,
    nullif(missing_frac, '')::numeric,
    nullif(coverage_ratio, '')::numeric,
    nullif(ecwt_f, '')::numeric,
    nullif(ecwt_c, '')::numeric,
    nullif(ecwt_discrete_f, '')::numeric,
    nullif(ecwt_discrete_c, '')::numeric,
    nullif(discrete_rank, '')::integer,
    tail_hour_count::bigint,
    confidence_tier,
    needs_review::boolean,
    reason,
    coverage_basis,
    gap_calendar_basis,
    nullif(provenance_summary_json, '')::jsonb,
    nullif(contributing_towers_json, '')::jsonb,
    nullif(source_channels_json, '')::jsonb,
    nullif(cold_tail_provenance_json, '')::jsonb,
    publication_caveat
from tmp_adr0004_result
on conflict (adr0004_result_id) do update set
    release_id = excluded.release_id,
    primary_station_id = excluded.primary_station_id,
    primary_station_distance_km = excluded.primary_station_distance_km,
    primary_station_rank_order = excluded.primary_station_rank_order,
    calculation_date = excluded.calculation_date,
    calculation_cutoff_utc = excluded.calculation_cutoff_utc,
    valid_hour_count = excluded.valid_hour_count,
    expected_hour_count = excluded.expected_hour_count,
    missing_hour_count = excluded.missing_hour_count,
    missing_frac = excluded.missing_frac,
    coverage_ratio = excluded.coverage_ratio,
    ecwt_f = excluded.ecwt_f,
    ecwt_c = excluded.ecwt_c,
    ecwt_discrete_f = excluded.ecwt_discrete_f,
    ecwt_discrete_c = excluded.ecwt_discrete_c,
    discrete_rank = excluded.discrete_rank,
    tail_hour_count = excluded.tail_hour_count,
    confidence_tier = excluded.confidence_tier,
    needs_review = excluded.needs_review,
    reason = excluded.reason,
    coverage_basis = excluded.coverage_basis,
    gap_calendar_basis = excluded.gap_calendar_basis,
    provenance_summary = excluded.provenance_summary,
    contributing_towers = excluded.contributing_towers,
    source_channels = excluded.source_channels,
    cold_tail_provenance = excluded.cold_tail_provenance,
    publication_caveat = excluded.publication_caveat;

delete from calc.plant_ecwt_adr0004_source
where adr0004_run_id = {sql_literal(run_id)};
insert into calc.plant_ecwt_adr0004_source (
    adr0004_run_id, plant_id, station_id, role, fill_priority,
    distance_km, rank_order, used_hour_count, filled_hour_count
)
select
    adr0004_run_id,
    plant_id,
    station_id,
    role,
    fill_priority::integer,
    nullif(distance_km, '')::numeric,
    nullif(rank_order, '')::integer,
    used_hour_count::bigint,
    filled_hour_count::bigint
from tmp_adr0004_source;

delete from calc.plant_ecwt_adr0004_cold_tail_hour
where adr0004_run_id = {sql_literal(run_id)};
insert into calc.plant_ecwt_adr0004_cold_tail_hour (
    adr0004_run_id, plant_id, hour_ending_utc, hour_local, obs_timestamp,
    station_id, dry_bulb_f, source_channel, source_code, report_type,
    source_file_id, filled
)
select
    adr0004_run_id,
    plant_id,
    hour_ending_utc::timestamptz,
    nullif(hour_local, '')::timestamp,
    nullif(obs_timestamp, '')::timestamptz,
    station_id,
    dry_bulb_f::numeric,
    nullif(source_channel, '')::weather.source_channel,
    nullif(source_code, ''),
    nullif(report_type, ''),
    nullif(source_file_id, ''),
    filled::boolean
from tmp_adr0004_tail;

delete from calc.plant_ecwt_adr0004_summary;
insert into calc.plant_ecwt_adr0004_summary (metric, metric_value, adr0004_run_id)
select metric, metric_value, {sql_literal(run_id)}
from (
    values
        ('release_id', {sql_literal(release_id)}),
        ('result_rows', (select count(*)::text from calc.plant_ecwt_adr0004_result where adr0004_run_id = {sql_literal(run_id)})),
        ('rows_with_ecwt', (select count(*)::text from calc.plant_ecwt_adr0004_result where adr0004_run_id = {sql_literal(run_id)} and ecwt_f is not null)),
        ('cold_tail_rows', (select count(*)::text from calc.plant_ecwt_adr0004_cold_tail_hour where adr0004_run_id = {sql_literal(run_id)})),
        ('complete', (select count(*)::text from calc.plant_ecwt_adr0004_result where adr0004_run_id = {sql_literal(run_id)} and confidence_tier = 'complete')),
        ('adequate', (select count(*)::text from calc.plant_ecwt_adr0004_result where adr0004_run_id = {sql_literal(run_id)} and confidence_tier = 'adequate')),
        ('provisional_review', (select count(*)::text from calc.plant_ecwt_adr0004_result where adr0004_run_id = {sql_literal(run_id)} and confidence_tier = 'provisional_review')),
        ('blocked_no_data', (select count(*)::text from calc.plant_ecwt_adr0004_result where adr0004_run_id = {sql_literal(run_id)} and confidence_tier = 'blocked_no_data'))
) as v(metric, metric_value);

insert into audit.release_manifest (
    release_id, calculation_run_id, release_name, release_created_at_utc,
    code_commit, source_manifest_sha256, release_notes
) values (
    {sql_literal(release_id)},
    {sql_literal(run_id)},
    'ADR-0004 scoped plant ECWT release',
    now(),
    {sql_literal(code_commit)},
    {sql_literal(release_sha)},
    'ADR-0004 observational ECWT release with confidence tiers and cold-tail provenance.'
) on conflict (release_id) do update set
    calculation_run_id = excluded.calculation_run_id,
    release_name = excluded.release_name,
    release_created_at_utc = excluded.release_created_at_utc,
    code_commit = excluded.code_commit,
    source_manifest_sha256 = excluded.source_manifest_sha256,
    release_notes = excluded.release_notes;

insert into publish.release_artifact (
    release_artifact_id, release_id, artifact_name, artifact_type,
    local_path, size_bytes, sha256, row_count
) values (
    {sql_literal(release_id + ':adr0004_release_csv')},
    {sql_literal(release_id)},
    'adr0004_release_csv',
    'csv',
    {sql_literal(str(release_csv.relative_to(project_root)))},
    {release_csv.stat().st_size},
    {sql_literal(release_sha)},
    {outputs['release_rows']}
) on conflict (release_artifact_id) do update set
    local_path = excluded.local_path,
    size_bytes = excluded.size_bytes,
    sha256 = excluded.sha256,
    row_count = excluded.row_count,
    created_at_utc = now();

commit;
"""


def db_sanity_counts(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    run_id: str,
) -> OrderedDict[str, object]:
    tier_rows = psql_csv_query(
        psql,
        host,
        port,
        dbname,
        user,
        f"""
        select confidence_tier, count(*)::bigint as rows
        from calc.plant_ecwt_adr0004_result
        where adr0004_run_id = {sql_literal(run_id)}
        group by confidence_tier
        order by confidence_tier
        """,
    )
    scalar_rows = psql_csv_query(
        psql,
        host,
        port,
        dbname,
        user,
        f"""
        select
            count(*)::bigint as result_rows,
            count(*) filter (where ecwt_f is not null)::bigint as rows_with_ecwt,
            count(*) filter (where ecwt_f is null and confidence_tier <> 'blocked_no_data')::bigint as unexpected_null_ecwt,
            (select count(*) from calc.plant_ecwt_adr0004_cold_tail_hour where adr0004_run_id = {sql_literal(run_id)})::bigint as cold_tail_rows,
            (select count(distinct plant_id) from calc.plant_ecwt_adr0004_cold_tail_hour where adr0004_run_id = {sql_literal(run_id)})::bigint as plants_with_cold_tail
        from calc.plant_ecwt_adr0004_result
        where adr0004_run_id = {sql_literal(run_id)}
        """,
    )[0]
    return OrderedDict([("tiers", tier_rows), ("sanity", scalar_rows)])


def render_status_doc(
    path: Path,
    outputs: OrderedDict[str, object],
    db_counts: OrderedDict[str, object],
    release_sha: str,
    code_commit: str,
) -> None:
    tiers = {row["confidence_tier"]: row["rows"] for row in db_counts["tiers"]}
    sanity = db_counts["sanity"]
    lines = [
        "# ADR-0004 ECWT Status",
        "",
        f"- ADR-0004 run ID: `{outputs['run_id']}`",
        f"- Release ID: `{outputs['release_id']}`",
        f"- Station candidate run ID: `{outputs['station_candidate_run_id']}`",
        f"- Calculation date: `{outputs['calculation_date']}`",
        f"- Expected DJF hours: `{outputs['expected_djf_hours']}`",
        f"- Git commit: `{code_commit}`",
        f"- Release CSV: `{outputs['release_csv']}`",
        f"- Release CSV SHA-256: `{release_sha}`",
        "",
        "## Counts",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| Result rows | {sanity['result_rows']} |",
        f"| Rows with ECWT | {sanity['rows_with_ecwt']} |",
        f"| Cold-tail rows | {sanity['cold_tail_rows']} |",
        f"| Plants with cold-tail rows | {sanity['plants_with_cold_tail']} |",
        f"| Unexpected null ECWT rows | {sanity['unexpected_null_ecwt']} |",
        "",
        "## Confidence Split",
        "",
        "| Tier | Plants |",
        "| --- | ---: |",
        f"| `complete` | {tiers.get('complete', '0')} |",
        f"| `adequate` | {tiers.get('adequate', '0')} |",
        f"| `provisional_review` | {tiers.get('provisional_review', '0')} |",
        f"| `blocked_no_data` | {tiers.get('blocked_no_data', '0')} |",
        "",
        "## Notes",
        "",
        "- ECWT math was calculated through `scripts/ecwt_core.py`; the script does not reimplement percentile or adequacy math.",
        "- The release is analytical and is not a Generator Owner compliance filing.",
        "- Existing `weather.hourly_djf.obs_timestamp` is backfilled to the canonical hour where the prior loader did not retain the raw NOAA `DATE` timestamp. Future loads should populate the raw observation timestamp directly.",
        "- Full composite hours are exposed by `calc.plant_ecwt_adr0004_composite_hour`; materialized audit rows are limited to cold-tail hours to avoid duplicating the primary-station series hundreds of millions of times.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--psql", type=Path, default=PSQL)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5436)
    parser.add_argument("--dbname", default="eop012")
    parser.add_argument("--user", default=None)
    parser.add_argument("--station-candidate-run-id")
    parser.add_argument("--calc-date")
    parser.add_argument("--run-id")
    parser.add_argument("--release-id")
    parser.add_argument("--include-ak", action="store_true")
    parser.add_argument("--limit-plants", type=int)
    parser.add_argument("--skip-hourly-provenance-backfill", action="store_true")
    parser.add_argument("--skip-db-load", action="store_true")
    args = parser.parse_args()

    started_at = utc_now()
    timestamp = started_at.strftime("%Y%m%dT%H%M%SZ")
    run_id = args.run_id or f"plant_ecwt_adr0004_{timestamp}"
    release_id = args.release_id or f"scoped_plant_ecwt_adr0004_release_{timestamp}"
    station_candidate_run_id = args.station_candidate_run_id or latest_successful_run_id(
        args.psql, args.host, args.port, args.dbname, args.user, DEFAULT_CANDIDATE_PREFIX
    )
    calc_date = date.fromisoformat(args.calc_date) if args.calc_date else max_loaded_calc_date(
        args.psql, args.host, args.port, args.dbname, args.user
    )
    project_root = args.project_root.resolve()
    code_commit = git_commit_label(project_root)

    ensure_schema(args.psql, args.host, args.port, args.dbname, args.user)
    if not args.skip_hourly_provenance_backfill:
        backfill_hourly_provenance(args.psql, args.host, args.port, args.dbname, args.user)

    outputs = build_outputs(
        args.psql,
        args.host,
        args.port,
        args.dbname,
        args.user,
        project_root,
        run_id,
        release_id,
        station_candidate_run_id,
        calc_date,
        args.include_ak,
        args.limit_plants,
    )

    if not args.skip_db_load:
        load_sql = create_load_sql(run_id, release_id, started_at, code_commit, outputs, project_root)
        psql_execute(args.psql, args.host, args.port, args.dbname, args.user, load_sql)
        db_counts = db_sanity_counts(args.psql, args.host, args.port, args.dbname, args.user, run_id)
    else:
        db_counts = OrderedDict([("tiers", []), ("sanity", {})])

    release_sha = sha256_file(Path(str(outputs["release_csv"])))
    status_doc = project_root / "docs" / "adr0004_ecwt_status.md"
    if not args.skip_db_load:
        render_status_doc(status_doc, outputs, db_counts, release_sha, code_commit)
    outputs["release_sha256"] = release_sha
    outputs["status_doc"] = str(status_doc)
    outputs["db_counts"] = db_counts
    print(json.dumps(outputs, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
