# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-24T20:01:42+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260624T195519Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `d7dfe307bd62b36e30127c7bd715dd45383fd810`
- Source selector: `downloaded`
- Limit files: `2000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2012-2013`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 1387 |
| Loaded files | 1387 |
| Failed files | 0 |
| Source bytes parsed | 12431798984 |
| Raw rows seen | 31420444 |
| DJF rows seen | 7859632 |
| Rejected source-code rows | 1691543 |
| Valid DJF temperature rows | 5956488 |
| Invalid DJF temperature rows | 211425 |
| Rejected plausibility rows | 176 |
| Duplicate station-hour observations | 4296503 |
| Canonical hourly rows staged | 1659985 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 48663564 |
| `weather.hourly_djf rows for this run (file audit)` | 1659985 |
| `loaded files for this run` | 1387 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 1659985 |
| `invalid temp rows for this run` | 211425 |
| `rejected source rows for this run` | 1691543 |
| `rejected plausibility rows for this run` | 176 |
| `duplicate hour count for this run` | 4296503 |
| `audit.calculation_run` | 417 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
