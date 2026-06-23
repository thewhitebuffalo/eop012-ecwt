# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-23T23:23:27+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch9_20260623T231656Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `9`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `1992520b60f19f08c3f604d399c496be12ea7b39`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 636 |
| `failed_http` | 364 |
| `total_bytes_downloaded_or_observed` | 5125004130 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 636 |
| `skipped_existing` | 0 |
| `failed_http` | 364 |
| `failed_exception` | 0 |
| `downloaded bytes` | 5125004130 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 5800 |
| `audit.calculation_run` | 38 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `254960-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/25496099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690260-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/69026099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690290-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/69029099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690524-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/69052499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690584-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/69058499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `691334-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/69133499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `692784-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/69278499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `693254-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/69325499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700001-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/70000199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700300-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/70030099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700365-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/70036599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700450-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/70045099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700630-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/70063099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700632-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/70063299999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700860-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/70086099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701045-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/70104599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701046-26418` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/70104626418.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701160-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/70116099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701210-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/70121099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701335-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/70133599999.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
