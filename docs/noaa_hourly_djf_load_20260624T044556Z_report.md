# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-24T04:48:31+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260624T044556Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `b35ae6d028ff68b919bd3657bcb60c651b8d706c`
- Source selector: `downloaded`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2009-2009`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 576 |
| Loaded files | 576 |
| Failed files | 0 |
| Source bytes parsed | 4129130364 |
| Raw rows seen | 9917876 |
| DJF rows seen | 2441525 |
| Rejected source-code rows | 977114 |
| Valid DJF temperature rows | 1381019 |
| Invalid DJF temperature rows | 83392 |
| Rejected plausibility rows | 0 |
| Duplicate station-hour observations | 841320 |
| Canonical hourly rows staged | 539699 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 16271002 |
| `weather.hourly_djf rows for this run (file audit)` | 539699 |
| `loaded files for this run` | 576 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 539699 |
| `invalid temp rows for this run` | 83392 |
| `rejected source rows for this run` | 977114 |
| `rejected plausibility rows for this run` | 0 |
| `duplicate hour count for this run` | 841320 |
| `audit.calculation_run` | 155 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
