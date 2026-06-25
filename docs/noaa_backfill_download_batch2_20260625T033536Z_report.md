# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-25T03:52:06+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch2_20260625T033536Z`
- Manifest run ID: `noaa_backfill_manifest_20260625T023857Z`
- Manifest batch number: `2`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `2eb08d0b703820e49406ce689f0bf149cdd675a2`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 1000 |
| `total_bytes_downloaded_or_observed` | 7098278104 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 1000 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 0 |
| `failed_http` | 0 |
| `failed_exception` | 0 |
| `downloaded bytes` | 7098278104 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 62330 |
| `audit.calculation_run` | 471 |

## Missing On AWS Sample

No HTTP 404 missing-object outcomes recorded.

## Failure Sample

No failures recorded.

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
- Candidate station-years are selected only when station metadata has Jan-Feb or December active-window overlap for the source year, or when the station active window is unknown.
- `missing_on_aws` means the NOAA public AWS endpoint returned HTTP 404 for that station-year object; this is treated as a terminal missing source object, not a corrupted local file.
- `failed_http` is reserved for non-404 HTTP errors such as 500 or 503 and should remain retryable.
- `failed_exception` indicates a local or network exception and should be investigated before retrying.
