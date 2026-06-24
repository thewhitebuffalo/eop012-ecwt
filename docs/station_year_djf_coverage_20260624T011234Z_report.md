# Station-Year DJF Coverage Report

Generated UTC: 2026-06-24T01:13:44+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `station_year_djf_coverage_20260624T011234Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `2aa504b0a1dcc760d1462915d0cf12cb819b220d`
- Year range: `2000-2025`
- Complete threshold: `0.95`

## Summary

| Relation or Check | Rows / Value |
| --- | ---: |
| `coverage rows for this run` | 15000 |
| `complete station-years` | 1703 |
| `partial station-years` | 12945 |
| `empty station-years` | 352 |
| `valid DJF hours represented` | 9291323 |
| `rejected source rows represented` | 38059452 |

## Coverage By Year

| Year | Complete | Partial | Empty | Valid DJF Hours |
| ---: | ---: | ---: | ---: | ---: |
| 2025 | 0 | 2704 | 105 | 1261604 |
| 2024 | 426 | 2342 | 72 | 2393065 |
| 2023 | 435 | 2331 | 76 | 1896281 |
| 2022 | 325 | 1623 | 35 | 1058154 |
| 2021 | 110 | 1830 | 33 | 1157948 |
| 2020 | 16 | 186 | 2 | 84659 |
| 2011 | 391 | 1929 | 29 | 1439612 |

## Interpretation

- This is station-year coverage for the currently loaded canonical DJF table, not final plant ECWT.
- `complete` means `coverage_ratio >= complete_threshold`; this run uses the configured threshold above.
- Coverage will change as more NOAA files are downloaded and loaded.
