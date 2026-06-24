# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T19:37:27+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch82_20260624T192807Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `82`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `d7dfe307bd62b36e30127c7bd715dd45383fd810`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 508 |
| `missing_on_aws` | 30 |
| `total_bytes_downloaded_or_observed` | 4313162098 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 538 |
| `downloaded` | 508 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 30 |
| `failed_http` | 0 |
| `failed_exception` | 0 |
| `downloaded bytes` | 4313162098 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 33883 |
| `audit.calculation_run` | 411 |

## Missing On AWS Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `missing_on_aws` | 404 | `700638-99999` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/70063899999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702195-99999` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/70219599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702670-26415` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/70267026415.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702757-26444` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/70275726444.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702986-26557` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/70298626557.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `703335-99999` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/70333599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710010-99999` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/71001099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `711870-99999` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/71187099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `718800-99999` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/71880099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720359-23902` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/72035923902.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720504-99999` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/72050499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720975-99999` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/72097599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `722294-99999` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/72229499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `722821-53988` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/72282153988.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `724720-99999` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/72472099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `724776-93075` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/72477693075.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `725244-99999` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/72524499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `725635-24044` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/72563524044.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `725637-99999` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/72563799999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `725875-99999` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/72587599999.csv` | HTTP Error 404: Not Found |

## Failure Sample

No failures recorded.

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
- `missing_on_aws` means the NOAA public AWS endpoint returned HTTP 404 for that station-year object; this is treated as a terminal missing source object, not a corrupted local file.
- `failed_http` is reserved for non-404 HTTP errors such as 500 or 503 and should remain retryable.
- `failed_exception` indicates a local or network exception and should be investigated before retrying.
