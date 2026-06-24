# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-24T01:12:24+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260624T010653Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `2aa504b0a1dcc760d1462915d0cf12cb819b220d`
- Source selector: `downloaded`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2011-2011`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 1000 |
| Loaded files | 1000 |
| Failed files | 0 |
| Source bytes parsed | 6774106370 |
| Raw rows seen | 14744170 |
| DJF rows seen | 3747093 |
| Rejected source-code rows | 2882081 |
| Valid DJF temperature rows | 761929 |
| Invalid DJF temperature rows | 103082 |
| Rejected plausibility rows | 1 |
| Duplicate station-hour observations | 192125 |
| Canonical hourly rows staged | 569804 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf total` | 9291323 |
| `weather.hourly_djf rows for this run` | 569804 |
| `loaded files for this run` | 1000 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 569804 |
| `invalid temp rows for this run` | 103082 |
| `rejected source rows for this run` | 2882081 |
| `rejected plausibility rows for this run` | 1 |
| `duplicate hour count for this run` | 192125 |
| `audit.calculation_run` | 81 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
