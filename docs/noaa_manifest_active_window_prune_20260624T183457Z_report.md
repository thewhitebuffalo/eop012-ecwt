# NOAA Backfill Manifest Active-Window Prune Report

Generated UTC: 2026-06-24T18:34:57+00:00

## Run

- Calculation run ID: `noaa_manifest_active_window_prune_20260624T183457Z`
- Manifest run ID: `noaa_backfill_manifest_20260623T215215Z`
- Dry run: `True`
- Methodology version: `eop012-ecwt-method-v0.1.0`

## Summary

| Metric | Count |
| --- | ---: |
| Planned rows before prune | 10839 |
| Rows with no station active DJF overlap | 7735 |
| Distinct stations affected | 2332 |
| Planned `999999-*` rows before prune | 1030 |
| `999999-*` rows skipped by active window | 648 |
| Candidate plant links represented by skipped rows | 257943 |

## Manifest Status After Prune

| Status | Rows |
| --- | ---: |
| `downloaded` | 32194 |
| `failed` | 10 |
| `missing` | 43796 |
| `planned` | 10839 |

## Sample Skipped Rows

| Station | Year | Name | State | First Observation | Last Observation | Candidate Links | Batch | Rank |
| --- | ---: | --- | --- | --- | --- | ---: | ---: | ---: |
| `723898-99999` | 2014 | HANFORD MUNI | CA | 1998-10-04 17:00:00-07 | 2005-12-30 16:00:00-08 | 315 | 78 | 77278 |
| `723898-99999` | 2013 | HANFORD MUNI | CA | 1998-10-04 17:00:00-07 | 2005-12-30 16:00:00-08 | 315 | 80 | 79643 |
| `723898-99999` | 2012 | HANFORD MUNI | CA | 1998-10-04 17:00:00-07 | 2005-12-30 16:00:00-08 | 315 | 83 | 82022 |
| `723898-99999` | 2006 | HANFORD MUNI | CA | 1998-10-04 17:00:00-07 | 2005-12-30 16:00:00-08 | 315 | 85 | 84444 |
| `749171-00479` | 2006 | TEHACHAPI MUNICIPAL AIRPORT | CA | 2009-12-08 16:00:00-08 | 2025-08-24 17:00:00-07 | 307 | 85 | 84445 |
| `723897-99999` | 2014 | FRESNO CHANDLER EXECUTIVE | CA | 2015-07-16 17:00:00-07 | 2025-08-23 17:00:00-07 | 290 | 78 | 77279 |
| `723897-99999` | 2013 | FRESNO CHANDLER EXECUTIVE | CA | 2015-07-16 17:00:00-07 | 2025-08-23 17:00:00-07 | 290 | 80 | 79644 |
| `723897-99999` | 2012 | FRESNO CHANDLER EXECUTIVE | CA | 2015-07-16 17:00:00-07 | 2025-08-23 17:00:00-07 | 290 | 83 | 82023 |
| `723897-99999` | 2006 | FRESNO CHANDLER EXECUTIVE | CA | 2015-07-16 17:00:00-07 | 2025-08-23 17:00:00-07 | 290 | 85 | 84446 |
| `744910-99999` | 2014 | CHICOPEE FALLS/WEST | MA | 1999-12-31 16:00:00-08 | 2004-12-30 16:00:00-08 | 286 | 78 | 77280 |
| `744910-99999` | 2013 | CHICOPEE FALLS/WEST | MA | 1999-12-31 16:00:00-08 | 2004-12-30 16:00:00-08 | 286 | 80 | 79645 |
| `744910-99999` | 2012 | CHICOPEE FALLS/WEST | MA | 1999-12-31 16:00:00-08 | 2004-12-30 16:00:00-08 | 286 | 83 | 82024 |
| `744910-99999` | 2006 | CHICOPEE FALLS/WEST | MA | 1999-12-31 16:00:00-08 | 2004-12-30 16:00:00-08 | 286 | 85 | 84447 |
| `723810-99999` | 2014 | EDWARDS AFB | CA | 1999-12-31 16:00:00-08 | 2004-12-30 16:00:00-08 | 277 | 78 | 77281 |
| `723810-99999` | 2013 | EDWARDS AFB | CA | 1999-12-31 16:00:00-08 | 2004-12-30 16:00:00-08 | 277 | 80 | 79646 |
| `723810-99999` | 2012 | EDWARDS AFB | CA | 1999-12-31 16:00:00-08 | 2004-12-30 16:00:00-08 | 277 | 83 | 82025 |
| `723810-99999` | 2006 | EDWARDS AFB | CA | 1999-12-31 16:00:00-08 | 2004-12-30 16:00:00-08 | 277 | 85 | 84448 |
| `725085-99999` | 2014 | ORANGE MUNI | MA | 1999-12-31 16:00:00-08 | 2003-12-30 16:00:00-08 | 263 | 78 | 77282 |
| `725085-99999` | 2013 | ORANGE MUNI | MA | 1999-12-31 16:00:00-08 | 2003-12-30 16:00:00-08 | 263 | 80 | 79647 |
| `725085-99999` | 2012 | ORANGE MUNI | MA | 1999-12-31 16:00:00-08 | 2003-12-30 16:00:00-08 | 263 | 83 | 82026 |
| `725085-99999` | 2006 | ORANGE MUNI | MA | 1999-12-31 16:00:00-08 | 2003-12-30 16:00:00-08 | 263 | 85 | 84449 |
| `745046-99999` | 2014 | MADERA MUNI | CA | 1999-01-13 16:00:00-08 | 2005-12-30 16:00:00-08 | 251 | 78 | 77283 |
| `745046-99999` | 2013 | MADERA MUNI | CA | 1999-01-13 16:00:00-08 | 2005-12-30 16:00:00-08 | 251 | 80 | 79648 |
| `745046-99999` | 2012 | MADERA MUNI | CA | 1999-01-13 16:00:00-08 | 2005-12-30 16:00:00-08 | 251 | 83 | 82027 |
| `745046-99999` | 2006 | MADERA MUNI | CA | 1999-01-13 16:00:00-08 | 2005-12-30 16:00:00-08 | 251 | 85 | 84450 |

## Interpretation

- A row is skipped only when station metadata proves there is no overlap with January-February or December for that source year.
- `999999-*` station IDs are not globally invalid. NOAA Global Hourly contains valid WBAN-only station files using the `999999` USAF placeholder.
- This prune prevents known out-of-active-window station-years from consuming public AWS requests while preserving valid `999999-*` stations.
