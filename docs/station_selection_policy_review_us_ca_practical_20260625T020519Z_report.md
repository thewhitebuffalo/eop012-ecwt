# Station Selection Policy Review Worksheet

Generated UTC: 2026-06-25T02:05:19+00:00

## Run

- Worksheet run ID: `station_selection_policy_review_us_ca_practical_20260625T020519Z`
- Source review run ID: `station_selection_review_update_20260625T015957Z`
- Scenario ID: `us_ca_practical`
- Scenario name: `US and Canada practical`
- Code commit: `97cd500d68a0d32f6cec41248a7c1c9f7d9fc19a`
- Worksheet CSV: `station_selection_policy_review_us_ca_practical_20260625T020519Z.csv`

## Policy

Accept US or Canadian stations within 75 km, rank <= 10, and coverage >= 0.95.

## Counts

| Metric | Rows |
| --- | ---: |
| Source review rows | 162 |
| Proposed accepted rows | 108 |
| Preserved as current disposition | 54 |

## Accepted Rows By Plant State

| Plant State | Rows |
| --- | ---: |
| `NY` | 43 |
| `UT` | 32 |
| `WA` | 15 |
| `VT` | 10 |
| `ND` | 5 |
| `ID` | 2 |
| `MI` | 1 |

## Accepted Rows By Station Country

| Station Country | Rows |
| --- | ---: |
| `CA` | 76 |
| `US` | 32 |

## Accepted Row QA Flags

| QA Flag | Rows |
| --- | ---: |
| `coverage_below_0_97` | 99 |
| `station_country_not_us` | 76 |
| `station_state_missing` | 76 |
| `shared_station_gt_25_plants` | 64 |
| `selected_rank_gt_3` | 61 |
| `distance_gt_50km` | 43 |
| `selected_rank_gt_1` | 39 |
| `shared_station_gt_10_plants` | 11 |

## Interpretation

- This file is a complete review worksheet for `scripts/apply_station_selection_review_updates.py`.
- Rows not qualifying under the policy keep blank proposed fields, which preserves their current disposition.
- Applying this worksheet changes only the station-selection review snapshot and derived release-readiness gate.
