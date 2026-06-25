# Expanded Candidate Coverage Scenario

- Scenario run ID: `expanded_candidate_coverage_scenario_20260625T064545Z`
- Priority run ID: `normalized_active_window_blocker_priority_20260625T060119Z`
- Coverage run ID: `station_year_djf_coverage_20260625T035921Z`
- Station ECWT run ID: `station_ecwt_loaded_20260625T042423Z`
- Search radii km: `[50.0, 75.0, 100.0, 150.0, 250.0, 500.0, 1000.0]`
- Minimum normalized coverage ratio: `0.95`
- Minimum normalized loaded-year ratio: `0.95`
- Plant CSV: `expanded_candidate_coverage_scenario_20260625T064545Z_plants.csv`
- Radius summary CSV: `expanded_candidate_coverage_scenario_20260625T064545Z_radius_summary.csv`
- State summary CSV: `expanded_candidate_coverage_scenario_20260625T064545Z_state_summary.csv`

## Headline

| Metric | Value |
| --- | ---: |
| Near-threshold plants audited | 1,004 |
| Plants with passing expanded station within max radius | 1,001 |
| Plants without passing expanded station within max radius | 3 |
| Median nearest passing station rank among loaded stations | 24.0 |
| Median nearest passing station rank among all station-history rows | 26.0 |

## Radius Summary

| Radius km | Plants | Passing | Not Passing | Pass Rate | Median Distance km | Median Loaded Rank | Median All-Station Rank |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 50.000 | 1004 | 76 | 928 | 0.075697 | 42.882 | 13.5 | 14.0 |
| 75.000 | 1004 | 256 | 748 | 0.254980 | 59.597 | 15.0 | 15.0 |
| 100.000 | 1004 | 379 | 625 | 0.377490 | 67.512 | 16.0 | 17.0 |
| 150.000 | 1004 | 635 | 369 | 0.632470 | 87.835 | 19.0 | 20.0 |
| 250.000 | 1004 | 995 | 9 | 0.991036 | 124.131 | 23.0 | 26.0 |
| 500.000 | 1004 | 1000 | 4 | 0.996016 | 124.695 | 24.0 | 26.0 |
| 1000.000 | 1004 | 1001 | 3 | 0.997012 | 124.971 | 24.0 | 26.0 |

## Nearest Passing Radius Buckets

| Bucket km | Plants |
| --- | ---: |
| 50.000 | 76 |
| 75.000 | 180 |
| 100.000 | 123 |
| 150.000 | 256 |
| 250.000 | 360 |
| 500.000 | 5 |
| 1000.000 | 1 |

## Top States

| State | Plants | Passing | Buckets | Median Distance km | Max Distance km |
| --- | --- | --- | --- | --- | --- |
| CA | 265 | 265 | 250.000:208;150.000:57 | 174.307 | 211.043 |
| NC | 117 | 117 | 150.000:52;100.000:41;75.000:24 | 91.585 | 133.317 |
| NJ | 79 | 79 | 75.000:40;50.000:39 | 50.384 | 71.130 |
| SC | 56 | 56 | 75.000:27;100.000:18;50.000:8;150.000:3 | 69.471 | 104.380 |
| FL | 54 | 54 | 250.000:26;150.000:19;75.000:6;50.000:2;100.000:1 | 145.661 | 195.028 |
| CT | 51 | 51 | 75.000:48;50.000:2;100.000:1 | 68.140 | 76.130 |
| TX | 50 | 50 | 250.000:25;150.000:15;100.000:5;75.000:5 | 149.937 | 242.550 |
| IN | 44 | 44 | 150.000:30;100.000:8;250.000:6 | 124.523 | 166.011 |
| VA | 36 | 36 | 150.000:24;100.000:8;75.000:4 | 114.084 | 143.227 |
| ME | 28 | 28 | 250.000:28 | 223.892 | 239.432 |
| WY | 28 | 28 | 250.000:27;150.000:1 | 189.438 | 233.838 |
| OH | 24 | 24 | 75.000:13;100.000:11 | 72.473 | 83.287 |
| PA | 22 | 22 | 50.000:14;75.000:4;100.000:3;150.000:1 | 47.385 | 121.779 |
| WI | 18 | 18 | 150.000:8;100.000:8;75.000:1;250.000:1 | 100.949 | 151.267 |
| AL | 15 | 15 | 100.000:9;150.000:3;75.000:3 | 83.561 | 110.874 |
| MT | 15 | 15 | 250.000:10;500.000:5 | 214.383 | 257.879 |
| NM | 12 | 12 | 250.000:6;150.000:6 | 150.074 | 172.563 |
| MS | 10 | 10 | 150.000:9;75.000:1 | 118.295 | 147.467 |
| UT | 9 | 9 | 250.000:7;150.000:2 | 169.332 | 202.117 |
| ID | 8 | 8 | 150.000:6;250.000:2 | 139.576 | 158.939 |

## Nearest Passing Examples

| Plant | State | Current Station | Pass Station | Distance km | Loaded Rank | All Rank | Coverage | ECWT F |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 63023 | PA | 724085-99999 | 724095-99999 | 26.764 | 11 | 11 | 0.972299 | 8.600 |
| 61819 | PA | 724085-99999 | 725113-99999 | 30.731 | 11 | 11 | 0.964330 | 3.200 |
| 54625 | PA | 724085-99999 | 725113-99999 | 30.758 | 11 | 11 | 0.964330 | 3.200 |
| 60809 | NJ | 724085-99999 | 724095-99999 | 31.104 | 11 | 11 | 0.972299 | 8.600 |
| 65465 | NJ | 724085-99999 | 724095-99999 | 31.992 | 12 | 12 | 0.972299 | 8.600 |
| 61073 | NJ | 724085-99999 | 724095-99999 | 32.895 | 11 | 11 | 0.972299 | 8.600 |
| 61074 | NJ | 724085-99999 | 724095-99999 | 32.992 | 11 | 11 | 0.972299 | 8.600 |
| 65329 | NJ | 724085-99999 | 724095-99999 | 33.271 | 12 | 12 | 0.972299 | 8.600 |
| 58793 | NJ | 724085-99999 | 724095-99999 | 33.492 | 11 | 12 | 0.972299 | 8.600 |
| 54250 | PA | 724085-99999 | 724095-99999 | 35.403 | 12 | 12 | 0.972299 | 8.600 |
| 61864 | NJ | 724085-99999 | 724095-99999 | 35.583 | 11 | 12 | 0.972299 | 8.600 |
| 64530 | RI | 725046-99999 | 725079-99999 | 36.101 | 15 | 15 | 0.964483 | 1.400 |
| 56511 | NJ | 724085-99999 | 724095-99999 | 37.002 | 12 | 12 | 0.972299 | 8.600 |
| 56883 | NJ | 724085-99999 | 724095-99999 | 37.002 | 12 | 12 | 0.972299 | 8.600 |
| 54623 | FL | 722037-99999 | 722026-99999 | 37.480 | 10 | 11 | 0.968842 | 39.200 |
| 62301 | RI | 725046-99999 | 725079-99999 | 37.516 | 15 | 16 | 0.964483 | 1.400 |
| 58029 | NJ | 724085-99999 | 724095-99999 | 37.628 | 12 | 12 | 0.972299 | 8.600 |
| 58030 | NJ | 724085-99999 | 724095-99999 | 37.678 | 12 | 12 | 0.972299 | 8.600 |
| 59278 | NJ | 724085-99999 | 724095-99999 | 37.861 | 12 | 12 | 0.972299 | 8.600 |
| 57661 | NJ | 724096-99999 | 724095-99999 | 38.225 | 10 | 11 | 0.972299 | 8.600 |

## Interpretation

- This is a scenario audit only. It does not alter `link.station_candidate`, station selection, readiness, or plant ECWT results.
- The scenario searches loaded stations with provisional station ECWT rows and requires normalized active-window coverage ratio and loaded-year ratio to meet the configured thresholds.
- A pass means an ECWT-ready station exists within the searched radius under the coverage policy. It does not prove the station is meteorologically acceptable for the plant.
- If this scenario is adopted, the real pipeline change is candidate expansion plus station-selection policy review, followed by a full plant ECWT/readiness rebuild.
