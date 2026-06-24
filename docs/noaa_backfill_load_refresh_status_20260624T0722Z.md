# NOAA Backfill, Load, And ECWT Refresh Status

Generated UTC: 2026-06-24T07:22Z

Database: `eop012` on `127.0.0.1:5436`

## Summary

This cycle ran AWS backfill batch 27 in parallel with another inventory load, then loaded the new batch 27 downloads and refreshed coverage, station ECWT, corrected plant ECWT, and fixed-denominator plant readiness.

The fixed-denominator strict publication count increased from `71` to `75`. The relaxed diagnostic count increased from `2,516` to `2,740`.

| Metric | Value |
| --- | ---: |
| Plant ECWT rows | 16,132 |
| Strict publication candidates | 75 |
| Strict provisional low coverage | 16,029 |
| Strict blocked | 28 |
| Diagnostic publication candidates at 0.25 coverage | 2,740 |
| Diagnostic provisional low coverage at 0.25 coverage | 13,364 |
| Diagnostic blocked | 28 |

## NOAA Progress

Completed AWS backfill batch:

| Batch | Run ID | Downloaded | HTTP failures | Bytes | Elapsed seconds |
| ---: | --- | ---: | ---: | ---: | ---: |
| 27 | `noaa_backfill_download_batch27_20260624T070012Z` | 546 | 454 | 3,787,302,418 | 416.387 |

Completed NOAA loads:

| Run ID | Source | Files | Canonical DJF Hours | Invalid Temp Rows | Rejected SOURCE Rows | Rejected Plausibility Rows | Duplicate Hour Count |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `noaa_hourly_djf_load_20260624T070012Z` | inventory | 1,000 | 1,210,464 | 222,064 | 1,637,727 | 3 | 3,973,881 |
| `noaa_hourly_djf_load_20260624T070739Z` | downloaded | 546 | 507,144 | 55,081 | 990,909 | 2 | 608,947 |

Plausibility rejection detail:

| Run ID | Station | Year | Rejected Plausibility Rows | Source File ID |
| --- | --- | ---: | ---: | --- |
| `noaa_hourly_djf_load_20260624T070012Z` | `703830-25310` | 2014 | 3 | `noaa_global_hourly_local_raw_inventory_3e447b31e3e36679` |
| `noaa_hourly_djf_load_20260624T070739Z` | `720267-23224` | 2007 | 2 | `noaa_global_hourly_csv_2007_72026723224_96d1247d6332909e` |

Current NOAA/cache status:

| Metric | Value |
| --- | ---: |
| AWS CSV files | 16,668 |
| AWS `.part` files | 0 |
| AWS cache disk usage | 128 GB |
| Manifest downloaded rows | 16,668 |
| Manifest failed rows | 10,332 |
| Manifest planned rows | 59,839 |
| Manifest skipped rows | 86,839 |

## Refreshed Result Runs

| Layer | Run ID | Rows / Result |
| --- | --- | ---: |
| Station-year coverage | `station_year_djf_coverage_20260624T071037Z` | 36,668 rows; 5,551 complete, 30,263 partial, 854 empty |
| Station ECWT | `station_ecwt_loaded_20260624T071536Z` | 3,122 provisional, 80 blocked |
| Plant ECWT | `plant_ecwt_provisional_20260624T071911Z` | 16,104 provisional, 28 blocked |
| Strict plant readiness | `plant_ecwt_readiness_20260624T071938Z` | 75 publication candidates |
| Diagnostic plant readiness | `plant_ecwt_readiness_20260624T071951Z` | 2,740 diagnostic candidates |

Current canonical weather:

| Metric | Value |
| --- | ---: |
| `weather.hourly_djf` rows | 23,194,562 |
| Distinct stations | 3,122 |
| Minimum dry-bulb F | -61.600 |
| Maximum dry-bulb F | 104.000 |
| `SHEF` rows below `-50 C` | 0 |
| Database size | 9,902 MB |

## Stability Checks

Compared with the previous corrected plant run `plant_ecwt_provisional_20260624T065532Z`:

| Check | Plants |
| --- | ---: |
| Selected station unchanged | 16,094 |
| Selected station changed | 38 |

Compared with previous strict readiness `plant_ecwt_readiness_20260624T065552Z`:

| Transition | Plants |
| --- | ---: |
| Strict candidate remained candidate | 71 |
| Strict low coverage became candidate | 4 |
| Strict low coverage remained low coverage | 16,029 |
| Strict blocked remained blocked | 28 |

Compared with previous diagnostic readiness `plant_ecwt_readiness_20260624T065624Z`:

| Transition | Plants |
| --- | ---: |
| Diagnostic candidate remained candidate | 2,514 |
| Diagnostic candidate became low coverage | 2 |
| Diagnostic low coverage became candidate | 226 |
| Diagnostic low coverage remained low coverage | 13,362 |
| Diagnostic blocked remained blocked | 28 |

## Interpretation

- Batch 27 added `546` NOAA CSVs and there are no `.part` files left in the cache.
- The hardened `SHEF < -50 C` plausibility rule held through this cycle.
- Fixed-denominator strict readiness improved from `71` to `75` publication candidates.
- Fixed-denominator diagnostic readiness improved from `2,516` to `2,740` candidates.
- Five physically implausible rows were rejected across this cycle's two NOAA load runs.
- The immediate next step is to continue the parallel download/load/refresh cycle with batch 28.
