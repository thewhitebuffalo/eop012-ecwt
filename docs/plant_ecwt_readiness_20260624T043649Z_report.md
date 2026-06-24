# Plant ECWT Readiness Report

Generated UTC: 2026-06-24T04:36:50+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `plant_ecwt_readiness_20260624T043649Z`
- Plant ECWT run ID: `plant_ecwt_provisional_20260624T043636Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `23e67f27d52beebddc77612cf270c48939242097`
- Minimum valid hours: `2000`
- Minimum coverage ratio: `0.95`

## Summary

| Relation or Check | Rows / Value |
| --- | ---: |
| `readiness rows` | 16132 |
| `publication candidates` | 357 |
| `provisional low coverage` | 15747 |
| `blocked` | 28 |
| `minimum coverage ratio` | 0.0005 |
| `median coverage ratio` | 0.0880 |

## By Reason

| Readiness | Reason | Rows |
| --- | --- | ---: |
| `blocked` | `no_candidate_station_with_provisional_ecwt` | 28 |
| `provisional_low_coverage` | `coverage_ratio_below_threshold` | 8327 |
| `provisional_low_coverage` | `valid_hours_below_threshold` | 7420 |
| `publication_candidate` | `passes_current_publication_gate` | 357 |

## Interpretation

- This is a working publication-readiness gate for provisional plant ECWT rows.
- `publication_candidate` is not the same as final accepted compliance output; it means the row passes the current coverage thresholds.
- Rows that fail this gate should stay out of a published compliance dataset until more weather coverage or manual review is available.
