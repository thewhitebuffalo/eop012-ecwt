# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-25T11:56:22+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch11_20260625T115105Z`
- Manifest run ID: `noaa_backfill_manifest_20260625T070923Z`
- Manifest batch number: `11`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `f08661b0c85195ea5d46db3d2d81535a51d67344`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 892 |
| `missing_on_aws` | 108 |
| `total_bytes_downloaded_or_observed` | 1851802178 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 892 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 108 |
| `failed_http` | 0 |
| `failed_exception` | 0 |
| `downloaded bytes` | 1851802178 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 72276 |
| `audit.calculation_run` | 539 |

## Missing On AWS Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `missing_on_aws` | 404 | `252820-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/25282099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `253720-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/25372099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702460-26512` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/70246026512.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702460-26512` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/70246026512.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `703430-25402` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/70343025402.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `703430-25402` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/70343025402.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `704540-25704` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/70454025704.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710351-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/71035199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710351-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/71035199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710400-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/71040099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710400-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/71040099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710400-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/71040099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710455-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/71045599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710513-27201` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/71051327201.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710513-27201` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/71051327201.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `711000-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/71100099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `711510-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/71151099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `711510-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/71151099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `711510-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/71151099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `711830-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/71183099999.csv` | HTTP Error 404: Not Found |

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
