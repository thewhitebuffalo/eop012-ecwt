# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-25T15:46:20+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260625T154554Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `bd3c33c8073c2a66057773e07ae474d2b8eb9be4`
- Source selector: `inventory`
- Limit files: `100`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2024-2024`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 100 |
| Loaded files | 100 |
| Failed files | 0 |
| Source bytes parsed | 342010930 |
| Raw rows seen | 955243 |
| DJF rows seen | 250239 |
| Rejected source-code rows | 17695 |
| Valid DJF temperature rows | 230547 |
| Invalid DJF temperature rows | 1997 |
| Rejected plausibility rows | 0 |
| Duplicate station-hour observations | 69787 |
| Canonical hourly rows staged | 160760 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 57346472 |
| `weather.hourly_djf rows for this run (file audit)` | 160760 |
| `loaded files for this run` | 100 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 160760 |
| `invalid temp rows for this run` | 1997 |
| `rejected source rows for this run` | 17695 |
| `rejected plausibility rows for this run` | 0 |
| `duplicate hour count for this run` | 69787 |
| `audit.calculation_run` | 573 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
