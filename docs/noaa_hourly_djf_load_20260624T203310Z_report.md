# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-24T20:33:20+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260624T203310Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `d7dfe307bd62b36e30127c7bd715dd45383fd810`
- Source selector: `downloaded`
- Limit files: `2000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2007-2023`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 5 |
| Loaded files | 5 |
| Failed files | 0 |
| Source bytes parsed | 41230710 |
| Raw rows seen | 80599 |
| DJF rows seen | 21360 |
| Rejected source-code rows | 13448 |
| Valid DJF temperature rows | 7464 |
| Invalid DJF temperature rows | 448 |
| Rejected plausibility rows | 0 |
| Duplicate station-hour observations | 2447 |
| Canonical hourly rows staged | 5017 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 48663564 |
| `weather.hourly_djf rows for this run (file audit)` | 5017 |
| `loaded files for this run` | 5 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 5017 |
| `invalid temp rows for this run` | 448 |
| `rejected source rows for this run` | 13448 |
| `rejected plausibility rows for this run` | 0 |
| `duplicate hour count for this run` | 2447 |
| `audit.calculation_run` | 431 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
