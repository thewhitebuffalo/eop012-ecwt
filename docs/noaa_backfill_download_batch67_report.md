# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T16:46:20+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch67_20260624T164222Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `67`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `3545b09233891eb8b53a3cd7593fab5554724722`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 239 |
| `missing_on_aws` | 761 |
| `total_bytes_downloaded_or_observed` | 2103161099 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 239 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 761 |
| `failed_http` | 0 |
| `failed_exception` | 0 |
| `downloaded bytes` | 2103161099 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 29340 |
| `audit.calculation_run` | 375 |

## Missing On AWS Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `missing_on_aws` | 404 | `690020-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/69002099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `690190-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/69019099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `690330-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/69033099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `690584-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/69058499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `691174-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/69117499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710190-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/71019099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710361-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/71036199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710364-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/71036499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710366-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/71036699999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710373-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/71037399999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `713671-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/71367199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `717115-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/71711599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720046-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/72004699999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720120-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/72012099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720137-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/72013799999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720141-04868` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/72014104868.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720141-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/72014199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720150-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/72015099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720151-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/72015199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720165-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/72016599999.csv` | HTTP Error 404: Not Found |

## Failure Sample

No failures recorded.

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
- `missing_on_aws` means the NOAA public AWS endpoint returned HTTP 404 for that station-year object; this is treated as a terminal missing source object, not a corrupted local file.
- `failed_http` is reserved for non-404 HTTP errors such as 500 or 503 and should remain retryable.
- `failed_exception` indicates a local or network exception and should be investigated before retrying.
