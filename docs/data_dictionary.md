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

## `weather.hourly_djf`

| Column | Type | Meaning |
| --- | --- | --- |
| `station_id` | text | Canonical NOAA ISD station identifier. |
| `hour_ending_utc` | timestamptz | Canonical UTC station-hour used for ECWT-oriented DJF weather analysis. Current loader policy floors the NOAA observation timestamp to the UTC hour. |
| `hour_local` | timestamp | Reserved for local station-hour once timezone handling is added. |
| `dry_bulb_c` | numeric | Dry-bulb temperature in degrees C parsed from NOAA Global Hourly `TMP`. |
| `dry_bulb_f` | numeric | Dry-bulb temperature in degrees F. |
| `source_file_id` | text | Source file lineage. Downloaded AWS files have per-file lineage; preexisting local-inventory files currently use the inventory source-root lineage. |
| `quality_flags` | text[] | Loader-retained NOAA quality context, such as TMP quality code, report type, source code, and quality-control code. |
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
| `djf_rows_seen` | bigint | Rows whose observation timestamp is in December, January, or February. |
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
| `source_year` | integer | NOAA Global Hourly source year. |
| `calculation_run_id` | text | Coverage-build run lineage. |
| `period_start_utc` | timestamptz | Start of the source calendar year. |
| `period_end_utc` | timestamptz | End of the source calendar year. |
| `expected_djf_hours` | bigint | Expected UTC hours in January, February, and December for the source year. |
| `valid_djf_hours` | bigint | Canonical loaded DJF hours available for the station-year. |
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
| `manifest_status` | text | `planned`, `downloaded`, `skipped`, or `failed`. |
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
| `download_status` | text | `downloaded`, `skipped_existing`, `failed_http`, `failed_exception`, or `dry_run`. |
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
