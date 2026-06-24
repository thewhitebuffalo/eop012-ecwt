# NOAA Backfill, Load, And ECWT Refresh Status

Generated UTC: 2026-06-24T08:44Z

Database: `eop012` on `127.0.0.1:5436`

## Summary

This cycle ran AWS backfill batch 30 in parallel with another inventory load, then loaded the new batch 30 downloads and refreshed coverage, station ECWT, corrected plant ECWT, and fixed-denominator plant readiness.

The fixed-denominator strict publication count remained `100`. The relaxed diagnostic count increased from `3,071` to `3,289`.

| Metric | Value |
| --- | ---: |
| Plant ECWT rows | 16,132 |
| Strict publication candidates | 100 |
| Strict provisional low coverage | 16,004 |
| Strict blocked | 28 |
| Diagnostic publication candidates at 0.25 coverage | 3,289 |
| Diagnostic provisional low coverage at 0.25 coverage | 12,815 |
| Diagnostic blocked | 28 |

## NOAA Progress

Completed AWS backfill batch:

| Batch | Run ID | Downloaded | HTTP failures | Bytes | Elapsed seconds |
| ---: | --- | ---: | ---: | ---: | ---: |
| 30 | `noaa_backfill_download_batch30_20260624T082339Z` | 417 | 583 | 3,807,036,434 | 436.953 |

Completed NOAA loads:

| Run ID | Source | Files | Canonical DJF Hours | Invalid Temp Rows | Rejected SOURCE Rows | Rejected Plausibility Rows | Duplicate Hour Count |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `noaa_hourly_djf_load_20260624T082339Z` | inventory | 1,000 | 228,604 | 83,886 | 3,576,040 | 0 | 131,614 |
| `noaa_hourly_djf_load_20260624T083138Z` | downloaded | 417 | 422,313 | 37,451 | 769,634 | 0 | 886,977 |

Plausibility rejection detail:

No rows were rejected by the configured plausibility limits in this cycle.

Current NOAA/cache status:

| Metric | Value |
| --- | ---: |
| AWS CSV files | 18,099 |
| AWS `.part` files | 0 |
| AWS cache disk usage | 141 GB |
| Manifest downloaded rows | 18,099 |
| Manifest failed rows | 11,901 |
| Manifest planned rows | 56,839 |
| Manifest skipped rows | 86,839 |

## Refreshed Result Runs

| Layer | Run ID | Rows / Result |
| --- | --- | ---: |
| Station-year coverage | `station_year_djf_coverage_20260624T083424Z` | 41,099 rows; 6,474 complete, 33,715 partial, 910 empty |
| Station ECWT | `station_ecwt_loaded_20260624T083857Z` | 3,131 provisional, 84 blocked |
| Plant ECWT | `plant_ecwt_provisional_20260624T084134Z` | 16,104 provisional, 28 blocked |
| Strict plant readiness | `plant_ecwt_readiness_20260624T084240Z` | 100 publication candidates |
| Diagnostic plant readiness | `plant_ecwt_readiness_20260624T084258Z` | 3,289 diagnostic candidates |

Current canonical weather:

| Metric | Value |
| --- | ---: |
| `weather.hourly_djf` rows | 26,239,542 |
| Distinct stations | 3,131 |
| Minimum dry-bulb F | -61.600 |
| Maximum dry-bulb F | 104.000 |
| `SHEF` rows below `-50 C` | 0 |
| Database size | 11 GB |

## Stability Checks

Compared with the previous corrected plant run `plant_ecwt_provisional_20260624T081147Z`:

| Check | Plants |
| --- | ---: |
| Selected station unchanged | 16,128 |
| Selected station changed | 4 |

Compared with previous strict readiness `plant_ecwt_readiness_20260624T081234Z`:

| Transition | Plants |
| --- | ---: |
| Strict candidate remained candidate | 100 |
| Strict low coverage remained low coverage | 16,004 |
| Strict blocked remained blocked | 28 |

Compared with previous diagnostic readiness `plant_ecwt_readiness_20260624T081248Z`:

| Transition | Plants |
| --- | ---: |
| Diagnostic candidate remained candidate | 3,068 |
| Diagnostic candidate became low coverage | 3 |
| Diagnostic low coverage became candidate | 221 |
| Diagnostic low coverage remained low coverage | 12,812 |
| Diagnostic blocked remained blocked | 28 |

## Interpretation

- Batch 30 added `417` NOAA CSVs and there are no `.part` files left in the cache.
- The hardened `SHEF < -50 C` plausibility rule held through this cycle.
- Fixed-denominator strict readiness remained at `100` publication candidates.
- Fixed-denominator diagnostic readiness improved from `3,071` to `3,289` candidates.
- No physically implausible rows were rejected in this cycle.
- The immediate next step is to continue the parallel download/load/refresh cycle with batch 31.
