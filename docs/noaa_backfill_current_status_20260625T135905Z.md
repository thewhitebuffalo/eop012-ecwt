# NOAA Backfill Current Status

Generated UTC: 2026-06-25T13:59:05Z

## Summary

The active NOAA AWS backfill queue is exhausted for the latest manifest, and the historical retryable HTTP failure has been retried successfully through the auditable downloader path.

## Latest Manifest

- Manifest run ID: `noaa_backfill_manifest_20260625T070923Z`
- `downloaded` rows: 10,282
- `missing` rows: 1,150
- `planned` rows: 0
- Downloaded latest-manifest station-years not loaded into `weather.noaa_hourly_load_file`: 0

## Current Latest Download Attempt State

These counts use the latest attempt per `(station_id, source_year, raw_station_id)`.

| Latest status | HTTP | Station-years |
| --- | ---: | ---: |
| `downloaded` | 200 | 46,632 |
| `skipped_existing` |  | 407 |
| `missing_on_aws` | 404 | 45,497 |

Current latest retryable station-years: 0

`skipped_existing` is a successful terminal downloader state for this audit purpose: the target file already existed, was hashed, and was registered without overwriting.

## Retry Closure

- Retry run ID: `noaa_backfill_download_batch1_20260625T135651Z`
- Manifest retried: `noaa_backfill_manifest_20260625T023857Z`, batch 1
- Attempt rows: 408
- `skipped_existing`: 407
- `downloaded`: 1
- `failed_http`: 0
- `failed_exception`: 0

The retry closed the last current retryable station-year:

| Station | Year | Outcome | DJF coverage after load |
| --- | ---: | --- | --- |
| `725103-14712` | 2006 | downloaded | 34 / 2,160 valid DJF hours, partial |

This closes the transport failure. It does not imply the station-year has enough DJF coverage to help ECWT readiness.

## Policy Result State

- Policy materialization run ID: `plant_ecwt_policy_result_all_plants_normalized_active_window_loaded_year_20260625T135248Z`
- Plant rows: 16,132
- Distinct plants: 16,132
- Publication candidates: 16,089
- Blocked rows: 43

| Readiness status | Reason | Rows |
| --- | --- | ---: |
| `publication_candidate` | `passes_current_fixed_period_gate` | 1,641 |
| `publication_candidate` | `passes_normalized_active_window_policy` | 14,448 |
| `blocked` | `no_station_candidates` | 28 |
| `blocked` | `normalized_active_window_coverage_below_threshold` | 15 |

## Interpretation

- The remaining ECWT gap is not an active AWS downloader queue. The latest manifest has no planned rows, and there are no current retryable latest-attempt station-years.
- Remaining blocked plants are now policy/data-quality issues: 28 have no station candidates, and 15 still fail normalized active-window coverage.
- Further improvement should target station-candidate/geocoding review for the 28 no-station plants and coverage/methodology review for the 15 near-coverage plants.
