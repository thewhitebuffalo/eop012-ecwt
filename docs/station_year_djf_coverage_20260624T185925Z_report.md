# Station-Year DJF Coverage Report

Generated UTC: 2026-06-24T19:15:29+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `station_year_djf_coverage_20260624T185925Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `1c36bdf53ca8b7619d743a34a54d4a3f8f12931a`
- Year range: `2000-2025`
- Complete threshold: `0.95`

## Summary

| Relation or Check | Rows / Value |
| --- | ---: |
| `coverage rows for this run` | 60926 |
| `complete station-years` | 13593 |
| `partial station-years` | 45049 |
| `empty station-years` | 2284 |
| `valid DJF hours represented` | 48681345 |
| `rejected source rows represented` | 136271677 |

## Coverage By Year

| Year | Complete | Partial | Empty | Valid DJF Hours |
| ---: | ---: | ---: | ---: | ---: |
| 2025 | 0 | 2704 | 105 | 1261604 |
| 2024 | 426 | 2342 | 72 | 2393065 |
| 2023 | 435 | 2331 | 76 | 1896281 |
| 2022 | 568 | 2200 | 74 | 1808978 |
| 2021 | 163 | 2611 | 71 | 1922241 |
| 2020 | 522 | 2258 | 72 | 1853104 |
| 2019 | 573 | 2216 | 57 | 1960143 |
| 2018 | 581 | 2203 | 66 | 1850073 |
| 2017 | 577 | 2208 | 63 | 1857478 |
| 2016 | 300 | 2138 | 18 | 1334345 |
| 2015 | 432 | 2337 | 68 | 1829693 |
| 2014 | 527 | 2258 | 72 | 2114926 |
| 2013 | 558 | 1763 | 49 | 1693606 |
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
