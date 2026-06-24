# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-24T11:44:01+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260624T114227Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `50ccc0ea9eb41b69da2ee2762c49f370c488853b`
- Source selector: `downloaded`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2004-2004`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 341 |
| Loaded files | 341 |
| Failed files | 0 |
| Source bytes parsed | 1794693097 |
| Raw rows seen | 4275526 |
| DJF rows seen | 1040556 |
| Rejected source-code rows | 0 |
| Valid DJF temperature rows | 754095 |
| Invalid DJF temperature rows | 286199 |
| Rejected plausibility rows | 262 |
| Duplicate station-hour observations | 273377 |
| Canonical hourly rows staged | 480718 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 31981914 |
| `weather.hourly_djf rows for this run (file audit)` | 480718 |
| `loaded files for this run` | 341 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 480718 |
| `invalid temp rows for this run` | 286199 |
| `rejected source rows for this run` | 0 |
| `rejected plausibility rows for this run` | 262 |
| `duplicate hour count for this run` | 273377 |
| `audit.calculation_run` | 289 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
