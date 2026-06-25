# ECWT Readiness Policy Scenario Comparison

Generated UTC: 2026-06-25T13:40:50+00:00

## Run

- Scenario run ID: `readiness_policy_scenarios_all_plants_20260625T134050Z`
- Code commit: `ec55b1db935c268fb75ef6b5098a3fa115ed1ee2`
- Plant scope: `all-plants`
- Strict fixed-period candidates CSV: `plant_ecwt_publication_candidates_20260625T125617Z.csv`
- Denominator diagnostic CSV: `fixed_period_denominator_diagnostic_all-plants_20260625T134039Z.csv`
- Scenario matrix CSV: `readiness_policy_scenarios_all_plants_20260625T134050Z_matrix.csv`
- Scenario candidate detail CSV: `readiness_policy_scenarios_all_plants_20260625T134050Z_candidates.csv`

## Scenario Matrix

| Scenario | Candidates | Promoted Blockers | Remaining Blocked | Overfill Rows | Suitability |
| --- | --- | --- | --- | --- | --- |
| fixed_period_current_gate | 1,641 | 0 | 14,491 | 0 | current_conservative_gate |
| raw_active_window_metadata | 16,104 | 14,463 | 28 | 10,364 | diagnostic_only_overfill_present |
| raw_active_window_metadata_plus_20_loaded_years | 11,556 | 9,915 | 4,576 | 6,746 | diagnostic_only_overfill_present |
| normalized_active_window_loaded_year | 16,089 | 14,448 | 43 | 0 | candidate_policy_option |
| normalized_active_window_loaded_year_plus_20_loaded_years | 6,126 | 4,485 | 10,006 | 0 | candidate_policy_option_stricter |

## Interpretation

- The current fixed-period gate has 1,641 all-plants publication candidates.
- The raw station metadata active-window scenario would produce 16,104 candidates, but it promotes 10,364 rows with overfilled active-window denominators, so it remains diagnostic only.
- The normalized active-window loaded-year scenario would produce 16,089 candidates and has 0 promoted overfill rows in this diagnostic.
- Scenario candidates are not final compliance outputs; they are auditable policy alternatives for deciding the next publication gate.
- The current fixed-period readiness table in Postgres is not overwritten by this script.

## Candidate Detail Rows

| Scenario | Rows |
| --- | ---: |
| `fixed_period_current_gate` | 1,641 |
| `raw_active_window_metadata` | 16,104 |
| `raw_active_window_metadata_plus_20_loaded_years` | 11,556 |
| `normalized_active_window_loaded_year` | 16,089 |
| `normalized_active_window_loaded_year_plus_20_loaded_years` | 6,126 |
