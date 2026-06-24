# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T12:58:08+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch46_20260624T125339Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `46`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `a1e2c4ba5f09f8bccfe984d71f66d7cdfcc8b954`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 327 |
| `failed_http` | 673 |
| `total_bytes_downloaded_or_observed` | 1658512741 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 327 |
| `skipped_existing` | 0 |
| `failed_http` | 673 |
| `failed_exception` | 0 |
| `downloaded bytes` | 1658512741 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 23566 |
| `audit.calculation_run` | 312 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `690020-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/69002099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710361-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/71036199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710364-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/71036499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710366-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/71036699999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710373-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/71037399999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `713041-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/71304199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `717520-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/71752099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720129-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/72012999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720151-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/72015199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720168-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/72016899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720171-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/72017199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720175-53919` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/72017553919.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720255-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/72025599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720259-63844` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/72025963844.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720259-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/72025999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720268-53882` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/72026853882.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720268-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/72026899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720275-04872` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/72027504872.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720281-53969` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/72028153969.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720281-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/72028199999.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
