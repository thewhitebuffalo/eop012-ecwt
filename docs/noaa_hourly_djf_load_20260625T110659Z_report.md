# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-25T11:10:55+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260625T110659Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `a254c646319119499ef4a63d22d84015e71d9089`
- Source selector: `downloaded`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2010-2011`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 931 |
| Loaded files | 931 |
| Failed files | 0 |
| Source bytes parsed | 2732835180 |
| Raw rows seen | 7590110 |
| DJF rows seen | 1900993 |
| Rejected source-code rows | 132644 |
| Valid DJF temperature rows | 1679023 |
| Invalid DJF temperature rows | 89319 |
| Rejected plausibility rows | 7 |
| Duplicate station-hour observations | 345378 |
| Canonical hourly rows staged | 1333645 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 55124384 |
| `weather.hourly_djf rows for this run (file audit)` | 1333645 |
| `loaded files for this run` | 931 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 1333645 |
| `invalid temp rows for this run` | 89319 |
| `rejected source rows for this run` | 132644 |
| `rejected plausibility rows for this run` | 7 |
| `duplicate hour count for this run` | 345378 |
| `audit.calculation_run` | 528 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
