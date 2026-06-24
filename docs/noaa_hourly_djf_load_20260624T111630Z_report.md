# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-24T11:18:29+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260624T111630Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `60da55785ceb0b129992646d8cda0c86164bddd5`
- Source selector: `downloaded`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2004-2004`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 398 |
| Loaded files | 398 |
| Failed files | 0 |
| Source bytes parsed | 2476739545 |
| Raw rows seen | 5836104 |
| DJF rows seen | 1377759 |
| Rejected source-code rows | 0 |
| Valid DJF temperature rows | 925489 |
| Invalid DJF temperature rows | 452256 |
| Rejected plausibility rows | 14 |
| Duplicate station-hour observations | 337952 |
| Canonical hourly rows staged | 587537 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 31981914 |
| `weather.hourly_djf rows for this run (file audit)` | 587537 |
| `loaded files for this run` | 398 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 587537 |
| `invalid temp rows for this run` | 452256 |
| `rejected source rows for this run` | 0 |
| `rejected plausibility rows for this run` | 14 |
| `duplicate hour count for this run` | 337952 |
| `audit.calculation_run` | 280 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
