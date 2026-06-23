# Station-Year DJF Coverage Report

Generated UTC: 2026-06-23T23:04:10+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `station_year_djf_coverage_20260623T230407Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `55e07669c484f3298a781d06a8591ca3dbbfe210`
- Year range: `2000-2025`
- Complete threshold: `0.95`

## Summary

| Relation or Check | Rows / Value |
| --- | ---: |
| `coverage rows for this run` | 4000 |
| `complete station-years` | 175 |
| `partial station-years` | 3774 |
| `empty station-years` | 51 |
| `valid DJF hours represented` | 1885936 |
| `rejected source rows represented` | 9958996 |

## Coverage By Year

| Year | Complete | Partial | Empty | Valid DJF Hours |
| ---: | ---: | ---: | ---: | ---: |
| 2025 | 0 | 1962 | 38 | 596689 |
| 2024 | 175 | 1812 | 13 | 1289247 |

## Interpretation

- This is station-year coverage for the currently loaded canonical DJF table, not final plant ECWT.
- `complete` means `coverage_ratio >= complete_threshold`; this run uses the configured threshold above.
- Coverage will change as more NOAA files are downloaded and loaded.
