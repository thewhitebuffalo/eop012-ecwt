# ECWT Readiness Policy Scenario Comparison

Generated UTC: 2026-06-25T13:39:45+00:00

## Run

- Scenario run ID: `readiness_policy_scenarios_first_operable_20260625T133945Z`
- Code commit: `ec55b1db935c268fb75ef6b5098a3fa115ed1ee2`
- Plant scope: `first-operable`
- Strict fixed-period candidates CSV: `plant_ecwt_publication_candidates_first_operable_20260625T133846Z.csv`
- Denominator diagnostic CSV: `fixed_period_denominator_diagnostic_first-operable_20260625T133008Z.csv`
- Scenario matrix CSV: `readiness_policy_scenarios_first_operable_20260625T133945Z_matrix.csv`
- Scenario candidate detail CSV: `readiness_policy_scenarios_first_operable_20260625T133945Z_candidates.csv`

## Scenario Matrix

| Scenario | Candidates | Promoted Blockers | Remaining Blocked | Overfill Rows | Suitability |
| --- | --- | --- | --- | --- | --- |
| fixed_period_current_gate | 1,405 | 0 | 11,965 | 0 | current_conservative_gate |
| raw_active_window_metadata | 13,370 | 11,965 | 0 | 8,493 | diagnostic_only_overfill_present |
| raw_active_window_metadata_plus_20_loaded_years | 9,681 | 8,276 | 3,689 | 5,554 | diagnostic_only_overfill_present |
| normalized_active_window_loaded_year | 13,355 | 11,950 | 15 | 0 | candidate_policy_option |
| normalized_active_window_loaded_year_plus_20_loaded_years | 5,266 | 3,861 | 8,104 | 0 | candidate_policy_option_stricter |

## Interpretation

- The current fixed-period gate has 1,405 first-operable publication candidates.
- The raw station metadata active-window scenario would produce 13,370 candidates, but it promotes 8,493 rows with overfilled active-window denominators, so it remains diagnostic only.
- The normalized active-window loaded-year scenario would produce 13,355 candidates and has 0 promoted overfill rows in this diagnostic.
- Scenario candidates are not final compliance outputs; they are auditable policy alternatives for deciding the next publication gate.
- The current fixed-period readiness table in Postgres is not overwritten by this script.

## Candidate Detail Rows

| Scenario | Rows |
| --- | ---: |
| `fixed_period_current_gate` | 1,405 |
| `raw_active_window_metadata` | 13,370 |
| `raw_active_window_metadata_plus_20_loaded_years` | 9,681 |
| `normalized_active_window_loaded_year` | 13,355 |
| `normalized_active_window_loaded_year_plus_20_loaded_years` | 5,266 |
