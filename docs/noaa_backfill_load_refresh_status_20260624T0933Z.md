# NOAA Backfill, Load, And ECWT Refresh Status

Generated UTC: 2026-06-24T09:33Z

Database: `eop012` on `127.0.0.1:5436`

## Summary

This cycle ran AWS backfill batch 32 in parallel with another inventory load, then loaded the new batch 32 downloads and refreshed coverage, station ECWT, corrected plant ECWT, and fixed-denominator plant readiness.

The fixed-denominator strict publication count increased from `124` to `139`. The relaxed diagnostic count increased from `3,719` to `4,250`.

| Metric | Value |
| --- | ---: |
| Plant ECWT rows | 16,132 |
| Strict publication candidates | 139 |
| Strict provisional low coverage | 15,965 |
| Strict blocked | 28 |
| Diagnostic publication candidates at 0.25 coverage | 4,250 |
| Diagnostic provisional low coverage at 0.25 coverage | 11,854 |
| Diagnostic blocked | 28 |

## NOAA Progress

Completed AWS backfill batch:

| Batch | Run ID | Downloaded | HTTP failures | Bytes | Elapsed seconds |
| ---: | --- | ---: | ---: | ---: | ---: |
| 32 | `noaa_backfill_download_batch32_20260624T091132Z` | 370 | 630 | 2,614,943,516 | 321.487 |

Completed NOAA loads:

| Run ID | Source | Files | Canonical DJF Hours | Invalid Temp Rows | Rejected SOURCE Rows | Rejected Plausibility Rows | Duplicate Hour Count |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `noaa_hourly_djf_load_20260624T091132Z` | inventory | 1,000 | 244,652 | 80,512 | 3,512,780 | 0 | 131,263 |
| `noaa_hourly_djf_load_20260624T091725Z` | downloaded | 370 | 445,391 | 125,648 | 430,428 | 1 | 495,396 |

Plausibility rejection detail:

| Run ID | Station | Year | Rejected Plausibility Rows | Source File ID |
| --- | --- | ---: | ---: | --- |
| `noaa_hourly_djf_load_20260624T091725Z` | `722535-12909` | 2005 | 1 | `noaa_global_hourly_csv_2005_72253512909_a9c0d55dca0cbff6` |

Current NOAA/cache status:

| Metric | Value |
| --- | ---: |
| AWS CSV files | 18,889 |
| AWS `.part` files | 0 |
| AWS cache disk usage | 147 GB |
| Manifest downloaded rows | 18,889 |
| Manifest failed rows | 13,111 |
| Manifest planned rows | 54,839 |
| Manifest skipped rows | 86,839 |

## Refreshed Result Runs

| Layer | Run ID | Rows / Result |
| --- | --- | ---: |
| Station-year coverage | `station_year_djf_coverage_20260624T091944Z` | 43,889 rows; 7,201 complete, 35,731 partial, 957 empty |
| Station ECWT | `station_ecwt_loaded_20260624T092541Z` | 3,293 provisional, 86 blocked |
| Plant ECWT | `plant_ecwt_provisional_20260624T092912Z` | 16,104 provisional, 28 blocked |
| Strict plant readiness | `plant_ecwt_readiness_20260624T093031Z` | 139 publication candidates |
| Diagnostic plant readiness | `plant_ecwt_readiness_20260624T093040Z` | 4,250 diagnostic candidates |

Current canonical weather:

| Metric | Value |
| --- | ---: |
| `weather.hourly_djf` rows | 28,486,311 |
| Distinct stations | 3,293 |
| Minimum dry-bulb F | -61.600 |
| Maximum dry-bulb F | 104.000 |
| `SHEF` rows below `-50 C` | 0 |
| Database size | 12 GB |

## Stability Checks

Compared with the previous corrected plant run `plant_ecwt_provisional_20260624T090344Z`:

| Check | Plants |
| --- | ---: |
| Selected station unchanged | 15,316 |
| Selected station changed | 816 |

Compared with previous strict readiness `plant_ecwt_readiness_20260624T090509Z`:

| Transition | Plants |
| --- | ---: |
| Strict candidate remained candidate | 124 |
| Strict low coverage became candidate | 15 |
| Strict low coverage remained low coverage | 15,965 |
| Strict blocked remained blocked | 28 |

Compared with previous diagnostic readiness `plant_ecwt_readiness_20260624T090522Z`:

| Transition | Plants |
| --- | ---: |
| Diagnostic candidate remained candidate | 3,717 |
| Diagnostic candidate became low coverage | 2 |
| Diagnostic low coverage became candidate | 533 |
| Diagnostic low coverage remained low coverage | 11,852 |
| Diagnostic blocked remained blocked | 28 |

## Interpretation

- Batch 32 added `370` NOAA CSVs and there are no `.part` files left in the cache.
- The hardened `SHEF < -50 C` plausibility rule held through this cycle.
- Fixed-denominator strict readiness improved from `124` to `139` publication candidates.
- Fixed-denominator diagnostic readiness improved from `3,719` to `4,250` candidates.
- One physically implausible row was rejected from one 2005 downloaded station-year.
- Station selection changed for `816` plants, so station-selection churn should remain a monitored QA signal while backfill coverage is still incomplete.
- The immediate next step is to continue the parallel download/load/refresh cycle with batch 33.
