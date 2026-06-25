# ECWT Readiness Policy Scenario Comparison

Generated UTC: 2026-06-25T05:37:24+00:00

## Run

- Scenario run ID: `readiness_policy_scenarios_first_operable_20260625T053723Z`
- Code commit: `41649537ccdeef469c3594e4c52eb0339ae0241a`
- Strict fixed-period candidates CSV: `plant_ecwt_publication_candidates_first_operable_20260625T045722Z.csv`
- Denominator diagnostic CSV: `fixed_period_denominator_diagnostic_first-operable_20260625T053208Z.csv`
- Scenario matrix CSV: `readiness_policy_scenarios_first_operable_20260625T053723Z_matrix.csv`
- Scenario candidate detail CSV: `readiness_policy_scenarios_first_operable_20260625T053723Z_candidates.csv`

## Scenario Matrix

| Scenario | Candidates | Promoted Blockers | Remaining Blocked | Overfill Rows | Suitability |
| --- | --- | --- | --- | --- | --- |
| fixed_period_current_gate | 144 | 0 | 13,226 | 0 | current_conservative_gate |
| raw_active_window_metadata | 11,112 | 10,968 | 2,258 | 2,794 | diagnostic_only_overfill_present |
| raw_active_window_metadata_plus_20_loaded_years | 2,070 | 1,926 | 11,300 | 314 | diagnostic_only_overfill_present |
| normalized_active_window_loaded_year | 6,136 | 5,992 | 7,234 | 0 | candidate_policy_option |
| normalized_active_window_loaded_year_plus_20_loaded_years | 577 | 433 | 12,793 | 0 | candidate_policy_option_stricter |

## Interpretation

- The current fixed-period gate has 144 first-operable publication candidates.
- The raw station metadata active-window scenario would produce 11,112 candidates, but it promotes 2,794 rows with overfilled active-window denominators, so it remains diagnostic only.
- The normalized active-window loaded-year scenario would produce 6,136 candidates and has 0 promoted overfill rows in this diagnostic.
- Scenario candidates are not final compliance outputs; they are auditable policy alternatives for deciding the next publication gate.
- The current fixed-period readiness table in Postgres is not overwritten by this script.

## Candidate Detail Rows

| Scenario | Rows |
| --- | ---: |
| `fixed_period_current_gate` | 144 |
| `raw_active_window_metadata` | 11,112 |
| `raw_active_window_metadata_plus_20_loaded_years` | 2,070 |
| `normalized_active_window_loaded_year` | 6,136 |
| `normalized_active_window_loaded_year_plus_20_loaded_years` | 577 |
