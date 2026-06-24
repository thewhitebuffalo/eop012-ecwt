# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T19:50:36+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch84_20260624T194220Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `84`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `d7dfe307bd62b36e30127c7bd715dd45383fd810`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 383 |
| `missing_on_aws` | 41 |
| `total_bytes_downloaded_or_observed` | 4308629858 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 424 |
| `downloaded` | 383 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 41 |
| `failed_http` | 0 |
| `failed_exception` | 0 |
| `downloaded bytes` | 4308629858 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 34508 |
| `audit.calculation_run` | 413 |

## Missing On AWS Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `missing_on_aws` | 404 | `711870-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/71187099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `716269-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/71626999999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720263-63834` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/72026363834.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720385-00419` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/72038500419.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720729-00435` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/72072900435.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `722344-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/72234499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `725244-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/72524499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `725835-24119` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/72583524119.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `725875-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/72587599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `727873-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/72787399999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `746720-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/74672099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `747780-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/74778099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `911907-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/91190799999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `994019-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/99401999999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `994046-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/99404699999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `994050-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/99405099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `997261-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/99726199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `997262-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/99726299999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `997282-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/99728299999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `997293-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/99729399999.csv` | HTTP Error 404: Not Found |

## Failure Sample

No failures recorded.

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
- `missing_on_aws` means the NOAA public AWS endpoint returned HTTP 404 for that station-year object; this is treated as a terminal missing source object, not a corrupted local file.
- `failed_http` is reserved for non-404 HTTP errors such as 500 or 503 and should remain retryable.
- `failed_exception` indicates a local or network exception and should be investigated before retrying.
