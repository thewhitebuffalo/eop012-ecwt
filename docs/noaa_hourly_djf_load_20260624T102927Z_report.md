# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-24T10:32:30+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260624T102927Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `13450e7833a9a40fe011eac55bde7b0468cf5c98`
- Source selector: `downloaded`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2005-2005`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 309 |
| Loaded files | 309 |
| Failed files | 0 |
| Source bytes parsed | 1842538465 |
| Raw rows seen | 4142667 |
| DJF rows seen | 1046997 |
| Rejected source-code rows | 257283 |
| Valid DJF temperature rows | 667925 |
| Invalid DJF temperature rows | 121789 |
| Rejected plausibility rows | 0 |
| Duplicate station-hour observations | 299414 |
| Canonical hourly rows staged | 368511 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 31040118 |
| `weather.hourly_djf rows for this run (file audit)` | 368511 |
| `loaded files for this run` | 309 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 368511 |
| `invalid temp rows for this run` | 121789 |
| `rejected source rows for this run` | 257283 |
| `rejected plausibility rows for this run` | 0 |
| `duplicate hour count for this run` | 299414 |
| `audit.calculation_run` | 265 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
