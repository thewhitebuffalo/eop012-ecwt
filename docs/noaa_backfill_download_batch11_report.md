# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T00:03:01+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch11_20260623T235525Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `11`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `21e5e54ae61f56d12f48645a7965047ed330fe01`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 626 |
| `failed_http` | 374 |
| `total_bytes_downloaded_or_observed` | 6139006076 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 626 |
| `skipped_existing` | 0 |
| `failed_http` | 374 |
| `failed_exception` | 0 |
| `downloaded bytes` | 6139006076 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 7087 |
| `audit.calculation_run` | 56 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `690020-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/69002099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710361-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/71036199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710364-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/71036499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710373-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/71037399999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `713041-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/71304199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `717115-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/71711599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720120-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/72012099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720129-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/72012999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720150-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/72015099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720151-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/72015199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720168-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/72016899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720171-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/72017199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720255-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/72025599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720259-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/72025999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720268-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/72026899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720281-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/72028199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720284-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/72028499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720285-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/72028599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720289-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/72028999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720291-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/72029199999.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
