# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-24T07:41:20+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260624T073851Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `164eec34fe3b7cc2b663811dd7e3de43d9e94ddd`
- Source selector: `downloaded`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2007-2007`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 519 |
| Loaded files | 519 |
| Failed files | 0 |
| Source bytes parsed | 4570697032 |
| Raw rows seen | 10271175 |
| DJF rows seen | 2576161 |
| Rejected source-code rows | 1042828 |
| Valid DJF temperature rows | 1493434 |
| Invalid DJF temperature rows | 39898 |
| Rejected plausibility rows | 1 |
| Duplicate station-hour observations | 952350 |
| Canonical hourly rows staged | 541084 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 23196608 |
| `weather.hourly_djf rows for this run (file audit)` | 541084 |
| `loaded files for this run` | 519 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 541084 |
| `invalid temp rows for this run` | 39898 |
| `rejected source rows for this run` | 1042828 |
| `rejected plausibility rows for this run` | 1 |
| `duplicate hour count for this run` | 952350 |
| `audit.calculation_run` | 209 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
