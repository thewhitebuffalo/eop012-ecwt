# Station Selection Review Update Report

Generated UTC: 2026-06-25T02:05:43+00:00

## Summary

- Update run ID: `station_selection_review_update_20260625T020542Z`
- Source review run ID: `station_selection_review_update_20260625T015957Z`
- Code commit: `97cd500d68a0d32f6cec41248a7c1c9f7d9fc19a`
- Input CSV: `/Users/Shared/EOP012/rebuild/docs/station_selection_policy_review_us_ca_practical_20260625T020519Z.csv`
- Output review snapshot CSV: `station_selection_review_update_20260625T020542Z.csv`
- Dry run: `False`

## Review Status Counts

| Review Status | Rows |
| --- | ---: |
| `accepted` | 108 |
| `needs_review` | 54 |

## Review Basis Counts

| Review Basis | Rows |
| --- | ---: |
| `policy_override` | 108 |
| `automated_policy_seed` | 54 |

## Disposition Reasons

| Reason | Rows |
| --- | ---: |
| `policy_accept_us_ca_practical` | 108 |
| `needs_policy_cross_border_station` | 34 |
| `needs_review_high_distance` | 20 |

## Release Readiness Counts

| Release Status | Rows |
| --- | ---: |
| `blocked_readiness` | 15,970 |
| `blocked_station_review` | 54 |
| `release_ready` | 108 |

## Interpretation

- This tool creates a complete review snapshot. Blank proposed fields preserve the source review disposition.
- Accepted rows become release-ready only after the DB write rebuilds `publish.plant_ecwt_release_readiness`.
- Rejected rows remain blocked with their disposition reason.
- Dry-run mode validates and summarizes the worksheet without writing to Postgres.
