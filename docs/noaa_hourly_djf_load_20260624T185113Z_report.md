# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-24T18:59:07+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260624T185113Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `1c36bdf53ca8b7619d743a34a54d4a3f8f12931a`
- Source selector: `downloaded`
- Limit files: `2000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2013-2016`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 1642 |
| Loaded files | 1642 |
| Failed files | 0 |
| Source bytes parsed | 14371990032 |
| Raw rows seen | 34435637 |
| DJF rows seen | 8980334 |
| Rejected source-code rows | 2860675 |
| Valid DJF temperature rows | 5870022 |
| Invalid DJF temperature rows | 249632 |
| Rejected plausibility rows | 5 |
| Duplicate station-hour observations | 4196114 |
| Canonical hourly rows staged | 1673908 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 45516536 |
| `weather.hourly_djf rows for this run (file audit)` | 1673908 |
| `loaded files for this run` | 1642 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 1673908 |
| `invalid temp rows for this run` | 249632 |
| `rejected source rows for this run` | 2860675 |
| `rejected plausibility rows for this run` | 5 |
| `duplicate hour count for this run` | 4196114 |
| `audit.calculation_run` | 405 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
