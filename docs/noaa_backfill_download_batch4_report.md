# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-23T22:34:25+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch4_20260623T222846Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `4`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `85bf909850aa30b2ed11597e083fcdb4b9fc4b78`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 623 |
| `failed_http` | 377 |
| `total_bytes_downloaded_or_observed` | 3590769094 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 623 |
| `skipped_existing` | 0 |
| `failed_http` | 377 |
| `failed_exception` | 0 |
| `downloaded bytes` | 3590769094 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 2584 |
| `audit.calculation_run` | 14 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `690090-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/69009099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690260-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/69026099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690290-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/69029099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690524-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/69052499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `691164-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/69116499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `693254-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/69325499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `697534-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/69753499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700300-27503` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/70030027503.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700300-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/70030099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700631-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/70063199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700632-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/70063299999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701045-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/70104599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701160-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/70116099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701190-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/70119099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701335-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/70133599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701718-26551` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/70171826551.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701995-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/70199599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702070-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/70207099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702120-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/70212099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702186-26651` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/70218626651.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
