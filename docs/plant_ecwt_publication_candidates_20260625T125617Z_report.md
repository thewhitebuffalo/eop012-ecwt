# Plant ECWT Strict Publication Candidate Export Report

Generated UTC: 2026-06-25T12:56:20+00:00

## Run

- Export run ID: `plant_ecwt_publication_candidates_20260625T125617Z`
- Release ID: `preview-plant_ecwt_publication_candidates_20260625T125617Z`
- Code commit: `41478111915114cd79294d0261f5b9fb6f936f5b`
- Strict readiness run ID: `plant_ecwt_readiness_fixed_period_20260625T125602Z`
- Plant scope: `all-plants`
- CSV preview: `plant_ecwt_publication_candidates_20260625T125617Z.csv`

## Summary

| Metric | Count |
| --- | ---: |
| Exported strict publication candidates | 1641 |
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
| NY | 436 |
| ME | 258 |
| UT | 143 |
| WA | 143 |
| TX | 107 |
| VT | 106 |
| MI | 91 |
| MT | 79 |
| NV | 69 |
| ND | 62 |
| AK | 49 |
| OH | 27 |
| NH | 23 |
| AZ | 13 |
| ID | 13 |
| PA | 13 |
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
| Sweetheart Lake Hydroelectric Facility | AK | 719530-99999 | -54.400 | 0.975110 |
| Gustavus | AK | 719530-99999 | -54.400 | 0.975110 |
| Gwitchyaa Zhee | AK | 719570-99999 | -43.600 | 0.976779 |
| NSB Kaktovik Utility | AK | 719570-99999 | -43.600 | 0.976779 |
| NSB Nuiqsut Utility | AK | 719570-99999 | -43.600 | 0.976779 |
| TNSG South Plant | AK | 719570-99999 | -43.600 | 0.976779 |

## Warmest Exported Plant ECWT Values

| Plant | State | Station | ECWT F | Coverage |
| --- | --- | --- | --- | --- |
| Eagle Pass | TX | 763943-99999 | 30.200 | 0.955280 |
| Laredo | TX | 763943-99999 | 30.200 | 0.955280 |
| Silas Ray | TX | 763943-99999 | 30.200 | 0.955280 |
| Falcon Dam & Power | TX | 763943-99999 | 30.200 | 0.955280 |
| Rio Grande Valley Sugar Growers | TX | 763943-99999 | 30.200 | 0.955280 |
| Frontera Energy Center | TX | 763943-99999 | 30.200 | 0.955280 |
| Magic Valley Generating Station | TX | 763943-99999 | 30.200 | 0.955280 |
| Hidalgo Energy Center | TX | 763943-99999 | 30.200 | 0.955280 |
| Pattern Gulf Wind | TX | 763943-99999 | 30.200 | 0.955280 |
| Texas Gulf Wind 2 | TX | 763943-99999 | 30.200 | 0.955280 |
| Cedro Hill Wind LLC | TX | 763943-99999 | 30.200 | 0.955280 |
| Hidalgo Wind Farm LLC | TX | 763943-99999 | 30.200 | 0.955280 |
| Los Vientos Wind 1A | TX | 763943-99999 | 30.200 | 0.955280 |
| Los Vientos Wind 1B | TX | 763943-99999 | 30.200 | 0.955280 |
| Magic Valley Wind Farm I LLC | TX | 763943-99999 | 30.200 | 0.955280 |
| Whitetail | TX | 763943-99999 | 30.200 | 0.955280 |
| Stella Wind Farm | TX | 763943-99999 | 30.200 | 0.955280 |
| Stella Wind Farm II | TX | 763943-99999 | 30.200 | 0.955280 |
| Bruennings Breeze Wind Farm | TX | 763943-99999 | 30.200 | 0.955280 |
| Cameron Wind 1 LLC | TX | 763943-99999 | 30.200 | 0.955280 |

## Interpretation

- This is a preview export of rows that passed the current strict publication gate, not a final compliance release.
- The CSV intentionally excludes provisional low-coverage and blocked rows.
- `first-operable` scope means plants with at least one `OP`, `SB`, `OA`, or `OS` generator status.
- Raw NOAA files and the Postgres database are not included in Git; source lineage and run IDs are retained for reproducibility.
- Before a national release, QA must close out plausibility rejects, warm station ECWT outliers, and station-selection review.
