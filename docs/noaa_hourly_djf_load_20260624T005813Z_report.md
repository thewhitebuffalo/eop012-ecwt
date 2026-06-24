# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-24T01:06:48+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260624T005813Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `2aa504b0a1dcc760d1462915d0cf12cb819b220d`
- Source selector: `inventory`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2020-2021`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 1000 |
| Loaded files | 1000 |
| Failed files | 0 |
| Source bytes parsed | 10737801341 |
| Raw rows seen | 24296006 |
| DJF rows seen | 6050940 |
| Rejected source-code rows | 2498756 |
| Valid DJF temperature rows | 3398005 |
| Invalid DJF temperature rows | 154179 |
| Rejected plausibility rows | 0 |
| Duplicate station-hour observations | 2616966 |
| Canonical hourly rows staged | 781039 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf total` | 8721519 |
| `weather.hourly_djf rows for this run` | 781039 |
| `loaded files for this run` | 1000 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 781039 |
| `invalid temp rows for this run` | 154179 |
| `rejected source rows for this run` | 2498756 |
| `rejected plausibility rows for this run` | 0 |
| `duplicate hour count for this run` | 2616966 |
| `audit.calculation_run` | 80 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
