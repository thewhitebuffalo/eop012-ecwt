# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-25T01:32:15+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260625T013212Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `5f98bf3e40843271aa1a260746046836380182e3`
- Source selector: `downloaded`
- Limit files: `10`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `None-None`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 0 |
| Loaded files | 0 |
| Failed files | 0 |
| Source bytes parsed | 0 |
| Raw rows seen | 0 |
| DJF rows seen | 0 |
| Rejected source-code rows | 0 |
| Valid DJF temperature rows | 0 |
| Invalid DJF temperature rows | 0 |
| Rejected plausibility rows | 0 |
| Duplicate station-hour observations | 0 |
| Canonical hourly rows staged | 0 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 50403776 |
| `weather.hourly_djf rows for this run (file audit)` | 0 |
| `loaded files for this run` | 0 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 0 |
| `invalid temp rows for this run` | 0 |
| `rejected source rows for this run` | 0 |
| `rejected plausibility rows for this run` | 0 |
| `duplicate hour count for this run` | 0 |
| `audit.calculation_run` | 449 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
- No candidate files were selected, so this run is an auditable no-op and loaded zero weather rows.
