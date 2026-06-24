# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T03:43:39+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch19_20260624T033552Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `19`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `c59d6eb231a1b35d980818aec9f8ecd6b9aab536`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 624 |
| `failed_http` | 376 |
| `total_bytes_downloaded_or_observed` | 5469308070 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 624 |
| `skipped_existing` | 0 |
| `failed_http` | 376 |
| `failed_exception` | 0 |
| `downloaded bytes` | 5469308070 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 12125 |
| `audit.calculation_run` | 127 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `690020-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/69002099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690330-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/69033099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `691174-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/69117499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710361-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/71036199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710366-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/71036699999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `713671-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/71367199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720141-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/72014199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720168-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/72016899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720193-00117` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/72019300117.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720259-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/72025999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720267-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/72026799999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720273-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/72027399999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720274-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/72027499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720275-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/72027599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720276-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/72027699999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720277-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/72027799999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720278-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/72027899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720283-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/72028399999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720284-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/72028499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720291-99999` | 2009 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2009/72029199999.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
