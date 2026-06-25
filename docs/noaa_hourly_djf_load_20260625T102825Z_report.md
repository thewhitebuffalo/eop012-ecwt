# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-25T10:32:09+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260625T102825Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `fede167fe6955e38678ef5e738b1a7b52ed39b86`
- Source selector: `downloaded`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2016-2018`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 937 |
| Loaded files | 937 |
| Failed files | 0 |
| Source bytes parsed | 3744542762 |
| Raw rows seen | 10398029 |
| DJF rows seen | 2599533 |
| Rejected source-code rows | 289798 |
| Valid DJF temperature rows | 2261706 |
| Invalid DJF temperature rows | 48029 |
| Rejected plausibility rows | 0 |
| Duplicate station-hour observations | 761621 |
| Canonical hourly rows staged | 1500085 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 55124384 |
| `weather.hourly_djf rows for this run (file audit)` | 1500085 |
| `loaded files for this run` | 937 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 1500085 |
| `invalid temp rows for this run` | 48029 |
| `rejected source rows for this run` | 289798 |
| `rejected plausibility rows for this run` | 0 |
| `duplicate hour count for this run` | 761621 |
| `audit.calculation_run` | 519 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
