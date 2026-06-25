# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-25T09:40:08+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch3_20260625T093037Z`
- Manifest run ID: `noaa_backfill_manifest_20260625T070923Z`
- Manifest batch number: `3`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `891886d03bf8418f4458e9f9f56459cf39cb2c67`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 964 |
| `missing_on_aws` | 36 |
| `total_bytes_downloaded_or_observed` | 3734049068 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 964 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 36 |
| `failed_http` | 0 |
| `failed_exception` | 0 |
| `downloaded bytes` | 3734049068 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 65274 |
| `audit.calculation_run` | 512 |

## Missing On AWS Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `missing_on_aws` | 404 | `710520-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/71052099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `710520-99999` | 2020 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2020/71052099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `711110-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/71111099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `711110-99999` | 2020 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2020/71111099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `711860-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/71186099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `712470-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/71247099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `712470-99999` | 2020 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2020/71247099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `715910-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/71591099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `716850-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/71685099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `716850-99999` | 2020 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2020/71685099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `717495-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/71749599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `717495-99999` | 2020 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2020/71749599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `718438-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/71843899999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `719561-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/71956199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `719561-99999` | 2020 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2020/71956199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720352-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/72035299999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `721025-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/72102599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `780610-99999` | 2018 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2018/78061099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `780630-99999` | 2019 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2019/78063099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `780630-99999` | 2020 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2020/78063099999.csv` | HTTP Error 404: Not Found |

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
