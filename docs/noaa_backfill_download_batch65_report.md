# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T16:35:51+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch65_20260624T163127Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `65`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `3545b09233891eb8b53a3cd7593fab5554724722`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 281 |
| `missing_on_aws` | 719 |
| `total_bytes_downloaded_or_observed` | 2566368493 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 281 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 719 |
| `failed_http` | 0 |
| `failed_exception` | 0 |
| `downloaded bytes` | 2566368493 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 28599 |
| `audit.calculation_run` | 373 |

## Missing On AWS Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `missing_on_aws` | 404 | `690020-99999` | 2020 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2020/69002099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `692694-99999` | 2020 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2020/69269499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `695414-99999` | 2020 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2020/69541499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `698414-99999` | 2020 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2020/69841499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `703920-99999` | 2020 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2020/70392099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `703985-99999` | 2020 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2020/70398599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710190-99999` | 2020 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2020/71019099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710268-99999` | 2020 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2020/71026899999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710361-99999` | 2020 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2020/71036199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710364-99999` | 2020 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2020/71036499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710366-99999` | 2020 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2020/71036699999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710373-99999` | 2020 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2020/71037399999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710375-99999` | 2020 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2020/71037599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `713069-99999` | 2020 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2020/71306999999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `713931-99999` | 2020 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2020/71393199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `716269-99999` | 2020 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2020/71626999999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `717115-99999` | 2020 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2020/71711599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720113-99999` | 2020 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2020/72011399999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720120-99999` | 2020 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2020/72012099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720150-99999` | 2020 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2020/72015099999.csv` | HTTP Error 404: Not Found |

## Failure Sample

No failures recorded.

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
- `missing_on_aws` means the NOAA public AWS endpoint returned HTTP 404 for that station-year object; this is treated as a terminal missing source object, not a corrupted local file.
- `failed_http` is reserved for non-404 HTTP errors such as 500 or 503 and should remain retryable.
- `failed_exception` indicates a local or network exception and should be investigated before retrying.
