# Readiness Policy Scenario DB Load Report

Generated UTC: 2026-06-25T13:30:32+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `readiness_policy_scenarios_db_load_20260625T133025Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `eecb8b3f03847a6b12256e488c0105e5e84a1351`
- Matrix CSV: `readiness_policy_scenarios_first_operable_20260625T133017Z_matrix.csv`
- Matrix SHA-256: `f0a4167881a1310f316da8c7bb7ec0db764d2fd066c52988d58f9ae75de59f3b`
- Candidate CSV: `readiness_policy_scenarios_first_operable_20260625T133017Z_candidates.csv`
- Candidate SHA-256: `85c8373d3028ccf8811ac3b56d216f1891feab2ddde888b635bb7989c6b4b606`

## Loaded DB Counts

| Relation or check | Rows |
| --- | ---: |
| `calc.readiness_policy_scenario` | 5 |
| `calc.readiness_policy_scenario_candidate` | 44257 |
| `audit.source_file rows` | 2 |

## Scenario Matrix

| Scenario | Candidates | Promoted | Blocked | Overfill |
| --- | ---: | ---: | ---: | ---: |
| `fixed_period_current_gate` | 1641 | 0 | 11965 | 0 |
| `normalized_active_window_loaded_year` | 13591 | 11950 | 15 | 0 |
| `normalized_active_window_loaded_year_plus_20_loaded_years` | 5502 | 3861 | 8104 | 0 |
| `raw_active_window_metadata` | 13606 | 11965 | 0 | 8493 |
| `raw_active_window_metadata_plus_20_loaded_years` | 9917 | 8276 | 3689 | 5554 |

## Candidate Rows By Scenario

| Scenario | Rows |
| --- | ---: |
| `fixed_period_current_gate` | 1641 |
| `normalized_active_window_loaded_year` | 13591 |
| `normalized_active_window_loaded_year_plus_20_loaded_years` | 5502 |
| `raw_active_window_metadata` | 13606 |
| `raw_active_window_metadata_plus_20_loaded_years` | 9917 |

## Interpretation

- The scenario artifacts are now queryable in `calc.readiness_policy_scenario` and `calc.readiness_policy_scenario_candidate`.
- This load does not replace `calc.plant_ecwt_readiness`; the conservative fixed-period readiness run remains intact.
- Source CSV hashes are recorded in `audit.source_file` and in the calculation-run parameters.
