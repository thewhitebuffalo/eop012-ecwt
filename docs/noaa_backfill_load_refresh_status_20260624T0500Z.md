# NOAA Backfill, Load, And ECWT Refresh Status

Generated UTC: 2026-06-24T05:00Z

Database: `eop012` on `127.0.0.1:5436`

## Summary

This cycle ran AWS backfill batch 22 in parallel with another inventory load, then loaded the new batch 22 downloads and refreshed coverage, station ECWT, corrected plant ECWT, and plant readiness.

Under the corrected rank/distance-first station-selection rule, selected representative stations stayed stable for `16,131` of `16,132` plants. During this cycle, the readiness builder was also hardened to use fixed selected-station active-period DJF expected hours for `2000-2025`, rather than using only station-year files that happen to be loaded already.

The fixed-denominator readiness counts are much lower than the superseded loaded-denominator counts. This is expected and more defensible: loaded-file denominators were overstating readiness while the NOAA backfill is incomplete.

| Metric | Value |
| --- | ---: |
| Plant ECWT rows | 16,132 |
| Strict publication candidates | 44 |
| Strict provisional low coverage | 16,060 |
| Strict blocked | 28 |
| Diagnostic publication candidates at 0.25 coverage | 2,170 |
| Diagnostic provisional low coverage at 0.25 coverage | 13,934 |
| Diagnostic blocked | 28 |

## NOAA Progress

Completed AWS backfill batch:

| Batch | Run ID | Downloaded | HTTP failures | Bytes | Elapsed seconds |
| ---: | --- | ---: | ---: | ---: | ---: |
| 22 | `noaa_backfill_download_batch22_20260624T044005Z` | 576 | 424 | 4,129,130,364 | 279.585 |

Completed NOAA loads:

| Run ID | Source | Files | Canonical DJF Hours | Invalid Temp Rows | Rejected SOURCE Rows | Rejected Plausibility Rows | Duplicate Hour Count |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `noaa_hourly_djf_load_20260624T044005Z` | inventory | 1,000 | 852,654 | 165,454 | 2,451,443 | 1 | 2,752,031 |
| `noaa_hourly_djf_load_20260624T044556Z` | downloaded | 576 | 539,699 | 83,392 | 977,114 | 0 | 841,320 |

Plausibility rejection detail:

| Run ID | Station | Year | Rejected Plausibility Rows | Source File ID |
| --- | --- | ---: | ---: | --- |
| `noaa_hourly_djf_load_20260624T044005Z` | `911620-22501` | 2017 | 1 | `noaa_global_hourly_local_raw_inventory_3e447b31e3e36679` |

Current NOAA/cache status:

| Metric | Value |
| --- | ---: |
| AWS CSV files | 13,858 |
| AWS `.part` files | 0 |
| AWS cache disk usage | 108 GB |
| Manifest downloaded rows | 13,858 |
| Manifest failed rows | 8,142 |
| Manifest planned rows | 64,839 |
| Manifest skipped rows | 86,839 |

## Refreshed Result Runs

| Layer | Run ID | Rows / Result |
| --- | --- | ---: |
| Station-year coverage | `station_year_djf_coverage_20260624T044835Z` | 28,858 rows; 4,384 complete, 23,781 partial, 693 empty |
| Station ECWT | `station_ecwt_loaded_20260624T045251Z` | 3,093 provisional, 78 blocked |
| Plant ECWT | `plant_ecwt_provisional_20260624T045441Z` | 16,104 provisional, 28 blocked |
| Strict plant readiness | `plant_ecwt_readiness_20260624T050435Z` | 44 publication candidates |
| Diagnostic plant readiness | `plant_ecwt_readiness_20260624T050443Z` | 2,170 diagnostic candidates |

Current canonical weather:

| Metric | Value |
| --- | ---: |
| `weather.hourly_djf` rows | 18,362,666 |
| Distinct stations | 3,093 |
| Minimum dry-bulb F | -61.600 |
| Maximum dry-bulb F | 104.000 |
| `SHEF` rows below `-50 C` | 0 |
| Database size | 7,759 MB |

## Stability Checks

Compared with the previous corrected plant run `plant_ecwt_provisional_20260624T043636Z`:

| Check | Plants |
| --- | ---: |
| Selected station unchanged | 16,131 |
| Selected station changed | 1 |

Impact of replacing the superseded loaded-file readiness denominator with the fixed selected-station active-period denominator:

| Transition | Plants |
| --- | ---: |
| Strict candidate remained candidate | 1 |
| Strict candidate became low coverage | 392 |
| Strict low coverage became candidate | 43 |
| Strict low coverage remained low coverage | 15,668 |
| Strict blocked remained blocked | 28 |
| Diagnostic candidate remained candidate | 2,170 |
| Diagnostic candidate became low coverage | 1,981 |
| Diagnostic low coverage remained low coverage | 11,953 |
| Diagnostic blocked remained blocked | 28 |

## Interpretation

- Batch 22 added `576` NOAA CSVs and there are no `.part` files left in the cache.
- The hardened `SHEF < -50 C` plausibility rule held through this cycle.
- The corrected station selector was stable for nearly the full plant universe.
- Fixed-denominator strict readiness is `44` publication candidates.
- Fixed-denominator diagnostic readiness is `2,170` candidates at the relaxed `0.25` coverage threshold.
- The immediate next step is to continue the parallel download/load/refresh cycle and track readiness only against the fixed-denominator runs.
