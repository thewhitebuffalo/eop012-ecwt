# Plant ECWT Strict Publication Candidate Export Report

Generated UTC: 2026-06-25T04:57:23+00:00

## Run

- Export run ID: `plant_ecwt_publication_candidates_first_operable_20260625T045722Z`
- Release ID: `preview-plant_ecwt_publication_candidates_first_operable_20260625T045722Z`
- Code commit: `8ae85365a06b20f0b1e709761b331238d1ef97bb`
- Strict readiness run ID: `plant_ecwt_readiness_fixed_period_20260625T043609Z`
- Plant scope: `first-operable`
- CSV preview: `plant_ecwt_publication_candidates_first_operable_20260625T045722Z.csv`

## Summary

| Metric | Count |
| --- | ---: |
| Exported strict publication candidates | 144 |
| Distinct plant states | 9 |
| Distinct selected stations | 17 |

## Full Readiness Run Counts

| Readiness | Reason | Rows |
| --- | --- | --- |
| blocked | no_candidate_station_with_provisional_ecwt | 15970 |
| publication_candidate | passes_current_publication_gate | 162 |

## Exported Candidates By State

| State | Rows |
| --- | --- |
| NY | 50 |
| UT | 42 |
| WA | 20 |
| MT | 10 |
| VT | 9 |
| ME | 6 |
| ND | 4 |
| ID | 2 |
| NV | 1 |

## Coldest Exported Plant ECWT Values

| Plant | State | Station | ECWT F | Coverage |
| --- | --- | --- | --- | --- |
| Hungry Horse | MT | 711540-99999 | -32.800 | 0.953504 |
| Big Fork | MT | 711540-99999 | -32.800 | 0.953504 |
| Fort Peck | MT | 715160-99999 | -32.800 | 0.950149 |
| Culbertson Generation Station | MT | 715160-99999 | -32.800 | 0.950149 |
| OREG 1 Inc | MT | 715160-99999 | -32.800 | 0.950149 |
| OREG 2 Inc | MT | 715160-99999 | -32.800 | 0.950149 |
| Stoltze CoGen1 | MT | 711540-99999 | -32.800 | 0.953504 |
| Flathead Landfill to Gas Energy Facility | MT | 711540-99999 | -32.800 | 0.953504 |
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
| Brassua Hydroelectric Project | ME | 713230-99999 | -24.160 | 0.953806 |
| Newport | VT | 716110-99999 | -24.160 | 0.957428 |

## Warmest Exported Plant ECWT Values

| Plant | State | Station | ECWT F | Coverage |
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
| McKinley Paper Co. - Washington Mill | WA | 712000-99999 | 3.920 | 0.964618 |
| Boundary | WA | 717760-99999 | -3.100 | 0.964991 |
| Sheep Creek Hydro | WA | 717760-99999 | -3.100 | 0.964991 |
| Kettle Falls Generating Station | WA | 712150-99999 | -3.421 | 0.959647 |
| Wells | WA | 712150-99999 | -3.421 | 0.959647 |
| Chief Joseph | WA | 712150-99999 | -3.421 | 0.959647 |
| Ross | WA | 711140-99999 | -4.000 | 0.960339 |
| Gorge | WA | 711140-99999 | -4.000 | 0.960339 |
| Diablo | WA | 711140-99999 | -4.000 | 0.960339 |
| Newhalem | WA | 711140-99999 | -4.000 | 0.960339 |
| Moyie Springs | ID | 717700-99999 | -5.080 | 0.968222 |

## Interpretation

- This is a preview export of rows that passed the current strict publication gate, not a final compliance release.
- The CSV intentionally excludes provisional low-coverage and blocked rows.
- `first-operable` scope means plants with at least one `OP`, `SB`, `OA`, or `OS` generator status.
- Raw NOAA files and the Postgres database are not included in Git; source lineage and run IDs are retained for reproducibility.
- Before a national release, QA must close out plausibility rejects, warm station ECWT outliers, and station-selection review.
