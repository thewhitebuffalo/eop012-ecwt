# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T14:49:08+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch54_20260624T144618Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `54`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `d80e885cc20835d99a6bbc66a5156b02adb133e0`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 260 |
| `missing_on_aws` | 740 |
| `total_bytes_downloaded_or_observed` | 1290362139 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 260 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 740 |
| `failed_http` | 0 |
| `failed_exception` | 0 |
| `downloaded bytes` | 1290362139 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 25777 |
| `audit.calculation_run` | 343 |

## Missing On AWS Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `missing_on_aws` | 404 | `690330-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/69033099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710366-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/71036699999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `713000-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/71300099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `713671-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/71367199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720137-04867` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/72013704867.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720137-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/72013799999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720141-04868` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/72014104868.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720141-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/72014199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720165-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/72016599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720193-00117` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/72019300117.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720267-23224` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/72026723224.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720267-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/72026799999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720271-03044` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/72027103044.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720271-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/72027199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720273-12981` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/72027312981.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720273-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/72027399999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720274-93799` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/72027493799.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720274-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/72027499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720275-04872` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/72027504872.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720275-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/72027599999.csv` | HTTP Error 404: Not Found |

## Failure Sample

No failures recorded.

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
- `missing_on_aws` means the NOAA public AWS endpoint returned HTTP 404 for that station-year object; this is treated as a terminal missing source object, not a corrupted local file.
- `failed_http` is reserved for non-404 HTTP errors such as 500 or 503 and should remain retryable.
- `failed_exception` indicates a local or network exception and should be investigated before retrying.
