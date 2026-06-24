# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-24T13:36:27+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260624T133502Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `82d45ac19319fe7817bf7cd2839ce16e29b79555`
- Source selector: `downloaded`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2001-2002`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 322 |
| Loaded files | 322 |
| Failed files | 0 |
| Source bytes parsed | 1300390316 |
| Raw rows seen | 3189102 |
| DJF rows seen | 779779 |
| Rejected source-code rows | 0 |
| Valid DJF temperature rows | 519434 |
| Invalid DJF temperature rows | 260338 |
| Rejected plausibility rows | 7 |
| Duplicate station-hour observations | 83454 |
| Canonical hourly rows staged | 435980 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 38271296 |
| `weather.hourly_djf rows for this run (file audit)` | 435980 |
| `loaded files for this run` | 322 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 435980 |
| `invalid temp rows for this run` | 260338 |
| `rejected source rows for this run` | 0 |
| `rejected plausibility rows for this run` | 7 |
| `duplicate hour count for this run` | 83454 |
| `audit.calculation_run` | 324 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
