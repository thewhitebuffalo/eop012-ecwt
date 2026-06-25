# Expanded Candidate ECWT Refresh Status

Generated UTC: 2026-06-25T07:10Z

## Scope

This refresh used the expanded NOAA station-candidate run `noaa_station_candidates_20260625T065445Z` with top 100 distance-ranked stations per plant. It did not use the legacy `ecwt_raw_station` coverage bridge; all ECWT and coverage gates came from the current canonical EOP012 Postgres tables.

## Inputs

| Input | Run ID |
| --- | --- |
| Station candidates | `noaa_station_candidates_20260625T065445Z` |
| Station-year DJF coverage | `station_year_djf_coverage_20260625T035921Z` |
| Station ECWT | `station_ecwt_loaded_20260625T042423Z` |

## Results

| Layer | Run ID | Key Counts |
| --- | --- | --- |
| Active-window plant ECWT | `plant_ecwt_provisional_20260625T070228Z` | 16,104 provisional, 28 blocked |
| Fixed-period plant ECWT | `plant_ecwt_provisional_fixed_period_20260625T070144Z` | 1,346 provisional, 14,786 blocked |
| Fixed-period readiness | `plant_ecwt_readiness_fixed_period_20260625T070613Z` | 1,346 publication candidates, 14,786 blocked |

## Interpretation

- The top-100 candidate expansion materially improved the strict fixed-period gate: publication candidates increased from 162 in the prior fixed-period run to 1,346.
- The active-window result still covers every plant with coordinates: 16,104 provisional rows and 28 blocked rows. The 28 active-window blocked rows are plants with missing coordinates.
- Of the 14,786 fixed-period blocked rows, 14,758 have an active-window provisional ECWT. The remaining bottleneck is therefore fixed-period station coverage eligibility, not basic ECWT calculability.
- Fixed-period readiness blockers now use reason code `no_fixed_period_eligible_candidate_station`, which more accurately describes the strict gate than the older generic active-window blocker label.

## Reports Produced

- `docs/plant_ecwt_provisional_20260625T070228Z_report.md`
- `docs/plant_ecwt_provisional_fixed_period_20260625T070144Z_report.md`
- `docs/plant_ecwt_readiness_fixed_period_20260625T070613Z_report.md`

## Next Operational Step

Build a new NOAA backfill manifest from the expanded top-100 candidate run and the current raw-file inventory, excluding station-years already proven `missing_on_aws`. Then download and load the next manageable manifest batch, rebuild station-year coverage, station ECWT, fixed-period plant ECWT, and fixed-period readiness.
