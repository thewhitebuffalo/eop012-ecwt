# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-24T10:06:22+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260624T100353Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `4c03d5489b8914cebdc683e9d4ac1cef18d92df1`
- Source selector: `downloaded`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2005-2005`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 330 |
| Loaded files | 330 |
| Failed files | 0 |
| Source bytes parsed | 2182031367 |
| Raw rows seen | 4940829 |
| DJF rows seen | 1242278 |
| Rejected source-code rows | 341445 |
| Valid DJF temperature rows | 809535 |
| Invalid DJF temperature rows | 91298 |
| Rejected plausibility rows | 0 |
| Duplicate station-hour observations | 414068 |
| Canonical hourly rows staged | 395467 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 31040118 |
| `weather.hourly_djf rows for this run (file audit)` | 395467 |
| `loaded files for this run` | 330 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 395467 |
| `invalid temp rows for this run` | 91298 |
| `rejected source rows for this run` | 341445 |
| `rejected plausibility rows for this run` | 0 |
| `duplicate hour count for this run` | 414068 |
| `audit.calculation_run` | 257 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
