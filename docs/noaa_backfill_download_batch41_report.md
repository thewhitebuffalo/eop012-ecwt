# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T12:11:22+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch41_20260624T120558Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `41`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `ae1ddcd57df0ba0cf685ce5002a5a8231a97f6f4`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 324 |
| `failed_http` | 676 |
| `total_bytes_downloaded_or_observed` | 1927338889 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 324 |
| `skipped_existing` | 0 |
| `failed_http` | 676 |
| `failed_exception` | 0 |
| `downloaded bytes` | 1927338889 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 22070 |
| `audit.calculation_run` | 297 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `690330-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/69033099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710361-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/71036199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710366-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/71036699999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `713000-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/71300099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `713671-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/71367199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720141-04868` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/72014104868.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720141-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/72014199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720168-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/72016899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720175-53919` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/72017553919.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720193-00117` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/72019300117.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720259-63844` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/72025963844.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720259-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/72025999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720267-23224` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/72026723224.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720267-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/72026799999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720271-03044` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/72027103044.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720273-12981` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/72027312981.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720273-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/72027399999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720274-93799` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/72027493799.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720274-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/72027499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720275-04872` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/72027504872.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
