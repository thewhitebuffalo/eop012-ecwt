# NOAA Backfill, Load, And ECWT Refresh Status

Generated UTC: 2026-06-24T10:41Z

Database: `eop012` on `127.0.0.1:5436`

## Summary

This cycle ran AWS backfill batch 35 in parallel with another inventory load, then loaded the new batch 35 downloads and refreshed coverage, station ECWT, corrected plant ECWT, and fixed-denominator plant readiness.

The fixed-denominator strict publication count increased from `267` to `318`. The relaxed diagnostic count increased from `4,585` to `4,608`.

| Metric | Value |
| --- | ---: |
| Plant ECWT rows | 16,132 |
| Strict publication candidates | 318 |
| Strict provisional low coverage | 15,786 |
| Strict blocked | 28 |
| Diagnostic publication candidates at 0.25 coverage | 4,608 |
| Diagnostic provisional low coverage at 0.25 coverage | 11,496 |
| Diagnostic blocked | 28 |

## NOAA Progress

Completed AWS backfill batch:

| Batch | Run ID | Downloaded | HTTP failures | Exception failures | Bytes | Elapsed seconds |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 35 | `noaa_backfill_download_batch35_20260624T102440Z` | 309 | 691 | 0 | 1,842,538,465 | 240.794 |

Completed NOAA loads:

| Run ID | Source | Files | Canonical DJF Hours | Invalid Temp Rows | Rejected SOURCE Rows | Rejected Plausibility Rows | Duplicate Hour Count |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `noaa_hourly_djf_load_20260624T102440Z` | inventory | 561 | 566,043 | 47,971 | 1,037,560 | 0 | 1,174,724 |
| `noaa_hourly_djf_load_20260624T102927Z` | downloaded | 309 | 368,511 | 121,789 | 257,283 | 0 | 299,414 |

Plausibility rejection detail: none in this cycle.

Current NOAA/cache status:

| Metric | Value |
| --- | ---: |
| AWS CSV files | 19,909 |
| AWS `.part` files | 0 |
| AWS cache disk usage | 153 GB |
| Manifest downloaded rows | 19,909 |
| Manifest failed rows | 15,091 |
| Manifest planned rows | 51,839 |
| Manifest skipped rows | 86,839 |

## Refreshed Result Runs

| Layer | Run ID | Rows / Result |
| --- | --- | ---: |
| Station-year coverage | `station_year_djf_coverage_20260624T103241Z` | 47,470 rows; 8,519 complete, 37,899 partial, 1,052 empty |
| Station ECWT | `station_ecwt_loaded_20260624T103657Z` | 3,635 provisional, 105 blocked |
| Plant ECWT | `plant_ecwt_provisional_20260624T103934Z` | 16,104 provisional, 28 blocked |
| Strict plant readiness | `plant_ecwt_readiness_20260624T104012Z` | 318 publication candidates |
| Diagnostic plant readiness | `plant_ecwt_readiness_20260624T104030Z` | 4,608 diagnostic candidates |

Current canonical weather:

| Metric | Value |
| --- | ---: |
| `weather.hourly_djf` rows | 32,351,280 |
| Distinct stations | 3,635 |
| Minimum dry-bulb F | -61.600 |
| Maximum dry-bulb F | 104.000 |
| `SHEF` rows below `-50 C` | 0 |
| Database size | 13 GB |

## Stability Checks

Compared with the previous corrected plant run `plant_ecwt_provisional_20260624T101640Z`:

| Check | Plants |
| --- | ---: |
| Selected station unchanged | 16,095 |
| Selected station changed | 37 |

Compared with previous strict readiness `plant_ecwt_readiness_20260624T101730Z`:

| Transition | Plants |
| --- | ---: |
| Strict candidate remained candidate | 267 |
| Strict low coverage became candidate | 51 |
| Strict low coverage remained low coverage | 15,786 |
| Strict blocked remained blocked | 28 |

Compared with previous diagnostic readiness `plant_ecwt_readiness_20260624T101745Z`:

| Transition | Plants |
| --- | ---: |
| Diagnostic candidate remained candidate | 4,585 |
| Diagnostic low coverage became candidate | 23 |
| Diagnostic low coverage remained low coverage | 11,496 |
| Diagnostic blocked remained blocked | 28 |

## Interpretation

- Batch 35 added `309` NOAA CSVs and there are no `.part` files left in the cache.
- The inventory selector found only `561` remaining eligible files in this cycle, down from the normal `1,000` file cap.
- The hardened `SHEF < -50 C` plausibility rule held through this cycle.
- Fixed-denominator strict readiness improved from `267` to `318` publication candidates.
- Fixed-denominator diagnostic readiness improved from `4,585` to `4,608` candidates.
- No physically implausible rows were rejected in either batch-35 load.
- Station selection changed for `37` plants, lower than recent cycles, but station-selection churn remains a monitored QA signal while backfill coverage is incomplete.
- The immediate next step is to continue the parallel download/load/refresh cycle with batch 36.
