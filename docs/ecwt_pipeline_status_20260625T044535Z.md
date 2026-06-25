# ECWT Pipeline Status

Generated UTC: 2026-06-25T04:45:35Z

## Current Checkpoint

| Layer | Current run ID | Rows / status |
| --- | --- | ---: |
| NOAA raw inventory | `noaa_raw_file_inventory_20260625T043845Z` | 62,318 available station-years |
| NOAA AWS backfill manifest | `noaa_backfill_manifest_20260625T043945Z` | 0 planned downloads |
| Station-year DJF coverage | `station_year_djf_coverage_20260625T035921Z` | 62,318 station-years |
| Station ECWT | `station_ecwt_loaded_20260625T042423Z` | 4,250 stations |
| Fixed-period plant ECWT | `plant_ecwt_provisional_fixed_period_20260625T043543Z` | 16,132 plants |
| Fixed-period readiness | `plant_ecwt_readiness_fixed_period_20260625T043609Z` | 162 publication candidates |

## Plant Readiness

| Status | Plants |
| --- | ---: |
| Publication candidate | 162 |
| Blocked | 15,970 |

## NOAA Backfill State

The corrected NOAA inventory includes every local NOAA raw root observed in the loader audit:

- `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly`
- `/Volumes/NOAA_CACHE/noaa-global-hourly-pds-full`
- `/Volumes/NOAA_CACHE/noaa-global-hourly-year-staging`
- `/Volumes/NOAA_CACHE/BACKUP_TO_DELETE_LATER_noaa-cache_2026-02-19/gh_2012_2022_p1_1000`

With those roots included, there are no remaining station-years that are all of:

- missing locally,
- active during the EOP-012 DJF weather window, and
- not already proven missing from the NOAA public AWS bucket.

The current AWS backfill queue is therefore exhausted under the active ECWT-targeted manifest policy.

## Remaining Blockers

| Blocker class | Plants |
| --- | ---: |
| `fixed_coverage_below_threshold` | 15,923 |
| `fixed_coverage_and_loaded_years_below_threshold` | 19 |
| `no_station_candidates` | 28 |

The next useful work is no longer bulk AWS download. It is station-selection and coverage-policy work:

1. Review whether the fixed `2000-2025`, 95% coverage, 20-loaded-year gate is the intended publication gate for every plant class.
2. Prioritize the 15,923 fixed-coverage blockers by best available coverage, distance, NERC region, and plant criticality.
3. Resolve the 28 no-candidate plants by fixing missing plant coordinates or excluding placeholder/unsited plant records from the publication universe.
4. Decide how to publish the 162 current publication candidates: as preview candidates, not final compliance output, until station-selection review is complete.

The 28 no-candidate plants are itemized in `no_candidate_plants_20260625T044535Z.csv`
and summarized in `no_candidate_plants_20260625T044535Z_report.md`. All 28 lack
plant coordinates and have only `CN` generator status.

The fixed-coverage blockers are summarized in
`fixed_coverage_threshold_diagnostic_20260625T044535Z.md`. No blocked plant has
best-candidate fixed-period coverage above 94%, so small coverage-threshold
relaxations do not materially change readiness.

## Guardrail Added

`scripts/inventory_noaa_raw_files.py` now auto-includes existing NOAA raw roots referenced by `weather.noaa_hourly_load_file`, unless `--no-include-loaded-roots` is supplied. This prevents an incremental rebuild from omitting a cache root and creating duplicate AWS download work.
