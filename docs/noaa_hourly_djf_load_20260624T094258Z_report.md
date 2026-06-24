# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-24T09:44:56+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260624T094258Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `56e65ed883387568b9894bc05e20a1681dae8979`
- Source selector: `downloaded`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2005-2005`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 381 |
| Loaded files | 381 |
| Failed files | 0 |
| Source bytes parsed | 2671468058 |
| Raw rows seen | 5985974 |
| DJF rows seen | 1510624 |
| Rejected source-code rows | 416773 |
| Valid DJF temperature rows | 928583 |
| Invalid DJF temperature rows | 165089 |
| Rejected plausibility rows | 179 |
| Duplicate station-hour observations | 467760 |
| Canonical hourly rows staged | 460823 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 28486288 |
| `weather.hourly_djf rows for this run (file audit)` | 460823 |
| `loaded files for this run` | 381 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 460823 |
| `invalid temp rows for this run` | 165089 |
| `rejected source rows for this run` | 416773 |
| `rejected plausibility rows for this run` | 179 |
| `duplicate hour count for this run` | 467760 |
| `audit.calculation_run` | 249 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
