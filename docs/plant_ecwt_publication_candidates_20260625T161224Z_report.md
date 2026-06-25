# Plant ECWT Strict Publication Candidate Export Report

Generated UTC: 2026-06-25T16:12:28+00:00

## Run

- Export run ID: `plant_ecwt_publication_candidates_20260625T161224Z`
- Release ID: `preview-plant_ecwt_publication_candidates_20260625T161224Z`
- Code commit: `bd3c33c8073c2a66057773e07ae474d2b8eb9be4`
- Strict readiness run ID: `plant_ecwt_readiness_fixed_period_20260625T161109Z`
- Plant scope: `all-plants`
- CSV preview: `plant_ecwt_publication_candidates_20260625T161224Z.csv`

## Summary

| Metric | Count |
| --- | ---: |
| Exported strict publication candidates | 1868 |
| Distinct plant states | 18 |
| Distinct selected stations | 34 |

## Full Readiness Run Counts

| Readiness | Reason | Rows |
| --- | --- | --- |
| blocked | no_fixed_period_eligible_candidate_station | 14264 |
| publication_candidate | passes_current_publication_gate | 1868 |

## Exported Candidates By State

| State | Rows |
| --- | --- |
| NY | 646 |
| ME | 258 |
| UT | 143 |
| WA | 143 |
| TX | 107 |
| VT | 106 |
| MI | 96 |
| MT | 79 |
| NV | 69 |
| ND | 62 |
| AK | 54 |
| OH | 27 |
| NH | 23 |
| PA | 18 |
| AZ | 13 |
| ID | 13 |
| MN | 7 |
| OR | 4 |

## Coldest Exported Plant ECWT Values

| Plant | State | Station | ECWT F | Coverage |
| --- | --- | --- | --- | --- |
| Tok | AK | 719650-99999 | -58.000 | 0.974489 |
| Yakutat | AK | 719650-99999 | -58.000 | 0.974489 |
| Northway | AK | 719650-99999 | -58.000 | 0.974489 |
| 7-Mile Ridge Wind Project | AK | 719650-99999 | -58.000 | 0.974489 |
| Slana Generating Station | AK | 719650-99999 | -58.000 | 0.974489 |
| Gwitchyaa Zhee | AK | 719570-99999 | -43.600 | 0.976779 |
| NSB Kaktovik Utility | AK | 719570-99999 | -43.600 | 0.976779 |
| NSB Nuiqsut Utility | AK | 719570-99999 | -43.600 | 0.976779 |
| TNSG South Plant | AK | 719570-99999 | -43.600 | 0.976779 |
| TNSG North Plant | AK | 719570-99999 | -43.600 | 0.976779 |
| Annex Creek | AK | 712220-99999 | -41.800 | 0.961085 |
| Gold Creek | AK | 712220-99999 | -41.800 | 0.961085 |
| Lemon Creek | AK | 712220-99999 | -41.800 | 0.961085 |
| Salmon Creek 1 | AK | 712220-99999 | -41.800 | 0.961085 |
| Skagway | AK | 712220-99999 | -41.800 | 0.961085 |
| Haines | AK | 712220-99999 | -41.800 | 0.961085 |
| Snettisham | AK | 712220-99999 | -41.800 | 0.961085 |
| Petersburg | AK | 712220-99999 | -41.800 | 0.961085 |
| Blue Lake Hydro | AK | 712220-99999 | -41.800 | 0.961085 |
| Wrangell | AK | 712220-99999 | -41.800 | 0.961085 |

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
