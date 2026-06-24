# NOAA Backfill, Load, And ECWT Refresh Status

Generated UTC: 2026-06-24T03:54Z

Database: `eop012` on `127.0.0.1:5436`

## Summary

This cycle ran AWS backfill batch 19 in parallel with another inventory load, then loaded downloaded files and refreshed coverage, station ECWT, plant ECWT, and plant readiness.

Strict publication candidates changed from `2,599` to `2,494`. The movement is not monotonic because the provisional station-selection algorithm can choose a different station as coverage changes. The dataset is still not publication-complete because most plants remain below the strict coverage threshold.

| Metric | Value |
| --- | ---: |
| Plant ECWT rows | 16,132 |
| Strict publication candidates | 2,494 |
| Strict provisional low coverage | 13,610 |
| Strict blocked | 28 |
| Diagnostic publication candidates at 0.25 coverage | 13,289 |
| Diagnostic provisional low coverage at 0.25 coverage | 2,815 |
| Diagnostic blocked | 28 |

## NOAA Progress

Completed AWS backfill batch:

| Batch | Run ID | Downloaded | HTTP failures | Bytes | Elapsed seconds |
| ---: | --- | ---: | ---: | ---: | ---: |
| 19 | `noaa_backfill_download_batch19_20260624T033552Z` | 624 | 376 | 5,469,308,070 | 456.730 |

Completed NOAA loads:

| Run ID | Source | Files | Canonical DJF Hours | Invalid Temp Rows | Rejected SOURCE Rows | Rejected Plausibility Rows | Duplicate Hour Count |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `noaa_hourly_djf_load_20260624T033552Z` | inventory | 1,000 | 245,839 | 75,975 | 3,622,739 | 0 | 162,850 |
| `noaa_hourly_djf_load_20260624T034358Z` | downloaded | 624 | 351,338 | 53,571 | 1,793,630 | 0 | 868,313 |

Current NOAA/cache status:

| Metric | Value |
| --- | ---: |
| AWS CSV files | 12,115 |
| AWS `.part` files | 0 |
| AWS cache disk usage | 94 GB |
| Manifest downloaded rows | 12,115 |
| Manifest failed rows | 6,885 |
| Manifest planned rows | 67,839 |
| Manifest skipped rows | 86,839 |

## Refreshed Result Runs

| Layer | Run ID | Rows / Result |
| --- | --- | ---: |
| Station-year coverage | `station_year_djf_coverage_20260624T034627Z` | 24,115 rows; 3,356 complete, 20,188 partial, 571 empty |
| Station ECWT | `station_ecwt_loaded_20260624T034859Z` | 3,080 provisional, 75 blocked |
| Plant ECWT | `plant_ecwt_provisional_20260624T035120Z` | 16,104 provisional, 28 blocked |
| Strict plant readiness | `plant_ecwt_readiness_20260624T035218Z` | 2,494 publication candidates |
| Diagnostic plant readiness | `plant_ecwt_readiness_20260624T035231Z` | 13,289 diagnostic candidates |

Current canonical weather:

| Metric | Value |
| --- | ---: |
| `weather.hourly_djf` rows | 15,084,286 |
| Distinct stations | 3,080 |
| Minimum dry-bulb F | -61.060 |
| Maximum dry-bulb F | 104.000 |
| `SHEF` rows below `-50 C` | 0 |
| Database size | 6,409 MB |

## Interpretation

- Strict readiness moved down from `2,599` to `2,494`; this confirms that current provisional station selection is coverage-sensitive and not monotonic.
- The dominant blocker remains weather coverage: `13,610` plants are still below the strict coverage threshold.
- The hardened `SHEF < -50 C` plausibility rule held through this cycle: no canonical rows violate it.
- The immediate next step remains another parallel download/load/refresh cycle, with growing priority on stabilizing station selection before any publication claim.
