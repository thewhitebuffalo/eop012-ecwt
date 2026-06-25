# Plant ECWT Strict Publication Candidate Export Report

Generated UTC: 2026-06-25T12:27:30+00:00

## Run

- Export run ID: `plant_ecwt_publication_candidates_20260625T122728Z`
- Release ID: `preview-plant_ecwt_publication_candidates_20260625T122728Z`
- Code commit: `243c7e86938907ea002e856bf673030226560888`
- Strict readiness run ID: `plant_ecwt_readiness_fixed_period_20260625T121909Z`
- Plant scope: `all-plants`
- CSV preview: `plant_ecwt_publication_candidates_20260625T122728Z.csv`

## Summary

| Metric | Count |
| --- | ---: |
| Exported strict publication candidates | 1346 |
| Distinct plant states | 14 |
| Distinct selected stations | 21 |

## Full Readiness Run Counts

| Readiness | Reason | Rows |
| --- | --- | --- |
| blocked | no_fixed_period_eligible_candidate_station | 14786 |
| publication_candidate | passes_current_publication_gate | 1346 |

## Exported Candidates By State

| State | Rows |
| --- | --- |
| NY | 345 |
| ME | 258 |
| UT | 143 |
| WA | 143 |
| VT | 106 |
| MI | 83 |
| MT | 79 |
| NV | 69 |
| ND | 62 |
| NH | 23 |
| AZ | 13 |
| ID | 13 |
| MN | 5 |
| OR | 4 |

## Coldest Exported Plant ECWT Values

| Plant | State | Station | ECWT F | Coverage |
| --- | --- | --- | --- | --- |
| J E Corette Plant | MT | 711370-99999 | -39.280 | 0.956292 |
| Yellowtail | MT | 711370-99999 | -39.280 | 0.956292 |
| Colstrip | MT | 711370-99999 | -39.280 | 0.956292 |
| South Dry Creek Hydro | MT | 711370-99999 | -39.280 | 0.956292 |
| Colstrip Energy LP | MT | 711370-99999 | -39.280 | 0.956292 |
| Yellowstone Energy LP | MT | 711370-99999 | -39.280 | 0.956292 |
| Hardin Generator Project | MT | 711370-99999 | -39.280 | 0.956292 |
| Phillips 66 Billings Refinery | MT | 711370-99999 | -39.280 | 0.956292 |
| Horse Thief Wind Project, LLC | MT | 711370-99999 | -39.280 | 0.956292 |
| South Mills Solar, LLC | MT | 711370-99999 | -39.280 | 0.956292 |
| Magpie Solar, LLC | MT | 711370-99999 | -39.280 | 0.956292 |
| Western Sugar Cooperative - Billings | MT | 711370-99999 | -39.280 | 0.956292 |
| MTSUN | MT | 711370-99999 | -39.280 | 0.956292 |
| Two Dot Wind Broadview East LLC | MT | 711370-99999 | -39.280 | 0.956292 |
| Beartooth Energy Storage LLC | MT | 711370-99999 | -39.280 | 0.956292 |
| Yellowstone County Generating Station | MT | 711370-99999 | -39.280 | 0.956292 |
| Glendive GT | MT | 715160-99999 | -32.800 | 0.950149 |
| Miles City GT | MT | 715160-99999 | -32.800 | 0.950149 |
| Selis Ksanka Qlispe | MT | 711540-99999 | -32.800 | 0.953504 |
| Milltown | MT | 711540-99999 | -32.800 | 0.953504 |

## Warmest Exported Plant ECWT Values

| Plant | State | Station | ECWT F | Coverage |
| --- | --- | --- | --- | --- |
| Fredonia (WA) | WA | 711080-99999 | 10.400 | 0.976406 |
| Lower Baker | WA | 711080-99999 | 10.400 | 0.976406 |
| Upper Baker | WA | 711080-99999 | 10.400 | 0.976406 |
| Whitehorn | WA | 711080-99999 | 10.400 | 0.976406 |
| Encogen | WA | 711080-99999 | 10.400 | 0.976406 |
| Koma Kulshan | WA | 711080-99999 | 10.400 | 0.976406 |
| Sumas Power Plant | WA | 711080-99999 | 10.400 | 0.976406 |
| Ferndale Generating Station | WA | 711080-99999 | 10.400 | 0.976406 |
| Sierra Pacific Burlington Facility | WA | 711080-99999 | 10.400 | 0.976406 |
| Darrington | WA | 711080-99999 | 10.400 | 0.976406 |
| Nooksack Hydro | WA | 711080-99999 | 10.400 | 0.976406 |
| Glacier Battery Storage | WA | 711080-99999 | 10.400 | 0.976406 |
| Beaver | OR | 712000-99999 | 3.920 | 0.964618 |
| Georgia-Pacific Wauna Mill | OR | 712000-99999 | 3.920 | 0.964618 |
| Port Westward | OR | 712000-99999 | 3.920 | 0.964618 |
| Port Westward Unit 2 | OR | 712000-99999 | 3.920 | 0.964618 |
| Frederickson | WA | 712000-99999 | 3.920 | 0.964618 |
| South Fork Tolt | WA | 712000-99999 | 3.920 | 0.964618 |
| Transalta Centralia Generation | WA | 712000-99999 | 3.920 | 0.964618 |
| Crystal Mountain | WA | 712000-99999 | 3.920 | 0.964618 |

## Interpretation

- This is a preview export of rows that passed the current strict publication gate, not a final compliance release.
- The CSV intentionally excludes provisional low-coverage and blocked rows.
- `first-operable` scope means plants with at least one `OP`, `SB`, `OA`, or `OS` generator status.
- Raw NOAA files and the Postgres database are not included in Git; source lineage and run IDs are retained for reproducibility.
- Before a national release, QA must close out plausibility rejects, warm station ECWT outliers, and station-selection review.
