# NOAA Backfill, Load, And ECWT Refresh Status

Generated UTC: 2026-06-24T12:03Z

Database: `eop012` on `127.0.0.1:5436`

## Summary

This cycle ran AWS backfill batches 38, 39, and 40, loaded each batch's new downloads, and then refreshed coverage, station ECWT, plant ECWT, and fixed-denominator plant readiness once for the three-batch window.

The fixed-denominator strict publication count increased from `676` to `745`. The relaxed diagnostic count increased from `5,193` to `5,639`.

| Metric | Value |
| --- | ---: |
| Plant ECWT rows | 16,132 |
| Strict publication candidates | 745 |
| Strict provisional low coverage | 15,359 |
| Strict blocked | 28 |
| Diagnostic publication candidates at 0.25 coverage | 5,639 |
| Diagnostic provisional low coverage at 0.25 coverage | 10,465 |
| Diagnostic blocked | 28 |

## NOAA Progress

Completed AWS backfill batches:

| Batch | Run ID | Downloaded | HTTP failures | Exception failures | Bytes | Elapsed seconds |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 38 | `noaa_backfill_download_batch38_20260624T112958Z` | 351 | 649 | 0 | 2,111,816,551 | 310.434 |
| 39 | `noaa_backfill_download_batch39_20260624T113733Z` | 341 | 659 | 0 | 1,794,693,097 | 274.566 |
| 40 | `noaa_backfill_download_batch40_20260624T114413Z` | 364 | 636 | 0 | 1,647,034,087 | 248.342 |
| Total |  | 1,056 | 1,944 | 0 | 5,553,543,735 | 833.342 |

Completed NOAA loads:

| Run ID | Source | Files | Canonical DJF Hours | Invalid Temp Rows | Rejected SOURCE Rows | Rejected Plausibility Rows | Duplicate Hour Count |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `noaa_hourly_djf_load_20260624T113527Z` | downloaded | 351 | 515,213 | 362,052 | 0 | 0 | 315,621 |
| `noaa_hourly_djf_load_20260624T114227Z` | downloaded | 341 | 480,718 | 286,199 | 0 | 262 | 273,377 |
| `noaa_hourly_djf_load_20260624T114848Z` | downloaded | 364 | 507,534 | 279,921 | 0 | 0 | 189,206 |
| Total |  | 1,056 | 1,503,465 | 928,172 | 0 | 262 | 778,204 |

Plausibility rejection detail:

| Run ID | Station | Year | Rejected Plausibility Rows | Source File ID |
| --- | --- | ---: | ---: | --- |
| `noaa_hourly_djf_load_20260624T114227Z` | `722133-99999` | 2004 | 262 | `noaa_global_hourly_csv_2004_72213399999_d633ad8696a912c0` |

Current NOAA/cache status:

| Metric | Value |
| --- | ---: |
| AWS CSV files | 21,736 |
| AWS `.part` / `.partial` files | 0 |
| AWS raw cache disk usage | 163 GB |
| Manifest downloaded rows | 21,736 |
| Manifest failed rows | 18,264 |
| Manifest planned rows | 46,839 |
| Manifest skipped rows | 86,839 |

## Refreshed Result Runs

| Layer | Run ID | Rows / Result |
| --- | --- | ---: |
| Station-year coverage | `station_year_djf_coverage_20260624T115029Z` | 49,297 rows; 9,371 complete, 38,649 partial, 1,277 empty |
| Station ECWT | `station_ecwt_loaded_20260624T115715Z` | 3,861 provisional, 165 blocked |
| Plant ECWT | `plant_ecwt_provisional_20260624T120057Z` | 16,104 provisional, 28 blocked |
| Strict plant readiness | `plant_ecwt_readiness_20260624T120143Z` | 745 publication candidates |
| Diagnostic plant readiness | `plant_ecwt_readiness_20260624T120152Z` | 5,639 diagnostic candidates |

Current canonical weather:

| Metric | Value |
| --- | ---: |
| `weather.hourly_djf` rows | 34,985,959 |
| Distinct stations | 3,861 |
| Minimum dry-bulb F | -67.000 |
| Maximum dry-bulb F | 104.000 |
| `SHEF` rows below `-50 C` | 0 |
| Database size | 14 GB |

## Stability Checks

Compared with the previous plant run `plant_ecwt_provisional_20260624T112546Z`:

| Check | Plants |
| --- | ---: |
| Selected station unchanged | 15,851 |
| Selected station changed | 281 |

Compared with previous strict readiness `plant_ecwt_readiness_20260624T112629Z`:

| Transition | Plants |
| --- | ---: |
| Strict candidate remained candidate | 676 |
| Strict low coverage became candidate | 69 |
| Strict low coverage remained low coverage | 15,359 |
| Strict blocked remained blocked | 28 |

Compared with previous diagnostic readiness `plant_ecwt_readiness_20260624T112641Z`:

| Transition | Plants |
| --- | ---: |
| Diagnostic candidate remained candidate | 5,167 |
| Diagnostic candidate became low coverage | 26 |
| Diagnostic low coverage became candidate | 472 |
| Diagnostic low coverage remained low coverage | 10,439 |
| Diagnostic blocked remained blocked | 28 |

## Interpretation

- Batches 38-40 added `1,056` NOAA CSVs and there are no incomplete raw downloads left in the cache.
- The three-batch cadence preserved per-batch download/load audit reports while avoiding two extra full-table ECWT refreshes.
- The inventory selector remains exhausted for the current source-selection criteria; the remaining forward progress is coming from AWS backfill batches and downloaded-file loads.
- The hardened `SHEF < -50 C` check still shows zero rows, and the generic plausibility gate rejected `262` rows from one 2004 station-year file.
- Fixed-denominator strict readiness improved from `676` to `745` publication candidates.
- Fixed-denominator diagnostic readiness improved from `5,193` to `5,639` candidates, with `26` diagnostic candidates moving back to low coverage as selected stations changed.
- Station selection changed for `281` plants across this three-batch window; station-selection churn remains a QA signal while weather coverage is incomplete.
- The immediate next step is to continue the same three-batch download/load/window-refresh cadence with batches 41-43.
