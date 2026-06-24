# NOAA Backfill, Load, And ECWT Refresh Status

Generated UTC: 2026-06-24T03:11Z

Database: `eop012` on `127.0.0.1:5436`

## Summary

This cycle inspected the downloaded loader queue, ran AWS backfill batch 18 in parallel with another inventory load, then loaded downloaded files and refreshed coverage, station ECWT, plant ECWT, and plant readiness. It also hardened the NOAA loader against implausible `SHEF` cold outliers and refreshed results after the cleanup.

Strict publication candidates increased from `2,485` to `2,599`. The dataset is still not publication-complete because most plants remain below the strict coverage threshold.

| Metric | Value |
| --- | ---: |
| Plant ECWT rows | 16,132 |
| Strict publication candidates | 2,599 |
| Strict provisional low coverage | 13,505 |
| Strict blocked | 28 |
| Diagnostic publication candidates at 0.25 coverage | 13,589 |
| Diagnostic provisional low coverage at 0.25 coverage | 2,515 |
| Diagnostic blocked | 28 |

## NOAA Progress

Completed AWS backfill batch:

| Batch | Run ID | Downloaded | HTTP failures | Bytes | Elapsed seconds |
| ---: | --- | ---: | ---: | ---: | ---: |
| 18 | `noaa_backfill_download_batch18_20260624T025109Z` | 645 | 355 | 4,464,983,988 | 478.360 |

Completed NOAA loads:

| Run ID | Source | Files | Canonical DJF Hours | Invalid Temp Rows | Rejected SOURCE Rows | Rejected Plausibility Rows | Duplicate Hour Count |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `noaa_hourly_djf_load_20260624T025109Z` | inventory | 1,000 | 849,419 | 189,072 | 2,652,202 | 56 | 2,601,126 |
| `noaa_hourly_djf_load_20260624T025933Z` | downloaded | 645 | 518,199 | 113,030 | 1,231,875 | 1 | 728,147 |

Post-load QA cleanup:

| Run ID | Rows Removed | Rule | Result |
| --- | ---: | --- | --- |
| `noaa_hourly_djf_shef_cold_cleanup_20260624T031200Z` | 2 | Reject `SHEF` report-type rows below `-60 C` | Initial Wisconsin pier outliers removed |
| `noaa_hourly_djf_shef_cold_cleanup2_20260624T031800Z` | 7 | Reject `SHEF` report-type rows below `-50 C` | Remaining Wisconsin pier outliers removed |

Current NOAA/cache status:

| Metric | Value |
| --- | ---: |
| AWS CSV files | 11,491 |
| AWS `.part` files | 0 |
| AWS cache disk usage | 89 GB |
| Manifest downloaded rows | 11,491 |
| Manifest failed rows | 6,509 |
| Manifest planned rows | 68,839 |
| Manifest skipped rows | 86,839 |

## Refreshed Result Runs

| Layer | Run ID | Rows / Result |
| --- | --- | ---: |
| Station-year coverage | `station_year_djf_coverage_20260624T032829Z` | 22,491 rows; 3,234 complete, 18,699 partial, 558 empty |
| Station ECWT | `station_ecwt_loaded_20260624T032918Z` | 3,075 provisional, 74 blocked |
| Plant ECWT | `plant_ecwt_provisional_20260624T033019Z` | 16,104 provisional, 28 blocked |
| Strict plant readiness | `plant_ecwt_readiness_20260624T033114Z` | 2,599 publication candidates |
| Diagnostic plant readiness | `plant_ecwt_readiness_20260624T033133Z` | 13,589 diagnostic candidates |

Current canonical weather:

| Metric | Value |
| --- | ---: |
| `weather.hourly_djf` rows | 14,487,109 |
| Distinct stations | 3,075 |
| Minimum dry-bulb F | -61.060 |
| Maximum dry-bulb F | 104.000 |
| Database size | 6,084 MB |

## Interpretation

- Strict readiness improved from `2,485` to `2,599` plants.
- The dominant blocker remains weather coverage: `13,505` plants are still below the strict coverage threshold.
- The downloaded queue was empty after batch 17; batch 18 added and loaded `645` downloaded files, confirming the loader queue is healthy.
- The `-84.820 F` minimum was traced to implausible `SHEF` readings at Wisconsin station `994973-99999` (`N PIER DEATHS DOOR`). Nine bad canonical rows were removed, file-level metrics were adjusted, and the loader now rejects `SHEF` temperatures below `-50 C`.
- The immediate next step remains another parallel download/load/refresh cycle.
