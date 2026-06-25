-- Initial EOP012 audit schema for Postgres.
-- Heavy working databases should live on /Volumes/NOAA_CACHE, not in Git.

create schema if not exists audit;
create schema if not exists asset;
create schema if not exists weather;
create schema if not exists link;
create schema if not exists calc;
create schema if not exists publish;

create table if not exists audit.methodology_version (
    methodology_version text primary key,
    methodology_name text not null,
    effective_at_utc timestamptz not null,
    source_standard text,
    notes text
);

create table if not exists audit.source_file (
    source_file_id text primary key,
    source_family text not null,
    source_url text,
    local_path text,
    file_name text not null,
    size_bytes bigint,
    sha256 text,
    retrieved_at_utc timestamptz,
    source_year integer,
    source_release text,
    notes text,
    created_at_utc timestamptz not null default now(),
    constraint source_file_sha256_len check (sha256 is null or length(sha256) = 64)
);

create table if not exists audit.calculation_run (
    calculation_run_id text primary key,
    methodology_version text not null references audit.methodology_version(methodology_version),
    code_commit text,
    run_started_at_utc timestamptz not null default now(),
    run_finished_at_utc timestamptz,
    run_status text not null,
    parameters_json jsonb not null default '{}'::jsonb,
    notes text,
    constraint calculation_run_status_check
        check (run_status in ('running', 'succeeded', 'failed', 'superseded'))
);

create table if not exists audit.release_manifest (
    release_id text primary key,
    calculation_run_id text not null references audit.calculation_run(calculation_run_id),
    release_name text not null,
    release_created_at_utc timestamptz not null default now(),
    code_commit text,
    source_manifest_sha256 text,
    release_notes text,
    constraint release_manifest_sha256_len
        check (source_manifest_sha256 is null or length(source_manifest_sha256) = 64)
);

create table if not exists asset.utility (
    utility_id text primary key,
    utility_name text not null,
    entity_type text,
    source_file_id text references audit.source_file(source_file_id),
    source_year integer,
    created_at_utc timestamptz not null default now()
);

create table if not exists asset.plant (
    plant_id text primary key,
    eia_plant_code text not null unique,
    plant_name text not null,
    utility_id text references asset.utility(utility_id),
    utility_name text,
    street_address text,
    city text,
    state text,
    zip text,
    county text,
    latitude numeric,
    longitude numeric,
    nerc_region text,
    balancing_authority_code text,
    balancing_authority_name text,
    sector_name text,
    source_file_id text references audit.source_file(source_file_id),
    source_year integer,
    created_at_utc timestamptz not null default now(),
    constraint plant_latitude_range check (latitude is null or latitude between -90 and 90),
    constraint plant_longitude_range check (longitude is null or longitude between -180 and 180)
);

create table if not exists asset.generator (
    generator_id_internal text primary key,
    eia_plant_code text not null,
    generator_id text not null,
    utility_id text,
    utility_name text,
    plant_name text,
    state text,
    county text,
    technology text,
    prime_mover text,
    unit_code text,
    ownership text,
    nameplate_capacity_mw numeric,
    summer_capacity_mw numeric,
    winter_capacity_mw numeric,
    status text not null,
    generator_sheet text not null,
    source_file_id text references audit.source_file(source_file_id),
    source_year integer,
    created_at_utc timestamptz not null default now(),
    unique (eia_plant_code, generator_id, generator_sheet, source_year)
);

create index if not exists ix_asset_generator_plant
    on asset.generator (eia_plant_code);

create index if not exists ix_asset_generator_status
    on asset.generator (status);

create table if not exists weather.station (
    station_id text primary key,
    station_name text,
    latitude numeric,
    longitude numeric,
    elevation_m numeric,
    state text,
    country text,
    first_observation_utc timestamptz,
    last_observation_utc timestamptz,
    source_file_id text references audit.source_file(source_file_id),
    created_at_utc timestamptz not null default now(),
    constraint station_latitude_range check (latitude is null or latitude between -90 and 90),
    constraint station_longitude_range check (longitude is null or longitude between -180 and 180)
);

create table if not exists weather.hourly_djf (
    station_id text not null references weather.station(station_id),
    hour_ending_utc timestamptz not null,
    hour_local timestamp,
    dry_bulb_c numeric,
    dry_bulb_f numeric,
    source_file_id text references audit.source_file(source_file_id),
    quality_flags text[],
    calculation_run_id text references audit.calculation_run(calculation_run_id),
    created_at_utc timestamptz not null default now(),
    primary key (station_id, hour_ending_utc)
);

create index if not exists ix_weather_hourly_djf_hour
    on weather.hourly_djf (hour_ending_utc);

create table if not exists weather.noaa_hourly_load_file (
    load_file_id text primary key,
    calculation_run_id text not null references audit.calculation_run(calculation_run_id),
    station_id text not null references weather.station(station_id),
    source_year integer not null,
    raw_station_id text not null,
    local_path text not null,
    source_file_id text references audit.source_file(source_file_id),
    source_basis text not null,
    file_size_bytes bigint,
    file_status text not null,
    rows_seen bigint not null default 0,
    djf_rows_seen bigint not null default 0,
    rejected_source_rows bigint not null default 0,
    valid_temp_rows bigint not null default 0,
    invalid_temp_rows bigint not null default 0,
    rejected_plausibility_rows bigint not null default 0,
    duplicate_hour_count bigint not null default 0,
    loaded_hour_count bigint not null default 0,
    min_hour_ending_utc timestamptz,
    max_hour_ending_utc timestamptz,
    error_message text,
    notes text,
    created_at_utc timestamptz not null default now(),
    unique (station_id, source_year, local_path),
    constraint noaa_hourly_load_file_status_check
        check (file_status in ('loaded', 'failed', 'skipped'))
);

create index if not exists ix_noaa_hourly_load_file_status
    on weather.noaa_hourly_load_file (calculation_run_id, file_status);

create index if not exists ix_noaa_hourly_load_file_station_year
    on weather.noaa_hourly_load_file (station_id, source_year);

alter table weather.noaa_hourly_load_file
    add column if not exists rejected_source_rows bigint not null default 0;

alter table weather.noaa_hourly_load_file
    add column if not exists rejected_plausibility_rows bigint not null default 0;

create table if not exists weather.station_year_djf_coverage (
    station_year_djf_coverage_id text primary key,
    station_id text not null references weather.station(station_id),
    source_year integer not null,
    calculation_run_id text not null references audit.calculation_run(calculation_run_id),
    period_start_utc timestamptz not null,
    period_end_utc timestamptz not null,
    expected_djf_hours bigint not null,
    valid_djf_hours bigint not null,
    missing_hour_count bigint not null,
    loaded_file_count bigint not null,
    invalid_temp_row_count bigint not null,
    rejected_source_row_count bigint not null,
    rejected_plausibility_row_count bigint not null,
    duplicate_hour_count bigint not null,
    coverage_ratio numeric,
    coverage_status text not null,
    notes text,
    created_at_utc timestamptz not null default now(),
    unique (station_id, source_year, calculation_run_id),
    constraint station_year_djf_coverage_status_check
        check (coverage_status in ('complete', 'partial', 'empty'))
);

create index if not exists ix_station_year_djf_coverage_station_year
    on weather.station_year_djf_coverage (station_id, source_year);

create index if not exists ix_station_year_djf_coverage_status
    on weather.station_year_djf_coverage (calculation_run_id, coverage_status);

create table if not exists weather.noaa_raw_file_inventory (
    inventory_id text primary key,
    station_id text not null references weather.station(station_id),
    source_year integer not null,
    calculation_run_id text not null references audit.calculation_run(calculation_run_id),
    source_file_id text references audit.source_file(source_file_id),
    raw_station_id text not null,
    local_path text,
    file_name text,
    source_root text,
    file_size_bytes bigint,
    file_mtime_utc timestamptz,
    file_status text not null,
    notes text,
    created_at_utc timestamptz not null default now(),
    unique (station_id, source_year, calculation_run_id),
    constraint noaa_raw_file_inventory_status_check
        check (file_status in ('available', 'missing'))
);

create index if not exists ix_noaa_raw_file_inventory_year_status
    on weather.noaa_raw_file_inventory (source_year, file_status);

create table if not exists weather.noaa_raw_backfill_manifest (
    manifest_id text primary key,
    inventory_run_id text not null references audit.calculation_run(calculation_run_id),
    calculation_run_id text not null references audit.calculation_run(calculation_run_id),
    station_id text not null references weather.station(station_id),
    source_year integer not null,
    raw_station_id text not null,
    download_url text not null,
    target_path text not null,
    priority_rank integer not null,
    batch_number integer not null,
    station_candidate_plant_links integer not null,
    source_year_available_count integer not null,
    source_year_missing_count integer not null,
    manifest_status text not null,
    priority_reason text,
    notes text,
    created_at_utc timestamptz not null default now(),
    unique (inventory_run_id, station_id, source_year, calculation_run_id),
    constraint noaa_raw_backfill_manifest_status_check
        check (manifest_status in ('planned', 'downloaded', 'skipped', 'missing', 'failed'))
);

create index if not exists ix_noaa_raw_backfill_manifest_batch
    on weather.noaa_raw_backfill_manifest (calculation_run_id, batch_number, priority_rank);

create index if not exists ix_noaa_raw_backfill_manifest_year_status
    on weather.noaa_raw_backfill_manifest (source_year, manifest_status);

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
        check (download_status in ('downloaded', 'skipped_existing', 'missing_on_aws', 'failed_http', 'failed_exception', 'dry_run')),
    constraint noaa_raw_download_attempt_sha256_len
        check (file_sha256 is null or length(file_sha256) = 64)
);

create index if not exists ix_noaa_raw_download_attempt_status
    on weather.noaa_raw_download_attempt (calculation_run_id, download_status);

create table if not exists weather.station_coverage_audit (
    station_coverage_audit_id text primary key,
    station_id text not null references weather.station(station_id),
    calculation_run_id text not null references audit.calculation_run(calculation_run_id),
    period_start_utc timestamptz not null,
    period_end_utc timestamptz not null,
    expected_djf_hours bigint not null,
    valid_djf_hours bigint not null,
    missing_hour_count bigint not null,
    duplicate_hour_count bigint not null,
    invalid_temp_count bigint not null,
    coverage_ratio numeric,
    source_basis text,
    notes text,
    created_at_utc timestamptz not null default now()
);

create table if not exists link.station_candidate (
    candidate_id text primary key,
    plant_id text not null references asset.plant(plant_id),
    station_id text not null references weather.station(station_id),
    calculation_run_id text not null references audit.calculation_run(calculation_run_id),
    distance_km numeric,
    elevation_delta_m numeric,
    valid_djf_hours bigint,
    expected_djf_hours bigint,
    coverage_ratio numeric,
    rank_order integer,
    candidate_status text not null,
    reason_code text,
    notes text,
    created_at_utc timestamptz not null default now(),
    unique (plant_id, station_id, calculation_run_id),
    constraint station_candidate_status_check
        check (candidate_status in ('candidate', 'selected', 'rejected', 'needs_review'))
);

create index if not exists ix_station_candidate_plant_rank
    on link.station_candidate (plant_id, rank_order);

create table if not exists link.station_selection (
    station_selection_id text primary key,
    plant_id text not null references asset.plant(plant_id),
    calculation_run_id text not null references audit.calculation_run(calculation_run_id),
    methodology_version text not null references audit.methodology_version(methodology_version),
    selection_status text not null,
    decision_basis text not null,
    reviewer text,
    notes text,
    created_at_utc timestamptz not null default now(),
    constraint station_selection_status_check
        check (selection_status in ('algorithmic', 'manual_reviewed', 'provisional', 'blocked'))
);

create table if not exists link.station_selection_segment (
    station_selection_segment_id text primary key,
    station_selection_id text not null references link.station_selection(station_selection_id),
    station_id text not null references weather.station(station_id),
    segment_start_utc timestamptz not null,
    segment_end_utc timestamptz not null,
    reason_code text not null,
    notes text,
    created_at_utc timestamptz not null default now(),
    constraint station_selection_segment_dates
        check (segment_end_utc >= segment_start_utc)
);
create index if not exists ix_station_selection_segment_selection
    on link.station_selection_segment (station_selection_id);

create table if not exists calc.station_ecwt (
    station_ecwt_id text primary key,
    station_id text not null references weather.station(station_id),
    calculation_run_id text not null references audit.calculation_run(calculation_run_id),
    methodology_version text not null references audit.methodology_version(methodology_version),
    calculation_cutoff_utc timestamptz not null,
    valid_hour_count bigint not null,
    expected_hour_count bigint not null,
    missing_hour_count bigint not null,
    duplicate_hour_count bigint not null,
    percentile_target numeric not null default 0.002,
    ecwt_c numeric,
    ecwt_f numeric,
    discrete_rank integer,
    ecwt_discrete_c numeric,
    ecwt_discrete_f numeric,
    result_status text not null,
    created_at_utc timestamptz not null default now(),
    constraint station_ecwt_result_status_check
        check (result_status in ('accepted', 'provisional', 'blocked', 'superseded'))
);

create table if not exists calc.plant_ecwt (
    plant_ecwt_id text primary key,
    plant_id text not null references asset.plant(plant_id),
    station_selection_id text references link.station_selection(station_selection_id),
    calculation_run_id text not null references audit.calculation_run(calculation_run_id),
    methodology_version text not null references audit.methodology_version(methodology_version),
    calculation_cutoff_utc timestamptz not null,
    valid_hour_count bigint not null,
    expected_hour_count bigint not null,
    missing_hour_count bigint not null,
    duplicate_hour_count bigint not null,
    percentile_target numeric not null default 0.002,
    ecwt_c numeric,
    ecwt_f numeric,
    discrete_rank integer,
    ecwt_discrete_c numeric,
    ecwt_discrete_f numeric,
    governing_ecwt_f numeric,
    result_status text not null,
    created_at_utc timestamptz not null default now(),
    constraint plant_ecwt_result_status_check
        check (result_status in ('accepted', 'provisional', 'blocked', 'superseded'))
);
create index if not exists ix_plant_ecwt_run_selection
    on calc.plant_ecwt (calculation_run_id, station_selection_id);

create table if not exists calc.generator_ecwt (
    generator_ecwt_id text primary key,
    generator_id_internal text not null references asset.generator(generator_id_internal),
    plant_ecwt_id text not null references calc.plant_ecwt(plant_ecwt_id),
    calculation_run_id text not null references audit.calculation_run(calculation_run_id),
    methodology_version text not null references audit.methodology_version(methodology_version),
    ecwt_f numeric,
    governing_ecwt_f numeric,
    result_status text not null,
    created_at_utc timestamptz not null default now(),
    constraint generator_ecwt_result_status_check
        check (result_status in ('accepted', 'provisional', 'blocked', 'superseded'))
);

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

create table if not exists audit.exception_log (
    exception_id text primary key,
    calculation_run_id text references audit.calculation_run(calculation_run_id),
    entity_type text not null,
    entity_id text,
    severity text not null,
    reason_code text not null,
    message text not null,
    resolution_status text not null,
    notes text,
    created_at_utc timestamptz not null default now(),
    resolved_at_utc timestamptz,
    constraint exception_log_severity_check
        check (severity in ('info', 'warning', 'error', 'blocker')),
    constraint exception_log_resolution_status_check
        check (resolution_status in ('open', 'resolved', 'accepted_risk', 'blocked'))
);

create table if not exists publish.release_artifact (
    release_artifact_id text primary key,
    release_id text not null references audit.release_manifest(release_id),
    artifact_name text not null,
    artifact_type text not null,
    artifact_url text,
    local_path text,
    size_bytes bigint,
    sha256 text,
    row_count bigint,
    created_at_utc timestamptz not null default now(),
    constraint release_artifact_sha256_len
        check (sha256 is null or length(sha256) = 64)
);
