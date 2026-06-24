# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T18:46:56+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch80_20260624T184240Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `80`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `1c36bdf53ca8b7619d743a34a54d4a3f8f12931a`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 428 |
| `missing_on_aws` | 38 |
| `total_bytes_downloaded_or_observed` | 3049924130 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 466 |
| `downloaded` | 428 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 38 |
| `failed_http` | 0 |
| `failed_exception` | 0 |
| `downloaded bytes` | 3049924130 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 33102 |
| `audit.calculation_run` | 403 |

## Missing On AWS Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `missing_on_aws` | 404 | `702195-99999` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/70219599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702757-26444` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/70275726444.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702910-26412` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/70291026412.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702986-26557` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/70298626557.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `703335-99999` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/70333599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710160-99999` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/71016099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `711870-99999` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/71187099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720579-99999` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/72057999999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `722158-13752` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/72215813752.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `722294-99999` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/72229499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `722821-53988` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/72282153988.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `724015-99999` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/72401599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `725186-99999` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/72518699999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `725188-99999` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/72518899999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `725306-99999` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/72530699999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `725636-24017` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/72563624017.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `725637-99999` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/72563799999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `725650-03017` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/72565003017.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `725670-24032` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/72567024032.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `725700-24046` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/72570024046.csv` | HTTP Error 404: Not Found |

## Failure Sample

No failures recorded.

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
- `missing_on_aws` means the NOAA public AWS endpoint returned HTTP 404 for that station-year object; this is treated as a terminal missing source object, not a corrupted local file.
- `failed_http` is reserved for non-404 HTTP errors such as 500 or 503 and should remain retryable.
- `failed_exception` indicates a local or network exception and should be investigated before retrying.
