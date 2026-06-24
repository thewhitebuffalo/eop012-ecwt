# NOAA Backfill, Load, And ECWT Refresh Status

Generated UTC: 2026-06-24T13:50Z

Database: `eop012` on `127.0.0.1:5436`

## Summary

This cycle ran AWS backfill batches 47, 48, and 49, loaded each batch's new downloads, and then refreshed coverage, station ECWT, plant ECWT, and fixed-denominator plant readiness once for the three-batch window.

The fixed-denominator strict publication count increased from `828` to `903`. The relaxed diagnostic count increased from `7,061` to `7,198`.

| Metric | Value |
| --- | ---: |
| Plant ECWT rows | 16,132 |
| Strict publication candidates | 903 |
| Strict provisional low coverage | 15,201 |
| Strict blocked | 28 |
| Diagnostic publication candidates at 0.25 coverage | 7,198 |
| Diagnostic provisional low coverage at 0.25 coverage | 8,906 |
| Diagnostic blocked | 28 |

## NOAA Progress

Completed AWS backfill batches:

| Batch | Run ID | Downloaded | HTTP failures | Exception failures | Bytes | Elapsed seconds |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 47 | `noaa_backfill_download_batch47_20260624T132024Z` | 283 | 717 | 0 | 1,348,680,464 | 232.352 |
| 48 | `noaa_backfill_download_batch48_20260624T132542Z` | 283 | 717 | 0 | 1,292,973,842 | 217.578 |
| 49 | `noaa_backfill_download_batch49_20260624T133047Z` | 322 | 678 | 0 | 1,300,390,316 | 237.999 |
| Total |  | 888 | 2,112 | 0 | 3,942,044,622 | 687.929 |

Completed NOAA loads:

| Run ID | Source | Files | Canonical DJF Hours | Invalid Temp Rows | Rejected SOURCE Rows | Rejected Plausibility Rows | Duplicate Hour Count |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `noaa_hourly_djf_load_20260624T132438Z` | downloaded | 283 | 402,561 | 232,177 | 0 | 0 | 110,988 |
| `noaa_hourly_djf_load_20260624T132935Z` | downloaded | 283 | 405,201 | 239,015 | 0 | 2 | 88,109 |
| `noaa_hourly_djf_load_20260624T133502Z` | downloaded | 322 | 435,980 | 260,338 | 0 | 7 | 83,454 |
| Total |  | 888 | 1,243,742 | 731,530 | 0 | 9 | 282,551 |

Plausibility rejection detail:

| Run ID | Station | Year | Rejected Plausibility Rows | Source File ID |
| --- | --- | ---: | ---: | --- |
| `noaa_hourly_djf_load_20260624T132935Z` | `746140-99999` | 2002 | 2 | `noaa_global_hourly_csv_2002_74614099999_de15ce70e7117872` |
| `noaa_hourly_djf_load_20260624T133502Z` | `690190-99999` | 2001 | 7 | `noaa_global_hourly_csv_2001_69019099999_58a7ef3fe0fee7f9` |

Current NOAA/cache status:

| Metric | Value |
| --- | ---: |
| AWS CSV files | 24,444 |
| AWS `.part` / `.partial` files | 0 |
| AWS raw cache disk usage | 177 GB |
| Manifest downloaded rows | 24,444 |
| Manifest failed rows | 24,556 |
| Manifest planned rows | 37,839 |
| Manifest skipped rows | 86,839 |

## Refreshed Result Runs

| Layer | Run ID | Rows / Result |
| --- | --- | ---: |
| Station-year coverage | `station_year_djf_coverage_20260624T133641Z` | 52,005 rows; 10,703 complete, 39,594 partial, 1,708 empty |
| Station ECWT | `station_ecwt_loaded_20260624T134258Z` | 4,015 provisional, 190 blocked |
| Plant ECWT | `plant_ecwt_provisional_20260624T134639Z` | 16,104 provisional, 28 blocked |
| Strict plant readiness | `plant_ecwt_readiness_20260624T134810Z` | 903 publication candidates |
| Diagnostic plant readiness | `plant_ecwt_readiness_20260624T134835Z` | 7,198 diagnostic candidates |

Current canonical weather:

| Metric | Value |
| --- | ---: |
| `weather.hourly_djf` rows | 39,102,448 |
| Distinct stations | 4,015 |
| Minimum dry-bulb F | -74.200 |
| Maximum dry-bulb F | 104.000 |
| `SHEF` rows below `-50 C` | 0 |
| Database size | 16 GB |

## Stability Checks

Compared with the previous plant run `plant_ecwt_provisional_20260624T131445Z`:

| Check | Plants |
| --- | ---: |
| Selected station unchanged | 16,098 |
| Selected station changed | 34 |

Compared with previous strict readiness `plant_ecwt_readiness_20260624T131613Z`:

| Transition | Plants |
| --- | ---: |
| Strict candidate remained candidate | 827 |
| Strict candidate became low coverage | 1 |
| Strict low coverage became candidate | 76 |
| Strict low coverage remained low coverage | 15,200 |
| Strict blocked remained blocked | 28 |

Compared with previous diagnostic readiness `plant_ecwt_readiness_20260624T131622Z`:

| Transition | Plants |
| --- | ---: |
| Diagnostic candidate remained candidate | 7,041 |
| Diagnostic candidate became low coverage | 20 |
| Diagnostic low coverage became candidate | 157 |
| Diagnostic low coverage remained low coverage | 8,886 |
| Diagnostic blocked remained blocked | 28 |

## Interpretation

- Batches 47-49 added `888` NOAA CSVs and there are no incomplete raw downloads left in the cache.
- The three-batch cadence preserved per-batch download/load audit reports while avoiding two extra full-table ECWT refreshes.
- The inventory selector remains exhausted for the current source-selection criteria; the remaining forward progress is coming from AWS backfill batches and downloaded-file loads.
- The hardened `SHEF < -50 C` check still shows zero rows, and the generic plausibility gate rejected `9` rows across two station-year files.
- Fixed-denominator strict readiness improved from `828` to `903` publication candidates, with `1` former candidate moving back to low coverage.
- Fixed-denominator diagnostic readiness improved from `7,061` to `7,198` candidates, with `20` diagnostic candidates moving back to low coverage as selected stations changed.
- Station selection changed for `34` plants across this three-batch window.
- The canonical weather minimum moved from `-67.000 F` to `-74.200 F`; this is still inside the configured plausibility range and should remain visible in QA monitoring.
- The immediate next step is to continue the same three-batch download/load/window-refresh cadence with batches 50-52.
