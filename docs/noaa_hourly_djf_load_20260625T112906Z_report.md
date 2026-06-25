# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-25T11:32:25+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260625T112906Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `66fc6f9cc20081a97c9ab607de0fa2c787c57987`
- Source selector: `downloaded`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2005-2008`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 716 |
| Loaded files | 716 |
| Failed files | 0 |
| Source bytes parsed | 2021443427 |
| Raw rows seen | 5614969 |
| DJF rows seen | 1399994 |
| Rejected source-code rows | 49751 |
| Valid DJF temperature rows | 1289344 |
| Invalid DJF temperature rows | 60895 |
| Rejected plausibility rows | 4 |
| Duplicate station-hour observations | 249745 |
| Canonical hourly rows staged | 1039599 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 60275160 |
| `weather.hourly_djf rows for this run (file audit)` | 1039599 |
| `loaded files for this run` | 716 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 1039599 |
| `invalid temp rows for this run` | 60895 |
| `rejected source rows for this run` | 49751 |
| `rejected plausibility rows for this run` | 4 |
| `duplicate hour count for this run` | 249745 |
| `audit.calculation_run` | 534 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
