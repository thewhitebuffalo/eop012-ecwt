# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T18:50:39+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch81_20260624T184704Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `81`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `1c36bdf53ca8b7619d743a34a54d4a3f8f12931a`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 273 |
| `missing_on_aws` | 31 |
| `total_bytes_downloaded_or_observed` | 2749102968 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 304 |
| `downloaded` | 273 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 31 |
| `failed_http` | 0 |
| `failed_exception` | 0 |
| `downloaded bytes` | 2749102968 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 33375 |
| `audit.calculation_run` | 404 |

## Missing On AWS Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `missing_on_aws` | 404 | `713041-99999` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/71304199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `716269-99999` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/71626999999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720263-63834` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/72026363834.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720399-99999` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/72039999999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720409-99999` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/72040999999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720619-99999` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/72061999999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720747-99999` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/72074799999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720776-99999` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/72077699999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `722005-99999` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/72200599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `722344-99999` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/72234499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `723264-99999` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/72326499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `723640-99999` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/72364099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `724466-03929` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/72446603929.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `724700-93141` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/72470093141.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `724856-99999` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/72485699999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `725375-14822` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/72537514822.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `725610-24030` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/72561024030.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `725785-24145` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/72578524145.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `725786-24151` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/72578624151.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `725835-24119` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/72583524119.csv` | HTTP Error 404: Not Found |

## Failure Sample

No failures recorded.

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
- `missing_on_aws` means the NOAA public AWS endpoint returned HTTP 404 for that station-year object; this is treated as a terminal missing source object, not a corrupted local file.
- `failed_http` is reserved for non-404 HTTP errors such as 500 or 503 and should remain retryable.
- `failed_exception` indicates a local or network exception and should be investigated before retrying.
