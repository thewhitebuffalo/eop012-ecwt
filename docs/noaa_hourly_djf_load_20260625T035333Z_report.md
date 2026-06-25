# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-25T03:54:52+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260625T035333Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `2eb08d0b703820e49406ce689f0bf149cdd675a2`
- Source selector: `downloaded`
- Limit files: `250`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2006-2006`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 250 |
| Loaded files | 250 |
| Failed files | 0 |
| Source bytes parsed | 1785869799 |
| Raw rows seen | 3988027 |
| DJF rows seen | 984931 |
| Rejected source-code rows | 441527 |
| Valid DJF temperature rows | 523288 |
| Invalid DJF temperature rows | 20116 |
| Rejected plausibility rows | 0 |
| Duplicate station-hour observations | 257677 |
| Canonical hourly rows staged | 265611 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 50403776 |
| `weather.hourly_djf rows for this run (file audit)` | 265611 |
| `loaded files for this run` | 250 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 265611 |
| `invalid temp rows for this run` | 20116 |
| `rejected source rows for this run` | 441527 |
| `rejected plausibility rows for this run` | 0 |
| `duplicate hour count for this run` | 257677 |
| `audit.calculation_run` | 473 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
