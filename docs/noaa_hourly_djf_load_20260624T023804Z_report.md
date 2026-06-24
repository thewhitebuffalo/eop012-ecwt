# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-24T02:42:51+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260624T023804Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `4213bd46fec9f6cb2a66524316141c02cd69cf14`
- Source selector: `downloaded`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2010-2010`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 846 |
| Loaded files | 846 |
| Failed files | 0 |
| Source bytes parsed | 10288213956 |
| Raw rows seen | 25040041 |
| DJF rows seen | 6084830 |
| Rejected source-code rows | 1259675 |
| Valid DJF temperature rows | 4684884 |
| Invalid DJF temperature rows | 140271 |
| Rejected plausibility rows | 0 |
| Duplicate station-hour observations | 3772878 |
| Canonical hourly rows staged | 912006 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 11922827 |
| `weather.hourly_djf rows for this run (file audit)` | 912006 |
| `loaded files for this run` | 846 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 912006 |
| `invalid temp rows for this run` | 140271 |
| `rejected source rows for this run` | 1259675 |
| `rejected plausibility rows for this run` | 0 |
| `duplicate hour count for this run` | 3772878 |
| `audit.calculation_run` | 105 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
