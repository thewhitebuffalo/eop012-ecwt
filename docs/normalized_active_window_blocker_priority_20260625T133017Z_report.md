# Normalized Active-Window Coverage Blocker Priority

Generated UTC: 2026-06-25T13:30:19+00:00

## Run

- Priority run ID: `normalized_active_window_blocker_priority_20260625T133017Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `eecb8b3f03847a6b12256e488c0105e5e84a1351`
- Source diagnostic CSV: `fixed_period_denominator_diagnostic_first-operable_20260625T133008Z.csv`
- Detail CSV: `normalized_active_window_blocker_priority_20260625T133017Z_plants.csv`
- Station summary CSV: `normalized_active_window_blocker_priority_20260625T133017Z_stations.csv`
- State summary CSV: `normalized_active_window_blocker_priority_20260625T133017Z_states.csv`
- Normalized active-window coverage threshold: `0.95`

## Loaded DB Counts

| Check | Rows |
| --- | --- |
| calc.coverage_blocker_priority | 15 |
| calc.coverage_blocker_station_summary | 5 |
| calc.coverage_blocker_state_summary | 2 |
| audit.source_file rows | 1 |

## Gap Buckets

| Bucket | Rows |
| --- | --- |
| gap_le_168h | 12 |
| gap_le_720h | 3 |

## Top Plant States

| State | Plants | Stations | Median Ratio | Total Gap Hours | Gap <= 168h |
| --- | --- | --- | --- | --- | --- |
| AK | 11 | 3 | 0.938422 | 2540 | 8 |
| TX | 4 | 2 | 0.945034 | 231 | 4 |

## Top Shared Stations

| Station | Name | Country | Plants | Median Ratio | Total Gap Hours | Top States |
| --- | --- | --- | --- | --- | --- | --- |
| 702460-99999 | MINCHUMINA | US | 7 | 0.938422 | 882 | AK:7 |
| 723528-99999 | FREDERICK MUNI | US | 3 | 0.945034 | 195 | TX:3 |
| 999999-26655 | RED DOG MINE 3 SSW | US | 3 | 0.934586 | 1605 | AK:3 |
| 722539-99999 | SAN MARCOS MUNI | US | 1 | 0.947263 | 36 | TX:1 |
| 703430-99999 | MIDDLETON ISLAND | US | 1 | 0.945151 | 53 | AK:1 |

## First 20 Priority Rows

| Rank | Plant | State | Station | Ratio | Gap Hours | Distance km | Station Rank |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Brightside | TX | 722539-99999 | 0.947263 | 36 | 163.362 | 59 |
| 2 | Yakutat | AK | 703430-99999 | 0.945151 | 53 | 373.143 | 44 |
| 3 | BayWa r.e Mozart LLC | TX | 723528-99999 | 0.945034 | 65 | 209.620 | 33 |
| 4 | Amadeus Wind Farm | TX | 723528-99999 | 0.945034 | 65 | 212.354 | 35 |
| 5 | Lumina II Solar Project | TX | 723528-99999 | 0.945034 | 65 | 230.847 | 39 |
| 6 | Kotzebue Hybrid | AK | 702460-99999 | 0.938422 | 126 | 576.932 | 89 |
| 7 | Kiana | AK | 702460-99999 | 0.938422 | 126 | 508.357 | 75 |
| 8 | NSB Atqasuk Utility | AK | 702460-99999 | 0.938422 | 126 | 764.321 | 97 |
| 9 | NSB Point Lay Utility | AK | 702460-99999 | 0.938422 | 126 | 799.291 | 98 |
| 10 | NSB Wainwright Utility | AK | 702460-99999 | 0.938422 | 126 | 818.938 | 100 |
| 11 | Noatak | AK | 702460-99999 | 0.938422 | 126 | 635.424 | 95 |
| 12 | Ambler | AK | 702460-99999 | 0.938422 | 126 | 437.973 | 59 |
| 13 | Barrow | AK | 999999-26655 | 0.934586 | 535 | 433.235 | 28 |
| 14 | NSB Point Hope Utility | AK | 999999-26655 | 0.934586 | 535 | 161.616 | 6 |
| 15 | Kivalina | AK | 999999-26655 | 0.934586 | 535 | 75.564 | 6 |

## Interpretation

- This is a priority queue for the remaining first-operable plants that still fail the conservative normalized active-window coverage screen.
- `valid_hour_gap_to_threshold` is the additional valid DJF-hour count needed for the best normalized-active candidate station to reach the configured coverage threshold.
- Small gaps are likely the cheapest rows to audit first, but a small gap is not proof that a station assignment is publishable.
- The NOAA AWS backfill queue is already exhausted under the corrected manifest; this artifact is for coverage/methodology triage, not blind bulk download.
- The table does not change readiness or release status.
