# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-24T13:30:38+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260624T132935Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `82d45ac19319fe7817bf7cd2839ce16e29b79555`
- Source selector: `downloaded`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2002-2002`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 283 |
| Loaded files | 283 |
| Failed files | 0 |
| Source bytes parsed | 1292973842 |
| Raw rows seen | 3123049 |
| DJF rows seen | 732327 |
| Rejected source-code rows | 0 |
| Valid DJF temperature rows | 493310 |
| Invalid DJF temperature rows | 239015 |
| Rejected plausibility rows | 2 |
| Duplicate station-hour observations | 88109 |
| Canonical hourly rows staged | 405201 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 38271296 |
| `weather.hourly_djf rows for this run (file audit)` | 405201 |
| `loaded files for this run` | 283 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 405201 |
| `invalid temp rows for this run` | 239015 |
| `rejected source rows for this run` | 0 |
| `rejected plausibility rows for this run` | 2 |
| `duplicate hour count for this run` | 88109 |
| `audit.calculation_run` | 322 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
