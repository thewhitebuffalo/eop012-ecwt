# Fixed-Period Denominator Diagnostic

Generated UTC: 2026-06-25T05:32:08+00:00

## Run

- Diagnostic run ID: `fixed_period_denominator_diagnostic_first-operable_20260625T053208Z`
- Code commit: `bf206949496c2ee9abb576068080783fe7ee4919`
- Plant scope: `first-operable`
- Plant ECWT run ID: `plant_ecwt_provisional_fixed_period_20260625T043543Z`
- Readiness run ID: `plant_ecwt_readiness_fixed_period_20260625T043609Z`
- Candidate run ID: `noaa_station_candidates_20260623T210132Z`
- Station ECWT run ID: `station_ecwt_loaded_20260625T042423Z`
- Station-year coverage run ID: `station_year_djf_coverage_20260625T035921Z`
- Fixed period: `2000-2025`
- Fixed minimum coverage ratio: `0.95`
- Fixed minimum loaded station-years: `20`
- Detail CSV: `fixed_period_denominator_diagnostic_first-operable_20260625T053208Z.csv`

## Summary

| Metric | Count |
| --- | ---: |
| Blocked plant rows in scope | 13,226 |
| Active-window coverage pass, any candidate | 10,968 |
| Active-window coverage plus 20 loaded fixed years pass, any candidate | 1,926 |
| Active-window coverage plus active-loaded-year-ratio pass, any candidate | 10,968 |
| Normalized active-window coverage pass, any candidate | 5,992 |
| Normalized active-window coverage plus 20 loaded fixed years pass, any candidate | 433 |
| Normalized active-window coverage plus active-loaded-year-ratio pass, any candidate | 5,992 |
| Best active-window candidate has valid hours beyond active expected hours | 2,794 |
| Best active-window coverage ratio > 1.00 | 2,794 |
| Best active-window coverage ratio > 1.05 | 36 |
| Maximum best active-window coverage ratio | 8.000 |
| Best normalized active-window candidate has valid hours beyond normalized expected hours | 0 |
| Best normalized active-window coverage ratio > 1.00 | 0 |
| Best normalized active-window coverage ratio > 1.05 | 0 |
| Maximum best normalized active-window coverage ratio | 0.994 |

## Current Fixed-Period Blocker Classes

| Class | Rows |
| --- | --- |
| fixed_coverage_below_threshold | 13,219 |
| fixed_coverage_and_loaded_years_below_threshold | 7 |

## Raw Active-Window Sensitivity Classes

| Class | Rows |
| --- | --- |
| would_pass_active_window_coverage_and_active_year_ratio | 10,968 |
| still_fails_active_window_coverage | 2,258 |

## Normalized Active-Window Sensitivity Classes

| Class | Rows |
| --- | --- |
| still_fails_normalized_active_window_coverage | 7,234 |
| would_pass_normalized_active_window_coverage_and_active_year_ratio | 5,992 |

## Top Blocked Plant States

| Plant State | Rows |
| --- | --- |
| CA | 1,790 |
| NY | 984 |
| NC | 918 |
| TX | 908 |
| MN | 780 |
| MA | 658 |
| IL | 404 |
| NJ | 404 |
| FL | 310 |
| CO | 303 |
| IA | 299 |
| OR | 284 |
| MI | 272 |
| GA | 265 |
| PA | 260 |
| WI | 250 |
| VA | 240 |
| ME | 231 |
| MD | 209 |
| SC | 209 |

## Active-Window Overfill Examples

| Plant | State | Station | Active Ratio | Active Valid | Active Expected | Overfilled Hours | First Obs | Last Obs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| McManus | GA | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Edwin I Hatch | GA | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Jesup Plant | GA | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Brunswick Cellulose | GA | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Interstate Paper LLC Riceboro | GA | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Fort Stewart Solar Facility | GA | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Solar Glynn | GA | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Baxley | GA | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Curry Solar | GA | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Ware Avra I | GA | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Ware Avra II | GA | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Westberry Jesup | GA | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Reidsville Renewables, Inc. | GA | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Pierce Eunice | GA | 720671-99999 | 8.000000 | 8 | 1 | 7 | 2010-01-11T00:00:00Z | 2010-01-11T00:00:00Z |
| Delray | MI | 720113-99999 | 1.400000 | 35 | 25 | 10 | 2004-12-30T00:00:00Z | 2004-12-31T00:00:00Z |
| Hancock | MI | 720113-99999 | 1.400000 | 35 | 25 | 10 | 2004-12-30T00:00:00Z | 2004-12-31T00:00:00Z |
| Northeast (MI) | MI | 720113-99999 | 1.400000 | 35 | 25 | 10 | 2004-12-30T00:00:00Z | 2004-12-31T00:00:00Z |
| Placid 12 | MI | 720113-99999 | 1.400000 | 35 | 25 | 10 | 2004-12-30T00:00:00Z | 2004-12-31T00:00:00Z |
| Putnam (MI) | MI | 720113-99999 | 1.400000 | 35 | 25 | 10 | 2004-12-30T00:00:00Z | 2004-12-31T00:00:00Z |
| Corewell Health Dearborn Campus | MI | 720113-99999 | 1.400000 | 35 | 25 | 10 | 2004-12-30T00:00:00Z | 2004-12-31T00:00:00Z |

## Still Fails Active-Window Coverage Examples

| Plant | State | Station | Active Ratio | Fixed Ratio | Active Loaded Year Ratio | Distance km | Rank |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Cherry Hill | NJ | 724085-99999 | 0.949890 | 0.145718 | 1.000000 | 22.895 | 7 |
| Constellation New Energy Inc | NJ | 724085-99999 | 0.949890 | 0.145718 | 1.000000 | 23.663 | 8 |
| Reeves Station Rd East | NJ | 724085-99999 | 0.949890 | 0.145718 | 1.000000 | 23.922 | 9 |
| JMB Mcguire-Dix-Lakehurst Solar Project | NJ | 724085-99999 | 0.949890 | 0.145718 | 1.000000 | 33.354 | 10 |
| Kinsley Landfill Solar | NJ | 724085-99999 | 0.949890 | 0.145718 | 1.000000 | 33.113 | 8 |
| Medford WWTP | NJ | 724085-99999 | 0.949890 | 0.145718 | 1.000000 | 24.871 | 9 |
| Reeves South | NJ | 724085-99999 | 0.949890 | 0.145718 | 1.000000 | 24.104 | 9 |
| Gloucester Community College Solar | NJ | 724085-99999 | 0.949890 | 0.145718 | 1.000000 | 34.825 | 8 |
| Timber Creek HS | NJ | 724085-99999 | 0.949890 | 0.145718 | 1.000000 | 35.787 | 8 |
| Summit Water Nexus Mt. Holly, LLC Solar | NJ | 724085-99999 | 0.949890 | 0.145718 | 1.000000 | 20.691 | 8 |
| Pemberton Road I | NJ | 724085-99999 | 0.949890 | 0.145718 | 1.000000 | 28.935 | 7 |
| Pemberton Road II | NJ | 724085-99999 | 0.949890 | 0.145718 | 1.000000 | 28.659 | 7 |
| Dix Solar, L.L.C | NJ | 724085-99999 | 0.949890 | 0.145718 | 1.000000 | 35.113 | 10 |
| Owens Corning | NJ | 724085-99999 | 0.949890 | 0.145718 | 1.000000 | 27.280 | 7 |
| Aero Haven Solar | NJ | 724085-99999 | 0.949890 | 0.145718 | 1.000000 | 30.803 | 8 |
| Mount Laurel Solar | NJ | 724085-99999 | 0.949890 | 0.145718 | 1.000000 | 15.762 | 6 |
| Cinnaminson Landfill Solar | NJ | 724085-99999 | 0.949890 | 0.145718 | 1.000000 | 7.720 | 3 |
| Kinsley II Landfill Solar System | NJ | 724085-99999 | 0.949890 | 0.145718 | 1.000000 | 33.287 | 8 |
| DRPA Lindenwold Station Solar Project | NJ | 724085-99999 | 0.949890 | 0.145718 | 1.000000 | 27.855 | 7 |
| DRPA Ashland Station Solar Project | NJ | 724085-99999 | 0.949890 | 0.145718 | 1.000000 | 24.849 | 7 |

## Still Fails Normalized Active-Window Coverage Examples

| Plant | State | Station | Normalized Ratio | Fixed Ratio | Normalized Loaded Year Ratio | Distance km | Rank |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Lange Generating Station | SD | 726516-99999 | 0.949677 | 0.146073 | 1.000000 | 133.151 | 10 |
| RMQ 1 and 2 | NC | 724008-99999 | 0.949569 | 0.219287 | 1.000000 | 56.935 | 6 |
| Warrenton Farm | NC | 724008-99999 | 0.949569 | 0.219287 | 1.000000 | 40.680 | 4 |
| Bolton Farm | NC | 724008-99999 | 0.949569 | 0.219287 | 1.000000 | 37.179 | 4 |
| Franklin Solar, LLC | NC | 724008-99999 | 0.949569 | 0.219287 | 1.000000 | 55.001 | 7 |
| Boseman Solar Center LLC | NC | 724008-99999 | 0.949569 | 0.219287 | 1.000000 | 47.983 | 6 |
| Nash 58 Farm | NC | 724008-99999 | 0.949569 | 0.219287 | 1.000000 | 51.306 | 6 |
| Dement Farm LLC | NC | 724008-99999 | 0.949569 | 0.219287 | 1.000000 | 59.374 | 9 |
| BearPond Solar Center LLC | NC | 724008-99999 | 0.949569 | 0.219287 | 1.000000 | 61.644 | 9 |
| Martin Creek Farm LLC | NC | 724008-99999 | 0.949569 | 0.219287 | 1.000000 | 62.095 | 9 |
| Sarah Solar | NC | 724008-99999 | 0.949569 | 0.219287 | 1.000000 | 50.503 | 6 |
| Melinda Solar | NC | 724008-99999 | 0.949569 | 0.219287 | 1.000000 | 60.076 | 9 |
| Sun Devil Solar | NC | 724008-99999 | 0.949569 | 0.219287 | 1.000000 | 22.661 | 1 |
| Kenneth Solar | NC | 724008-99999 | 0.949569 | 0.219287 | 1.000000 | 38.970 | 4 |
| Franklin Solar 2 | NC | 724008-99999 | 0.949569 | 0.219287 | 1.000000 | 51.789 | 7 |
| Spring Valley Farm 2, LLC | NC | 724008-99999 | 0.949569 | 0.219287 | 1.000000 | 62.872 | 9 |
| Stagecoach Solar | NC | 724008-99999 | 0.949569 | 0.219287 | 1.000000 | 66.484 | 9 |
| Vicksburg Solar | NC | 724008-99999 | 0.949569 | 0.219287 | 1.000000 | 57.319 | 6 |
| Soul City Solar | NC | 724008-99999 | 0.949569 | 0.219287 | 1.000000 | 51.895 | 6 |
| Red Hill Solar Center, LLC | NC | 724008-99999 | 0.949569 | 0.219287 | 1.000000 | 38.082 | 4 |

## Interpretation

- The current fixed-period gate uses the full 2000-2025 DJF denominator for station eligibility, plus a 20 loaded station-year minimum.
- The raw active-window sensitivity uses NOAA station first/last observation metadata to shrink the expected-hour denominator before testing coverage.
- The normalized active-window sensitivity expands each station window to the union of NOAA station metadata bounds and full loaded station-years observed in `weather.station_year_djf_coverage`.
- A large active-window pass count means the full fixed-period denominator is the dominant blocker for many plants.
- Raw active-window ratios above 1.00 are a warning sign, not a pass recommendation: they mean the loaded annual file contributes more valid DJF hours than the station metadata active window expects.
- Normalized active-window overfill counts should be zero or near zero; nonzero values would indicate the normalization rule still understates actual loaded observations.
- This diagnostic supports a methodology decision. It does not change publication readiness or plant ECWT selection by itself.

