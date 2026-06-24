# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T08:31:14+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch30_20260624T082339Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `30`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `2136f38fe838410e162350eed29d48b74d422ae8`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 417 |
| `failed_http` | 583 |
| `total_bytes_downloaded_or_observed` | 3807036434 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 417 |
| `skipped_existing` | 0 |
| `failed_http` | 583 |
| `failed_exception` | 0 |
| `downloaded bytes` | 3807036434 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 18109 |
| `audit.calculation_run` | 224 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `690090-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/69009099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `691164-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/69116499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `692694-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/69269499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `695414-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/69541499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `697534-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/69753499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700631-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/70063199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702600-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/70260099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702628-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/70262899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702629-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/70262999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702645-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/70264599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702700-00489` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/70270000489.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702700-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/70270099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702735-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/70273599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `703053-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/70305399999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `703056-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/70305699999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `703670-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/70367099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `703880-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/70388099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `703920-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/70392099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710365-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/71036599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710378-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/71037899999.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
