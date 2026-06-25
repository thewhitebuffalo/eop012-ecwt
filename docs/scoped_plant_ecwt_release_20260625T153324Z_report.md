# Scoped Plant ECWT Dataset Export

- Release ID: `scoped_plant_ecwt_release_20260625T153324Z`
- Policy result run ID: `plant_ecwt_policy_result_all_plants_normalized_active_window_loaded_year_20260625T135248Z`
- Secondary fill run ID: `secondary_station_fill_ecwt_20260625T152742Z`
- Station ECWT run ID: `station_ecwt_loaded_20260625T124223Z`
- Dataset CSV: `/Users/Shared/EOP012/rebuild/data/processed/scoped_plant_ecwt_release_20260625T153324Z.csv`
- Exclusions CSV: `/Users/Shared/EOP012/rebuild/data/processed/scoped_plant_ecwt_release_20260625T153324Z_exclusions.csv`

## Scope

This export includes non-Alaska plant rows that are publication-ready under the normalized active-window loaded-year policy, plus rows made publication-ready by the documented secondary-station fill method. It excludes Alaska and the reviewed no-station edge cases from the current publication denominator.

## Row Counts

| Category | Rows |
| --- | ---: |
| Exported scoped ready rows | 15947 |
| Excluded rows | 185 |

## Export Method Counts

| Method Source | Rows |
| --- | ---: |
| `policy_result` | 15943 |
| `secondary_station_fill` | 4 |

## Exclusion Counts

| Exclusion Reason | Rows |
| --- | ---: |
| `alaska_excluded_by_scope` | 157 |
| `no_station_edge_case_excluded` | 28 |

## Largest State Counts In Export

| State | Rows |
| --- | ---: |
| `CA` | 2171 |
| `TX` | 1367 |
| `NY` | 1215 |
| `NC` | 985 |
| `MN` | 837 |
| `MA` | 700 |
| `IL` | 566 |
| `NJ` | 427 |
| `FL` | 400 |
| `CO` | 342 |
| `MI` | 332 |
| `IA` | 331 |
