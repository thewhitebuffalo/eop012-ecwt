# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-23T22:11:05+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch2_20260623T220516Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `2`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `c14a37f5680a4beee2fd6da33d40a3a31cfc9af3`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 651 |
| `failed_http` | 349 |
| `total_bytes_downloaded_or_observed` | 4117331668 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 651 |
| `skipped_existing` | 0 |
| `failed_http` | 349 |
| `failed_exception` | 0 |
| `downloaded bytes` | 4117331668 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 1321 |
| `audit.calculation_run` | 8 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `690020-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/69002099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710361-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/71036199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710364-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/71036499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710366-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/71036699999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `710373-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/71037399999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720151-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72015199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720259-63844` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72025963844.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720259-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72025999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720268-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72026899999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720281-53969` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72028153969.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720281-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72028199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720284-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72028499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720285-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72028599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720289-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72028999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720291-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72029199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720295-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72029599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720299-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72029999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720300-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72030099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720301-99999` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72030199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `720302-53963` | 2025 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72030253963.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
