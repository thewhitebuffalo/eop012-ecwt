# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-24T04:26:14+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260624T042304Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `779eaf7545abcd2f6a8dbbc11beb1f7b28a275d4`
- Source selector: `downloaded`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2009-2009`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 580 |
| Loaded files | 580 |
| Failed files | 0 |
| Source bytes parsed | 5141326885 |
| Raw rows seen | 12065395 |
| DJF rows seen | 2968040 |
| Rejected source-code rows | 1252245 |
| Valid DJF temperature rows | 1634394 |
| Invalid DJF temperature rows | 81401 |
| Rejected plausibility rows | 0 |
| Duplicate station-hour observations | 1181855 |
| Canonical hourly rows staged | 452539 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 16271002 |
| `weather.hourly_djf rows for this run (file audit)` | 452539 |
| `loaded files for this run` | 580 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 452539 |
| `invalid temp rows for this run` | 81401 |
| `rejected source rows for this run` | 1252245 |
| `rejected plausibility rows for this run` | 0 |
| `duplicate hour count for this run` | 1181855 |
| `audit.calculation_run` | 144 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
