# Station Selection Policy Review Worksheet

Generated UTC: 2026-06-25T02:10:58+00:00

## Run

- Worksheet run ID: `station_selection_policy_review_us_ca_distance_cap_150_20260625T021058Z`
- Source review run ID: `station_selection_review_update_20260625T020542Z`
- Scenario ID: `us_ca_distance_cap_150`
- Scenario name: `US and Canada distance cap 150 km`
- Code commit: `05905b52bbc68d40247e103048db2937b21f9818`
- Worksheet CSV: `station_selection_policy_review_us_ca_distance_cap_150_20260625T021058Z.csv`
- Preserve current accepted rows: `True`

## Policy

Accept US or Canadian stations within 150 km, rank <= 10, and coverage >= 0.95.

## Counts

| Metric | Rows |
| --- | ---: |
| Source review rows | 162 |
| Current accepted rows | 108 |
| Newly proposed accepted rows | 54 |
| Accepted rows after applying worksheet | 162 |
| Preserved as current disposition | 108 |

## Accepted Rows After Applying Worksheet By Plant State

| Plant State | Rows |
| --- | ---: |
| `NY` | 52 |
| `UT` | 50 |
| `WA` | 23 |
| `MT` | 11 |
| `VT` | 10 |
| `ME` | 6 |
| `ND` | 5 |
| `ID` | 2 |
| `NV` | 2 |
| `MI` | 1 |

## Accepted Rows After Applying Worksheet By Station Country

| Station Country | Rows |
| --- | ---: |
| `CA` | 110 |
| `US` | 52 |

## Accepted Rows After Applying Worksheet QA Flags

| QA Flag | Rows |
| --- | ---: |
| `coverage_below_0_97` | 153 |
| `station_country_not_us` | 110 |
| `station_state_missing` | 110 |
| `selected_rank_gt_3` | 110 |
| `shared_station_gt_25_plants` | 93 |
| `distance_gt_75km` | 54 |
| `selected_rank_gt_1` | 44 |
| `distance_gt_50km` | 43 |
| `shared_station_gt_10_plants` | 11 |
| `plant_station_state_mismatch` | 2 |

## Interpretation

- This file is a complete review worksheet for `scripts/apply_station_selection_review_updates.py`.
- Rows not qualifying under the policy keep blank proposed fields, which preserves their current disposition.
- When current accepted rows are preserved, this worksheet layers the new policy onto unresolved rows without rewriting prior accepted dispositions.
- Applying this worksheet changes only the station-selection review snapshot and derived release-readiness gate.
