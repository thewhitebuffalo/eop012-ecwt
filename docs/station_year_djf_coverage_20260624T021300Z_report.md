# Station-Year DJF Coverage Report

Generated UTC: 2026-06-24T02:16:41+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `station_year_djf_coverage_20260624T021300Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `ec4f3e306097d39440575bdb79e8cabc99498898`
- Year range: `2000-2025`
- Complete threshold: `0.95`

## Summary

| Relation or Check | Rows / Value |
| --- | ---: |
| `coverage rows for this run` | 19000 |
| `complete station-years` | 2472 |
| `partial station-years` | 16076 |
| `empty station-years` | 452 |
| `valid DJF hours represented` | 11922371 |
| `rejected source rows represented` | 49097717 |

## Coverage By Year

| Year | Complete | Partial | Empty | Valid DJF Hours |
| ---: | ---: | ---: | ---: | ---: |
| 2025 | 0 | 2704 | 105 | 1261604 |
| 2024 | 426 | 2342 | 72 | 2393065 |
| 2023 | 435 | 2331 | 76 | 1896281 |
| 2022 | 325 | 1623 | 35 | 1058154 |
| 2021 | 110 | 1830 | 33 | 1157948 |
| 2020 | 273 | 1672 | 33 | 1063476 |
| 2019 | 25 | 199 | 2 | 114511 |
| 2011 | 719 | 2018 | 80 | 2264509 |
| 2010 | 159 | 1357 | 16 | 712823 |

## Interpretation

- This is station-year coverage for the currently loaded canonical DJF table, not final plant ECWT.
- `complete` means `coverage_ratio >= complete_threshold`; this run uses the configured threshold above.
- Coverage will change as more NOAA files are downloaded and loaded.
