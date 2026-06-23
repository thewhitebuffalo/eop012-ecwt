# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-23T21:59:06+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch1_20260623T215245Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `1`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `d8531a65af1ffb3e6fb39789ed9abf4edbba33db`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 660 |
| `failed_http` | 340 |
| `total_bytes_downloaded_or_observed` | 3868046149 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 660 |
| `skipped_existing` | 0 |
| `failed_http` | 340 |
| `failed_exception` | 0 |
| `downloaded bytes` | 3868046149 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 670 |
| `audit.calculation_run` | 7 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `690190-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/69019099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690330-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/69033099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690584-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/69058499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `691174-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/69117499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `713671-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/71367199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720046-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72004699999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720137-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72013799999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720141-04868` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72014104868.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720141-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72014199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720165-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72016599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720267-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72026799999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720271-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72027199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720273-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72027399999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720274-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72027499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720275-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72027599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720276-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72027699999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720277-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72027799999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720278-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72027899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720279-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72027999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720283-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72028399999.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
