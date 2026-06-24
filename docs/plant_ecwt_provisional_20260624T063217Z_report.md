# Provisional Plant ECWT Report

Generated UTC: 2026-06-24T06:32:37+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `plant_ecwt_provisional_20260624T063217Z`
- Candidate run ID: `noaa_station_candidates_20260623T210132Z`
- Station ECWT run ID: `station_ecwt_loaded_20260624T063008Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `958969d0a3d5dc2746dba091f7bc527cec078cba`

## Summary

| Relation or Check | Rows / Value |
| --- | ---: |
| `station selections` | 16132 |
| `provisional selections` | 16104 |
| `blocked selections` | 28 |
| `selection segments` | 16104 |
| `plant ECWT rows` | 16132 |
| `provisional plant ECWT rows` | 16104 |
| `blocked plant ECWT rows` | 28 |
| `minimum plant ECWT F` | -56.200 |
| `maximum plant ECWT F` | 78.800 |

## Coldest Provisional Plant ECWT Values

| Plant | State | Selected Station | Valid Hours | ECWT F | Status |
| --- | --- | --- | ---: | ---: | --- |
| Gwitchyaa Zhee | AK | `701940-26413` | 12519 | -56.200 | provisional |
| Northway | AK | `702910-26412` | 3428 | -56.200 | provisional |
| Tok | AK | `702910-26412` | 3428 | -56.200 | provisional |
| Galena Electric Utility | AK | `702220-26501` | 1338 | -49.000 | provisional |
| McGrath | AK | `702310-26510` | 7725 | -49.000 | provisional |
| NSB Nuiqsut Utility | AK | `703644-27515` | 3673 | -49.000 | provisional |
| Eielson AFB Central Heat & Power Plant | AK | `702650-26407` | 1884 | -48.322 | provisional |
| North Pole | AK | `702650-26407` | 1884 | -48.322 | provisional |
| Battery Energy Storage System | AK | `702615-26498` | 1510 | -47.200 | provisional |
| Chena Power Plant | AK | `702615-26498` | 1510 | -47.200 | provisional |
| Fairbanks | AK | `702615-26498` | 1510 | -47.200 | provisional |
| Utility Plants Section | AK | `702615-26498` | 1510 | -47.200 | provisional |
| NSB Atqasuk Utility | AK | `702685-27518` | 1853 | -47.020 | provisional |
| University of Alaska Fairbanks | AK | `702610-26411` | 6507 | -45.940 | provisional |
| NSB Point Lay Utility | AK | `701210-26624` | 14445 | -45.400 | provisional |
| Shungnak | AK | `701719-00490` | 4757 | -45.400 | provisional |
| Barrow | AK | `700260-27502` | 5294 | -45.040 | provisional |
| Delta Power | AK | `702670-26415` | 7100 | -43.960 | provisional |
| Delta Wind Farm | AK | `702670-26415` | 7100 | -43.960 | provisional |
| Fort Greely Power Plant | AK | `702670-26415` | 7100 | -43.960 | provisional |

## Interpretation

- These are provisional plant-level ECWT values from the currently loaded canonical weather set.
- Selection chooses one currently usable candidate station per plant using candidate rank and distance before loaded valid-hour count.
- Results are blocked where no candidate station currently has provisional station ECWT.
- These rows are not final compliance publication values until NOAA coverage, source QA, and station-selection review are complete.
