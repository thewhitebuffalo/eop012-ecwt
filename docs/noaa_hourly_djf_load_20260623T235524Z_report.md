# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-24T00:02:31+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260623T235524Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `21e5e54ae61f56d12f48645a7965047ed330fe01`
- Source selector: `inventory`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2022-2022`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 1000 |
| Loaded files | 1000 |
| Failed files | 0 |
| Source bytes parsed | 7969946335 |
| Raw rows seen | 16578472 |
| DJF rows seen | 4166220 |
| Rejected source-code rows | 3470874 |
| Valid DJF temperature rows | 623555 |
| Invalid DJF temperature rows | 71791 |
| Rejected plausibility rows | 0 |
| Duplicate station-hour observations | 310943 |
| Canonical hourly rows staged | 312612 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf total` | 4667615 |
| `weather.hourly_djf rows for this run` | 312612 |
| `loaded files for this run` | 1000 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 312612 |
| `invalid temp rows for this run` | 71791 |
| `rejected source rows for this run` | 3470874 |
| `rejected plausibility rows for this run` | 0 |
| `duplicate hour count for this run` | 310943 |
| `audit.calculation_run` | 55 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
