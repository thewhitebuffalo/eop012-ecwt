# NOAA Backfill Manifest Report

Generated UTC: 2026-06-25T02:38:59+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_manifest_20260625T023857Z`
- Source inventory run ID: `noaa_raw_file_inventory_20260625T023833Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `5459c3331356c83dfeb2b7299a271a50da74d9d3`
- Source file ID: `noaa_global_hourly_backfill_manifest_d07d8caa7a62d5f8`

## Manifest Scope

- Download base URL: `https://noaa-global-hourly-pds.s3.amazonaws.com/`
- Target root: `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly`
- Manifest rows: `19811`
- Batch size: `1000`
- Batch count: `20`
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
| 2006 | 1999 |
| 2012 | 1176 |
| 2013 | 1203 |
| 2014 | 1211 |
| 2015 | 1998 |
| 2016 | 1123 |
| 2017 | 1258 |
| 2018 | 1941 |
| 2019 | 1968 |
| 2020 | 1978 |
| 2021 | 1973 |
| 2022 | 1983 |

## First 20 Planned Downloads

| Rank | Batch | Year | Station | Plant Links | URL | Target |
| ---: | ---: | ---: | --- | ---: | --- | --- |
| 1 | 1 | 2006 | `725100-94746` | 312 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72510094746.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2006/72510094746.csv` |
| 2 | 1 | 2006 | `722953-03183` | 309 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72295303183.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2006/72295303183.csv` |
| 3 | 1 | 2006 | `723898-53119` | 303 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72389853119.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2006/72389853119.csv` |
| 4 | 1 | 2006 | `723896-93144` | 302 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72389693144.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2006/72389693144.csv` |
| 5 | 1 | 2006 | `723816-03159` | 297 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72381603159.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2006/72381603159.csv` |
| 6 | 1 | 2006 | `747020-23110` | 294 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/74702023110.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2006/74702023110.csv` |
| 7 | 1 | 2006 | `744910-14703` | 293 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/74491014703.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2006/74491014703.csv` |
| 8 | 1 | 2006 | `744915-14775` | 291 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/74491514775.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2006/74491514775.csv` |
| 9 | 1 | 2006 | `723895-23149` | 290 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72389523149.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2006/72389523149.csv` |
| 10 | 1 | 2006 | `723890-93193` | 284 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72389093193.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2006/72389093193.csv` |
| 11 | 1 | 2006 | `723830-23187` | 272 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72383023187.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2006/72383023187.csv` |
| 12 | 1 | 2006 | `723810-23114` | 266 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72381023114.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2006/72381023114.csv` |
| 13 | 1 | 2006 | `745046-93242` | 259 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/74504693242.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2006/74504693242.csv` |
| 14 | 1 | 2006 | `723171-53144` | 250 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72317153144.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2006/72317153144.csv` |
| 15 | 1 | 2006 | `725085-54756` | 248 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72508554756.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2006/72508554756.csv` |
| 16 | 1 | 2006 | `725075-54768` | 246 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72507554768.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2006/72507554768.csv` |
| 17 | 1 | 2006 | `723820-23182` | 233 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72382023182.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2006/72382023182.csv` |
| 18 | 1 | 2006 | `723840-23155` | 233 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72384023155.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2006/72384023155.csv` |
| 19 | 1 | 2006 | `725180-14735` | 231 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72518014735.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2006/72518014735.csv` |
| 20 | 1 | 2006 | `725190-14771` | 230 | `https://noaa-global-hourly-pds.s3.amazonaws.com/2006/72519014771.csv` | `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly/2006/72519014771.csv` |

## Database Row Counts

| Relation or Check | Rows |
| --- | ---: |
| `weather.noaa_raw_backfill_manifest for this run` | 19811 |
| `planned manifest rows` | 19811 |
| `batches` | 20 |
| `batch 1 rows` | 1000 |
| `audit.source_file` | 62330 |
| `audit.calculation_run` | 461 |

## Interpretation

- This is a download plan, not a download run.
- Batch 1 is intentionally limited to the first 1,000 planned files so the downloader can be tested without launching the entire backfill.
- The next step should implement or run a batch downloader that consumes this manifest and records HTTP status, bytes, hashes, and failures.
