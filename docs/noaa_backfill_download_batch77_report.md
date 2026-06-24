# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T18:36:39+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch77_20260624T183635Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `77`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `1c36bdf53ca8b7619d743a34a54d4a3f8f12931a`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `missing_on_aws` | 27 |
| `total_bytes_downloaded_or_observed` | 0 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 27 |
| `downloaded` | 0 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 27 |
| `failed_http` | 0 |
| `failed_exception` | 0 |
| `downloaded bytes` | 0 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 32204 |
| `audit.calculation_run` | 400 |

## Missing On AWS Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `missing_on_aws` | 404 | `716269-99999` | 2015 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2015/71626999999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720263-63834` | 2015 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2015/72026363834.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720302-53963` | 2015 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2015/72030253963.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720359-23902` | 2015 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2015/72035923902.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720565-99999` | 2015 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2015/72056599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720569-99999` | 2015 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2015/72056999999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720672-00485` | 2015 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2015/72067200485.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720724-99999` | 2015 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2015/72072499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720975-99999` | 2015 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2015/72097599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `722005-99999` | 2015 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2015/72200599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `722344-99999` | 2015 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2015/72234499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `723264-99999` | 2015 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2015/72326499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `723513-99999` | 2015 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2015/72351399999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `723640-99999` | 2015 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2015/72364099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `724466-03929` | 2015 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2015/72446603929.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `724856-99999` | 2015 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2015/72485699999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `725835-24119` | 2015 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2015/72583524119.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `725837-99999` | 2015 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2015/72583799999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `725875-99999` | 2015 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2015/72587599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `746720-99999` | 2015 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2015/74672099999.csv` | HTTP Error 404: Not Found |

## Failure Sample

No failures recorded.

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
- `missing_on_aws` means the NOAA public AWS endpoint returned HTTP 404 for that station-year object; this is treated as a terminal missing source object, not a corrupted local file.
- `failed_http` is reserved for non-404 HTTP errors such as 500 or 503 and should remain retryable.
- `failed_exception` indicates a local or network exception and should be investigated before retrying.
