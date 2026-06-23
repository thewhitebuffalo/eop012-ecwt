# NOAA Raw File Inventory Report

Generated UTC: 2026-06-23T21:34:51+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_raw_file_inventory_20260623T213439Z`
- Candidate run ID inventoried: `noaa_station_candidates_20260623T210132Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `6b12c8cdfbb6725fc82a145ff3a9e3621ac0575c`

## Inventory Scope

- Candidate stations: `4400`
- Year range: `2000-2025`
- Station-year checks: `114400`
- Source file ID: `noaa_global_hourly_local_raw_inventory_3e447b31e3e36679`

Configured roots, in priority order:

- `/Volumes/NOAA_CACHE/noaa-global-hourly-pds-full`
- `/Volumes/NOAA_CACHE/noaa-global-hourly-year-staging`
- `/Volumes/NOAA_CACHE/noaa-global-hourly-unified`
- `/Volumes/NOAA_CACHE/BACKUP_TO_DELETE_LATER_noaa-cache_2026-02-19`

## Summary

| Metric | Count |
| --- | ---: |
| Available station-year files | 27561 |
| Missing station-year files | 86839 |
| Stations with all years available | 0 |
| Stations with at least one year available | 3052 |
| Stations with no years available | 1348 |
| Total bytes for available inventoried files | 254790570660 |

## Availability By Year

| Year | Available | Missing | Year Directories Found |
| --- | ---: | ---: | ---: |
| 2000 | 0 | 4400 | 0 |
| 2001 | 0 | 4400 | 0 |
| 2002 | 0 | 4400 | 0 |
| 2003 | 0 | 4400 | 0 |
| 2004 | 0 | 4400 | 0 |
| 2005 | 0 | 4400 | 0 |
| 2006 | 2004 | 2396 | 1 |
| 2007 | 0 | 4400 | 0 |
| 2008 | 0 | 4400 | 0 |
| 2009 | 0 | 4400 | 0 |
| 2010 | 0 | 4400 | 0 |
| 2011 | 0 | 4400 | 0 |
| 2012 | 1978 | 2422 | 4 |
| 2013 | 2021 | 2379 | 4 |
| 2014 | 2035 | 2365 | 4 |
| 2015 | 2837 | 1563 | 4 |
| 2016 | 1867 | 2533 | 4 |
| 2017 | 2104 | 2296 | 4 |
| 2018 | 1973 | 2427 | 4 |
| 2019 | 1968 | 2432 | 4 |
| 2020 | 1978 | 2422 | 4 |
| 2021 | 1973 | 2427 | 4 |
| 2022 | 1983 | 2417 | 4 |
| 2023 | 0 | 4400 | 0 |
| 2024 | 2840 | 1560 | 1 |
| 2025 | 0 | 4400 | 0 |

## Availability By Root

| Root | Station-Year Files Used |
| --- | ---: |
| `/Volumes/NOAA_CACHE/noaa-global-hourly-pds-full` | 24005 |
| `/Volumes/NOAA_CACHE/noaa-global-hourly-year-staging` | 2840 |
| `/Volumes/NOAA_CACHE/BACKUP_TO_DELETE_LATER_noaa-cache_2026-02-19` | 716 |

## Database Row Counts

| Relation or Check | Rows |
| --- | ---: |
| `weather.noaa_raw_file_inventory for this run` | 114400 |
| `available station-year files` | 27561 |
| `missing station-year files` | 86839 |
| `audit.source_file` | 8 |
| `audit.calculation_run` | 4 |
| `audit.exception_log` | 398 |

## Interpretation

- This inventory checks local raw NOAA station-year file presence only; it does not parse hourly observations yet.
- Missing years or missing station files must be downloaded before a compliance-grade full hourly rebuild can be complete.
- The next parser step should process available station-year CSV files into a normalized hourly DJF staging table and produce raw missing, duplicate, and invalid-temperature counts.
