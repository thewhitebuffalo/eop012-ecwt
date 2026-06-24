# NOAA Backfill, Load, And ECWT Refresh Status

Generated UTC: 2026-06-24T11:07Z

Database: `eop012` on `127.0.0.1:5436`

## Summary

This cycle ran AWS backfill batch 36, hardened the NOAA DJF loader for exhausted selectors, recorded an inventory-selector no-op load, loaded the new batch 36 downloads, and refreshed coverage, station ECWT, plant ECWT, and fixed-denominator plant readiness.

The fixed-denominator strict publication count increased from `318` to `525`. The relaxed diagnostic count increased from `4,608` to `4,989`.

| Metric | Value |
| --- | ---: |
| Plant ECWT rows | 16,132 |
| Strict publication candidates | 525 |
| Strict provisional low coverage | 15,579 |
| Strict blocked | 28 |
| Diagnostic publication candidates at 0.25 coverage | 4,989 |
| Diagnostic provisional low coverage at 0.25 coverage | 11,115 |
| Diagnostic blocked | 28 |

## NOAA Progress

Completed AWS backfill batch:

| Batch | Run ID | Downloaded | HTTP failures | Exception failures | Bytes | Elapsed seconds |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 36 | `noaa_backfill_download_batch36_20260624T104511Z` | 373 | 627 | 0 | 2,179,465,271 | 295.934 |

Completed NOAA loads:

| Run ID | Source | Files | Canonical DJF Hours | Invalid Temp Rows | Rejected SOURCE Rows | Rejected Plausibility Rows | Duplicate Hour Count |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `noaa_hourly_djf_load_20260624T104729Z` | inventory | 0 | 0 | 0 | 0 | 0 | 0 |
| `noaa_hourly_djf_load_20260624T105050Z` | downloaded | 373 | 543,677 | 351,637 | 39,133 | 0 | 296,220 |

Plausibility rejection detail: none in this cycle.

Current NOAA/cache status:

| Metric | Value |
| --- | ---: |
| AWS CSV files | 20,282 |
| AWS `.part` / `.partial` files | 0 |
| AWS raw cache disk usage | 155 GB |
| Manifest downloaded rows | 20,282 |
| Manifest failed rows | 15,718 |
| Manifest planned rows | 50,839 |
| Manifest skipped rows | 86,839 |

## Refreshed Result Runs

| Layer | Run ID | Rows / Result |
| --- | --- | ---: |
| Station-year coverage | `station_year_djf_coverage_20260624T105442Z` | 47,843 rows; 8,690 complete, 38,066 partial, 1,087 empty |
| Station ECWT | `station_ecwt_loaded_20260624T105838Z` | 3,678 provisional, 112 blocked |
| Plant ECWT | `plant_ecwt_provisional_20260624T110204Z` | 16,104 provisional, 28 blocked |
| Strict plant readiness | `plant_ecwt_readiness_20260624T110422Z` | 525 publication candidates |
| Diagnostic plant readiness | `plant_ecwt_readiness_20260624T110431Z` | 4,989 diagnostic candidates |

Current canonical weather:

| Metric | Value |
| --- | ---: |
| `weather.hourly_djf` rows | 32,894,957 |
| Distinct stations | 3,678 |
| Minimum dry-bulb F | -67.000 |
| Maximum dry-bulb F | 104.000 |
| `SHEF` rows below `-50 C` | 0 |
| Database size | 14 GB |

## Stability Checks

Compared with the previous plant run `plant_ecwt_provisional_20260624T103934Z`:

| Check | Plants |
| --- | ---: |
| Selected station unchanged | 15,938 |
| Selected station changed | 194 |

Compared with previous strict readiness `plant_ecwt_readiness_20260624T104012Z`:

| Transition | Plants |
| --- | ---: |
| Strict candidate remained candidate | 318 |
| Strict low coverage became candidate | 207 |
| Strict low coverage remained low coverage | 15,579 |
| Strict blocked remained blocked | 28 |

Compared with previous diagnostic readiness `plant_ecwt_readiness_20260624T104030Z`:

| Transition | Plants |
| --- | ---: |
| Diagnostic candidate remained candidate | 4,598 |
| Diagnostic candidate became low coverage | 10 |
| Diagnostic low coverage became candidate | 391 |
| Diagnostic low coverage remained low coverage | 11,105 |
| Diagnostic blocked remained blocked | 28 |

## Loader Hardening

The inventory selector returned zero eligible files in this cycle. The loader now treats that condition as an auditable no-op, writes a normal report, records run parameters including `no_candidate_files_selected`, and loads zero rows instead of raising an exception.

## Interpretation

- Batch 36 added `373` NOAA CSVs and there are no incomplete raw downloads left in the cache.
- The inventory selector is exhausted for the current source-selection criteria; the remaining forward progress is coming from AWS backfill batches and downloaded-file loads.
- The hardened `SHEF < -50 C` plausibility rule held through this cycle.
- Fixed-denominator strict readiness improved from `318` to `525` publication candidates.
- Fixed-denominator diagnostic readiness improved from `4,608` to `4,989` candidates, with `10` diagnostic candidates moving back to low coverage as selected stations changed.
- No physically implausible rows were rejected in either batch-36 load.
- Station selection changed for `194` plants, so station-selection churn remains a QA signal while weather coverage is incomplete.
- The immediate next step is to continue the parallel download/load/refresh cycle with batch 37.
