# Provisional Plant ECWT Report

Generated UTC: 2026-06-24T04:30:25+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `plant_ecwt_provisional_20260624T043007Z`
- Candidate run ID: `noaa_station_candidates_20260623T210132Z`
- Station ECWT run ID: `station_ecwt_loaded_20260624T042844Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `779eaf7545abcd2f6a8dbbc11beb1f7b28a275d4`

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
| `minimum plant ECWT F` | -51.160 |
| `maximum plant ECWT F` | 64.220 |

## Coldest Provisional Plant ECWT Values

| Plant | State | Selected Station | Valid Hours | ECWT F | Status |
| --- | --- | --- | ---: | ---: | --- |
| 7-Mile Ridge Wind Project | AK | `999999-96404` | 15027 | -51.160 | provisional |
| Northway | AK | `999999-96404` | 15027 | -51.160 | provisional |
| Slana Generating Station | AK | `999999-96404` | 15027 | -51.160 | provisional |
| Tok | AK | `999999-96404` | 15027 | -51.160 | provisional |
| Ambler | AK | `999999-96407` | 15422 | -50.288 | provisional |
| Kiana | AK | `999999-96407` | 15422 | -50.288 | provisional |
| Noorvik | AK | `999999-96407` | 15422 | -50.288 | provisional |
| Selawik | AK | `999999-96407` | 15422 | -50.288 | provisional |
| Shungnak | AK | `999999-96407` | 15422 | -50.288 | provisional |
| NSB Kaktovik Utility | AK | `999999-26565` | 13657 | -49.180 | provisional |
| NSB Nuiqsut Utility | AK | `999999-26565` | 13657 | -49.180 | provisional |
| TNSG North Plant | AK | `999999-26565` | 13657 | -49.180 | provisional |
| TNSG South Plant | AK | `999999-26565` | 13657 | -49.180 | provisional |
| Eva Creek Wind | AK | `702610-26411` | 5712 | -45.940 | provisional |
| Healy | AK | `702610-26411` | 5712 | -45.940 | provisional |
| Barrow | AK | `999999-27516` | 19143 | -42.700 | provisional |
| NSB Atqasuk Utility | AK | `999999-27516` | 19143 | -42.700 | provisional |
| NSB Wainwright Utility | AK | `999999-27516` | 19143 | -42.700 | provisional |
| Kotlik | AK | `702628-00105` | 4447 | -41.800 | provisional |
| Marshall | AK | `702628-00105` | 4447 | -41.800 | provisional |

## Interpretation

- These are provisional plant-level ECWT values from the currently loaded canonical weather set.
- Selection chooses one currently usable candidate station per plant using valid-hour count, distance, and candidate rank.
- Results are blocked where no candidate station currently has provisional station ECWT.
- These rows are not final compliance publication values until NOAA coverage, source QA, and station-selection review are complete.
