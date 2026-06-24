# NOAA Backfill, Load, And ECWT Refresh Status

Generated UTC: 2026-06-24T09:56Z

Database: `eop012` on `127.0.0.1:5436`

## Summary

This cycle ran AWS backfill batch 33 in parallel with another inventory load, then loaded the new batch 33 downloads and refreshed coverage, station ECWT, corrected plant ECWT, and fixed-denominator plant readiness.

The fixed-denominator strict publication count increased from `139` to `234`. The relaxed diagnostic count increased from `4,250` to `4,492`.

| Metric | Value |
| --- | ---: |
| Plant ECWT rows | 16,132 |
| Strict publication candidates | 234 |
| Strict provisional low coverage | 15,870 |
| Strict blocked | 28 |
| Diagnostic publication candidates at 0.25 coverage | 4,492 |
| Diagnostic provisional low coverage at 0.25 coverage | 11,612 |
| Diagnostic blocked | 28 |

## NOAA Progress

Completed AWS backfill batch:

| Batch | Run ID | Downloaded | HTTP failures | Bytes | Elapsed seconds |
| ---: | --- | ---: | ---: | ---: | ---: |
| 33 | `noaa_backfill_download_batch33_20260624T093704Z` | 381 | 619 | 2,671,468,058 | 318.528 |

Completed NOAA loads:

| Run ID | Source | Files | Canonical DJF Hours | Invalid Temp Rows | Rejected SOURCE Rows | Rejected Plausibility Rows | Duplicate Hour Count |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `noaa_hourly_djf_load_20260624T093703Z` | inventory | 1,000 | 1,254,716 | 116,298 | 1,439,262 | 0 | 3,076,990 |
| `noaa_hourly_djf_load_20260624T094258Z` | downloaded | 381 | 460,823 | 165,089 | 416,773 | 179 | 467,760 |

Plausibility rejection detail:

| Run ID | Station | Year | Rejected Plausibility Rows | Source File ID |
| --- | --- | ---: | ---: | --- |
| `noaa_hourly_djf_load_20260624T094258Z` | `720319-99999` | 2005 | 179 | `noaa_global_hourly_csv_2005_72031999999_17b381c961ec6e4e` |

Current NOAA/cache status:

| Metric | Value |
| --- | ---: |
| AWS CSV files | 19,270 |
| AWS `.part` files | 0 |
| AWS cache disk usage | 149 GB |
| Manifest downloaded rows | 19,270 |
| Manifest failed rows | 13,730 |
| Manifest planned rows | 53,839 |
| Manifest skipped rows | 86,839 |

## Refreshed Result Runs

| Layer | Run ID | Rows / Result |
| --- | --- | ---: |
| Station-year coverage | `station_year_djf_coverage_20260624T094505Z` | 45,270 rows; 7,814 complete, 36,456 partial, 1,000 empty |
| Station ECWT | `station_ecwt_loaded_20260624T095031Z` | 3,437 provisional, 92 blocked |
| Plant ECWT | `plant_ecwt_provisional_20260624T095247Z` | 16,104 provisional, 28 blocked |
| Strict plant readiness | `plant_ecwt_readiness_20260624T095424Z` | 234 publication candidates |
| Diagnostic plant readiness | `plant_ecwt_readiness_20260624T095435Z` | 4,492 diagnostic candidates |

Current canonical weather:

| Metric | Value |
| --- | ---: |
| `weather.hourly_djf` rows | 30,201,850 |
| Distinct stations | 3,437 |
| Minimum dry-bulb F | -61.600 |
| Maximum dry-bulb F | 104.000 |
| `SHEF` rows below `-50 C` | 0 |
| Database size | 12 GB |

## Stability Checks

Compared with the previous corrected plant run `plant_ecwt_provisional_20260624T092912Z`:

| Check | Plants |
| --- | ---: |
| Selected station unchanged | 15,850 |
| Selected station changed | 282 |

Compared with previous strict readiness `plant_ecwt_readiness_20260624T093031Z`:

| Transition | Plants |
| --- | ---: |
| Strict candidate remained candidate | 135 |
| Strict candidate became low coverage | 4 |
| Strict low coverage became candidate | 99 |
| Strict low coverage remained low coverage | 15,866 |
| Strict blocked remained blocked | 28 |

Compared with previous diagnostic readiness `plant_ecwt_readiness_20260624T093040Z`:

| Transition | Plants |
| --- | ---: |
| Diagnostic candidate remained candidate | 4,228 |
| Diagnostic candidate became low coverage | 22 |
| Diagnostic low coverage became candidate | 264 |
| Diagnostic low coverage remained low coverage | 11,590 |
| Diagnostic blocked remained blocked | 28 |

## Interpretation

- Batch 33 added `381` NOAA CSVs and there are no `.part` files left in the cache.
- The hardened `SHEF < -50 C` plausibility rule held through this cycle.
- Fixed-denominator strict readiness improved from `139` to `234` publication candidates, despite `4` prior candidates falling back to low coverage after station selection changed.
- Fixed-denominator diagnostic readiness improved from `4,250` to `4,492` candidates, despite `22` prior diagnostic candidates falling back to low coverage.
- One downloaded 2005 station-year contributed `179` physically implausible rows rejected by the canonical loader.
- Station selection changed for `282` plants, so station-selection churn remains a monitored QA signal while backfill coverage is still incomplete.
- The immediate next step is to continue the parallel download/load/refresh cycle with batch 34.
