# Plant ECWT Readiness Report

Generated UTC: 2026-06-23T23:30:47+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `plant_ecwt_readiness_20260623T233046Z`
- Plant ECWT run ID: `plant_ecwt_provisional_20260623T232311Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `c22cc01f4cb305ebb316c53a74ae66fb88dd50da`
- Minimum valid hours: `2000`
- Minimum coverage ratio: `0.25`

## Summary

| Relation or Check | Rows / Value |
| --- | ---: |
| `readiness rows` | 16132 |
| `publication candidates` | 3891 |
| `provisional low coverage` | 12213 |
| `blocked` | 28 |
| `minimum coverage ratio` | 0.0347 |
| `median coverage ratio` | 0.4160 |

## By Reason

| Readiness | Reason | Rows |
| --- | --- | ---: |
| `blocked` | `no_candidate_station_with_provisional_ecwt` | 28 |
| `provisional_low_coverage` | `valid_hours_below_threshold` | 12213 |
| `publication_candidate` | `passes_current_publication_gate` | 3891 |

## Interpretation

- This is a working publication-readiness gate for provisional plant ECWT rows.
- `publication_candidate` is not the same as final accepted compliance output; it means the row passes the current coverage thresholds.
- Rows that fail this gate should stay out of a published compliance dataset until more weather coverage or manual review is available.
