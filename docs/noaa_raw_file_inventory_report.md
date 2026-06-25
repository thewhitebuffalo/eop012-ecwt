# NOAA Raw File Inventory Report

Generated UTC: 2026-06-25T02:38:44+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_raw_file_inventory_20260625T023833Z`
- Candidate run ID inventoried: `noaa_station_candidates_20260623T210132Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `5459c3331356c83dfeb2b7299a271a50da74d9d3`

## Inventory Scope

- Candidate stations: `4400`
- Year range: `2000-2025`
- Station-year checks: `114400`
- Source file ID: `noaa_global_hourly_local_raw_inventory_eb0ddadee8a77f36`

Configured roots, in priority order:

- `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly`
- `/Volumes/NOAA_CACHE/noaa-global-hourly-year-staging`
- `/Volumes/NOAA_CACHE/BACKUP_TO_DELETE_LATER_noaa-cache_2026-02-19/gh_2012_2022_p1_1000`

## Summary

| Metric | Count |
| --- | ---: |
| Available station-year files | 42502 |
| Missing station-year files | 71898 |
| Stations with all years available | 0 |
| Stations with at least one year available | 4243 |
| Stations with no years available | 157 |
| Total bytes for available inventoried files | 336352476052 |

## Availability By Year

| Year | Available | Missing | Year Directories Found |
| --- | ---: | ---: | ---: |
| 2000 | 1062 | 3338 | 1 |
| 2001 | 1192 | 3208 | 1 |
| 2002 | 1352 | 3048 | 1 |
| 2003 | 1302 | 3098 | 1 |
| 2004 | 1626 | 2774 | 1 |
| 2005 | 1530 | 2870 | 1 |
| 2006 | 0 | 4400 | 1 |
| 2007 | 2106 | 2294 | 1 |
| 2008 | 2477 | 1923 | 1 |
| 2009 | 2624 | 1776 | 1 |
| 2010 | 2766 | 1634 | 1 |
| 2011 | 2817 | 1583 | 1 |
| 2012 | 1667 | 2733 | 2 |
| 2013 | 1689 | 2711 | 2 |
| 2014 | 1646 | 2754 | 2 |
| 2015 | 839 | 3561 | 2 |
| 2016 | 1333 | 3067 | 2 |
| 2017 | 1590 | 2810 | 2 |
| 2018 | 909 | 3491 | 2 |
| 2019 | 878 | 3522 | 2 |
| 2020 | 874 | 3526 | 2 |
| 2021 | 872 | 3528 | 2 |
| 2022 | 859 | 3541 | 2 |
| 2023 | 2843 | 1557 | 1 |
| 2024 | 2840 | 1560 | 2 |
| 2025 | 2809 | 1591 | 1 |

## Availability By Root

| Root | Station-Year Files Used |
| --- | ---: |
| `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly` | 34757 |
| `/Volumes/NOAA_CACHE/BACKUP_TO_DELETE_LATER_noaa-cache_2026-02-19/gh_2012_2022_p1_1000` | 4905 |
| `/Volumes/NOAA_CACHE/noaa-global-hourly-year-staging` | 2840 |

## Database Row Counts

| Relation or Check | Rows |
| --- | ---: |
| `weather.noaa_raw_file_inventory for this run` | 114400 |
| `available station-year files` | 42502 |
| `missing station-year files` | 71898 |
| `audit.source_file` | 62330 |
| `audit.calculation_run` | 460 |
| `audit.exception_log` | 481 |

## Interpretation

- This inventory checks local raw NOAA station-year file presence only; it does not parse hourly observations yet.
- Missing years or missing station files must be downloaded before a compliance-grade full hourly rebuild can be complete.
- The next parser step should process available station-year CSV files into a normalized hourly DJF staging table and produce raw missing, duplicate, and invalid-temperature counts.
