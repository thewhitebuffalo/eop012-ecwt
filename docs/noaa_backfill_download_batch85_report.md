# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T19:54:08+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch85_20260624T195047Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `85`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `d7dfe307bd62b36e30127c7bd715dd45383fd810`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 254 |
| `missing_on_aws` | 62 |
| `total_bytes_downloaded_or_observed` | 1454045607 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 316 |
| `downloaded` | 254 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 62 |
| `failed_http` | 0 |
| `failed_exception` | 0 |
| `downloaded bytes` | 1454045607 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 34762 |
| `audit.calculation_run` | 414 |

## Missing On AWS Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `missing_on_aws` | 404 | `690330-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/69033099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701046-26418` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/70104626418.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `701745-26480` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/70174526480.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702195-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/70219599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `703335-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/70333599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `711610-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/71161099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `711680-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/71168099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `718530-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/71853099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `720021-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/72002199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `722158-13752` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72215813752.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `722294-99999` | 2012 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2012/72229499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `722580-13960` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72258013960.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `722618-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72261899999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `723084-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72308499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `724015-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72401599999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `724750-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72475099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `724810-23203` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72481023203.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `724836-23208` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72483623208.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `725188-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72518899999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `725306-99999` | 2006 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72530699999.csv` | HTTP Error 404: Not Found |

## Failure Sample

No failures recorded.

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
- `missing_on_aws` means the NOAA public AWS endpoint returned HTTP 404 for that station-year object; this is treated as a terminal missing source object, not a corrupted local file.
- `failed_http` is reserved for non-404 HTTP errors such as 500 or 503 and should remain retryable.
- `failed_exception` indicates a local or network exception and should be investigated before retrying.
