# Fixed-Period Readiness Blocker Report

Generated UTC: 2026-06-25T02:16:00+00:00

## Run

- Diagnostic run ID: `fixed_period_readiness_blockers_20260625T021546Z`
- Code commit: `05905b52bbc68d40247e103048db2937b21f9818`
- Plant ECWT run ID: `plant_ecwt_provisional_fixed_period_20260625T012402Z`
- Candidate run ID: `noaa_station_candidates_20260623T210132Z`
- Station ECWT run ID: `station_ecwt_loaded_20260625T004335Z`
- Station-year coverage run ID: `station_year_djf_coverage_20260625T002229Z`
- Fixed period: `2000-2025`
- Fixed minimum coverage ratio: `0.95`
- Fixed minimum loaded station-years: `20`
- Detail CSV: `fixed_period_readiness_blockers_20260625T021546Z.csv`

## Summary

| Metric | Count |
| --- | ---: |
| Blocked plant rows diagnosed | 15,970 |
| Distinct plant states | 51 |

## Blocker Classes

| Blocker Class | Rows |
| --- | --- |
| fixed_coverage_below_threshold | 15923 |
| no_station_candidates | 28 |
| fixed_coverage_and_loaded_years_below_threshold | 19 |

## Top Blocked Plant States

| Plant State | Rows |
| --- | --- |
| CA | 2171 |
| TX | 1368 |
| NY | 1163 |
| NC | 988 |
| MN | 837 |
| MA | 700 |
| IL | 566 |
| NJ | 427 |
| FL | 405 |
| CO | 342 |
| IA | 331 |
| MI | 331 |
| PA | 324 |
| OR | 321 |
| VA | 317 |
| GA | 315 |
| WI | 292 |
| IN | 269 |
| ME | 263 |
| OH | 262 |

## Top Best-Coverage Stations Among Blocked Plants

| Station | Rows |
| --- | --- |
| 723830-23187 SANDBERG | 237 |
| 723890-93193 FRESNO YOSEMITE INTERNATIONAL AIRPORT | 203 |
| 999999-64758 ITHACA 13 E | 202 |
| 744907-14753 EAST MILTON | 185 |
| 725080-14740 BRADLEY INTERNATIONAL AIRPORT | 174 |
| 725180-14735 ALBANY INTERNATIONAL AIRPORT | 164 |
| 997743-99999 ROBBINS REEF | 159 |
| 722866-99999 SAN BERNARDINO INTL | 152 |
| 722970-23129 LONG BEACH / DAUGHERTY FIELD / AIRPORT | 131 |
| 760053-99999 GENERAL RODOLFO SANCHEZ TABOADA INTL / MEXICALI INTL | 129 |
| 725100-94746 WORCESTER REGIONAL AIRPORT | 124 |
| 999999-93243 MERCED 23 WSW | 122 |
| 726580-14922 MINNEAPOLIS-ST PAUL INTERNATIONAL AP | 119 |
| 999999-64756 MILLBROOK 3 W | 115 |
| 720972-99999 ST MARY HOSPITAL HELIPORT | 111 |
| 997280-99999 KINGS POINT | 110 |
| 999999-03072 BRONTE 11 NNE | 101 |
| 723109-99999 MAXTON | 99 |
| 997278-99999 PROVIDENCE | 96 |
| 999999-03047 MONAHANS 6 ENE | 94 |

## Near-Threshold Blocked Examples

| Plant | State | Best Station | Coverage | Loaded Years | Distance km | Rank |
| --- | --- | --- | --- | --- | --- | --- |
| Ogdensburg Power | NY | 716280-99999 | 0.939053 | 25 | 68.767 | 10 |
| Ogdensburg | NY | 716280-99999 | 0.939053 | 25 | 70.290 | 10 |
| Acer | NY | 716280-99999 | 0.939053 | 25 | 74.598 | 9 |
| Fulton Hydro | NY | 714300-99999 | 0.938876 | 26 | 81.666 | 8 |
| Granby | NY | 714300-99999 | 0.938876 | 26 | 81.610 | 8 |
| High Dam | NY | 714300-99999 | 0.938876 | 26 | 68.145 | 7 |
| Minetto | NY | 714300-99999 | 0.938876 | 26 | 72.645 | 7 |
| Nine Mile Point Nuclear Station | NY | 714300-99999 | 0.938876 | 26 | 68.880 | 9 |
| Oswego Harbor Power | NY | 714300-99999 | 0.938876 | 26 | 64.858 | 7 |
| Oswego Falls East | NY | 714300-99999 | 0.938876 | 26 | 82.501 | 8 |
| Oswego Falls West | NY | 714300-99999 | 0.938876 | 26 | 82.431 | 8 |
| Varick | NY | 714300-99999 | 0.938876 | 26 | 67.200 | 7 |
| Rochester 7 | NY | 714300-99999 | 0.938876 | 26 | 73.671 | 5 |
| James A Fitzpatrick | NY | 714300-99999 | 0.938876 | 26 | 68.975 | 9 |
| R E Ginna Nuclear Power Plant | NY | 714300-99999 | 0.938876 | 26 | 63.077 | 5 |
| Indeck Oswego Energy Center | NY | 714300-99999 | 0.938876 | 26 | 66.359 | 7 |
| Oswego County Energy Recovery | NY | 714300-99999 | 0.938876 | 26 | 79.412 | 8 |
| Sithe Independence Station | NY | 714300-99999 | 0.938876 | 26 | 67.624 | 8 |
| Town of Williamson Landfill PV | NY | 714300-99999 | 0.938876 | 26 | 65.475 | 9 |
| Onondaga County- Clearwater | NY | 714300-99999 | 0.938876 | 26 | 67.977 | 7 |
| Oswego County - Fulton Solar | NY | 714300-99999 | 0.938876 | 26 | 84.837 | 9 |
| Monroe County Sites C, D, & E | NY | 714300-99999 | 0.938876 | 26 | 74.362 | 5 |
| Burritt Rd Community Solar Farm | NY | 714300-99999 | 0.938876 | 26 | 79.360 | 10 |
| Furnace Rd Community Solar Farm | NY | 714300-99999 | 0.938876 | 26 | 66.534 | 6 |
| Harbec Energy | NY | 714300-99999 | 0.938876 | 26 | 69.526 | 5 |

## No Provisional Station ECWT Examples

| Plant | State | Nearest Station | Nearest Status | Distance km | Rank |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

## No Station Candidate Examples

| Plant | State | County | Latitude | Longitude | NERC Region | BA |
| --- | --- | --- | --- | --- | --- | --- |
| APC1 | AL |  |  |  | SERC | SOCO |
| APC2 | AL |  |  |  | SERC | SOCO |
| APC3 | AL |  |  |  | SERC | SOCO |
| Unsited | FL |  |  |  | SERC |  |
| NA 1 | FL |  |  |  | SERC |  |
| Unnamed | FL |  |  |  | SERC | SEC |
| Midway | FL | Taylor |  |  | SERC |  |
| Tampa Electric Co NA 4 | FL |  |  |  | SERC |  |
| GPC3 | GA |  |  |  | SERC |  |
| GPC4 | GA |  |  |  | SERC |  |
| GPC5 | GA |  |  |  | SERC |  |
| GPC6 | GA |  |  |  | SERC |  |
| MEAG1 | GA |  |  |  | SERC |  |
| MEAG2 | GA |  |  |  | SERC |  |
| MEAG3 | GA |  |  |  | SERC |  |
| NA 1 (IN) | IN | NOT IN FILE |  |  | RFC |  |
| Unknown | KY |  |  |  | SERC |  |
| MPC1 | MS |  |  |  | SERC |  |
| NA 1 (NC) | NC | NOT IN FILE |  |  | SERC | CPLE |
| Future Gen Plant 1 | NC |  |  |  | SERC | CPLE |
| Future Gen Plant 2 | NC |  |  |  | SERC | CPLE |
| Eddy County Generating Station | NM | Eddy |  |  | WECC |  |
| NA 1 (SC) | SC | NOT IN FILE |  |  | SERC |  |
| NA 5 | SC | NOT IN FILE |  |  | SERC |  |
| NA 8 | SC | NOT IN FILE |  |  | SERC |  |

## Interpretation

- `no_candidate_with_provisional_station_ecwt` means none of the plant's candidate stations has a provisional station ECWT in the selected station ECWT run.
- `fixed_coverage_below_threshold` means at least one candidate has provisional station ECWT, but no candidate reaches the fixed-period coverage threshold.
- `fixed_loaded_years_below_threshold` means the candidate coverage ratio can be high but the station does not satisfy the loaded-year span rule.
- The next data step is to prioritize NOAA backfill and station-candidate expansion around these blocker classes instead of spending effort on rows already release-ready.
