# Provisional Plant ECWT Report

Generated UTC: 2026-06-24T02:20:56+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `plant_ecwt_provisional_20260624T022025Z`
- Candidate run ID: `noaa_station_candidates_20260623T210132Z`
- Station ECWT run ID: `station_ecwt_loaded_20260624T021645Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `ec4f3e306097d39440575bdb79e8cabc99498898`

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
| `minimum plant ECWT F` | -51.574 |
| `maximum plant ECWT F` | 64.760 |

## Coldest Provisional Plant ECWT Values

| Plant | State | Selected Station | Valid Hours | ECWT F | Status |
| --- | --- | --- | ---: | ---: | --- |
| 7-Mile Ridge Wind Project | AK | `999999-96404` | 12850 | -51.574 | provisional |
| Northway | AK | `999999-96404` | 12850 | -51.574 | provisional |
| Slana Generating Station | AK | `999999-96404` | 12850 | -51.574 | provisional |
| Tok | AK | `999999-96404` | 12850 | -51.574 | provisional |
| Ambler | AK | `999999-96407` | 11103 | -50.980 | provisional |
| Kiana | AK | `999999-96407` | 11103 | -50.980 | provisional |
| Noorvik | AK | `999999-96407` | 11103 | -50.980 | provisional |
| Selawik | AK | `999999-96407` | 11103 | -50.980 | provisional |
| Shungnak | AK | `999999-96407` | 11103 | -50.980 | provisional |
| NSB Kaktovik Utility | AK | `999999-26565` | 10081 | -49.511 | provisional |
| NSB Nuiqsut Utility | AK | `999999-26565` | 10081 | -49.511 | provisional |
| TNSG North Plant | AK | `999999-26565` | 10081 | -49.511 | provisional |
| TNSG South Plant | AK | `999999-26565` | 10081 | -49.511 | provisional |
| Galena Electric Utility | AK | `999999-96406` | 4770 | -49.000 | provisional |
| Eva Creek Wind | AK | `702610-26411` | 3986 | -45.416 | provisional |
| Barrow | AK | `999999-27516` | 12671 | -43.060 | provisional |
| NSB Atqasuk Utility | AK | `999999-27516` | 12671 | -43.060 | provisional |
| NSB Wainwright Utility | AK | `999999-27516` | 12671 | -43.060 | provisional |
| Kotlik | AK | `702628-00105` | 2305 | -41.800 | provisional |
| Marshall | AK | `702628-00105` | 2305 | -41.800 | provisional |

## Interpretation

- These are provisional plant-level ECWT values from the currently loaded canonical weather set.
- Selection chooses one currently usable candidate station per plant using valid-hour count, distance, and candidate rank.
- Results are blocked where no candidate station currently has provisional station ECWT.
- These rows are not final compliance publication values until NOAA coverage, source QA, and station-selection review are complete.
