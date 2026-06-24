# NOAA Backfill, Load, And ECWT Refresh Status

Generated UTC: 2026-06-24T11:28Z

Database: `eop012` on `127.0.0.1:5436`

## Summary

This cycle ran AWS backfill batch 37, loaded the new batch 37 downloads, and refreshed coverage, station ECWT, plant ECWT, and fixed-denominator plant readiness.

The fixed-denominator strict publication count increased from `525` to `676`. The relaxed diagnostic count increased from `4,989` to `5,193`.

| Metric | Value |
| --- | ---: |
| Plant ECWT rows | 16,132 |
| Strict publication candidates | 676 |
| Strict provisional low coverage | 15,428 |
| Strict blocked | 28 |
| Diagnostic publication candidates at 0.25 coverage | 5,193 |
| Diagnostic provisional low coverage at 0.25 coverage | 10,911 |
| Diagnostic blocked | 28 |

## NOAA Progress

Completed AWS backfill batch:

| Batch | Run ID | Downloaded | HTTP failures | Exception failures | Bytes | Elapsed seconds |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 37 | `noaa_backfill_download_batch37_20260624T111001Z` | 398 | 602 | 0 | 2,476,739,545 | 361.793 |

Completed NOAA load:

| Run ID | Source | Files | Canonical DJF Hours | Invalid Temp Rows | Rejected SOURCE Rows | Rejected Plausibility Rows | Duplicate Hour Count |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `noaa_hourly_djf_load_20260624T111630Z` | downloaded | 398 | 587,537 | 452,256 | 0 | 14 | 337,952 |

Plausibility rejection detail:

| Station | Year | Rejected Plausibility Rows | Source File ID |
| --- | ---: | ---: | --- |
| `720319-99999` | 2004 | 14 | `noaa_global_hourly_csv_2004_72031999999_ea00b7d9d9714a9c` |

Current NOAA/cache status:

| Metric | Value |
| --- | ---: |
| AWS CSV files | 20,680 |
| AWS `.part` / `.partial` files | 0 |
| AWS raw cache disk usage | 158 GB |
| Manifest downloaded rows | 20,680 |
| Manifest failed rows | 16,320 |
| Manifest planned rows | 49,839 |
| Manifest skipped rows | 86,839 |

## Refreshed Result Runs

| Layer | Run ID | Rows / Result |
| --- | --- | ---: |
| Station-year coverage | `station_year_djf_coverage_20260624T111840Z` | 48,241 rows; 8,877 complete, 38,231 partial, 1,133 empty |
| Station ECWT | `station_ecwt_loaded_20260624T112250Z` | 3,727 provisional, 123 blocked |
| Plant ECWT | `plant_ecwt_provisional_20260624T112546Z` | 16,104 provisional, 28 blocked |
| Strict plant readiness | `plant_ecwt_readiness_20260624T112629Z` | 676 publication candidates |
| Diagnostic plant readiness | `plant_ecwt_readiness_20260624T112641Z` | 5,193 diagnostic candidates |

Current canonical weather:

| Metric | Value |
| --- | ---: |
| `weather.hourly_djf` rows | 33,482,494 |
| Distinct stations | 3,727 |
| Minimum dry-bulb F | -67.000 |
| Maximum dry-bulb F | 104.000 |
| `SHEF` rows below `-50 C` | 0 |
| Database size | 14 GB |

## Stability Checks

Compared with the previous plant run `plant_ecwt_provisional_20260624T110204Z`:

| Check | Plants |
| --- | ---: |
| Selected station unchanged | 16,043 |
| Selected station changed | 89 |

Compared with previous strict readiness `plant_ecwt_readiness_20260624T110422Z`:

| Transition | Plants |
| --- | ---: |
| Strict candidate remained candidate | 525 |
| Strict low coverage became candidate | 151 |
| Strict low coverage remained low coverage | 15,428 |
| Strict blocked remained blocked | 28 |

Compared with previous diagnostic readiness `plant_ecwt_readiness_20260624T110431Z`:

| Transition | Plants |
| --- | ---: |
| Diagnostic candidate remained candidate | 4,947 |
| Diagnostic candidate became low coverage | 42 |
| Diagnostic low coverage became candidate | 246 |
| Diagnostic low coverage remained low coverage | 10,869 |
| Diagnostic blocked remained blocked | 28 |

## Interpretation

- Batch 37 added `398` NOAA CSVs and there are no incomplete raw downloads left in the cache.
- The inventory selector remains exhausted for the current source-selection criteria; the remaining forward progress is coming from AWS backfill batches and downloaded-file loads.
- The hardened `SHEF < -50 C` check still shows zero rows, and the generic plausibility gate rejected `14` rows from one 2004 station-year file.
- Fixed-denominator strict readiness improved from `525` to `676` publication candidates.
- Fixed-denominator diagnostic readiness improved from `4,989` to `5,193` candidates, with `42` diagnostic candidates moving back to low coverage as selected stations changed.
- Station selection changed for `89` plants, down from `194` in the prior cycle, but station-selection churn remains a QA signal while weather coverage is incomplete.
- The immediate next step is to continue the parallel download/load/refresh cycle with batch 38.
