# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-24T03:02:08+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260624T025933Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `b68bd1d44aafc4d25f023da2cee212ba7c8bec71`
- Source selector: `downloaded`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2009-2010`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 645 |
| Loaded files | 645 |
| Failed files | 0 |
| Source bytes parsed | 4464983988 |
| Raw rows seen | 10465348 |
| DJF rows seen | 2591252 |
| Rejected source-code rows | 1231875 |
| Valid DJF temperature rows | 1246346 |
| Invalid DJF temperature rows | 113030 |
| Rejected plausibility rows | 1 |
| Duplicate station-hour observations | 728147 |
| Canonical hourly rows staged | 518199 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 13118617 |
| `weather.hourly_djf rows for this run (file audit)` | 518199 |
| `loaded files for this run` | 645 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 518199 |
| `invalid temp rows for this run` | 113030 |
| `rejected source rows for this run` | 1231875 |
| `rejected plausibility rows for this run` | 1 |
| `duplicate hour count for this run` | 728147 |
| `audit.calculation_run` | 113 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
