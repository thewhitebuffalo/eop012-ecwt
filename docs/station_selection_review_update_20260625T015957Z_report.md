# Station Selection Review Update Report

Generated UTC: 2026-06-25T02:00:02+00:00

## Summary

- Update run ID: `station_selection_review_update_20260625T015957Z`
- Source review run ID: `station_selection_review_seed_20260625T013744Z`
- Code commit: `1a846a8f435119faf10e41d890d2c352fed650d8`
- Input CSV: `/Users/Shared/EOP012/rebuild/docs/station_selection_policy_review_us_ca_core_20260625T015940Z.csv`
- Output review snapshot CSV: `station_selection_review_update_20260625T015957Z.csv`
- Dry run: `False`

## Review Status Counts

| Review Status | Rows |
| --- | ---: |
| `needs_review` | 159 |
| `accepted` | 3 |

## Review Basis Counts

| Review Basis | Rows |
| --- | ---: |
| `automated_policy_seed` | 159 |
| `policy_override` | 3 |

## Disposition Reasons

| Reason | Rows |
| --- | ---: |
| `needs_policy_cross_border_station` | 107 |
| `needs_review_near_threshold_coverage` | 24 |
| `needs_review_high_distance` | 20 |
| `needs_review_high_candidate_rank` | 8 |
| `policy_accept_us_ca_core` | 3 |

## Release Readiness Counts

| Release Status | Rows |
| --- | ---: |
| `blocked_readiness` | 15,970 |
| `blocked_station_review` | 159 |
| `release_ready` | 3 |

## Interpretation

- This tool creates a complete review snapshot. Blank proposed fields preserve the source review disposition.
- Accepted rows become release-ready only after the DB write rebuilds `publish.plant_ecwt_release_readiness`.
- Rejected rows remain blocked with their disposition reason.
- Dry-run mode validates and summarizes the worksheet without writing to Postgres.
