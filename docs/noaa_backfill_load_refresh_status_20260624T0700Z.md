# NOAA Backfill, Load, And ECWT Refresh Status

Generated UTC: 2026-06-24T07:00Z

Database: `eop012` on `127.0.0.1:5436`

## Summary

This cycle ran AWS backfill batch 26 in parallel with another inventory load, then loaded the new batch 26 downloads and refreshed coverage, station ECWT, corrected plant ECWT, and fixed-denominator plant readiness.

The fixed-denominator strict publication count remained `71`. The relaxed diagnostic count increased from `2,488` to `2,516`.

| Metric | Value |
| --- | ---: |
| Plant ECWT rows | 16,132 |
| Strict publication candidates | 71 |
| Strict provisional low coverage | 16,033 |
| Strict blocked | 28 |
| Diagnostic publication candidates at 0.25 coverage | 2,516 |
| Diagnostic provisional low coverage at 0.25 coverage | 13,588 |
| Diagnostic blocked | 28 |

## NOAA Progress

Completed AWS backfill batch:

| Batch | Run ID | Downloaded | HTTP failures | Bytes | Elapsed seconds |
| ---: | --- | ---: | ---: | ---: | ---: |
| 26 | `noaa_backfill_download_batch26_20260624T063701Z` | 543 | 457 | 4,344,936,888 | 551.527 |

Completed NOAA loads:

| Run ID | Source | Files | Canonical DJF Hours | Invalid Temp Rows | Rejected SOURCE Rows | Rejected Plausibility Rows | Duplicate Hour Count |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `noaa_hourly_djf_load_20260624T063700Z` | inventory | 1,000 | 327,612 | 94,410 | 3,519,409 | 0 | 109,226 |
| `noaa_hourly_djf_load_20260624T064654Z` | downloaded | 543 | 430,058 | 68,879 | 1,205,070 | 1 | 877,631 |

Plausibility rejection detail:

| Run ID | Station | Year | Rejected Plausibility Rows | Source File ID |
| --- | --- | ---: | ---: | --- |
| `noaa_hourly_djf_load_20260624T064654Z` | `720346-53991` | 2008 | 1 | `noaa_global_hourly_csv_2008_72034653991_7c26432a1f1ae0a6` |

Current NOAA/cache status:

| Metric | Value |
| --- | ---: |
| AWS CSV files | 16,122 |
| AWS `.part` files | 0 |
| AWS cache disk usage | 126 GB |
| Manifest downloaded rows | 16,122 |
| Manifest failed rows | 9,878 |
| Manifest planned rows | 60,839 |
| Manifest skipped rows | 86,839 |

## Refreshed Result Runs

| Layer | Run ID | Rows / Result |
| --- | --- | ---: |
| Station-year coverage | `station_year_djf_coverage_20260624T065003Z` | 35,122 rows; 5,106 complete, 29,227 partial, 789 empty |
| Station ECWT | `station_ecwt_loaded_20260624T065337Z` | 3,108 provisional, 81 blocked |
| Plant ECWT | `plant_ecwt_provisional_20260624T065532Z` | 16,104 provisional, 28 blocked |
| Strict plant readiness | `plant_ecwt_readiness_20260624T065552Z` | 71 publication candidates |
| Diagnostic plant readiness | `plant_ecwt_readiness_20260624T065624Z` | 2,516 diagnostic candidates |

Current canonical weather:

| Metric | Value |
| --- | ---: |
| `weather.hourly_djf` rows | 21,476,954 |
| Distinct stations | 3,108 |
| Minimum dry-bulb F | -61.600 |
| Maximum dry-bulb F | 104.000 |
| `SHEF` rows below `-50 C` | 0 |
| Database size | 9,243 MB |

## Stability Checks

Compared with the previous corrected plant run `plant_ecwt_provisional_20260624T063217Z`:

| Check | Plants |
| --- | ---: |
| Selected station unchanged | 16,130 |
| Selected station changed | 2 |

Compared with previous strict readiness `plant_ecwt_readiness_20260624T063246Z`:

| Transition | Plants |
| --- | ---: |
| Strict candidate remained candidate | 71 |
| Strict low coverage remained low coverage | 16,033 |
| Strict blocked remained blocked | 28 |

Compared with previous diagnostic readiness `plant_ecwt_readiness_20260624T063302Z`:

| Transition | Plants |
| --- | ---: |
| Diagnostic candidate remained candidate | 2,486 |
| Diagnostic candidate became low coverage | 2 |
| Diagnostic low coverage became candidate | 30 |
| Diagnostic low coverage remained low coverage | 13,586 |
| Diagnostic blocked remained blocked | 28 |

## Interpretation

- Batch 26 added `543` NOAA CSVs and there are no `.part` files left in the cache.
- The hardened `SHEF < -50 C` plausibility rule held through this cycle.
- Fixed-denominator strict readiness remained at `71` publication candidates.
- Fixed-denominator diagnostic readiness improved from `2,488` to `2,516` candidates.
- One physically implausible row was rejected from station `720346-53991` for 2008.
- The immediate next step is to continue the parallel download/load/refresh cycle with batch 27.
