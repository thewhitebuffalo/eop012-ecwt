# NOAA Backfill Zero-Remaining Report

Generated UTC: 2026-06-25T04:39:45Z

## Scope

- Inventory run ID: `noaa_raw_file_inventory_20260625T043845Z`
- Backfill manifest run ID: `noaa_backfill_manifest_20260625T043945Z`
- Target root: `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly`
- Additional inventory roots:
  - `/Volumes/NOAA_CACHE/noaa-global-hourly-pds-full`
  - `/Volumes/NOAA_CACHE/noaa-global-hourly-year-staging`
  - `/Volumes/NOAA_CACHE/BACKUP_TO_DELETE_LATER_noaa-cache_2026-02-19/gh_2012_2022_p1_1000`

## Result

The corrected manifest has zero planned AWS download rows.

| Metric | Count |
| --- | ---: |
| Candidate station-years in inventory | 114,400 |
| Locally available station-years | 62,318 |
| Locally missing station-years | 52,082 |
| Planned AWS backfill rows | 0 |

## Missing Station-Year Decomposition

| Active during DJF window | Prior AWS 404 recorded | Missing station-years |
| --- | --- | ---: |
| No | No | 7,735 |
| No | Yes | 41,216 |
| Yes | Yes | 3,131 |
| Yes | No | 0 |

## Interpretation

There are no remaining station-years that are all of:

- missing from the known local NOAA raw roots,
- active during the EOP-012 DJF weather window, and
- not already proven missing from the NOAA public AWS bucket.

The earlier nonzero manifest was inflated because `/Volumes/NOAA_CACHE/noaa-global-hourly-pds-full`
was not included in the inventory roots even though it had already supplied many loaded NOAA files.
Batch 2 confirmed this problem: all 1,000 downloaded files were already represented in canonical
station-hour coverage, so valid DJF coverage did not increase after loading the batch.
