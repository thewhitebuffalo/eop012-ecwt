# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T18:30:48+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch76_20260624T182652Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `76`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `1c36bdf53ca8b7619d743a34a54d4a3f8f12931a`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 255 |
| `missing_on_aws` | 745 |
| `total_bytes_downloaded_or_observed` | 2176863854 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 255 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 745 |
| `failed_http` | 0 |
| `failed_exception` | 0 |
| `downloaded bytes` | 2176863854 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 32204 |
| `audit.calculation_run` | 397 |

## Missing On AWS Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `missing_on_aws` | 404 | `254960-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/25496099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `690190-99999` | 2015 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2015/69019099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `690260-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/69026099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `690290-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/69029099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `690330-99999` | 2015 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2015/69033099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `690524-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/69052499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `690584-99999` | 2015 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2015/69058499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `691174-99999` | 2015 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2015/69117499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `691334-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/69133499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `692784-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/69278499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `693254-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/69325499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700001-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/70000199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700300-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/70030099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700365-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/70036599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700450-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/70045099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700630-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/70063099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700631-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/70063199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700632-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/70063299999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700860-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/70086099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701045-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/70104599999.csv` | HTTP Error 404: Not Found |

## Failure Sample

No failures recorded.

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
- `missing_on_aws` means the NOAA public AWS endpoint returned HTTP 404 for that station-year object; this is treated as a terminal missing source object, not a corrupted local file.
- `failed_http` is reserved for non-404 HTTP errors such as 500 or 503 and should remain retryable.
- `failed_exception` indicates a local or network exception and should be investigated before retrying.
