# Fixed-Period Denominator Diagnostic

Generated UTC: 2026-06-25T16:11:54+00:00

## Run

- Diagnostic run ID: `fixed_period_denominator_diagnostic_all-plants_20260625T161153Z`
- Code commit: `bd3c33c8073c2a66057773e07ae474d2b8eb9be4`
- Plant scope: `all-plants`
- Plant ECWT run ID: `plant_ecwt_provisional_fixed_period_20260625T161041Z`
- Readiness run ID: `plant_ecwt_readiness_fixed_period_20260625T161109Z`
- Candidate run ID: `noaa_station_candidates_20260625T065445Z`
- Station ECWT run ID: `station_ecwt_loaded_20260625T155645Z`
- Station-year coverage run ID: `station_year_djf_coverage_20260625T155613Z`
- Station-year coverage table: `weather.station_year_djf_coverage_current`
- Fixed period: `2000-2025`
- Fixed minimum coverage ratio: `0.95`
- Fixed minimum loaded station-years: `20`
- Detail CSV: `fixed_period_denominator_diagnostic_all-plants_20260625T161153Z.csv`

## Summary

| Metric | Count |
| --- | ---: |
| Blocked plant rows in scope | 14,264 |
| Active-window coverage pass, any candidate | 14,236 |
| Active-window coverage plus 20 loaded fixed years pass, any candidate | 9,702 |
| Active-window coverage plus active-loaded-year-ratio pass, any candidate | 14,236 |
| Normalized active-window coverage pass, any candidate | 14,222 |
| Normalized active-window coverage plus 20 loaded fixed years pass, any candidate | 4,476 |
| Normalized active-window coverage plus active-loaded-year-ratio pass, any candidate | 14,222 |
| Best active-window candidate has valid hours beyond active expected hours | 10,352 |
| Best active-window coverage ratio > 1.00 | 10,352 |
| Best active-window coverage ratio > 1.05 | 457 |
| Maximum best active-window coverage ratio | 8.000 |
| Best normalized active-window candidate has valid hours beyond normalized expected hours | 0 |
| Best normalized active-window coverage ratio > 1.00 | 0 |
| Best normalized active-window coverage ratio > 1.05 | 0 |
| Maximum best normalized active-window coverage ratio | 0.994 |

## Current Fixed-Period Blocker Classes

| Class | Rows |
| --- | --- |
| fixed_coverage_below_threshold | 14,236 |
| no_station_candidates | 28 |

## Raw Active-Window Sensitivity Classes

| Class | Rows |
| --- | --- |
| would_pass_active_window_coverage_and_active_year_ratio | 14,236 |
| no_station_candidates | 28 |

## Normalized Active-Window Sensitivity Classes

| Class | Rows |
| --- | --- |
| would_pass_normalized_active_window_coverage_and_active_year_ratio | 14,222 |
| no_station_candidates | 28 |
| still_fails_normalized_active_window_coverage | 14 |

## Top Blocked Plant States

| Plant State | Rows |
| --- | --- |
| CA | 2,171 |
| TX | 1,261 |
| NC | 988 |
| MN | 830 |
| MA | 700 |
| NY | 569 |
| IL | 566 |
| NJ | 427 |
| FL | 405 |
| CO | 342 |
| IA | 331 |
| OR | 317 |
| VA | 317 |
| GA | 315 |
| PA | 306 |
| WI | 292 |
| IN | 269 |
| SC | 259 |
| MD | 246 |
| MI | 236 |

## Active-Window Overfill Examples

| Plant | State | Station | Active Ratio | Active Valid | Active Expected | Overfilled Hours | First Obs | Last Obs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Seminole (FL) | FL | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| St Johns River Power Park | FL | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Suwannee River | FL | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Deerhaven Generating Station | FL | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| J D Kennedy | FL | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Northside Generating Station | FL | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Southside Generating Station | FL | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Putnam | FL | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Girvin Landfill | FL | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Brandy Branch | FL | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Baptist Medical Center | FL | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Fernandina Beach Mill | FL | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Anheuser-Busch Jacksonville | FL | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Fernandina Plant | FL | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Georgia-Pacific Palatka Operations | FL | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Suwannee River Chemical Complex | FL | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Swift Creek Chemical Complex | FL | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Seminole Mill | FL | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Jackson Mill | FL | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Greenland Energy Center | FL | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |

## Still Fails Active-Window Coverage Examples

| Plant | State | Station | Active Ratio | Fixed Ratio | Active Loaded Year Ratio | Distance km | Rank |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |

## Still Fails Normalized Active-Window Coverage Examples

| Plant | State | Station | Normalized Ratio | Fixed Ratio | Normalized Loaded Year Ratio | Distance km | Rank |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Brightside | TX | 722539-99999 | 0.947263 | 0.218754 | 1.000000 | 163.362 | 59 |
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
