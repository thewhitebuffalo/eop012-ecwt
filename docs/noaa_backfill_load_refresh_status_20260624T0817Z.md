# NOAA Backfill, Load, And ECWT Refresh Status

Generated UTC: 2026-06-24T08:17Z

Database: `eop012` on `127.0.0.1:5436`

## Summary

This cycle ran AWS backfill batch 29 in parallel with another inventory load, then loaded the new batch 29 downloads and refreshed coverage, station ECWT, corrected plant ECWT, and fixed-denominator plant readiness.

The fixed-denominator strict publication count increased from `75` to `100`. The relaxed diagnostic count increased from `2,823` to `3,071`.

| Metric | Value |
| --- | ---: |
| Plant ECWT rows | 16,132 |
| Strict publication candidates | 100 |
| Strict provisional low coverage | 16,004 |
| Strict blocked | 28 |
| Diagnostic publication candidates at 0.25 coverage | 3,071 |
| Diagnostic provisional low coverage at 0.25 coverage | 13,033 |
| Diagnostic blocked | 28 |

## NOAA Progress

Completed AWS backfill batch:

| Batch | Run ID | Downloaded | HTTP failures | Bytes | Elapsed seconds |
| ---: | --- | ---: | ---: | ---: | ---: |
| 29 | `noaa_backfill_download_batch29_20260624T075432Z` | 495 | 505 | 4,431,029,180 | 464.343 |

Completed NOAA loads:

| Run ID | Source | Files | Canonical DJF Hours | Invalid Temp Rows | Rejected SOURCE Rows | Rejected Plausibility Rows | Duplicate Hour Count |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `noaa_hourly_djf_load_20260624T075431Z` | inventory | 1,000 | 1,087,183 | 153,538 | 1,963,429 | 0 | 3,264,448 |
| `noaa_hourly_djf_load_20260624T080258Z` | downloaded | 495 | 539,804 | 39,368 | 981,894 | 0 | 955,656 |

Plausibility rejection detail:

No rows were rejected by the configured plausibility limits in this cycle.

Current NOAA/cache status:

| Metric | Value |
| --- | ---: |
| AWS CSV files | 17,682 |
| AWS `.part` files | 0 |
| AWS cache disk usage | 137 GB |
| Manifest downloaded rows | 17,682 |
| Manifest failed rows | 11,318 |
| Manifest planned rows | 57,839 |
| Manifest skipped rows | 86,839 |

## Refreshed Result Runs

| Layer | Run ID | Rows / Result |
| --- | --- | ---: |
| Station-year coverage | `station_year_djf_coverage_20260624T080521Z` | 39,682 rows; 6,305 complete, 32,474 partial, 903 empty |
| Station ECWT | `station_ecwt_loaded_20260624T080856Z` | 3,128 provisional, 84 blocked |
| Plant ECWT | `plant_ecwt_provisional_20260624T081147Z` | 16,104 provisional, 28 blocked |
| Strict plant readiness | `plant_ecwt_readiness_20260624T081234Z` | 100 publication candidates |
| Diagnostic plant readiness | `plant_ecwt_readiness_20260624T081248Z` | 3,071 diagnostic candidates |

Current canonical weather:

| Metric | Value |
| --- | ---: |
| `weather.hourly_djf` rows | 25,588,625 |
| Distinct stations | 3,128 |
| Minimum dry-bulb F | -61.600 |
| Maximum dry-bulb F | 104.000 |
| `SHEF` rows below `-50 C` | 0 |
| Database size | 11 GB |

## Stability Checks

Compared with the previous corrected plant run `plant_ecwt_provisional_20260624T074807Z`:

| Check | Plants |
| --- | ---: |
| Selected station unchanged | 16,130 |
| Selected station changed | 2 |

Compared with previous strict readiness `plant_ecwt_readiness_20260624T074841Z`:

| Transition | Plants |
| --- | ---: |
| Strict candidate remained candidate | 75 |
| Strict low coverage became candidate | 25 |
| Strict low coverage remained low coverage | 16,004 |
| Strict blocked remained blocked | 28 |

Compared with previous diagnostic readiness `plant_ecwt_readiness_20260624T074850Z`:

| Transition | Plants |
| --- | ---: |
| Diagnostic candidate remained candidate | 2,823 |
| Diagnostic low coverage became candidate | 248 |
| Diagnostic low coverage remained low coverage | 13,033 |
| Diagnostic blocked remained blocked | 28 |

## Interpretation

- Batch 29 added `495` NOAA CSVs and there are no `.part` files left in the cache.
- The hardened `SHEF < -50 C` plausibility rule held through this cycle.
- Fixed-denominator strict readiness improved from `75` to `100` publication candidates.
- Fixed-denominator diagnostic readiness improved from `2,823` to `3,071` candidates.
- No physically implausible rows were rejected in this cycle.
- The immediate next step is to continue the parallel download/load/refresh cycle with batch 30.
