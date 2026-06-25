# Plant ECWT Strict Publication Candidate Export Report

Generated UTC: 2026-06-25T13:38:48+00:00

## Run

- Export run ID: `plant_ecwt_publication_candidates_first_operable_20260625T133846Z`
- Release ID: `preview-plant_ecwt_publication_candidates_first_operable_20260625T133846Z`
- Code commit: `9831c576c8974deb9d26e15e6b0681458d10009f`
- Strict readiness run ID: `plant_ecwt_readiness_fixed_period_20260625T125602Z`
- Plant scope: `first-operable`
- CSV preview: `plant_ecwt_publication_candidates_first_operable_20260625T133846Z.csv`

## Summary

| Metric | Count |
| --- | ---: |
| Exported strict publication candidates | 1405 |
| Distinct plant states | 18 |
| Distinct selected stations | 26 |

## Full Readiness Run Counts

| Readiness | Reason | Rows |
| --- | --- | --- |
| blocked | no_fixed_period_eligible_candidate_station | 14491 |
| publication_candidate | passes_current_publication_gate | 1641 |

## Exported Candidates By State

| State | Rows |
| --- | --- |
| NY | 378 |
| ME | 229 |
| UT | 120 |
| WA | 117 |
| VT | 102 |
| MI | 80 |
| TX | 79 |
| MT | 69 |
| ND | 53 |
| NV | 52 |
| AK | 46 |
| NH | 23 |
| OH | 21 |
| ID | 13 |
| PA | 8 |
| AZ | 6 |
| MN | 5 |
| OR | 4 |

## Coldest Exported Plant ECWT Values

| Plant | State | Station | ECWT F | Coverage |
| --- | --- | --- | --- | --- |
| Annex Creek | AK | 719530-99999 | -54.400 | 0.975110 |
| Gold Creek | AK | 719530-99999 | -54.400 | 0.975110 |
| Lemon Creek | AK | 719530-99999 | -54.400 | 0.975110 |
| Salmon Creek 1 | AK | 719530-99999 | -54.400 | 0.975110 |
| Skagway | AK | 719530-99999 | -54.400 | 0.975110 |
| Haines | AK | 719530-99999 | -54.400 | 0.975110 |
| Snettisham | AK | 719530-99999 | -54.400 | 0.975110 |
| Pelican | AK | 719530-99999 | -54.400 | 0.975110 |
| Auke Bay | AK | 719530-99999 | -54.400 | 0.975110 |
| Hoonah | AK | 719530-99999 | -54.400 | 0.975110 |
| Goat Lake Hydro | AK | 719530-99999 | -54.400 | 0.975110 |
| Kasidaya Creek Hydro | AK | 719530-99999 | -54.400 | 0.975110 |
| Lake Dorothy Hydroelectric Project | AK | 719530-99999 | -54.400 | 0.975110 |
| Industrial Plant | AK | 719530-99999 | -54.400 | 0.975110 |
| Gustavus | AK | 719530-99999 | -54.400 | 0.975110 |
| Gwitchyaa Zhee | AK | 719570-99999 | -43.600 | 0.976779 |
| NSB Kaktovik Utility | AK | 719570-99999 | -43.600 | 0.976779 |
| NSB Nuiqsut Utility | AK | 719570-99999 | -43.600 | 0.976779 |
| TNSG South Plant | AK | 719570-99999 | -43.600 | 0.976779 |
| TNSG North Plant | AK | 719570-99999 | -43.600 | 0.976779 |

## Warmest Exported Plant ECWT Values

| Plant | State | Station | ECWT F | Coverage |
| --- | --- | --- | --- | --- |
| Eagle Pass | TX | 763943-99999 | 30.200 | 0.955280 |
| Laredo | TX | 763943-99999 | 30.200 | 0.955280 |
| Silas Ray | TX | 763943-99999 | 30.200 | 0.955280 |
| Falcon Dam & Power | TX | 763943-99999 | 30.200 | 0.955280 |
| Frontera Energy Center | TX | 763943-99999 | 30.200 | 0.955280 |
| Magic Valley Generating Station | TX | 763943-99999 | 30.200 | 0.955280 |
| Hidalgo Energy Center | TX | 763943-99999 | 30.200 | 0.955280 |
| Pattern Gulf Wind | TX | 763943-99999 | 30.200 | 0.955280 |
| Cedro Hill Wind LLC | TX | 763943-99999 | 30.200 | 0.955280 |
| Hidalgo Wind Farm LLC | TX | 763943-99999 | 30.200 | 0.955280 |
| Los Vientos Wind 1A | TX | 763943-99999 | 30.200 | 0.955280 |
| Los Vientos Wind 1B | TX | 763943-99999 | 30.200 | 0.955280 |
| Magic Valley Wind Farm I LLC | TX | 763943-99999 | 30.200 | 0.955280 |
| Whitetail | TX | 763943-99999 | 30.200 | 0.955280 |
| Stella Wind Farm | TX | 763943-99999 | 30.200 | 0.955280 |
| Bruennings Breeze Wind Farm | TX | 763943-99999 | 30.200 | 0.955280 |
| Cameron Wind 1 LLC | TX | 763943-99999 | 30.200 | 0.955280 |
| Los Vientos Windpower III | TX | 763943-99999 | 30.200 | 0.955280 |
| Los Vientos Windpower IV | TX | 763943-99999 | 30.200 | 0.955280 |
| Red Gate Power Plant | TX | 763943-99999 | 30.200 | 0.955280 |

## Interpretation

- This is a preview export of rows that passed the current strict publication gate, not a final compliance release.
- The CSV intentionally excludes provisional low-coverage and blocked rows.
- `first-operable` scope means plants with at least one `OP`, `SB`, `OA`, or `OS` generator status.
- Raw NOAA files and the Postgres database are not included in Git; source lineage and run IDs are retained for reproducibility.
- Before a national release, QA must close out plausibility rejects, warm station ECWT outliers, and station-selection review.
