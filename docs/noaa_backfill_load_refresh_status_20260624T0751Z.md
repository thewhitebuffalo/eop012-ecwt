# NOAA Backfill, Load, And ECWT Refresh Status

Generated UTC: 2026-06-24T07:51Z

Database: `eop012` on `127.0.0.1:5436`

## Summary

This cycle ran AWS backfill batch 28 in parallel with another inventory load, then loaded the new batch 28 downloads and refreshed coverage, station ECWT, corrected plant ECWT, and fixed-denominator plant readiness.

The fixed-denominator strict publication count remained `75`. The relaxed diagnostic count increased from `2,740` to `2,823`.

| Metric | Value |
| --- | ---: |
| Plant ECWT rows | 16,132 |
| Strict publication candidates | 75 |
| Strict provisional low coverage | 16,029 |
| Strict blocked | 28 |
| Diagnostic publication candidates at 0.25 coverage | 2,823 |
| Diagnostic provisional low coverage at 0.25 coverage | 13,281 |
| Diagnostic blocked | 28 |

## NOAA Progress

Completed AWS backfill batch:

| Batch | Run ID | Downloaded | HTTP failures | Bytes | Elapsed seconds |
| ---: | --- | ---: | ---: | ---: | ---: |
| 28 | `noaa_backfill_download_batch28_20260624T072817Z` | 519 | 481 | 4,570,697,032 | 591.532 |

Completed NOAA loads:

| Run ID | Source | Files | Canonical DJF Hours | Invalid Temp Rows | Rejected SOURCE Rows | Rejected Plausibility Rows | Duplicate Hour Count |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `noaa_hourly_djf_load_20260624T072817Z` | inventory | 1,000 | 225,992 | 89,387 | 3,618,949 | 0 | 115,607 |
| `noaa_hourly_djf_load_20260624T073851Z` | downloaded | 519 | 541,084 | 39,898 | 1,042,828 | 1 | 952,350 |

Plausibility rejection detail:

| Run ID | Station | Year | Rejected Plausibility Rows | Source File ID |
| --- | --- | ---: | ---: | --- |
| `noaa_hourly_djf_load_20260624T073851Z` | `722017-12876` | 2007 | 1 | `noaa_global_hourly_csv_2007_72201712876_5c18ffda4841e9b0` |

Current NOAA/cache status:

| Metric | Value |
| --- | ---: |
| AWS CSV files | 17,187 |
| AWS `.part` files | 0 |
| AWS cache disk usage | 133 GB |
| Manifest downloaded rows | 17,187 |
| Manifest failed rows | 10,813 |
| Manifest planned rows | 58,839 |
| Manifest skipped rows | 86,839 |

## Refreshed Result Runs

| Layer | Run ID | Rows / Result |
| --- | --- | ---: |
| Station-year coverage | `station_year_djf_coverage_20260624T074137Z` | 38,187 rows; 5,725 complete, 31,602 partial, 860 empty |
| Station ECWT | `station_ecwt_loaded_20260624T074509Z` | 3,126 provisional, 81 blocked |
| Plant ECWT | `plant_ecwt_provisional_20260624T074807Z` | 16,104 provisional, 28 blocked |
| Strict plant readiness | `plant_ecwt_readiness_20260624T074841Z` | 75 publication candidates |
| Diagnostic plant readiness | `plant_ecwt_readiness_20260624T074850Z` | 2,823 diagnostic candidates |

Current canonical weather:

| Metric | Value |
| --- | ---: |
| `weather.hourly_djf` rows | 23,961,638 |
| Distinct stations | 3,126 |
| Minimum dry-bulb F | -61.600 |
| Maximum dry-bulb F | 104.000 |
| `SHEF` rows below `-50 C` | 0 |
| Database size | 10,234 MB |

## Stability Checks

Compared with the previous corrected plant run `plant_ecwt_provisional_20260624T071911Z`:

| Check | Plants |
| --- | ---: |
| Selected station unchanged | 16,114 |
| Selected station changed | 18 |

Compared with previous strict readiness `plant_ecwt_readiness_20260624T071938Z`:

| Transition | Plants |
| --- | ---: |
| Strict candidate remained candidate | 75 |
| Strict low coverage remained low coverage | 16,029 |
| Strict blocked remained blocked | 28 |

Compared with previous diagnostic readiness `plant_ecwt_readiness_20260624T071951Z`:

| Transition | Plants |
| --- | ---: |
| Diagnostic candidate remained candidate | 2,723 |
| Diagnostic candidate became low coverage | 17 |
| Diagnostic low coverage became candidate | 100 |
| Diagnostic low coverage remained low coverage | 13,264 |
| Diagnostic blocked remained blocked | 28 |

## Interpretation

- Batch 28 added `519` NOAA CSVs and there are no `.part` files left in the cache.
- The hardened `SHEF < -50 C` plausibility rule held through this cycle.
- Fixed-denominator strict readiness remained at `75` publication candidates.
- Fixed-denominator diagnostic readiness improved from `2,740` to `2,823` candidates.
- One physically implausible row was rejected from station `722017-12876` for 2007.
- The immediate next step is to continue the parallel download/load/refresh cycle with batch 29.
