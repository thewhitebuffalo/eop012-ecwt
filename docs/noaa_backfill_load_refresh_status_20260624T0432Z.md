# NOAA Backfill, Load, And ECWT Refresh Status

Generated UTC: 2026-06-24T04:32Z

Database: `eop012` on `127.0.0.1:5436`

## Summary

This cycle ran AWS backfill batch 21, loaded another inventory slice, loaded the new batch 21 downloads, and refreshed coverage, station ECWT, plant ECWT, and plant readiness.

Strict publication candidates moved from `2,646` to `2,612`. That is a regression in readiness count after adding weather data, not a raw-load failure. It confirms the current station-selection method is not monotonic as coverage changes and remains a publication risk.

| Metric | Value |
| --- | ---: |
| Plant ECWT rows | 16,132 |
| Strict publication candidates | 2,612 |
| Strict provisional low coverage | 13,492 |
| Strict blocked | 28 |
| Diagnostic publication candidates at 0.25 coverage | 13,345 |
| Diagnostic provisional low coverage at 0.25 coverage | 2,759 |
| Diagnostic blocked | 28 |

## NOAA Progress

Completed AWS backfill batch:

| Batch | Run ID | Downloaded | HTTP failures | Bytes | Elapsed seconds |
| ---: | --- | ---: | ---: | ---: | ---: |
| 21 | `noaa_backfill_download_batch21_20260624T041726Z` | 580 | 420 | 5,141,326,885 | 320.155 |

Completed NOAA loads:

| Run ID | Source | Files | Canonical DJF Hours | Invalid Temp Rows | Rejected SOURCE Rows | Rejected Plausibility Rows | Duplicate Hour Count |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `noaa_hourly_djf_load_20260624T041729Z` | inventory | 1,000 | 246,966 | 76,127 | 3,590,636 | 0 | 166,816 |
| `noaa_hourly_djf_load_20260624T042304Z` | downloaded | 580 | 452,539 | 81,401 | 1,252,245 | 0 | 1,181,855 |

Current NOAA/cache status:

| Metric | Value |
| --- | ---: |
| AWS CSV files | 13,282 |
| AWS `.part` files | 0 |
| AWS cache disk usage | 104 GB |
| Manifest downloaded rows | 13,282 |
| Manifest failed rows | 7,718 |
| Manifest planned rows | 65,839 |
| Manifest skipped rows | 86,839 |

## Refreshed Result Runs

| Layer | Run ID | Rows / Result |
| --- | --- | ---: |
| Station-year coverage | `station_year_djf_coverage_20260624T042620Z` | 27,282 rows; 3,921 complete, 22,724 partial, 637 empty |
| Station ECWT | `station_ecwt_loaded_20260624T042844Z` | 3,090 provisional, 79 blocked |
| Plant ECWT | `plant_ecwt_provisional_20260624T043007Z` | 16,104 provisional, 28 blocked |
| Strict plant readiness | `plant_ecwt_readiness_20260624T043029Z` | 2,612 publication candidates |
| Diagnostic plant readiness | `plant_ecwt_readiness_20260624T043036Z` | 13,345 diagnostic candidates |

Current canonical weather:

| Metric | Value |
| --- | ---: |
| `weather.hourly_djf` rows | 16,970,313 |
| Distinct stations | 3,090 |
| Minimum dry-bulb F | -61.060 |
| Maximum dry-bulb F | 104.000 |
| `SHEF` rows below `-50 C` | 0 |
| Database size | 7,174 MB |

## Interpretation

- Batch 21 added `580` NOAA CSVs and there are no `.part` files left in the cache.
- The hardened `SHEF < -50 C` plausibility rule held through this cycle.
- The dominant blocker remains weather coverage: `13,492` plants are still below the strict coverage threshold.
- The station-selection instability is now visible in the strict readiness count and should be fixed before any publication claim.
- The immediate next step is to make plant station selection stable, then continue the parallel download/load/refresh cycle.
