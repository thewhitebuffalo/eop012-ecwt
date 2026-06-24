# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T08:02:36+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch29_20260624T075432Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `29`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `3e964a5c5ddaa4534dc927579e462160e7ff30dd`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 495 |
| `failed_http` | 505 |
| `total_bytes_downloaded_or_observed` | 4431029180 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 495 |
| `skipped_existing` | 0 |
| `failed_http` | 505 |
| `failed_exception` | 0 |
| `downloaded bytes` | 4431029180 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 17692 |
| `audit.calculation_run` | 216 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `698414-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/69841499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `703985-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/70398599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710375-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/71037599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `716269-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/71626999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `717115-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/71711599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720120-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/72012099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720129-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/72012999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720150-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/72015099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720151-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/72015199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720169-00116` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/72016900116.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720170-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/72017099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720171-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/72017199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720202-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/72020299999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720255-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/72025599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720257-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/72025799999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720261-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/72026199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720266-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/72026699999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720268-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/72026899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720289-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/72028999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720294-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/72029499999.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
