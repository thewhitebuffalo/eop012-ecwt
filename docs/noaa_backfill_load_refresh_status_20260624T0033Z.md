# NOAA Backfill, Load, And ECWT Refresh Status

Generated UTC: 2026-06-24T00:33Z

Database: `eop012` on `127.0.0.1:5436`

## Summary

This cycle ran AWS backfill batch 12 in parallel with another inventory load, then loaded downloaded files and refreshed coverage, station ECWT, plant ECWT, and plant readiness.

The strict publication gate is no longer zero: `169` plants now meet the current provisional publication-candidate thresholds. Most plants are still below the strict coverage threshold, so the dataset is not publication-complete.

| Metric | Value |
| --- | ---: |
| Plant ECWT rows | 16,132 |
| Strict publication candidates | 169 |
| Strict provisional low coverage | 15,935 |
| Strict blocked | 28 |
| Diagnostic publication candidates at 0.25 coverage | 13,384 |
| Diagnostic provisional low coverage at 0.25 coverage | 2,720 |
| Diagnostic blocked | 28 |

## NOAA Progress

Completed AWS backfill batch:

| Batch | Run ID | Downloaded | HTTP failures | Bytes |
| ---: | --- | ---: | ---: | ---: |
| 12 | `noaa_backfill_download_batch12_20260624T001545Z` | 614 | 386 | 5,922,237,084 |

Completed NOAA loads:

| Run ID | Source | Files | Canonical DJF Hours | Invalid Temp Rows | Rejected SOURCE Rows | Rejected Plausibility Rows | Duplicate Hour Count |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `noaa_hourly_djf_load_20260624T001544Z` | inventory | 1,000 | 766,174 | 169,727 | 2,550,654 | 0 | 2,568,588 |
| `noaa_hourly_djf_load_20260624T002205Z` | downloaded | 1,000 | 1,380,573 | 252,447 | 985,529 | 14 | 4,261,446 |

Current NOAA/cache status:

| Metric | Value |
| --- | ---: |
| AWS CSV files | 7,691 |
| AWS `.part` files | 0 |
| AWS cache disk usage | 58 GB |
| Manifest downloaded rows | 7,691 |
| Manifest failed rows | 4,309 |
| Manifest planned rows | 74,839 |
| Manifest skipped rows | 86,839 |

## Refreshed Result Runs

| Layer | Run ID | Rows / Result |
| --- | --- | ---: |
| Station-year coverage | `station_year_djf_coverage_20260624T002843Z` | 11,000 rows; 1,312 complete, 9,395 partial, 293 empty |
| Station ECWT | `station_ecwt_loaded_20260624T002938Z` | 2,841 provisional, 74 blocked |
| Plant ECWT | `plant_ecwt_provisional_20260624T003116Z` | 16,104 provisional, 28 blocked |
| Strict plant readiness | `plant_ecwt_readiness_20260624T003201Z` | 169 publication candidates |
| Diagnostic plant readiness | `plant_ecwt_readiness_20260624T003209Z` | 13,384 diagnostic candidates |

Current canonical weather:

| Metric | Value |
| --- | ---: |
| `weather.hourly_djf` rows | 7,070,538 |
| Distinct stations | 2,841 |
| Minimum dry-bulb F | -56.920 |
| Maximum dry-bulb F | 104.000 |
| Database size | 3,230 MB |

## Interpretation

- Coverage is improving enough to produce the first strict publication candidates.
- The dominant blocker remains weather coverage: `15,935` plants are still provisional because they do not meet the strict coverage gate.
- The relaxed diagnostic gate rose from `12,770` to `13,384` candidates, showing continued but incomplete progress.
- The immediate next step remains another parallel download/load/refresh cycle.
