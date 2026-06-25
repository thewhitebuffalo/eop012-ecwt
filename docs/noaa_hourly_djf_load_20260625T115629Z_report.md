# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-25T11:59:08+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260625T115629Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `f08661b0c85195ea5d46db3d2d81535a51d67344`
- Source selector: `downloaded`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2001-2003`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 892 |
| Loaded files | 892 |
| Failed files | 0 |
| Source bytes parsed | 1851802178 |
| Raw rows seen | 4983128 |
| DJF rows seen | 1229741 |
| Rejected source-code rows | 0 |
| Valid DJF temperature rows | 1079470 |
| Invalid DJF temperature rows | 150260 |
| Rejected plausibility rows | 11 |
| Duplicate station-hour observations | 47800 |
| Canonical hourly rows staged | 1031670 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 57346472 |
| `weather.hourly_djf rows for this run (file audit)` | 1031670 |
| `loaded files for this run` | 892 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 1031670 |
| `invalid temp rows for this run` | 150260 |
| `rejected source rows for this run` | 0 |
| `rejected plausibility rows for this run` | 11 |
| `duplicate hour count for this run` | 47800 |
| `audit.calculation_run` | 540 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
