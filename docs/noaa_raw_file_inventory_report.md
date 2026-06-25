# NOAA Raw File Inventory Report

Generated UTC: 2026-06-25T15:39:23+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_raw_file_inventory_20260625T153854Z`
- Candidate run ID inventoried: `noaa_station_candidates_20260625T065445Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `bd3c33c8073c2a66057773e07ae474d2b8eb9be4`

## Inventory Scope

- Candidate stations: `5152`
- Year range: `2000-2025`
- Station-year checks: `133952`
- Source file ID: `noaa_global_hourly_local_raw_inventory_1547d01933bb5668`

Configured roots, in priority order:

- `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly`
- `/Volumes/NOAA_CACHE/noaa-global-hourly-pds-full`
- `/Volumes/NOAA_CACHE/noaa-global-hourly-year-staging`
- `/Volumes/NOAA_CACHE/BACKUP_TO_DELETE_LATER_noaa-cache_2026-02-19/gh_2012_2022_p1_1000`

Previously loaded NOAA roots observed in this database:

- `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly`
- `/Volumes/NOAA_CACHE/noaa-global-hourly-pds-full`
- `/Volumes/NOAA_CACHE/noaa-global-hourly-year-staging`
- `/Volumes/NOAA_CACHE/BACKUP_TO_DELETE_LATER_noaa-cache_2026-02-19/gh_2012_2022_p1_1000`

Loaded roots auto-included in this inventory:

- `/Volumes/NOAA_CACHE/noaa-global-hourly-pds-full`
- `/Volumes/NOAA_CACHE/noaa-global-hourly-year-staging`
- `/Volumes/NOAA_CACHE/BACKUP_TO_DELETE_LATER_noaa-cache_2026-02-19/gh_2012_2022_p1_1000`

## Summary

| Metric | Count |
| --- | ---: |
| Available station-year files | 73979 |
| Missing station-year files | 59973 |
| Stations with all years available | 709 |
| Stations with at least one year available | 4936 |
| Stations with no years available | 216 |
| Total bytes for available inventoried files | 557260472927 |

## Availability By Year

| Year | Available | Missing | Year Directories Found |
| --- | ---: | ---: | ---: |
| 2000 | 1346 | 3806 | 1 |
| 2001 | 1544 | 3608 | 1 |
| 2002 | 1714 | 3438 | 1 |
| 2003 | 1674 | 3478 | 1 |
| 2004 | 2086 | 3066 | 1 |
| 2005 | 1920 | 3232 | 1 |
| 2006 | 2438 | 2714 | 2 |
| 2007 | 2535 | 2617 | 1 |
| 2008 | 2950 | 2202 | 1 |
| 2009 | 3111 | 2041 | 1 |
| 2010 | 3269 | 1883 | 1 |
| 2011 | 3326 | 1826 | 1 |
| 2012 | 3335 | 1817 | 3 |
| 2013 | 3385 | 1767 | 3 |
| 2014 | 3344 | 1808 | 3 |
| 2015 | 3341 | 1811 | 3 |
| 2016 | 2928 | 2224 | 3 |
| 2017 | 3331 | 1821 | 3 |
| 2018 | 3337 | 1815 | 3 |
| 2019 | 3319 | 1833 | 3 |
| 2020 | 3331 | 1821 | 3 |
| 2021 | 3317 | 1835 | 3 |
| 2022 | 3303 | 1849 | 3 |
| 2023 | 3301 | 1851 | 1 |
| 2024 | 3281 | 1871 | 2 |
| 2025 | 3213 | 1939 | 1 |

## Availability By Root

| Root | Station-Year Files Used |
| --- | ---: |
| `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly` | 47039 |
| `/Volumes/NOAA_CACHE/noaa-global-hourly-pds-full` | 22943 |
| `/Volumes/NOAA_CACHE/noaa-global-hourly-year-staging` | 3281 |
| `/Volumes/NOAA_CACHE/BACKUP_TO_DELETE_LATER_noaa-cache_2026-02-19/gh_2012_2022_p1_1000` | 716 |

## Database Row Counts

| Relation or Check | Rows |
| --- | ---: |
| `weather.noaa_raw_file_inventory for this run` | 133952 |
| `available station-year files` | 73979 |
| `missing station-year files` | 59973 |
| `audit.source_file` | 72633 |
| `audit.calculation_run` | 571 |
| `audit.exception_log` | 559 |

## Interpretation

- This inventory checks local raw NOAA station-year file presence only; it does not parse hourly observations yet.
- Missing years or missing station files must be downloaded before a compliance-grade full hourly rebuild can be complete.
- The next parser step should process available station-year CSV files into a normalized hourly DJF staging table and produce raw missing, duplicate, and invalid-temperature counts.
