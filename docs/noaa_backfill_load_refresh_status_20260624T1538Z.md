# NOAA Backfill Load Refresh Status

Generated UTC: 2026-06-24T15:38Z

## Scope

This refresh covers NOAA backfill batches 55 through 59, retrying two transient batch 55 HTTP 503 responses, loading newly downloaded files, and refreshing station-year coverage plus provisional ECWT readiness outputs.

## Download And Cache Status

| Metric | Value |
| --- | ---: |
| Raw NOAA CSV files in cache | 26,541 |
| Raw NOAA `.part` files in cache | 0 |
| Raw NOAA cache size | 186 GB |
| Database size | 17 GB |
| Manifest `downloaded` rows | 26,541 |
| Manifest `missing` rows | 32,449 |
| Manifest `failed` rows | 10 |
| Manifest `planned` rows | 27,839 |
| Manifest `skipped` rows | 86,839 |

## Download Attempts

| Status | HTTP | Rows |
| --- | ---: | ---: |
| `downloaded` | 200 | 26,541 |
| `missing_on_aws` | 404 | 32,449 |
| `failed_http` | 500 | 1 |
| `failed_http` | 503 | 9 |
| `failed_exception` |  | 3 |

The attempt table preserves historical failed attempts. The two new batch 55 HTTP 503 attempts were retried and resolved as `missing_on_aws`; the manifest remains at `10` true failed rows.

## Batch Results

| Batch | Downloaded | Missing On AWS | True Failures | Notes |
| ---: | ---: | ---: | ---: | --- |
| 55 | 256 | 744 | 0 remaining in manifest | Original run had two HTTP 503 rows; both retried and resolved as `missing_on_aws`. |
| 56 | 209 | 791 | 0 | Clean split under corrected status semantics. |
| 57 | 223 | 777 | 0 | Clean split under corrected status semantics. |
| 58 | 46 | 954 | 0 | Mostly terminal missing-object evidence for 2000 station-year URLs. |
| 59 | 40 | 960 | 0 | Mostly terminal missing-object evidence for 2000 station-year URLs. |
| Total | 774 | 4,226 | 0 new remaining in manifest | Planned queue reduced by 5,000 rows. |

## Load Refresh

| Metric | Value |
| --- | ---: |
| New downloaded files selected | 774 |
| Loaded files | 774 |
| Failed files | 0 |
| Source bytes parsed | 3,624,645,341 |
| Raw rows seen | 8,540,604 |
| DJF rows seen | 2,154,259 |
| Rejected source-code rows | 92,063 |
| Valid DJF temperature rows | 1,466,728 |
| Invalid DJF temperature rows | 595,466 |
| Rejected plausibility rows | 2 |
| Duplicate station-hour observations | 267,710 |
| Canonical hourly rows added/staged | 1,199,018 |
| Total loaded canonical DJF hours by file audit | 42,332,554 |

## Coverage Refresh

Run ID: `station_year_djf_coverage_20260624T152609Z`

| Metric | Value |
| --- | ---: |
| Station-year coverage rows | 54,102 |
| Complete station-years | 11,794 |
| Partial station-years | 40,315 |
| Empty station-years | 1,993 |
| Valid DJF hours represented | 42,332,554 |
| Rejected source rows represented | 122,786,160 |

## Provisional ECWT Refresh

| Layer | Run ID | Key Counts |
| --- | --- | --- |
| Station ECWT | `station_ecwt_loaded_20260624T153216Z` | 4,039 provisional, 196 blocked; min ECWT F `-58.216`, max ECWT F `100.400` |
| Plant ECWT | `plant_ecwt_provisional_20260624T153607Z` | 16,104 provisional, 28 blocked; min plant ECWT F `-58.000`, max plant ECWT F `88.160` |
| Strict readiness | `plant_ecwt_readiness_20260624T153809Z` | 1,658 publication candidates, 14,446 low coverage, 28 blocked |
| Diagnostic readiness | `plant_ecwt_readiness_20260624T153826Z` | 7,647 candidates at 0.25 coverage threshold, 8,457 low coverage, 28 blocked |

## QA Notes

- The maximum station ECWT F is from station `727500-99999` with only `1` valid hour in the station ECWT run. It is retained in provisional station output but should not be treated as publication-ready evidence.
- The plant-level readiness gate still filters publication candidates by minimum valid hours and fixed-denominator coverage ratio.

## Net Movement Since Prior Status

Compared with `docs/noaa_backfill_load_refresh_status_20260624T1506Z`:

| Metric | Prior | Current | Change |
| --- | ---: | ---: | ---: |
| Raw NOAA CSV files | 25,767 | 26,541 | +774 |
| Manifest downloaded | 25,767 | 26,541 | +774 |
| Manifest missing | 28,223 | 32,449 | +4,226 |
| Manifest planned | 32,839 | 27,839 | -5,000 |
| Loaded canonical DJF hours | 41,133,536 | 42,332,554 | +1,199,018 |
| Complete station-years | 11,415 | 11,794 | +379 |
| Provisional station ECWT rows | 4,031 | 4,039 | +8 |
| Strict publication candidates | 1,463 | 1,658 | +195 |
| Diagnostic candidates | 7,522 | 7,647 | +125 |

## Reports Produced

- `docs/noaa_backfill_download_batch55_report.md`
- `docs/noaa_backfill_download_batch55_20260624T151301Z_report.md`
- `docs/noaa_backfill_download_batch56_report.md`
- `docs/noaa_backfill_download_batch57_report.md`
- `docs/noaa_backfill_download_batch58_report.md`
- `docs/noaa_backfill_download_batch59_report.md`
- `docs/noaa_hourly_djf_load_20260624T152227Z_report.md`
- `docs/station_year_djf_coverage_20260624T152609Z_report.md`
- `docs/station_ecwt_loaded_20260624T153216Z_report.md`
- `docs/plant_ecwt_provisional_20260624T153607Z_report.md`
- `docs/plant_ecwt_readiness_20260624T153809Z_report.md`
- `docs/plant_ecwt_readiness_20260624T153826Z_report.md`

## Next Operational Step

Continue NOAA AWS backfill from batch 60. The remaining `27,839` planned rows are now concentrated in older and lower-yield candidate station-years, so future batches may have high `missing_on_aws` ratios with fewer downloaded files per batch.
