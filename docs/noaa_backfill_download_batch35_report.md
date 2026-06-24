# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T10:29:14+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch35_20260624T102440Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `35`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `13450e7833a9a40fe011eac55bde7b0468cf5c98`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 309 |
| `failed_http` | 691 |
| `total_bytes_downloaded_or_observed` | 1842538465 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 309 |
| `skipped_existing` | 0 |
| `failed_http` | 691 |
| `failed_exception` | 0 |
| `downloaded bytes` | 1842538465 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 19919 |
| `audit.calculation_run` | 264 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `254960-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/25496099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690090-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/69009099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690260-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/69026099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690290-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/69029099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690524-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/69052499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `691334-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/69133499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `693254-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/69325499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `697534-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/69753499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700001-26492` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/70000126492.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700197-26558` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/70019726558.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700300-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/70030099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700365-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/70036599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700450-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/70045099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700630-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/70063099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700632-26645` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/70063226645.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700634-27408` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/70063427408.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700638-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/70063899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701040-26631` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/70104026631.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701043-26623` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/70104326623.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701045-26649` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/70104526649.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
