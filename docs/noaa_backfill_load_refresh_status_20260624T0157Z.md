# NOAA Backfill, Load, And ECWT Refresh Status

Generated UTC: 2026-06-24T01:57Z

Database: `eop012` on `127.0.0.1:5436`

## Summary

This cycle ran AWS backfill batch 15 in parallel with another inventory load, then loaded downloaded files and refreshed coverage, station ECWT, plant ECWT, and plant readiness.

Strict publication candidates increased from `204` to `367`. The dataset is still not publication-complete because most plants remain below the strict coverage threshold.

| Metric | Value |
| --- | ---: |
| Plant ECWT rows | 16,132 |
| Strict publication candidates | 367 |
| Strict provisional low coverage | 15,737 |
| Strict blocked | 28 |
| Diagnostic publication candidates at 0.25 coverage | 13,679 |
| Diagnostic provisional low coverage at 0.25 coverage | 2,425 |
| Diagnostic blocked | 28 |

## NOAA Progress

Completed AWS backfill batch:

| Batch | Run ID | Downloaded | HTTP failures | Bytes | Elapsed seconds |
| ---: | --- | ---: | ---: | ---: | ---: |
| 15 | `noaa_backfill_download_batch15_20260624T012102Z` | 626 | 374 | 5,814,093,998 | 484.217 |

Completed NOAA loads:

| Run ID | Source | Files | Canonical DJF Hours | Invalid Temp Rows | Rejected SOURCE Rows | Rejected Plausibility Rows | Duplicate Hour Count |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `noaa_hourly_djf_load_20260624T012101Z` | inventory | 1,000 | 273,376 | 77,281 | 3,640,559 | 0 | 218,923 |
| `noaa_hourly_djf_load_20260624T013317Z` | downloaded | 1,000 | 1,103,326 | 166,165 | 1,614,964 | 0 | 5,079,462 |

Current NOAA/cache status:

| Metric | Value |
| --- | ---: |
| AWS CSV files | 9,620 |
| AWS `.part` files | 0 |
| AWS cache disk usage | 74 GB |
| Manifest downloaded rows | 9,620 |
| Manifest failed rows | 5,380 |
| Manifest planned rows | 71,839 |
| Manifest skipped rows | 86,839 |

## Refreshed Result Runs

| Layer | Run ID | Rows / Result |
| --- | --- | ---: |
| Station-year coverage | `station_year_djf_coverage_20260624T014923Z` | 17,000 rows; 2,136 complete, 14,452 partial, 412 empty |
| Station ECWT | `station_ecwt_loaded_20260624T015123Z` | 3,044 provisional, 67 blocked |
| Plant ECWT | `plant_ecwt_provisional_20260624T015403Z` | 16,104 provisional, 28 blocked |
| Strict plant readiness | `plant_ecwt_readiness_20260624T015450Z` | 367 publication candidates |
| Diagnostic plant readiness | `plant_ecwt_readiness_20260624T015510Z` | 13,679 diagnostic candidates |

Current canonical weather:

| Metric | Value |
| --- | ---: |
| `weather.hourly_djf` rows | 10,668,025 |
| Distinct stations | 3,044 |
| Minimum dry-bulb F | -61.060 |
| Maximum dry-bulb F | 104.000 |
| Database size | 4,612 MB |

## Interpretation

- Strict readiness improved materially this cycle, from `204` to `367` plants.
- The dominant blocker remains weather coverage: `15,737` plants are still below the strict coverage threshold.
- The relaxed diagnostic gate rose from `13,393` to `13,679` candidates.
- Loader validation counts are becoming a measurable runtime cost as `weather.hourly_djf` grows; future hardening should avoid full-table counts in per-run report generation.
- The immediate next step remains another parallel download/load/refresh cycle, plus loader-report optimization if we want faster iteration.
