# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-24T00:51:10+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260624T004532Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `cb6b00bc1d7017e560a767ff99318b25c87ddfb6`
- Source selector: `downloaded`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2011-2011`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 1000 |
| Loaded files | 1000 |
| Failed files | 0 |
| Source bytes parsed | 7038676166 |
| Raw rows seen | 15222317 |
| DJF rows seen | 3849178 |
| Rejected source-code rows | 2914499 |
| Valid DJF temperature rows | 860230 |
| Invalid DJF temperature rows | 74445 |
| Rejected plausibility rows | 4 |
| Duplicate station-hour observations | 383948 |
| Canonical hourly rows staged | 476282 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf total` | 7940480 |
| `weather.hourly_djf rows for this run` | 476282 |
| `loaded files for this run` | 1000 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 476282 |
| `invalid temp rows for this run` | 74445 |
| `rejected source rows for this run` | 2914499 |
| `rejected plausibility rows for this run` | 4 |
| `duplicate hour count for this run` | 383948 |
| `audit.calculation_run` | 73 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
