# NOAA Backfill Manifest Report

Generated UTC: 2026-06-25T04:39:46+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_backfill_manifest_20260625T043945Z`
- Source inventory run ID: `noaa_raw_file_inventory_20260625T043845Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `5503ab1066d72b419ee1d304290326c19309827a`
- Source file ID: `noaa_global_hourly_backfill_manifest_d07d8caa7a62d5f8`

## Manifest Scope

- Download base URL: `https://noaa-global-hourly-pds.s3.amazonaws.com/`
- Target root: `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly`
- Manifest rows: `0`
- Batch size: `1000`
- Batch count: `0`
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

## First 20 Planned Downloads

| Rank | Batch | Year | Station | Plant Links | URL | Target |
| ---: | ---: | ---: | --- | ---: | --- | --- |

## Database Row Counts

| Relation or Check | Rows |
| --- | ---: |
| `weather.noaa_raw_backfill_manifest for this run` | 0 |
| `planned manifest rows` | 0 |
| `batches` | 0 |
| `batch 1 rows` | 0 |
| `audit.source_file` | 62331 |
| `audit.calculation_run` | 481 |

## Interpretation

- This is a download plan, not a download run.
- This manifest has zero planned rows.
- Under the configured roots, DJF active-window filter, and known terminal AWS 404 exclusion, there are no remaining AWS download candidates.
