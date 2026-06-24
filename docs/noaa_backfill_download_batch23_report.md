# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T05:18:20+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch23_20260624T050914Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `23`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `88f480aea132c23dcb91df828d5148ffb6ecbf0b`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 610 |
| `failed_http` | 390 |
| `total_bytes_downloaded_or_observed` | 5004860108 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 610 |
| `skipped_existing` | 0 |
| `failed_http` | 390 |
| `failed_exception` | 0 |
| `downloaded bytes` | 5004860108 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 14478 |
| `audit.calculation_run` | 166 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `690190-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/69019099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690330-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/69033099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690584-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/69058499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `691174-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/69117499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `711680-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/71168099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `713671-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/71367199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720137-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/72013799999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720141-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/72014199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720193-00117` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/72019300117.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720267-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/72026799999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720271-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/72027199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720273-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/72027399999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720274-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/72027499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720275-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/72027599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720276-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/72027699999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720277-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/72027799999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720278-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/72027899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720279-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/72027999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720283-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/72028399999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720288-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/72028899999.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
