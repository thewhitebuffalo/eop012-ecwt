# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-25T07:56:32+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch2_20260625T075043Z`
- Manifest run ID: `noaa_backfill_manifest_20260625T070923Z`
- Manifest batch number: `2`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `5364db70888272cd0eddfc40a421d6743835481e`
- Max workers: `8`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 981 |
| `missing_on_aws` | 19 |
| `total_bytes_downloaded_or_observed` | 3741422527 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 981 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 19 |
| `failed_http` | 0 |
| `failed_exception` | 0 |
| `downloaded bytes` | 3741422527 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 64310 |
| `audit.calculation_run` | 503 |

## Missing On AWS Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `missing_on_aws` | 404 | `711110-99999` | 2022 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2022/71111099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `712470-99999` | 2022 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2022/71247099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `714090-99999` | 2022 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2022/71409099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720956-00332` | 2022 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2022/72095600332.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `760500-99999` | 2021 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2021/76050099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `780630-99999` | 2021 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2021/78063099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `780700-99999` | 2020 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2020/78070099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `780700-99999` | 2021 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2021/78070099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `780700-99999` | 2022 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2022/78070099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `782300-99999` | 2021 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2021/78230099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `782300-99999` | 2022 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2022/78230099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `783280-99999` | 2022 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2022/78328099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `783320-99999` | 2021 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2021/78332099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `783320-99999` | 2022 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2022/78332099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `917010-99999` | 2021 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2021/91701099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `918120-99999` | 2020 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2020/91812099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `918120-99999` | 2021 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2021/91812099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `919010-99999` | 2020 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2020/91901099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `919010-99999` | 2021 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2021/91901099999.csv` | HTTP Error 404: Not Found |

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
