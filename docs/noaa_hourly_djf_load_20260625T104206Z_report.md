# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-25T10:45:38+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260625T104206Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `ffe11babb912514245701f30e4d43bdf816d8c60`
- Source selector: `downloaded`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2013-2016`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 909 |
| Loaded files | 909 |
| Failed files | 0 |
| Source bytes parsed | 3278543244 |
| Raw rows seen | 9185739 |
| DJF rows seen | 2287005 |
| Rejected source-code rows | 166830 |
| Valid DJF temperature rows | 2052181 |
| Invalid DJF temperature rows | 67994 |
| Rejected plausibility rows | 0 |
| Duplicate station-hour observations | 623052 |
| Canonical hourly rows staged | 1429129 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 55124384 |
| `weather.hourly_djf rows for this run (file audit)` | 1429129 |
| `loaded files for this run` | 909 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 1429129 |
| `invalid temp rows for this run` | 67994 |
| `rejected source rows for this run` | 166830 |
| `rejected plausibility rows for this run` | 0 |
| `duplicate hour count for this run` | 623052 |
| `audit.calculation_run` | 522 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
