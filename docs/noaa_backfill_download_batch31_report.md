# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T08:54:51+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch31_20260624T084828Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `31`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `3bbb1391388ca386a595e9720e759eb1723e5e41`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 420 |
| `failed_http` | 580 |
| `total_bytes_downloaded_or_observed` | 3205014469 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 420 |
| `skipped_existing` | 0 |
| `failed_http` | 580 |
| `failed_exception` | 0 |
| `downloaded bytes` | 3205014469 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 18529 |
| `audit.calculation_run` | 232 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `254960-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/25496099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690260-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/69026099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690290-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/69029099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690524-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/69052499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690584-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/69058499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `691334-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/69133499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `692784-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/69278499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `693254-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/69325499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700001-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/70000199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700300-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/70030099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700365-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/70036599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700450-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/70045099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700630-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/70063099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700632-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/70063299999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700638-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/70063899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700860-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/70086099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701045-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/70104599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701160-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/70116099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701196-00102` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/70119600102.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701210-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/70121099999.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
