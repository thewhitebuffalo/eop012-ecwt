# ECWT Readiness Policy Scenario Comparison

Generated UTC: 2026-06-25T16:12:35+00:00

## Run

- Scenario run ID: `readiness_policy_scenarios_all_plants_20260625T161235Z`
- Code commit: `bd3c33c8073c2a66057773e07ae474d2b8eb9be4`
- Plant scope: `all-plants`
- Strict fixed-period candidates CSV: `plant_ecwt_publication_candidates_20260625T161224Z.csv`
- Denominator diagnostic CSV: `fixed_period_denominator_diagnostic_all-plants_20260625T161153Z.csv`
- Scenario matrix CSV: `readiness_policy_scenarios_all_plants_20260625T161235Z_matrix.csv`
- Scenario candidate detail CSV: `readiness_policy_scenarios_all_plants_20260625T161235Z_candidates.csv`

## Scenario Matrix

| Scenario | Candidates | Promoted Blockers | Remaining Blocked | Overfill Rows | Suitability |
| --- | --- | --- | --- | --- | --- |
| fixed_period_current_gate | 1,868 | 0 | 14,264 | 0 | current_conservative_gate |
| raw_active_window_metadata | 16,104 | 14,236 | 28 | 10,352 | diagnostic_only_overfill_present |
| raw_active_window_metadata_plus_20_loaded_years | 11,570 | 9,702 | 4,562 | 6,743 | diagnostic_only_overfill_present |
| normalized_active_window_loaded_year | 16,090 | 14,222 | 42 | 0 | candidate_policy_option |
| normalized_active_window_loaded_year_plus_20_loaded_years | 6,344 | 4,476 | 9,788 | 0 | candidate_policy_option_stricter |

## Interpretation

- The current fixed-period gate has 1,868 all-plants publication candidates.
- The raw station metadata active-window scenario would produce 16,104 candidates, but it promotes 10,352 rows with overfilled active-window denominators, so it remains diagnostic only.
- The normalized active-window loaded-year scenario would produce 16,090 candidates and has 0 promoted overfill rows in this diagnostic.
- Scenario candidates are not final compliance outputs; they are auditable policy alternatives for deciding the next publication gate.
- The current fixed-period readiness table in Postgres is not overwritten by this script.

## Candidate Detail Rows

| Scenario | Rows |
| --- | ---: |
| `fixed_period_current_gate` | 1,868 |
| `raw_active_window_metadata` | 16,104 |
| `raw_active_window_metadata_plus_20_loaded_years` | 11,570 |
| `normalized_active_window_loaded_year` | 16,090 |
| `normalized_active_window_loaded_year_plus_20_loaded_years` | 6,344 |
