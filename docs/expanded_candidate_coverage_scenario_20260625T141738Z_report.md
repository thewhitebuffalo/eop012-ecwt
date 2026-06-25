# Expanded Candidate Coverage Scenario

- Scenario run ID: `expanded_candidate_coverage_scenario_20260625T141738Z`
- Priority run ID: `normalized_active_window_blocker_priority_20260625T133017Z`
- Coverage run ID: `station_year_djf_coverage_20260625T124149Z`
- Station ECWT run ID: `station_ecwt_loaded_20260625T124223Z`
- Search radii km: `[50.0, 75.0, 100.0, 150.0, 250.0, 500.0, 1000.0]`
- Minimum normalized coverage ratio: `0.95`
- Minimum normalized loaded-year ratio: `0.95`
- Plant CSV: `expanded_candidate_coverage_scenario_20260625T141738Z_plants.csv`
- Radius summary CSV: `expanded_candidate_coverage_scenario_20260625T141738Z_radius_summary.csv`
- State summary CSV: `expanded_candidate_coverage_scenario_20260625T141738Z_state_summary.csv`

## Headline

| Metric | Value |
| --- | ---: |
| Near-threshold plants audited | 15 |
| Plants with passing expanded station within max radius | 0 |
| Plants without passing expanded station within max radius | 15 |
| Median nearest passing station rank among loaded stations |  |
| Median nearest passing station rank among all station-history rows |  |

## Radius Summary

| Radius km | Plants | Passing | Not Passing | Pass Rate | Median Distance km | Median Loaded Rank | Median All-Station Rank |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 50.000 | 15 | 0 | 15 | 0.000000 |  |  |  |
| 75.000 | 15 | 0 | 15 | 0.000000 |  |  |  |
| 100.000 | 15 | 0 | 15 | 0.000000 |  |  |  |
| 150.000 | 15 | 0 | 15 | 0.000000 |  |  |  |
| 250.000 | 15 | 0 | 15 | 0.000000 |  |  |  |
| 500.000 | 15 | 0 | 15 | 0.000000 |  |  |  |
| 1000.000 | 15 | 0 | 15 | 0.000000 |  |  |  |

## Nearest Passing Radius Buckets

| Bucket km | Plants |
| --- | ---: |

## Top States

| State | Plants | Passing | Buckets | Median Distance km | Max Distance km |
| --- | --- | --- | --- | --- | --- |
| AK | 11 | 0 |  |  |  |
| TX | 4 | 0 |  |  |  |

## Nearest Passing Examples

| Plant | State | Current Station | Pass Station | Distance km | Loaded Rank | All Rank | Coverage | ECWT F |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Interpretation

- This is a scenario audit only. It does not alter `link.station_candidate`, station selection, readiness, or plant ECWT results.
- The scenario searches loaded stations with provisional station ECWT rows and requires normalized active-window coverage ratio and loaded-year ratio to meet the configured thresholds.
- A pass means an ECWT-ready station exists within the searched radius under the coverage policy. It does not prove the station is meteorologically acceptable for the plant.
- If this scenario is adopted, the real pipeline change is candidate expansion plus station-selection policy review, followed by a full plant ECWT/readiness rebuild.
