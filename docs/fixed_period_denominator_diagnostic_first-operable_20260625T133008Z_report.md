# Fixed-Period Denominator Diagnostic

Generated UTC: 2026-06-25T13:30:09+00:00

## Run

- Diagnostic run ID: `fixed_period_denominator_diagnostic_first-operable_20260625T133008Z`
- Code commit: `eecb8b3f03847a6b12256e488c0105e5e84a1351`
- Plant scope: `first-operable`
- Plant ECWT run ID: `plant_ecwt_provisional_fixed_period_20260625T125534Z`
- Readiness run ID: `plant_ecwt_readiness_fixed_period_20260625T125602Z`
- Candidate run ID: `noaa_station_candidates_20260625T065445Z`
- Station ECWT run ID: `station_ecwt_loaded_20260625T124223Z`
- Station-year coverage run ID: `station_year_djf_coverage_20260625T124149Z`
- Station-year coverage table: `weather.station_year_djf_coverage_current`
- Fixed period: `2000-2025`
- Fixed minimum coverage ratio: `0.95`
- Fixed minimum loaded station-years: `20`
- Detail CSV: `fixed_period_denominator_diagnostic_first-operable_20260625T133008Z.csv`

## Summary

| Metric | Count |
| --- | ---: |
| Blocked plant rows in scope | 11,965 |
| Active-window coverage pass, any candidate | 11,965 |
| Active-window coverage plus 20 loaded fixed years pass, any candidate | 8,276 |
| Active-window coverage plus active-loaded-year-ratio pass, any candidate | 11,965 |
| Normalized active-window coverage pass, any candidate | 11,950 |
| Normalized active-window coverage plus 20 loaded fixed years pass, any candidate | 3,861 |
| Normalized active-window coverage plus active-loaded-year-ratio pass, any candidate | 11,950 |
| Best active-window candidate has valid hours beyond active expected hours | 8,493 |
| Best active-window coverage ratio > 1.00 | 8,493 |
| Best active-window coverage ratio > 1.05 | 361 |
| Maximum best active-window coverage ratio | 8.000 |
| Best normalized active-window candidate has valid hours beyond normalized expected hours | 0 |
| Best normalized active-window coverage ratio > 1.00 | 0 |
| Best normalized active-window coverage ratio > 1.05 | 0 |
| Maximum best normalized active-window coverage ratio | 0.994 |

## Current Fixed-Period Blocker Classes

| Class | Rows |
| --- | --- |
| fixed_coverage_below_threshold | 11,965 |

## Raw Active-Window Sensitivity Classes

| Class | Rows |
| --- | --- |
| would_pass_active_window_coverage_and_active_year_ratio | 11,965 |

## Normalized Active-Window Sensitivity Classes

| Class | Rows |
| --- | --- |
| would_pass_normalized_active_window_coverage_and_active_year_ratio | 11,950 |
| still_fails_normalized_active_window_coverage | 15 |

## Top Blocked Plant States

| Plant State | Rows |
| --- | --- |
| CA | 1,790 |
| NC | 918 |
| TX | 829 |
| MN | 775 |
| MA | 658 |
| NY | 656 |
| IL | 404 |
| NJ | 404 |
| FL | 310 |
| CO | 303 |
| IA | 299 |
| OR | 280 |
| GA | 265 |
| PA | 252 |
| WI | 250 |
| VA | 240 |
| MD | 209 |
| SC | 209 |
| IN | 207 |
| MI | 192 |

## Active-Window Overfill Examples

| Plant | State | Station | Active Ratio | Active Valid | Active Expected | Overfilled Hours | First Obs | Last Obs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Seminole (FL) | FL | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Suwannee River | FL | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Deerhaven Generating Station | FL | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| J D Kennedy | FL | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Northside Generating Station | FL | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Brandy Branch | FL | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Baptist Medical Center | FL | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Fernandina Beach Mill | FL | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Anheuser-Busch Jacksonville | FL | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Fernandina Plant | FL | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Georgia-Pacific Palatka Operations | FL | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Swift Creek Chemical Complex | FL | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Seminole Mill | FL | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Greenland Energy Center | FL | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Trail Ridge Landfill Gas Recovery | FL | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Jacksonville Solar | FL | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Deerhaven Renewable | FL | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Solar Park Gainesville, LLC | FL | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Eight Flags Energy | FL | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Perry Solar Facility | FL | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |

## Still Fails Active-Window Coverage Examples

| Plant | State | Station | Active Ratio | Fixed Ratio | Active Loaded Year Ratio | Distance km | Rank |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |

## Still Fails Normalized Active-Window Coverage Examples

| Plant | State | Station | Normalized Ratio | Fixed Ratio | Normalized Loaded Year Ratio | Distance km | Rank |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Brightside | TX | 722539-99999 | 0.947263 | 0.218754 | 1.000000 | 163.362 | 59 |
| Yakutat | AK | 703430-99999 | 0.945151 | 0.182023 | 1.000000 | 373.143 | 44 |
| BayWa r.e Mozart LLC | TX | 723528-99999 | 0.945034 | 0.218240 | 1.000000 | 209.620 | 33 |
| Amadeus Wind Farm | TX | 723528-99999 | 0.945034 | 0.218240 | 1.000000 | 212.354 | 35 |
| Lumina II Solar Project | TX | 723528-99999 | 0.945034 | 0.218240 | 1.000000 | 230.847 | 39 |
| Kotzebue Hybrid | AK | 702460-99999 | 0.938422 | 0.180727 | 1.000000 | 576.932 | 89 |
| Kiana | AK | 702460-99999 | 0.938422 | 0.180727 | 1.000000 | 508.357 | 75 |
| NSB Atqasuk Utility | AK | 702460-99999 | 0.938422 | 0.180727 | 1.000000 | 764.321 | 97 |
| NSB Point Lay Utility | AK | 702460-99999 | 0.938422 | 0.180727 | 1.000000 | 799.291 | 98 |
| NSB Wainwright Utility | AK | 702460-99999 | 0.938422 | 0.180727 | 1.000000 | 818.938 | 100 |
| Noatak | AK | 702460-99999 | 0.938422 | 0.180727 | 1.000000 | 635.424 | 95 |
| Ambler | AK | 702460-99999 | 0.938422 | 0.180727 | 1.000000 | 437.973 | 59 |
| Barrow | AK | 999999-26655 | 0.934586 | 0.575007 | 1.000000 | 433.235 | 28 |
| NSB Point Hope Utility | AK | 999999-26655 | 0.934586 | 0.575007 | 1.000000 | 161.616 | 6 |
| Kivalina | AK | 999999-26655 | 0.934586 | 0.575007 | 1.000000 | 75.564 | 6 |

## Interpretation

- The current fixed-period gate uses the full 2000-2025 DJF denominator for station eligibility, plus a 20 loaded station-year minimum.
- The raw active-window sensitivity uses NOAA station first/last observation metadata to shrink the expected-hour denominator before testing coverage.
- The normalized active-window sensitivity expands each station window to the union of NOAA station metadata bounds and full loaded station-years observed in `weather.station_year_djf_coverage_current`.
- A large active-window pass count means the full fixed-period denominator is the dominant blocker for many plants.
- Raw active-window ratios above 1.00 are a warning sign, not a pass recommendation: they mean the loaded annual file contributes more valid DJF hours than the station metadata active window expects.
- Normalized active-window overfill counts should be zero or near zero; nonzero values would indicate the normalization rule still understates actual loaded observations.
- This diagnostic supports a methodology decision. It does not change publication readiness or plant ECWT selection by itself.
