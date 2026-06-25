# Station Selection Review Update Report

Generated UTC: 2026-06-25T01:44:12+00:00

## Summary

- Update run ID: `station_selection_review_update_20260625T014412Z`
- Source review run ID: `station_selection_review_seed_20260625T013744Z`
- Code commit: `eb8423b45b4df214884f724cd09ab9141d41e039`
- Input CSV: `/Users/Shared/EOP012/rebuild/docs/station_selection_review_update_template_20260625T0140Z.csv`
- Output review snapshot CSV: `station_selection_review_update_20260625T014412Z.csv`
- Dry run: `True`

## Review Status Counts

| Review Status | Rows |
| --- | ---: |
| `needs_review` | 162 |

## Review Basis Counts

| Review Basis | Rows |
| --- | ---: |
| `automated_policy_seed` | 162 |

## Disposition Reasons

| Reason | Rows |
| --- | ---: |
| `needs_policy_cross_border_station` | 110 |
| `needs_review_near_threshold_coverage` | 24 |
| `needs_review_high_distance` | 20 |
| `needs_review_high_candidate_rank` | 8 |

## Interpretation

- This tool creates a complete review snapshot. Blank proposed fields preserve the source review disposition.
- Accepted rows become release-ready only after the DB write rebuilds `publish.plant_ecwt_release_readiness`.
- Rejected rows remain blocked with their disposition reason.
- Dry-run mode validates and summarizes the worksheet without writing to Postgres.
