# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T18:42:34+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch79_20260624T183840Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `79`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `1c36bdf53ca8b7619d743a34a54d4a3f8f12931a`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 326 |
| `missing_on_aws` | 43 |
| `total_bytes_downloaded_or_observed` | 3012564279 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 369 |
| `downloaded` | 326 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 43 |
| `failed_http` | 0 |
| `failed_exception` | 0 |
| `downloaded bytes` | 3012564279 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 32674 |
| `audit.calculation_run` | 402 |

## Missing On AWS Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `missing_on_aws` | 404 | `702615-26498` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/70261526498.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `716269-99999` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/71626999999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720263-63834` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/72026363834.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720359-23902` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/72035923902.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720369-04135` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/72036904135.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720409-99999` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/72040999999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720569-99999` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/72056999999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720619-99999` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/72061999999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720776-99999` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/72077699999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720975-99999` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/72097599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720981-99999` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/72098199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720987-99999` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/72098799999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720999-99999` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/72099999999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `721005-99999` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/72100599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `721007-99999` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/72100799999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `721016-99999` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/72101699999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `722344-99999` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/72234499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `723513-99999` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/72351399999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `724450-03945` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/72445003945.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `724620-23061` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/72462023061.csv` | HTTP Error 404: Not Found |

## Failure Sample

No failures recorded.

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
- `missing_on_aws` means the NOAA public AWS endpoint returned HTTP 404 for that station-year object; this is treated as a terminal missing source object, not a corrupted local file.
- `failed_http` is reserved for non-404 HTTP errors such as 500 or 503 and should remain retryable.
- `failed_exception` indicates a local or network exception and should be investigated before retrying.
