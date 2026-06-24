# NOAA Backfill, Load, And ECWT Refresh Status

Generated UTC: 2026-06-24T00:12Z

Database: `eop012` on `127.0.0.1:5436`

## Summary

This cycle continued the parallel NOAA path: AWS backfill batch 11 ran while another inventory load populated canonical DJF weather. After batch 11 completed, downloaded files were loaded and the coverage, station ECWT, plant ECWT, and plant readiness layers were refreshed.

Strict publication readiness is still blocked by coverage, not by plant-universe construction.

| Metric | Value |
| --- | ---: |
| Plant ECWT rows | 16,132 |
| Strict publication candidates | 0 |
| Strict provisional low coverage | 16,104 |
| Strict blocked | 28 |
| Diagnostic publication candidates at 0.25 coverage | 12,770 |
| Diagnostic provisional low coverage at 0.25 coverage | 3,334 |
| Diagnostic blocked | 28 |

## NOAA Progress

Completed AWS backfill batch:

| Batch | Run ID | Downloaded | HTTP failures | Bytes |
| ---: | --- | ---: | ---: | ---: |
| 11 | `noaa_backfill_download_batch11_20260623T235525Z` | 626 | 374 | 6,139,006,076 |

Completed NOAA loads:

| Run ID | Source | Files | Canonical DJF Hours | Invalid Temp Rows | Rejected SOURCE Rows | Rejected Plausibility Rows | Duplicate Hour Count |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `noaa_hourly_djf_load_20260623T235524Z` | inventory | 1,000 | 312,612 | 71,791 | 3,470,874 | 0 | 310,943 |
| `noaa_hourly_djf_load_20260624T000305Z` | downloaded | 1,000 | 256,176 | 85,272 | 3,419,901 | 0 | 129,525 |

Current NOAA/cache status:

| Metric | Value |
| --- | ---: |
| AWS CSV files | 7,077 |
| AWS `.part` files | 0 |
| AWS cache disk usage | 53 GB |
| Manifest downloaded rows | 7,077 |
| Manifest failed rows | 3,923 |
| Manifest planned rows | 75,839 |
| Manifest skipped rows | 86,839 |

## Refreshed Result Runs

| Layer | Run ID | Rows / Result |
| --- | --- | ---: |
| Station-year coverage | `station_year_djf_coverage_20260624T000708Z` | 9,000 rows; 679 complete, 8,123 partial, 198 empty |
| Station ECWT | `station_ecwt_loaded_20260624T000839Z` | 2,781 provisional, 70 blocked |
| Plant ECWT | `plant_ecwt_provisional_20260624T001040Z` | 16,104 provisional, 28 blocked |
| Strict plant readiness | `plant_ecwt_readiness_20260624T001115Z` | 0 publication candidates |
| Diagnostic plant readiness | `plant_ecwt_readiness_20260624T001127Z` | 12,770 diagnostic candidates |

Current canonical weather:

| Metric | Value |
| --- | ---: |
| `weather.hourly_djf` rows | 4,923,791 |
| Distinct stations | 2,781 |
| Minimum dry-bulb F | -56.920 |
| Maximum dry-bulb F | 104.000 |
| Database size | 2,447 MB |

## Interpretation

- The plant universe and provisional plant ECWT table continue to cover every plant.
- The strict publication gate correctly returns zero candidates because coverage remains below the `0.95` threshold.
- The relaxed diagnostic gate improved from `10,292` to `12,770` candidate plants after this cycle, so the download/load path is materially improving coverage.
- The immediate next step is batch 12 plus another inventory/downloaded load cycle, followed by the same coverage and ECWT refresh.
