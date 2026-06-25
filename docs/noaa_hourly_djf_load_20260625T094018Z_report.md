# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-25T09:45:03+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260625T094018Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `891886d03bf8418f4458e9f9f56459cf39cb2c67`
- Source selector: `downloaded`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2018-2020`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 964 |
| Loaded files | 964 |
| Failed files | 0 |
| Source bytes parsed | 3734049068 |
| Raw rows seen | 10379807 |
| DJF rows seen | 2636980 |
| Rejected source-code rows | 275541 |
| Valid DJF temperature rows | 2276114 |
| Invalid DJF temperature rows | 85192 |
| Rejected plausibility rows | 133 |
| Duplicate station-hour observations | 768379 |
| Canonical hourly rows staged | 1507735 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 50403776 |
| `weather.hourly_djf rows for this run (file audit)` | 1507735 |
| `loaded files for this run` | 964 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 1507735 |
| `invalid temp rows for this run` | 85192 |
| `rejected source rows for this run` | 275541 |
| `rejected plausibility rows for this run` | 133 |
| `duplicate hour count for this run` | 768379 |
| `audit.calculation_run` | 513 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
