# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T13:24:29+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch47_20260624T132024Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `47`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `82d45ac19319fe7817bf7cd2839ce16e29b79555`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 283 |
| `failed_http` | 717 |
| `total_bytes_downloaded_or_observed` | 1348680464 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 283 |
| `skipped_existing` | 0 |
| `failed_http` | 717 |
| `failed_exception` | 0 |
| `downloaded bytes` | 1348680464 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 23849 |
| `audit.calculation_run` | 319 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `695414-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/69541499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `698414-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/69841499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `703884-25376` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/70388425376.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710190-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/71019099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710268-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/71026899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710375-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/71037599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `713069-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/71306999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `713931-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/71393199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `715900-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/71590099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `716269-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/71626999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720113-54829` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/72011354829.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720113-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/72011399999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720120-63837` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/72012063837.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720120-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/72012099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720150-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/72015099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720151-03049` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/72015103049.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720160-63884` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/72016063884.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720169-00116` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/72016900116.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720170-63851` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/72017063851.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720170-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/72017099999.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
