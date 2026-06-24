# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T01:04:30+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch14_20260624T005814Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `14`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `2aa504b0a1dcc760d1462915d0cf12cb819b220d`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 648 |
| `failed_http` | 352 |
| `total_bytes_downloaded_or_observed` | 4988798831 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 648 |
| `skipped_existing` | 0 |
| `failed_http` | 352 |
| `failed_exception` | 0 |
| `downloaded bytes` | 4988798831 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 9004 |
| `audit.calculation_run` | 80 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `690190-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/69019099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690330-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/69033099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690584-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/69058499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `691174-99999` | 2010 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2010/69117499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `692784-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/69278499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700860-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/70086099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701749-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/70174999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701940-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/70194099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701945-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/70194599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701970-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/70197099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702312-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/70231299999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702625-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/70262599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702715-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/70271599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702980-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/70298099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `703609-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/70360999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `703627-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/70362799999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710362-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/71036299999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710445-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/71044599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `712040-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/71204099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `713059-99999` | 2011 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2011/71305999999.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
