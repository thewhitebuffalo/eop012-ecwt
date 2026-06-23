# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-23T23:20:53+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260623T231622Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `1992520b60f19f08c3f604d399c496be12ea7b39`
- Source selector: `downloaded`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-90.0` to `50.0`
- Years represented: `2023-2025`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 1000 |
| Loaded files | 1000 |
| Failed files | 0 |
| Source bytes parsed | 8131384202 |
| Raw rows seen | 19134002 |
| DJF rows seen | 4781376 |
| Rejected source-code rows | 1330988 |
| Valid DJF temperature rows | 3287778 |
| Invalid DJF temperature rows | 162610 |
| Rejected plausibility rows | 0 |
| Duplicate station-hour observations | 2521325 |
| Canonical hourly rows staged | 766453 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf total` | 2652389 |
| `weather.hourly_djf rows for this run` | 766453 |
| `loaded files for this run` | 1000 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 766453 |
| `invalid temp rows for this run` | 162610 |
| `rejected source rows for this run` | 1330988 |
| `rejected plausibility rows for this run` | 0 |
| `duplicate hour count for this run` | 2521325 |
| `audit.calculation_run` | 32 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
