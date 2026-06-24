# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T11:48:33+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch40_20260624T114413Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `40`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `50ccc0ea9eb41b69da2ee2762c49f370c488853b`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 364 |
| `failed_http` | 636 |
| `total_bytes_downloaded_or_observed` | 1647034087 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 364 |
| `skipped_existing` | 0 |
| `failed_http` | 636 |
| `failed_exception` | 0 |
| `downloaded bytes` | 1647034087 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 21746 |
| `audit.calculation_run` | 290 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `254960-99999` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/25496099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690584-99999` | 2003 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2003/69058499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `691334-99999` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/69133499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `692784-99999` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/69278499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700001-26492` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/70000126492.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700365-99999` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/70036599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700630-99999` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/70063099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700634-27408` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/70063427408.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700635-26465` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/70063526465.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700638-99999` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/70063899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701040-26631` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/70104026631.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701043-26623` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/70104326623.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701045-26649` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/70104526649.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701170-26634` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/70117026634.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701195-26625` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/70119526625.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701210-26624` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/70121026624.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701337-00103` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/70133700103.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701486-26642` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/70148626642.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701625-26542` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/70162526542.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701718-26551` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/70171826551.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
