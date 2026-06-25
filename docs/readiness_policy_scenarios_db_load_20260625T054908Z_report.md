# Readiness Policy Scenario DB Load Report

Generated UTC: 2026-06-25T05:49:12+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `readiness_policy_scenarios_db_load_20260625T054908Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `258f4f1394cdfc5b301dbb4e20dcccc5aa3971d7`
- Matrix CSV: `readiness_policy_scenarios_first_operable_20260625T053723Z_matrix.csv`
- Matrix SHA-256: `14447c7f9701931d6b475c65cc5618737e7b5fdaa3772be2d545cb5a2c025787`
- Candidate CSV: `readiness_policy_scenarios_first_operable_20260625T053723Z_candidates.csv`
- Candidate SHA-256: `34ce5cc3217c014684eda930fb392a4394d2fc440e51d8f62b7d490d02b8780d`

## Loaded DB Counts

| Relation or check | Rows |
| --- | ---: |
| `calc.readiness_policy_scenario` | 5 |
| `calc.readiness_policy_scenario_candidate` | 20039 |
| `audit.source_file rows` | 2 |

## Scenario Matrix

| Scenario | Candidates | Promoted | Blocked | Overfill |
| --- | ---: | ---: | ---: | ---: |
| `fixed_period_current_gate` | 144 | 0 | 13226 | 0 |
| `normalized_active_window_loaded_year` | 6136 | 5992 | 7234 | 0 |
| `normalized_active_window_loaded_year_plus_20_loaded_years` | 577 | 433 | 12793 | 0 |
| `raw_active_window_metadata` | 11112 | 10968 | 2258 | 2794 |
| `raw_active_window_metadata_plus_20_loaded_years` | 2070 | 1926 | 11300 | 314 |

## Candidate Rows By Scenario

| Scenario | Rows |
| --- | ---: |
| `fixed_period_current_gate` | 144 |
| `normalized_active_window_loaded_year` | 6136 |
| `normalized_active_window_loaded_year_plus_20_loaded_years` | 577 |
| `raw_active_window_metadata` | 11112 |
| `raw_active_window_metadata_plus_20_loaded_years` | 2070 |

## Interpretation

- The scenario artifacts are now queryable in `calc.readiness_policy_scenario` and `calc.readiness_policy_scenario_candidate`.
- This load does not replace `calc.plant_ecwt_readiness`; the conservative fixed-period readiness run remains intact.
- Source CSV hashes are recorded in `audit.source_file` and in the calculation-run parameters.
