# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-23T22:48:09+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch5_20260623T224117Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `5`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `55e07669c484f3298a781d06a8591ca3dbbfe210`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 629 |
| `failed_http` | 371 |
| `total_bytes_downloaded_or_observed` | 4401775178 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 629 |
| `skipped_existing` | 0 |
| `failed_http` | 371 |
| `failed_exception` | 0 |
| `downloaded bytes` | 4401775178 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 3213 |
| `audit.calculation_run` | 18 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `254960-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/25496099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690190-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/69019099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690330-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/69033099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690584-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/69058499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `691334-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/69133499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `692784-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/69278499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700001-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/70000199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700365-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/70036599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700450-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/70045099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700630-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/70063099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700860-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/70086099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701046-26418` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/70104626418.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701210-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/70121099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701486-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/70148699999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701620-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/70162099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701745-26480` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/70174526480.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701749-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/70174999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701793-26524` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/70179326524.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701940-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/70194099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701945-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/70194599999.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
