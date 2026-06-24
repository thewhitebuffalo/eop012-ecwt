# NOAA Backfill, Load, And ECWT Refresh Status

Generated UTC: 2026-06-24T00:56Z

Database: `eop012` on `127.0.0.1:5436`

## Summary

This cycle ran AWS backfill batch 13 in parallel with another inventory load, then loaded downloaded files and refreshed coverage, station ECWT, plant ECWT, and plant readiness.

Strict publication candidates increased from `169` to `203`. The dataset is still not publication-complete because most plants remain below the strict coverage threshold.

| Metric | Value |
| --- | ---: |
| Plant ECWT rows | 16,132 |
| Strict publication candidates | 203 |
| Strict provisional low coverage | 15,901 |
| Strict blocked | 28 |
| Diagnostic publication candidates at 0.25 coverage | 13,456 |
| Diagnostic provisional low coverage at 0.25 coverage | 2,648 |
| Diagnostic blocked | 28 |

## NOAA Progress

Completed AWS backfill batch:

| Batch | Run ID | Downloaded | HTTP failures | Bytes | Elapsed seconds |
| ---: | --- | ---: | ---: | ---: | ---: |
| 13 | `noaa_backfill_download_batch13_20260624T003410Z` | 655 | 345 | 5,938,532,225 | 655.119 |

Completed NOAA loads:

| Run ID | Source | Files | Canonical DJF Hours | Invalid Temp Rows | Rejected SOURCE Rows | Rejected Plausibility Rows | Duplicate Hour Count |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `noaa_hourly_djf_load_20260624T003409Z` | inventory | 1,000 | 393,660 | 76,848 | 3,334,115 | 0 | 375,671 |
| `noaa_hourly_djf_load_20260624T004532Z` | downloaded | 1,000 | 476,282 | 74,445 | 2,914,499 | 4 | 383,948 |

Current NOAA/cache status:

| Metric | Value |
| --- | ---: |
| AWS CSV files | 8,346 |
| AWS `.part` files | 0 |
| AWS cache disk usage | 64 GB |
| Manifest downloaded rows | 8,346 |
| Manifest failed rows | 4,654 |
| Manifest planned rows | 73,839 |
| Manifest skipped rows | 86,839 |

## Refreshed Result Runs

| Layer | Run ID | Rows / Result |
| --- | --- | ---: |
| Station-year coverage | `station_year_djf_coverage_20260624T005121Z` | 13,000 rows; 1,427 complete, 11,269 partial, 304 empty |
| Station ECWT | `station_ecwt_loaded_20260624T005228Z` | 2,883 provisional, 73 blocked |
| Plant ECWT | `plant_ecwt_provisional_20260624T005417Z` | 16,104 provisional, 28 blocked |
| Strict plant readiness | `plant_ecwt_readiness_20260624T005455Z` | 203 publication candidates |
| Diagnostic plant readiness | `plant_ecwt_readiness_20260624T005510Z` | 13,456 diagnostic candidates |

Current canonical weather:

| Metric | Value |
| --- | ---: |
| `weather.hourly_djf` rows | 7,940,480 |
| Distinct stations | 2,883 |
| Minimum dry-bulb F | -61.060 |
| Maximum dry-bulb F | 104.000 |
| Database size | 3,577 MB |

## Operational Note

The strict and diagnostic readiness scripts should be run serially. A parallel attempt hit a PostgreSQL deadlock on shared audit/index writes; the diagnostic run was retried serially and completed as `plant_ecwt_readiness_20260624T005510Z`.

## Interpretation

- Strict readiness is improving, but slowly: `203` plants currently meet the provisional publication-candidate gate.
- The dominant blocker remains weather coverage: `15,901` plants are still below the strict coverage threshold.
- The relaxed diagnostic gate rose from `13,384` to `13,456` candidates.
- The immediate next step remains another parallel download/load/refresh cycle, with readiness writes kept serial.
