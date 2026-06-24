# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-24T03:46:13+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260624T034358Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `c59d6eb231a1b35d980818aec9f8ecd6b9aab536`
- Source selector: `downloaded`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2009-2009`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 624 |
| Loaded files | 624 |
| Failed files | 0 |
| Source bytes parsed | 5469308070 |
| Raw rows seen | 12369781 |
| DJF rows seen | 3066852 |
| Rejected source-code rows | 1793630 |
| Valid DJF temperature rows | 1219651 |
| Invalid DJF temperature rows | 53571 |
| Rejected plausibility rows | 0 |
| Duplicate station-hour observations | 868313 |
| Canonical hourly rows staged | 351338 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 14488060 |
| `weather.hourly_djf rows for this run (file audit)` | 351338 |
| `loaded files for this run` | 624 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 351338 |
| `invalid temp rows for this run` | 53571 |
| `rejected source rows for this run` | 1793630 |
| `rejected plausibility rows for this run` | 0 |
| `duplicate hour count for this run` | 868313 |
| `audit.calculation_run` | 128 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
