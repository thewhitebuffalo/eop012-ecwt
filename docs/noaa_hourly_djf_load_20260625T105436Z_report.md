# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-25T10:58:18+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260625T105436Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `11cd1431d252dd9eb5fe78bb97a4ebe629b99da4`
- Source selector: `downloaded`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2011-2013`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 915 |
| Loaded files | 915 |
| Failed files | 0 |
| Source bytes parsed | 2949283352 |
| Raw rows seen | 8315800 |
| DJF rows seen | 2078753 |
| Rejected source-code rows | 120966 |
| Valid DJF temperature rows | 1865048 |
| Invalid DJF temperature rows | 92739 |
| Rejected plausibility rows | 0 |
| Duplicate station-hour observations | 457971 |
| Canonical hourly rows staged | 1407077 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 55124384 |
| `weather.hourly_djf rows for this run (file audit)` | 1407077 |
| `loaded files for this run` | 915 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 1407077 |
| `invalid temp rows for this run` | 92739 |
| `rejected source rows for this run` | 120966 |
| `rejected plausibility rows for this run` | 0 |
| `duplicate hour count for this run` | 457971 |
| `audit.calculation_run` | 525 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
