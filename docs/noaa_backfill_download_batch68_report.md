# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T16:52:25+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch68_20260624T164627Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `68`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `3545b09233891eb8b53a3cd7593fab5554724722`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 398 |
| `missing_on_aws` | 602 |
| `total_bytes_downloaded_or_observed` | 3690018448 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 398 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 602 |
| `failed_http` | 0 |
| `failed_exception` | 0 |
| `downloaded bytes` | 3690018448 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 29738 |
| `audit.calculation_run` | 376 |

## Missing On AWS Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `missing_on_aws` | 404 | `690090-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/69009099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `690260-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/69026099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `690524-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/69052499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `691164-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/69116499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `692694-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/69269499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `693254-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/69325499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `695414-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/69541499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `697534-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/69753499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `698414-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/69841499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700631-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/70063199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700632-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/70063299999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701160-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/70116099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701190-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/70119099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701335-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/70133599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701995-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/70199599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702070-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/70207099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702120-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/70212099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702600-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/70260099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702628-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/70262899999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702629-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/70262999999.csv` | HTTP Error 404: Not Found |

## Failure Sample

No failures recorded.

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
- `missing_on_aws` means the NOAA public AWS endpoint returned HTTP 404 for that station-year object; this is treated as a terminal missing source object, not a corrupted local file.
- `failed_http` is reserved for non-404 HTTP errors such as 500 or 503 and should remain retryable.
- `failed_exception` indicates a local or network exception and should be investigated before retrying.
