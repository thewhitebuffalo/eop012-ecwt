# Station-Year DJF Coverage Report

Generated UTC: 2026-06-25T11:32:42+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `station_year_djf_coverage_20260625T113234Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `66fc6f9cc20081a97c9ab607de0fa2c787c57987`
- Year range: `2000-2025`
- Complete threshold: `0.95`
- Snapshot mode: `current`
- Coverage table: `weather.station_year_djf_coverage_current`

## Summary

| Relation or Check | Rows / Value |
| --- | ---: |
| `coverage rows for this run` | 70516 |
| `complete station-years` | 18172 |
| `partial station-years` | 49632 |
| `empty station-years` | 2712 |
| `valid DJF hours represented` | 62672609 |
| `rejected source rows represented` | 143188798 |

## Coverage By Year

| Year | Complete | Partial | Empty | Valid DJF Hours |
| ---: | ---: | ---: | ---: | ---: |
| 2025 | 0 | 3092 | 121 | 1711201 |
| 2024 | 426 | 2342 | 72 | 2393065 |
| 2023 | 687 | 2512 | 102 | 2622751 |
| 2022 | 825 | 2384 | 94 | 2531119 |
| 2021 | 196 | 3033 | 88 | 2623223 |
| 2020 | 787 | 2451 | 93 | 2600907 |
| 2019 | 847 | 2398 | 74 | 2710864 |
| 2018 | 856 | 2387 | 94 | 2604392 |
| 2017 | 858 | 2386 | 87 | 2621658 |
| 2016 | 580 | 2325 | 23 | 2082212 |
| 2015 | 432 | 2337 | 68 | 1829693 |
| 2014 | 805 | 2446 | 93 | 2877657 |
| 2013 | 1032 | 2253 | 100 | 3085782 |
| 2012 | 1011 | 2223 | 101 | 2998313 |
| 2011 | 979 | 2233 | 114 | 3000379 |
| 2010 | 835 | 2324 | 110 | 2741590 |
| 2009 | 793 | 2205 | 113 | 2541524 |
| 2008 | 709 | 2144 | 97 | 2342963 |
| 2007 | 958 | 1528 | 49 | 2877967 |
| 2006 | 648 | 1324 | 32 | 1989126 |
| 2005 | 665 | 953 | 48 | 2002924 |
| 2004 | 766 | 659 | 201 | 2340405 |
| 2003 | 632 | 494 | 176 | 2074261 |
| 2002 | 665 | 441 | 246 | 1980163 |
| 2001 | 613 | 413 | 166 | 1780508 |
| 2000 | 567 | 345 | 150 | 1707962 |

## Interpretation

- This is station-year coverage for the currently loaded canonical DJF table, not final plant ECWT.
- Valid-hour counts are read from `weather.station_year_hourly_summary`, which is maintained by the NOAA DJF loader and can be backfilled from `weather.hourly_djf` for existing rows.
- `current` snapshot mode replaces the compact operational coverage table; `historical` mode appends a milestone snapshot to the full audit table.
- `complete` means `coverage_ratio >= complete_threshold`; this run uses the configured threshold above.
- Coverage will change as more NOAA files are downloaded and loaded.
