# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-23T23:04:02+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260623T230025Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `55e07669c484f3298a781d06a8591ca3dbbfe210`
- Source selector: `inventory`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-90.0` to `50.0`
- Years represented: `2024-2024`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 1000 |
| Loaded files | 1000 |
| Failed files | 0 |
| Source bytes parsed | 7379374784 |
| Raw rows seen | 14714803 |
| DJF rows seen | 3792522 |
| Rejected source-code rows | 2879389 |
| Valid DJF temperature rows | 833644 |
| Invalid DJF temperature rows | 79489 |
| Rejected plausibility rows | 0 |
| Duplicate station-hour observations | 317909 |
| Canonical hourly rows staged | 515735 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf total` | 1885936 |
| `weather.hourly_djf rows for this run` | 515735 |
| `loaded files for this run` | 1000 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 515735 |
| `invalid temp rows for this run` | 79489 |
| `rejected source rows for this run` | 2879389 |
| `rejected plausibility rows for this run` | 0 |
| `duplicate hour count for this run` | 317909 |
| `audit.calculation_run` | 26 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
