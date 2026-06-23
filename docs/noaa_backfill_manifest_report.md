# NOAA Backfill Manifest Report

Generated UTC: 2026-06-23T21:52:24+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_manifest_20260623T215215Z`
- Source inventory run ID: `noaa_raw_file_inventory_20260623T213439Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `d8531a65af1ffb3e6fb39789ed9abf4edbba33db`
- Source file ID: `noaa_global_hourly_backfill_manifest_d07d8caa7a62d5f8`

## Manifest Scope

- Download base URL: `https://noaa-global-hourly-pds.s3.amazonaws.com/`
- Target root: `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly`
- Manifest rows: `86839`
- Batch size: `1000`
- Batch count: `87`
- Status: `planned`; no files were downloaded by this step.

## Priority Rule

Rows are sorted by:

1. years with zero local candidate-station raw files first
2. newer source years first
3. stations linked to more candidate plants first
4. station ID as a stable tie-breaker

## Planned Rows By Year

| Year | Planned Downloads |
| --- | ---: |
| 2000 | 4400 |
| 2001 | 4400 |
| 2002 | 4400 |
| 2003 | 4400 |
| 2004 | 4400 |
| 2005 | 4400 |
| 2006 | 2396 |
| 2007 | 4400 |
| 2008 | 4400 |
| 2009 | 4400 |
| 2010 | 4400 |
| 2011 | 4400 |
| 2012 | 2422 |
| 2013 | 2379 |
| 2014 | 2365 |
| 2015 | 1563 |
| 2016 | 2533 |
| 2017 | 2296 |
| 2018 | 2427 |
| 2019 | 2432 |
| 2020 | 2422 |
| 2021 | 2427 |
| 2022 | 2417 |
| 2023 | 4400 |
| 2024 | 1560 |
| 2025 | 4400 |

## First 20 Planned Downloads

| Rank | Batch | Year | Station | Plant Links | URL | Target |
| ---: | ---: | ---: | --- | ---: | --- | --- |
| 1 | 1 | 2025 | `723898-99999` | 315 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72389899999.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2025/72389899999.csv` |
| 2 | 1 | 2025 | `725100-94746` | 312 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72510094746.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2025/72510094746.csv` |
| 3 | 1 | 2025 | `722953-03183` | 309 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72295303183.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2025/72295303183.csv` |
| 4 | 1 | 2025 | `749171-00479` | 307 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/74917100479.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2025/74917100479.csv` |
| 5 | 1 | 2025 | `723898-53119` | 303 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72389853119.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2025/72389853119.csv` |
| 6 | 1 | 2025 | `723896-93144` | 302 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72389693144.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2025/72389693144.csv` |
| 7 | 1 | 2025 | `723816-03159` | 297 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72381603159.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2025/72381603159.csv` |
| 8 | 1 | 2025 | `747020-23110` | 294 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/74702023110.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2025/74702023110.csv` |
| 9 | 1 | 2025 | `744910-14703` | 293 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/74491014703.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2025/74491014703.csv` |
| 10 | 1 | 2025 | `744915-14775` | 291 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/74491514775.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2025/74491514775.csv` |
| 11 | 1 | 2025 | `723895-23149` | 290 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72389523149.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2025/72389523149.csv` |
| 12 | 1 | 2025 | `723897-99999` | 290 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72389799999.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2025/72389799999.csv` |
| 13 | 1 | 2025 | `744910-99999` | 286 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/74491099999.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2025/74491099999.csv` |
| 14 | 1 | 2025 | `723890-93193` | 284 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72389093193.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2025/72389093193.csv` |
| 15 | 1 | 2025 | `723810-99999` | 277 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72381099999.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2025/72381099999.csv` |
| 16 | 1 | 2025 | `723830-23187` | 272 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72383023187.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2025/72383023187.csv` |
| 17 | 1 | 2025 | `723810-23114` | 266 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72381023114.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2025/72381023114.csv` |
| 18 | 1 | 2025 | `725085-99999` | 263 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/72508599999.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2025/72508599999.csv` |
| 19 | 1 | 2025 | `745046-93242` | 259 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/74504693242.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2025/74504693242.csv` |
| 20 | 1 | 2025 | `745046-99999` | 251 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2025/74504699999.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2025/74504699999.csv` |

## Database Row Counts

| Relation or Check | Rows |
| --- | ---: |
| `weather.noaa_raw_backfill_manifest for this run` | 86839 |
| `planned manifest rows` | 86839 |
| `batches` | 87 |
| `batch 1 rows` | 1000 |
| `audit.source_file` | 10 |
| `audit.calculation_run` | 6 |

## Interpretation

- This is a download plan, not a download run.
- Batch 1 is intentionally limited to the first 1,000 planned files so the downloader can be tested without launching the entire backfill.
- The next step should implement or run a batch downloader that consumes this manifest and records HTTP status, bytes, hashes, and failures.
