# Station Selection Policy Review Worksheet

Generated UTC: 2026-06-25T01:59:40+00:00

## Run

- Worksheet run ID: `station_selection_policy_review_us_ca_core_20260625T015940Z`
- Source review run ID: `station_selection_review_seed_20260625T013744Z`
- Scenario ID: `us_ca_core`
- Scenario name: `US and Canada core`
- Code commit: `1a846a8f435119faf10e41d890d2c352fed650d8`
- Worksheet CSV: `station_selection_policy_review_us_ca_core_20260625T015940Z.csv`

## Policy

Accept US or Canadian stations within 75 km, rank <= 3, and coverage >= 0.97.

## Counts

| Metric | Rows |
| --- | ---: |
| Source review rows | 162 |
| Proposed accepted rows | 3 |
| Preserved as current disposition | 159 |

## Accepted Rows By Plant State

| Plant State | Rows |
| --- | ---: |
| `WA` | 3 |

## Accepted Rows By Station Country

| Station Country | Rows |
| --- | ---: |
| `CA` | 3 |

## Accepted Row QA Flags

| QA Flag | Rows |
| --- | ---: |
| `station_country_not_us` | 3 |
| `station_state_missing` | 3 |
| `selected_rank_gt_1` | 1 |

## Interpretation

- This file is a complete review worksheet for `scripts/apply_station_selection_review_updates.py`.
- Rows not qualifying under the policy keep blank proposed fields, which preserves their current disposition.
- Applying this worksheet changes only the station-selection review snapshot and derived release-readiness gate.
