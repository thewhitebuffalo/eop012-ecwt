# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-25T11:18:18+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch8_20260625T111201Z`
- Manifest run ID: `noaa_backfill_manifest_20260625T070923Z`
- Manifest batch number: `8`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `b8c3f0898a79bc239022df07315483810d3d7fb5`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 851 |
| `missing_on_aws` | 149 |
| `total_bytes_downloaded_or_observed` | 2436159345 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 851 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 149 |
| `failed_http` | 0 |
| `failed_exception` | 0 |
| `downloaded bytes` | 2436159345 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 69817 |
| `audit.calculation_run` | 530 |

## Missing On AWS Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `missing_on_aws` | 404 | `710220-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/71022099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710220-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/71022099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710367-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/71036799999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710367-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/71036799999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710369-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/71036999999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710380-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/71038099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710380-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/71038099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710564-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/71056499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710720-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/71072099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710720-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/71072099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710730-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/71073099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `711110-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/71111099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `711110-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/71111099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `711360-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/71136099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `711360-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/71136099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `711960-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/71196099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `711960-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/71196099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `712470-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/71247099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `712470-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/71247099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `712680-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/71268099999.csv` | HTTP Error 404: Not Found |

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
