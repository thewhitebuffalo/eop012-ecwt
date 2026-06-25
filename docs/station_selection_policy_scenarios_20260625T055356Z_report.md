# Station Selection Policy Scenario Report

Generated UTC: 2026-06-25T05:53:57+00:00

## Summary

This read-only report evaluates named policy scenarios against the current fixed-period station-selection review queue. It does not accept or reject any station assignment.

## Run

- Scenario run ID: `station_selection_policy_scenarios_20260625T055356Z`
- Source review run ID: `station_selection_review_seed_20260625T055346Z`
- Code commit: `683fea6a5ead106306b10578c639822119461f7d`
- Scenario summary CSV: `station_selection_policy_scenarios_20260625T055356Z.csv`
- Row-level scenario matrix CSV: `station_selection_policy_scenarios_20260625T055356Z_matrix.csv`

## Scenario Counts

| Scenario | Accepted | Blocked | Stations | Min Coverage | Max Distance km | Max Rank | Min ECWT F | Max ECWT F |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| current_gate | 0 | 162 | 0 |  |  |  |  |  |
| us_same_state_core | 0 | 162 | 0 |  |  |  |  |  |
| us_regional_core | 0 | 162 | 0 |  |  |  |  |  |
| us_fixed_gate_only | 52 | 110 | 1 | 0.951 | 149.459 | 10 | -9.940 | -9.940 |
| us_ca_core | 3 | 159 | 1 | 0.976 | 42.132 | 2 | 10.400 | 10.400 |
| us_ca_practical | 108 | 54 | 12 | 0.951 | 74.950 | 10 | -31 | 10.400 |
| us_ca_distance_cap_150 | 162 | 0 | 19 | 0.950 | 149.459 | 10 | -32.800 | 10.400 |
| fixed_coverage_only | 162 | 0 | 19 | 0.950 | 149.459 | 10 | -32.800 | 10.400 |

## QA Flag Inventory

| QA Flag | Rows |
| --- | --- |
| coverage_below_0_97 | 153 |
| station_country_not_us | 110 |
| station_state_missing | 110 |
| selected_rank_gt_3 | 110 |
| shared_station_gt_25_plants | 93 |
| distance_gt_75km | 54 |
| selected_rank_gt_1 | 44 |
| distance_gt_50km | 43 |
| shared_station_gt_10_plants | 11 |
| plant_station_state_mismatch | 2 |

## Interpretation

- `current_gate` matches the current release gate: no rows are accepted until review dispositions change.
- `fixed_coverage_only` is the mathematical upper bound from the current fixed-period candidate cohort.
- Scenarios that allow Canadian stations unlock most of the queue, but they are policy decisions, not data-quality facts.
- High-rank and long-distance fallbacks dominate the remaining decision surface. Those should be accepted only if the methodology explicitly allows them.
- To apply a policy, edit the review worksheet and run `scripts/apply_station_selection_review_updates.py` without `--dry-run`.
