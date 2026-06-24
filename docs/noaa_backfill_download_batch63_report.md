# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T16:00:12+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch63_20260624T155540Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `63`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `ed0506ba184fdb7a06fb1ba7aca9489ea7b67bf1`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 367 |
| `missing_on_aws` | 633 |
| `total_bytes_downloaded_or_observed` | 3120998523 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 367 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 633 |
| `failed_http` | 0 |
| `failed_exception` | 0 |
| `downloaded bytes` | 3120998523 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 27913 |
| `audit.calculation_run` | 365 |

## Missing On AWS Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `missing_on_aws` | 404 | `690090-99999` | 2021 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2021/69009099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `691164-99999` | 2021 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2021/69116499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `692694-99999` | 2021 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2021/69269499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `695414-99999` | 2021 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2021/69541499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `697534-99999` | 2021 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2021/69753499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `698414-99999` | 2021 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2021/69841499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700631-99999` | 2021 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2021/70063199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702600-99999` | 2021 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2021/70260099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702628-99999` | 2021 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2021/70262899999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702629-99999` | 2021 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2021/70262999999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702645-99999` | 2021 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2021/70264599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702647-26499` | 2021 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2021/70264726499.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702675-26484` | 2021 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2021/70267526484.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702700-99999` | 2021 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2021/70270099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702735-99999` | 2021 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2021/70273599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `703053-99999` | 2021 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2021/70305399999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `703056-99999` | 2021 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2021/70305699999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `703670-99999` | 2021 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2021/70367099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `703880-99999` | 2021 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2021/70388099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `703920-99999` | 2021 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2021/70392099999.csv` | HTTP Error 404: Not Found |

## Failure Sample

No failures recorded.

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
- `missing_on_aws` means the NOAA public AWS endpoint returned HTTP 404 for that station-year object; this is treated as a terminal missing source object, not a corrupted local file.
- `failed_http` is reserved for non-404 HTTP errors such as 500 or 503 and should remain retryable.
- `failed_exception` indicates a local or network exception and should be investigated before retrying.
