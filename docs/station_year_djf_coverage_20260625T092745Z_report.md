# Station-Year DJF Coverage Report

Generated UTC: 2026-06-25T09:27:53+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `station_year_djf_coverage_20260625T092745Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `2b09d4f02c9280bc9bed41c41390e1131e7a8a32`
- Year range: `2000-2025`
- Complete threshold: `0.95`
- Snapshot mode: `current`
- Coverage table: `weather.station_year_djf_coverage_current`

## Summary

| Relation or Check | Rows / Value |
| --- | ---: |
| `coverage rows for this run` | 64293 |
| `complete station-years` | 14791 |
| `partial station-years` | 47056 |
| `empty station-years` | 2446 |
| `valid DJF hours represented` | 53192557 |
| `rejected source rows represented` | 142016030 |

## Coverage By Year

| Year | Complete | Partial | Empty | Valid DJF Hours |
| ---: | ---: | ---: | ---: | ---: |
| 2025 | 0 | 3092 | 121 | 1711201 |
| 2024 | 426 | 2342 | 72 | 2393065 |
| 2023 | 687 | 2512 | 102 | 2622751 |
| 2022 | 825 | 2384 | 94 | 2531119 |
| 2021 | 196 | 3033 | 88 | 2623223 |
| 2020 | 610 | 2336 | 86 | 2100837 |
| 2019 | 573 | 2216 | 57 | 1960143 |
| 2018 | 581 | 2203 | 66 | 1850073 |
| 2017 | 577 | 2208 | 63 | 1857478 |
| 2016 | 300 | 2138 | 18 | 1334345 |
| 2015 | 432 | 2337 | 68 | 1829693 |
| 2014 | 527 | 2258 | 72 | 2114926 |
| 2013 | 766 | 2047 | 79 | 2331271 |
| 2012 | 745 | 2025 | 73 | 2260433 |
| 2011 | 719 | 2018 | 80 | 2264509 |
| 2010 | 583 | 2097 | 86 | 2012082 |
| 2009 | 545 | 1984 | 95 | 1840799 |
| 2008 | 466 | 1929 | 82 | 1641711 |
| 2007 | 734 | 1341 | 31 | 2217742 |
| 2006 | 648 | 1324 | 32 | 1989126 |
| 2005 | 608 | 880 | 42 | 1822731 |
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
