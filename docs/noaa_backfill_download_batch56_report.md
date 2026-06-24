# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T15:15:53+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch56_20260624T151319Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `56`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `7c20d9d216e1f96e9f5ba6bd0adc9b15aaf922b8`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 209 |
| `missing_on_aws` | 791 |
| `total_bytes_downloaded_or_observed` | 995969341 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 209 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 791 |
| `failed_http` | 0 |
| `failed_exception` | 0 |
| `downloaded bytes` | 995969341 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 26242 |
| `audit.calculation_run` | 352 |

## Missing On AWS Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `missing_on_aws` | 404 | `691164-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/69116499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `692694-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/69269499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `695414-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/69541499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `698414-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/69841499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702725-26491` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/70272526491.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `703884-25376` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/70388425376.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `703920-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/70392099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `703985-25377` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/70398525377.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710268-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/71026899999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710375-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/71037599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710378-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/71037899999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `713069-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/71306999999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `713931-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/71393199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `715900-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/71590099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `716269-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/71626999999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `717040-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/71704099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `717460-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/71746099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720110-53983` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/72011053983.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720110-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/72011099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720113-54829` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/72011354829.csv` | HTTP Error 404: Not Found |

## Failure Sample

No failures recorded.

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
- `missing_on_aws` means the NOAA public AWS endpoint returned HTTP 404 for that station-year object; this is treated as a terminal missing source object, not a corrupted local file.
- `failed_http` is reserved for non-404 HTTP errors such as 500 or 503 and should remain retryable.
- `failed_exception` indicates a local or network exception and should be investigated before retrying.
