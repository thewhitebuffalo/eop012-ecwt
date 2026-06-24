# Provisional Plant ECWT Report

Generated UTC: 2026-06-24T00:11:09+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `plant_ecwt_provisional_20260624T001040Z`
- Candidate run ID: `noaa_station_candidates_20260623T210132Z`
- Station ECWT run ID: `station_ecwt_loaded_20260624T000839Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `21e5e54ae61f56d12f48645a7965047ed330fe01`

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
| `maximum plant ECWT F` | 67.640 |

## Coldest Provisional Plant ECWT Values

| Plant | State | Selected Station | Valid Hours | ECWT F | Status |
| --- | --- | --- | ---: | ---: | --- |
| NSB Anaktuvuk Pass | AK | `703609-99999` | 4290 | -52.600 | provisional |
| Northway | AK | `719664-99999` | 5628 | -50.574 | provisional |
| Ambler | AK | `999999-96407` | 3581 | -50.411 | provisional |
| Kiana | AK | `999999-96407` | 3581 | -50.411 | provisional |
| Noorvik | AK | `999999-96407` | 3581 | -50.411 | provisional |
| Selawik | AK | `999999-96407` | 3581 | -50.411 | provisional |
| Shungnak | AK | `999999-96407` | 3581 | -50.411 | provisional |
| Galena Electric Utility | AK | `999999-96406` | 2610 | -49.000 | provisional |
| 7-Mile Ridge Wind Project | AK | `999999-96404` | 3581 | -46.782 | provisional |
| Slana Generating Station | AK | `999999-96404` | 3581 | -46.782 | provisional |
| Tok | AK | `999999-96404` | 3581 | -46.782 | provisional |
| NSB Kaktovik Utility | AK | `719770-99999` | 5624 | -46.660 | provisional |
| Eva Creek Wind | AK | `702610-26411` | 2244 | -45.940 | provisional |
| Healy | AK | `702610-26411` | 2244 | -45.940 | provisional |
| Bridgewater Power LP | NH | `726130-14755` | 4582 | -45.400 | provisional |
| CED Denmark Solar Hybrid | ME | `726130-14755` | 4582 | -45.400 | provisional |
| Fryeburg | ME | `726130-14755` | 4582 | -45.400 | provisional |
| Groton Wind LLC | NH | `726130-14755` | 4582 | -45.400 | provisional |
| Hiram | ME | `726130-14755` | 4582 | -45.400 | provisional |
| ISM Solar Shepherd Acres | ME | `726130-14755` | 4582 | -45.400 | provisional |

## Interpretation

- These are provisional plant-level ECWT values from the currently loaded canonical weather set.
- Selection chooses one currently usable candidate station per plant using valid-hour count, distance, and candidate rank.
- Results are blocked where no candidate station currently has provisional station ECWT.
- These rows are not final compliance publication values until NOAA coverage, source QA, and station-selection review are complete.
