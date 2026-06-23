# Station-Year DJF Coverage Report

Generated UTC: 2026-06-23T23:21:16+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `station_year_djf_coverage_20260623T232101Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `1992520b60f19f08c3f604d399c496be12ea7b39`
- Year range: `2000-2025`
- Complete threshold: `0.95`

## Summary

| Relation or Check | Rows / Value |
| --- | ---: |
| `coverage rows for this run` | 5000 |
| `complete station-years` | 205 |
| `partial station-years` | 4674 |
| `empty station-years` | 121 |
| `valid DJF hours represented` | 2652389 |
| `rejected source rows represented` | 11289984 |

## Coverage By Year

| Year | Complete | Partial | Empty | Valid DJF Hours |
| ---: | ---: | ---: | ---: | ---: |
| 2025 | 0 | 2705 | 104 | 1261605 |
| 2024 | 175 | 1812 | 13 | 1289247 |
| 2023 | 30 | 157 | 4 | 101537 |

## Interpretation

- This is station-year coverage for the currently loaded canonical DJF table, not final plant ECWT.
- `complete` means `coverage_ratio >= complete_threshold`; this run uses the configured threshold above.
- Coverage will change as more NOAA files are downloaded and loaded.
