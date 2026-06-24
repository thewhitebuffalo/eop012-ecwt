# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T04:23:00+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch21_20260624T041726Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `21`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `779eaf7545abcd2f6a8dbbc11beb1f7b28a275d4`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 580 |
| `failed_http` | 420 |
| `total_bytes_downloaded_or_observed` | 5141326885 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 580 |
| `skipped_existing` | 0 |
| `failed_http` | 420 |
| `failed_exception` | 0 |
| `downloaded bytes` | 5141326885 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 13292 |
| `audit.calculation_run` | 143 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `690090-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/69009099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `691164-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/69116499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `692694-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/69269499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `695414-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/69541499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `697534-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/69753499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702645-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/70264599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702700-00489` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/70270000489.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702700-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/70270099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `703920-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/70392099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `703985-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/70398599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710375-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/71037599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710378-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/71037899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `713069-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/71306999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `713931-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/71393199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720110-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/72011099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720113-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/72011399999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720160-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/72016099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720172-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/72017299999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720198-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/72019899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720254-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/72025499999.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
