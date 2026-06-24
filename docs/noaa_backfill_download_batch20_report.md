# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T04:02:44+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch20_20260624T035647Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `20`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `980f32ae3bbd22947707f1e0aab7e73d9bd26fe0`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 587 |
| `failed_http` | 413 |
| `total_bytes_downloaded_or_observed` | 5435180348 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 587 |
| `skipped_existing` | 0 |
| `failed_http` | 413 |
| `failed_exception` | 0 |
| `downloaded bytes` | 5435180348 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 12712 |
| `audit.calculation_run` | 135 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `698414-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/69841499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710268-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/71026899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710364-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/71036499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710373-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/71037399999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `713041-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/71304199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `716269-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/71626999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `717115-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/71711599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720120-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/72012099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720129-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/72012999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720150-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/72015099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720151-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/72015199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720169-00116` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/72016900116.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720170-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/72017099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720171-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/72017199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720202-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/72020299999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720255-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/72025599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720261-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/72026199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720266-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/72026699999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720268-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/72026899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720281-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/72028199999.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
