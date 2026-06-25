# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-25T08:01:01+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260625T075706Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `5364db70888272cd0eddfc40a421d6743835481e`
- Source selector: `downloaded`
- Limit files: `981`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2020-2022`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 981 |
| Loaded files | 981 |
| Failed files | 0 |
| Source bytes parsed | 3741422527 |
| Raw rows seen | 10462537 |
| DJF rows seen | 2593597 |
| Rejected source-code rows | 246958 |
| Valid DJF temperature rows | 2238731 |
| Invalid DJF temperature rows | 107891 |
| Rejected plausibility rows | 17 |
| Duplicate station-hour observations | 748572 |
| Canonical hourly rows staged | 1490159 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 50403776 |
| `weather.hourly_djf rows for this run (file audit)` | 1490159 |
| `loaded files for this run` | 981 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 1490159 |
| `invalid temp rows for this run` | 107891 |
| `rejected source rows for this run` | 246958 |
| `rejected plausibility rows for this run` | 17 |
| `duplicate hour count for this run` | 748572 |
| `audit.calculation_run` | 504 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
