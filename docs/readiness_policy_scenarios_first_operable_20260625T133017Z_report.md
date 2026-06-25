# ECWT Readiness Policy Scenario Comparison

Generated UTC: 2026-06-25T13:30:18+00:00

## Run

- Scenario run ID: `readiness_policy_scenarios_first_operable_20260625T133017Z`
- Code commit: `eecb8b3f03847a6b12256e488c0105e5e84a1351`
- Strict fixed-period candidates CSV: `plant_ecwt_publication_candidates_20260625T125617Z.csv`
- Denominator diagnostic CSV: `fixed_period_denominator_diagnostic_first-operable_20260625T133008Z.csv`
- Scenario matrix CSV: `readiness_policy_scenarios_first_operable_20260625T133017Z_matrix.csv`
- Scenario candidate detail CSV: `readiness_policy_scenarios_first_operable_20260625T133017Z_candidates.csv`

## Scenario Matrix

| Scenario | Candidates | Promoted Blockers | Remaining Blocked | Overfill Rows | Suitability |
| --- | --- | --- | --- | --- | --- |
| fixed_period_current_gate | 1,641 | 0 | 11,965 | 0 | current_conservative_gate |
| raw_active_window_metadata | 13,606 | 11,965 | 0 | 8,493 | diagnostic_only_overfill_present |
| raw_active_window_metadata_plus_20_loaded_years | 9,917 | 8,276 | 3,689 | 5,554 | diagnostic_only_overfill_present |
| normalized_active_window_loaded_year | 13,591 | 11,950 | 15 | 0 | candidate_policy_option |
| normalized_active_window_loaded_year_plus_20_loaded_years | 5,502 | 3,861 | 8,104 | 0 | candidate_policy_option_stricter |

## Interpretation

- The current fixed-period gate has 1,641 first-operable publication candidates.
- The raw station metadata active-window scenario would produce 13,606 candidates, but it promotes 8,493 rows with overfilled active-window denominators, so it remains diagnostic only.
- The normalized active-window loaded-year scenario would produce 13,591 candidates and has 0 promoted overfill rows in this diagnostic.
- Scenario candidates are not final compliance outputs; they are auditable policy alternatives for deciding the next publication gate.
- The current fixed-period readiness table in Postgres is not overwritten by this script.

## Candidate Detail Rows

| Scenario | Rows |
| --- | ---: |
| `fixed_period_current_gate` | 1,641 |
| `raw_active_window_metadata` | 13,606 |
| `raw_active_window_metadata_plus_20_loaded_years` | 9,917 |
| `normalized_active_window_loaded_year` | 13,591 |
| `normalized_active_window_loaded_year_plus_20_loaded_years` | 5,502 |
