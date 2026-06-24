# Plant ECWT Readiness Report

Generated UTC: 2026-06-24T21:00:18+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `plant_ecwt_readiness_20260624T210010Z`
- Plant ECWT run ID: `plant_ecwt_provisional_20260624T205856Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `d7dfe307bd62b36e30127c7bd715dd45383fd810`
- Minimum valid hours: `2000`
- Minimum coverage ratio: `0.95`
- Coverage denominator: `fixed selected-station active-period DJF hours`
- Coverage year range: `2000-2025`

## Summary

| Relation or Check | Rows / Value |
| --- | ---: |
| `readiness rows` | 16132 |
| `publication candidates` | 1964 |
| `provisional low coverage` | 14140 |
| `blocked` | 28 |
| `minimum coverage ratio` | 0.0000 |
| `median coverage ratio` | 0.2517 |

## By Reason

| Readiness | Reason | Rows |
| --- | --- | ---: |
| `blocked` | `no_candidate_station_with_provisional_ecwt` | 28 |
| `provisional_low_coverage` | `coverage_ratio_below_threshold` | 12885 |
| `provisional_low_coverage` | `valid_hours_below_threshold` | 1255 |
| `publication_candidate` | `passes_current_publication_gate` | 1964 |

## Interpretation

- This is a working publication-readiness gate for provisional plant ECWT rows.
- Coverage ratios use a fixed selected-station active-period DJF denominator, not only currently loaded station-year files.
- `publication_candidate` is not the same as final accepted compliance output; it means the row passes the current coverage thresholds.
- Rows that fail this gate should stay out of a published compliance dataset until more weather coverage or manual review is available.
