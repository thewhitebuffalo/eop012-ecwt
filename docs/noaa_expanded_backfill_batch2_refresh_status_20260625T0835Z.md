# NOAA Expanded Backfill Batch 2 Refresh Status

Generated UTC: 2026-06-25T08:35Z

## Scope

This cycle consumed batch 2 from the expanded top-100 NOAA backfill manifest `noaa_backfill_manifest_20260625T070923Z`, loaded the downloaded files into canonical DJF weather tables, and rebuilt coverage, station ECWT, fixed-period plant ECWT, fixed-period readiness, and active-window plant ECWT.

## Inputs

| Input | Run ID |
| --- | --- |
| Expanded station candidates | `noaa_station_candidates_20260625T065445Z` |
| Expanded raw-file inventory | `noaa_raw_file_inventory_20260625T070816Z` |
| Expanded backfill manifest | `noaa_backfill_manifest_20260625T070923Z` |
| Prior refresh status | `docs/noaa_expanded_backfill_batch1_refresh_status_20260625T0750Z.md` |

## Batch 2 Download

| Metric | Count |
| --- | ---: |
| Attempt rows | 1,000 |
| Downloaded | 981 |
| Missing on AWS | 19 |
| Retryable HTTP failures | 0 |
| Local exceptions | 0 |
| Downloaded bytes | 3,741,422,527 |

After batch 2, the expanded manifest has 1,975 downloaded rows, 25 missing rows, and 9,432 planned rows remaining.

## Canonical Load

| Metric | Count |
| --- | ---: |
| Files loaded | 981 |
| Failed files | 0 |
| Source bytes parsed | 3,741,422,527 |
| Raw rows seen | 10,462,537 |
| DJF rows seen | 2,593,597 |
| Canonical hourly rows staged | 1,490,159 |
| Invalid TMP rows | 107,891 |
| Rejected source-code rows | 246,958 |
| Rejected plausibility rows | 17 |
| Duplicate station-hour observations | 748,572 |

## Refreshed Results

| Layer | Prior Run | New Run | Movement |
| --- | --- | --- | --- |
| Station-year coverage | `station_year_djf_coverage_20260625T071904Z` | `station_year_djf_coverage_20260625T080126Z` | complete rows 14,479 to 14,791; valid hours 51,702,398 to 53,192,557 |
| Station ECWT | `station_ecwt_loaded_20260625T073259Z` | `station_ecwt_loaded_20260625T081200Z` | provisional rows 4,499 to 4,525 |
| Fixed-period plant ECWT | `plant_ecwt_provisional_fixed_period_20260625T074453Z` | `plant_ecwt_provisional_fixed_period_20260625T082342Z` | provisional rows unchanged at 1,346 |
| Fixed-period readiness | `plant_ecwt_readiness_fixed_period_20260625T074529Z` | `plant_ecwt_readiness_fixed_period_20260625T082916Z` | publication candidates unchanged at 1,346 |
| Active-window plant ECWT | `plant_ecwt_provisional_20260625T074547Z` | `plant_ecwt_provisional_20260625T082931Z` | provisional rows unchanged at 16,104 |

## Interpretation

- Batch 2 was operationally successful: it had no retryable download failures and no load failures.
- The downloaded files again improved lower layers: complete station-years increased by 312 and provisional station ECWT rows increased by 26.
- The fixed-period plant gate still did not move. This is expected while the backfill is concentrated in 2020-2025 rows; the strict gate requires candidate stations to satisfy the 2000-2025 fixed-period coverage rule with at least 20 loaded station-years.
- The broad active-window plant ECWT layer still provides provisional values for all 16,104 plants with coordinates; 28 plants remain blocked because they lack usable coordinates.
- Runtime is now the main operational blocker for repeated full-refresh loops. Coverage, station ECWT, fixed-period plant ECWT, and active-window plant ECWT all required broad scans or top-100 candidate scoring. Batch 3 should wait for performance hardening unless an immediate long-running refresh is acceptable.

## Reports Produced

- `docs/noaa_backfill_download_batch2_20260625T075043Z_report.md`
- `docs/noaa_hourly_djf_load_20260625T075706Z_report.md`
- `docs/station_year_djf_coverage_20260625T080126Z_report.md`
- `docs/station_ecwt_loaded_20260625T081200Z_report.md`
- `docs/plant_ecwt_provisional_fixed_period_20260625T082342Z_report.md`
- `docs/plant_ecwt_readiness_fixed_period_20260625T082916Z_report.md`
- `docs/plant_ecwt_provisional_20260625T082931Z_report.md`

## Next Operational Step

Add performance hardening before the next full loop: materialize or incrementally refresh station-year DJF coverage, station ECWT inputs, and plant candidate scoring so batches 3-12 can be processed without repeated full-table and full-candidate rescans. After that, continue with batch 3 of `noaa_backfill_manifest_20260625T070923Z`.
