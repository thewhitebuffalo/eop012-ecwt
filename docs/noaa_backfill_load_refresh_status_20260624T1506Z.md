# NOAA Backfill Load Refresh Status

Generated UTC: 2026-06-24T15:06Z

## Scope

This refresh covers NOAA backfill batches 52 through 54, the retry of one transient batch 53 DNS failure, loading the newly downloaded files, and refreshing coverage plus provisional ECWT readiness outputs.

## Download And Cache Status

| Metric | Value |
| --- | ---: |
| Raw NOAA CSV files in cache | 25,767 |
| Raw NOAA `.part` files in cache | 0 |
| Raw NOAA cache size | 183 GB |
| Database size | 17 GB |
| Manifest `downloaded` rows | 25,767 |
| Manifest `missing` rows | 28,223 |
| Manifest `failed` rows | 10 |
| Manifest `planned` rows | 32,839 |
| Manifest `skipped` rows | 86,839 |

## Download Attempts

| Status | HTTP | Rows |
| --- | ---: | ---: |
| `downloaded` | 200 | 25,767 |
| `missing_on_aws` | 404 | 28,223 |
| `failed_http` | 500 | 1 |
| `failed_http` | 503 | 7 |
| `failed_exception` |  | 3 |

The attempt table still preserves historical failed attempts. One batch 53 `failed_exception` row was retried and resolved as `missing_on_aws`; the manifest has only `10` true failed rows remaining.

## Batch Results

| Batch | Downloaded | Missing On AWS | True Failures | Notes |
| ---: | ---: | ---: | ---: | --- |
| 52 | 237 | 763 | 0 | Clean split under corrected status semantics. |
| 53 | 273 | 726 | 1 | One DNS exception retried in a follow-up one-row run and resolved as `missing_on_aws`. |
| 54 | 260 | 740 | 0 | Clean split under corrected status semantics. |
| Total | 770 | 2,230 | 0 remaining in manifest | Batch 53 retry removed the transient row from the manifest failed set. |

## Load Refresh

| Metric | Value |
| --- | ---: |
| New downloaded files selected | 770 |
| Loaded files | 770 |
| Failed files | 0 |
| Canonical hourly rows added/staged | 1,182,746 |
| Invalid temp rows for this run | 642,551 |
| Rejected source rows for this run | 0 |
| Rejected plausibility rows for this run | 0 |
| Duplicate station-hour observations | 219,241 |
| Total loaded canonical DJF hours by file audit | 41,133,536 |

## Coverage Refresh

Run ID: `station_year_djf_coverage_20260624T145255Z`

| Metric | Value |
| --- | ---: |
| Station-year coverage rows | 53,328 |
| Complete station-years | 11,415 |
| Partial station-years | 40,017 |
| Empty station-years | 1,896 |
| Valid DJF hours represented | 41,133,536 |

## Provisional ECWT Refresh

| Layer | Run ID | Key Counts |
| --- | --- | --- |
| Station ECWT | `station_ecwt_loaded_20260624T145908Z` | 4,031 provisional, 198 blocked; min ECWT F `-58.216`, max ECWT F `88.160` |
| Plant ECWT | `plant_ecwt_provisional_20260624T150405Z` | 16,104 provisional, 28 blocked; min plant ECWT F `-58.000`, max plant ECWT F `88.160` |
| Strict readiness | `plant_ecwt_readiness_20260624T150549Z` | 1,463 publication candidates, 14,641 low coverage, 28 blocked |
| Diagnostic readiness | `plant_ecwt_readiness_20260624T150601Z` | 7,522 candidates at 0.25 coverage threshold, 8,582 low coverage, 28 blocked |

## Net Movement Since Prior Status

Compared with `docs/noaa_backfill_load_refresh_status_20260624T1436Z`:

| Metric | Prior | Current | Change |
| --- | ---: | ---: | ---: |
| Raw NOAA CSV files | 24,997 | 25,767 | +770 |
| Manifest downloaded | 24,997 | 25,767 | +770 |
| Manifest missing | 25,993 | 28,223 | +2,230 |
| Manifest planned | 35,839 | 32,839 | -3,000 |
| Loaded canonical DJF hours | 39,950,790 | 41,133,536 | +1,182,746 |
| Complete station-years | 11,005 | 11,415 | +410 |
| Provisional station ECWT rows | 4,020 | 4,031 | +11 |
| Strict publication candidates | 958 | 1,463 | +505 |
| Diagnostic candidates | 7,212 | 7,522 | +310 |

## Reports Produced

- `docs/noaa_backfill_download_batch52_report.md`
- `docs/noaa_backfill_download_batch53_report.md`
- `docs/noaa_backfill_download_batch53_retry_20260624T144415_report.md`
- `docs/noaa_backfill_download_batch54_report.md`
- `docs/noaa_hourly_djf_load_20260624T144934Z_report.md`
- `docs/station_year_djf_coverage_20260624T145255Z_report.md`
- `docs/station_ecwt_loaded_20260624T145908Z_report.md`
- `docs/plant_ecwt_provisional_20260624T150405Z_report.md`
- `docs/plant_ecwt_readiness_20260624T150549Z_report.md`
- `docs/plant_ecwt_readiness_20260624T150601Z_report.md`

## Next Operational Step

Continue NOAA AWS backfill from batch 55. The remaining `32,839` planned rows should continue to split into downloaded files, `missing_on_aws`, or a small set of true retryable failures.
