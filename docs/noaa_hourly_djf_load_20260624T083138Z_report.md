# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-24T08:34:15+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260624T083138Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `2136f38fe838410e162350eed29d48b74d422ae8`
- Source selector: `downloaded`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2007-2007`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 417 |
| Loaded files | 417 |
| Failed files | 0 |
| Source bytes parsed | 3807036434 |
| Raw rows seen | 8670423 |
| DJF rows seen | 2116375 |
| Rejected source-code rows | 769634 |
| Valid DJF temperature rows | 1309290 |
| Invalid DJF temperature rows | 37451 |
| Rejected plausibility rows | 0 |
| Duplicate station-hour observations | 886977 |
| Canonical hourly rows staged | 422313 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 25817504 |
| `weather.hourly_djf rows for this run (file audit)` | 422313 |
| `loaded files for this run` | 417 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 422313 |
| `invalid temp rows for this run` | 37451 |
| `rejected source rows for this run` | 769634 |
| `rejected plausibility rows for this run` | 0 |
| `duplicate hour count for this run` | 886977 |
| `audit.calculation_run` | 225 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
