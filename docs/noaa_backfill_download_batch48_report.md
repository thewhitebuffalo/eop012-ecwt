# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T13:29:27+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch48_20260624T132542Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `48`
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
| `total_bytes_downloaded_or_observed` | 1292973842 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 283 |
| `skipped_existing` | 0 |
| `failed_http` | 717 |
| `failed_exception` | 0 |
| `downloaded bytes` | 1292973842 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 24132 |
| `audit.calculation_run` | 321 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `690090-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/69009099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690260-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/69026099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690290-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/69029099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `691164-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/69116499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `697534-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/69753499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700197-26558` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/70019726558.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700631-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/70063199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700632-26645` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/70063226645.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700632-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/70063299999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700638-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/70063899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701045-26649` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/70104526649.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701160-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/70116099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701170-26634` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/70117026634.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701196-00102` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/70119600102.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701335-26648` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/70133526648.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701337-00103` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/70133700103.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701338-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/70133899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701718-26551` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/70171826551.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701995-26628` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/70199526628.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702004-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/70200499999.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
