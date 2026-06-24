# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T15:13:02+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch55_20260624T151301Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `55`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `7c20d9d216e1f96e9f5ba6bd0adc9b15aaf922b8`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `missing_on_aws` | 2 |
| `total_bytes_downloaded_or_observed` | 0 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 2 |
| `downloaded` | 0 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 2 |
| `failed_http` | 0 |
| `failed_exception` | 0 |
| `downloaded bytes` | 0 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 26033 |
| `audit.calculation_run` | 351 |

## Missing On AWS Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `missing_on_aws` | 404 | `720623-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/72062399999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `723441-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/72344199999.csv` | HTTP Error 404: Not Found |

## Failure Sample

No failures recorded.

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
- `missing_on_aws` means the NOAA public AWS endpoint returned HTTP 404 for that station-year object; this is treated as a terminal missing source object, not a corrupted local file.
- `failed_http` is reserved for non-404 HTTP errors such as 500 or 503 and should remain retryable.
- `failed_exception` indicates a local or network exception and should be investigated before retrying.
