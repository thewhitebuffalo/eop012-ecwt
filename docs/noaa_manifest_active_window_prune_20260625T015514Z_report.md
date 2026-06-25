# NOAA Backfill Manifest Active-Window Prune Report

Generated UTC: 2026-06-25T01:55:32+00:00

## Run

- Calculation run ID: `noaa_manifest_active_window_prune_20260625T015514Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Dry run: `False`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Target statuses: `planned, missing, failed`

## Summary

| Metric | Count |
| --- | ---: |
| Target-status rows before prune | 44347 |
| Target-status rows with no station active DJF overlap | 41216 |
| Distinct stations affected | 3630 |
| All manifest rows with no station active DJF overlap | 49085 |
| Downloaded rows with no station active DJF overlap | 134 |
| Target-status `999999-*` rows before prune | 3832 |
| `999999-*` rows skipped by active window | 3587 |
| Candidate plant links represented by skipped rows | 1467686 |

## Manifest Status After Prune

| Status | Rows |
| --- | ---: |
| `downloaded` | 34757 |
| `missing` | 3131 |
| `skipped` | 48951 |

## Sample Skipped Rows

| Station | Year | Previous Status | Name | State | First Observation | Last Observation | Candidate Links | Batch | Rank |
| --- | ---: | --- | --- | --- | --- | --- | ---: | ---: | ---: |
| `723898-99999` | 2025 | `missing` | HANFORD MUNI | CA | 1998-10-04 17:00:00-07 | 2005-12-30 16:00:00-08 | 315 | 1 | 1 |
| `723898-99999` | 2023 | `missing` | HANFORD MUNI | CA | 1998-10-04 17:00:00-07 | 2005-12-30 16:00:00-08 | 315 | 5 | 4401 |
| `723898-99999` | 2011 | `missing` | HANFORD MUNI | CA | 1998-10-04 17:00:00-07 | 2005-12-30 16:00:00-08 | 315 | 9 | 8801 |
| `723898-99999` | 2010 | `missing` | HANFORD MUNI | CA | 1998-10-04 17:00:00-07 | 2005-12-30 16:00:00-08 | 315 | 14 | 13201 |
| `723898-99999` | 2009 | `missing` | HANFORD MUNI | CA | 1998-10-04 17:00:00-07 | 2005-12-30 16:00:00-08 | 315 | 18 | 17601 |
| `723898-99999` | 2008 | `missing` | HANFORD MUNI | CA | 1998-10-04 17:00:00-07 | 2005-12-30 16:00:00-08 | 315 | 23 | 22001 |
| `723898-99999` | 2007 | `missing` | HANFORD MUNI | CA | 1998-10-04 17:00:00-07 | 2005-12-30 16:00:00-08 | 315 | 27 | 26401 |
| `723898-99999` | 2024 | `missing` | HANFORD MUNI | CA | 1998-10-04 17:00:00-07 | 2005-12-30 16:00:00-08 | 315 | 58 | 57201 |
| `723898-99999` | 2022 | `missing` | HANFORD MUNI | CA | 1998-10-04 17:00:00-07 | 2005-12-30 16:00:00-08 | 315 | 59 | 58761 |
| `723898-99999` | 2021 | `missing` | HANFORD MUNI | CA | 1998-10-04 17:00:00-07 | 2005-12-30 16:00:00-08 | 315 | 62 | 61178 |
| `723898-99999` | 2020 | `missing` | HANFORD MUNI | CA | 1998-10-04 17:00:00-07 | 2005-12-30 16:00:00-08 | 315 | 64 | 63605 |
| `723898-99999` | 2019 | `missing` | HANFORD MUNI | CA | 1998-10-04 17:00:00-07 | 2005-12-30 16:00:00-08 | 315 | 67 | 66027 |
| `723898-99999` | 2018 | `missing` | HANFORD MUNI | CA | 1998-10-04 17:00:00-07 | 2005-12-30 16:00:00-08 | 315 | 69 | 68459 |
| `723898-99999` | 2017 | `missing` | HANFORD MUNI | CA | 1998-10-04 17:00:00-07 | 2005-12-30 16:00:00-08 | 315 | 71 | 70886 |
| `723898-99999` | 2016 | `missing` | HANFORD MUNI | CA | 1998-10-04 17:00:00-07 | 2005-12-30 16:00:00-08 | 315 | 74 | 73182 |
| `723898-99999` | 2015 | `missing` | HANFORD MUNI | CA | 1998-10-04 17:00:00-07 | 2005-12-30 16:00:00-08 | 315 | 76 | 75715 |
| `725100-94746` | 2004 | `missing` | WORCESTER REGIONAL AIRPORT | MA | 2004-12-31 16:00:00-08 | 2025-08-25 17:00:00-07 | 312 | 36 | 35202 |
| `725100-94746` | 2003 | `missing` | WORCESTER REGIONAL AIRPORT | MA | 2004-12-31 16:00:00-08 | 2025-08-25 17:00:00-07 | 312 | 40 | 39602 |
| `725100-94746` | 2002 | `missing` | WORCESTER REGIONAL AIRPORT | MA | 2004-12-31 16:00:00-08 | 2025-08-25 17:00:00-07 | 312 | 45 | 44002 |
| `725100-94746` | 2001 | `missing` | WORCESTER REGIONAL AIRPORT | MA | 2004-12-31 16:00:00-08 | 2025-08-25 17:00:00-07 | 312 | 49 | 48402 |
| `725100-94746` | 2000 | `missing` | WORCESTER REGIONAL AIRPORT | MA | 2004-12-31 16:00:00-08 | 2025-08-25 17:00:00-07 | 312 | 53 | 52802 |
| `722953-03183` | 2005 | `missing` | MOJAVE AIRPORT | CA | 2006-01-01 16:00:00-08 | 2025-08-24 17:00:00-07 | 309 | 31 | 30803 |
| `722953-03183` | 2004 | `missing` | MOJAVE AIRPORT | CA | 2006-01-01 16:00:00-08 | 2025-08-24 17:00:00-07 | 309 | 36 | 35203 |
| `722953-03183` | 2003 | `missing` | MOJAVE AIRPORT | CA | 2006-01-01 16:00:00-08 | 2025-08-24 17:00:00-07 | 309 | 40 | 39603 |
| `722953-03183` | 2002 | `missing` | MOJAVE AIRPORT | CA | 2006-01-01 16:00:00-08 | 2025-08-24 17:00:00-07 | 309 | 45 | 44003 |
| `722953-03183` | 2001 | `missing` | MOJAVE AIRPORT | CA | 2006-01-01 16:00:00-08 | 2025-08-24 17:00:00-07 | 309 | 49 | 48403 |
| `722953-03183` | 2000 | `missing` | MOJAVE AIRPORT | CA | 2006-01-01 16:00:00-08 | 2025-08-24 17:00:00-07 | 309 | 53 | 52803 |
| `749171-00479` | 2008 | `missing` | TEHACHAPI MUNICIPAL AIRPORT | CA | 2009-12-08 16:00:00-08 | 2025-08-24 17:00:00-07 | 307 | 23 | 22004 |
| `749171-00479` | 2007 | `missing` | TEHACHAPI MUNICIPAL AIRPORT | CA | 2009-12-08 16:00:00-08 | 2025-08-24 17:00:00-07 | 307 | 27 | 26404 |
| `749171-00479` | 2005 | `missing` | TEHACHAPI MUNICIPAL AIRPORT | CA | 2009-12-08 16:00:00-08 | 2025-08-24 17:00:00-07 | 307 | 31 | 30804 |

## Interpretation

- A row is skipped only when station metadata proves there is no overlap with January-February or December for that source year.
- By default this repairs `planned`, `missing`, and `failed` rows. `downloaded` rows are counted but not reclassified unless explicitly requested, because the download-attempt audit still truthfully records a fetched raw object.
- `999999-*` station IDs are not globally invalid. NOAA Global Hourly contains valid WBAN-only station files using the `999999` USAF placeholder.
- This prune prevents known out-of-active-window station-years from consuming public AWS requests while preserving valid `999999-*` stations.
