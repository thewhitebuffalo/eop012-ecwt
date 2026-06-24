# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T02:37:52+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch17_20260624T022728Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `17`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `4213bd46fec9f6cb2a66524316141c02cd69cf14`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 618 |
| `failed_http` | 382 |
| `total_bytes_downloaded_or_observed` | 5680652802 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 618 |
| `skipped_existing` | 0 |
| `failed_http` | 382 |
| `failed_exception` | 0 |
| `downloaded bytes` | 5680652802 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 10856 |
| `audit.calculation_run` | 104 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `690090-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/69009099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690260-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/69026099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690524-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/69052499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `691164-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/69116499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `692694-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/69269499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `693254-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/69325499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `695414-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/69541499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `697534-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/69753499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700631-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/70063199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701335-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/70133599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702120-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/70212099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702600-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/70260099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702628-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/70262899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702629-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/70262999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702645-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/70264599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702686-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/70268699999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702700-00489` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/70270000489.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702700-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/70270099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702735-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/70273599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `703053-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/70305399999.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
