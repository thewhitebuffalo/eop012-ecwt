# NOAA Backfill Manifest Report

Generated UTC: 2026-06-25T07:09:24+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_manifest_20260625T070923Z`
- Source inventory run ID: `noaa_raw_file_inventory_20260625T070816Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `70638301a8b6cfadca8421d1616fd7bf0d1d24bb`
- Source file ID: `noaa_global_hourly_backfill_manifest_d07d8caa7a62d5f8`

## Manifest Scope

- Download base URL: `https://noaa-global-hourly-pds.s3.amazonaws.com/`
- Target root: `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly`
- Manifest rows: `11432`
- Batch size: `1000`
- Batch count: `12`
- Status: `planned`; no files were downloaded by this step.
- Known terminal AWS 404 station-years are excluded unless `--include-known-missing-aws` is supplied.

## Priority Rule

Rows are sorted by:

1. years with zero local candidate-station raw files first
2. newer source years first
3. stations linked to more candidate plants first
4. station ID as a stable tie-breaker

## Planned Rows By Year

| Year | Planned Downloads |
| --- | ---: |
| 2000 | 362 |
| 2001 | 403 |
| 2002 | 403 |
| 2003 | 423 |
| 2004 | 499 |
| 2005 | 530 |
| 2006 | 100 |
| 2007 | 542 |
| 2008 | 595 |
| 2009 | 528 |
| 2010 | 550 |
| 2011 | 540 |
| 2012 | 537 |
| 2013 | 537 |
| 2014 | 531 |
| 2015 | 21 |
| 2016 | 523 |
| 2017 | 504 |
| 2018 | 500 |
| 2019 | 495 |
| 2020 | 492 |
| 2021 | 480 |
| 2022 | 470 |
| 2023 | 461 |
| 2024 | 2 |
| 2025 | 404 |

## First 20 Planned Downloads

| Rank | Batch | Year | Station | Plant Links | URL | Target |
| ---: | ---: | ---: | --- | ---: | --- | --- |
| 1 | 1 | 2025 | `716210-99999` | 573 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/71621099999.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2025/71621099999.csv` |
| 2 | 1 | 2025 | `714360-99999` | 459 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/71436099999.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2025/71436099999.csv` |
| 3 | 1 | 2025 | `722910-93116` | 458 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72291093116.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2025/72291093116.csv` |
| 4 | 1 | 2025 | `716970-99999` | 410 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/71697099999.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2025/71697099999.csv` |
| 5 | 1 | 2025 | `710367-99999` | 372 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/71036799999.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2025/71036799999.csv` |
| 6 | 1 | 2025 | `712650-99999` | 354 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/71265099999.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2025/71265099999.csv` |
| 7 | 1 | 2025 | `715080-99999` | 342 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/71508099999.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2025/71508099999.csv` |
| 8 | 1 | 2025 | `712940-99999` | 317 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/71294099999.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2025/71294099999.csv` |
| 9 | 1 | 2025 | `714370-99999` | 317 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/71437099999.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2025/71437099999.csv` |
| 10 | 1 | 2025 | `716240-99999` | 315 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/71624099999.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2025/71624099999.csv` |
| 11 | 1 | 2025 | `715730-99999` | 310 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/71573099999.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2025/71573099999.csv` |
| 12 | 1 | 2025 | `712630-99999` | 301 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/71263099999.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2025/71263099999.csv` |
| 13 | 1 | 2025 | `712970-99999` | 299 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/71297099999.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2025/71297099999.csv` |
| 14 | 1 | 2025 | `710630-99999` | 293 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/71063099999.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2025/71063099999.csv` |
| 15 | 1 | 2025 | `713770-99999` | 286 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/71377099999.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2025/71377099999.csv` |
| 16 | 1 | 2025 | `711830-99999` | 285 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/71183099999.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2025/71183099999.csv` |
| 17 | 1 | 2025 | `716270-94792` | 284 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/71627094792.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2025/71627094792.csv` |
| 18 | 1 | 2025 | `716120-99999` | 277 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/71612099999.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2025/71612099999.csv` |
| 19 | 1 | 2025 | `713710-99999` | 272 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/71371099999.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2025/71371099999.csv` |
| 20 | 1 | 2025 | `760550-99999` | 263 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/76055099999.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2025/76055099999.csv` |

## Database Row Counts

| Relation or Check | Rows |
| --- | ---: |
| `weather.noaa_raw_backfill_manifest for this run` | 11432 |
| `planned manifest rows` | 11432 |
| `batches` | 12 |
| `batch 1 rows` | 1000 |
| `audit.source_file` | 62335 |
| `audit.calculation_run` | 495 |

## Interpretation

- This is a download plan, not a download run.
- Batch 1 is intentionally limited to the first 1,000 planned files so the downloader can be tested without launching the entire backfill.
- The next step should run a batch downloader that consumes this manifest and records HTTP status, bytes, hashes, and failures.
