# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T19:54:27+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch86_20260624T195419Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `86`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `d7dfe307bd62b36e30127c7bd715dd45383fd810`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `missing_on_aws` | 87 |
| `total_bytes_downloaded_or_observed` | 0 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 87 |
| `downloaded` | 0 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 87 |
| `failed_http` | 0 |
| `failed_exception` | 0 |
| `downloaded bytes` | 0 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 34762 |
| `audit.calculation_run` | 415 |

## Missing On AWS Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `missing_on_aws` | 404 | `695414-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/69541499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `716269-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/71626999999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `718200-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/71820099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720202-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72020299999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720263-63834` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72026363834.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `722005-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72200599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `722322-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72232299999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `722323-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72232399999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `722344-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72234499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `723020-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72302099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `723097-93743` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72309793743.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `723264-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72326499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `723424-53919` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72342453919.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `723425-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72342599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `723490-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72349099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `723513-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72351399999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `723640-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72364099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `724466-03929` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72446603929.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `724856-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72485699999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `725244-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72524499999.csv` | HTTP Error 404: Not Found |

## Failure Sample

No failures recorded.

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
- `missing_on_aws` means the NOAA public AWS endpoint returned HTTP 404 for that station-year object; this is treated as a terminal missing source object, not a corrupted local file.
- `failed_http` is reserved for non-404 HTTP errors such as 500 or 503 and should remain retryable.
- `failed_exception` indicates a local or network exception and should be investigated before retrying.
