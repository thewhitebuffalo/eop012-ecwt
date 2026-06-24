# Station-Year DJF Coverage Report

Generated UTC: 2026-06-24T16:20:09+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `station_year_djf_coverage_20260624T161255Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `ed0506ba184fdb7a06fb1ba7aca9489ea7b67bf1`
- Year range: `2000-2025`
- Complete threshold: `0.95`

## Summary

| Relation or Check | Rows / Value |
| --- | ---: |
| `coverage rows for this run` | 55869 |
| `complete station-years` | 12095 |
| `partial station-years` | 41702 |
| `empty station-years` | 2072 |
| `valid DJF hours represented` | 43875893 |
| `rejected source rows represented` | 126303766 |

## Coverage By Year

| Year | Complete | Partial | Empty | Valid DJF Hours |
| ---: | ---: | ---: | ---: | ---: |
| 2025 | 0 | 2704 | 105 | 1261604 |
| 2024 | 426 | 2342 | 72 | 2393065 |
| 2023 | 435 | 2331 | 76 | 1896281 |
| 2022 | 568 | 2200 | 74 | 1808978 |
| 2021 | 163 | 2611 | 71 | 1922241 |
| 2020 | 288 | 1730 | 36 | 1122290 |
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
| 2005 | 608 | 880 | 42 | 1822731 |
| 2004 | 766 | 659 | 201 | 2340405 |
| 2003 | 632 | 494 | 176 | 2074261 |
| 2002 | 665 | 441 | 246 | 1980163 |
| 2001 | 613 | 413 | 166 | 1780508 |
| 2000 | 567 | 345 | 150 | 1707962 |

## Interpretation

- This is station-year coverage for the currently loaded canonical DJF table, not final plant ECWT.
- `complete` means `coverage_ratio >= complete_threshold`; this run uses the configured threshold above.
- Coverage will change as more NOAA files are downloaded and loaded.
