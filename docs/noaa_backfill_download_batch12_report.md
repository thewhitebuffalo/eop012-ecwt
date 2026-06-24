# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T00:21:51+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch12_20260624T001545Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `12`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `043fc4c3996489b673409b968dae9df329a961d9`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 614 |
| `failed_http` | 386 |
| `total_bytes_downloaded_or_observed` | 5922237084 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 614 |
| `skipped_existing` | 0 |
| `failed_http` | 386 |
| `failed_exception` | 0 |
| `downloaded bytes` | 5922237084 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 7701 |
| `audit.calculation_run` | 64 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `691164-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/69116499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `692694-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/69269499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `695414-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/69541499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `698414-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/69841499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `703920-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/70392099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `703985-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/70398599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710268-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/71026899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710375-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/71037599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710378-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/71037899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `713069-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/71306999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `713931-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/71393199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `716269-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/71626999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720110-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/72011099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720113-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/72011399999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720160-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/72016099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720169-00116` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/72016900116.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720170-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/72017099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720198-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/72019899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720202-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/72020299999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720254-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/72025499999.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
