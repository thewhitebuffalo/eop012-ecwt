# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-25T02:52:09+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch1_20260625T023959Z`
- Manifest run ID: `noaa_backfill_manifest_20260625T023857Z`
- Manifest batch number: `1`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `3062fa36c307d32792275ad15f71a3f2bd74e50b`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 999 |
| `failed_http` | 1 |
| `total_bytes_downloaded_or_observed` | 7493439336 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 999 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 0 |
| `failed_http` | 1 |
| `failed_exception` | 0 |
| `downloaded bytes` | 7493439336 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 62330 |
| `audit.calculation_run` | 462 |

## Missing On AWS Sample

No HTTP 404 missing-object outcomes recorded.

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 503 | `725103-14712` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72510314712.csv` | HTTP Error 503: Service Unavailable |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
- Candidate station-years are selected only when station metadata has Jan-Feb or December active-window overlap for the source year, or when the station active window is unknown.
- `missing_on_aws` means the NOAA public AWS endpoint returned HTTP 404 for that station-year object; this is treated as a terminal missing source object, not a corrupted local file.
- `failed_http` is reserved for non-404 HTTP errors such as 500 or 503 and should remain retryable.
- `failed_exception` indicates a local or network exception and should be investigated before retrying.
