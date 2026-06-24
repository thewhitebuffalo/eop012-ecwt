# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T15:18:44+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch57_20260624T151600Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `57`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `7c20d9d216e1f96e9f5ba6bd0adc9b15aaf922b8`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 223 |
| `missing_on_aws` | 777 |
| `total_bytes_downloaded_or_observed` | 926965882 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 223 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 777 |
| `failed_http` | 0 |
| `failed_exception` | 0 |
| `downloaded bytes` | 926965882 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 26465 |
| `audit.calculation_run` | 353 |

## Missing On AWS Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `missing_on_aws` | 404 | `254960-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/25496099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `690090-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/69009099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `690260-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/69026099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `690290-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/69029099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `697534-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/69753499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700001-26492` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/70000126492.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700001-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/70000199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700197-26558` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/70019726558.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700365-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/70036599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700450-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/70045099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700630-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/70063099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700631-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/70063199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700632-26645` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/70063226645.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700632-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/70063299999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700634-27408` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/70063427408.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700638-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/70063899999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701040-26631` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/70104026631.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701043-26623` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/70104326623.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701045-26649` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/70104526649.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701160-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/70116099999.csv` | HTTP Error 404: Not Found |

## Failure Sample

No failures recorded.

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
- `missing_on_aws` means the NOAA public AWS endpoint returned HTTP 404 for that station-year object; this is treated as a terminal missing source object, not a corrupted local file.
- `failed_http` is reserved for non-404 HTTP errors such as 500 or 503 and should remain retryable.
- `failed_exception` indicates a local or network exception and should be investigated before retrying.
