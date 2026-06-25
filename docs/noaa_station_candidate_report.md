# NOAA Station Candidate Report

Generated UTC: 2026-06-25T06:57:07+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_station_candidates_20260625T065445Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `417d0a63175928fc7d21f579520d787523497a52`

## Source

- Source URL: `https://www.ncei.noaa.gov/pub/data/noaa/isd-history.csv`
- Local path: `/Volumes/NOAA_CACHE/EOP012/raw/noaa/isd-history.csv`
- Size bytes: `2914601`
- SHA-256: `1994747ab4af1b97e63adb434b4d0d022f2daee76f0c144ea9ab46be2d906604`

## Candidate Parameters

- Top candidates per plant: `100`
- Initial radius: `250 km`
- Expanded radius: `1000 km`
- Coverage metrics: pending; these candidates are distance-only station metadata candidates.

## Counts

| Metric | Count |
| --- | ---: |
| Parsed NOAA stations loaded | 19164 |
| Plants with valid coordinates considered | 16104 |
| Station candidate rows generated | 1610400 |
| Plants satisfied by initial radius | 10955 |
| Plants requiring expanded radius | 5052 |
| Plants requiring global fallback | 97 |
| Plants with no candidate | 0 |

## Database Row Counts

| Relation | Rows |
| --- | ---: |
| `weather.station` | 19164 |
| `link.station_candidate for this run` | 1610400 |
| `plants with candidates for this run` | 16104 |
| `audit.source_file` | 62334 |
| `audit.calculation_run` | 489 |
| `audit.exception_log` | 507 |

## Notes

- Station IDs use NOAA ISD `USAF-WBAN` format, matching the local NOAA hourly cache format.
- Candidate ranking is distance-only for this phase.
- Representative station selection is not complete until hourly DJF coverage metrics are joined and reviewed.
- `valid_djf_hours`, `expected_djf_hours`, and `coverage_ratio` are intentionally null in this phase.
