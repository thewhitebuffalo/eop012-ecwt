# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T01:30:02+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch15_20260624T012102Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `15`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `5ed115bce9078238739a56a5ced32e36af85befd`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 626 |
| `failed_http` | 374 |
| `total_bytes_downloaded_or_observed` | 5814093998 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 626 |
| `skipped_existing` | 0 |
| `failed_http` | 374 |
| `failed_exception` | 0 |
| `downloaded bytes` | 5814093998 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 9630 |
| `audit.calculation_run` | 88 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `690020-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/69002099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710361-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/71036199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710364-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/71036499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710366-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/71036699999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710373-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/71037399999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `713041-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/71304199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `713671-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/71367199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720168-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/72016899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720171-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/72017199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720259-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/72025999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720268-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/72026899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720274-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/72027499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720275-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/72027599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720276-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/72027699999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720281-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/72028199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720284-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/72028499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720285-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/72028599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720289-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/72028999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720291-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/72029199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720294-53898` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/72029453898.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
