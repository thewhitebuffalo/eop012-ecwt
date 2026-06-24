# Plant ECWT Readiness Report

Generated UTC: 2026-06-24T00:32:03+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `plant_ecwt_readiness_20260624T003201Z`
- Plant ECWT run ID: `plant_ecwt_provisional_20260624T003116Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `043fc4c3996489b673409b968dae9df329a961d9`
- Minimum valid hours: `2000`
- Minimum coverage ratio: `0.95`

## Summary

| Relation or Check | Rows / Value |
| --- | ---: |
| `readiness rows` | 16132 |
| `publication candidates` | 169 |
| `provisional low coverage` | 15935 |
| `blocked` | 28 |
| `minimum coverage ratio` | 0.0377 |
| `median coverage ratio` | 0.8346 |

## By Reason

| Readiness | Reason | Rows |
| --- | --- | ---: |
| `blocked` | `no_candidate_station_with_provisional_ecwt` | 28 |
| `provisional_low_coverage` | `coverage_ratio_below_threshold` | 14153 |
| `provisional_low_coverage` | `valid_hours_below_threshold` | 1782 |
| `publication_candidate` | `passes_current_publication_gate` | 169 |

## Interpretation

- This is a working publication-readiness gate for provisional plant ECWT rows.
- `publication_candidate` is not the same as final accepted compliance output; it means the row passes the current coverage thresholds.
- Rows that fail this gate should stay out of a published compliance dataset until more weather coverage or manual review is available.
