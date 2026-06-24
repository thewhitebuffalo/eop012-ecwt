# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T10:50:19+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch36_20260624T104511Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `36`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `ed27f0321f2dba010c8bf04889dace64f068d250`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 373 |
| `failed_http` | 627 |
| `total_bytes_downloaded_or_observed` | 2179465271 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 373 |
| `skipped_existing` | 0 |
| `failed_http` | 627 |
| `failed_exception` | 0 |
| `downloaded bytes` | 2179465271 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 20292 |
| `audit.calculation_run` | 272 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `690330-99999` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/69033099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690584-99999` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/69058499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `691174-99999` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/69117499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `692784-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/69278499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700635-26465` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/70063526465.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700860-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/70086099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701625-26542` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/70162526542.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701749-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/70174999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701793-26524` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/70179326524.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701940-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/70194099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701945-46405` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/70194546405.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701975-26422` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/70197526422.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702220-26501` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/70222026501.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702312-26555` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/70231226555.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702315-26536` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/70231526536.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702350-26534` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/70235026534.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702490-26526` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/70249026526.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702606-96401` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/70260696401.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702625-00104` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/70262500104.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702625-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/70262599999.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
