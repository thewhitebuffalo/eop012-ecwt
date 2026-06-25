# Plant ECWT Readiness Report

Generated UTC: 2026-06-25T04:36:12+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `plant_ecwt_readiness_fixed_period_20260625T043609Z`
- Plant ECWT run ID: `plant_ecwt_provisional_fixed_period_20260625T043543Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `7b889f18ad75a2aed0069af2fa8278b5f0322464`
- Minimum valid hours: `2000`
- Minimum coverage ratio: `0.95`
- Coverage denominator mode: `plant-ecwt-row`
- Coverage year range: `2000-2025`

## Summary

| Relation or Check | Rows / Value |
| --- | ---: |
| `readiness rows` | 16132 |
| `publication candidates` | 162 |
| `provisional low coverage` | 0 |
| `blocked` | 15970 |
| `minimum coverage ratio` | 0.9501 |
| `median coverage ratio` | 0.9596 |

## By Reason

| Readiness | Reason | Rows |
| --- | --- | ---: |
| `blocked` | `no_candidate_station_with_provisional_ecwt` | 15970 |
| `publication_candidate` | `passes_current_publication_gate` | 162 |

## Interpretation

- This is a working publication-readiness gate for provisional plant ECWT rows.
- Coverage ratios use the denominator mode recorded above, not only currently loaded station-year files.
- For fixed-period plant selection runs, use `plant-ecwt-row` so readiness preserves the fixed-period valid/expected hours stored on `calc.plant_ecwt`.
- `publication_candidate` is not the same as final accepted compliance output; it means the row passes the current coverage thresholds.
- Rows that fail this gate should stay out of a published compliance dataset until more weather coverage or manual review is available.
