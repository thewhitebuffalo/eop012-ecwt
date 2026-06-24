# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T17:39:10+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch71_20260624T173411Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `71`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `c29c0a49ce6c391545b2dd5ab6fabda91eaf199a`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 481 |
| `missing_on_aws` | 519 |
| `total_bytes_downloaded_or_observed` | 3653392108 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 481 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 519 |
| `failed_http` | 0 |
| `failed_exception` | 0 |
| `downloaded bytes` | 3653392108 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 30890 |
| `audit.calculation_run` | 385 |

## Missing On AWS Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `missing_on_aws` | 404 | `254960-99999` | 2018 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2018/25496099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `690090-99999` | 2018 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2018/69009099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `690260-99999` | 2018 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2018/69026099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `690290-99999` | 2018 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2018/69029099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `690524-99999` | 2018 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2018/69052499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `690584-99999` | 2017 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2017/69058499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `691334-99999` | 2018 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2018/69133499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `692784-99999` | 2018 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2018/69278499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `693254-99999` | 2018 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2018/69325499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `697534-99999` | 2018 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2018/69753499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700001-99999` | 2018 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2018/70000199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700300-99999` | 2018 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2018/70030099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700365-99999` | 2018 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2018/70036599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700450-99999` | 2018 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2018/70045099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700630-99999` | 2018 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2018/70063099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700631-99999` | 2018 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2018/70063199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700632-99999` | 2018 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2018/70063299999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700860-99999` | 2018 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2018/70086099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701045-99999` | 2018 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2018/70104599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701046-26418` | 2018 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2018/70104626418.csv` | HTTP Error 404: Not Found |

## Failure Sample

No failures recorded.

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
- `missing_on_aws` means the NOAA public AWS endpoint returned HTTP 404 for that station-year object; this is treated as a terminal missing source object, not a corrupted local file.
- `failed_http` is reserved for non-404 HTTP errors such as 500 or 503 and should remain retryable.
- `failed_exception` indicates a local or network exception and should be investigated before retrying.
