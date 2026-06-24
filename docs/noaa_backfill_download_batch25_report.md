# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T06:22:41+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch25_20260624T061220Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `25`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `958969d0a3d5dc2746dba091f7bc527cec078cba`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 542 |
| `failed_http` | 458 |
| `total_bytes_downloaded_or_observed` | 4944929434 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 542 |
| `skipped_existing` | 0 |
| `failed_http` | 458 |
| `failed_exception` | 0 |
| `downloaded bytes` | 4944929434 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 15589 |
| `audit.calculation_run` | 184 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `692694-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/69269499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `695414-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/69541499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `698414-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/69841499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `703920-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/70392099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `703985-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/70398599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710268-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/71026899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710375-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/71037599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `713069-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/71306999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `713931-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/71393199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `716269-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/71626999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `717115-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/71711599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720113-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/72011399999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720120-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/72012099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720150-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/72015099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720169-00116` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/72016900116.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720170-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/72017099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720202-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/72020299999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720254-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/72025499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720257-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/72025799999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720261-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/72026199999.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
