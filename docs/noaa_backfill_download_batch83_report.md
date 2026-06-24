# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T19:42:07+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch83_20260624T193737Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `83`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `d7dfe307bd62b36e30127c7bd715dd45383fd810`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 242 |
| `missing_on_aws` | 42 |
| `total_bytes_downloaded_or_observed` | 2355961421 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 284 |
| `downloaded` | 242 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 42 |
| `failed_http` | 0 |
| `failed_exception` | 0 |
| `downloaded bytes` | 2355961421 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 34125 |
| `audit.calculation_run` | 412 |

## Missing On AWS Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `missing_on_aws` | 404 | `713041-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/71304199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720399-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/72039999999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720409-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/72040999999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720562-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/72056299999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `722005-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/72200599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `722158-13752` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/72215813752.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `723264-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/72326499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `723640-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/72364099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `724015-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/72401599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `724466-03929` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/72446603929.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `724856-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/72485699999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `725186-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/72518699999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `725188-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/72518899999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `725306-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/72530699999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `725786-24151` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/72578624151.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `725837-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/72583799999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `726887-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/72688799999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `727815-24237` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/72781524237.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `727884-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/72788499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `743920-14611` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/74392014611.csv` | HTTP Error 404: Not Found |

## Failure Sample

No failures recorded.

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
- `missing_on_aws` means the NOAA public AWS endpoint returned HTTP 404 for that station-year object; this is treated as a terminal missing source object, not a corrupted local file.
- `failed_http` is reserved for non-404 HTTP errors such as 500 or 503 and should remain retryable.
- `failed_exception` indicates a local or network exception and should be investigated before retrying.
