# Plant ECWT Release-Ready Export Report

Generated UTC: 2026-06-25T02:08:02+00:00

## Run

- Export run ID: `plant_ecwt_release_ready_20260625T020802Z`
- Release ID: `preview-plant_ecwt_release_ready_20260625T020802Z`
- Code commit: `97cd500d68a0d32f6cec41248a7c1c9f7d9fc19a`
- Release gate run ID: `station_selection_review_update_20260625T020542Z`
- CSV preview: `plant_ecwt_release_ready_20260625T020802Z.csv`

## Summary

| Metric | Count |
| --- | ---: |
| Exported release-ready rows | 108 |
| Distinct plant states | 7 |
| Distinct selected stations | 12 |

## Full Release Gate Counts

| Release Status | Reason | Rows |
| --- | --- | --- |
| blocked_readiness | upstream_no_candidate_station_with_provisional_ecwt | 15970 |
| blocked_station_review | needs_policy_cross_border_station | 34 |
| blocked_station_review | needs_review_high_distance | 20 |
| release_ready | station_selection_review_accepted | 108 |

## Exported Rows By Plant State

| State | Rows |
| --- | --- |
| NY | 43 |
| UT | 32 |
| WA | 15 |
| VT | 10 |
| ND | 5 |
| ID | 2 |
| MI | 1 |

## Exported Rows By Station Country

| Country | Rows |
| --- | --- |
| CA | 76 |
| US | 32 |

## Exported Rows By Review Basis

| Review Basis | Rows |
| --- | --- |
| policy_override | 108 |

## Coldest Exported Plant ECWT Values

| Plant | State | Station | Governing ECWT F | Coverage |
| --- | --- | --- | --- | --- |
| Walhalla | ND | 711470-99999 | -31.000 | 0.969695 |
| Langdon Renewables, LLC | ND | 711480-99999 | -31.000 | 0.960552 |
| Langdon Wind II LLC | ND | 711480-99999 | -31.000 | 0.960552 |
| Langdon Wind Energy Center | ND | 711480-99999 | -31.000 | 0.960552 |
| Border Winds Wind Farm | ND | 711480-99999 | -31.000 | 0.960552 |
| Newport Diesels | VT | 716110-99999 | -24.160 | 0.957428 |
| Newport | VT | 716110-99999 | -24.160 | 0.957428 |
| Canaan | VT | 716110-99999 | -24.160 | 0.957428 |
| West Charleston | VT | 716110-99999 | -24.160 | 0.957428 |
| Allens Falls | NY | 717120-99999 | -23.620 | 0.963162 |
| Chasm | NY | 717120-99999 | -23.620 | 0.963162 |
| East Norfolk | NY | 717120-99999 | -23.620 | 0.963162 |
| Macomb | NY | 717120-99999 | -23.620 | 0.963162 |
| Norfolk | NY | 717120-99999 | -23.620 | 0.963162 |
| Norwood | NY | 717120-99999 | -23.620 | 0.963162 |
| Parishville | NY | 717120-99999 | -23.620 | 0.963162 |
| Raymondville | NY | 717120-99999 | -23.620 | 0.963162 |
| Yaleville | NY | 717120-99999 | -23.620 | 0.963162 |
| Robert Moses Power Dam | NY | 717120-99999 | -23.620 | 0.963162 |
| Sissonville Hydro | NY | 717120-99999 | -23.620 | 0.963162 |

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
| Moyie Springs | ID | 717700-99999 | -5.080 | 0.968222 |
| Smith Falls Hydro Project | ID | 717700-99999 | -5.080 | 0.968222 |
| Sullivan CR | WA | 717700-99999 | -5.080 | 0.968222 |
| Blundell | UT | 724797-23176 | -9.940 | 0.951374 |
| Upper Beaver | UT | 724797-23176 | -9.940 | 0.951374 |
| Milford Wind Corridor I LLC | UT | 724797-23176 | -9.940 | 0.951374 |

## Interpretation

- This is a preview export of rows that passed fixed-period readiness and station-selection review.
- It is narrower than the publication-candidate export because it uses `publish.plant_ecwt_release_readiness`.
- The CSV intentionally excludes blocked readiness rows and station-review-blocked rows.
- For a national release, remaining blocked rows require additional weather coverage or explicit station-selection policy decisions.

