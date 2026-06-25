# Readiness Policy Scenario DB Load Report

Generated UTC: 2026-06-25T13:40:03+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `readiness_policy_scenarios_db_load_20260625T133957Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `ec55b1db935c268fb75ef6b5098a3fa115ed1ee2`
- Matrix CSV: `readiness_policy_scenarios_first_operable_20260625T133945Z_matrix.csv`
- Matrix SHA-256: `cc5ccfec0edd1c91cb220c0868e179b5e3529791befadd94ed77aa3c46857fc5`
- Candidate CSV: `readiness_policy_scenarios_first_operable_20260625T133945Z_candidates.csv`
- Candidate SHA-256: `6d8ed64e397c66c96150196307c06a07654a53be41cc4cd75df5ad01e45c3239`

## Loaded DB Counts

| Relation or check | Rows |
| --- | ---: |
| `calc.readiness_policy_scenario` | 5 |
| `calc.readiness_policy_scenario_candidate` | 43077 |
| `audit.source_file rows` | 2 |

## Scenario Matrix

| Scenario | Candidates | Promoted | Blocked | Overfill |
| --- | ---: | ---: | ---: | ---: |
| `fixed_period_current_gate` | 1405 | 0 | 11965 | 0 |
| `normalized_active_window_loaded_year` | 13355 | 11950 | 15 | 0 |
| `normalized_active_window_loaded_year_plus_20_loaded_years` | 5266 | 3861 | 8104 | 0 |
| `raw_active_window_metadata` | 13370 | 11965 | 0 | 8493 |
| `raw_active_window_metadata_plus_20_loaded_years` | 9681 | 8276 | 3689 | 5554 |

## Candidate Rows By Scenario

| Scenario | Rows |
| --- | ---: |
| `fixed_period_current_gate` | 1405 |
| `normalized_active_window_loaded_year` | 13355 |
| `normalized_active_window_loaded_year_plus_20_loaded_years` | 5266 |
| `raw_active_window_metadata` | 13370 |
| `raw_active_window_metadata_plus_20_loaded_years` | 9681 |

## Interpretation

- The scenario artifacts are now queryable in `calc.readiness_policy_scenario` and `calc.readiness_policy_scenario_candidate`.
- This load does not replace `calc.plant_ecwt_readiness`; the conservative fixed-period readiness run remains intact.
- Source CSV hashes are recorded in `audit.source_file` and in the calculation-run parameters.
