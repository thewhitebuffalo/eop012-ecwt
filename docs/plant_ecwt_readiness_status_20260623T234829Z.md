# Plant ECWT Readiness Status

Generated UTC: 2026-06-23T23:48:29Z

Database: `eop012` on `127.0.0.1:5436`

## Summary

This pass added an explicit plant ECWT readiness gate and continued the NOAA download/load/refresh loop.

Latest strict readiness run: `plant_ecwt_readiness_20260623T234820Z`

| Metric | Value |
| --- | ---: |
| Readiness rows | 16,132 |
| Publication candidates | 0 |
| Provisional low coverage | 16,104 |
| Blocked | 28 |
| Minimum coverage ratio | 0.0353 |
| Median coverage ratio | 0.7449 |

The strict readiness gate uses:

| Threshold | Value |
| --- | ---: |
| Minimum valid DJF hours | 2,000 |
| Minimum coverage ratio | 0.95 |

Under a diagnostic relaxed gate using `2,000` valid hours and `0.25` coverage ratio, `10,292` plants currently pass. That diagnostic gate is useful for tracking progress, but it is not a publication gate.

## NOAA Progress

Completed AWS backfill batch:

| Batch | Run ID | Downloaded | HTTP 404 | Bytes |
| ---: | --- | ---: | ---: | ---: |
| 10 | `noaa_backfill_download_batch10_20260623T232806Z` | 661 | 339 | 6,013,209,787 |

Completed hardened NOAA loads:

| Run ID | Source | Files | Canonical DJF Hours | Rejected SOURCE Rows | Rejected Plausibility Rows |
| --- | --- | ---: | ---: | ---: | ---: |
| `noaa_hourly_djf_load_20260623T233448Z` | inventory | 1,000 | 1,151,096 | 1,546,626 | 0 |
| `noaa_hourly_djf_load_20260623T234021Z` | downloaded | 1,000 | 551,521 | 3,166,433 | 0 |

Current NOAA/cache status:

| Metric | Value |
| --- | ---: |
| AWS CSV files | 6,451 |
| AWS `.part` files | 0 |
| AWS cache disk usage | 47 GB |
| Manifest downloaded rows | 6,451 |
| Manifest failed rows | 3,549 |
| Manifest planned rows | 76,839 |
| Manifest skipped rows | 86,839 |

## Weather And Result State

The canonical loader defaults now reject NOAA `SOURCE=7`, temperatures below `-65 C`, and temperatures above `40 C`. A QA cleanup removed two DJF hot outliers above `40 C`; one boundary row at exactly `40.000 C` remains under the inclusive threshold and does not affect cold ECWT minima.

Latest weather/result runs:

| Layer | Run ID | Rows / Result |
| --- | --- | ---: |
| Station-year coverage | `station_year_djf_coverage_20260623T234705Z` | 7,000 rows |
| Station ECWT | `station_ecwt_loaded_20260623T234720Z` | 2,780 provisional, 70 blocked |
| Plant ECWT | `plant_ecwt_provisional_20260623T234745Z` | 16,104 provisional, 28 blocked |
| Plant readiness | `plant_ecwt_readiness_20260623T234820Z` | 0 publication candidates |

Current canonical weather:

| Metric | Value |
| --- | ---: |
| `weather.hourly_djf` rows | 4,355,003 |
| Distinct stations | 2,780 |
| Minimum dry-bulb F | -56.920 |
| Maximum dry-bulb F | 104.000 |

## Interpretation

- The pipeline now has explicit plant ECWT readiness gates.
- The plant ECWT table is populated for every plant, but the strict publication gate properly blocks all rows until coverage improves.
- The fastest path toward publication readiness is still more NOAA download/load coverage, followed by repeated coverage and ECWT refreshes.
