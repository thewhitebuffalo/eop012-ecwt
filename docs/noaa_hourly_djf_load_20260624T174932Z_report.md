# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-24T17:56:30+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260624T174932Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `c29c0a49ce6c391545b2dd5ab6fabda91eaf199a`
- Source selector: `downloaded`
- Limit files: `2000`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Years represented: `2016-2018`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 1629 |
| Loaded files | 1629 |
| Failed files | 0 |
| Source bytes parsed | 12849561361 |
| Raw rows seen | 29915004 |
| DJF rows seen | 7453452 |
| Rejected source-code rows | 3281822 |
| Valid DJF temperature rows | 3924190 |
| Invalid DJF temperature rows | 247440 |
| Rejected plausibility rows | 0 |
| Duplicate station-hour observations | 2431754 |
| Canonical hourly rows staged | 1492436 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf estimated total` | 45516536 |
| `weather.hourly_djf rows for this run (file audit)` | 1492436 |
| `loaded files for this run` | 1629 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 1492436 |
| `invalid temp rows for this run` | 247440 |
| `rejected source rows for this run` | 3281822 |
| `rejected plausibility rows for this run` | 0 |
| `duplicate hour count for this run` | 2431754 |
| `audit.calculation_run` | 389 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Configured rejected NOAA source codes are excluded before TMP interpretation.
- Rows outside the configured C range are excluded as physically implausible for canonical ECWT weather input.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
- This is now a canonical-load candidate, but final compliance publication still depends on station selection and ECWT method validation.
