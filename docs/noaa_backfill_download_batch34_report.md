# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T10:03:39+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch34_20260624T095858Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `34`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `4c03d5489b8914cebdc683e9d4ac1cef18d92df1`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 330 |
| `failed_exception` | 2 |
| `failed_http` | 668 |
| `total_bytes_downloaded_or_observed` | 2182031367 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 330 |
| `skipped_existing` | 0 |
| `failed_http` | 668 |
| `failed_exception` | 2 |
| `downloaded bytes` | 2182031367 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 19610 |
| `audit.calculation_run` | 256 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `691164-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/69116499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `692694-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/69269499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `695414-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/69541499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `698414-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/69841499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `703884-25376` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/70388425376.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `703920-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/70392099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `703985-25377` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/70398525377.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `715380-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/71538099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `716269-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/71626999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `717040-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/71704099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `717460-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/71746099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720110-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/72011099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720113-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/72011399999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720151-03049` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/72015103049.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720160-63884` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/72016063884.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720169-00116` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/72016900116.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720172-53996` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/72017253996.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720198-54813` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/72019854813.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720202-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/72020299999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720254-00119` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/72025400119.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
