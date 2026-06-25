# Provisional Plant ECWT Report

Generated UTC: 2026-06-25T12:17:42+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `plant_ecwt_provisional_20260625T121704Z`
- Candidate run ID: `noaa_station_candidates_20260625T065445Z`
- Station ECWT run ID: `station_ecwt_loaded_20260625T120444Z`
- Coverage run ID: `station_year_djf_coverage_20260625T120423Z`
- Coverage table: `weather.station_year_djf_coverage_current`
- Selection coverage policy: `active-window`
- Fixed-period coverage years: `2000-2025`
- Fixed-period minimum coverage ratio: `0.95`
- Fixed-period minimum loaded years: `20`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `1beb1b418f745a3b4ecd929433a29c492b3fee09`

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
| Northway | AK | `702910-26412` | 14732 | -54.400 | provisional |
| Tok | AK | `702910-26412` | 14732 | -54.400 | provisional |
| Source Power Company - Aldrich | NY | `711610-99999` | 31767 | -52.600 | provisional |
| McGrath | AK | `702310-26510` | 21654 | -50.980 | provisional |
| NSB Nuiqsut Utility | AK | `703644-27515` | 5747 | -50.800 | provisional |
| Noatak | AK | `701335-26648` | 6194 | -50.800 | provisional |
| Shungnak | AK | `701719-00490` | 11100 | -50.444 | provisional |
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
| TNSG North Plant | AK | `700637-27406` | 16471 | -47.200 | provisional |
| TNSG South Plant | AK | `700637-27406` | 16471 | -47.200 | provisional |

## Interpretation

- These are provisional plant-level ECWT values from the currently loaded canonical weather set.
- Selection chooses one currently usable candidate station per plant using candidate rank and distance before valid-hour count.
- When `selection_coverage_policy` is `fixed-period`, candidates must also pass the fixed-period coverage gate before they are eligible for selection.
- Results are blocked where no candidate station currently has provisional station ECWT.
- These rows are not final compliance publication values until NOAA coverage, source QA, and station-selection review are complete.
