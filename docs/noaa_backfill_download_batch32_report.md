# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T09:17:13+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch32_20260624T091132Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `32`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `51dfc45e47108eb1e6e2474ef1aa97bae44177f4`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 370 |
| `failed_http` | 630 |
| `total_bytes_downloaded_or_observed` | 2614943516 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 370 |
| `skipped_existing` | 0 |
| `failed_http` | 630 |
| `failed_exception` | 0 |
| `downloaded bytes` | 2614943516 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 18899 |
| `audit.calculation_run` | 240 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `690190-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/69019099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690330-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/69033099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `691174-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/69117499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `711610-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/71161099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `711680-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/71168099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `714630-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/71463099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720137-04867` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/72013704867.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720141-04868` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/72014104868.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720165-99999` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/72016599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720193-00117` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/72019300117.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720267-23224` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/72026723224.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720271-03044` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/72027103044.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720273-12981` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/72027312981.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720274-93799` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/72027493799.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720275-04872` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/72027504872.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720276-12983` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/72027612983.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720277-63843` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/72027763843.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720278-03704` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/72027803704.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720279-03705` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/72027903705.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720281-53969` | 2005 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2005/72028153969.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
