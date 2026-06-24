# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T15:55:08+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch62_20260624T155126Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `62`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `ed0506ba184fdb7a06fb1ba7aca9489ea7b67bf1`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 265 |
| `missing_on_aws` | 735 |
| `total_bytes_downloaded_or_observed` | 2137749376 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 265 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 735 |
| `failed_http` | 0 |
| `failed_exception` | 0 |
| `downloaded bytes` | 2137749376 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 27546 |
| `audit.calculation_run` | 364 |

## Missing On AWS Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `missing_on_aws` | 404 | `690020-99999` | 2021 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2021/69002099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `690190-99999` | 2021 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2021/69019099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `690330-99999` | 2021 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2021/69033099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `690584-99999` | 2021 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2021/69058499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `691174-99999` | 2021 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2021/69117499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `692784-99999` | 2022 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2022/69278499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700860-99999` | 2022 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2022/70086099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701046-26418` | 2022 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2022/70104626418.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701749-99999` | 2022 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2022/70174999999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701793-26524` | 2022 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2022/70179326524.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701940-99999` | 2022 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2022/70194099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701945-99999` | 2022 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2022/70194599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701970-99999` | 2022 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2022/70197099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702312-26555` | 2022 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2022/70231226555.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702312-99999` | 2022 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2022/70231299999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702625-99999` | 2022 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2022/70262599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702711-26439` | 2022 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2022/70271126439.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702715-99999` | 2022 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2022/70271599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702745-26560` | 2022 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2022/70274526560.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702980-99999` | 2022 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2022/70298099999.csv` | HTTP Error 404: Not Found |

## Failure Sample

No failures recorded.

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
- `missing_on_aws` means the NOAA public AWS endpoint returned HTTP 404 for that station-year object; this is treated as a terminal missing source object, not a corrupted local file.
- `failed_http` is reserved for non-404 HTTP errors such as 500 or 503 and should remain retryable.
- `failed_exception` indicates a local or network exception and should be investigated before retrying.
