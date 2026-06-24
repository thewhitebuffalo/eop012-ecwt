# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T19:54:52+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch87_20260624T195443Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `87`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `d7dfe307bd62b36e30127c7bd715dd45383fd810`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `missing_on_aws` | 107 |
| `total_bytes_downloaded_or_observed` | 0 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 107 |
| `downloaded` | 0 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 107 |
| `failed_http` | 0 |
| `failed_exception` | 0 |
| `downloaded bytes` | 0 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 34762 |
| `audit.calculation_run` | 416 |

## Missing On AWS Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `missing_on_aws` | 404 | `697534-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/69753499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700638-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/70063899999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702195-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/70219599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `703335-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/70333599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710420-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/71042099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `711870-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/71187099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `712040-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/71204099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `712390-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/71239099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `713040-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/71304099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `718427-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/71842799999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720365-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72036599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `722138-63852` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72213863852.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `722142-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72214299999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `722163-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72216399999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `722294-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72229499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `722339-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72233999999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `723870-03160` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72387003160.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `724720-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72472099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `725637-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72563799999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `725753-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72575399999.csv` | HTTP Error 404: Not Found |

## Failure Sample

No failures recorded.

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
- `missing_on_aws` means the NOAA public AWS endpoint returned HTTP 404 for that station-year object; this is treated as a terminal missing source object, not a corrupted local file.
- `failed_http` is reserved for non-404 HTTP errors such as 500 or 503 and should remain retryable.
- `failed_exception` indicates a local or network exception and should be investigated before retrying.
