# NOAA 404 Reclassification Report

Generated UTC: 2026-06-24T14:11:34+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_404_missing_reclassification_20260624T141114Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `3ddf7b4914837c1d572547904339f0558c4a1a1d`

## Rows Changed

| Metric | Value |
| --- | ---: |
| `download_attempt_rows_reclassified` | 0 |
| `manifest_rows_reclassified` | 25260 |

## Status Counts Before

| Object | Status | HTTP | Rows |
| --- | --- | ---: | ---: |
| `download_attempt` | `downloaded` | 200 | 24730 |
| `download_attempt` | `failed_exception` |  | 2 |
| `download_attempt` | `failed_http` | 500 | 1 |
| `download_attempt` | `failed_http` | 503 | 7 |
| `download_attempt` | `missing_on_aws` | 404 | 25260 |
| `manifest` | `downloaded` |  | 24730 |
| `manifest` | `failed` |  | 25270 |
| `manifest` | `planned` |  | 36839 |
| `manifest` | `skipped` |  | 86839 |

## Status Counts After

| Object | Status | HTTP | Rows |
| --- | --- | ---: | ---: |
| `download_attempt` | `downloaded` | 200 | 24730 |
| `download_attempt` | `failed_exception` |  | 2 |
| `download_attempt` | `failed_http` | 500 | 1 |
| `download_attempt` | `failed_http` | 503 | 7 |
| `download_attempt` | `missing_on_aws` | 404 | 25260 |
| `manifest` | `downloaded` |  | 24730 |
| `manifest` | `failed` |  | 10 |
| `manifest` | `missing` |  | 25260 |
| `manifest` | `planned` |  | 36839 |
| `manifest` | `skipped` |  | 86839 |

## Interpretation

- NOAA HTTP 404 responses are now classified as `missing_on_aws` in `weather.noaa_raw_download_attempt`.
- Matching manifest rows are now classified as `missing` instead of generic `failed`.
- Non-404 HTTP errors remain `failed_http` so they can be retried separately.
- This reclassification does not alter downloaded files or canonical weather rows.
