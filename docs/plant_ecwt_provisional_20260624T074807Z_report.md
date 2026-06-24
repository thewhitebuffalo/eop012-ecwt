# Provisional Plant ECWT Report

Generated UTC: 2026-06-24T07:48:33+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `plant_ecwt_provisional_20260624T074807Z`
- Candidate run ID: `noaa_station_candidates_20260623T210132Z`
- Station ECWT run ID: `station_ecwt_loaded_20260624T074509Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `164eec34fe3b7cc2b663811dd7e3de43d9e94ddd`

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
| `minimum plant ECWT F` | -58.000 |
| `maximum plant ECWT F` | 88.160 |

## Coldest Provisional Plant ECWT Values

| Plant | State | Selected Station | Valid Hours | ECWT F | Status |
| --- | --- | --- | ---: | ---: | --- |
| Gwitchyaa Zhee | AK | `701940-26413` | 15445 | -58.000 | provisional |
| Northway | AK | `702910-26412` | 3676 | -56.200 | provisional |
| Tok | AK | `702910-26412` | 3676 | -56.200 | provisional |
| McGrath | AK | `702310-26510` | 8720 | -49.000 | provisional |
| NSB Nuiqsut Utility | AK | `703644-27515` | 4140 | -49.000 | provisional |
| Eielson AFB Central Heat & Power Plant | AK | `702650-26407` | 2236 | -48.280 | provisional |
| North Pole | AK | `702650-26407` | 2236 | -48.280 | provisional |
| Galena Electric Utility | AK | `702220-26501` | 2247 | -48.100 | provisional |
| Battery Energy Storage System | AK | `702615-26498` | 1556 | -47.200 | provisional |
| Chena Power Plant | AK | `702615-26498` | 1556 | -47.200 | provisional |
| Fairbanks | AK | `702615-26498` | 1556 | -47.200 | provisional |
| Utility Plants Section | AK | `702615-26498` | 1556 | -47.200 | provisional |
| NSB Atqasuk Utility | AK | `702685-27518` | 1940 | -47.020 | provisional |
| University of Alaska Fairbanks | AK | `702610-26411` | 7348 | -45.940 | provisional |
| Shungnak | AK | `701719-00490` | 4757 | -45.400 | provisional |
| TNSG North Plant | AK | `700637-27406` | 2667 | -45.400 | provisional |
| TNSG South Plant | AK | `700637-27406` | 2667 | -45.400 | provisional |
| Barrow | AK | `700260-27502` | 5691 | -44.630 | provisional |
| Delta Power | AK | `702670-26415` | 8017 | -43.960 | provisional |
| Delta Wind Farm | AK | `702670-26415` | 8017 | -43.960 | provisional |

## Interpretation

- These are provisional plant-level ECWT values from the currently loaded canonical weather set.
- Selection chooses one currently usable candidate station per plant using candidate rank and distance before loaded valid-hour count.
- Results are blocked where no candidate station currently has provisional station ECWT.
- These rows are not final compliance publication values until NOAA coverage, source QA, and station-selection review are complete.
