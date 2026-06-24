# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T12:18:17+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch42_20260624T121339Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `42`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `ae1ddcd57df0ba0cf685ce5002a5a8231a97f6f4`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 296 |
| `failed_http` | 704 |
| `total_bytes_downloaded_or_observed` | 1657097905 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 296 |
| `skipped_existing` | 0 |
| `failed_http` | 704 |
| `failed_exception` | 0 |
| `downloaded bytes` | 1657097905 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 22366 |
| `audit.calculation_run` | 299 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `698414-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/69841499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710268-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/71026899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710364-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/71036499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710373-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/71037399999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `713041-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/71304199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `716269-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/71626999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `717520-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/71752099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720113-54829` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/72011354829.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720120-63837` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/72012063837.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720120-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/72012099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720129-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/72012999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720150-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/72015099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720151-03049` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/72015103049.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720151-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/72015199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720169-00116` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/72016900116.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720170-63851` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/72017063851.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720170-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/72017099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720171-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/72017199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720202-00118` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/72020200118.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720202-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/72020299999.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
