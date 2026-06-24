# NOAA Backfill, Load, And ECWT Refresh Status

Generated UTC: 2026-06-24T01:18Z

Database: `eop012` on `127.0.0.1:5436`

## Summary

This cycle ran AWS backfill batch 14 in parallel with another inventory load, then loaded downloaded files and refreshed coverage, station ECWT, plant ECWT, and plant readiness.

Strict publication candidates increased from `203` to `204`. The dataset is still not publication-complete because most plants remain below the strict coverage threshold.

| Metric | Value |
| --- | ---: |
| Plant ECWT rows | 16,132 |
| Strict publication candidates | 204 |
| Strict provisional low coverage | 15,900 |
| Strict blocked | 28 |
| Diagnostic publication candidates at 0.25 coverage | 13,393 |
| Diagnostic provisional low coverage at 0.25 coverage | 2,711 |
| Diagnostic blocked | 28 |

## NOAA Progress

Completed AWS backfill batch:

| Batch | Run ID | Downloaded | HTTP failures | Bytes | Elapsed seconds |
| ---: | --- | ---: | ---: | ---: | ---: |
| 14 | `noaa_backfill_download_batch14_20260624T005814Z` | 648 | 352 | 4,988,798,831 | 276.207 |

Completed NOAA loads:

| Run ID | Source | Files | Canonical DJF Hours | Invalid Temp Rows | Rejected SOURCE Rows | Rejected Plausibility Rows | Duplicate Hour Count |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `noaa_hourly_djf_load_20260624T005813Z` | inventory | 1,000 | 781,039 | 154,179 | 2,498,756 | 0 | 2,616,966 |
| `noaa_hourly_djf_load_20260624T010653Z` | downloaded | 1,000 | 569,804 | 103,082 | 2,882,081 | 1 | 192,125 |

Current NOAA/cache status:

| Metric | Value |
| --- | ---: |
| AWS CSV files | 8,994 |
| AWS `.part` files | 0 |
| AWS cache disk usage | 68 GB |
| Manifest downloaded rows | 8,994 |
| Manifest failed rows | 5,006 |
| Manifest planned rows | 72,839 |
| Manifest skipped rows | 86,839 |

## Refreshed Result Runs

| Layer | Run ID | Rows / Result |
| --- | --- | ---: |
| Station-year coverage | `station_year_djf_coverage_20260624T011234Z` | 15,000 rows; 1,703 complete, 12,945 partial, 352 empty |
| Station ECWT | `station_ecwt_loaded_20260624T011348Z` | 2,939 provisional, 66 blocked |
| Plant ECWT | `plant_ecwt_provisional_20260624T011618Z` | 16,104 provisional, 28 blocked |
| Strict plant readiness | `plant_ecwt_readiness_20260624T011654Z` | 204 publication candidates |
| Diagnostic plant readiness | `plant_ecwt_readiness_20260624T011720Z` | 13,393 diagnostic candidates |

Current canonical weather:

| Metric | Value |
| --- | ---: |
| `weather.hourly_djf` rows | 9,291,323 |
| Distinct stations | 2,939 |
| Minimum dry-bulb F | -61.060 |
| Maximum dry-bulb F | 104.000 |
| Database size | 4,090 MB |

## Interpretation

- Strict readiness improved slightly, from `203` to `204` plants.
- The dominant blocker remains weather coverage: `15,900` plants are still below the strict coverage threshold.
- The relaxed diagnostic candidate count fell from `13,456` to `13,393` because plant station selection changed as station coverage improved. These diagnostic rows remain provisional progress indicators, not compliance output.
- The immediate next step remains another parallel download/load/refresh cycle.
