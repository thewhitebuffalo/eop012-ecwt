# Normalized Active-Window Coverage Blocker Priority

Generated UTC: 2026-06-25T06:01:22+00:00

## Run

- Priority run ID: `normalized_active_window_blocker_priority_20260625T060119Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `c01665c1533c36ef7edfa199c3f7e9a665426f7a`
- Source diagnostic CSV: `fixed_period_denominator_diagnostic_first-operable_20260625T053208Z.csv`
- Detail CSV: `normalized_active_window_blocker_priority_20260625T060119Z_plants.csv`
- Station summary CSV: `normalized_active_window_blocker_priority_20260625T060119Z_stations.csv`
- State summary CSV: `normalized_active_window_blocker_priority_20260625T060119Z_states.csv`
- Normalized active-window coverage threshold: `0.95`

## Loaded DB Counts

| Check | Rows |
| --- | --- |
| calc.coverage_blocker_priority | 7234 |
| calc.coverage_blocker_station_summary | 639 |
| calc.coverage_blocker_state_summary | 50 |
| audit.source_file rows | 1 |

## Gap Buckets

| Bucket | Rows |
| --- | --- |
| gap_le_24h | 156 |
| gap_le_168h | 848 |
| gap_le_720h | 1,351 |
| gap_le_2160h | 3,047 |
| gap_gt_2160h | 1,832 |

## Top Plant States

| State | Plants | Stations | Median Ratio | Total Gap Hours | Gap <= 168h |
| --- | --- | --- | --- | --- | --- |
| CA | 944 | 40 | 0.928960 | 2022333 | 265 |
| TX | 578 | 58 | 0.889392 | 1141488 | 50 |
| NC | 541 | 29 | 0.844974 | 615138 | 68 |
| NY | 472 | 24 | 0.851564 | 1324002 | 2 |
| MN | 461 | 22 | 0.821571 | 788240 | 0 |
| IL | 354 | 25 | 0.844512 | 634816 | 2 |
| NJ | 236 | 15 | 0.865462 | 443630 | 32 |
| FL | 235 | 36 | 0.915468 | 509722 | 54 |
| ME | 220 | 11 | 0.916051 | 947685 | 28 |
| IA | 212 | 27 | 0.648711 | 1302781 | 0 |
| GA | 178 | 24 | 0.880641 | 343969 | 1 |
| MD | 160 | 13 | 0.898505 | 589765 | 0 |
| MA | 155 | 5 | 0.920895 | 79708 | 2 |
| VA | 151 | 24 | 0.892428 | 194381 | 29 |
| WI | 147 | 24 | 0.842295 | 264741 | 18 |
| AK | 129 | 40 | 0.882681 | 292683 | 7 |
| AZ | 128 | 14 | 0.825600 | 142762 | 5 |
| CT | 117 | 7 | 0.888042 | 188684 | 51 |
| CO | 113 | 16 | 0.833641 | 311900 | 0 |
| NV | 109 | 6 | 0.921202 | 159715 | 0 |
| ... | 30 more rows omitted | | | | |

## Top Shared Stations

| Station | Name | Country | Plants | Median Ratio | Total Gap Hours | Top States |
| --- | --- | --- | --- | --- | --- | --- |
| 723898-99999 | HANFORD MUNI | US | 265 | 0.943650 | 21995 | CA:265 |
| 726166-99999 | WILLIAM H MORSE STATE | US | 149 | 0.844697 | 169860 | NY:130;MA:13;VT:6 |
| 725068-99999 | TAUNTON MUNI | US | 129 | 0.920895 | 48891 | MA:129 |
| 720972-99999 | ST MARY HOSPITAL HELIPORT | US | 101 | 0.917313 | 107363 | MN:94;IA:4;WI:3 |
| 997743-99999 | ROBBINS REEF | US | 95 | 0.851564 | 364705 | NJ:72;NY:23 |
| 746929-99999 | DUPLIN CO | US | 91 | 0.844974 | 103467 | NC:91 |
| 727517-99999 | GLENCOE MUNI | US | 86 | 0.817535 | 123324 | MN:86 |
| 999999-94644 | OLD TOWN 2 W | US | 79 | 0.916051 | 139435 | ME:79 |
| 724846-99999 | NORTH LAS VEGAS | US | 77 | 0.921202 | 28875 | NV:61;AZ:12;CA:4 |
| 999999-03758 | DURHAM 11 W | US | 76 | 0.946574 | 10716 | NC:68;VA:8 |
| 720329-99999 | CABLE | US | 74 | 0.852781 | 140230 | CA:74 |
| 745944-93784 | BALTIMORE DOWNTOWN | US | 70 | 0.898505 | 203070 | MD:70 |
| 999999-03047 | MONAHANS 6 ENE | US | 69 | 0.909642 | 138759 | TX:66;NM:3 |
| 726596-99999 | DODGE CENTER | US | 64 | 0.848023 | 70656 | MN:55;IA:9 |
| 724085-99999 | NORTHEAST PHILADELPH | US | 63 | 0.947368 | 1449 | NJ:47;PA:16 |
| 999999-54811 | SHABBONA 5 NNE | US | 62 | 0.941153 | 27342 | IL:62 |
| 999999-03072 | BRONTE 11 NNE | US | 62 | 0.938389 | 31186 | TX:62 |
| 725348-99999 | LEWIS UNIVERSITY | US | 62 | 0.854675 | 63984 | IL:62 |
| 999999-04990 | SIOUX FALLS 14 NNE | US | 62 | 0.916109 | 109244 | MN:53;SD:8;IA:1 |
| 725046-99999 | GROTON NEW LONDON | US | 61 | 0.932595 | 9211 | CT:51;RI:8;NY:2 |
| ... | 619 more rows omitted | | | | | |

## First 20 Priority Rows

| Rank | Plant | State | Station | Ratio | Gap Hours | Distance km | Station Rank |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Lange Generating Station | SD | 726516-99999 | 0.949677 | 3 | 133.151 | 10 |
| 2 | Caledonia | MS | 722286-99999 | 0.949561 | 4 | 78.517 | 8 |
| 3 | RMQ 1 and 2 | NC | 724008-99999 | 0.949569 | 6 | 56.935 | 6 |
| 4 | Warrenton Farm | NC | 724008-99999 | 0.949569 | 6 | 40.680 | 4 |
| 5 | Bolton Farm | NC | 724008-99999 | 0.949569 | 6 | 37.179 | 4 |
| 6 | Franklin Solar, LLC | NC | 724008-99999 | 0.949569 | 6 | 55.001 | 7 |
| 7 | Boseman Solar Center LLC | NC | 724008-99999 | 0.949569 | 6 | 47.983 | 6 |
| 8 | Nash 58 Farm | NC | 724008-99999 | 0.949569 | 6 | 51.306 | 6 |
| 9 | Dement Farm LLC | NC | 724008-99999 | 0.949569 | 6 | 59.374 | 9 |
| 10 | BearPond Solar Center LLC | NC | 724008-99999 | 0.949569 | 6 | 61.644 | 9 |
| 11 | Martin Creek Farm LLC | NC | 724008-99999 | 0.949569 | 6 | 62.095 | 9 |
| 12 | Sarah Solar | NC | 724008-99999 | 0.949569 | 6 | 50.503 | 6 |
| 13 | Melinda Solar | NC | 724008-99999 | 0.949569 | 6 | 60.076 | 9 |
| 14 | Sun Devil Solar | NC | 724008-99999 | 0.949569 | 6 | 22.661 | 1 |
| 15 | Kenneth Solar | NC | 724008-99999 | 0.949569 | 6 | 38.970 | 4 |
| 16 | Franklin Solar 2 | NC | 724008-99999 | 0.949569 | 6 | 51.789 | 7 |
| 17 | Spring Valley Farm 2, LLC | NC | 724008-99999 | 0.949569 | 6 | 62.872 | 9 |
| 18 | Stagecoach Solar | NC | 724008-99999 | 0.949569 | 6 | 66.484 | 9 |
| 19 | Vicksburg Solar | NC | 724008-99999 | 0.949569 | 6 | 57.319 | 6 |
| 20 | Soul City Solar | NC | 724008-99999 | 0.949569 | 6 | 51.895 | 6 |

## Interpretation

- This is a priority queue for the remaining first-operable plants that still fail the conservative normalized active-window coverage screen.
- `valid_hour_gap_to_threshold` is the additional valid DJF-hour count needed for the best normalized-active candidate station to reach the configured coverage threshold.
- Small gaps are likely the cheapest rows to audit first, but a small gap is not proof that a station assignment is publishable.
- The NOAA AWS backfill queue is already exhausted under the corrected manifest; this artifact is for coverage/methodology triage, not blind bulk download.
- The table does not change readiness or release status.
