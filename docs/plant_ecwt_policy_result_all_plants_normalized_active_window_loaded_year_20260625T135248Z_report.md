# Plant ECWT Policy Result Materialization

Generated UTC: 2026-06-25T13:52:52+00:00

## Run

- Policy result run ID: `plant_ecwt_policy_result_all_plants_normalized_active_window_loaded_year_20260625T135248Z`
- Code commit: `dde4f9831f304f229d32a1284c438ceb77b35b7d`
- Plant scope: `all-plants`
- Policy ID: `normalized_active_window_loaded_year`
- Scenario candidate CSV: `readiness_policy_scenarios_all_plants_20260625T134050Z_candidates.csv`
- Denominator diagnostic CSV: `fixed_period_denominator_diagnostic_all-plants_20260625T134039Z.csv`
- Result CSV: `plant_ecwt_policy_result_all_plants_normalized_active_window_loaded_year_20260625T135248Z.csv`

## Summary

| Metric | Count |
| --- | ---: |
| Plant rows materialized | 16,132 |
| Publication candidates | 16,089 |
| Blocked rows | 43 |

## Loaded DB Counts

| Check | Rows |
| --- | ---: |
| calc.plant_ecwt_policy_result | 16132 |
| publication candidates | 16089 |
| blocked rows | 43 |
| audit.source_file rows | 3 |

## Reason Counts

| Reason | Rows |
| --- | --- |
| passes_normalized_active_window_policy | 14,448 |
| passes_current_fixed_period_gate | 1,641 |
| no_station_candidates | 28 |
| normalized_active_window_coverage_below_threshold | 15 |

## Candidate Rows By State

| State | Rows |
| --- | --- |
| CA | 2,171 |
| TX | 1,363 |
| NY | 1,215 |
| NC | 985 |
| MN | 837 |
| MA | 700 |
| IL | 566 |
| NJ | 427 |
| FL | 400 |
| CO | 342 |
| MI | 332 |
| IA | 331 |
| PA | 324 |
| OR | 321 |
| VA | 317 |
| GA | 308 |
| WI | 291 |
| ME | 269 |
| IN | 268 |
| OH | 262 |

## Blocked Rows

| Plant | State | Reason | Best Station | Coverage | ECWT F |
| --- | --- | --- | --- | --- | --- |
| Kotzebue Hybrid | AK | normalized_active_window_coverage_below_threshold | 702460-99999 | 0.938422 | -50.800 |
| Kiana | AK | normalized_active_window_coverage_below_threshold | 702460-99999 | 0.938422 | -50.800 |
| Yakutat | AK | normalized_active_window_coverage_below_threshold | 703430-99999 | 0.945151 | 24.800 |
| Barrow | AK | normalized_active_window_coverage_below_threshold | 999999-26655 | 0.934586 | -33.700 |
| NSB Atqasuk Utility | AK | normalized_active_window_coverage_below_threshold | 702460-99999 | 0.938422 | -50.800 |
| NSB Point Hope Utility | AK | normalized_active_window_coverage_below_threshold | 999999-26655 | 0.934586 | -33.700 |
| NSB Point Lay Utility | AK | normalized_active_window_coverage_below_threshold | 702460-99999 | 0.938422 | -50.800 |
| NSB Wainwright Utility | AK | normalized_active_window_coverage_below_threshold | 702460-99999 | 0.938422 | -50.800 |
| Noatak | AK | normalized_active_window_coverage_below_threshold | 702460-99999 | 0.938422 | -50.800 |
| Kivalina | AK | normalized_active_window_coverage_below_threshold | 999999-26655 | 0.934586 | -33.700 |
| Ambler | AK | normalized_active_window_coverage_below_threshold | 702460-99999 | 0.938422 | -50.800 |
| APC1 | AL | no_station_candidates |  |  |  |
| APC2 | AL | no_station_candidates |  |  |  |
| APC3 | AL | no_station_candidates |  |  |  |
| Unsited | FL | no_station_candidates |  |  |  |
| NA 1 | FL | no_station_candidates |  |  |  |
| Unnamed | FL | no_station_candidates |  |  |  |
| Midway | FL | no_station_candidates |  |  |  |
| Tampa Electric Co NA 4 | FL | no_station_candidates |  |  |  |
| GPC3 | GA | no_station_candidates |  |  |  |
| GPC4 | GA | no_station_candidates |  |  |  |
| GPC5 | GA | no_station_candidates |  |  |  |
| GPC6 | GA | no_station_candidates |  |  |  |
| MEAG1 | GA | no_station_candidates |  |  |  |
| MEAG2 | GA | no_station_candidates |  |  |  |
| MEAG3 | GA | no_station_candidates |  |  |  |
| NA 1 (IN) | IN | no_station_candidates |  |  |  |
| Unknown | KY | no_station_candidates |  |  |  |
| MPC1 | MS | no_station_candidates |  |  |  |
| NA 1 (NC) | NC | no_station_candidates |  |  |  |
| Future Gen Plant 1 | NC | no_station_candidates |  |  |  |
| Future Gen Plant 2 | NC | no_station_candidates |  |  |  |
| Eddy County Generating Station | NM | no_station_candidates |  |  |  |
| NA 1 (SC) | SC | no_station_candidates |  |  |  |
| NA 5 | SC | no_station_candidates |  |  |  |
| NA 8 | SC | no_station_candidates |  |  |  |
| Turbine | TX | no_station_candidates |  |  |  |
| BayWa r.e Mozart LLC | TX | normalized_active_window_coverage_below_threshold | 723528-99999 | 0.945034 | 14.000 |
| Amadeus Wind Farm | TX | normalized_active_window_coverage_below_threshold | 723528-99999 | 0.945034 | 14.000 |
| Brightside | TX | normalized_active_window_coverage_below_threshold | 722539-99999 | 0.947263 | 24.800 |
| Lumina II Solar Project | TX | normalized_active_window_coverage_below_threshold | 723528-99999 | 0.945034 | 14.000 |
| SPI - Everett | WA | no_station_candidates |  |  |  |
| Wheaton Solar | WI | no_station_candidates |  |  |  |

## Interpretation

- This table materializes a policy scenario into one row per plant in scope.
- `publication_candidate` rows are ECWT-ready under the selected policy, but still require final methodology approval before compliance publication.
- `blocked` rows remain in the table so national-scope coverage is explicit and auditable.
- The conservative fixed-period readiness table is not overwritten.
