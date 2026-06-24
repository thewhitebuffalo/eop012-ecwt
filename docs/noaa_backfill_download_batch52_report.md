# NOAA Backfill Batch Download Report

Generated UTC: 2026-06-24T14:40:53+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_download_batch52_20260624T143812Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Manifest batch number: `52`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `6d9f01486ea78c2b73073972e0f447fb89d4f923`
- Max workers: `4`
- Overwrite enabled: `False`
- Dry run: `False`

## Results

| Status | Count |
| --- | ---: |
| `downloaded` | 237 |
| `missing_on_aws` | 763 |
| `total_bytes_downloaded_or_observed` | 1045880198 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `download attempts for this run` | 1000 |
| `downloaded` | 237 |
| `skipped_existing` | 0 |
| `missing_on_aws` | 763 |
| `failed_http` | 0 |
| `failed_exception` | 0 |
| `downloaded bytes` | 1045880198 |
| `remaining planned rows in batch` | 0 |
| `audit.source_file` | 25244 |
| `audit.calculation_run` | 340 |

## Missing On AWS Sample

| Status | HTTP | Station | Year | URL | Error |
| --- | ---: | --- | ---: | --- | --- |
| `missing_on_aws` | 404 | `690090-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/69009099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `697534-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/69753499999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `700631-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/70063199999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702084-26650` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/70208426650.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702595-26559` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/70259526559.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702607-25378` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/70260725378.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702615-26498` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/70261526498.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702628-00105` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/70262800105.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702628-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/70262899999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702629-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/70262999999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702645-46403` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/70264546403.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702647-26499` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/70264726499.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702650-26407` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/70265026407.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702675-26484` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/70267526484.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702700-00489` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/70270000489.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702700-99999` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/70270099999.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702720-26401` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/70272026401.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702725-26491` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/70272526491.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `702756-26479` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/70275626479.csv` | HTTP Error 404: Not Found |
| `missing_on_aws` | 404 | `703053-26654` | 2001 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2001/70305326654.csv` | HTTP Error 404: Not Found |

## Failure Sample

No failures recorded.

## Interpretation

- Files are written through temporary `.part` files and moved into place only after the stream completes.
- Existing files are not overwritten unless `--overwrite` is explicitly supplied.
- Successful downloads are hashed with SHA-256 and registered in `audit.source_file`.
- `missing_on_aws` means the NOAA public AWS endpoint returned HTTP 404 for that station-year object; this is treated as a terminal missing source object, not a corrupted local file.
- `failed_http` is reserved for non-404 HTTP errors such as 500 or 503 and should remain retryable.
- `failed_exception` indicates a local or network exception and should be investigated before retrying.
