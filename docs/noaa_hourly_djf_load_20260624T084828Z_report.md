# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-24T08:54:11+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260624T084828Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `3bbb1391388ca386a595e9720e759eb1723e5e41`
- Source selector: `inventory`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2012-2013`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 1000 |
| Loaded files | 1000 |
| Failed files | 0 |
| Source bytes parsed | 10813272741 |
| Raw rows seen | 25798207 |
| DJF rows seen | 6411543 |
| Rejected source-code rows | 2023338 |
| Valid DJF temperature rows | 4253116 |
| Invalid DJF temperature rows | 135054 |
| Rejected plausibility rows | 35 |
| Duplicate station-hour observations | 3194239 |
| Canonical hourly rows staged | 1058877 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 25817504 |
| `weather.hourly_djf rows for this run (file audit)` | 1058877 |
| `loaded files for this run` | 1000 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 1058877 |
| `invalid temp rows for this run` | 135054 |
| `rejected source rows for this run` | 2023338 |
| `rejected plausibility rows for this run` | 35 |
| `duplicate hour count for this run` | 3194239 |
| `audit.calculation_run` | 231 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
