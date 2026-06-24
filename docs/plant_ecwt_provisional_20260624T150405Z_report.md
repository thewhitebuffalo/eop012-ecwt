# Provisional Plant ECWT Report

Generated UTC: 2026-06-24T15:05:39+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `plant_ecwt_provisional_20260624T150405Z`
- Candidate run ID: `noaa_station_candidates_20260623T210132Z`
- Station ECWT run ID: `station_ecwt_loaded_20260624T145908Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `d80e885cc20835d99a6bbc66a5156b02adb133e0`

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
| Gwitchyaa Zhee | AK | `701940-26413` | 27084 | -58.000 | provisional |
| Northway | AK | `702910-26412` | 12857 | -54.918 | provisional |
| Tok | AK | `702910-26412` | 12857 | -54.918 | provisional |
| Source Power Company - Aldrich | NY | `711610-99999` | 13631 | -53.500 | provisional |
| NSB Nuiqsut Utility | AK | `703644-27515` | 5747 | -50.800 | provisional |
| Noatak | AK | `701335-26648` | 5385 | -50.800 | provisional |
| McGrath | AK | `702310-26510` | 19512 | -49.000 | provisional |
| Selawik | AK | `700197-26558` | 5719 | -49.000 | provisional |
| Eielson AFB Central Heat & Power Plant | AK | `702650-26407` | 2638 | -48.721 | provisional |
| North Pole | AK | `702650-26407` | 2638 | -48.721 | provisional |
| Galena Electric Utility | AK | `702220-26501` | 5560 | -48.100 | provisional |
| Battery Energy Storage System | AK | `702615-26498` | 1667 | -47.200 | provisional |
| Chena Power Plant | AK | `702615-26498` | 1667 | -47.200 | provisional |
| Fairbanks | AK | `702615-26498` | 1667 | -47.200 | provisional |
| Kiana | AK | `701196-00102` | 12689 | -47.200 | provisional |
| NSB Point Lay Utility | AK | `701210-26624` | 27191 | -47.200 | provisional |
| Noorvik | AK | `704898-00113` | 8247 | -47.200 | provisional |
| TNSG North Plant | AK | `700637-27406` | 11404 | -47.200 | provisional |
| TNSG South Plant | AK | `700637-27406` | 11404 | -47.200 | provisional |
| Utility Plants Section | AK | `702615-26498` | 1667 | -47.200 | provisional |

## Interpretation

- These are provisional plant-level ECWT values from the currently loaded canonical weather set.
- Selection chooses one currently usable candidate station per plant using candidate rank and distance before loaded valid-hour count.
- Results are blocked where no candidate station currently has provisional station ECWT.
- These rows are not final compliance publication values until NOAA coverage, source QA, and station-selection review are complete.
