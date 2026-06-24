# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T17:49:12+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch74_20260624T174624Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `74`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `c29c0a49ce6c391545b2dd5ab6fabda91eaf199a`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 217 |
| `missing_on_aws` | 783 |
| `total_bytes_downloaded_or_observed` | 1646341452 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 217 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 783 |
| `failed_http` | 0 |
| `failed_exception` | 0 |
| `downloaded bytes` | 1646341452 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 31733 |
| `audit.calculation_run` | 388 |

## Missing On AWS Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `missing_on_aws` | 404 | `690020-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/69002099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `690190-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/69019099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `690330-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/69033099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `690584-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/69058499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `691174-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/69117499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `692784-99999` | 2017 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2017/69278499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700860-99999` | 2017 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2017/70086099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701046-26418` | 2017 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2017/70104626418.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701749-99999` | 2017 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2017/70174999999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701793-26524` | 2017 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2017/70179326524.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701940-99999` | 2017 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2017/70194099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701945-99999` | 2017 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2017/70194599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701970-99999` | 2017 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2017/70197099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702312-26555` | 2017 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2017/70231226555.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702312-99999` | 2017 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2017/70231299999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702625-99999` | 2017 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2017/70262599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702711-26439` | 2017 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2017/70271126439.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702715-99999` | 2017 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2017/70271599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702745-26560` | 2017 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2017/70274526560.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702980-99999` | 2017 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2017/70298099999.csv` | HTTP Error 404: Not Found |

## Failure Sample

No failures recorded.

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
- `missing_on_aws` means the NOAA public AWS endpoint returned HTTP 404 for that station-year object; this is treated as a terminal missing source object, not a corrupted local file.
- `failed_http` is reserved for non-404 HTTP errors such as 500 or 503 and should remain retryable.
- `failed_exception` indicates a local or network exception and should be investigated before retrying.
