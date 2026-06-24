# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-24T07:10:28+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260624T070739Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `26b8fe67506d2ffc156a91dffd8029ebe333eb9c`
- Source selector: `downloaded`
- Limit files: `1000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2007-2008`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 546 |
| Loaded files | 546 |
| Failed files | 0 |
| Source bytes parsed | 3787302418 |
| Raw rows seen | 8610145 |
| DJF rows seen | 2162083 |
| Rejected source-code rows | 990909 |
| Valid DJF temperature rows | 1116091 |
| Invalid DJF temperature rows | 55081 |
| Rejected plausibility rows | 2 |
| Duplicate station-hour observations | 608947 |
| Canonical hourly rows staged | 507144 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 20720460 |
| `weather.hourly_djf rows for this run (file audit)` | 507144 |
| `loaded files for this run` | 546 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 507144 |
| `invalid temp rows for this run` | 55081 |
| `rejected source rows for this run` | 990909 |
| `rejected plausibility rows for this run` | 2 |
| `duplicate hour count for this run` | 608947 |
| `audit.calculation_run` | 201 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
