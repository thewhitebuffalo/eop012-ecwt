# NOAA Backfill Load Refresh Status

Generated UTC: 2026-06-24T14:36Z

## Scope

This refresh covered the NOAA HTTP 404 status hardening, batch 50/51 backfill outcomes, loading newly downloaded NOAA Global Hourly CSV files into `weather.hourly_djf`, and rebuilding the provisional ECWT result tables.

## Key Change

NOAA HTTP 404 outcomes are no longer treated as generic download failures. They are now stored as:

- `weather.noaa_raw_download_attempt.download_status = 'missing_on_aws'`
- `weather.noaa_raw_backfill_manifest.manifest_status = 'missing'`

Only non-404 HTTP outcomes and local exceptions remain true failed attempts. After reclassification, the database has `25,993` NOAA-missing objects and only `10` true failed manifest rows.

## Download And Cache Status

| Metric | Value |
| --- | ---: |
| Raw NOAA CSV files in cache | 24,997 |
| Raw NOAA `.part` files in cache | 0 |
| Raw NOAA cache size | 179 GB |
| Database size | 16 GB |
| Manifest `downloaded` rows | 24,997 |
| Manifest `missing` rows | 25,993 |
| Manifest `failed` rows | 10 |
| Manifest `planned` rows | 35,839 |
| Manifest `skipped` rows | 86,839 |

## Download Attempts

| Status | HTTP | Rows |
| --- | ---: | ---: |
| `downloaded` | 200 | 24,997 |
| `missing_on_aws` | 404 | 25,993 |
| `failed_http` | 500 | 1 |
| `failed_http` | 503 | 7 |
| `failed_exception` |  | 2 |

Batch 51 validated the new status model: `267` downloaded, `733` `missing_on_aws`, and zero true failures.

## Load Refresh

| Metric | Value |
| --- | ---: |
| New downloaded files selected | 553 |
| Loaded files | 553 |
| Failed files | 0 |
| Source bytes parsed | 2,641,699,100 |
| Raw rows seen | 6,312,872 |
| DJF rows seen | 1,585,435 |
| Valid DJF temperature rows | 1,014,376 |
| Invalid DJF temperature rows | 571,057 |
| Rejected plausibility rows | 2 |
| Duplicate station-hour observations | 166,034 |
| Canonical hourly rows added/staged | 848,342 |
| Total loaded canonical DJF hours by file audit | 39,950,790 |

## Coverage Refresh

Run ID: `station_year_djf_coverage_20260624T141927Z`

| Metric | Value |
| --- | ---: |
| Station-year coverage rows | 52,558 |
| Complete station-years | 11,005 |
| Partial station-years | 39,764 |
| Empty station-years | 1,789 |
| Valid DJF hours represented | 39,950,790 |

## Provisional ECWT Refresh

| Layer | Run ID | Key Counts |
| --- | --- | --- |
| Station ECWT | `station_ecwt_loaded_20260624T143054Z` | 4,020 provisional, 190 blocked; min ECWT F `-58.216`, max ECWT F `88.160` |
| Plant ECWT | `plant_ecwt_provisional_20260624T143507Z` | 16,104 provisional, 28 blocked; min plant ECWT F `-58.000`, max plant ECWT F `88.160` |
| Strict readiness | `plant_ecwt_readiness_20260624T143552Z` | 958 publication candidates, 15,146 low coverage, 28 blocked |
| Diagnostic readiness | `plant_ecwt_readiness_20260624T143603Z` | 7,212 candidates at 0.25 coverage threshold, 8,892 low coverage, 28 blocked |

## Net Movement Since Prior Published Status

Compared with `docs/noaa_backfill_load_refresh_status_20260624T1350Z`:

| Metric | Prior | Current | Change |
| --- | ---: | ---: | ---: |
| Raw NOAA CSV files | 24,444 | 24,997 | +553 |
| Manifest downloaded | 24,444 | 24,997 | +553 |
| Manifest planned | 37,839 | 35,839 | -2,000 |
| Complete station-years | 10,703 | 11,005 | +302 |
| Provisional station ECWT rows | 4,015 | 4,020 | +5 |
| Strict publication candidates | 903 | 958 | +55 |
| Diagnostic candidates | 7,198 | 7,212 | +14 |

## Reports Produced

- `docs/noaa_404_reclassification_report.md`
- `docs/noaa_backfill_download_batch50_report.md`
- `docs/noaa_backfill_download_batch51_report.md`
- `docs/noaa_hourly_djf_load_20260624T141634Z_report.md`
- `docs/station_year_djf_coverage_20260624T141927Z_report.md`
- `docs/station_ecwt_loaded_20260624T143054Z_report.md`
- `docs/plant_ecwt_provisional_20260624T143507Z_report.md`
- `docs/plant_ecwt_readiness_20260624T143552Z_report.md`
- `docs/plant_ecwt_readiness_20260624T143603Z_report.md`

## Next Operational Step

Continue NOAA AWS backfill from batch 52. The remaining `35,839` planned manifest rows should now split cleanly into `downloaded`, `missing_on_aws`, or true retryable failures. The `10` true failed rows should be retried separately after the main planned queue is reduced.
