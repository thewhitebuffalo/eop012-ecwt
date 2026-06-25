# NOAA Raw File Inventory Report

Generated UTC: 2026-06-25T07:08:44+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_raw_file_inventory_20260625T070816Z`
- Candidate run ID inventoried: `noaa_station_candidates_20260625T065445Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `2dcc1f5022ae8ae59ac10305789e6c47d0871913`

## Inventory Scope

- Candidate stations: `5152`
- Year range: `2000-2025`
- Station-year checks: `133952`
- Source file ID: `noaa_global_hourly_local_raw_inventory_facf644b90b8e3a1`

Configured roots, in priority order:

- `/Users/whitebuffalo/eop012_data/raw/noaa/global-hourly`
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

- `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly`
- `/Volumes/NOAA_CACHE/noaa-global-hourly-pds-full`
- `/Volumes/NOAA_CACHE/noaa-global-hourly-year-staging`
- `/Volumes/NOAA_CACHE/BACKUP_TO_DELETE_LATER_noaa-cache_2026-02-19/gh_2012_2022_p1_1000`

## Summary

| Metric | Count |
| --- | ---: |
| Available station-year files | 63697 |
| Missing station-year files | 70255 |
| Stations with all years available | 546 |
| Stations with at least one year available | 4806 |
| Stations with no years available | 346 |
| Total bytes for available inventoried files | 524879179334 |

## Availability By Year

| Year | Available | Missing | Year Directories Found |
| --- | ---: | ---: | ---: |
| 2000 | 1062 | 4090 | 1 |
| 2001 | 1192 | 3960 | 1 |
| 2002 | 1352 | 3800 | 1 |
| 2003 | 1302 | 3850 | 1 |
| 2004 | 1626 | 3526 | 1 |
| 2005 | 1530 | 3622 | 1 |
| 2006 | 2438 | 2714 | 2 |
| 2007 | 2106 | 3046 | 1 |
| 2008 | 2477 | 2675 | 1 |
| 2009 | 2624 | 2528 | 1 |
| 2010 | 2766 | 2386 | 1 |
| 2011 | 2817 | 2335 | 1 |
| 2012 | 2843 | 2309 | 3 |
| 2013 | 2892 | 2260 | 3 |
| 2014 | 2857 | 2295 | 3 |
| 2015 | 3341 | 1811 | 3 |
| 2016 | 2456 | 2696 | 3 |
| 2017 | 2848 | 2304 | 3 |
| 2018 | 2850 | 2302 | 3 |
| 2019 | 2846 | 2306 | 3 |
| 2020 | 2852 | 2300 | 3 |
| 2021 | 2845 | 2307 | 3 |
| 2022 | 2842 | 2310 | 3 |
| 2023 | 2843 | 2309 | 1 |
| 2024 | 3281 | 1871 | 2 |
| 2025 | 2809 | 2343 | 1 |

## Availability By Root

| Root | Station-Year Files Used |
| --- | ---: |
| `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly` | 36756 |
| `/Volumes/NOAA_CACHE/noaa-global-hourly-pds-full` | 22944 |
| `/Volumes/NOAA_CACHE/noaa-global-hourly-year-staging` | 3281 |
| `/Volumes/NOAA_CACHE/BACKUP_TO_DELETE_LATER_noaa-cache_2026-02-19/gh_2012_2022_p1_1000` | 716 |

## Database Row Counts

| Relation or Check | Rows |
| --- | ---: |
| `weather.noaa_raw_file_inventory for this run` | 133952 |
| `available station-year files` | 63697 |
| `missing station-year files` | 70255 |
| `audit.source_file` | 62335 |
| `audit.calculation_run` | 494 |
| `audit.exception_log` | 533 |

## Interpretation

- This inventory checks local raw NOAA station-year file presence only; it does not parse hourly observations yet.
- Missing years or missing station files must be downloaded before a compliance-grade full hourly rebuild can be complete.
- The next parser step should process available station-year CSV files into a normalized hourly DJF staging table and produce raw missing, duplicate, and invalid-temperature counts.
