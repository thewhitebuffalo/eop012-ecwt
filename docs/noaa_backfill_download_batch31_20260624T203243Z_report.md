# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T20:32:44+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch31_20260624T203243Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `31`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `d7dfe307bd62b36e30127c7bd715dd45383fd810`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `missing_on_aws` | 1 |
| `total_bytes_downloaded_or_observed` | 0 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1 |
| `downloaded` | 0 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 1 |
| `failed_http` | 0 |
| `failed_exception` | 0 |
| `downloaded bytes` | 0 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 34767 |
| `audit.calculation_run` | 427 |

## Missing On AWS Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `missing_on_aws` | 404 | `744915-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/74491599999.csv` | HTTP Error 404: Not Found |

## Failure Sample

No failures recorded.

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
- `missing_on_aws` means the NOAA public AWS endpoint returned HTTP 404 for that station-year object; this is treated as a terminal missing source object, not a corrupted local file.
- `failed_http` is reserved for non-404 HTTP errors such as 500 or 503 and should remain retryable.
- `failed_exception` indicates a local or network exception and should be investigated before retrying.
