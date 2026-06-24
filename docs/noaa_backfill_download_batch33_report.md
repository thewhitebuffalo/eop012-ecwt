# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T09:42:46+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch33_20260624T093704Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `33`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `56e65ed883387568b9894bc05e20a1681dae8979`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 381 |
| `failed_http` | 619 |
| `total_bytes_downloaded_or_observed` | 2671468058 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 381 |
| `skipped_existing` | 0 |
| `failed_http` | 619 |
| `failed_exception` | 0 |
| `downloaded bytes` | 2671468058 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 19280 |
| `audit.calculation_run` | 248 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `690020-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/69002099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `717115-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/71711599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `717520-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/71752099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `718200-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/71820099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720120-63837` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/72012063837.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720129-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/72012999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720150-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/72015099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720168-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/72016899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720170-63851` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/72017063851.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720171-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/72017199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720255-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/72025599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720257-63835` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/72025763835.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720259-63844` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/72025963844.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720268-53882` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/72026853882.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720284-04877` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/72028404877.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720285-03734` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/72028503734.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720289-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/72028999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720291-53970` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/72029153970.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720294-53898` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/72029453898.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720294-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/72029499999.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
