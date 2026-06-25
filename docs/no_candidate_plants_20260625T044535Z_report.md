# No-Candidate Plant Diagnostic

Generated UTC: 2026-06-25T04:45:35Z

## Scope

- Readiness run ID: `plant_ecwt_readiness_fixed_period_20260625T043609Z`
- Station candidate run ID: `noaa_station_candidates_20260623T210132Z`
- Detail CSV: `no_candidate_plants_20260625T044535Z.csv`

## Result

The current fixed-period readiness run has 28 blocked plants with no station candidates.

| Metric | Count |
| --- | ---: |
| No-candidate plants | 28 |
| No-candidate plants missing latitude or longitude | 28 |
| Attached generator rows | 69 |
| Attached generator nameplate MW | 17,925.6 |
| No-candidate plants with only `CN` generator status | 28 |

## Interpretation

These rows are not NOAA download failures. The station-candidate loader requires plant
latitude and longitude, and all 28 no-candidate plants have missing coordinates.

Every generator row attached to these plants has EIA status `CN`. The ECWT publication
universe should therefore make an explicit policy decision before trying to repair these
records:

1. If `CN` rows are outside the compliance/publication universe, exclude them from the
   release-facing plant universe and keep the exclusion auditable.
2. If any `CN` rows must remain in scope, obtain or derive plant coordinates before
   station-candidate generation.
3. Do not spend NOAA AWS backfill effort on these plants; weather data cannot create
   station candidates without plant coordinates.
