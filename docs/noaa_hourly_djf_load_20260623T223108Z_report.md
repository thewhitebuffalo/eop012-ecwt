# NOAA DJF Hourly Load Report

Generated UTC: 2026-06-23T22:33:49+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `noaa_hourly_djf_load_20260623T223108Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `85bf909850aa30b2ed11597e083fcdb4b9fc4b78`
- Source selector: `inventory`
- Limit files: `500`
- Years represented: `2024-2024`

## Results

| Metric | Count |
| --- | ---: |
| Candidate files selected | 500 |
| Loaded files | 500 |
| Failed files | 0 |
| Source bytes parsed | 4094174587 |
| Raw rows seen | 9653827 |
| DJF rows seen | 2429648 |
| Valid DJF temperature rows | 2382401 |
| Invalid DJF temperature rows | 47247 |
| Duplicate station-hour observations | 1411328 |
| Canonical hourly rows staged | 971073 |

## Database Row Counts

| Relation or Check | Rows / Value |
| --- | ---: |
| `weather.hourly_djf total` | 1465923 |
| `weather.hourly_djf rows for this run` | 971073 |
| `loaded files for this run` | 500 |
| `failed files for this run` | 0 |
| `loaded hour count for this run` | 971073 |
| `invalid temp rows for this run` | 47247 |
| `duplicate hour count for this run` | 1411328 |
| `audit.calculation_run` | 13 |

## Interpretation

- This loader populates `weather.hourly_djf`, not the final ECWT tables.
- `TMP` values are parsed as tenths of degrees C; `+9999` and quality code `9` are treated as invalid.
- Multiple valid observations in the same station-hour are collapsed to one canonical hour using quality, report type, and closeness to minute 56.
- The timestamp policy for this run is: canonical hour = NOAA observation timestamp floored to the UTC hour.
