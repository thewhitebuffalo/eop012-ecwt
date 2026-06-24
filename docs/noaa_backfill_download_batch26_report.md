# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T06:46:44+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch26_20260624T063701Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `26`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `bd9b876cf3e00028f3088805cac252947d234fe5`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 543 |
| `failed_http` | 457 |
| `total_bytes_downloaded_or_observed` | 4344936888 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 543 |
| `skipped_existing` | 0 |
| `failed_http` | 457 |
| `failed_exception` | 0 |
| `downloaded bytes` | 4344936888 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 16132 |
| `audit.calculation_run` | 192 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `690090-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/69009099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690260-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/69026099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690290-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/69029099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690524-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/69052499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `691164-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/69116499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `693254-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/69325499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `697534-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/69753499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700300-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/70030099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700631-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/70063199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700632-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/70063299999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700638-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/70063899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701045-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/70104599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701160-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/70116099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701190-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/70119099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701335-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/70133599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701337-00103` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/70133700103.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701338-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/70133899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701995-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/70199599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702004-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/70200499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702070-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/70207099999.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
