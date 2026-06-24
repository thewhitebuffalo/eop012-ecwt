# NOAA Backfill, Load, And ECWT Refresh Status

Generated UTC: 2026-06-24T09:07Z

Database: `eop012` on `127.0.0.1:5436`

## Summary

This cycle ran AWS backfill batch 31 in parallel with another inventory load, then loaded the new batch 31 downloads and refreshed coverage, station ECWT, corrected plant ECWT, and fixed-denominator plant readiness.

The fixed-denominator strict publication count increased from `100` to `124`. The relaxed diagnostic count increased from `3,289` to `3,719`.

| Metric | Value |
| --- | ---: |
| Plant ECWT rows | 16,132 |
| Strict publication candidates | 124 |
| Strict provisional low coverage | 15,980 |
| Strict blocked | 28 |
| Diagnostic publication candidates at 0.25 coverage | 3,719 |
| Diagnostic provisional low coverage at 0.25 coverage | 12,385 |
| Diagnostic blocked | 28 |

## NOAA Progress

Completed AWS backfill batch:

| Batch | Run ID | Downloaded | HTTP failures | Bytes | Elapsed seconds |
| ---: | --- | ---: | ---: | ---: | ---: |
| 31 | `noaa_backfill_download_batch31_20260624T084828Z` | 420 | 580 | 3,205,014,469 | 371.279 |

Completed NOAA loads:

| Run ID | Source | Files | Canonical DJF Hours | Invalid Temp Rows | Rejected SOURCE Rows | Rejected Plausibility Rows | Duplicate Hour Count |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `noaa_hourly_djf_load_20260624T084828Z` | inventory | 1,000 | 1,058,877 | 135,054 | 2,023,338 | 35 | 3,194,239 |
| `noaa_hourly_djf_load_20260624T085516Z` | downloaded | 420 | 497,849 | 46,967 | 591,785 | 0 | 712,170 |

Plausibility rejection detail:

| Run ID | Station | Year | Rejected Plausibility Rows | Source File ID |
| --- | --- | ---: | ---: | --- |
| `noaa_hourly_djf_load_20260624T084828Z` | `703830-25310` | 2012 | 12 | `noaa_global_hourly_local_raw_inventory_3e447b31e3e36679` |
| `noaa_hourly_djf_load_20260624T084828Z` | `720966-00339` | 2012 | 23 | `noaa_global_hourly_local_raw_inventory_3e447b31e3e36679` |

Current NOAA/cache status:

| Metric | Value |
| --- | ---: |
| AWS CSV files | 18,519 |
| AWS `.part` files | 0 |
| AWS cache disk usage | 144 GB |
| Manifest downloaded rows | 18,519 |
| Manifest failed rows | 12,481 |
| Manifest planned rows | 55,839 |
| Manifest skipped rows | 86,839 |

## Refreshed Result Runs

| Layer | Run ID | Rows / Result |
| --- | --- | ---: |
| Station-year coverage | `station_year_djf_coverage_20260624T085731Z` | 42,519 rows; 7,033 complete, 34,537 partial, 949 empty |
| Station ECWT | `station_ecwt_loaded_20260624T090140Z` | 3,155 provisional, 84 blocked |
| Plant ECWT | `plant_ecwt_provisional_20260624T090344Z` | 16,104 provisional, 28 blocked |
| Strict plant readiness | `plant_ecwt_readiness_20260624T090509Z` | 124 publication candidates |
| Diagnostic plant readiness | `plant_ecwt_readiness_20260624T090522Z` | 3,719 diagnostic candidates |

Current canonical weather:

| Metric | Value |
| --- | ---: |
| `weather.hourly_djf` rows | 27,796,268 |
| Distinct stations | 3,155 |
| Minimum dry-bulb F | -61.600 |
| Maximum dry-bulb F | 104.000 |
| `SHEF` rows below `-50 C` | 0 |
| Database size | 11 GB |

## Stability Checks

Compared with the previous corrected plant run `plant_ecwt_provisional_20260624T084134Z`:

| Check | Plants |
| --- | ---: |
| Selected station unchanged | 15,967 |
| Selected station changed | 165 |

Compared with previous strict readiness `plant_ecwt_readiness_20260624T084240Z`:

| Transition | Plants |
| --- | ---: |
| Strict candidate remained candidate | 100 |
| Strict low coverage became candidate | 24 |
| Strict low coverage remained low coverage | 15,980 |
| Strict blocked remained blocked | 28 |

Compared with previous diagnostic readiness `plant_ecwt_readiness_20260624T084258Z`:

| Transition | Plants |
| --- | ---: |
| Diagnostic candidate remained candidate | 3,288 |
| Diagnostic candidate became low coverage | 1 |
| Diagnostic low coverage became candidate | 431 |
| Diagnostic low coverage remained low coverage | 12,384 |
| Diagnostic blocked remained blocked | 28 |

## Interpretation

- Batch 31 added `420` NOAA CSVs and there are no `.part` files left in the cache.
- The hardened `SHEF < -50 C` plausibility rule held through this cycle.
- Fixed-denominator strict readiness improved from `100` to `124` publication candidates.
- Fixed-denominator diagnostic readiness improved from `3,289` to `3,719` candidates.
- Thirty-five physically implausible rows were rejected from two 2012 inventory station-years.
- The immediate next step is to continue the parallel download/load/refresh cycle with batch 32.
