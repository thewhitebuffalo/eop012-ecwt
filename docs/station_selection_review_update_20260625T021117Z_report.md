# Station Selection Review Update Report

Generated UTC: 2026-06-25T02:11:19+00:00

## Summary

- Update run ID: `station_selection_review_update_20260625T021117Z`
- Source review run ID: `station_selection_review_update_20260625T020542Z`
- Code commit: `05905b52bbc68d40247e103048db2937b21f9818`
- Input CSV: `/Users/Shared/EOP012/rebuild/docs/station_selection_policy_review_us_ca_distance_cap_150_20260625T021058Z.csv`
- Output review snapshot CSV: `station_selection_review_update_20260625T021117Z.csv`
- Dry run: `False`

## Review Status Counts

| Review Status | Rows |
| --- | ---: |
| `accepted` | 162 |

## Review Basis Counts

| Review Basis | Rows |
| --- | ---: |
| `policy_override` | 162 |

## Disposition Reasons

| Reason | Rows |
| --- | ---: |
| `policy_accept_us_ca_practical` | 108 |
| `policy_accept_us_ca_distance_cap_150` | 54 |

## Release Readiness Counts

| Release Status | Rows |
| --- | ---: |
| `blocked_readiness` | 15,970 |
| `release_ready` | 162 |

## Interpretation

- This tool creates a complete review snapshot. Blank proposed fields preserve the source review disposition.
- Accepted rows become release-ready only after the DB write rebuilds `publish.plant_ecwt_release_readiness`.
- Rejected rows remain blocked with their disposition reason.
- Dry-run mode validates and summarizes the worksheet without writing to Postgres.
