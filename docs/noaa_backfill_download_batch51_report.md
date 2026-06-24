# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T14:16:03+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch51_20260624T141326Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `51`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `46d593525e8d28c7defc6a8b356bea10a2944f7a`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 267 |
| `missing_on_aws` | 733 |
| `total_bytes_downloaded_or_observed` | 1260198878 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 267 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 733 |
| `failed_http` | 0 |
| `failed_exception` | 0 |
| `downloaded bytes` | 1260198878 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 25007 |
| `audit.calculation_run` | 333 |

## Missing On AWS Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `missing_on_aws` | 404 | `703884-25376` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/70388425376.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710190-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/71019099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710268-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/71026899999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710375-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/71037599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `715900-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/71590099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `716269-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/71626999999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720113-54829` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/72011354829.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720120-63837` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/72012063837.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720120-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/72012099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720129-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/72012999999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720150-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/72015099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720151-03049` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/72015103049.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720151-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/72015199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720169-00116` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/72016900116.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720170-63851` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/72017063851.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720170-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/72017099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720171-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/72017199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720202-00118` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/72020200118.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720202-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/72020299999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720255-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/72025599999.csv` | HTTP Error 404: Not Found |

## Failure Sample

No failures recorded.

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
- `missing_on_aws` means the NOAA public AWS endpoint returned HTTP 404 for that station-year object; this is treated as a terminal missing source object, not a corrupted local file.
- `failed_http` is reserved for non-404 HTTP errors such as 500 or 503 and should remain retryable.
- `failed_exception` indicates a local or network exception and should be investigated before retrying.
