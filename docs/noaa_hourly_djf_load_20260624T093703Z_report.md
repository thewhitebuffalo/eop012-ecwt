# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-24T09:42:30+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260624T093703Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `56e65ed883387568b9894bc05e20a1681dae8979`
- Source selector: `inventory`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2006-2012`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 1000 |
| Loaded files | 1000 |
| Failed files | 0 |
| Source bytes parsed | 9899007672 |
| Raw rows seen | 23547544 |
| DJF rows seen | 5887266 |
| Rejected source-code rows | 1439262 |
| Valid DJF temperature rows | 4331706 |
| Invalid DJF temperature rows | 116298 |
| Rejected plausibility rows | 0 |
| Duplicate station-hour observations | 3076990 |
| Canonical hourly rows staged | 1254716 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 28486288 |
| `weather.hourly_djf rows for this run (file audit)` | 1254716 |
| `loaded files for this run` | 1000 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 1254716 |
| `invalid temp rows for this run` | 116298 |
| `rejected source rows for this run` | 1439262 |
| `rejected plausibility rows for this run` | 0 |
| `duplicate hour count for this run` | 3076990 |
| `audit.calculation_run` | 247 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
