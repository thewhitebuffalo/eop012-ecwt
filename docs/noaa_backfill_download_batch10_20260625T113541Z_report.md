# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-25T11:41:22+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch10_20260625T113541Z`
- Manifest run ID: `noaa_backfill_manifest_20260625T070923Z`
- Manifest batch number: `10`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `14ba661f2581ddd9b191eff65ac1d870b9cde9ef`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 851 |
| `missing_on_aws` | 149 |
| `total_bytes_downloaded_or_observed` | 1839544363 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 851 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 149 |
| `failed_http` | 0 |
| `failed_exception` | 0 |
| `downloaded bytes` | 1839544363 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 71384 |
| `audit.calculation_run` | 536 |

## Missing On AWS Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `missing_on_aws` | 404 | `252820-99999` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/25282099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `252820-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/25282099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702460-26512` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/70246026512.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `703430-25402` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/70343025402.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `703430-25402` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/70343025402.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710220-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/71022099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710351-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/71035199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710450-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/71045099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710455-99999` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/71045599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710480-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/71048099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710513-27201` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/71051327201.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710720-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/71072099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710730-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/71073099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `711000-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/71100099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `711050-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/71105099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `711110-99999` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/71111099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `711110-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/71111099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `711226-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/71122699999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `711380-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/71138099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `711510-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/71151099999.csv` | HTTP Error 404: Not Found |

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
