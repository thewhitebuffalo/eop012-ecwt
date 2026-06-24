# Provisional Plant ECWT Report

Generated UTC: 2026-06-24T03:31:08+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `plant_ecwt_provisional_20260624T033019Z`
- Candidate run ID: `noaa_station_candidates_20260623T210132Z`
- Station ECWT run ID: `station_ecwt_loaded_20260624T032918Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `b68bd1d44aafc4d25f023da2cee212ba7c8bec71`

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
| `minimum plant ECWT F` | -51.480 |
| `maximum plant ECWT F` | 64.154 |

## Coldest Provisional Plant ECWT Values

| Plant | State | Selected Station | Valid Hours | ECWT F | Status |
| --- | --- | --- | ---: | ---: | --- |
| 7-Mile Ridge Wind Project | AK | `999999-96404` | 13611 | -51.480 | provisional |
| Northway | AK | `999999-96404` | 13611 | -51.480 | provisional |
| Slana Generating Station | AK | `999999-96404` | 13611 | -51.480 | provisional |
| Tok | AK | `999999-96404` | 13611 | -51.480 | provisional |
| Ambler | AK | `999999-96407` | 13262 | -50.706 | provisional |
| Kiana | AK | `999999-96407` | 13262 | -50.706 | provisional |
| Noorvik | AK | `999999-96407` | 13262 | -50.706 | provisional |
| Selawik | AK | `999999-96407` | 13262 | -50.706 | provisional |
| Shungnak | AK | `999999-96407` | 13262 | -50.706 | provisional |
| NSB Kaktovik Utility | AK | `999999-26565` | 11497 | -49.360 | provisional |
| NSB Nuiqsut Utility | AK | `999999-26565` | 11497 | -49.360 | provisional |
| TNSG North Plant | AK | `999999-26565` | 11497 | -49.360 | provisional |
| TNSG South Plant | AK | `999999-26565` | 11497 | -49.360 | provisional |
| Eva Creek Wind | AK | `702610-26411` | 4859 | -43.960 | provisional |
| Healy | AK | `702610-26411` | 4859 | -43.960 | provisional |
| Barrow | AK | `999999-27516` | 16983 | -42.700 | provisional |
| NSB Atqasuk Utility | AK | `999999-27516` | 16983 | -42.700 | provisional |
| NSB Wainwright Utility | AK | `999999-27516` | 16983 | -42.700 | provisional |
| Kotlik | AK | `702628-00105` | 4447 | -41.800 | provisional |
| Marshall | AK | `702628-00105` | 4447 | -41.800 | provisional |

## Interpretation

- These are provisional plant-level ECWT values from the currently loaded canonical weather set.
- Selection chooses one currently usable candidate station per plant using valid-hour count, distance, and candidate rank.
- Results are blocked where no candidate station currently has provisional station ECWT.
- These rows are not final compliance publication values until NOAA coverage, source QA, and station-selection review are complete.
