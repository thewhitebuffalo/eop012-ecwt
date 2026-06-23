# Station-Year DJF Coverage Report

Generated UTC: 2026-06-23T22:53:23+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `station_year_djf_coverage_20260623T225320Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `55e07669c484f3298a781d06a8591ca3dbbfe210`
- Year range: `2000-2025`
- Complete threshold: `0.95`

## Summary

| Relation or Check | Rows / Value |
| --- | ---: |
| `coverage rows for this run` | 2000 |
| `complete station-years` | 160 |
| `partial station-years` | 1804 |
| `empty station-years` | 36 |
| `valid DJF hours represented` | 1108193 |
| `rejected source rows represented` | 5100150 |

## Coverage By Year

| Year | Complete | Partial | Empty | Valid DJF Hours |
| ---: | ---: | ---: | ---: | ---: |
| 2025 | 0 | 972 | 28 | 334681 |
| 2024 | 160 | 832 | 8 | 773512 |

## Interpretation

- This is station-year coverage for the currently loaded canonical DJF table, not final plant ECWT.
- `complete` means `coverage_ratio >= complete_threshold`; this run uses the configured threshold above.
- Coverage will change as more NOAA files are downloaded and loaded.
