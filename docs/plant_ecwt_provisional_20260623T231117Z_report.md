# Provisional Plant ECWT Report

Generated UTC: 2026-06-23T23:11:22+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `plant_ecwt_provisional_20260623T231117Z`
- Candidate run ID: `noaa_station_candidates_20260623T210132Z`
- Station ECWT run ID: `station_ecwt_loaded_20260623T230415Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `1992520b60f19f08c3f604d399c496be12ea7b39`

## Summary

| Relation or Check | Rows / Value |
| --- | ---: |
| `station selections` | 16132 |
| `provisional selections` | 15793 |
| `blocked selections` | 339 |
| `selection segments` | 15793 |
| `plant ECWT rows` | 16132 |
| `provisional plant ECWT rows` | 15793 |
| `blocked plant ECWT rows` | 339 |
| `minimum plant ECWT F` | -56.020 |
| `maximum plant ECWT F` | 56.074 |

## Coldest Provisional Plant ECWT Values

| Plant | State | Selected Station | Valid Hours | ECWT F | Status |
| --- | --- | --- | ---: | ---: | --- |
| Gwitchyaa Zhee | AK | `701940-26413` | 1279 | -56.020 | provisional |
| NSB Anaktuvuk Pass | AK | `703609-99999` | 3548 | -52.600 | provisional |
| Northway | AK | `719664-99999` | 3509 | -51.871 | provisional |
| Ambler | AK | `703655-26552` | 827 | -47.826 | provisional |
| Galena Electric Utility | AK | `703655-26552` | 827 | -47.826 | provisional |
| Shungnak | AK | `703655-26552` | 827 | -47.826 | provisional |
| Eva Creek Wind | AK | `702610-26411` | 1236 | -47.020 | provisional |
| Healy | AK | `702610-26411` | 1236 | -47.020 | provisional |
| McGrath | AK | `702310-26510` | 1678 | -47.020 | provisional |
| University of Alaska Fairbanks | AK | `702610-26411` | 1236 | -47.020 | provisional |
| NSB Kaktovik Utility | AK | `719780-99999` | 3502 | -45.040 | provisional |
| 7-Mile Ridge Wind Project | AK | `702670-26415` | 1363 | -44.506 | provisional |
| Battery Energy Storage System | AK | `702670-26415` | 1363 | -44.506 | provisional |
| Chena Power Plant | AK | `702670-26415` | 1363 | -44.506 | provisional |
| Delta Power | AK | `702670-26415` | 1363 | -44.506 | provisional |
| Delta Wind Farm | AK | `702670-26415` | 1363 | -44.506 | provisional |
| Eielson AFB Central Heat & Power Plant | AK | `702670-26415` | 1363 | -44.506 | provisional |
| Fairbanks | AK | `702670-26415` | 1363 | -44.506 | provisional |
| Fort Greely Power Plant | AK | `702670-26415` | 1363 | -44.506 | provisional |
| North Pole | AK | `702670-26415` | 1363 | -44.506 | provisional |

## Interpretation

- These are provisional plant-level ECWT values from the currently loaded canonical weather set.
- Selection chooses one currently usable candidate station per plant using valid-hour count, distance, and candidate rank.
- Results are blocked where no candidate station currently has provisional station ECWT.
- These rows are not final compliance publication values until NOAA coverage, source QA, and station-selection review are complete.
