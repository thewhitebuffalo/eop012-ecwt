# Station-Year DJF Coverage Report

Generated UTC: 2026-06-24T07:15:24+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `station_year_djf_coverage_20260624T071037Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `26b8fe67506d2ffc156a91dffd8029ebe333eb9c`
- Year range: `2000-2025`
- Complete threshold: `0.95`

## Summary

| Relation or Check | Rows / Value |
| --- | ---: |
| `coverage rows for this run` | 36668 |
| `complete station-years` | 5551 |
| `partial station-years` | 30263 |
| `empty station-years` | 854 |
| `valid DJF hours represented` | 23194562 |
| `rejected source rows represented` | 98611468 |

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
| 2014 | 14 | 463 | 0 | 301691 |
| 2011 | 719 | 2018 | 80 | 2264509 |
| 2010 | 583 | 2097 | 86 | 2012082 |
| 2009 | 545 | 1984 | 95 | 1840799 |
| 2008 | 466 | 1927 | 82 | 1640167 |
| 2007 | 106 | 224 | 5 | 299089 |

## Interpretation

- This is station-year coverage for the currently loaded canonical DJF table, not final plant ECWT.
- `complete` means `coverage_ratio >= complete_threshold`; this run uses the configured threshold above.
- Coverage will change as more NOAA files are downloaded and loaded.
