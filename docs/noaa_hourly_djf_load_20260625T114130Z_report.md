# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-25T11:49:34+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260625T114130Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `14ba661f2581ddd9b191eff65ac1d870b9cde9ef`
- Source selector: `downloaded`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2003-2005`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 851 |
| Loaded files | 851 |
| Failed files | 0 |
| Source bytes parsed | 1839544363 |
| Raw rows seen | 4998470 |
| DJF rows seen | 1244747 |
| Rejected source-code rows | 6470 |
| Valid DJF temperature rows | 1130136 |
| Invalid DJF temperature rows | 108138 |
| Rejected plausibility rows | 3 |
| Duplicate station-hour observations | 131799 |
| Canonical hourly rows staged | 998337 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 60275160 |
| `weather.hourly_djf rows for this run (file audit)` | 998337 |
| `loaded files for this run` | 851 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 998337 |
| `invalid temp rows for this run` | 108138 |
| `rejected source rows for this run` | 6470 |
| `rejected plausibility rows for this run` | 3 |
| `duplicate hour count for this run` | 131799 |
| `audit.calculation_run` | 537 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
