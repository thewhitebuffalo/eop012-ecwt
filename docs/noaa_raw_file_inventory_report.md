# NOAA Raw File Inventory Report

Generated UTC: 2026-06-25T04:39:08+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_raw_file_inventory_20260625T043845Z`
- Candidate run ID inventoried: `noaa_station_candidates_20260623T210132Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `5503ab1066d72b419ee1d304290326c19309827a`

## Inventory Scope

- Candidate stations: `4400`
- Year range: `2000-2025`
- Station-year checks: `114400`
- Source file ID: `noaa_global_hourly_local_raw_inventory_1547d01933bb5668`

Configured roots, in priority order:

- `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly`
- `/Volumes/NOAA_CACHE/noaa-global-hourly-pds-full`
- `/Volumes/NOAA_CACHE/noaa-global-hourly-year-staging`
- `/Volumes/NOAA_CACHE/BACKUP_TO_DELETE_LATER_noaa-cache_2026-02-19/gh_2012_2022_p1_1000`

## Summary

| Metric | Count |
| --- | ---: |
| Available station-year files | 62318 |
| Missing station-year files | 52082 |
| Stations with all years available | 546 |
| Stations with at least one year available | 4250 |
| Stations with no years available | 150 |
| Total bytes for available inventoried files | 520224904668 |

## Availability By Year

| Year | Available | Missing | Year Directories Found |
| --- | ---: | ---: | ---: |
| 2000 | 1062 | 3338 | 1 |
| 2001 | 1192 | 3208 | 1 |
| 2002 | 1352 | 3048 | 1 |
| 2003 | 1302 | 3098 | 1 |
| 2004 | 1626 | 2774 | 1 |
| 2005 | 1530 | 2870 | 1 |
| 2006 | 2004 | 2396 | 2 |
| 2007 | 2106 | 2294 | 1 |
| 2008 | 2477 | 1923 | 1 |
| 2009 | 2624 | 1776 | 1 |
| 2010 | 2766 | 1634 | 1 |
| 2011 | 2817 | 1583 | 1 |
| 2012 | 2843 | 1557 | 3 |
| 2013 | 2892 | 1508 | 3 |
| 2014 | 2857 | 1543 | 3 |
| 2015 | 2837 | 1563 | 3 |
| 2016 | 2456 | 1944 | 3 |
| 2017 | 2848 | 1552 | 3 |
| 2018 | 2850 | 1550 | 3 |
| 2019 | 2846 | 1554 | 3 |
| 2020 | 2852 | 1548 | 3 |
| 2021 | 2845 | 1555 | 3 |
| 2022 | 2842 | 1558 | 3 |
| 2023 | 2843 | 1557 | 1 |
| 2024 | 2840 | 1560 | 2 |
| 2025 | 2809 | 1591 | 1 |

## Availability By Root

| Root | Station-Year Files Used |
| --- | ---: |
| `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly` | 36756 |
| `/Volumes/NOAA_CACHE/noaa-global-hourly-pds-full` | 22006 |
| `/Volumes/NOAA_CACHE/noaa-global-hourly-year-staging` | 2840 |
| `/Volumes/NOAA_CACHE/BACKUP_TO_DELETE_LATER_noaa-cache_2026-02-19/gh_2012_2022_p1_1000` | 716 |

## Database Row Counts

| Relation or Check | Rows |
| --- | ---: |
| `weather.noaa_raw_file_inventory for this run` | 114400 |
| `available station-year files` | 62318 |
| `missing station-year files` | 52082 |
| `audit.source_file` | 62331 |
| `audit.calculation_run` | 480 |
| `audit.exception_log` | 507 |

## Interpretation

- This inventory checks local raw NOAA station-year file presence only; it does not parse hourly observations yet.
- Missing years or missing station files must be downloaded before a compliance-grade full hourly rebuild can be complete.
- The next parser step should process available station-year CSV files into a normalized hourly DJF staging table and produce raw missing, duplicate, and invalid-temperature counts.
