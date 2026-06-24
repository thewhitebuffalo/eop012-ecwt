# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T07:07:28+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch27_20260624T070012Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `27`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `26b8fe67506d2ffc156a91dffd8029ebe333eb9c`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 546 |
| `failed_http` | 454 |
| `total_bytes_downloaded_or_observed` | 3787302418 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 546 |
| `skipped_existing` | 0 |
| `failed_http` | 454 |
| `failed_exception` | 0 |
| `downloaded bytes` | 3787302418 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 16678 |
| `audit.calculation_run` | 200 |

## Failure Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `failed_http` | 404 | `254960-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/25496099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690190-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/69019099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690330-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/69033099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `690584-99999` | 2007 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2007/69058499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `691334-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/69133499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `692784-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/69278499999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700001-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/70000199999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700365-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/70036599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700450-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/70045099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700630-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/70063099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `700860-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/70086099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701210-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/70121099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701486-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/70148699999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701620-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/70162099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701719-00490` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/70171900490.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701749-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/70174999999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701940-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/70194099999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `701945-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/70194599999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702006-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/70200699999.csv` | HTTP Error 404: Not Found |
| `failed_http` | 404 | `702040-99999` | 2008 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2008/70204099999.csv` | HTTP Error 404: Not Found |

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
