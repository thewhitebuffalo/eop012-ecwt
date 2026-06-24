# NOAA Backfill, Load, And ECWT Refresh Status

Generated UTC: 2026-06-24T13:18Z

Database: `eop012` on `127.0.0.1:5436`

## Summary

This cycle ran AWS backfill batches 44, 45, and 46, loaded each batch's new downloads, and then refreshed coverage, station ECWT, plant ECWT, and fixed-denominator plant readiness once for the three-batch window.

The fixed-denominator strict publication count increased from `760` to `828`. The relaxed diagnostic count increased from `6,161` to `7,061`.

| Metric | Value |
| --- | ---: |
| Plant ECWT rows | 16,132 |
| Strict publication candidates | 828 |
| Strict provisional low coverage | 15,276 |
| Strict blocked | 28 |
| Diagnostic publication candidates at 0.25 coverage | 7,061 |
| Diagnostic provisional low coverage at 0.25 coverage | 9,043 |
| Diagnostic blocked | 28 |

## NOAA Progress

Completed AWS backfill batches:

| Batch | Run ID | Downloaded | HTTP failures | Exception failures | Bytes | Elapsed seconds |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 44 | `noaa_backfill_download_batch44_20260624T124101Z` | 279 | 721 | 0 | 1,299,734,329 | 233.104 |
| 45 | `noaa_backfill_download_batch45_20260624T124646Z` | 334 | 666 | 0 | 1,705,514,143 | 275.254 |
| 46 | `noaa_backfill_download_batch46_20260624T125339Z` | 327 | 673 | 0 | 1,658,512,741 | 256.254 |
| Total |  | 940 | 2,060 | 0 | 4,663,761,213 | 764.612 |

Completed NOAA loads:

| Run ID | Source | Files | Canonical DJF Hours | Invalid Temp Rows | Rejected SOURCE Rows | Rejected Plausibility Rows | Duplicate Hour Count |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `noaa_hourly_djf_load_20260624T124513Z` | downloaded | 279 | 423,049 | 210,340 | 0 | 80 | 150,037 |
| `noaa_hourly_djf_load_20260624T125145Z` | downloaded | 334 | 529,789 | 327,817 | 0 | 0 | 121,416 |
| `noaa_hourly_djf_load_20260624T125816Z` | downloaded | 327 | 495,589 | 322,342 | 0 | 0 | 114,941 |
| Total |  | 940 | 1,448,427 | 860,499 | 0 | 80 | 386,394 |

Plausibility rejection detail:

| Run ID | Station | Year | Rejected Plausibility Rows | Source File ID |
| --- | --- | ---: | ---: | --- |
| `noaa_hourly_djf_load_20260624T124513Z` | `701940-99999` | 2003 | 80 | `noaa_global_hourly_csv_2003_70194099999_3b4d3e72f1ae74f3` |

Current NOAA/cache status:

| Metric | Value |
| --- | ---: |
| AWS CSV files | 23,556 |
| AWS `.part` / `.partial` files | 0 |
| AWS raw cache disk usage | 173 GB |
| Manifest downloaded rows | 23,556 |
| Manifest failed rows | 22,444 |
| Manifest planned rows | 40,839 |
| Manifest skipped rows | 86,839 |

## Refreshed Result Runs

| Layer | Run ID | Rows / Result |
| --- | --- | ---: |
| Station-year coverage | `station_year_djf_coverage_20260624T130018Z` | 51,117 rows; 10,305 complete, 39,265 partial, 1,547 empty |
| Station ECWT | `station_ecwt_loaded_20260624T130806Z` | 3,996 provisional, 178 blocked |
| Plant ECWT | `plant_ecwt_provisional_20260624T131445Z` | 16,104 provisional, 28 blocked |
| Strict plant readiness | `plant_ecwt_readiness_20260624T131613Z` | 828 publication candidates |
| Diagnostic plant readiness | `plant_ecwt_readiness_20260624T131622Z` | 7,061 diagnostic candidates |

Current canonical weather:

| Metric | Value |
| --- | ---: |
| `weather.hourly_djf` rows | 37,858,706 |
| Distinct stations | 3,996 |
| Minimum dry-bulb F | -67.000 |
| Maximum dry-bulb F | 104.000 |
| `SHEF` rows below `-50 C` | 0 |
| Database size | 16 GB |

## Stability Checks

Compared with the previous plant run `plant_ecwt_provisional_20260624T123513Z`:

| Check | Plants |
| --- | ---: |
| Selected station unchanged | 16,115 |
| Selected station changed | 17 |

Compared with previous strict readiness `plant_ecwt_readiness_20260624T123605Z`:

| Transition | Plants |
| --- | ---: |
| Strict candidate remained candidate | 759 |
| Strict candidate became low coverage | 1 |
| Strict low coverage became candidate | 69 |
| Strict low coverage remained low coverage | 15,275 |
| Strict blocked remained blocked | 28 |

Compared with previous diagnostic readiness `plant_ecwt_readiness_20260624T123615Z`:

| Transition | Plants |
| --- | ---: |
| Diagnostic candidate remained candidate | 6,156 |
| Diagnostic candidate became low coverage | 5 |
| Diagnostic low coverage became candidate | 905 |
| Diagnostic low coverage remained low coverage | 9,038 |
| Diagnostic blocked remained blocked | 28 |

## Interpretation

- Batches 44-46 added `940` NOAA CSVs and there are no incomplete raw downloads left in the cache.
- The three-batch cadence preserved per-batch download/load audit reports while avoiding two extra full-table ECWT refreshes.
- The inventory selector remains exhausted for the current source-selection criteria; the remaining forward progress is coming from AWS backfill batches and downloaded-file loads.
- The hardened `SHEF < -50 C` check still shows zero rows, and the generic plausibility gate rejected `80` rows from one 2003 station-year file.
- Fixed-denominator strict readiness improved from `760` to `828` publication candidates, with `1` former candidate moving back to low coverage.
- Fixed-denominator diagnostic readiness improved from `6,161` to `7,061` candidates, with `5` diagnostic candidates moving back to low coverage as selected stations changed.
- Station selection changed for only `17` plants across this three-batch window, a lower churn signal than the prior windows.
- The immediate next step is to continue the same three-batch download/load/window-refresh cadence with batches 47-49.
