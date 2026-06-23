# Provisional Plant ECWT Report

Generated UTC: 2026-06-23T23:23:58+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `plant_ecwt_provisional_20260623T232311Z`
- Candidate run ID: `noaa_station_candidates_20260623T210132Z`
- Station ECWT run ID: `station_ecwt_loaded_20260623T232301Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `1992520b60f19f08c3f604d399c496be12ea7b39`

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
| `minimum plant ECWT F` | -52.600 |
| `maximum plant ECWT F` | 68.290 |

## Coldest Provisional Plant ECWT Values

| Plant | State | Selected Station | Valid Hours | ECWT F | Status |
| --- | --- | --- | ---: | ---: | --- |
| NSB Anaktuvuk Pass | AK | `703609-99999` | 3548 | -52.600 | provisional |
| Northway | AK | `719664-99999` | 3509 | -51.871 | provisional |
| Galena Electric Utility | AK | `999999-96406` | 1416 | -49.241 | provisional |
| Ambler | AK | `999999-96407` | 1416 | -47.231 | provisional |
| Shungnak | AK | `999999-96407` | 1416 | -47.231 | provisional |
| McGrath | AK | `702310-26510` | 1678 | -47.020 | provisional |
| Eva Creek Wind | AK | `702610-26411` | 1822 | -46.327 | provisional |
| Healy | AK | `702610-26411` | 1822 | -46.327 | provisional |
| University of Alaska Fairbanks | AK | `702610-26411` | 1822 | -46.327 | provisional |
| NSB Kaktovik Utility | AK | `719780-99999` | 3502 | -45.040 | provisional |
| NaturEner Rim Rock Energy | MT | `712440-99999` | 3417 | -44.411 | provisional |
| Yakutat | AK | `710010-99999` | 3516 | -43.218 | provisional |
| 7-Mile Ridge Wind Project | AK | `702670-26415` | 1917 | -42.313 | provisional |
| Battery Energy Storage System | AK | `702670-26415` | 1917 | -42.313 | provisional |
| Chena Power Plant | AK | `702670-26415` | 1917 | -42.313 | provisional |
| Delta Power | AK | `702670-26415` | 1917 | -42.313 | provisional |
| Delta Wind Farm | AK | `702670-26415` | 1917 | -42.313 | provisional |
| Eielson AFB Central Heat & Power Plant | AK | `702670-26415` | 1917 | -42.313 | provisional |
| Fairbanks | AK | `702670-26415` | 1917 | -42.313 | provisional |
| Fort Greely Power Plant | AK | `702670-26415` | 1917 | -42.313 | provisional |

## Interpretation

- These are provisional plant-level ECWT values from the currently loaded canonical weather set.
- Selection chooses one currently usable candidate station per plant using valid-hour count, distance, and candidate rank.
- Results are blocked where no candidate station currently has provisional station ECWT.
- These rows are not final compliance publication values until NOAA coverage, source QA, and station-selection review are complete.
