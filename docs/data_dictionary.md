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

