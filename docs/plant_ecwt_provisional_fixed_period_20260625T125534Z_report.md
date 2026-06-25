# Provisional Plant ECWT Report

Generated UTC: 2026-06-25T12:55:54+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `plant_ecwt_provisional_fixed_period_20260625T125534Z`
- Candidate run ID: `noaa_station_candidates_20260625T065445Z`
- Station ECWT run ID: `station_ecwt_loaded_20260625T124223Z`
- Coverage run ID: `station_year_djf_coverage_20260625T124149Z`
- Coverage table: `weather.station_year_djf_coverage_current`
- Selection coverage policy: `fixed-period`
- Fixed-period coverage years: `2000-2025`
- Fixed-period minimum coverage ratio: `0.95`
- Fixed-period minimum loaded years: `20`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `41478111915114cd79294d0261f5b9fb6f936f5b`

## Summary

| Relation or Check | Rows / Value |
| --- | ---: |
| `station selections` | 16132 |
| `provisional selections` | 1641 |
| `blocked selections` | 14491 |
| `selection segments` | 1641 |
| `plant ECWT rows` | 16132 |
| `provisional plant ECWT rows` | 1641 |
| `blocked plant ECWT rows` | 14491 |
| `minimum plant ECWT F` | -54.400 |
| `maximum plant ECWT F` | 30.200 |

## Coldest Provisional Plant ECWT Values

| Plant | State | Selected Station | Valid Hours | ECWT F | Status |
| --- | --- | --- | ---: | ---: | --- |
| Annex Creek | AK | `719530-99999` | 54926 | -54.400 | provisional |
| Auke Bay | AK | `719530-99999` | 54926 | -54.400 | provisional |
| Goat Lake Hydro | AK | `719530-99999` | 54926 | -54.400 | provisional |
| Gold Creek | AK | `719530-99999` | 54926 | -54.400 | provisional |
| Gustavus | AK | `719530-99999` | 54926 | -54.400 | provisional |
| Haines | AK | `719530-99999` | 54926 | -54.400 | provisional |
| Hoonah | AK | `719530-99999` | 54926 | -54.400 | provisional |
| Industrial Plant | AK | `719530-99999` | 54926 | -54.400 | provisional |
| Kasidaya Creek Hydro | AK | `719530-99999` | 54926 | -54.400 | provisional |
| Lake Dorothy Hydroelectric Project | AK | `719530-99999` | 54926 | -54.400 | provisional |
| Lemon Creek | AK | `719530-99999` | 54926 | -54.400 | provisional |
| Pelican | AK | `719530-99999` | 54926 | -54.400 | provisional |
| Salmon Creek 1 | AK | `719530-99999` | 54926 | -54.400 | provisional |
| Skagway | AK | `719530-99999` | 54926 | -54.400 | provisional |
| Snettisham | AK | `719530-99999` | 54926 | -54.400 | provisional |
| Sweetheart Lake Hydroelectric Facility | AK | `719530-99999` | 54926 | -54.400 | provisional |
| Gwitchyaa Zhee | AK | `719570-99999` | 55020 | -43.600 | provisional |
| NSB Kaktovik Utility | AK | `719570-99999` | 55020 | -43.600 | provisional |
| NSB Nuiqsut Utility | AK | `719570-99999` | 55020 | -43.600 | provisional |
| TNSG North Plant | AK | `719570-99999` | 55020 | -43.600 | provisional |

## Interpretation

- These are provisional plant-level ECWT values from the currently loaded canonical weather set.
- Selection chooses one currently usable candidate station per plant using candidate rank and distance before valid-hour count.
- When `selection_coverage_policy` is `fixed-period`, candidates must also pass the fixed-period coverage gate before they are eligible for selection.
- Results are blocked where no candidate station currently has provisional station ECWT.
- These rows are not final compliance publication values until NOAA coverage, source QA, and station-selection review are complete.
