# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T12:24:34+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch43_20260624T122017Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `43`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `ae1ddcd57df0ba0cf685ce5002a5a8231a97f6f4`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 260 |
| `failed_http` | 740 |
| `total_bytes_downloaded_or_observed` | 1507163405 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 260 |
| `skipped_existing` | 0 |
| `failed_http` | 740 |
| `failed_exception` | 0 |
| `downloaded bytes` | 1507163405 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 22626 |
| `audit.calculation_run` | 301 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `690090-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/69009099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `691164-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/69116499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `692694-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/69269499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `695414-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/69541499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `697534-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/69753499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702607-25378` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/70260725378.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702615-26498` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/70261526498.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702645-46403` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/70264546403.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702647-26499` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/70264726499.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702650-26407` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/70265026407.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702700-00489` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/70270000489.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702720-26401` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/70272026401.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `703670-25322` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/70367025322.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `703884-25376` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/70388425376.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `703920-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/70392099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `703985-25377` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/70398525377.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710375-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/71037599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710378-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/71037899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `713069-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/71306999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `713931-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/71393199999.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
