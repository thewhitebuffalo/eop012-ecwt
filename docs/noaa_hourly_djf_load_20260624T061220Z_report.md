# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-24T06:15:35+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260624T061220Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `958969d0a3d5dc2746dba091f7bc527cec078cba`
- Source selector: `inventory`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2015-2015`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 1000 |
| Loaded files | 1000 |
| Failed files | 0 |
| Source bytes parsed | 8605623951 |
| Raw rows seen | 18380137 |
| DJF rows seen | 4580536 |
| Rejected source-code rows | 3885223 |
| Valid DJF temperature rows | 623979 |
| Invalid DJF temperature rows | 71334 |
| Rejected plausibility rows | 0 |
| Duplicate station-hour observations | 292643 |
| Canonical hourly rows staged | 331336 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 20000640 |
| `weather.hourly_djf rows for this run (file audit)` | 331336 |
| `loaded files for this run` | 1000 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 331336 |
| `invalid temp rows for this run` | 71334 |
| `rejected source rows for this run` | 3885223 |
| `rejected plausibility rows for this run` | 0 |
| `duplicate hour count for this run` | 292643 |
| `audit.calculation_run` | 183 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
