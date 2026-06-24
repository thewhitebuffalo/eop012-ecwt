# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-24T02:05:15+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260624T020025Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `ec4f3e306097d39440575bdb79e8cabc99498898`
- Source selector: `inventory`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2019-2020`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 1000 |
| Loaded files | 1000 |
| Failed files | 0 |
| Source bytes parsed | 10850094806 |
| Raw rows seen | 24634688 |
| DJF rows seen | 6194717 |
| Rejected source-code rows | 2578646 |
| Valid DJF temperature rows | 3452232 |
| Invalid DJF temperature rows | 163829 |
| Rejected plausibility rows | 10 |
| Duplicate station-hour observations | 2632280 |
| Canonical hourly rows staged | 819952 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 10667540 |
| `weather.hourly_djf rows for this run (file audit)` | 819952 |
| `loaded files for this run` | 1000 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 819952 |
| `invalid temp rows for this run` | 163829 |
| `rejected source rows for this run` | 2578646 |
| `rejected plausibility rows for this run` | 10 |
| `duplicate hour count for this run` | 2632280 |
| `audit.calculation_run` | 95 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
