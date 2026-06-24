# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T16:56:56+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch69_20260624T165238Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `69`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `3545b09233891eb8b53a3cd7593fab5554724722`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 366 |
| `missing_on_aws` | 634 |
| `total_bytes_downloaded_or_observed` | 2598390933 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 366 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 634 |
| `failed_http` | 0 |
| `failed_exception` | 0 |
| `downloaded bytes` | 2598390933 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 30104 |
| `audit.calculation_run` | 377 |

## Missing On AWS Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `missing_on_aws` | 404 | `254960-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/25496099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `690190-99999` | 2018 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2018/69019099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `690290-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/69029099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `690330-99999` | 2018 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2018/69033099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `690584-99999` | 2018 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2018/69058499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `691174-99999` | 2018 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2018/69117499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `691334-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/69133499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `692784-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/69278499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700001-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/70000199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700300-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/70030099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700365-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/70036599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700450-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/70045099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700630-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/70063099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700860-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/70086099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701045-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/70104599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701046-26418` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/70104626418.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701210-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/70121099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701486-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/70148699999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701620-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/70162099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701745-26480` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/70174526480.csv` | HTTP Error 404: Not Found |

## Failure Sample

No failures recorded.

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
- `missing_on_aws` means the NOAA public AWS endpoint returned HTTP 404 for that station-year object; this is treated as a terminal missing source object, not a corrupted local file.
- `failed_http` is reserved for non-404 HTTP errors such as 500 or 503 and should remain retryable.
- `failed_exception` indicates a local or network exception and should be investigated before retrying.
