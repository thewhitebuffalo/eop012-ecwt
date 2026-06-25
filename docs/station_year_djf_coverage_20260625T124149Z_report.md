# Station-Year DJF Coverage Report

Generated UTC: 2026-06-25T12:42:04+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `station_year_djf_coverage_20260625T124149Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `41478111915114cd79294d0261f5b9fb6f936f5b`
- Year range: `2000-2025`
- Complete threshold: `0.95`
- Snapshot mode: `current`
- Coverage table: `weather.station_year_djf_coverage_current`

## Summary

| Relation or Check | Rows / Value |
| --- | ---: |
| `coverage rows for this run` | 72623 |
| `complete station-years` | 18795 |
| `partial station-years` | 51014 |
| `empty station-years` | 2814 |
| `valid DJF hours represented` | 65178134 |
| `rejected source rows represented` | 143195268 |

## Coverage By Year

| Year | Complete | Partial | Empty | Valid DJF Hours |
| ---: | ---: | ---: | ---: | ---: |
| 2025 | 0 | 3092 | 121 | 1711201 |
| 2024 | 434 | 2342 | 72 | 2410198 |
| 2023 | 687 | 2512 | 102 | 2622751 |
| 2022 | 825 | 2384 | 94 | 2531119 |
| 2021 | 196 | 3033 | 88 | 2623223 |
| 2020 | 787 | 2451 | 93 | 2600907 |
| 2019 | 847 | 2398 | 74 | 2710864 |
| 2018 | 856 | 2387 | 94 | 2604392 |
| 2017 | 858 | 2386 | 87 | 2621658 |
| 2016 | 580 | 2325 | 23 | 2082212 |
| 2015 | 439 | 2338 | 68 | 1846770 |
| 2014 | 805 | 2446 | 93 | 2877657 |
| 2013 | 1032 | 2253 | 100 | 3085782 |
| 2012 | 1011 | 2223 | 101 | 2998313 |
| 2011 | 979 | 2233 | 114 | 3000379 |
| 2010 | 835 | 2324 | 110 | 2741590 |
| 2009 | 793 | 2205 | 113 | 2541524 |
| 2008 | 709 | 2144 | 97 | 2342963 |
| 2007 | 958 | 1528 | 49 | 2877967 |
| 2006 | 653 | 1326 | 32 | 2002938 |
| 2005 | 767 | 1099 | 54 | 2324939 |
| 2004 | 907 | 946 | 233 | 2845381 |
| 2003 | 696 | 782 | 196 | 2508327 |
| 2002 | 738 | 711 | 265 | 2403929 |
| 2001 | 727 | 635 | 182 | 2179889 |
| 2000 | 676 | 511 | 159 | 2081261 |

## Interpretation

- This is station-year coverage for the currently loaded canonical DJF table, not final plant ECWT.
- Valid-hour counts are read from `weather.station_year_hourly_summary`, which is maintained by the NOAA DJF loader and can be backfilled from `weather.hourly_djf` for existing rows.
- `current` snapshot mode replaces the compact operational coverage table; `historical` mode appends a milestone snapshot to the full audit table.
- `complete` means `coverage_ratio >= complete_threshold`; this run uses the configured threshold above.
- Coverage will change as more NOAA files are downloaded and loaded.
