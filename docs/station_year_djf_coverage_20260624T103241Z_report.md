# Station-Year DJF Coverage Report

Generated UTC: 2026-06-24T10:36:43+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `station_year_djf_coverage_20260624T103241Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `13450e7833a9a40fe011eac55bde7b0468cf5c98`
- Year range: `2000-2025`
- Complete threshold: `0.95`

## Summary

| Relation or Check | Rows / Value |
| --- | ---: |
| `coverage rows for this run` | 47470 |
| `complete station-years` | 8519 |
| `partial station-years` | 37899 |
| `empty station-years` | 1052 |
| `valid DJF hours represented` | 32351280 |
| `rejected source rows represented` | 122654964 |

## Coverage By Year

| Year | Complete | Partial | Empty | Valid DJF Hours |
| ---: | ---: | ---: | ---: | ---: |
| 2025 | 0 | 2704 | 105 | 1261604 |
| 2024 | 426 | 2342 | 72 | 2393065 |
| 2023 | 435 | 2331 | 76 | 1896281 |
| 2022 | 325 | 1623 | 35 | 1058154 |
| 2021 | 110 | 1830 | 33 | 1157948 |
| 2020 | 273 | 1672 | 33 | 1063475 |
| 2019 | 302 | 1639 | 27 | 1137972 |
| 2018 | 321 | 1626 | 26 | 1066296 |
| 2017 | 338 | 1741 | 25 | 1141502 |
| 2016 | 156 | 1705 | 6 | 830235 |
| 2015 | 432 | 2337 | 68 | 1829693 |
| 2014 | 298 | 1707 | 30 | 1238485 |
| 2013 | 437 | 1549 | 35 | 1321443 |
| 2012 | 386 | 1558 | 34 | 1238113 |
| 2011 | 719 | 2018 | 80 | 2264509 |
| 2010 | 583 | 2097 | 86 | 2012082 |
| 2009 | 545 | 1984 | 95 | 1840799 |
| 2008 | 466 | 1927 | 82 | 1640167 |
| 2007 | 733 | 1340 | 31 | 2214982 |
| 2006 | 648 | 1324 | 32 | 1989126 |
| 2005 | 586 | 845 | 41 | 1755349 |

## Interpretation

- This is station-year coverage for the currently loaded canonical DJF table, not final plant ECWT.
- `complete` means `coverage_ratio >= complete_threshold`; this run uses the configured threshold above.
- Coverage will change as more NOAA files are downloaded and loaded.
