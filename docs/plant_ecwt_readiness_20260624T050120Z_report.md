# Plant ECWT Readiness Report

Generated UTC: 2026-06-24T05:01:21+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `plant_ecwt_readiness_20260624T050120Z`
- Plant ECWT run ID: `plant_ecwt_provisional_20260624T045441Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `aa9c265cafadf49d1669913bab20952c2e30a882`
- Minimum valid hours: `2000`
- Minimum coverage ratio: `0.25`
- Coverage denominator: `fixed selected-station active-period DJF hours`
- Coverage year range: `2000-2025`

## Summary

| Relation or Check | Rows / Value |
| --- | ---: |
| `readiness rows` | 16132 |
| `publication candidates` | 2170 |
| `provisional low coverage` | 13934 |
| `blocked` | 28 |
| `minimum coverage ratio` | 0.0000 |
| `median coverage ratio` | 0.0496 |

## By Reason

| Readiness | Reason | Rows |
| --- | --- | ---: |
| `blocked` | `no_candidate_station_with_provisional_ecwt` | 28 |
| `provisional_low_coverage` | `coverage_ratio_below_threshold` | 6733 |
| `provisional_low_coverage` | `valid_hours_below_threshold` | 7201 |
| `publication_candidate` | `passes_current_publication_gate` | 2170 |

## Interpretation

- This is a working publication-readiness gate for provisional plant ECWT rows.
- Coverage ratios use a fixed selected-station active-period DJF denominator, not only currently loaded station-year files.
- `publication_candidate` is not the same as final accepted compliance output; it means the row passes the current coverage thresholds.
- Rows that fail this gate should stay out of a published compliance dataset until more weather coverage or manual review is available.
