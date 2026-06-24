# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T17:42:10+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch72_20260624T173926Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `72`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `c29c0a49ce6c391545b2dd5ab6fabda91eaf199a`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 210 |
| `missing_on_aws` | 790 |
| `total_bytes_downloaded_or_observed` | 1724930177 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 210 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 790 |
| `failed_http` | 0 |
| `failed_exception` | 0 |
| `downloaded bytes` | 1724930177 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 31100 |
| `audit.calculation_run` | 386 |

## Missing On AWS Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `missing_on_aws` | 404 | `690020-99999` | 2017 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2017/69002099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `690190-99999` | 2017 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2017/69019099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `690330-99999` | 2017 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2017/69033099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `691174-99999` | 2017 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2017/69117499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `698414-99999` | 2017 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2017/69841499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `703985-99999` | 2017 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2017/70398599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710268-99999` | 2017 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2017/71026899999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710361-99999` | 2017 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2017/71036199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710364-99999` | 2017 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2017/71036499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710366-99999` | 2017 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2017/71036699999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710373-99999` | 2017 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2017/71037399999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710375-99999` | 2017 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2017/71037599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `713671-99999` | 2017 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2017/71367199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `716269-99999` | 2017 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2017/71626999999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `717115-99999` | 2017 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2017/71711599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720120-99999` | 2017 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2017/72012099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720137-99999` | 2017 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2017/72013799999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720141-04868` | 2017 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2017/72014104868.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720141-99999` | 2017 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2017/72014199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720150-99999` | 2017 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2017/72015099999.csv` | HTTP Error 404: Not Found |

## Failure Sample

No failures recorded.

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
- `missing_on_aws` means the NOAA public AWS endpoint returned HTTP 404 for that station-year object; this is treated as a terminal missing source object, not a corrupted local file.
- `failed_http` is reserved for non-404 HTTP errors such as 500 or 503 and should remain retryable.
- `failed_exception` indicates a local or network exception and should be investigated before retrying.
