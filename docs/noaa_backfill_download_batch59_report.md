# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T15:21:55+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch59_20260624T152028Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `59`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `7c20d9d216e1f96e9f5ba6bd0adc9b15aaf922b8`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 40 |
| `missing_on_aws` | 960 |
| `total_bytes_downloaded_or_observed` | 326889611 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 40 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 960 |
| `failed_http` | 0 |
| `failed_exception` | 0 |
| `downloaded bytes` | 326889611 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 26551 |
| `audit.calculation_run` | 355 |

## Missing On AWS Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `missing_on_aws` | 404 | `254960-99999` | 2024 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2024/25496099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `690090-99999` | 2024 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2024/69009099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `690190-99999` | 2022 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2022/69019099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `690260-99999` | 2024 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2024/69026099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `690290-99999` | 2024 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2024/69029099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `690330-99999` | 2022 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2022/69033099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `690524-99999` | 2024 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2024/69052499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `690584-99999` | 2022 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2022/69058499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `691164-99999` | 2024 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2024/69116499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `691334-99999` | 2024 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2024/69133499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `692694-99999` | 2024 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2024/69269499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `692784-99999` | 2024 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2024/69278499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `693254-99999` | 2024 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2024/69325499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `695414-99999` | 2024 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2024/69541499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `697534-99999` | 2024 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2024/69753499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700001-99999` | 2024 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2024/70000199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700300-99999` | 2024 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2024/70030099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700365-99999` | 2024 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2024/70036599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700450-99999` | 2024 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2024/70045099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700630-99999` | 2024 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2024/70063099999.csv` | HTTP Error 404: Not Found |

## Failure Sample

No failures recorded.

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
- `missing_on_aws` means the NOAA public AWS endpoint returned HTTP 404 for that station-year object; this is treated as a terminal missing source object, not a corrupted local file.
- `failed_http` is reserved for non-404 HTTP errors such as 500 or 503 and should remain retryable.
- `failed_exception` indicates a local or network exception and should be investigated before retrying.
