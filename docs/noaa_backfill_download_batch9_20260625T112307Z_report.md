# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-25T11:28:55+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch9_20260625T112307Z`
- Manifest run ID: `noaa_backfill_manifest_20260625T070923Z`
- Manifest batch number: `9`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `66fc6f9cc20081a97c9ab607de0fa2c787c57987`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 716 |
| `missing_on_aws` | 284 |
| `total_bytes_downloaded_or_observed` | 2021443427 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 716 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 284 |
| `failed_http` | 0 |
| `failed_exception` | 0 |
| `downloaded bytes` | 2021443427 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 70533 |
| `audit.calculation_run` | 533 |

## Missing On AWS Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `missing_on_aws` | 404 | `252820-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/25282099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `252820-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/25282099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `252820-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/25282099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710220-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/71022099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710220-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/71022099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710380-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/71038099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710380-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/71038099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710380-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/71038099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710480-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/71048099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710480-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/71048099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710480-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/71048099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710510-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/71051099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710510-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/71051099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710510-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/71051099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710564-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/71056499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710564-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/71056499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710564-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/71056499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710720-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/71072099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710720-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/71072099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710730-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/71073099999.csv` | HTTP Error 404: Not Found |

## Failure Sample

No failures recorded.

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
- Candidate station-years are selected only when station metadata has Jan-Feb or December active-window overlap for the source year, or when the station active window is unknown.
- `missing_on_aws` means the NOAA public AWS endpoint returned HTTP 404 for that station-year object; this is treated as a terminal missing source object, not a corrupted local file.
- `failed_http` is reserved for non-404 HTTP errors such as 500 or 503 and should remain retryable.
- `failed_exception` indicates a local or network exception and should be investigated before retrying.
