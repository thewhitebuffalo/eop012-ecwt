# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-24T15:25:51+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260624T152227Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `7c20d9d216e1f96e9f5ba6bd0adc9b15aaf922b8`
- Source selector: `downloaded`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2000-2022`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 774 |
| Loaded files | 774 |
| Failed files | 0 |
| Source bytes parsed | 3624645341 |
| Raw rows seen | 8540604 |
| DJF rows seen | 2154259 |
| Rejected source-code rows | 92063 |
| Valid DJF temperature rows | 1466728 |
| Invalid DJF temperature rows | 595466 |
| Rejected plausibility rows | 2 |
| Duplicate station-hour observations | 267710 |
| Canonical hourly rows staged | 1199018 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 39952200 |
| `weather.hourly_djf rows for this run (file audit)` | 1199018 |
| `loaded files for this run` | 774 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 1199018 |
| `invalid temp rows for this run` | 595466 |
| `rejected source rows for this run` | 92063 |
| `rejected plausibility rows for this run` | 2 |
| `duplicate hour count for this run` | 267710 |
| `audit.calculation_run` | 356 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
