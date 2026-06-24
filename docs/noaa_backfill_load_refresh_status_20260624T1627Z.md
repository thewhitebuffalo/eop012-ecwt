# NOAA Backfill Load Refresh Status

Generated UTC: 2026-06-24T16:27Z

## Scope

This refresh covers NOAA backfill batches 60 through 64, loading the newly downloaded files, and refreshing station-year coverage plus provisional ECWT readiness outputs.

## Download And Cache Status

| Metric | Value |
| --- | ---: |
| Raw NOAA CSV files in cache | 28,308 |
| Raw NOAA `.part` files in cache | 0 |
| Raw NOAA cache size | 200 GB |
| Database size | 18 GB |
| Manifest `downloaded` rows | 28,308 |
| Manifest `missing` rows | 35,682 |
| Manifest `failed` rows | 10 |
| Manifest `planned` rows | 22,839 |
| Manifest `skipped` rows | 86,839 |

## Batch Results

| Batch | Downloaded | Missing On AWS | True Failures | Notes |
| ---: | ---: | ---: | ---: | --- |
| 60 | 267 | 733 | 0 | Clean split under corrected status semantics. |
| 61 | 463 | 537 | 0 | High-yield batch with 3.70 GB downloaded. |
| 62 | 265 | 735 | 0 | Clean split under corrected status semantics. |
| 63 | 367 | 633 | 0 | Clean split under corrected status semantics. |
| 64 | 405 | 595 | 0 | High-yield batch with 3.01 GB downloaded. |
| Total | 1,767 | 3,233 | 0 | Planned queue reduced by 5,000 rows. |

## Load Refresh

| Metric | Value |
| --- | ---: |
| New downloaded files selected | 1,767 |
| Loaded files | 1,767 |
| Failed files | 0 |
| Source bytes parsed | 14,324,908,274 |
| Raw rows seen | 33,232,502 |
| DJF rows seen | 8,259,760 |
| Rejected source-code rows | 3,517,606 |
| Valid DJF temperature rows | 4,454,207 |
| Invalid DJF temperature rows | 287,947 |
| Rejected plausibility rows | 0 |
| Duplicate station-hour observations | 2,910,868 |
| Canonical hourly rows added/staged | 1,543,339 |
| Total loaded canonical DJF hours by file audit | 43,875,893 |

## Coverage Refresh

Run ID: `station_year_djf_coverage_20260624T161255Z`

| Metric | Value |
| --- | ---: |
| Station-year coverage rows | 55,869 |
| Complete station-years | 12,095 |
| Partial station-years | 41,702 |
| Empty station-years | 2,072 |
| Valid DJF hours represented | 43,875,893 |
| Rejected source rows represented | 126,303,766 |

## Provisional ECWT Refresh

| Layer | Run ID | Key Counts |
| --- | --- | --- |
| Station ECWT | `station_ecwt_loaded_20260624T162020Z` | 4,043 provisional, 195 blocked; min ECWT F `-58.216`, max ECWT F `100.400` |
| Plant ECWT | `plant_ecwt_provisional_20260624T162525Z` | 16,104 provisional, 28 blocked; min plant ECWT F `-58.000`, max plant ECWT F `88.160` |
| Strict readiness | `plant_ecwt_readiness_20260624T162656Z` | 1,655 publication candidates, 14,449 low coverage, 28 blocked |
| Diagnostic readiness | `plant_ecwt_readiness_20260624T162719Z` | 7,733 candidates at 0.25 coverage threshold, 8,371 low coverage, 28 blocked |

## QA Notes

- Batch 60-64 had zero true download failures.
- The station-level maximum ECWT remains `100.400 F`; this comes from a one-hour provisional station result and is not publication-ready evidence by itself.
- Strict readiness decreased by `3` rows while diagnostic readiness increased by `86`; readiness is recalculated from the latest selected-station coverage denominator and can move slightly as station ECWT and selection inputs update.

## Net Movement Since Prior Status

Compared with `docs/noaa_backfill_load_refresh_status_20260624T1538Z`:

| Metric | Prior | Current | Change |
| --- | ---: | ---: | ---: |
| Raw NOAA CSV files | 26,541 | 28,308 | +1,767 |
| Manifest downloaded | 26,541 | 28,308 | +1,767 |
| Manifest missing | 32,449 | 35,682 | +3,233 |
| Manifest planned | 27,839 | 22,839 | -5,000 |
| Loaded canonical DJF hours | 42,332,554 | 43,875,893 | +1,543,339 |
| Complete station-years | 11,794 | 12,095 | +301 |
| Provisional station ECWT rows | 4,039 | 4,043 | +4 |
| Strict publication candidates | 1,658 | 1,655 | -3 |
| Diagnostic candidates | 7,647 | 7,733 | +86 |

## Reports Produced

- `docs/noaa_backfill_download_batch60_report.md`
- `docs/noaa_backfill_download_batch61_report.md`
- `docs/noaa_backfill_download_batch62_report.md`
- `docs/noaa_backfill_download_batch63_report.md`
- `docs/noaa_backfill_download_batch64_report.md`
- `docs/noaa_hourly_djf_load_20260624T160500Z_report.md`
- `docs/station_year_djf_coverage_20260624T161255Z_report.md`
- `docs/station_ecwt_loaded_20260624T162020Z_report.md`
- `docs/plant_ecwt_provisional_20260624T162525Z_report.md`
- `docs/plant_ecwt_readiness_20260624T162656Z_report.md`
- `docs/plant_ecwt_readiness_20260624T162719Z_report.md`

## Next Operational Step

Continue NOAA AWS backfill from batch 65. The remaining `22,839` planned rows run through batch 87.
