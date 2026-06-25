# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-25T10:41:58+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch5_20260625T103323Z`
- Manifest run ID: `noaa_backfill_manifest_20260625T070923Z`
- Manifest batch number: `5`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `ffe11babb912514245701f30e4d43bdf816d8c60`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 909 |
| `missing_on_aws` | 91 |
| `total_bytes_downloaded_or_observed` | 3278543244 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 909 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 91 |
| `failed_http` | 0 |
| `failed_exception` | 0 |
| `downloaded bytes` | 3278543244 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 67120 |
| `audit.calculation_run` | 521 |

## Missing On AWS Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `missing_on_aws` | 404 | `710369-99999` | 2015 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2015/71036999999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `711110-99999` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/71111099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `711110-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/71111099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `712470-99999` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/71247099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `712470-99999` | 2015 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2015/71247099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `712470-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/71247099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `712670-99999` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/71267099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `715330-99999` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/71533099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `716004-99999` | 2013 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2013/71600499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `716004-99999` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/71600499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `716850-99999` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/71685099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `716850-99999` | 2015 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2015/71685099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `716850-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/71685099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `717134-99999` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/71713499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `717134-99999` | 2015 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2015/71713499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `717493-99999` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/71749399999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `717493-99999` | 2015 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2015/71749399999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `717493-99999` | 2016 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2016/71749399999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `717495-99999` | 2014 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2014/71749599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `717495-99999` | 2015 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2015/71749599999.csv` | HTTP Error 404: Not Found |

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
