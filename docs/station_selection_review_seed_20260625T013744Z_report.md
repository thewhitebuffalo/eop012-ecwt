# Station Selection Review Seed and Release Readiness Gate

Generated UTC: 2026-06-25T01:37:48+00:00

## Summary

This run seeded `162` station-selection review rows for fixed-period publication candidates from readiness run `plant_ecwt_readiness_fixed_period_20260625T012416Z`. The seed is intentionally conservative: rows with any QA flag are `needs_review`, and only clean rows can be automatically accepted.

Release readiness now requires both upstream fixed-period ECWT readiness and an accepted station-selection review. Because the current fixed-period candidate set still has QA flags on every row, this run produces no release-ready rows.

## Run

- Review run ID: `station_selection_review_seed_20260625T013744Z`
- Readiness run ID: `plant_ecwt_readiness_fixed_period_20260625T012416Z`
- Code commit: `91145502c821e543323336ce687c37c724f7e0e9`
- Review CSV: `station_selection_review_seed_20260625T013744Z.csv`

## Review Status Counts

| Review Status | Rows |
| --- | --- |
| needs_review | 162 |

## Release Readiness Counts

| Release Status | Rows |
| --- | --- |
| blocked_readiness | 15,970 |
| blocked_station_review | 162 |

## Review Disposition Reasons

| Disposition Reason | Rows |
| --- | --- |
| needs_policy_cross_border_station | 110 |
| needs_review_near_threshold_coverage | 24 |
| needs_review_high_distance | 20 |
| needs_review_high_candidate_rank | 8 |

## QA Flag Counts

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

- `link.station_selection_review` is the auditable disposition layer for plant-to-station assignments.
- `publish.plant_ecwt_release_readiness` is the current release gate. It is stricter than `calc.plant_ecwt_readiness` because it blocks rows that have not been accepted by station-selection review.
- This run does not make policy decisions about cross-border, high-rank, high-distance, or near-threshold stations. It records them as review work.
- A future manual or policy-override run can update review dispositions to `accepted` or `rejected`, after which release readiness can be rebuilt.
