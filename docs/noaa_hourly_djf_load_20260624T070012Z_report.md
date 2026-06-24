# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-24T07:06:41+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260624T070012Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `26b8fe67506d2ffc156a91dffd8029ebe333eb9c`
- Source selector: `inventory`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2014-2015`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 1000 |
| Loaded files | 1000 |
| Failed files | 0 |
| Source bytes parsed | 11890743817 |
| Raw rows seen | 28685130 |
| DJF rows seen | 7044139 |
| Rejected source-code rows | 1637727 |
| Valid DJF temperature rows | 5184345 |
| Invalid DJF temperature rows | 222064 |
| Rejected plausibility rows | 3 |
| Duplicate station-hour observations | 3973881 |
| Canonical hourly rows staged | 1210464 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 20720460 |
| `weather.hourly_djf rows for this run (file audit)` | 1210464 |
| `loaded files for this run` | 1000 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 1210464 |
| `invalid temp rows for this run` | 222064 |
| `rejected source rows for this run` | 1637727 |
| `rejected plausibility rows for this run` | 3 |
| `duplicate hour count for this run` | 3973881 |
| `audit.calculation_run` | 199 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
