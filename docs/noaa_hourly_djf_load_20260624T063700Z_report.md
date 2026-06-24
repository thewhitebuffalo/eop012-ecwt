# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-24T06:39:58+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260624T063700Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `bd9b876cf3e00028f3088805cac252947d234fe5`
- Source selector: `inventory`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2015-2015`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 1000 |
| Loaded files | 1000 |
| Failed files | 0 |
| Source bytes parsed | 7752959633 |
| Raw rows seen | 15738633 |
| DJF rows seen | 4050657 |
| Rejected source-code rows | 3519409 |
| Valid DJF temperature rows | 436838 |
| Invalid DJF temperature rows | 94410 |
| Rejected plausibility rows | 0 |
| Duplicate station-hour observations | 109226 |
| Canonical hourly rows staged | 327612 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 20720460 |
| `weather.hourly_djf rows for this run (file audit)` | 327612 |
| `loaded files for this run` | 1000 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 327612 |
| `invalid temp rows for this run` | 94410 |
| `rejected source rows for this run` | 3519409 |
| `rejected plausibility rows for this run` | 0 |
| `duplicate hour count for this run` | 109226 |
| `audit.calculation_run` | 191 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
