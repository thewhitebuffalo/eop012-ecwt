# NOAA Backfill, Load, And ECWT Refresh Status

Generated UTC: 2026-06-24T05:45Z

Database: `eop012` on `127.0.0.1:5436`

## Summary

This cycle ran AWS backfill batch 23 in parallel with another inventory load, then loaded the new batch 23 downloads and refreshed coverage, station ECWT, corrected plant ECWT, and fixed-denominator plant readiness.

The fixed-denominator strict publication count increased from `44` to `53`. The relaxed diagnostic count increased from `2,170` to `2,294`.

This cycle also hardened readiness performance. Fixed-denominator readiness initially ran in minutes because the query joined against historical plant station-selection rows without the right materialization and join indexes. The builder now creates the needed join indexes and materializes readiness inputs into analyzed temp tables. After that change, the strict gate ran in `7.38` seconds and the diagnostic gate ran in `1.35` seconds.

| Metric | Value |
| --- | ---: |
| Plant ECWT rows | 16,132 |
| Strict publication candidates | 53 |
| Strict provisional low coverage | 16,051 |
| Strict blocked | 28 |
| Diagnostic publication candidates at 0.25 coverage | 2,294 |
| Diagnostic provisional low coverage at 0.25 coverage | 13,810 |
| Diagnostic blocked | 28 |

## NOAA Progress

Completed AWS backfill batch:

| Batch | Run ID | Downloaded | HTTP failures | Bytes | Elapsed seconds |
| ---: | --- | ---: | ---: | ---: | ---: |
| 23 | `noaa_backfill_download_batch23_20260624T050914Z` | 610 | 390 | 5,004,860,108 | 531.181 |

Completed NOAA loads:

| Run ID | Source | Files | Canonical DJF Hours | Invalid Temp Rows | Rejected SOURCE Rows | Rejected Plausibility Rows | Duplicate Hour Count |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `noaa_hourly_djf_load_20260624T050913Z` | inventory | 1,000 | 329,475 | 72,310 | 3,530,598 | 0 | 297,739 |
| `noaa_hourly_djf_load_20260624T051830Z` | downloaded | 610 | 307,653 | 75,403 | 1,821,618 | 0 | 643,221 |

Current NOAA/cache status:

| Metric | Value |
| --- | ---: |
| AWS CSV files | 14,468 |
| AWS `.part` files | 0 |
| AWS cache disk usage | 112 GB |
| Manifest downloaded rows | 14,468 |
| Manifest failed rows | 8,532 |
| Manifest planned rows | 63,839 |
| Manifest skipped rows | 86,839 |

## Refreshed Result Runs

| Layer | Run ID | Rows / Result |
| --- | --- | ---: |
| Station-year coverage | `station_year_djf_coverage_20260624T052053Z` | 30,468 rows; 4,493 complete, 25,261 partial, 714 empty |
| Station ECWT | `station_ecwt_loaded_20260624T052456Z` | 3,095 provisional, 78 blocked |
| Plant ECWT | `plant_ecwt_provisional_20260624T052724Z` | 16,104 provisional, 28 blocked |
| Strict plant readiness | `plant_ecwt_readiness_20260624T054410Z` | 53 publication candidates |
| Diagnostic plant readiness | `plant_ecwt_readiness_20260624T054438Z` | 2,294 diagnostic candidates |

Current canonical weather:

| Metric | Value |
| --- | ---: |
| `weather.hourly_djf` rows | 18,999,794 |
| Distinct stations | 3,095 |
| Minimum dry-bulb F | -61.600 |
| Maximum dry-bulb F | 104.000 |
| `SHEF` rows below `-50 C` | 0 |
| Database size | 8,186 MB |

## Stability Checks

Compared with the previous corrected plant run `plant_ecwt_provisional_20260624T045441Z`:

| Check | Plants |
| --- | ---: |
| Selected station unchanged | 16,115 |
| Selected station changed | 17 |

Compared with previous strict readiness `plant_ecwt_readiness_20260624T050435Z`:

| Transition | Plants |
| --- | ---: |
| Strict candidate remained candidate | 44 |
| Strict low coverage became candidate | 9 |
| Strict low coverage remained low coverage | 16,051 |
| Strict blocked remained blocked | 28 |

Compared with previous diagnostic readiness `plant_ecwt_readiness_20260624T050443Z`:

| Transition | Plants |
| --- | ---: |
| Diagnostic candidate remained candidate | 2,165 |
| Diagnostic candidate became low coverage | 5 |
| Diagnostic low coverage became candidate | 129 |
| Diagnostic low coverage remained low coverage | 13,805 |
| Diagnostic blocked remained blocked | 28 |

## Code Hardening

| Commit | Change |
| --- | --- |
| `9296911` | Added indexes for plant readiness joins. |
| `219c91e` | Materialized fixed-denominator readiness inputs into analyzed temp tables. |

## Interpretation

- Batch 23 added `610` NOAA CSVs and there are no `.part` files left in the cache.
- The hardened `SHEF < -50 C` plausibility rule held through this cycle.
- Fixed-denominator strict readiness improved from `44` to `53` publication candidates.
- Readiness execution time is now acceptable for repeated batch cycles.
- The immediate next step is to continue the parallel download/load/refresh cycle with batch 24.
