# Readiness Policy Scenario DB Load Report

Generated UTC: 2026-06-25T13:41:20+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `readiness_policy_scenarios_db_load_20260625T134112Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `ec55b1db935c268fb75ef6b5098a3fa115ed1ee2`
- Matrix CSV: `readiness_policy_scenarios_all_plants_20260625T134050Z_matrix.csv`
- Matrix SHA-256: `e14f00adbf13348ebf551a7fa6834ae7b19242d8887125595f45714ca0db1b9e`
- Candidate CSV: `readiness_policy_scenarios_all_plants_20260625T134050Z_candidates.csv`
- Candidate SHA-256: `0ba14c162e2cfd0256885126008bf11f766f08f71af6786c73ddabc97591cb47`

## Loaded DB Counts

| Relation or check | Rows |
| --- | ---: |
| `calc.readiness_policy_scenario` | 5 |
| `calc.readiness_policy_scenario_candidate` | 51516 |
| `audit.source_file rows` | 2 |

## Scenario Matrix

| Scenario | Candidates | Promoted | Blocked | Overfill |
| --- | ---: | ---: | ---: | ---: |
| `fixed_period_current_gate` | 1641 | 0 | 14491 | 0 |
| `normalized_active_window_loaded_year` | 16089 | 14448 | 43 | 0 |
| `normalized_active_window_loaded_year_plus_20_loaded_years` | 6126 | 4485 | 10006 | 0 |
| `raw_active_window_metadata` | 16104 | 14463 | 28 | 10364 |
| `raw_active_window_metadata_plus_20_loaded_years` | 11556 | 9915 | 4576 | 6746 |

## Candidate Rows By Scenario

| Scenario | Rows |
| --- | ---: |
| `fixed_period_current_gate` | 1641 |
| `normalized_active_window_loaded_year` | 16089 |
| `normalized_active_window_loaded_year_plus_20_loaded_years` | 6126 |
| `raw_active_window_metadata` | 16104 |
| `raw_active_window_metadata_plus_20_loaded_years` | 11556 |

## Interpretation

- The scenario artifacts are now queryable in `calc.readiness_policy_scenario` and `calc.readiness_policy_scenario_candidate`.
- This load does not replace `calc.plant_ecwt_readiness`; the conservative fixed-period readiness run remains intact.
- Source CSV hashes are recorded in `audit.source_file` and in the calculation-run parameters.
