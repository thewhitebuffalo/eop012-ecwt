# Plant ECWT Release-Ready Export Report

Generated UTC: 2026-06-25T02:02:25+00:00

## Run

- Export run ID: `plant_ecwt_release_ready_20260625T020225Z`
- Release ID: `preview-plant_ecwt_release_ready_20260625T020225Z`
- Code commit: `1a846a8f435119faf10e41d890d2c352fed650d8`
- Release gate run ID: `station_selection_review_update_20260625T015957Z`
- CSV preview: `plant_ecwt_release_ready_20260625T020225Z.csv`

## Summary

| Metric | Count |
| --- | ---: |
| Exported release-ready rows | 3 |
| Distinct plant states | 1 |
| Distinct selected stations | 1 |

## Full Release Gate Counts

| Release Status | Reason | Rows |
| --- | --- | --- |
| blocked_readiness | upstream_no_candidate_station_with_provisional_ecwt | 15970 |
| blocked_station_review | needs_policy_cross_border_station | 107 |
| blocked_station_review | needs_review_high_candidate_rank | 8 |
| blocked_station_review | needs_review_high_distance | 20 |
| blocked_station_review | needs_review_near_threshold_coverage | 24 |
| release_ready | station_selection_review_accepted | 3 |

## Exported Rows By Plant State

| State | Rows |
| --- | --- |
| WA | 3 |

## Exported Rows By Station Country

| Country | Rows |
| --- | --- |
| CA | 3 |

## Exported Rows By Review Basis

| Review Basis | Rows |
| --- | --- |
| policy_override | 3 |

## Coldest Exported Plant ECWT Values

| Plant | State | Station | Governing ECWT F | Coverage |
| --- | --- | --- | --- | --- |
| Sumas Power Plant | WA | 711080-99999 | 10.400 | 0.976406 |
| Nooksack Hydro | WA | 711080-99999 | 10.400 | 0.976406 |
| Glacier Battery Storage | WA | 711080-99999 | 10.400 | 0.976406 |

## Warmest Exported Plant ECWT Values

| Plant | State | Station | Governing ECWT F | Coverage |
| --- | --- | --- | --- | --- |
| Sumas Power Plant | WA | 711080-99999 | 10.400 | 0.976406 |
| Nooksack Hydro | WA | 711080-99999 | 10.400 | 0.976406 |
| Glacier Battery Storage | WA | 711080-99999 | 10.400 | 0.976406 |

## Interpretation

- This is a preview export of rows that passed fixed-period readiness and station-selection review.
- It is narrower than the publication-candidate export because it uses `publish.plant_ecwt_release_readiness`.
- The CSV intentionally excludes blocked readiness rows and station-review-blocked rows.
- For a national release, remaining blocked rows require additional weather coverage or explicit station-selection policy decisions.

