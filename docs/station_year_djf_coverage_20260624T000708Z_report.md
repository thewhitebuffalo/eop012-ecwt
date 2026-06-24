# Station-Year DJF Coverage Report

Generated UTC: 2026-06-24T00:08:35+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `station_year_djf_coverage_20260624T000708Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `21e5e54ae61f56d12f48645a7965047ed330fe01`
- Year range: `2000-2025`
- Complete threshold: `0.95`

## Summary

| Relation or Check | Rows / Value |
| --- | ---: |
| `coverage rows for this run` | 9000 |
| `complete station-years` | 679 |
| `partial station-years` | 8123 |
| `empty station-years` | 198 |
| `valid DJF hours represented` | 4923791 |
| `rejected source rows represented` | 22893818 |

## Coverage By Year

| Year | Complete | Partial | Empty | Valid DJF Hours |
| ---: | ---: | ---: | ---: | ---: |
| 2025 | 0 | 2704 | 105 | 1261604 |
| 2024 | 426 | 2342 | 72 | 2393065 |
| 2023 | 180 | 1995 | 16 | 909234 |
| 2022 | 73 | 1082 | 5 | 359888 |

## Interpretation

- This is station-year coverage for the currently loaded canonical DJF table, not final plant ECWT.
- `complete` means `coverage_ratio >= complete_threshold`; this run uses the configured threshold above.
- Coverage will change as more NOAA files are downloaded and loaded.
