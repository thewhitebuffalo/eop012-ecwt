# NOAA Backfill, Load, And Policy Refresh

Generated UTC: 2026-06-25T16:17:43Z

## Source Runs

- Raw-file inventory run ID: `noaa_raw_file_inventory_20260625T153854Z`
- Backfill manifest run ID: `noaa_backfill_manifest_20260625T154422Z`
- NOAA DJF load runs: `noaa_hourly_djf_load_20260625T154554Z` through `noaa_hourly_djf_load_20260625T155515Z`
- Station-year coverage run ID: `station_year_djf_coverage_20260625T155613Z`
- Station ECWT run ID: `station_ecwt_loaded_20260625T155645Z`
- Fixed-period plant ECWT run ID: `plant_ecwt_provisional_fixed_period_20260625T161041Z`
- Fixed-period readiness run ID: `plant_ecwt_readiness_fixed_period_20260625T161109Z`
- Denominator diagnostic run ID: `fixed_period_denominator_diagnostic_all-plants_20260625T161153Z`
- Policy scenario DB load run ID: `readiness_policy_scenarios_db_load_20260625T161252Z`
- Policy result run ID: `plant_ecwt_policy_result_all_plants_normalized_active_window_loaded_year_20260625T161313Z`
- Secondary station fill run ID: `secondary_station_fill_ecwt_20260625T161345Z`
- Scoped release ID: `scoped_plant_ecwt_release_20260625T161629Z`

## Backfill Closure

The fresh raw-file inventory found 133,952 candidate station-years:

| Inventory Status | Station-Years |
| --- | ---: |
| Available locally | 73,979 |
| Missing locally before filters | 59,973 |

The fresh manifest applied the hardened filters:

| Manifest Filter | Rows |
| --- | ---: |
| Missing inventory rows | 59,973 |
| DJF active-window eligible rows | 4,281 |
| DJF active-window excluded rows | 55,692 |
| Known terminal AWS 404 rows | 45,497 |
| Planned rows after filters | 0 |

Interpretation: under the configured NOAA roots, station active-window filter, and terminal AWS 404 exclusion, there are no remaining NOAA public AWS download candidates.

## Available-File Load Closure

Before this refresh, 1,356 available station-years in the fresh inventory had no loaded station-year audit row. They were loaded in auditable batches through `load_noaa_hourly_djf.py`.

| Load Metric | Count |
| --- | ---: |
| Files loaded | 1,356 |
| File failures | 0 |
| Canonical DJF hours loaded | 2,057,523 |
| Invalid temperature rows rejected | 107,261 |
| Source-code rows rejected | 249,852 |
| Duplicate station-hour observations collapsed | 811,987 |
| Available inventory station-years still without a load row | 0 |

## Refreshed Weather Tables

| Table/Result | Count |
| --- | ---: |
| Station-year coverage rows | 73,979 |
| Complete station-years | 19,528 |
| Station ECWT rows | 4,936 |
| Provisional station ECWT rows | 4,707 |

## Refreshed Plant Policy Result

| Status | Reason | Rows |
| --- | --- | ---: |
| `publication_candidate` | `passes_current_fixed_period_gate` | 1,868 |
| `publication_candidate` | `passes_normalized_active_window_policy` | 14,222 |
| `blocked` | `no_station_candidates` | 28 |
| `blocked` | `normalized_active_window_coverage_below_threshold` | 14 |

Compared with the prior policy result, one Alaska plant, Yakutat, moved out of the blocked low-coverage bucket.

## Scoped Release

The current user-approved publication scope excludes Alaska and the 28 no-station edge cases. The refreshed scoped release remains complete:

| Scoped Release Metric | Rows |
| --- | ---: |
| Policy-result rows included directly | 15,943 |
| Secondary-fill Texas rows included | 4 |
| Scoped ready rows | 15,947 |
| Scoped exclusions | 185 |

The scoped release CSV is `data/processed/scoped_plant_ecwt_release_20260625T161629Z.csv`.
