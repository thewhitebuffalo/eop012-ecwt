# NOAA Backfill, Load, And ECWT Refresh Status

Generated UTC: 2026-06-24T12:37Z

Database: `eop012` on `127.0.0.1:5436`

## Summary

This cycle ran AWS backfill batches 41, 42, and 43, loaded each batch's new downloads, and then refreshed coverage, station ECWT, plant ECWT, and fixed-denominator plant readiness once for the three-batch window.

The fixed-denominator strict publication count increased from `745` to `760`. The relaxed diagnostic count increased from `5,639` to `6,161`.

| Metric | Value |
| --- | ---: |
| Plant ECWT rows | 16,132 |
| Strict publication candidates | 760 |
| Strict provisional low coverage | 15,344 |
| Strict blocked | 28 |
| Diagnostic publication candidates at 0.25 coverage | 6,161 |
| Diagnostic provisional low coverage at 0.25 coverage | 9,943 |
| Diagnostic blocked | 28 |

## NOAA Progress

Completed AWS backfill batches:

| Batch | Run ID | Downloaded | HTTP failures | Exception failures | Bytes | Elapsed seconds |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 41 | `noaa_backfill_download_batch41_20260624T120558Z` | 324 | 676 | 0 | 1,927,338,889 | 311.786 |
| 42 | `noaa_backfill_download_batch42_20260624T121339Z` | 296 | 704 | 0 | 1,657,097,905 | 266.594 |
| 43 | `noaa_backfill_download_batch43_20260624T122017Z` | 260 | 740 | 0 | 1,507,163,405 | 244.649 |
| Total |  | 880 | 2,120 | 0 | 5,091,600,199 | 823.029 |

Completed NOAA loads:

| Run ID | Source | Files | Canonical DJF Hours | Invalid Temp Rows | Rejected SOURCE Rows | Rejected Plausibility Rows | Duplicate Hour Count |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `noaa_hourly_djf_load_20260624T121134Z` | downloaded | 324 | 520,697 | 359,905 | 0 | 0 | 235,546 |
| `noaa_hourly_djf_load_20260624T121825Z` | downloaded | 296 | 457,729 | 313,745 | 0 | 0 | 189,729 |
| `noaa_hourly_djf_load_20260624T122447Z` | downloaded | 260 | 445,894 | 235,057 | 0 | 1 | 198,762 |
| Total |  | 880 | 1,424,320 | 908,707 | 0 | 1 | 624,037 |

Plausibility rejection detail:

| Run ID | Station | Year | Rejected Plausibility Rows | Source File ID |
| --- | --- | ---: | ---: | --- |
| `noaa_hourly_djf_load_20260624T122447Z` | `722730-99999` | 2003 | 1 | `noaa_global_hourly_csv_2003_72273099999_468e6003cbb34199` |

Current NOAA/cache status:

| Metric | Value |
| --- | ---: |
| AWS CSV files | 22,616 |
| AWS `.part` / `.partial` files | 0 |
| AWS raw cache disk usage | 168 GB |
| Manifest downloaded rows | 22,616 |
| Manifest failed rows | 20,384 |
| Manifest planned rows | 43,839 |
| Manifest skipped rows | 86,839 |

## Refreshed Result Runs

| Layer | Run ID | Rows / Result |
| --- | --- | ---: |
| Station-year coverage | `station_year_djf_coverage_20260624T122638Z` | 50,177 rows; 9,827 complete, 38,953 partial, 1,397 empty |
| Station ECWT | `station_ecwt_loaded_20260624T123157Z` | 3,964 provisional, 171 blocked |
| Plant ECWT | `plant_ecwt_provisional_20260624T123513Z` | 16,104 provisional, 28 blocked |
| Strict plant readiness | `plant_ecwt_readiness_20260624T123605Z` | 760 publication candidates |
| Diagnostic plant readiness | `plant_ecwt_readiness_20260624T123615Z` | 6,161 diagnostic candidates |

Current canonical weather:

| Metric | Value |
| --- | ---: |
| `weather.hourly_djf` rows | 36,410,279 |
| Distinct stations | 3,964 |
| Minimum dry-bulb F | -67.000 |
| Maximum dry-bulb F | 104.000 |
| `SHEF` rows below `-50 C` | 0 |
| Database size | 15 GB |

## Stability Checks

Compared with the previous plant run `plant_ecwt_provisional_20260624T120057Z`:

| Check | Plants |
| --- | ---: |
| Selected station unchanged | 15,839 |
| Selected station changed | 293 |

Compared with previous strict readiness `plant_ecwt_readiness_20260624T120143Z`:

| Transition | Plants |
| --- | ---: |
| Strict candidate remained candidate | 745 |
| Strict low coverage became candidate | 15 |
| Strict low coverage remained low coverage | 15,344 |
| Strict blocked remained blocked | 28 |

Compared with previous diagnostic readiness `plant_ecwt_readiness_20260624T120152Z`:

| Transition | Plants |
| --- | ---: |
| Diagnostic candidate remained candidate | 5,617 |
| Diagnostic candidate became low coverage | 22 |
| Diagnostic low coverage became candidate | 544 |
| Diagnostic low coverage remained low coverage | 9,921 |
| Diagnostic blocked remained blocked | 28 |

## Interpretation

- Batches 41-43 added `880` NOAA CSVs and there are no incomplete raw downloads left in the cache.
- The three-batch cadence preserved per-batch download/load audit reports while avoiding two extra full-table ECWT refreshes.
- The inventory selector remains exhausted for the current source-selection criteria; the remaining forward progress is coming from AWS backfill batches and downloaded-file loads.
- The hardened `SHEF < -50 C` check still shows zero rows, and the generic plausibility gate rejected `1` row from one 2003 station-year file.
- Fixed-denominator strict readiness improved from `745` to `760` publication candidates.
- Fixed-denominator diagnostic readiness improved from `5,639` to `6,161` candidates, with `22` diagnostic candidates moving back to low coverage as selected stations changed.
- Station selection changed for `293` plants across this three-batch window; station-selection churn remains a QA signal while weather coverage is incomplete.
- The immediate next step is to continue the same three-batch download/load/window-refresh cadence with batches 44-46.
