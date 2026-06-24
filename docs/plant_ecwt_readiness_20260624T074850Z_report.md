# Plant ECWT Readiness Report

Generated UTC: 2026-06-24T07:48:51+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `plant_ecwt_readiness_20260624T074850Z`
- Plant ECWT run ID: `plant_ecwt_provisional_20260624T074807Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `164eec34fe3b7cc2b663811dd7e3de43d9e94ddd`
- Minimum valid hours: `2000`
- Minimum coverage ratio: `0.25`
- Coverage denominator: `fixed selected-station active-period DJF hours`
- Coverage year range: `2000-2025`

## Summary

| Relation or Check | Rows / Value |
| --- | ---: |
| `readiness rows` | 16132 |
| `publication candidates` | 2823 |
| `provisional low coverage` | 13281 |
| `blocked` | 28 |
| `minimum coverage ratio` | 0.0000 |
| `median coverage ratio` | 0.0910 |

## By Reason

| Readiness | Reason | Rows |
| --- | --- | ---: |
| `blocked` | `no_candidate_station_with_provisional_ecwt` | 28 |
| `provisional_low_coverage` | `coverage_ratio_below_threshold` | 10596 |
| `provisional_low_coverage` | `valid_hours_below_threshold` | 2685 |
| `publication_candidate` | `passes_current_publication_gate` | 2823 |

## Interpretation

- This is a working publication-readiness gate for provisional plant ECWT rows.
- Coverage ratios use a fixed selected-station active-period DJF denominator, not only currently loaded station-year files.
- `publication_candidate` is not the same as final accepted compliance output; it means the row passes the current coverage thresholds.
- Rows that fail this gate should stay out of a published compliance dataset until more weather coverage or manual review is available.
