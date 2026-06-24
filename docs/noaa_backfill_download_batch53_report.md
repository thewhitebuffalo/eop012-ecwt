# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T14:45:25+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch53_20260624T144100Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `53`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `6d9f01486ea78c2b73073972e0f447fb89d4f923`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Retry Note

The single `failed_exception` row in this original batch report was retried in `docs/noaa_backfill_download_batch53_retry_20260624T144415_report.md` and resolved as `missing_on_aws` after NOAA returned HTTP 404.

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 273 |
| `failed_exception` | 1 |
| `missing_on_aws` | 726 |
| `total_bytes_downloaded_or_observed` | 1065696406 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 273 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 726 |
| `failed_http` | 0 |
| `failed_exception` | 1 |
| `downloaded bytes` | 1065696406 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 25517 |
| `audit.calculation_run` | 342 |

## Missing On AWS Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `missing_on_aws` | 404 | `254960-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/25496099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `690290-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/69029099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `692784-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/69278499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `693254-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/69325499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700001-26492` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/70000126492.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700001-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/70000199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700197-26558` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/70019726558.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700365-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/70036599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700450-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/70045099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700630-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/70063099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700632-26645` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/70063226645.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700632-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/70063299999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700634-27408` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/70063427408.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700635-26465` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/70063526465.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700638-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/70063899999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700860-27401` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/70086027401.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701040-26631` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/70104026631.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701043-26623` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/70104326623.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701045-26649` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/70104526649.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701046-26418` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/70104626418.csv` | HTTP Error 404: Not Found |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_exception` |  | `720340-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/72034099999.csv` | URLError(gaierror(8, 'nodename nor servname provided, or not known')) |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
- `missing_on_aws` means the NOAA public AWS endpoint returned HTTP 404 for that station-year object; this is treated as a terminal missing source object, not a corrupted local file.
- `failed_http` is reserved for non-404 HTTP errors such as 500 or 503 and should remain retryable.
- `failed_exception` indicates a local or network exception and should be investigated before retrying.
