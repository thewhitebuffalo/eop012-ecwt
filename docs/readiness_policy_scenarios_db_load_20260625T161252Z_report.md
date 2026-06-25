# Readiness Policy Scenario DB Load Report

Generated UTC: 2026-06-25T16:13:01+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `readiness_policy_scenarios_db_load_20260625T161252Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `bd3c33c8073c2a66057773e07ae474d2b8eb9be4`
- Matrix CSV: `readiness_policy_scenarios_all_plants_20260625T161235Z_matrix.csv`
- Matrix SHA-256: `c881e34d624a634dfa2d63b6f87f923876f3ba7f4769e50748b83091dbd0a775`
- Candidate CSV: `readiness_policy_scenarios_all_plants_20260625T161235Z_candidates.csv`
- Candidate SHA-256: `2f2e9c2fbd48bdfbd3b6d7cffbdf2e0d4fb583ed5d4b0a6bdabbb62d40eb1e9b`

## Loaded DB Counts

| Relation or check | Rows |
| --- | ---: |
| `calc.readiness_policy_scenario` | 5 |
| `calc.readiness_policy_scenario_candidate` | 51976 |
| `audit.source_file rows` | 2 |

## Scenario Matrix

| Scenario | Candidates | Promoted | Blocked | Overfill |
| --- | ---: | ---: | ---: | ---: |
| `fixed_period_current_gate` | 1868 | 0 | 14264 | 0 |
| `normalized_active_window_loaded_year` | 16090 | 14222 | 42 | 0 |
| `normalized_active_window_loaded_year_plus_20_loaded_years` | 6344 | 4476 | 9788 | 0 |
| `raw_active_window_metadata` | 16104 | 14236 | 28 | 10352 |
| `raw_active_window_metadata_plus_20_loaded_years` | 11570 | 9702 | 4562 | 6743 |

## Candidate Rows By Scenario

| Scenario | Rows |
| --- | ---: |
| `fixed_period_current_gate` | 1868 |
| `normalized_active_window_loaded_year` | 16090 |
| `normalized_active_window_loaded_year_plus_20_loaded_years` | 6344 |
| `raw_active_window_metadata` | 16104 |
| `raw_active_window_metadata_plus_20_loaded_years` | 11570 |

## Interpretation

- The scenario artifacts are now queryable in `calc.readiness_policy_scenario` and `calc.readiness_policy_scenario_candidate`.
- This load does not replace `calc.plant_ecwt_readiness`; the conservative fixed-period readiness run remains intact.
- Source CSV hashes are recorded in `audit.source_file` and in the calculation-run parameters.
