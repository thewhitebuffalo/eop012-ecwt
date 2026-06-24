# Plant ECWT Readiness Report

Generated UTC: 2026-06-24T03:31:34+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `plant_ecwt_readiness_20260624T033133Z`
- Plant ECWT run ID: `plant_ecwt_provisional_20260624T033019Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `b68bd1d44aafc4d25f023da2cee212ba7c8bec71`
- Minimum valid hours: `2000`
- Minimum coverage ratio: `0.25`

## Summary

| Relation or Check | Rows / Value |
| --- | ---: |
| `readiness rows` | 16132 |
| `publication candidates` | 13589 |
| `provisional low coverage` | 2515 |
| `blocked` | 28 |
| `minimum coverage ratio` | 0.0447 |
| `median coverage ratio` | 0.8305 |

## By Reason

| Readiness | Reason | Rows |
| --- | --- | ---: |
| `blocked` | `no_candidate_station_with_provisional_ecwt` | 28 |
| `provisional_low_coverage` | `coverage_ratio_below_threshold` | 1975 |
| `provisional_low_coverage` | `valid_hours_below_threshold` | 540 |
| `publication_candidate` | `passes_current_publication_gate` | 13589 |

## Interpretation

- This is a working publication-readiness gate for provisional plant ECWT rows.
- `publication_candidate` is not the same as final accepted compliance output; it means the row passes the current coverage thresholds.
- Rows that fail this gate should stay out of a published compliance dataset until more weather coverage or manual review is available.
