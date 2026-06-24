# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T13:56:26+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch50_20260624T135332Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `50`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `782c0c6edd9c95e41b649c6f80abe0f873fcdf83`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Reclassification Note

This report was generated before NOAA HTTP 404 outcomes were split out from generic HTTP failures. The `714` HTTP 404 rows shown below as `failed_http` were later reclassified in the live database as `missing_on_aws`; see `docs/noaa_404_reclassification_report.md`.

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 286 |
| `failed_http` | 714 |
| `total_bytes_downloaded_or_observed` | 1381500222 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 286 |
| `skipped_existing` | 0 |
| `failed_http` | 714 |
| `failed_exception` | 0 |
| `downloaded bytes` | 1381500222 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 24740 |
| `audit.calculation_run` | 330 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `690020-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/69002099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710361-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/71036199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710364-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/71036499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710366-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/71036699999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710373-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/71037399999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `713000-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/71300099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `713041-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/71304199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `713671-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/71367199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `717520-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/71752099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720168-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/72016899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720175-53919` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/72017553919.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720193-00117` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/72019300117.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720259-63844` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/72025963844.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720259-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/72025999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720267-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/72026799999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720268-53882` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/72026853882.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720273-12981` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/72027312981.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720274-93799` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/72027493799.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720274-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/72027499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720275-04872` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/72027504872.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
