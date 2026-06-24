# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T12:45:04+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch44_20260624T124101Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `44`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `a1e2c4ba5f09f8bccfe984d71f66d7cdfcc8b954`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 279 |
| `failed_http` | 721 |
| `total_bytes_downloaded_or_observed` | 1299734329 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 279 |
| `skipped_existing` | 0 |
| `failed_http` | 721 |
| `failed_exception` | 0 |
| `downloaded bytes` | 1299734329 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 22905 |
| `audit.calculation_run` | 308 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `254960-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/25496099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690260-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/69026099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690290-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/69029099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690524-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/69052499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `692784-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/69278499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700001-26492` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/70000126492.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700001-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/70000199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700197-26558` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/70019726558.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700365-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/70036599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700450-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/70045099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700631-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/70063199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700632-26645` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/70063226645.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700632-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/70063299999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700634-27408` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/70063427408.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700635-26465` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/70063526465.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700638-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/70063899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701040-26631` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/70104026631.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701043-26623` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/70104326623.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701045-26649` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/70104526649.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701046-26418` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/70104626418.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
