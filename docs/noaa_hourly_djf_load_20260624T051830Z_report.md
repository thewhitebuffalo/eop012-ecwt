# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-24T05:20:46+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260624T051830Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `88f480aea132c23dcb91df828d5148ffb6ecbf0b`
- Source selector: `downloaded`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2008-2008`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 610 |
| Loaded files | 610 |
| Failed files | 0 |
| Source bytes parsed | 5004860108 |
| Raw rows seen | 11180829 |
| DJF rows seen | 2847895 |
| Rejected source-code rows | 1821618 |
| Valid DJF temperature rows | 950874 |
| Invalid DJF temperature rows | 75403 |
| Rejected plausibility rows | 0 |
| Duplicate station-hour observations | 643221 |
| Canonical hourly rows staged | 307653 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 18361436 |
| `weather.hourly_djf rows for this run (file audit)` | 307653 |
| `loaded files for this run` | 610 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 307653 |
| `invalid temp rows for this run` | 75403 |
| `rejected source rows for this run` | 1821618 |
| `rejected plausibility rows for this run` | 0 |
| `duplicate hour count for this run` | 643221 |
| `audit.calculation_run` | 167 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
