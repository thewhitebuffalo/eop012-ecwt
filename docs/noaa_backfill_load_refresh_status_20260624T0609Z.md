# NOAA Backfill, Load, And ECWT Refresh Status

Generated UTC: 2026-06-24T06:09Z

Database: `eop012` on `127.0.0.1:5436`

## Summary

This cycle ran AWS backfill batch 24 in parallel with another inventory load, then loaded the new batch 24 downloads and refreshed coverage, station ECWT, corrected plant ECWT, and fixed-denominator plant readiness.

The fixed-denominator strict publication count remained `53`. The relaxed diagnostic count increased from `2,294` to `2,374`.

| Metric | Value |
| --- | ---: |
| Plant ECWT rows | 16,132 |
| Strict publication candidates | 53 |
| Strict provisional low coverage | 16,051 |
| Strict blocked | 28 |
| Diagnostic publication candidates at 0.25 coverage | 2,374 |
| Diagnostic provisional low coverage at 0.25 coverage | 13,730 |
| Diagnostic blocked | 28 |

## NOAA Progress

Completed AWS backfill batch:

| Batch | Run ID | Downloaded | HTTP failures | Bytes | Elapsed seconds |
| ---: | --- | ---: | ---: | ---: | ---: |
| 24 | `noaa_backfill_download_batch24_20260624T054922Z` | 569 | 431 | 5,216,938,911 | 608.765 |

Completed NOAA loads:

| Run ID | Source | Files | Canonical DJF Hours | Invalid Temp Rows | Rejected SOURCE Rows | Rejected Plausibility Rows | Duplicate Hour Count |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `noaa_hourly_djf_load_20260624T054922Z` | inventory | 1,000 | 693,753 | 78,297 | 2,881,485 | 0 | 2,886,566 |
| `noaa_hourly_djf_load_20260624T060001Z` | downloaded | 569 | 305,105 | 50,325 | 1,777,306 | 0 | 846,484 |

Current NOAA/cache status:

| Metric | Value |
| --- | ---: |
| AWS CSV files | 15,037 |
| AWS `.part` files | 0 |
| AWS cache disk usage | 117 GB |
| Manifest downloaded rows | 15,037 |
| Manifest failed rows | 8,963 |
| Manifest planned rows | 62,839 |
| Manifest skipped rows | 86,839 |

## Refreshed Result Runs

| Layer | Run ID | Rows / Result |
| --- | --- | ---: |
| Station-year coverage | `station_year_djf_coverage_20260624T060231Z` | 32,037 rows; 4,776 complete, 26,527 partial, 734 empty |
| Station ECWT | `station_ecwt_loaded_20260624T060552Z` | 3,097 provisional, 81 blocked |
| Plant ECWT | `plant_ecwt_provisional_20260624T060727Z` | 16,104 provisional, 28 blocked |
| Strict plant readiness | `plant_ecwt_readiness_20260624T060748Z` | 53 publication candidates |
| Diagnostic plant readiness | `plant_ecwt_readiness_20260624T060801Z` | 2,374 diagnostic candidates |

Current canonical weather:

| Metric | Value |
| --- | ---: |
| `weather.hourly_djf` rows | 19,998,652 |
| Distinct stations | 3,097 |
| Minimum dry-bulb F | -61.600 |
| Maximum dry-bulb F | 104.000 |
| `SHEF` rows below `-50 C` | 0 |
| Database size | 8,597 MB |

## Stability Checks

Compared with the previous corrected plant run `plant_ecwt_provisional_20260624T052724Z`:

| Check | Plants |
| --- | ---: |
| Selected station unchanged | 16,123 |
| Selected station changed | 9 |

Compared with previous strict readiness `plant_ecwt_readiness_20260624T054410Z`:

| Transition | Plants |
| --- | ---: |
| Strict candidate remained candidate | 53 |
| Strict low coverage remained low coverage | 16,051 |
| Strict blocked remained blocked | 28 |

Compared with previous diagnostic readiness `plant_ecwt_readiness_20260624T054438Z`:

| Transition | Plants |
| --- | ---: |
| Diagnostic candidate remained candidate | 2,294 |
| Diagnostic low coverage became candidate | 80 |
| Diagnostic low coverage remained low coverage | 13,730 |
| Diagnostic blocked remained blocked | 28 |

## Interpretation

- Batch 24 added `569` NOAA CSVs and there are no `.part` files left in the cache.
- The hardened `SHEF < -50 C` plausibility rule held through this cycle.
- Fixed-denominator strict readiness remained at `53` publication candidates.
- Fixed-denominator diagnostic readiness improved from `2,294` to `2,374` candidates.
- The optimized readiness path stayed fast: strict ran in `2.83` seconds and diagnostic ran in `7.13` seconds.
- The immediate next step is to continue the parallel download/load/refresh cycle with batch 25.
