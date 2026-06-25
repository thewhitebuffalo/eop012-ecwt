# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-25T10:54:29+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch6_20260625T104644Z`
- Manifest run ID: `noaa_backfill_manifest_20260625T070923Z`
- Manifest batch number: `6`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `11cd1431d252dd9eb5fe78bb97a4ebe629b99da4`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 915 |
| `missing_on_aws` | 85 |
| `total_bytes_downloaded_or_observed` | 2949283352 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 915 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 85 |
| `failed_http` | 0 |
| `failed_exception` | 0 |
| `downloaded bytes` | 2949283352 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 68035 |
| `audit.calculation_run` | 524 |

## Missing On AWS Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `missing_on_aws` | 404 | `252820-99999` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/25282099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710367-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/71036799999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710369-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/71036999999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710380-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/71038099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `711110-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/71111099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `711110-99999` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/71111099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `712470-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/71247099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `712470-99999` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/71247099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `712680-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/71268099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `713240-99999` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/71324099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `715330-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/71533099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `715330-99999` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/71533099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `716004-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/71600499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `716004-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/71600499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `716080-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/71608099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `716235-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/71623599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `716235-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/71623599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `717134-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/71713499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `717134-99999` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/71713499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `717493-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/71749399999.csv` | HTTP Error 404: Not Found |

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
