# Station-Year DJF Coverage Report

Generated UTC: 2026-06-25T00:43:25+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `station_year_djf_coverage_20260625T002229Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `c05c4979a8a5cd380d0e3c7871869df36039ac7e`
- Year range: `2000-2025`
- Complete threshold: `0.95`

## Summary

| Relation or Check | Rows / Value |
| --- | ---: |
| `coverage rows for this run` | 62318 |
| `complete station-years` | 14161 |
| `partial station-years` | 45804 |
| `empty station-years` | 2353 |
| `valid DJF hours represented` | 50346347 |
| `rejected source rows represented` | 137976668 |

## Coverage By Year

| Year | Complete | Partial | Empty | Valid DJF Hours |
| ---: | ---: | ---: | ---: | ---: |
| 2025 | 0 | 2704 | 105 | 1261604 |
| 2024 | 426 | 2342 | 72 | 2393065 |
| 2023 | 435 | 2332 | 76 | 1896994 |
| 2022 | 568 | 2200 | 74 | 1808978 |
| 2021 | 163 | 2611 | 71 | 1922241 |
| 2020 | 522 | 2258 | 72 | 1853104 |
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
- `complete` means `coverage_ratio >= complete_threshold`; this run uses the configured threshold above.
- Coverage will change as more NOAA files are downloaded and loaded.
