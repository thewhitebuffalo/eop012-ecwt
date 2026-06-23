# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-23T22:56:53+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch6_20260623T224814Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `6`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `55e07669c484f3298a781d06a8591ca3dbbfe210`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 652 |
| `failed_http` | 348 |
| `total_bytes_downloaded_or_observed` | 6091165197 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 652 |
| `skipped_existing` | 0 |
| `failed_http` | 348 |
| `failed_exception` | 0 |
| `downloaded bytes` | 6091165197 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 3865 |
| `audit.calculation_run` | 22 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `690020-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/69002099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `691174-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/69117499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710361-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/71036199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710364-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/71036499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710366-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/71036699999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710373-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/71037399999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `713671-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/71367199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720259-63844` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/72025963844.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720259-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/72025999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720267-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/72026799999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720274-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/72027499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720275-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/72027599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720276-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/72027699999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720278-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/72027899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720281-53969` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/72028153969.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720281-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/72028199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720283-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/72028399999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720284-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/72028499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720285-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/72028599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720291-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/72029199999.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
