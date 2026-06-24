# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T18:38:31+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch78_20260624T183645Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `78`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `1c36bdf53ca8b7619d743a34a54d4a3f8f12931a`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 144 |
| `missing_on_aws` | 38 |
| `total_bytes_downloaded_or_observed` | 1184672435 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 182 |
| `downloaded` | 144 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 38 |
| `failed_http` | 0 |
| `failed_exception` | 0 |
| `downloaded bytes` | 1184672435 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 32348 |
| `audit.calculation_run` | 401 |

## Missing On AWS Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `missing_on_aws` | 404 | `701745-26480` | 2015 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2015/70174526480.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702195-99999` | 2015 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2015/70219599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702757-26444` | 2015 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2015/70275726444.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702986-26557` | 2015 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2015/70298626557.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `703335-99999` | 2015 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2015/70333599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `713041-99999` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/71304199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720565-99999` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/72056599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720579-99999` | 2015 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2015/72057999999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720641-99999` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/72064199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720642-99999` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/72064299999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720724-99999` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/72072499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `722005-99999` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/72200599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `722158-13752` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/72215813752.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `722294-99999` | 2015 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2015/72229499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `723264-99999` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/72326499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `723640-99999` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/72364099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `724466-03929` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/72446603929.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `724856-99999` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/72485699999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `725186-99999` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/72518699999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `725188-99999` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/72518899999.csv` | HTTP Error 404: Not Found |

## Failure Sample

No failures recorded.

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
- `missing_on_aws` means the NOAA public AWS endpoint returned HTTP 404 for that station-year object; this is treated as a terminal missing source object, not a corrupted local file.
- `failed_http` is reserved for non-404 HTTP errors such as 500 or 503 and should remain retryable.
- `failed_exception` indicates a local or network exception and should be investigated before retrying.
