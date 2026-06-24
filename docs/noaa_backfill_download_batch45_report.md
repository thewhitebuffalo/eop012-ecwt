# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T12:51:38+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch45_20260624T124646Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `45`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `a1e2c4ba5f09f8bccfe984d71f66d7cdfcc8b954`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 334 |
| `failed_http` | 666 |
| `total_bytes_downloaded_or_observed` | 1705514143 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 334 |
| `skipped_existing` | 0 |
| `failed_http` | 666 |
| `failed_exception` | 0 |
| `downloaded bytes` | 1705514143 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 23239 |
| `audit.calculation_run` | 310 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `690330-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/69033099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690584-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/69058499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `713000-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/71300099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `713671-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/71367199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720046-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/72004699999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720137-04867` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/72013704867.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720137-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/72013799999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720141-04868` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/72014104868.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720141-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/72014199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720165-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/72016599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720193-00117` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/72019300117.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720267-23224` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/72026723224.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720267-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/72026799999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720271-03044` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/72027103044.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720271-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/72027199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720273-12981` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/72027312981.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720273-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/72027399999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720274-93799` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/72027493799.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720274-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/72027499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720275-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/72027599999.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
