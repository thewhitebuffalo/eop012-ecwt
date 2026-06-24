# Plant ECWT Readiness Report

Generated UTC: 2026-06-24T01:55:12+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `plant_ecwt_readiness_20260624T015510Z`
- Plant ECWT run ID: `plant_ecwt_provisional_20260624T015403Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `5ed115bce9078238739a56a5ced32e36af85befd`
- Minimum valid hours: `2000`
- Minimum coverage ratio: `0.25`

## Summary

| Relation or Check | Rows / Value |
| --- | ---: |
| `readiness rows` | 16132 |
| `publication candidates` | 13679 |
| `provisional low coverage` | 2425 |
| `blocked` | 28 |
| `minimum coverage ratio` | 0.0487 |
| `median coverage ratio` | 0.8324 |

## By Reason

| Readiness | Reason | Rows |
| --- | --- | ---: |
| `blocked` | `no_candidate_station_with_provisional_ecwt` | 28 |
| `provisional_low_coverage` | `coverage_ratio_below_threshold` | 1092 |
| `provisional_low_coverage` | `valid_hours_below_threshold` | 1333 |
| `publication_candidate` | `passes_current_publication_gate` | 13679 |

## Interpretation

- This is a working publication-readiness gate for provisional plant ECWT rows.
- `publication_candidate` is not the same as final accepted compliance output; it means the row passes the current coverage thresholds.
- Rows that fail this gate should stay out of a published compliance dataset until more weather coverage or manual review is available.
