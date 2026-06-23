# NOAA Weather Coverage Audit Report

Generated UTC: 2026-06-23T21:22:11+00:00

## Target Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Source Database

- Host: `127.0.0.1`
- Port: `5435`
- Database: `noaa_djf_hourly_bytower`
- Source table: `public.ecwt_raw_station`
- Source basis: `legacy_ecwt_raw_station_sample_hours`
- Local path: `/Volumes/NOAA_CACHE/postgres16_weather_build_5435`

## Run

- Calculation run ID: `noaa_weather_coverage_audit_20260623T212151Z`
- Candidate run ID enriched: `noaa_station_candidates_20260623T210132Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `a0180e7278ed0bf9a4346bd0fa8c7d8779bfaadc`

## Coverage Window

- Period start UTC: `2000-01-01T00:00:00+00:00`
- Period end UTC: `2025-12-31T23:00:00+00:00`
- Expected DJF hours per station: `56328`
- DJF filtering basis for this fast audit: UTC calendar months in the legacy station sample-hour inventory.

## Counts

| Metric | Count |
| --- | ---: |
| Candidate stations audited | 4400 |
| Stations with full-period legacy sample row | 4057 |
| Stations missing full-period legacy sample row | 343 |
| Stations with positive valid hours | 267 |
| Stations with zero valid hours | 4133 |
| Minimum valid hours | 0 |
| Maximum valid hours | 32330 |
| Maximum coverage ratio | 0.573959664820338 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.station_coverage_audit for this run` | 4400 |
| `link.station_candidate rows updated` | 161040 |
| `plants with at least one positive-coverage candidate` | 7249 |
| `plants with zero positive-coverage candidates` | 8855 |
| `max candidate coverage ratio` | 0.573960 |
| `audit.source_file` | 7 |
| `audit.calculation_run` | 3 |
| `audit.exception_log` | 372 |

## Interpretation

- This is a fast coverage audit against the legacy NOAA station sample-hour inventory, not a full raw-hour recount.
- `duplicate_hour_count` and `invalid_temp_count` are stored as `0` for this pass because `ecwt_raw_station.sample_hours` only exposes accepted sample-hour totals.
- The current NOAA cache is materially incomplete for a compliance-grade national ECWT run; station selection should not be finalized from this coverage pass alone.
- The next required build step is a full hourly NOAA DJF rebuild or recount that can populate raw missing, duplicate, and invalid-temperature evidence.
