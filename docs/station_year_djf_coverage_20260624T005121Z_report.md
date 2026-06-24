# Station-Year DJF Coverage Report

Generated UTC: 2026-06-24T00:52:22+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `station_year_djf_coverage_20260624T005121Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `cb6b00bc1d7017e560a767ff99318b25c87ddfb6`
- Year range: `2000-2025`
- Complete threshold: `0.95`

## Summary

| Relation or Check | Rows / Value |
| --- | ---: |
| `coverage rows for this run` | 13000 |
| `complete station-years` | 1427 |
| `partial station-years` | 11269 |
| `empty station-years` | 304 |
| `valid DJF hours represented` | 7940480 |
| `rejected source rows represented` | 32678615 |

## Coverage By Year

| Year | Complete | Partial | Empty | Valid DJF Hours |
| ---: | ---: | ---: | ---: | ---: |
| 2025 | 0 | 2704 | 105 | 1261604 |
| 2024 | 426 | 2342 | 72 | 2393065 |
| 2023 | 435 | 2331 | 76 | 1896281 |
| 2022 | 325 | 1623 | 35 | 1058154 |
| 2021 | 7 | 1164 | 6 | 461568 |
| 2011 | 234 | 1105 | 10 | 869808 |

## Interpretation

- This is station-year coverage for the currently loaded canonical DJF table, not final plant ECWT.
- `complete` means `coverage_ratio >= complete_threshold`; this run uses the configured threshold above.
- Coverage will change as more NOAA files are downloaded and loaded.
