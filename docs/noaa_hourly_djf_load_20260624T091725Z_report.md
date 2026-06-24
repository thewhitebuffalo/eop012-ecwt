# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-24T09:19:35+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260624T091725Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `51dfc45e47108eb1e6e2474ef1aa97bae44177f4`
- Source selector: `downloaded`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2005-2005`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 370 |
| Loaded files | 370 |
| Failed files | 0 |
| Source bytes parsed | 2614943516 |
| Raw rows seen | 5824568 |
| DJF rows seen | 1496864 |
| Rejected source-code rows | 430428 |
| Valid DJF temperature rows | 940787 |
| Invalid DJF temperature rows | 125648 |
| Rejected plausibility rows | 1 |
| Duplicate station-hour observations | 495396 |
| Canonical hourly rows staged | 445391 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 25817504 |
| `weather.hourly_djf rows for this run (file audit)` | 445391 |
| `loaded files for this run` | 370 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 445391 |
| `invalid temp rows for this run` | 125648 |
| `rejected source rows for this run` | 430428 |
| `rejected plausibility rows for this run` | 1 |
| `duplicate hour count for this run` | 495396 |
| `audit.calculation_run` | 241 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
