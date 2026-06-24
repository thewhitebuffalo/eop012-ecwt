# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T02:59:19+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch18_20260624T025109Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `18`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `b68bd1d44aafc4d25f023da2cee212ba7c8bec71`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 645 |
| `failed_http` | 355 |
| `total_bytes_downloaded_or_observed` | 4464983988 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 645 |
| `skipped_existing` | 0 |
| `failed_http` | 355 |
| `failed_exception` | 0 |
| `downloaded bytes` | 4464983988 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 11501 |
| `audit.calculation_run` | 112 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `254960-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/25496099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690190-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/69019099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690290-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/69029099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690584-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/69058499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `691334-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/69133499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `692784-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/69278499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700001-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/70000199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700300-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/70030099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700365-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/70036599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700450-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/70045099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700630-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/70063099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700632-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/70063299999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700860-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/70086099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701045-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/70104599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701160-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/70116099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701210-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/70121099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701486-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/70148699999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701620-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/70162099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701749-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/70174999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701940-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/70194099999.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
