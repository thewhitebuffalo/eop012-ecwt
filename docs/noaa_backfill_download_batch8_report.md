# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-23T23:16:13+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch8_20260623T230828Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `8`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `1992520b60f19f08c3f604d399c496be12ea7b39`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 633 |
| `failed_http` | 367 |
| `total_bytes_downloaded_or_observed` | 5728475141 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 633 |
| `skipped_existing` | 0 |
| `failed_http` | 367 |
| `failed_exception` | 0 |
| `downloaded bytes` | 5728475141 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 5164 |
| `audit.calculation_run` | 31 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `690090-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/69009099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `691164-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/69116499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `692694-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/69269499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `695414-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/69541499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `697534-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/69753499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700631-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/70063199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702600-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/70260099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702628-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/70262899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702629-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/70262999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702645-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/70264599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702647-26499` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/70264726499.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702675-26484` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/70267526484.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702700-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/70270099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702735-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/70273599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `703053-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/70305399999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `703056-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/70305699999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `703670-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/70367099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `703880-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/70388099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `703920-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/70392099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710365-99999` | 2023 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2023/71036599999.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
