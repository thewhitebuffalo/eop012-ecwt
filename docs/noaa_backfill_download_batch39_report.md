# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T11:42:22+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch39_20260624T113733Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `39`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `50ccc0ea9eb41b69da2ee2762c49f370c488853b`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 341 |
| `failed_http` | 659 |
| `total_bytes_downloaded_or_observed` | 1794693097 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 341 |
| `skipped_existing` | 0 |
| `failed_http` | 659 |
| `failed_exception` | 0 |
| `downloaded bytes` | 1794693097 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 21382 |
| `audit.calculation_run` | 288 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `690090-99999` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/69009099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690260-99999` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/69026099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690524-99999` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/69052499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `691164-99999` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/69116499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `692694-99999` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/69269499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `693254-99999` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/69325499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `695414-99999` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/69541499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `697534-99999` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/69753499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700197-26558` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/70019726558.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700632-26645` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/70063226645.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701196-00102` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/70119600102.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701335-26648` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/70133526648.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701338-99999` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/70133899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702005-26647` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/70200526647.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702084-26650` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/70208426650.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702120-26646` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/70212026646.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702595-26559` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/70259526559.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702600-99999` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/70260099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702607-25378` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/70260725378.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702615-26498` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/70261526498.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
