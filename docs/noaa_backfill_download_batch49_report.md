# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T13:34:53+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch49_20260624T133047Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `49`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `82d45ac19319fe7817bf7cd2839ce16e29b79555`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 322 |
| `failed_http` | 678 |
| `total_bytes_downloaded_or_observed` | 1300390316 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 322 |
| `skipped_existing` | 0 |
| `failed_http` | 678 |
| `failed_exception` | 0 |
| `downloaded bytes` | 1300390316 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 24454 |
| `audit.calculation_run` | 323 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `690330-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/69033099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `692784-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/69278499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700001-26492` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/70000126492.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700001-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/70000199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700365-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/70036599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700630-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/70063099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700634-27408` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/70063427408.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700635-26465` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/70063526465.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701040-26631` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/70104026631.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701043-26623` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/70104326623.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701195-26625` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/70119526625.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701210-26624` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/70121026624.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701486-26642` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/70148626642.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701625-26542` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/70162526542.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701719-00490` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/70171900490.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701730-26535` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/70173026535.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701745-26480` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/70174526480.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701748-99999` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/70174899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701793-26524` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/70179326524.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701945-46405` | 2002 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2002/70194546405.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
