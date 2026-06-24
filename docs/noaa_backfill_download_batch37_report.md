# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T11:16:14+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch37_20260624T111001Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `37`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `60da55785ceb0b129992646d8cda0c86164bddd5`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 398 |
| `failed_http` | 602 |
| `total_bytes_downloaded_or_observed` | 2476739545 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 398 |
| `skipped_existing` | 0 |
| `failed_http` | 602 |
| `failed_exception` | 0 |
| `downloaded bytes` | 2476739545 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 20690 |
| `audit.calculation_run` | 279 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `690020-99999` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/69002099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `713041-99999` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/71304199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `713671-99999` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/71367199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `717520-99999` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/71752099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720168-99999` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/72016899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720171-99999` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/72017199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720175-53919` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/72017553919.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720259-63844` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/72025963844.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720268-53882` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/72026853882.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720275-04872` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/72027504872.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720276-12983` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/72027612983.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720281-53969` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/72028153969.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720284-04877` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/72028404877.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720285-03734` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/72028503734.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720289-63836` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/72028963836.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720291-53970` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/72029153970.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720294-53898` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/72029453898.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720295-53972` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/72029553972.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720299-53966` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/72029953966.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720300-99999` | 2004 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2004/72030099999.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
