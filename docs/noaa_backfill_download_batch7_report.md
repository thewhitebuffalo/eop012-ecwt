# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-23T23:05:34+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch7_20260623T225737Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `7`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `55e07669c484f3298a781d06a8591ca3dbbfe210`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 666 |
| `failed_http` | 334 |
| `total_bytes_downloaded_or_observed` | 6354032458 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 666 |
| `skipped_existing` | 0 |
| `failed_http` | 334 |
| `failed_exception` | 0 |
| `downloaded bytes` | 6354032458 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 4531 |
| `audit.calculation_run` | 29 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `698414-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/69841499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `703985-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/70398599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710190-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/71019099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710268-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/71026899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710375-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/71037599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `717115-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/71711599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720120-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/72012099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720150-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/72015099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720151-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/72015199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720170-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/72017099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720202-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/72020299999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720257-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/72025799999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720261-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/72026199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720266-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/72026699999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720268-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/72026899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720289-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/72028999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720294-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/72029499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720297-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/72029799999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720305-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/72030599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720308-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/72030899999.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
