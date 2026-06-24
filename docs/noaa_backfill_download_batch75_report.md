# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T18:26:02+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch75_20260624T182205Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `75`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `1c36bdf53ca8b7619d743a34a54d4a3f8f12931a`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 216 |
| `failed_http` | 1 |
| `missing_on_aws` | 783 |
| `total_bytes_downloaded_or_observed` | 2198862366 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 216 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 783 |
| `failed_http` | 1 |
| `failed_exception` | 0 |
| `downloaded bytes` | 2198862366 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 31949 |
| `audit.calculation_run` | 395 |

## Missing On AWS Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `missing_on_aws` | 404 | `690090-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/69009099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `691164-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/69116499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `692694-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/69269499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `695414-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/69541499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `697534-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/69753499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `698414-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/69841499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702600-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/70260099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702628-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/70262899999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702629-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/70262999999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702645-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/70264599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702647-26499` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/70264726499.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702700-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/70270099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `703920-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/70392099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `703985-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/70398599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710268-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/71026899999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710375-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/71037599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710378-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/71037899999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `713069-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/71306999999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `713931-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/71393199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `716269-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/71626999999.csv` | HTTP Error 404: Not Found |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 503 | `999999-12989` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/99999912989.csv` | HTTP Error 503: Service Unavailable |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
- `missing_on_aws` means the NOAA public AWS endpoint returned HTTP 404 for that station-year object; this is treated as a terminal missing source object, not a corrupted local file.
- `failed_http` is reserved for non-404 HTTP errors such as 500 or 503 and should remain retryable.
- `failed_exception` indicates a local or network exception and should be investigated before retrying.
