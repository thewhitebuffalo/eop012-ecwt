# NOAA Expanded Backfill Batch 1 Refresh Status

Generated UTC: 2026-06-25T07:50Z

## Scope

This cycle consumed batch 1 from the expanded top-100 NOAA backfill manifest `noaa_backfill_manifest_20260625T070923Z`, loaded the downloaded files into canonical DJF weather tables, and rebuilt coverage, station ECWT, fixed-period plant ECWT, fixed-period readiness, and active-window plant ECWT.

## Inputs

| Input | Run ID |
| --- | --- |
| Expanded station candidates | `noaa_station_candidates_20260625T065445Z` |
| Expanded raw-file inventory | `noaa_raw_file_inventory_20260625T070816Z` |
| Expanded backfill manifest | `noaa_backfill_manifest_20260625T070923Z` |

## Batch 1 Download

| Metric | Count |
| --- | ---: |
| Attempt rows | 1,000 |
| Downloaded | 994 |
| Missing on AWS | 6 |
| Retryable HTTP failures | 0 |
| Local exceptions | 0 |
| Downloaded bytes | 3,285,981,118 |

After batch 1, the expanded manifest has 994 downloaded rows, 6 missing rows, and 10,432 planned rows remaining.

## Canonical Load

| Metric | Count |
| --- | ---: |
| Files loaded | 994 |
| Failed files | 0 |
| Source bytes parsed | 3,285,981,118 |
| Raw rows seen | 9,153,300 |
| DJF rows seen | 2,330,453 |
| Canonical hourly rows staged | 1,356,051 |
| Invalid TMP rows | 94,473 |
| Rejected source-code rows | 168,583 |
| Duplicate station-hour observations | 711,346 |

## Refreshed Results

| Layer | Prior Run | New Run | Movement |
| --- | --- | --- | --- |
| Station-year coverage | `station_year_djf_coverage_20260625T035921Z` | `station_year_djf_coverage_20260625T071904Z` | complete rows 14,161 to 14,479 |
| Station ECWT | `station_ecwt_loaded_20260625T042423Z` | `station_ecwt_loaded_20260625T073259Z` | provisional rows 4,057 to 4,499 |
| Fixed-period plant ECWT | `plant_ecwt_provisional_fixed_period_20260625T070144Z` | `plant_ecwt_provisional_fixed_period_20260625T074453Z` | provisional rows unchanged at 1,346 |
| Fixed-period readiness | `plant_ecwt_readiness_fixed_period_20260625T070613Z` | `plant_ecwt_readiness_fixed_period_20260625T074529Z` | publication candidates unchanged at 1,346 |
| Active-window plant ECWT | `plant_ecwt_provisional_20260625T070228Z` | `plant_ecwt_provisional_20260625T074547Z` | provisional rows unchanged at 16,104 |

## Interpretation

- Batch 1 was operationally successful: it had no retryable download failures and no load failures.
- The downloaded files materially improved lower layers: complete station-years increased by 318 and provisional station ECWT rows increased by 442.
- The strict fixed-period plant gate did not move because batch 1 was concentrated in recent years. The fixed-period gate requires candidate stations to satisfy the 2000-2025 coverage rule with at least 20 loaded years, so adding recent station-years alone may not promote plants immediately.
- The broad active-window plant ECWT layer still provides provisional values for all 16,104 plants with coordinates; 28 plants remain blocked because they lack usable coordinates.
- Coverage and station ECWT full-refresh steps are now the runtime bottleneck. The coverage rebuild and station ECWT rebuild both required broad scans over the canonical DJF table.

## Reports Produced

- `docs/noaa_backfill_download_batch1_20260625T071000Z_report.md`
- `docs/noaa_hourly_djf_load_20260625T071605Z_report.md`
- `docs/station_year_djf_coverage_20260625T071904Z_report.md`
- `docs/station_ecwt_loaded_20260625T073259Z_report.md`
- `docs/plant_ecwt_provisional_fixed_period_20260625T074453Z_report.md`
- `docs/plant_ecwt_readiness_fixed_period_20260625T074529Z_report.md`
- `docs/plant_ecwt_provisional_20260625T074547Z_report.md`

## Next Operational Step

Continue with batch 2 of `noaa_backfill_manifest_20260625T070923Z`, then load only newly downloaded files and refresh the same coverage and ECWT layers. In parallel, add a performance hardening task for incremental station-year coverage and station ECWT refreshes, because full-table rebuilds are now I/O-bound.
