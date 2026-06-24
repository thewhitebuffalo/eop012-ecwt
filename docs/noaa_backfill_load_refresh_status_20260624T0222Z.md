# NOAA Backfill, Load, And ECWT Refresh Status

Generated UTC: 2026-06-24T02:22Z

Database: `eop012` on `127.0.0.1:5436`

## Summary

This cycle ran AWS backfill batch 16 in parallel with another inventory load, then loaded downloaded files and refreshed coverage, station ECWT, plant ECWT, and plant readiness.

The NOAA loader report path was also hardened before this cycle: reports now avoid exact full-table `weather.hourly_djf` scans by default, using planner estimates for total rows and file-audit sums for run rows. The real batch 16 loader reports confirmed the faster path.

Strict publication candidates changed from `367` to `298` because provisional station selection shifted as newly loaded station-year coverage changed. The dataset is still not publication-complete because most plants remain below the strict coverage threshold.

| Metric | Value |
| --- | ---: |
| Plant ECWT rows | 16,132 |
| Strict publication candidates | 298 |
| Strict provisional low coverage | 15,806 |
| Strict blocked | 28 |
| Diagnostic publication candidates at 0.25 coverage | 13,723 |
| Diagnostic provisional low coverage at 0.25 coverage | 2,381 |
| Diagnostic blocked | 28 |

## NOAA Progress

Completed AWS backfill batch:

| Batch | Run ID | Downloaded | HTTP failures | Bytes | Elapsed seconds |
| ---: | --- | ---: | ---: | ---: | ---: |
| 16 | `noaa_backfill_download_batch16_20260624T020025Z` | 608 | 392 | 5,875,770,746 | 520.404 |

Completed NOAA loads:

| Run ID | Source | Files | Canonical DJF Hours | Invalid Temp Rows | Rejected SOURCE Rows | Rejected Plausibility Rows | Duplicate Hour Count |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `noaa_hourly_djf_load_20260624T020025Z` | inventory | 1,000 | 819,952 | 163,829 | 2,578,646 | 10 | 2,632,280 |
| `noaa_hourly_djf_load_20260624T020937Z` | downloaded | 1,000 | 434,394 | 87,830 | 3,204,096 | 0 | 285,004 |

Current NOAA/cache status:

| Metric | Value |
| --- | ---: |
| AWS CSV files | 10,228 |
| AWS `.part` files | 0 |
| AWS cache disk usage | 80 GB |
| Manifest downloaded rows | 10,228 |
| Manifest failed rows | 5,772 |
| Manifest planned rows | 70,839 |
| Manifest skipped rows | 86,839 |

## Refreshed Result Runs

| Layer | Run ID | Rows / Result |
| --- | --- | ---: |
| Station-year coverage | `station_year_djf_coverage_20260624T021300Z` | 19,000 rows; 2,472 complete, 16,076 partial, 452 empty |
| Station ECWT | `station_ecwt_loaded_20260624T021645Z` | 3,058 provisional, 69 blocked |
| Plant ECWT | `plant_ecwt_provisional_20260624T022025Z` | 16,104 provisional, 28 blocked |
| Strict plant readiness | `plant_ecwt_readiness_20260624T022100Z` | 298 publication candidates |
| Diagnostic plant readiness | `plant_ecwt_readiness_20260624T022112Z` | 13,723 diagnostic candidates |

Current canonical weather:

| Metric | Value |
| --- | ---: |
| `weather.hourly_djf` rows | 11,922,371 |
| Distinct stations | 3,058 |
| Minimum dry-bulb F | -68.440 |
| Maximum dry-bulb F | 104.000 |
| Database size | 5,095 MB |

## Interpretation

- The loader optimization worked: batch 16 loader reports completed without multi-minute exact table-count waits.
- Strict readiness is not monotonic under the current provisional station-selection algorithm; adding station data can change selected stations and move plants across readiness thresholds.
- The dominant blocker remains weather coverage: `15,806` plants are still below the strict coverage threshold.
- The relaxed diagnostic gate rose from `13,679` to `13,723` candidates.
- The immediate next step remains another parallel download/load/refresh cycle, while tracking whether station-selection volatility needs its own stabilization rule before publication.
