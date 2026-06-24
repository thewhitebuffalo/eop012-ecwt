# Provisional Plant ECWT Report

Generated UTC: 2026-06-24T01:54:38+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `plant_ecwt_provisional_20260624T015403Z`
- Candidate run ID: `noaa_station_candidates_20260623T210132Z`
- Station ECWT run ID: `station_ecwt_loaded_20260624T015123Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `5ed115bce9078238739a56a5ced32e36af85befd`

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
| `minimum plant ECWT F` | -51.880 |
| `maximum plant ECWT F` | 65.138 |

## Coldest Provisional Plant ECWT Values

| Plant | State | Selected Station | Valid Hours | ECWT F | Status |
| --- | --- | --- | ---: | ---: | --- |
| 7-Mile Ridge Wind Project | AK | `999999-96404` | 10667 | -51.880 | provisional |
| Northway | AK | `999999-96404` | 10667 | -51.880 | provisional |
| Slana Generating Station | AK | `999999-96404` | 10667 | -51.880 | provisional |
| Tok | AK | `999999-96404` | 10667 | -51.880 | provisional |
| Ambler | AK | `999999-96407` | 9109 | -49.681 | provisional |
| Kiana | AK | `999999-96407` | 9109 | -49.681 | provisional |
| Noorvik | AK | `999999-96407` | 9109 | -49.681 | provisional |
| Selawik | AK | `999999-96407` | 9109 | -49.681 | provisional |
| Shungnak | AK | `999999-96407` | 9109 | -49.681 | provisional |
| NSB Kaktovik Utility | AK | `999999-26565` | 9337 | -49.599 | provisional |
| NSB Nuiqsut Utility | AK | `999999-26565` | 9337 | -49.599 | provisional |
| TNSG North Plant | AK | `999999-26565` | 9337 | -49.599 | provisional |
| TNSG South Plant | AK | `999999-26565` | 9337 | -49.599 | provisional |
| Galena Electric Utility | AK | `999999-96406` | 4770 | -49.000 | provisional |
| Eva Creek Wind | AK | `702610-26411` | 3551 | -45.886 | provisional |
| Kotlik | AK | `702628-00105` | 2305 | -41.800 | provisional |
| Marshall | AK | `702628-00105` | 2305 | -41.800 | provisional |
| Barrow | AK | `999999-27516` | 10782 | -40.900 | provisional |
| NSB Atqasuk Utility | AK | `999999-27516` | 10782 | -40.900 | provisional |
| NSB Wainwright Utility | AK | `999999-27516` | 10782 | -40.900 | provisional |

## Interpretation

- These are provisional plant-level ECWT values from the currently loaded canonical weather set.
- Selection chooses one currently usable candidate station per plant using valid-hour count, distance, and candidate rank.
- Results are blocked where no candidate station currently has provisional station ECWT.
- These rows are not final compliance publication values until NOAA coverage, source QA, and station-selection review are complete.
