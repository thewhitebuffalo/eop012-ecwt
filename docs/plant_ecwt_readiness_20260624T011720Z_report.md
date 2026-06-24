# Plant ECWT Readiness Report

Generated UTC: 2026-06-24T01:17:21+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `plant_ecwt_readiness_20260624T011720Z`
- Plant ECWT run ID: `plant_ecwt_provisional_20260624T011618Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `2aa504b0a1dcc760d1462915d0cf12cb819b220d`
- Minimum valid hours: `2000`
- Minimum coverage ratio: `0.25`

## Summary

| Relation or Check | Rows / Value |
| --- | ---: |
| `readiness rows` | 16132 |
| `publication candidates` | 13393 |
| `provisional low coverage` | 2711 |
| `blocked` | 28 |
| `minimum coverage ratio` | 0.0518 |
| `median coverage ratio` | 0.8313 |

## By Reason

| Readiness | Reason | Rows |
| --- | --- | ---: |
| `blocked` | `no_candidate_station_with_provisional_ecwt` | 28 |
| `provisional_low_coverage` | `coverage_ratio_below_threshold` | 1192 |
| `provisional_low_coverage` | `valid_hours_below_threshold` | 1519 |
| `publication_candidate` | `passes_current_publication_gate` | 13393 |

## Interpretation

- This is a working publication-readiness gate for provisional plant ECWT rows.
- `publication_candidate` is not the same as final accepted compliance output; it means the row passes the current coverage thresholds.
- Rows that fail this gate should stay out of a published compliance dataset until more weather coverage or manual review is available.
