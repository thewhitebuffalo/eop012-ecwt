# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-25T07:15:16+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch1_20260625T071000Z`
- Manifest run ID: `noaa_backfill_manifest_20260625T070923Z`
- Manifest batch number: `1`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `de30c2150b7ea91ae5f5f39dacd0b3cacd3495d3`
- Max workers: `8`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 994 |
| `missing_on_aws` | 6 |
| `total_bytes_downloaded_or_observed` | 3285981118 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 994 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 6 |
| `failed_http` | 0 |
| `failed_exception` | 0 |
| `downloaded bytes` | 3285981118 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 63329 |
| `audit.calculation_run` | 496 |

## Missing On AWS Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `missing_on_aws` | 404 | `760500-99999` | 2022 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2022/76050099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `782300-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/78230099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `782300-99999` | 2024 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2024/78230099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `783280-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/78328099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `783280-99999` | 2024 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2024/78328099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `783320-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/78332099999.csv` | HTTP Error 404: Not Found |

## Failure Sample

No failures recorded.

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
- Candidate station-years are selected only when station metadata has Jan-Feb or December active-window overlap for the source year, or when the station active window is unknown.
- `missing_on_aws` means the NOAA public AWS endpoint returned HTTP 404 for that station-year object; this is treated as a terminal missing source object, not a corrupted local file.
- `failed_http` is reserved for non-404 HTTP errors such as 500 or 503 and should remain retryable.
- `failed_exception` indicates a local or network exception and should be investigated before retrying.
