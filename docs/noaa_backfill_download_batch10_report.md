# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-23T23:36:23+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch10_20260623T232806Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `10`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `c22cc01f4cb305ebb316c53a74ae66fb88dd50da`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 661 |
| `failed_http` | 339 |
| `total_bytes_downloaded_or_observed` | 6013209787 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 661 |
| `skipped_existing` | 0 |
| `failed_http` | 339 |
| `failed_exception` | 0 |
| `downloaded bytes` | 6013209787 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 6461 |
| `audit.calculation_run` | 42 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `690190-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/69019099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690330-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/69033099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `691174-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/69117499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710366-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/71036699999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `713671-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/71367199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720137-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/72013799999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720141-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/72014199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720267-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/72026799999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720271-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/72027199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720273-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/72027399999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720274-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/72027499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720275-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/72027599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720276-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/72027699999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720277-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/72027799999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720278-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/72027899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720279-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/72027999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720283-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/72028399999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720288-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/72028899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720293-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/72029399999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720295-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/72029599999.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
