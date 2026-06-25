# Provisional Plant ECWT Report

Generated UTC: 2026-06-25T01:24:06+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `plant_ecwt_provisional_fixed_period_20260625T012402Z`
- Candidate run ID: `noaa_station_candidates_20260623T210132Z`
- Station ECWT run ID: `station_ecwt_loaded_20260625T004335Z`
- Coverage run ID: `station_year_djf_coverage_20260625T002229Z`
- Selection coverage policy: `fixed-period`
- Fixed-period coverage years: `2000-2025`
- Fixed-period minimum coverage ratio: `0.95`
- Fixed-period minimum loaded years: `20`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `d8aa9cfed64c5af96f8330223a12b1f5652676bb`

## Summary

| Relation or Check | Rows / Value |
| --- | ---: |
| `station selections` | 16132 |
| `provisional selections` | 162 |
| `blocked selections` | 15970 |
| `selection segments` | 162 |
| `plant ECWT rows` | 16132 |
| `provisional plant ECWT rows` | 162 |
| `blocked plant ECWT rows` | 15970 |
| `minimum plant ECWT F` | -32.800 |
| `maximum plant ECWT F` | 10.400 |

## Coldest Provisional Plant ECWT Values

| Plant | State | Selected Station | Valid Hours | ECWT F | Status |
| --- | --- | --- | ---: | ---: | --- |
| Big Fork | MT | `711540-99999` | 53709 | -32.800 | provisional |
| Culbertson Generation Station | MT | `715160-99999` | 53520 | -32.800 | provisional |
| Flathead Landfill to Gas Energy Facility | MT | `711540-99999` | 53709 | -32.800 | provisional |
| Fort Peck | MT | `715160-99999` | 53520 | -32.800 | provisional |
| Hungry Horse | MT | `711540-99999` | 53709 | -32.800 | provisional |
| OREG 1 Inc | MT | `715160-99999` | 53520 | -32.800 | provisional |
| OREG 2 Inc | MT | `715160-99999` | 53520 | -32.800 | provisional |
| Sand Creek Wind Farm | MT | `715160-99999` | 53520 | -32.800 | provisional |
| Stoltze CoGen1 | MT | `711540-99999` | 53709 | -32.800 | provisional |
| Border Winds Wind Farm | ND | `711480-99999` | 54106 | -31.000 | provisional |
| Langdon Renewables, LLC | ND | `711480-99999` | 54106 | -31.000 | provisional |
| Langdon Wind Energy Center | ND | `711480-99999` | 54106 | -31.000 | provisional |
| Langdon Wind II LLC | ND | `711480-99999` | 54106 | -31.000 | provisional |
| Walhalla | ND | `711470-99999` | 54621 | -31.000 | provisional |
| Tiber Dam Hydroelectric Plant | MT | `711160-99999` | 54242 | -28.573 | provisional |
| Aziscohos Hydroelectric Project | ME | `716100-99999` | 54507 | -25.600 | provisional |
| Kibby Wind Facility | ME | `716100-99999` | 54507 | -25.600 | provisional |
| ME Novel Lighthouse - Carrabassett | ME | `716100-99999` | 54507 | -25.600 | provisional |
| ReEnergy Stratton LLC | ME | `716100-99999` | 54507 | -25.600 | provisional |
| Brassua Hydroelectric Project | ME | `713230-99999` | 53726 | -24.160 | provisional |

## Interpretation

- These are provisional plant-level ECWT values from the currently loaded canonical weather set.
- Selection chooses one currently usable candidate station per plant using candidate rank and distance before valid-hour count.
- When `selection_coverage_policy` is `fixed-period`, candidates must also pass the fixed-period coverage gate before they are eligible for selection.
- Results are blocked where no candidate station currently has provisional station ECWT.
- These rows are not final compliance publication values until NOAA coverage, source QA, and station-selection review are complete.
