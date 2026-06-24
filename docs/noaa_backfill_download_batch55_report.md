# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T15:12:25+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch55_20260624T150929Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `55`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `7c20d9d216e1f96e9f5ba6bd0adc9b15aaf922b8`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Retry Note

The two `failed_http` rows in this original batch report were HTTP 503 responses. They were retried in `docs/noaa_backfill_download_batch55_20260624T151301Z_report.md` and both resolved as `missing_on_aws` after NOAA returned HTTP 404.

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 256 |
| `failed_http` | 2 |
| `missing_on_aws` | 742 |
| `total_bytes_downloaded_or_observed` | 1225855631 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 256 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 742 |
| `failed_http` | 2 |
| `failed_exception` | 0 |
| `downloaded bytes` | 1225855631 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 26033 |
| `audit.calculation_run` | 350 |

## Missing On AWS Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `missing_on_aws` | 404 | `690020-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/69002099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710190-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/71019099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710361-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/71036199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710364-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/71036499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710373-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/71037399999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `713041-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/71304199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `717520-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/71752099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720120-63837` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/72012063837.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720120-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/72012099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720129-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/72012999999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720150-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/72015099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720151-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/72015199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720168-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/72016899999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720170-63851` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/72017063851.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720171-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/72017199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720175-53919` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/72017553919.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720202-00118` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/72020200118.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720255-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/72025599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720257-63835` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/72025763835.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720259-63844` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/72025963844.csv` | HTTP Error 404: Not Found |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 503 | `720623-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/72062399999.csv` | HTTP Error 503: Service Unavailable |
| `failed_http` | 503 | `723441-99999` | 2000 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2000/72344199999.csv` | HTTP Error 503: Service Unavailable |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
- `missing_on_aws` means the NOAA public AWS endpoint returned HTTP 404 for that station-year object; this is treated as a terminal missing source object, not a corrupted local file.
- `failed_http` is reserved for non-404 HTTP errors such as 500 or 503 and should remain retryable.
- `failed_exception` indicates a local or network exception and should be investigated before retrying.
