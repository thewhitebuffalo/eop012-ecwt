# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T02:09:19+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch16_20260624T020025Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `16`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `ec4f3e306097d39440575bdb79e8cabc99498898`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 608 |
| `failed_http` | 392 |
| `total_bytes_downloaded_or_observed` | 5875770746 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 608 |
| `skipped_existing` | 0 |
| `failed_http` | 392 |
| `failed_exception` | 0 |
| `downloaded bytes` | 5875770746 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 10238 |
| `audit.calculation_run` | 96 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `698414-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/69841499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `703985-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/70398599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710268-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/71026899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710375-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/71037599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `713069-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/71306999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `713931-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/71393199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `716269-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/71626999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `717115-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/71711599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720113-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/72011399999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720120-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/72012099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720129-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/72012999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720150-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/72015099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720151-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/72015199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720169-00116` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/72016900116.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720170-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/72017099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720202-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/72020299999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720255-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/72025599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720257-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/72025799999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720261-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/72026199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720263-63834` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/72026363834.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
