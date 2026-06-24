# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T11:35:19+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch38_20260624T112958Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `38`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `50ccc0ea9eb41b69da2ee2762c49f370c488853b`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 351 |
| `failed_http` | 649 |
| `total_bytes_downloaded_or_observed` | 2111816551 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 351 |
| `skipped_existing` | 0 |
| `failed_http` | 649 |
| `failed_exception` | 0 |
| `downloaded bytes` | 2111816551 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 21041 |
| `audit.calculation_run` | 286 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `698414-99999` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/69841499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `703884-25376` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/70388425376.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `713069-99999` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/71306999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `713931-99999` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/71393199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `716269-99999` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/71626999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720113-54829` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/72011354829.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720120-63837` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/72012063837.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720129-99999` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/72012999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720151-03049` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/72015103049.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720169-00116` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/72016900116.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720170-63851` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/72017063851.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720202-00118` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/72020200118.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720255-99999` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/72025599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720257-63835` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/72025763835.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720261-53976` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/72026153976.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720263-63834` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/72026363834.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720266-54809` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/72026654809.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720269-12982` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/72026912982.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720272-94282` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/72027294282.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720287-53967` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/72028753967.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
