# Data Dictionary

This dictionary defines the initial publication-facing tables. It will expand as NOAA station matching and ECWT calculation are implemented.

## `audit.source_file`

| Column | Type | Meaning |
| --- | --- | --- |
| `source_file_id` | text | Stable source artifact identifier. |
| `source_family` | text | Source family, such as `eia860`, `noaa_global_hourly`, or `nerc_standard`. |
| `source_url` | text | Upstream URL when available. |
| `local_path` | text | Local path used during build. |
| `file_name` | text | File name. |
| `size_bytes` | bigint | File size in bytes. |
| `sha256` | text | SHA-256 hash. |
| `retrieved_at_utc` | timestamptz | Retrieval timestamp. |
| `notes` | text | Human-readable notes. |

## `audit.calculation_run`

| Column | Type | Meaning |
| --- | --- | --- |
| `calculation_run_id` | text | Stable run identifier. |
| `methodology_version` | text | Methodology version used by the run. |
| `code_commit` | text | Git commit hash. |
| `run_started_at_utc` | timestamptz | Start timestamp. |
| `run_finished_at_utc` | timestamptz | Finish timestamp. |
| `run_status` | text | `running`, `succeeded`, `failed`, or `superseded`. |
| `parameters_json` | jsonb | Run parameters. |

## `asset.plant`

| Column | Type | Meaning |
| --- | --- | --- |
| `plant_id` | text | Internal stable plant key. |
| `eia_plant_code` | text | EIA plant code. |
| `plant_name` | text | EIA plant name. |
| `utility_id` | text | EIA utility ID. |
| `utility_name` | text | EIA utility name. |
| `state` | text | State abbreviation. |
| `county` | text | County name. |
| `latitude` | numeric | Plant latitude. |
| `longitude` | numeric | Plant longitude. |
| `nerc_region` | text | EIA NERC region field. |
| `balancing_authority_code` | text | EIA balancing authority code. |
| `sector_name` | text | EIA sector name. |
| `source_file_id` | text | Source file lineage. |

## `asset.generator`

| Column | Type | Meaning |
| --- | --- | --- |
| `generator_id_internal` | text | Internal stable generator key. |
| `eia_plant_code` | text | EIA plant code. |
| `generator_id` | text | EIA generator ID. |
| `technology` | text | EIA technology description. |
| `prime_mover` | text | EIA prime mover code. |
| `status` | text | EIA generator status code. |
| `nameplate_capacity_mw` | numeric | Nameplate capacity. |
| `summer_capacity_mw` | numeric | Summer capacity. |
| `winter_capacity_mw` | numeric | Winter capacity. |
| `generator_sheet` | text | Source generator sheet, such as `Operable`. |
| `source_file_id` | text | Source file lineage. |

## `weather.station`

| Column | Type | Meaning |
| --- | --- | --- |
| `station_id` | text | Canonical weather station identifier. |
| `station_name` | text | Station name. |
| `latitude` | numeric | Station latitude. |
| `longitude` | numeric | Station longitude. |
| `elevation_m` | numeric | Station elevation where available. |
| `state` | text | State or region. |
| `country` | text | Country code. |
| `first_observation_utc` | timestamptz | Earliest known observation. |
| `last_observation_utc` | timestamptz | Latest known observation. |
| `local_standard_utc_offset_hours` | integer | Station-local standard-time UTC offset used for DJF month classification. The current loader derives it from station longitude when an authoritative offset is not available. |

## `weather.hourly_djf`

| Column | Type | Meaning |
| --- | --- | --- |
| `station_id` | text | Canonical NOAA ISD station identifier. |
| `hour_ending_utc` | timestamptz | Canonical UTC station-hour used for ECWT-oriented DJF weather analysis. Current loader policy floors the NOAA observation timestamp to the UTC hour. |
| `hour_local` | timestamp | Station-local standard-time hour used for DJF month classification. UTC remains canonical for storage and joins. |
| `dry_bulb_c` | numeric | Dry-bulb temperature in degrees C parsed from NOAA Global Hourly `TMP`. |
| `dry_bulb_f` | numeric | Dry-bulb temperature in degrees F. |
| `source_file_id` | text | Source file lineage. Downloaded AWS files have per-file lineage; preexisting local-inventory files currently use the inventory source-root lineage. |
| `quality_flags` | text[] | Loader-retained NOAA quality context, such as TMP quality code, report type, source code, quality-control code, and station-local offset. |
| `calculation_run_id` | text | DJF load run that inserted or last updated the row. |

## `weather.noaa_hourly_load_file`

| Column | Type | Meaning |
| --- | --- | --- |
| `load_file_id` | text | Stable file-load row identifier. |
| `calculation_run_id` | text | DJF load run lineage. |
| `station_id` | text | NOAA ISD station ID in `USAF-WBAN` form. |
| `source_year` | integer | NOAA Global Hourly source year. |
| `raw_station_id` | text | Raw NOAA station ID used in filenames, usually `USAFWBAN`. |
| `local_path` | text | Local CSV or gzip file parsed by the loader. |
| `source_file_id` | text | Source file lineage when available. |
| `source_basis` | text | Whether the file came from the preexisting raw inventory or a recorded AWS download attempt. |
| `file_size_bytes` | bigint | File size when available. |
| `file_status` | text | `loaded`, `failed`, or `skipped`. |
| `rows_seen` | bigint | Total CSV rows read. |
| `djf_rows_seen` | bigint | Rows whose station-local standard-time observation hour is in December, January, or February. |
| `rejected_source_rows` | bigint | DJF rows rejected before TMP interpretation because their NOAA `SOURCE` code is excluded by the canonical loader. |
| `valid_temp_rows` | bigint | DJF rows with a parseable non-missing `TMP` value accepted by the current loader. |
| `invalid_temp_rows` | bigint | DJF rows with missing or rejected `TMP` values. |
| `rejected_plausibility_rows` | bigint | DJF rows rejected because parsed dry-bulb temperature is outside the configured plausibility range. |
| `duplicate_hour_count` | bigint | Valid DJF observations that collided with another observation in the same canonical station-hour. |
| `loaded_hour_count` | bigint | Canonical station-hour rows staged from the file. |
| `min_hour_ending_utc` | timestamptz | Earliest canonical DJF hour loaded from the file. |
| `max_hour_ending_utc` | timestamptz | Latest canonical DJF hour loaded from the file. |
| `error_message` | text | Failure detail when applicable. |
| `notes` | text | Loader policy or caveat. |

## `weather.station_year_djf_coverage`

| Column | Type | Meaning |
| --- | --- | --- |
| `station_year_djf_coverage_id` | text | Stable station-year coverage row identifier. |
| `station_id` | text | NOAA ISD station ID in `USAF-WBAN` form. |
| `source_year` | integer | Station-local DJF source year used by the coverage builder. |
| `calculation_run_id` | text | Coverage-build run lineage. |
| `period_start_utc` | timestamptz | UTC timestamp corresponding to the start of the station-local source year. |
| `period_end_utc` | timestamptz | UTC timestamp corresponding to the end of the station-local source year. |
| `expected_djf_hours` | bigint | Expected station-local DJF hours in January, February, and December for the source year. |
| `valid_djf_hours` | bigint | Canonical loaded station-local DJF hours available for the station-year. |
| `missing_hour_count` | bigint | Expected minus valid DJF hours. |
| `loaded_file_count` | bigint | Loaded raw files contributing audit metrics for the station-year. |
| `invalid_temp_row_count` | bigint | Missing or invalid DJF TMP rows observed during loading. |
| `rejected_source_row_count` | bigint | Rows rejected by NOAA source-code policy. |
| `rejected_plausibility_row_count` | bigint | Rows rejected by physical plausibility policy. |
| `duplicate_hour_count` | bigint | Duplicate same-station-hour source observations collapsed by the loader. |
| `coverage_ratio` | numeric | Valid divided by expected DJF hours. |
| `coverage_status` | text | `complete`, `partial`, or `empty`. |
| `notes` | text | Coverage caveat or rule summary. |

## `weather.noaa_raw_file_inventory`

| Column | Type | Meaning |
| --- | --- | --- |
| `inventory_id` | text | Stable raw-file inventory row identifier. |
| `station_id` | text | NOAA ISD station ID in `USAF-WBAN` form. |
| `source_year` | integer | NOAA Global Hourly source year. |
| `calculation_run_id` | text | Inventory run lineage. |
| `source_file_id` | text | Source-root inventory provenance. |
| `raw_station_id` | text | Raw NOAA station ID used in filenames, usually `USAFWBAN`. |
| `local_path` | text | Local raw file path when available. |
| `file_name` | text | Local raw file name when available. |
| `source_root` | text | Configured raw root that supplied the file. |
| `file_size_bytes` | bigint | File size when available. |
| `file_mtime_utc` | timestamptz | Local file modified timestamp. |
| `file_status` | text | `available` or `missing`. |
| `notes` | text | Inventory caveat or status note. |

## `weather.noaa_raw_backfill_manifest`

| Column | Type | Meaning |
| --- | --- | --- |
| `manifest_id` | text | Stable planned-download row identifier. |
| `inventory_run_id` | text | Raw-file inventory run used as input. |
| `calculation_run_id` | text | Manifest-build run lineage. |
| `station_id` | text | NOAA ISD station ID in `USAF-WBAN` form. |
| `source_year` | integer | NOAA Global Hourly source year to backfill. |
| `raw_station_id` | text | Raw NOAA station ID used in filenames. |
| `download_url` | text | NOAA public CSV URL. |
| `target_path` | text | Planned local destination path. |
| `priority_rank` | integer | Stable manifest priority order. |
| `batch_number` | integer | Download batch number. |
| `station_candidate_plant_links` | integer | Number of candidate plant links for the station. |
| `source_year_available_count` | integer | Available station-year files found in the source year during inventory. |
| `source_year_missing_count` | integer | Missing station-year files found in the source year during inventory. |
| `manifest_status` | text | `planned`, `downloaded`, `skipped`, `missing`, or `failed`. `missing` means NOAA returned HTTP 404 for the planned public AWS object. |
| `priority_reason` | text | Machine-readable priority explanation. |
| `notes` | text | Manifest caveat or status note. |

## `weather.noaa_raw_download_attempt`

| Column | Type | Meaning |
| --- | --- | --- |
| `attempt_id` | text | Stable download-attempt row identifier. |
| `manifest_id` | text | Manifest row consumed by this attempt. |
| `manifest_run_id` | text | Manifest-build run that supplied the row. |
| `calculation_run_id` | text | Download-attempt run lineage. |
| `station_id` | text | NOAA ISD station ID in `USAF-WBAN` form. |
| `source_year` | integer | NOAA Global Hourly source year. |
| `raw_station_id` | text | Raw NOAA station ID used in filenames. |
| `download_url` | text | Public AWS S3 object URL attempted. |
| `target_path` | text | Local destination path. |
| `attempted_at_utc` | timestamptz | Attempt start timestamp. |
| `finished_at_utc` | timestamptz | Attempt finish timestamp. |
| `http_status` | integer | HTTP status returned by the source when available. |
| `download_status` | text | `downloaded`, `skipped_existing`, `missing_on_aws`, `failed_http`, `failed_exception`, or `dry_run`. `missing_on_aws` is a terminal NOAA HTTP 404 outcome; `failed_http` is reserved for non-404 HTTP errors that may be retried. |
| `file_size_bytes` | bigint | Downloaded or observed file size. |
| `file_sha256` | text | SHA-256 of downloaded or observed file. |
| `source_file_id` | text | `audit.source_file` row for successful or pre-existing files. |
| `error_message` | text | Failure detail when applicable. |
| `notes` | text | Attempt caveat or status note. |

## `weather.station_coverage_audit`

| Column | Type | Meaning |
| --- | --- | --- |
| `station_coverage_audit_id` | text | Stable coverage-audit row identifier. |
| `station_id` | text | Weather station audited. |
| `calculation_run_id` | text | Coverage-audit run lineage. |
| `period_start_utc` | timestamptz | First timestamp in the audited period. |
| `period_end_utc` | timestamptz | Last timestamp in the audited period. |
| `expected_djf_hours` | bigint | Expected DJF hours in the audited period. |
| `valid_djf_hours` | bigint | Valid dry-bulb sample hours found for the station. |
| `missing_hour_count` | bigint | Expected minus valid hours. |
| `duplicate_hour_count` | bigint | Duplicate/excess source hours identified by the audit method. |
| `invalid_temp_count` | bigint | Present but invalid dry-bulb observations identified by the audit method. |
| `coverage_ratio` | numeric | Valid divided by expected hours. |
| `source_basis` | text | Source/method used to produce the coverage counts. |
| `notes` | text | Caveats for the coverage-audit method. |

## `link.station_candidate`

| Column | Type | Meaning |
| --- | --- | --- |
| `candidate_id` | text | Stable candidate identifier. |
| `plant_id` | text | Internal plant key. |
| `station_id` | text | Candidate station. |
| `distance_km` | numeric | Great-circle distance from plant to station. |
| `valid_djf_hours` | bigint | Valid DJF dry-bulb hours in the calculation window. |
| `expected_djf_hours` | bigint | Expected DJF hours in the calculation window. |
| `coverage_ratio` | numeric | Valid divided by expected hours. |
| `rank_order` | integer | Algorithmic candidate rank. |
| `candidate_status` | text | `candidate`, `selected`, `rejected`, or `needs_review`. |
| `reason_code` | text | Machine-readable reason. |

## `link.station_selection`

| Column | Type | Meaning |
| --- | --- | --- |
| `station_selection_id` | text | Stable station-selection identifier. |
| `plant_id` | text | Internal plant key. |
| `calculation_run_id` | text | Selection run lineage. |
| `methodology_version` | text | Methodology version. |
| `selection_status` | text | `algorithmic`, `manual_reviewed`, `provisional`, or `blocked`. |
| `decision_basis` | text | Human-readable selection rule or blocking reason. |
| `reviewer` | text | Optional reviewer identifier for future manual review. |
| `notes` | text | Selection caveat or review note. |

## `link.station_selection_segment`

| Column | Type | Meaning |
| --- | --- | --- |
| `station_selection_segment_id` | text | Stable station-selection segment identifier. |
| `station_selection_id` | text | Parent station selection. |
| `station_id` | text | Selected NOAA ISD station. |
| `segment_start_utc` | timestamptz | First UTC timestamp covered by the selected-station segment. |
| `segment_end_utc` | timestamptz | Last UTC timestamp covered by the selected-station segment. |
| `reason_code` | text | Machine-readable reason for the segment. |
| `notes` | text | Segment caveat or selection detail. |

## `calc.coverage_blocker_raw_canonical_gap_summary`

| Column | Type | Meaning |
| --- | --- | --- |
| `raw_canonical_audit_run_id` | text | Raw-vs-canonical audit run lineage. |
| `gap_audit_run_id` | text | Near-threshold station-year gap audit used as input. |
| `priority_run_id` | text | Normalized active-window blocker priority run used as input. |
| `coverage_run_id` | text | Station-year coverage run used as input. |
| `inventory_run_id` | text | Raw-file inventory run used as input. |
| `station_id` | text | NOAA ISD station ID in `USAF-WBAN` form. |
| `station_name` | text | Station name from the gap audit. |
| `station_state` | text | Station state or region from the gap audit. |
| `station_country` | text | Station country from the gap audit. |
| `source_year` | integer | NOAA Global Hourly source year. |
| `impacted_plant_count` | bigint | Count of near-threshold plant blockers tied to the station-year's station. |
| `raw_file_path` | text | Local raw NOAA CSV inspected by the audit. |
| `raw_file_size_bytes` | bigint | Size of the inspected local raw file. |
| `coverage_status` | text | Prior station-year coverage status. |
| `loaded_file_count` | bigint | Loaded raw files contributing to the prior station-year coverage row. |
| `gap_table_expected_hours` | bigint | Normalized active-window expected DJF hours from the prior gap table. |
| `gap_table_valid_hours` | bigint | Full station-year valid DJF hours from the prior coverage table. |
| `gap_table_missing_hours` | bigint | Prior count-based missing hours for the station-year. |
| `expected_window_hour_count` | bigint | Exact selected normalized expected-window canonical UTC hours audited. |
| `canonical_present_expected_window_hours` | bigint | Expected-window hours present in `weather.hourly_djf`. |
| `canonical_missing_expected_window_hours` | bigint | Expected-window hours absent from `weather.hourly_djf`. |
| `window_missing_minus_gap_table_missing_hours` | bigint | Difference between exact expected-window missing hours and the prior count-based gap. |
| `expected_window_candidate_count` | integer | Number of priority rows with the selected expected-window hour count. |
| `expected_window_ambiguous` | boolean | Whether multiple priority rows tied for the selected expected-window count. |
| `expected_window_mismatch_hours` | bigint | Difference between selected expected-window hours and the prior expected count. |
| `raw_djf_row_count` | bigint | Raw NOAA rows in December, January, or February. |
| `raw_hour_observed_count` | bigint | Distinct canonical DJF hours with at least one raw row. |
| `raw_accepted_hour_count` | bigint | Distinct canonical DJF hours with at least one row that passes current loader rules. |
| `source_hour_absent_count` | bigint | Missing expected-window hours with no raw row in the local NOAA file. |
| `loader_rejected_source_hour_count` | bigint | Missing expected-window hours where all raw rows were rejected by NOAA source-code policy. |
| `loader_invalid_tmp_hour_count` | bigint | Missing expected-window hours with raw rows but invalid, sentinel, malformed, or quality-code-9 `TMP`. |
| `loader_rejected_plausibility_hour_count` | bigint | Missing expected-window hours with parsed temperatures outside the configured plausibility range. |
| `accepted_raw_not_in_canonical_hour_count` | bigint | Missing expected-window hours where at least one raw row would pass loader rules but is absent from `weather.hourly_djf`. |
| `raw_present_unclassified_hour_count` | bigint | Missing expected-window hours with raw rows that do not fit another reason bucket. |
| `primary_root_cause` | text | Largest missing-hour reason bucket for the station-year. |
| `raw_parse_error` | text | Raw-file parse error when applicable. |
| `notes` | text | Audit caveat or rule summary. |

## `calc.coverage_blocker_raw_canonical_station_summary`

| Column | Type | Meaning |
| --- | --- | --- |
| `raw_canonical_audit_run_id` | text | Raw-vs-canonical audit run lineage. |
| `gap_audit_run_id` | text | Near-threshold station-year gap audit used as input. |
| `station_id` | text | NOAA ISD station ID in `USAF-WBAN` form. |
| `station_name` | text | Station name from the gap audit. |
| `station_state` | text | Station state or region from the gap audit. |
| `station_country` | text | Station country from the gap audit. |
| `station_year_count` | bigint | Station-year rows audited for the station. |
| `impacted_plant_count` | bigint | Count of near-threshold plant blockers tied to the station. |
| `gap_table_missing_hours` | bigint | Sum of prior count-based missing hours. |
| `canonical_missing_expected_window_hours` | bigint | Sum of exact expected-window hours absent from `weather.hourly_djf`. |
| `window_missing_minus_gap_table_missing_hours` | bigint | Difference between exact expected-window missing hours and prior count-based gap hours. |
| `source_hour_absent_count` | bigint | Station-level sum of raw source-hour absences. |
| `loader_rejected_source_hour_count` | bigint | Station-level sum of source-code rejection blockers. |
| `loader_invalid_tmp_hour_count` | bigint | Station-level sum of invalid or missing NOAA `TMP` blockers. |
| `loader_rejected_plausibility_hour_count` | bigint | Station-level sum of plausibility rejection blockers. |
| `accepted_raw_not_in_canonical_hour_count` | bigint | Station-level sum of accepted raw rows absent from canonical hourly data. |
| `raw_present_unclassified_hour_count` | bigint | Station-level sum of raw-present missing hours that do not fit another reason bucket. |
| `accepted_raw_not_in_canonical_year_count` | bigint | Station-years with at least one accepted raw row absent from canonical hourly data. |
| `expected_window_mismatch_year_count` | bigint | Station-years where selected exact expected-window count does not match the prior gap table count. |
| `top_missing_years` | text | Compact year:hour list for the highest-missing station-years. |
| `primary_root_cause` | text | Largest missing-hour reason bucket for the station. |

## `calc.expanded_candidate_coverage_scenario_plant`

| Column | Type | Meaning |
| --- | --- | --- |
| `scenario_run_id` | text | Expanded-candidate scenario run lineage. |
| `priority_run_id` | text | Normalized active-window blocker priority run used as input. |
| `coverage_run_id` | text | Station-year coverage run used to calculate candidate coverage metrics. |
| `station_ecwt_run_id` | text | Station ECWT run used to require provisional ECWT availability. |
| `plant_id` | text | Internal plant key. |
| `eia_plant_code` | text | EIA plant code. |
| `plant_name` | text | EIA plant name. |
| `plant_state` | text | Plant state. |
| `priority_rank` | integer | Rank from the normalized active-window blocker queue. |
| `priority_bucket` | text | Near-threshold bucket such as `gap_le_24h` or `gap_le_168h`. |
| `valid_hour_gap_to_threshold` | bigint | Additional valid DJF hours needed for the current selected station to reach the configured threshold. |
| `current_station_id` | text | Current best selected candidate station in the blocker priority row. |
| `current_distance_km` | numeric | Distance from plant to current station. |
| `current_rank_order` | integer | Current station candidate rank from `link.station_candidate`. |
| `current_normalized_coverage_ratio` | numeric | Current station normalized active-window coverage ratio. |
| `current_normalized_loaded_year_ratio` | numeric | Current station normalized active-window loaded-year ratio. |
| `search_radius_km` | numeric | Maximum expanded-search radius used by the scenario. |
| `stations_searched_within_radius` | bigint | Loaded provisional-ECWT stations evaluated within the maximum radius. |
| `passing_station_count_within_radius` | bigint | Evaluated stations within the maximum radius passing both coverage and loaded-year gates. |
| `nearest_pass_radius_bucket_km` | numeric | Smallest configured radius bucket containing the nearest passing station. |
| `nearest_pass_rank_order_within_radius` | integer | Rank of the nearest passing station among loaded stations sorted by plant distance. |
| `nearest_pass_rank_order_all_stations` | integer | Rank of the nearest passing station among all geocoded NOAA station-history rows sorted by plant distance; this approximates the official nearest-station candidate-generator rank. |
| `nearest_pass_station_id` | text | Nearest expanded-search station passing the scenario gates. |
| `nearest_pass_distance_km` | numeric | Distance from plant to nearest passing expanded station. |
| `nearest_pass_normalized_coverage_ratio` | numeric | Normalized active-window coverage ratio for the nearest passing station. |
| `nearest_pass_normalized_loaded_year_ratio` | numeric | Normalized active-window loaded-year ratio for the nearest passing station. |
| `nearest_pass_station_ecwt_f` | numeric | Continuous station ECWT in Fahrenheit for the nearest passing station. |
| `scenario_status` | text | `expanded_candidate_passes_coverage_gate` or `no_passing_station_within_search_radius`. |
| `notes` | text | Scenario caveat; these rows do not alter official station selection. |

## `calc.expanded_candidate_coverage_scenario_radius_summary`

| Column | Type | Meaning |
| --- | --- | --- |
| `scenario_run_id` | text | Expanded-candidate scenario run lineage. |
| `radius_km` | numeric | Radius bucket evaluated. |
| `plant_count` | bigint | Near-threshold plants audited. |
| `plants_with_passing_station` | bigint | Plants with at least one passing expanded station at or within the radius. |
| `plants_without_passing_station` | bigint | Plants without a passing expanded station at or within the radius. |
| `pass_rate` | numeric | Plants with passing station divided by total audited plants. |
| `median_nearest_pass_distance_km` | numeric | Median nearest passing-station distance among pass rows. |
| `median_nearest_pass_rank_order` | numeric | Median nearest passing-station rank among loaded stations. |
| `median_nearest_pass_all_station_rank_order` | numeric | Median nearest passing-station rank among all geocoded NOAA station-history rows. |

## `calc.expanded_candidate_coverage_scenario_state_summary`

| Column | Type | Meaning |
| --- | --- | --- |
| `scenario_run_id` | text | Expanded-candidate scenario run lineage. |
| `plant_state` | text | Plant state. |
| `plant_count` | bigint | Near-threshold plants audited in the state. |
| `plants_with_passing_station_within_search_radius` | bigint | Plants in the state with a passing station within the maximum scenario radius. |
| `nearest_pass_radius_buckets` | text | Compact radius-bucket distribution for nearest passing stations. |
| `median_nearest_pass_distance_km` | numeric | Median nearest passing-station distance for pass rows in the state. |
| `max_nearest_pass_distance_km` | numeric | Maximum nearest passing-station distance for pass rows in the state. |

## `calc.plant_ecwt`

| Column | Type | Meaning |
| --- | --- | --- |
| `plant_ecwt_id` | text | Stable ECWT result identifier. |
| `plant_id` | text | Internal plant key. |
| `calculation_run_id` | text | Run lineage. |
| `methodology_version` | text | Methodology version. |
| `calculation_cutoff_utc` | timestamptz | Latest timestamp considered. |
| `valid_hour_count` | bigint | Count of valid hourly dry-bulb temperatures used. |
| `expected_hour_count` | bigint | Expected DJF hours for the window. |
| `missing_hour_count` | bigint | Missing expected hours. |
| `duplicate_hour_count` | bigint | Duplicate or excess observations. |
| `percentile_target` | numeric | Usually `0.002`. |
| `ecwt_f` | numeric | Continuous percentile ECWT in Fahrenheit. |
| `ecwt_c` | numeric | Continuous percentile ECWT in Celsius. |
| `discrete_rank` | integer | `ceil(percentile_target * valid_hour_count)`. |
| `ecwt_discrete_f` | numeric | Temperature at discrete audit rank. |
| `governing_ecwt_f` | numeric | Lowest accepted ECWT for the plant across accepted runs. |
| `result_status` | text | `accepted`, `provisional`, `blocked`, or `superseded`. |

## `calc.plant_ecwt_readiness`

| Column | Type | Meaning |
| --- | --- | --- |
| `plant_ecwt_readiness_id` | text | Stable readiness row identifier. |
| `plant_ecwt_id` | text | Plant ECWT row being classified. |
| `plant_id` | text | Internal plant key. |
| `calculation_run_id` | text | Readiness run lineage. |
| `methodology_version` | text | Methodology version. |
| `selected_station_id` | text | Selected NOAA station used by the plant ECWT row. |
| `selected_station_distance_km` | numeric | Distance from plant to selected station used by automated representativeness gates. |
| `selected_station_elevation_delta_m` | numeric | Selected station elevation minus plant elevation when available, used by automated representativeness gates. |
| `station_first_observation_utc` | timestamptz | First known station observation timestamp used to block single-station fixed-period rows whose station metadata begins after the fixed calculation period start. |
| `valid_hour_count` | bigint | Valid DJF dry-bulb hours in the plant ECWT row. |
| `expected_hour_count` | bigint | Expected DJF hours in the selected coverage window. |
| `coverage_ratio` | numeric | Valid divided by expected hours. |
| `min_valid_hour_threshold` | bigint | Gate threshold used by this readiness run. |
| `min_coverage_ratio_threshold` | numeric | Gate threshold used by this readiness run. |
| `max_station_distance_km_threshold` | numeric | Maximum selected-station distance allowed by the automated representativeness gate. |
| `max_elevation_delta_m_threshold` | numeric | Maximum absolute station elevation delta allowed by the automated representativeness gate when elevation is available. |
| `readiness_status` | text | `publication_candidate`, `provisional_low_coverage`, or `blocked`. |
| `reason_code` | text | Machine-readable reason for the readiness status. |
| `notes` | text | Readiness caveat or rule summary. |

## `audit.exception_log`

| Column | Type | Meaning |
| --- | --- | --- |
| `exception_id` | text | Stable exception identifier. |
| `calculation_run_id` | text | Run lineage. |
| `entity_type` | text | `plant`, `generator`, `station`, `source_file`, or `calculation`. |
| `entity_id` | text | Identifier for the affected entity. |
| `severity` | text | `info`, `warning`, `error`, or `blocker`. |
| `reason_code` | text | Machine-readable reason. |
| `message` | text | Human-readable explanation. |
| `resolution_status` | text | `open`, `resolved`, `accepted_risk`, or `blocked`. |
