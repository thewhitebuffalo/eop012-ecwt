# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-23T23:40:06+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260623T233448Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `c22cc01f4cb305ebb316c53a74ae66fb88dd50da`
- Source selector: `inventory`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `50.0`
- Years represented: `2022-2024`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 1000 |
| Loaded files | 1000 |
| Failed files | 0 |
| Source bytes parsed | 11427444453 |
| Raw rows seen | 26839145 |
| DJF rows seen | 6709812 |
| Rejected source-code rows | 1546626 |
| Valid DJF temperature rows | 4892638 |
| Invalid DJF temperature rows | 270548 |
| Rejected plausibility rows | 0 |
| Duplicate station-hour observations | 3741542 |
| Canonical hourly rows staged | 1151096 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf total` | 3803484 |
| `weather.hourly_djf rows for this run` | 1151096 |
| `loaded files for this run` | 1000 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 1151096 |
| `invalid temp rows for this run` | 270548 |
| `rejected source rows for this run` | 1546626 |
| `rejected plausibility rows for this run` | 0 |
| `duplicate hour count for this run` | 3741542 |
| `audit.calculation_run` | 43 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
