# NOAA Backfill, Load, And ECWT Refresh Status

Generated UTC: 2026-06-24T10:20Z

Database: `eop012` on `127.0.0.1:5436`

## Summary

This cycle ran AWS backfill batch 34 in parallel with another inventory load, then loaded the new batch 34 downloads and refreshed coverage, station ECWT, corrected plant ECWT, and fixed-denominator plant readiness.

The fixed-denominator strict publication count increased from `234` to `267`. The relaxed diagnostic count increased from `4,492` to `4,585`.

| Metric | Value |
| --- | ---: |
| Plant ECWT rows | 16,132 |
| Strict publication candidates | 267 |
| Strict provisional low coverage | 15,837 |
| Strict blocked | 28 |
| Diagnostic publication candidates at 0.25 coverage | 4,585 |
| Diagnostic provisional low coverage at 0.25 coverage | 11,519 |
| Diagnostic blocked | 28 |

## NOAA Progress

Completed AWS backfill batch:

| Batch | Run ID | Downloaded | HTTP failures | Exception failures | Bytes | Elapsed seconds |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 34 | `noaa_backfill_download_batch34_20260624T095858Z` | 330 | 668 | 2 | 2,182,031,367 | 241.671 |

Completed NOAA loads:

| Run ID | Source | Files | Canonical DJF Hours | Invalid Temp Rows | Rejected SOURCE Rows | Rejected Plausibility Rows | Duplicate Hour Count |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `noaa_hourly_djf_load_20260624T095857Z` | inventory | 1,000 | 819,409 | 75,481 | 2,040,068 | 4 | 666,496 |
| `noaa_hourly_djf_load_20260624T100353Z` | downloaded | 330 | 395,467 | 91,298 | 341,445 | 0 | 414,068 |

Plausibility rejection detail:

| Run ID | Station | Year | Rejected Plausibility Rows | Source File ID |
| --- | --- | ---: | ---: | --- |
| `noaa_hourly_djf_load_20260624T095857Z` | `722201-03723` | 2006 | 4 | `noaa_global_hourly_local_raw_inventory_3e447b31e3e36679` |

Current NOAA/cache status:

| Metric | Value |
| --- | ---: |
| AWS CSV files | 19,600 |
| AWS `.part` files | 0 |
| AWS cache disk usage | 151 GB |
| Manifest downloaded rows | 19,600 |
| Manifest failed rows | 14,400 |
| Manifest planned rows | 52,839 |
| Manifest skipped rows | 86,839 |

## Refreshed Result Runs

| Layer | Run ID | Rows / Result |
| --- | --- | ---: |
| Station-year coverage | `station_year_djf_coverage_20260624T100636Z` | 46,600 rows; 8,196 complete, 37,380 partial, 1,024 empty |
| Station ECWT | `station_ecwt_loaded_20260624T101132Z` | 3,546 provisional, 99 blocked |
| Plant ECWT | `plant_ecwt_provisional_20260624T101640Z` | 16,104 provisional, 28 blocked |
| Strict plant readiness | `plant_ecwt_readiness_20260624T101730Z` | 267 publication candidates |
| Diagnostic plant readiness | `plant_ecwt_readiness_20260624T101745Z` | 4,585 diagnostic candidates |

Current canonical weather:

| Metric | Value |
| --- | ---: |
| `weather.hourly_djf` rows | 31,416,726 |
| Distinct stations | 3,546 |
| Minimum dry-bulb F | -61.600 |
| Maximum dry-bulb F | 104.000 |
| `SHEF` rows below `-50 C` | 0 |
| Database size | 13 GB |

## Stability Checks

Compared with the previous corrected plant run `plant_ecwt_provisional_20260624T095247Z`:

| Check | Plants |
| --- | ---: |
| Selected station unchanged | 16,043 |
| Selected station changed | 89 |

Compared with previous strict readiness `plant_ecwt_readiness_20260624T095424Z`:

| Transition | Plants |
| --- | ---: |
| Strict candidate remained candidate | 234 |
| Strict low coverage became candidate | 33 |
| Strict low coverage remained low coverage | 15,837 |
| Strict blocked remained blocked | 28 |

Compared with previous diagnostic readiness `plant_ecwt_readiness_20260624T095435Z`:

| Transition | Plants |
| --- | ---: |
| Diagnostic candidate remained candidate | 4,488 |
| Diagnostic candidate became low coverage | 4 |
| Diagnostic low coverage became candidate | 97 |
| Diagnostic low coverage remained low coverage | 11,515 |
| Diagnostic blocked remained blocked | 28 |

## Interpretation

- Batch 34 added `330` NOAA CSVs and there are no `.part` files left in the cache.
- The downloader recorded `2` exception failures in addition to `668` HTTP failures; successful files were still loaded and audited.
- The hardened `SHEF < -50 C` plausibility rule held through this cycle.
- Fixed-denominator strict readiness improved from `234` to `267` publication candidates.
- Fixed-denominator diagnostic readiness improved from `4,492` to `4,585` candidates, despite `4` prior diagnostic candidates falling back to low coverage.
- Four physically implausible rows were rejected from one 2006 inventory station-year.
- Station selection changed for `89` plants, so station-selection churn remains a monitored QA signal while backfill coverage is still incomplete.
- The immediate next step is to continue the parallel download/load/refresh cycle with batch 35.
