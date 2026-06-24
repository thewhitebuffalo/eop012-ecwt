# NOAA Backfill, Load, And ECWT Refresh Status

Generated UTC: 2026-06-24T04:14Z

Database: `eop012` on `127.0.0.1:5436`

## Summary

This cycle ran AWS backfill batch 20 in parallel with another inventory load, then loaded downloaded files and refreshed coverage, station ECWT, plant ECWT, and plant readiness.

Strict publication candidates increased from `2,494` to `2,646`. The dataset is still not publication-complete because most plants remain below the strict coverage threshold.

| Metric | Value |
| --- | ---: |
| Plant ECWT rows | 16,132 |
| Strict publication candidates | 2,646 |
| Strict provisional low coverage | 13,458 |
| Strict blocked | 28 |
| Diagnostic publication candidates at 0.25 coverage | 13,369 |
| Diagnostic provisional low coverage at 0.25 coverage | 2,735 |
| Diagnostic blocked | 28 |

## NOAA Progress

Completed AWS backfill batch:

| Batch | Run ID | Downloaded | HTTP failures | Bytes | Elapsed seconds |
| ---: | --- | ---: | ---: | ---: | ---: |
| 20 | `noaa_backfill_download_batch20_20260624T035647Z` | 587 | 413 | 5,435,180,348 | 319.084 |

Completed NOAA loads:

| Run ID | Source | Files | Canonical DJF Hours | Invalid Temp Rows | Rejected SOURCE Rows | Rejected Plausibility Rows | Duplicate Hour Count |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `noaa_hourly_djf_load_20260624T035647Z` | inventory | 1,000 | 820,245 | 168,381 | 2,618,396 | 0 | 2,629,043 |
| `noaa_hourly_djf_load_20260624T040259Z` | downloaded | 587 | 366,277 | 58,939 | 1,690,681 | 0 | 935,843 |

Current NOAA/cache status:

| Metric | Value |
| --- | ---: |
| AWS CSV files | 12,702 |
| AWS `.part` files | 0 |
| AWS cache disk usage | 100 GB |
| Manifest downloaded rows | 12,702 |
| Manifest failed rows | 7,298 |
| Manifest planned rows | 66,839 |
| Manifest skipped rows | 86,839 |

## Refreshed Result Runs

| Layer | Run ID | Rows / Result |
| --- | --- | ---: |
| Station-year coverage | `station_year_djf_coverage_20260624T040547Z` | 25,702 rows; 3,753 complete, 21,337 partial, 612 empty |
| Station ECWT | `station_ecwt_loaded_20260624T040946Z` | 3,086 provisional, 78 blocked |
| Plant ECWT | `plant_ecwt_provisional_20260624T041121Z` | 16,104 provisional, 28 blocked |
| Strict plant readiness | `plant_ecwt_readiness_20260624T041226Z` | 2,646 publication candidates |
| Diagnostic plant readiness | `plant_ecwt_readiness_20260624T041245Z` | 13,369 diagnostic candidates |

Current canonical weather:

| Metric | Value |
| --- | ---: |
| `weather.hourly_djf` rows | 16,270,808 |
| Distinct stations | 3,086 |
| Minimum dry-bulb F | -61.060 |
| Maximum dry-bulb F | 104.000 |
| `SHEF` rows below `-50 C` | 0 |
| Database size | 6,873 MB |

## Interpretation

- Strict readiness improved from `2,494` to `2,646` plants.
- The dominant blocker remains weather coverage: `13,458` plants are still below the strict coverage threshold.
- The hardened `SHEF < -50 C` plausibility rule held through this cycle.
- The immediate next step remains another parallel download/load/refresh cycle, with station-selection stability still a publication risk.
