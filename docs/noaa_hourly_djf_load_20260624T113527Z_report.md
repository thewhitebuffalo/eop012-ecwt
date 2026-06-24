# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-24T11:37:21+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260624T113527Z`
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
| Candidate files selected | 351 |
| Loaded files | 351 |
| Failed files | 0 |
| Source bytes parsed | 2111816551 |
| Raw rows seen | 5023361 |
| DJF rows seen | 1192886 |
| Rejected source-code rows | 0 |
| Valid DJF temperature rows | 830834 |
| Invalid DJF temperature rows | 362052 |
| Rejected plausibility rows | 0 |
| Duplicate station-hour observations | 315621 |
| Canonical hourly rows staged | 515213 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 31981914 |
| `weather.hourly_djf rows for this run (file audit)` | 515213 |
| `loaded files for this run` | 351 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 515213 |
| `invalid temp rows for this run` | 362052 |
| `rejected source rows for this run` | 0 |
| `rejected plausibility rows for this run` | 0 |
| `duplicate hour count for this run` | 315621 |
| `audit.calculation_run` | 287 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
