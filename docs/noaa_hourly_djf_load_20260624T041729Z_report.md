# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-24T04:20:32+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260624T041729Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `779eaf7545abcd2f6a8dbbc11beb1f7b28a275d4`
- Source selector: `inventory`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2017-2017`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 1000 |
| Loaded files | 1000 |
| Failed files | 0 |
| Source bytes parsed | 7982061676 |
| Raw rows seen | 16202196 |
| DJF rows seen | 4080545 |
| Rejected source-code rows | 3590636 |
| Valid DJF temperature rows | 413782 |
| Invalid DJF temperature rows | 76127 |
| Rejected plausibility rows | 0 |
| Duplicate station-hour observations | 166816 |
| Canonical hourly rows staged | 246966 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 16271002 |
| `weather.hourly_djf rows for this run (file audit)` | 246966 |
| `loaded files for this run` | 1000 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 246966 |
| `invalid temp rows for this run` | 76127 |
| `rejected source rows for this run` | 3590636 |
| `rejected plausibility rows for this run` | 0 |
| `duplicate hour count for this run` | 166816 |
| `audit.calculation_run` | 142 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
