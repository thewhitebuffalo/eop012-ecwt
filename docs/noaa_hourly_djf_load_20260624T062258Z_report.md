# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-24T06:25:43+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260624T062258Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `958969d0a3d5dc2746dba091f7bc527cec078cba`
- Source selector: `downloaded`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2008-2008`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 542 |
| Loaded files | 542 |
| Failed files | 0 |
| Source bytes parsed | 4944929434 |
| Raw rows seen | 11484316 |
| DJF rows seen | 2887307 |
| Rejected source-code rows | 1393999 |
| Valid DJF temperature rows | 1419566 |
| Invalid DJF temperature rows | 73741 |
| Rejected plausibility rows | 1 |
| Duplicate station-hour observations | 1030270 |
| Canonical hourly rows staged | 389296 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 20000640 |
| `weather.hourly_djf rows for this run (file audit)` | 389296 |
| `loaded files for this run` | 542 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 389296 |
| `invalid temp rows for this run` | 73741 |
| `rejected source rows for this run` | 1393999 |
| `rejected plausibility rows for this run` | 1 |
| `duplicate hour count for this run` | 1030270 |
| `audit.calculation_run` | 185 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
