# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-25T15:55:33+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260625T155515Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `bd3c33c8073c2a66057773e07ae474d2b8eb9be4`
- Source selector: `inventory`
- Limit files: `100`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2006-2006`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 56 |
| Loaded files | 56 |
| Failed files | 0 |
| Source bytes parsed | 93383864 |
| Raw rows seen | 224943 |
| DJF rows seen | 55368 |
| Rejected source-code rows | 1992 |
| Valid DJF temperature rows | 52247 |
| Invalid DJF temperature rows | 1129 |
| Rejected plausibility rows | 0 |
| Duplicate station-hour observations | 26454 |
| Canonical hourly rows staged | 25793 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 57346472 |
| `weather.hourly_djf rows for this run (file audit)` | 25793 |
| `loaded files for this run` | 56 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 25793 |
| `invalid temp rows for this run` | 1129 |
| `rejected source rows for this run` | 1992 |
| `rejected plausibility rows for this run` | 0 |
| `duplicate hour count for this run` | 26454 |
| `audit.calculation_run` | 586 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
