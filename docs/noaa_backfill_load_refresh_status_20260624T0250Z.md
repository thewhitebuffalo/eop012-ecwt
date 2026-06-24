# NOAA Backfill, Load, And ECWT Refresh Status

Generated UTC: 2026-06-24T02:50Z

Database: `eop012` on `127.0.0.1:5436`

## Summary

This cycle ran AWS backfill batch 17 in parallel with another inventory load, then loaded downloaded files and refreshed coverage, station ECWT, plant ECWT, and plant readiness.

Strict publication candidates increased sharply from `298` to `2,485`. The dataset is still not publication-complete because most plants remain below the strict coverage threshold.

| Metric | Value |
| --- | ---: |
| Plant ECWT rows | 16,132 |
| Strict publication candidates | 2,485 |
| Strict provisional low coverage | 13,619 |
| Strict blocked | 28 |
| Diagnostic publication candidates at 0.25 coverage | 13,518 |
| Diagnostic provisional low coverage at 0.25 coverage | 2,586 |
| Diagnostic blocked | 28 |

## NOAA Progress

Completed AWS backfill batch:

| Batch | Run ID | Downloaded | HTTP failures | Bytes | Elapsed seconds |
| ---: | --- | ---: | ---: | ---: | ---: |
| 17 | `noaa_backfill_download_batch17_20260624T022728Z` | 618 | 382 | 5,680,652,802 | 614.430 |

Completed NOAA loads:

| Run ID | Source | Files | Canonical DJF Hours | Invalid Temp Rows | Rejected SOURCE Rows | Rejected Plausibility Rows | Duplicate Hour Count |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `noaa_hourly_djf_load_20260624T022727Z` | inventory | 1,000 | 285,123 | 78,619 | 3,729,771 | 0 | 180,858 |
| `noaa_hourly_djf_load_20260624T023804Z` | downloaded | 846 | 912,006 | 140,271 | 1,259,675 | 0 | 3,772,878 |

Current NOAA/cache status:

| Metric | Value |
| --- | ---: |
| AWS CSV files | 10,846 |
| AWS `.part` files | 0 |
| AWS cache disk usage | 85 GB |
| Manifest downloaded rows | 10,846 |
| Manifest failed rows | 6,154 |
| Manifest planned rows | 69,839 |
| Manifest skipped rows | 86,839 |

## Refreshed Result Runs

| Layer | Run ID | Rows / Result |
| --- | --- | ---: |
| Station-year coverage | `station_year_djf_coverage_20260624T024300Z` | 20,846 rows; 2,802 complete, 17,548 partial, 496 empty |
| Station ECWT | `station_ecwt_loaded_20260624T024617Z` | 3,069 provisional, 72 blocked |
| Plant ECWT | `plant_ecwt_provisional_20260624T024724Z` | 16,104 provisional, 28 blocked |
| Strict plant readiness | `plant_ecwt_readiness_20260624T024811Z` | 2,485 publication candidates |
| Diagnostic plant readiness | `plant_ecwt_readiness_20260624T024829Z` | 13,518 diagnostic candidates |

Current canonical weather:

| Metric | Value |
| --- | ---: |
| `weather.hourly_djf` rows | 13,119,500 |
| Distinct stations | 3,069 |
| Minimum dry-bulb F | -68.440 |
| Maximum dry-bulb F | 104.000 |
| Database size | 5,563 MB |

## Interpretation

- Strict readiness made the largest single-cycle jump so far, from `298` to `2,485` publication candidates.
- The dominant blocker remains weather coverage: `13,619` plants are still below the strict coverage threshold.
- The downloaded-source loader selected `846` files rather than `1,000`, which suggests the current downloaded candidate queue was exhausted under the loader selection rules after batch 17.
- The immediate next step is another parallel download/load/refresh cycle. If downloaded loads continue selecting fewer than the requested limit, rebuild or inspect the raw-file inventory before assuming the cache is fully consumed.
