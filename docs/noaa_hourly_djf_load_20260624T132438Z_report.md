# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-24T13:25:32+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260624T132438Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `82d45ac19319fe7817bf7cd2839ce16e29b79555`
- Source selector: `downloaded`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2002-2002`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 283 |
| Loaded files | 283 |
| Failed files | 0 |
| Source bytes parsed | 1348680464 |
| Raw rows seen | 3190227 |
| DJF rows seen | 745726 |
| Rejected source-code rows | 0 |
| Valid DJF temperature rows | 513549 |
| Invalid DJF temperature rows | 232177 |
| Rejected plausibility rows | 0 |
| Duplicate station-hour observations | 110988 |
| Canonical hourly rows staged | 402561 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 35966048 |
| `weather.hourly_djf rows for this run (file audit)` | 402561 |
| `loaded files for this run` | 283 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 402561 |
| `invalid temp rows for this run` | 232177 |
| `rejected source rows for this run` | 0 |
| `rejected plausibility rows for this run` | 0 |
| `duplicate hour count for this run` | 110988 |
| `audit.calculation_run` | 320 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
