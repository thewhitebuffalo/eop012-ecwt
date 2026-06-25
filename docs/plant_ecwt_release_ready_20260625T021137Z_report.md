# Plant ECWT Release-Ready Export Report

Generated UTC: 2026-06-25T02:11:37+00:00

## Run

- Export run ID: `plant_ecwt_release_ready_20260625T021137Z`
- Release ID: `preview-plant_ecwt_release_ready_20260625T021137Z`
- Code commit: `05905b52bbc68d40247e103048db2937b21f9818`
- Release gate run ID: `station_selection_review_update_20260625T021117Z`
- CSV preview: `plant_ecwt_release_ready_20260625T021137Z.csv`

## Summary

| Metric | Count |
| --- | ---: |
| Exported release-ready rows | 162 |
| Distinct plant states | 10 |
| Distinct selected stations | 19 |

## Full Release Gate Counts

| Release Status | Reason | Rows |
| --- | --- | --- |
| blocked_readiness | upstream_no_candidate_station_with_provisional_ecwt | 15970 |
| release_ready | station_selection_review_accepted | 162 |

## Exported Rows By Plant State

| State | Rows |
| --- | --- |
| NY | 52 |
| UT | 50 |
| WA | 23 |
| MT | 11 |
| VT | 10 |
| ME | 6 |
| ND | 5 |
| ID | 2 |
| NV | 2 |
| MI | 1 |

## Exported Rows By Station Country

| Country | Rows |
| --- | --- |
| CA | 110 |
| US | 52 |

## Exported Rows By Review Basis

| Review Basis | Rows |
| --- | --- |
| policy_override | 162 |

## Coldest Exported Plant ECWT Values

| Plant | State | Station | Governing ECWT F | Coverage |
| --- | --- | --- | --- | --- |
| Hungry Horse | MT | 711540-99999 | -32.800 | 0.953504 |
| Big Fork | MT | 711540-99999 | -32.800 | 0.953504 |
| Fort Peck | MT | 715160-99999 | -32.800 | 0.950149 |
| Culbertson Generation Station | MT | 715160-99999 | -32.800 | 0.950149 |
| OREG 1 Inc | MT | 715160-99999 | -32.800 | 0.950149 |
| OREG 2 Inc | MT | 715160-99999 | -32.800 | 0.950149 |
| Stoltze CoGen1 | MT | 711540-99999 | -32.800 | 0.953504 |
| Sand Creek Wind Farm | MT | 715160-99999 | -32.800 | 0.950149 |
| Flathead Landfill to Gas Energy Facility | MT | 711540-99999 | -32.800 | 0.953504 |
| Walhalla | ND | 711470-99999 | -31.000 | 0.969695 |
| Langdon Renewables, LLC | ND | 711480-99999 | -31.000 | 0.960552 |
| Langdon Wind II LLC | ND | 711480-99999 | -31.000 | 0.960552 |
| Langdon Wind Energy Center | ND | 711480-99999 | -31.000 | 0.960552 |
| Border Winds Wind Farm | ND | 711480-99999 | -31.000 | 0.960552 |
| Tiber Dam Hydroelectric Plant | MT | 711160-99999 | -28.573 | 0.962967 |
| ReEnergy Stratton LLC | ME | 716100-99999 | -25.600 | 0.967671 |
| Aziscohos Hydroelectric Project | ME | 716100-99999 | -25.600 | 0.967671 |
| Kibby Wind Facility | ME | 716100-99999 | -25.600 | 0.967671 |
| ME Novel Lighthouse - Carrabassett | ME | 716100-99999 | -25.600 | 0.967671 |
| Harris Hydro | ME | 713230-99999 | -24.160 | 0.953806 |

## Warmest Exported Plant ECWT Values

| Plant | State | Station | Governing ECWT F | Coverage |
| --- | --- | --- | --- | --- |
| Lower Baker | WA | 711080-99999 | 10.400 | 0.976406 |
| Upper Baker | WA | 711080-99999 | 10.400 | 0.976406 |
| Whitehorn | WA | 711080-99999 | 10.400 | 0.976406 |
| Encogen | WA | 711080-99999 | 10.400 | 0.976406 |
| Koma Kulshan | WA | 711080-99999 | 10.400 | 0.976406 |
| Sumas Power Plant | WA | 711080-99999 | 10.400 | 0.976406 |
| Ferndale Generating Station | WA | 711080-99999 | 10.400 | 0.976406 |
| Nooksack Hydro | WA | 711080-99999 | 10.400 | 0.976406 |
| Glacier Battery Storage | WA | 711080-99999 | 10.400 | 0.976406 |
| Glines Hydroelectric Project | WA | 712000-99999 | 3.920 | 0.964618 |
| Elwha Hydroelectric Project | WA | 712000-99999 | 3.920 | 0.964618 |
| McKinley Paper Co. - Washington Mill | WA | 712000-99999 | 3.920 | 0.964618 |
| Boundary | WA | 717760-99999 | -3.100 | 0.964991 |
| Sheep Creek Hydro | WA | 717760-99999 | -3.100 | 0.964991 |
| Kettle Falls Generating Station | WA | 712150-99999 | -3.421 | 0.959647 |
| Wells | WA | 712150-99999 | -3.421 | 0.959647 |
| Chief Joseph | WA | 712150-99999 | -3.421 | 0.959647 |
| Ross | WA | 711140-99999 | -4.000 | 0.960339 |
| Gorge | WA | 711140-99999 | -4.000 | 0.960339 |
| Diablo | WA | 711140-99999 | -4.000 | 0.960339 |

## Interpretation

- This is a preview export of rows that passed fixed-period readiness and station-selection review.
- It is narrower than the publication-candidate export because it uses `publish.plant_ecwt_release_readiness`.
- The CSV intentionally excludes blocked readiness rows and station-review-blocked rows.
- For a national release, remaining blocked rows require additional weather coverage or explicit station-selection policy decisions.
