# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T07:38:30+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch28_20260624T072817Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `28`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `164eec34fe3b7cc2b663811dd7e3de43d9e94ddd`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 519 |
| `failed_http` | 481 |
| `total_bytes_downloaded_or_observed` | 4570697032 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 519 |
| `skipped_existing` | 0 |
| `failed_http` | 481 |
| `failed_exception` | 0 |
| `downloaded bytes` | 4570697032 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 17197 |
| `audit.calculation_run` | 208 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `690020-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/69002099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `691174-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/69117499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710373-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/71037399999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `718200-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/71820099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720168-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/72016899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720193-00117` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/72019300117.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720259-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/72025999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720267-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/72026799999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720274-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/72027499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720275-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/72027599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720276-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/72027699999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720278-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/72027899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720281-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/72028199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720283-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/72028399999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720284-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/72028499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720285-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/72028599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720291-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/72029199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720293-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/72029399999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720295-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/72029599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720299-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/72029999999.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
