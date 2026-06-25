# Provisional Plant ECWT Report

Generated UTC: 2026-06-25T16:11:02+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `plant_ecwt_provisional_fixed_period_20260625T161041Z`
- Candidate run ID: `noaa_station_candidates_20260625T065445Z`
- Station ECWT run ID: `station_ecwt_loaded_20260625T155645Z`
- Coverage run ID: `station_year_djf_coverage_20260625T155613Z`
- Coverage table: `weather.station_year_djf_coverage_current`
- Selection coverage policy: `fixed-period`
- Fixed-period coverage years: `2000-2025`
- Fixed-period minimum coverage ratio: `0.95`
- Fixed-period minimum loaded years: `20`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `bd3c33c8073c2a66057773e07ae474d2b8eb9be4`

## Summary

| Relation or Check | Rows / Value |
| --- | ---: |
| `station selections` | 16132 |
| `provisional selections` | 1868 |
| `blocked selections` | 14264 |
| `selection segments` | 1868 |
| `plant ECWT rows` | 16132 |
| `provisional plant ECWT rows` | 1868 |
| `blocked plant ECWT rows` | 14264 |
| `minimum plant ECWT F` | -58.000 |
| `maximum plant ECWT F` | 30.200 |

## Coldest Provisional Plant ECWT Values

| Plant | State | Selected Station | Valid Hours | ECWT F | Status |
| --- | --- | --- | ---: | ---: | --- |
| 7-Mile Ridge Wind Project | AK | `719650-99999` | 54891 | -58.000 | provisional |
| Northway | AK | `719650-99999` | 54891 | -58.000 | provisional |
| Slana Generating Station | AK | `719650-99999` | 54891 | -58.000 | provisional |
| Tok | AK | `719650-99999` | 54891 | -58.000 | provisional |
| Yakutat | AK | `719650-99999` | 54891 | -58.000 | provisional |
| Gwitchyaa Zhee | AK | `719570-99999` | 55020 | -43.600 | provisional |
| NSB Kaktovik Utility | AK | `719570-99999` | 55020 | -43.600 | provisional |
| NSB Nuiqsut Utility | AK | `719570-99999` | 55020 | -43.600 | provisional |
| TNSG North Plant | AK | `719570-99999` | 55020 | -43.600 | provisional |
| TNSG South Plant | AK | `719570-99999` | 55020 | -43.600 | provisional |
| Angoon | AK | `712220-99999` | 54136 | -41.800 | provisional |
| Annex Creek | AK | `712220-99999` | 54136 | -41.800 | provisional |
| Auke Bay | AK | `712220-99999` | 54136 | -41.800 | provisional |
| Blue Lake Hydro | AK | `712220-99999` | 54136 | -41.800 | provisional |
| Goat Lake Hydro | AK | `712220-99999` | 54136 | -41.800 | provisional |
| Gold Creek | AK | `712220-99999` | 54136 | -41.800 | provisional |
| Green Lake | AK | `712220-99999` | 54136 | -41.800 | provisional |
| Gustavus | AK | `712220-99999` | 54136 | -41.800 | provisional |
| Haines | AK | `712220-99999` | 54136 | -41.800 | provisional |
| Hoonah | AK | `712220-99999` | 54136 | -41.800 | provisional |

## Interpretation

- These are provisional plant-level ECWT values from the currently loaded canonical weather set.
- Selection chooses one currently usable candidate station per plant using candidate rank and distance before valid-hour count.
- When `selection_coverage_policy` is `fixed-period`, candidates must also pass the fixed-period coverage gate before they are eligible for selection.
- Results are blocked where no candidate station currently has provisional station ECWT.
- These rows are not final compliance publication values until NOAA coverage, source QA, and station-selection review are complete.
