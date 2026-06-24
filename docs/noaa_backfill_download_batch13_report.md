# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T00:45:18+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch13_20260624T003410Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `13`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `cb6b00bc1d7017e560a767ff99318b25c87ddfb6`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 655 |
| `failed_http` | 345 |
| `total_bytes_downloaded_or_observed` | 5938532225 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 655 |
| `skipped_existing` | 0 |
| `failed_http` | 345 |
| `failed_exception` | 0 |
| `downloaded bytes` | 5938532225 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 8356 |
| `audit.calculation_run` | 72 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `254960-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/25496099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690090-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/69009099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690260-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/69026099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690290-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/69029099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690524-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/69052499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `691334-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/69133499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `693254-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/69325499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `697534-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/69753499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700001-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/70000199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700300-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/70030099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700365-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/70036599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700450-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/70045099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700630-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/70063099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700631-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/70063199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700632-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/70063299999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701045-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/70104599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701160-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/70116099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701210-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/70121099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701335-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/70133599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701486-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/70148699999.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
