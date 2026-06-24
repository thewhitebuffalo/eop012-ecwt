# NOAA Backfill, Load, And ECWT Refresh Status

Generated UTC: 2026-06-24T06:35Z

Database: `eop012` on `127.0.0.1:5436`

## Summary

This cycle ran AWS backfill batch 25 in parallel with another inventory load, then loaded the new batch 25 downloads and refreshed coverage, station ECWT, corrected plant ECWT, and fixed-denominator plant readiness.

The fixed-denominator strict publication count increased from `53` to `71`. The relaxed diagnostic count increased from `2,374` to `2,488`.

| Metric | Value |
| --- | ---: |
| Plant ECWT rows | 16,132 |
| Strict publication candidates | 71 |
| Strict provisional low coverage | 16,033 |
| Strict blocked | 28 |
| Diagnostic publication candidates at 0.25 coverage | 2,488 |
| Diagnostic provisional low coverage at 0.25 coverage | 13,616 |
| Diagnostic blocked | 28 |

## NOAA Progress

Completed AWS backfill batch:

| Batch | Run ID | Downloaded | HTTP failures | Bytes | Elapsed seconds |
| ---: | --- | ---: | ---: | ---: | ---: |
| 25 | `noaa_backfill_download_batch25_20260624T061220Z` | 542 | 458 | 4,944,929,434 | 604.812 |

Completed NOAA loads:

| Run ID | Source | Files | Canonical DJF Hours | Invalid Temp Rows | Rejected SOURCE Rows | Rejected Plausibility Rows | Duplicate Hour Count |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `noaa_hourly_djf_load_20260624T061220Z` | inventory | 1,000 | 331,336 | 71,334 | 3,885,223 | 0 | 292,643 |
| `noaa_hourly_djf_load_20260624T062258Z` | downloaded | 542 | 389,296 | 73,741 | 1,393,999 | 1 | 1,030,270 |

Plausibility rejection detail:

| Run ID | Station | Year | Rejected Plausibility Rows | Source File ID |
| --- | --- | ---: | ---: | --- |
| `noaa_hourly_djf_load_20260624T062258Z` | `724354-63815` | 2008 | 1 | `noaa_global_hourly_csv_2008_72435463815_c287fb65de5ac521` |

Current NOAA/cache status:

| Metric | Value |
| --- | ---: |
| AWS CSV files | 15,579 |
| AWS `.part` files | 0 |
| AWS cache disk usage | 122 GB |
| Manifest downloaded rows | 15,579 |
| Manifest failed rows | 9,421 |
| Manifest planned rows | 61,839 |
| Manifest skipped rows | 86,839 |

## Refreshed Result Runs

| Layer | Run ID | Rows / Result |
| --- | --- | ---: |
| Station-year coverage | `station_year_djf_coverage_20260624T062549Z` | 33,579 rows; 4,952 complete, 27,868 partial, 759 empty |
| Station ECWT | `station_ecwt_loaded_20260624T063008Z` | 3,105 provisional, 82 blocked |
| Plant ECWT | `plant_ecwt_provisional_20260624T063217Z` | 16,104 provisional, 28 blocked |
| Strict plant readiness | `plant_ecwt_readiness_20260624T063246Z` | 71 publication candidates |
| Diagnostic plant readiness | `plant_ecwt_readiness_20260624T063302Z` | 2,488 diagnostic candidates |

Current canonical weather:

| Metric | Value |
| --- | ---: |
| `weather.hourly_djf` rows | 20,719,284 |
| Distinct stations | 3,105 |
| Minimum dry-bulb F | -61.600 |
| Maximum dry-bulb F | 104.000 |
| `SHEF` rows below `-50 C` | 0 |
| Database size | 8,913 MB |

## Stability Checks

Compared with the previous corrected plant run `plant_ecwt_provisional_20260624T060727Z`:

| Check | Plants |
| --- | ---: |
| Selected station unchanged | 16,116 |
| Selected station changed | 16 |

Compared with previous strict readiness `plant_ecwt_readiness_20260624T060748Z`:

| Transition | Plants |
| --- | ---: |
| Strict candidate remained candidate | 53 |
| Strict low coverage became candidate | 18 |
| Strict low coverage remained low coverage | 16,033 |
| Strict blocked remained blocked | 28 |

Compared with previous diagnostic readiness `plant_ecwt_readiness_20260624T060801Z`:

| Transition | Plants |
| --- | ---: |
| Diagnostic candidate remained candidate | 2,365 |
| Diagnostic candidate became low coverage | 9 |
| Diagnostic low coverage became candidate | 123 |
| Diagnostic low coverage remained low coverage | 13,607 |
| Diagnostic blocked remained blocked | 28 |

## Interpretation

- Batch 25 added `542` NOAA CSVs and there are no `.part` files left in the cache.
- The hardened `SHEF < -50 C` plausibility rule held through this cycle.
- Fixed-denominator strict readiness improved from `53` to `71` publication candidates.
- Fixed-denominator diagnostic readiness improved from `2,374` to `2,488` candidates.
- One physically implausible row was rejected from station `724354-63815` for 2008.
- The immediate next step is to continue the parallel download/load/refresh cycle with batch 26.
