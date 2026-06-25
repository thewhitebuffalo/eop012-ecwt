# Provisional Plant ECWT Report

Generated UTC: 2026-06-25T07:01:58+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `plant_ecwt_provisional_fixed_period_20260625T070144Z`
- Candidate run ID: `noaa_station_candidates_20260625T065445Z`
- Station ECWT run ID: `station_ecwt_loaded_20260625T042423Z`
- Coverage run ID: `station_year_djf_coverage_20260625T035921Z`
- Selection coverage policy: `fixed-period`
- Fixed-period coverage years: `2000-2025`
- Fixed-period minimum coverage ratio: `0.95`
- Fixed-period minimum loaded years: `20`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `cfb92d09b8632116f082d29b78e2856c7157d9fa`

## Summary

| Relation or Check | Rows / Value |
| --- | ---: |
| `station selections` | 16132 |
| `provisional selections` | 1346 |
| `blocked selections` | 14786 |
| `selection segments` | 1346 |
| `plant ECWT rows` | 16132 |
| `provisional plant ECWT rows` | 1346 |
| `blocked plant ECWT rows` | 14786 |
| `minimum plant ECWT F` | -39.280 |
| `maximum plant ECWT F` | 10.400 |

## Coldest Provisional Plant ECWT Values

| Plant | State | Selected Station | Valid Hours | ECWT F | Status |
| --- | --- | --- | ---: | ---: | --- |
| Beartooth Energy Storage LLC | MT | `711370-99999` | 53866 | -39.280 | provisional |
| Colstrip | MT | `711370-99999` | 53866 | -39.280 | provisional |
| Colstrip Energy LP | MT | `711370-99999` | 53866 | -39.280 | provisional |
| Hardin Generator Project | MT | `711370-99999` | 53866 | -39.280 | provisional |
| Horse Thief Wind Project, LLC | MT | `711370-99999` | 53866 | -39.280 | provisional |
| J E Corette Plant | MT | `711370-99999` | 53866 | -39.280 | provisional |
| MTSUN | MT | `711370-99999` | 53866 | -39.280 | provisional |
| Magpie Solar, LLC | MT | `711370-99999` | 53866 | -39.280 | provisional |
| Phillips 66 Billings Refinery | MT | `711370-99999` | 53866 | -39.280 | provisional |
| South Dry Creek Hydro | MT | `711370-99999` | 53866 | -39.280 | provisional |
| South Mills Solar, LLC | MT | `711370-99999` | 53866 | -39.280 | provisional |
| Two Dot Wind Broadview East LLC | MT | `711370-99999` | 53866 | -39.280 | provisional |
| Western Sugar Cooperative - Billings | MT | `711370-99999` | 53866 | -39.280 | provisional |
| Yellowstone County Generating Station | MT | `711370-99999` | 53866 | -39.280 | provisional |
| Yellowstone Energy LP | MT | `711370-99999` | 53866 | -39.280 | provisional |
| Yellowtail | MT | `711370-99999` | 53866 | -39.280 | provisional |
| Aurora Wind Project | ND | `715160-99999` | 53520 | -32.800 | provisional |
| Big Fork | MT | `711540-99999` | 53709 | -32.800 | provisional |
| Bison Generation Station | ND | `715160-99999` | 53520 | -32.800 | provisional |
| Bowman Wind | ND | `715160-99999` | 53520 | -32.800 | provisional |

## Interpretation

- These are provisional plant-level ECWT values from the currently loaded canonical weather set.
- Selection chooses one currently usable candidate station per plant using candidate rank and distance before valid-hour count.
- When `selection_coverage_policy` is `fixed-period`, candidates must also pass the fixed-period coverage gate before they are eligible for selection.
- Results are blocked where no candidate station currently has provisional station ECWT.
- These rows are not final compliance publication values until NOAA coverage, source QA, and station-selection review are complete.
