# Station-Year DJF Coverage Report

Generated UTC: 2026-06-23T23:43:54+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `station_year_djf_coverage_20260623T234347Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `c22cc01f4cb305ebb316c53a74ae66fb88dd50da`
- Year range: `2000-2025`
- Complete threshold: `0.95`

## Summary

| Relation or Check | Rows / Value |
| --- | ---: |
| `coverage rows for this run` | 7000 |
| `complete station-years` | 602 |
| `partial station-years` | 6209 |
| `empty station-years` | 189 |
| `valid DJF hours represented` | 4355005 |
| `rejected source rows represented` | 16003043 |

## Coverage By Year

| Year | Complete | Partial | Empty | Valid DJF Hours |
| ---: | ---: | ---: | ---: | ---: |
| 2025 | 0 | 2704 | 105 | 1261604 |
| 2024 | 426 | 2342 | 72 | 2393067 |
| 2023 | 166 | 1014 | 11 | 653058 |
| 2022 | 10 | 149 | 1 | 47276 |

## Interpretation

- This is station-year coverage for the currently loaded canonical DJF table, not final plant ECWT.
- `complete` means `coverage_ratio >= complete_threshold`; this run uses the configured threshold above.
- Coverage will change as more NOAA files are downloaded and loaded.
