# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-24T00:39:06+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260624T003409Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `cb6b00bc1d7017e560a767ff99318b25c87ddfb6`
- Source selector: `inventory`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2021-2021`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 1000 |
| Loaded files | 1000 |
| Failed files | 0 |
| Source bytes parsed | 8018345951 |
| Raw rows seen | 16545655 |
| DJF rows seen | 4180294 |
| Rejected source-code rows | 3334115 |
| Valid DJF temperature rows | 769331 |
| Invalid DJF temperature rows | 76848 |
| Rejected plausibility rows | 0 |
| Duplicate station-hour observations | 375671 |
| Canonical hourly rows staged | 393660 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf total` | 7464198 |
| `weather.hourly_djf rows for this run` | 393660 |
| `loaded files for this run` | 1000 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 393660 |
| `invalid temp rows for this run` | 76848 |
| `rejected source rows for this run` | 3334115 |
| `rejected plausibility rows for this run` | 0 |
| `duplicate hour count for this run` | 375671 |
| `audit.calculation_run` | 71 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
