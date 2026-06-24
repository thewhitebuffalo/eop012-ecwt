# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T15:20:20+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch58_20260624T151850Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `58`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `7c20d9d216e1f96e9f5ba6bd0adc9b15aaf922b8`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 46 |
| `missing_on_aws` | 954 |
| `total_bytes_downloaded_or_observed` | 148964876 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 46 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 954 |
| `failed_http` | 0 |
| `failed_exception` | 0 |
| `downloaded bytes` | 148964876 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 26511 |
| `audit.calculation_run` | 354 |

## Missing On AWS Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `missing_on_aws` | 404 | `690020-99999` | 2024 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2024/69002099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `690190-99999` | 2024 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2024/69019099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `690330-99999` | 2024 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2024/69033099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `690584-99999` | 2024 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2024/69058499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `691174-99999` | 2024 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2024/69117499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `698414-99999` | 2024 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2024/69841499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700635-26465` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/70063526465.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700860-27401` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/70086027401.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701046-26418` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/70104626418.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701625-26542` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/70162526542.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701748-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/70174899999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701749-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/70174999999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701793-26524` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/70179326524.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701940-26413` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/70194026413.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701945-46405` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/70194546405.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701970-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/70197099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701975-26422` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/70197526422.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702220-26501` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/70222026501.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702312-26555` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/70231226555.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702315-26536` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/70231526536.csv` | HTTP Error 404: Not Found |

## Failure Sample

No failures recorded.

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
- `missing_on_aws` means the NOAA public AWS endpoint returned HTTP 404 for that station-year object; this is treated as a terminal missing source object, not a corrupted local file.
- `failed_http` is reserved for non-404 HTTP errors such as 500 or 503 and should remain retryable.
- `failed_exception` indicates a local or network exception and should be investigated before retrying.
