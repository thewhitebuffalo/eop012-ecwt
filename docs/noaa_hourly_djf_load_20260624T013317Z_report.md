# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-24T01:49:09+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260624T013317Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `5ed115bce9078238739a56a5ced32e36af85befd`
- Source selector: `downloaded`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2010-2011`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 1000 |
| Loaded files | 1000 |
| Failed files | 0 |
| Source bytes parsed | 13221796335 |
| Raw rows seen | 32231991 |
| DJF rows seen | 7963917 |
| Rejected source-code rows | 1614964 |
| Valid DJF temperature rows | 6182788 |
| Invalid DJF temperature rows | 166165 |
| Rejected plausibility rows | 0 |
| Duplicate station-hour observations | 5079462 |
| Canonical hourly rows staged | 1103326 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf total` | 10668025 |
| `weather.hourly_djf rows for this run` | 1103326 |
| `loaded files for this run` | 1000 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 1103326 |
| `invalid temp rows for this run` | 166165 |
| `rejected source rows for this run` | 1614964 |
| `rejected plausibility rows for this run` | 0 |
| `duplicate hour count for this run` | 5079462 |
| `audit.calculation_run` | 89 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
