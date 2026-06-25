# Fixed-Period Gap Cause Report

Generated UTC: 2026-06-25T12:38:52+00:00

## Run

- Diagnostic run ID: `fixed_period_gap_causes_20260625T123832Z`
- Code commit: `41478111915114cd79294d0261f5b9fb6f936f5b`
- Plant ECWT run ID: `plant_ecwt_provisional_fixed_period_20260625T121752Z`
- Candidate run ID: `noaa_station_candidates_20260625T065445Z`
- Station ECWT run ID: `station_ecwt_loaded_20260625T120444Z`
- Station-year coverage run ID: `station_year_djf_coverage_20260625T120423Z`
- Station-year coverage table: `weather.station_year_djf_coverage_current`
- Manifest run ID used for final queue counts: `noaa_backfill_manifest_20260625T070923Z`
- Fixed period: `2000-2025`
- Station-year detail CSV: `fixed_period_gap_causes_20260625T123832Z_station_years.csv`
- Station summary CSV: `fixed_period_gap_causes_20260625T123832Z_stations.csv`

## Summary

| Metric | Count |
| --- | ---: |
| Blocked plant rows | 14,786 |
| Blocked rows with a best provisional station candidate | 14,758 |
| Blocked rows with no best station candidate | 28 |
| Distinct best stations among blocked rows | 127 |
| Best-station years reviewed | 3,302 |
| Best-station years with any fixed-period missing hours | 2,404 |

## Plant ECWT Status Counts

| Status | Rows |
| --- | --- |
| blocked | 14786 |
| provisional | 1346 |

## Final Manifest Status Counts

| Status | Rows |
| --- | --- |
| downloaded | 10282 |
| missing | 1150 |

## Gap Causes

| Cause | Station-Years | Stations | Missing Hours | Plant-Weighted Missing Hours | Station-Year Plant Links |
| --- | --- | --- | --- | --- | --- |
| outside_station_metadata_window | 381 | 91 | 825,912 | 93,464,712 | 43,112 |
| partial_loaded | 491 | 127 | 388,213 | 37,479,092 | 47,313 |
| terminal_aws_missing | 125 | 64 | 270,624 | 20,973,264 | 9,698 |
| complete_loaded | 1,375 | 127 | 29,455 | 2,748,147 | 137,519 |
| empty_loaded | 9 | 7 | 19,536 | 1,366,824 | 629 |
| available_raw_not_loaded | 23 | 8 | 49,872 | 1,273,152 | 587 |

## Top Stations By Plant-Weighted Missing Hours

| Station | Blocked Plants | Coverage | Missing Hours | Plant-Weighted Missing Hours | Top Gap Years |
| --- | --- | --- | --- | --- | --- |
| 999999-53151 FALLBROOK 5 NE | 499 | 0.652198 | 19,591 | 9,775,909 | 2004:outside_station_metadata_window:2184h; 2000:outside_station_metadata_window:2184h; 2007:outside_station_metadata_window:2160h; 2006:outside_station_metadata_window:2160h; 2005:outside_station_metadata_window:2160h; 2003:outside_station_metadata_window:2160h; 2002:outside_station_metadata_window:2160h; 2001:outside_station_metadata_window:2160h |
| 999999-03758 DURHAM 11 W | 559 | 0.691681 | 17,367 | 9,708,153 | 2004:outside_station_metadata_window:2184h; 2000:outside_station_metadata_window:2184h; 2006:outside_station_metadata_window:2160h; 2005:outside_station_metadata_window:2160h; 2003:outside_station_metadata_window:2160h; 2002:outside_station_metadata_window:2160h; 2001:outside_station_metadata_window:2160h; 2007:partial_loaded:1425h |
| 999999-93243 MERCED 23 WSW | 645 | 0.759445 | 13,550 | 8,739,750 | 2000:outside_station_metadata_window:2184h; 2006:terminal_aws_missing:2160h; 2003:outside_station_metadata_window:2160h; 2002:outside_station_metadata_window:2160h; 2001:outside_station_metadata_window:2160h; 2004:partial_loaded:1440h; 2025:partial_loaded:744h; 2009:partial_loaded:471h |
| 999999-54932 SANDSTONE 6 W | 381 | 0.674354 | 18,343 | 6,988,683 | 2004:outside_station_metadata_window:2184h; 2000:outside_station_metadata_window:2184h; 2006:outside_station_metadata_window:2160h; 2005:outside_station_metadata_window:2160h; 2003:outside_station_metadata_window:2160h; 2002:outside_station_metadata_window:2160h; 2001:outside_station_metadata_window:2160h; 2007:partial_loaded:1475h |
| 999999-64756 MILLBROOK 3 W | 577 | 0.806828 | 10,881 | 6,278,337 | 2000:outside_station_metadata_window:2184h; 2003:outside_station_metadata_window:2160h; 2002:outside_station_metadata_window:2160h; 2001:outside_station_metadata_window:2160h; 2004:partial_loaded:1440h; 2025:partial_loaded:744h; 2024:complete_loaded:19h; 2007:complete_loaded:10h |
| 999999-54811 SHABBONA 5 NNE | 663 | 0.832481 | 9,436 | 6,256,068 | 2000:outside_station_metadata_window:2184h; 2002:outside_station_metadata_window:2160h; 2001:outside_station_metadata_window:2160h; 2003:partial_loaded:1416h; 2025:partial_loaded:744h; 2022:partial_loaded:744h; 2024:complete_loaded:20h; 2011:complete_loaded:2h |
| 999999-53139 STOVEPIPE WELLS 1 SW | 449 | 0.805905 | 10,933 | 4,908,917 | 2000:outside_station_metadata_window:2184h; 2003:outside_station_metadata_window:2160h; 2002:outside_station_metadata_window:2160h; 2001:outside_station_metadata_window:2160h; 2004:partial_loaded:1440h; 2025:partial_loaded:744h; 2010:complete_loaded:45h; 2024:complete_loaded:21h |
| 999999-53968 PALESTINE 6 WNW | 355 | 0.802620 | 11,118 | 3,946,890 | 2000:outside_station_metadata_window:2184h; 2006:terminal_aws_missing:2160h; 2002:outside_station_metadata_window:2160h; 2001:outside_station_metadata_window:2160h; 2003:partial_loaded:1416h; 2025:partial_loaded:744h; 2011:complete_loaded:86h; 2008:complete_loaded:85h |
| 999999-03761 AVONDALE 2 N | 225 | 0.704836 | 16,626 | 3,740,850 | 2004:outside_station_metadata_window:2184h; 2000:outside_station_metadata_window:2184h; 2005:outside_station_metadata_window:2160h; 2003:outside_station_metadata_window:2160h; 2002:outside_station_metadata_window:2160h; 2001:outside_station_metadata_window:2160h; 2006:partial_loaded:1416h; 2025:partial_loaded:744h |
| 745944-93784 BALTIMORE DOWNTOWN | 632 | 0.898505 | 5,717 | 3,613,144 | 2021:terminal_aws_missing:2160h; 2022:partial_loaded:1515h; 2025:partial_loaded:856h; 2020:partial_loaded:744h; 2019:partial_loaded:121h; 2023:complete_loaded:96h; 2018:complete_loaded:48h; 2001:complete_loaded:42h |
| 999999-03047 MONAHANS 6 ENE | 317 | 0.804609 | 11,006 | 3,488,902 | 2000:outside_station_metadata_window:2184h; 2006:terminal_aws_missing:2160h; 2002:outside_station_metadata_window:2160h; 2001:outside_station_metadata_window:2160h; 2003:partial_loaded:1419h; 2025:partial_loaded:744h; 2017:complete_loaded:92h; 2021:complete_loaded:23h |
| 999999-54794 DURHAM 2 N | 638 | 0.914430 | 4,820 | 3,075,160 | 2000:outside_station_metadata_window:2184h; 2001:partial_loaded:1820h; 2025:partial_loaded:744h; 2002:complete_loaded:41h; 2024:complete_loaded:18h; 2004:complete_loaded:5h; 2005:complete_loaded:3h; 2007:complete_loaded:2h |
| 999999-04990 SIOUX FALLS 14 NNE | 334 | 0.845459 | 8,705 | 2,907,470 | 2000:outside_station_metadata_window:2184h; 2006:terminal_aws_missing:2160h; 2001:outside_station_metadata_window:2160h; 2002:partial_loaded:1416h; 2025:partial_loaded:744h; 2024:complete_loaded:18h; 2007:complete_loaded:15h; 2005:complete_loaded:6h |
| 999999-04222 REDDING 12 WNW | 297 | 0.834043 | 9,348 | 2,776,356 | 2000:outside_station_metadata_window:2184h; 2002:outside_station_metadata_window:2160h; 2001:outside_station_metadata_window:2160h; 2003:partial_loaded:1516h; 2025:partial_loaded:744h; 2005:partial_loaded:220h; 2006:partial_loaded:192h; 2004:complete_loaded:83h |
| 999999-54808 CHAMPAIGN 9 SW | 254 | 0.808230 | 10,802 | 2,743,708 | 2000:outside_station_metadata_window:2184h; 2006:terminal_aws_missing:2160h; 2001:outside_station_metadata_window:2160h; 2002:partial_loaded:1918h; 2019:partial_loaded:862h; 2025:partial_loaded:744h; 2018:partial_loaded:744h; 2024:complete_loaded:18h |
| 999999-94074 NUNN 7 NNE | 312 | 0.845707 | 8,691 | 2,711,592 | 2000:outside_station_metadata_window:2184h; 2002:outside_station_metadata_window:2160h; 2001:outside_station_metadata_window:2160h; 2003:partial_loaded:1418h; 2025:partial_loaded:744h; 2024:complete_loaded:18h; 2007:complete_loaded:2h; 2005:complete_loaded:2h |
| 999999-54797 KINGSTON 1 W | 426 | 0.887019 | 6,364 | 2,711,064 | 2000:outside_station_metadata_window:2184h; 2001:partial_loaded:1823h; 2023:partial_loaded:786h; 2025:partial_loaded:744h; 2022:partial_loaded:744h; 2002:complete_loaded:24h; 2003:complete_loaded:21h; 2024:complete_loaded:18h |
| 994110-99999 PORT ARANSAS  TX | 206 | 0.767398 | 13,102 | 2,699,012 | 2016:terminal_aws_missing:2184h; 2007:terminal_aws_missing:2160h; 2006:terminal_aws_missing:2160h; 2005:terminal_aws_missing:2160h; 2018:partial_loaded:1416h; 2025:partial_loaded:780h; 2017:partial_loaded:756h; 2011:partial_loaded:456h |
| 999999-53878 ASHEVILLE 13 S | 306 | 0.845334 | 8,712 | 2,665,872 | 2000:empty_loaded:2184h; 2007:terminal_aws_missing:2160h; 2006:terminal_aws_missing:2160h; 2001:partial_loaded:1423h; 2025:partial_loaded:744h; 2024:complete_loaded:20h; 2005:complete_loaded:10h; 2017:complete_loaded:4h |
| 999999-94996 LINCOLN 11 SW | 310 | 0.863620 | 7,682 | 2,381,420 | 2000:outside_station_metadata_window:2184h; 2006:terminal_aws_missing:2160h; 2001:outside_station_metadata_window:2160h; 2025:partial_loaded:744h; 2002:partial_loaded:401h; 2024:complete_loaded:18h; 2019:complete_loaded:9h; 2005:complete_loaded:2h |

## Nearest To Strict Coverage Threshold

| Station | Blocked Plants | Coverage | Missing Hours | Top Gap Years |
| --- | --- | --- | --- | --- |
| 716280-99999 OTTAWA MACDONALD CARTIER INTL | 25 | 0.939053 | 3,433 | 2005:terminal_aws_missing:2160h; 2025:partial_loaded:765h; 2021:complete_loaded:90h; 2004:complete_loaded:67h; 2003:complete_loaded:66h; 2006:complete_loaded:40h; 2000:complete_loaded:40h; 2024:complete_loaded:33h |
| 714300-99999 POINT PETRE (AUT)  ONT | 344 | 0.938876 | 3,443 | 2025:partial_loaded:795h; 2003:partial_loaded:467h; 2000:partial_loaded:461h; 2009:partial_loaded:298h; 2002:partial_loaded:256h; 2015:partial_loaded:255h; 2021:partial_loaded:178h; 2022:complete_loaded:100h |
| 713730-99999 FRELIGHSBURG  QUE | 11 | 0.938734 | 3,451 | 2000:partial_loaded:852h; 2025:partial_loaded:810h; 2003:partial_loaded:343h; 2002:partial_loaded:294h; 2021:partial_loaded:206h; 2001:partial_loaded:183h; 2004:partial_loaded:175h; 2022:complete_loaded:99h |
| 760013-99999 GENERAL ABELARDO L RODRIGUEZ INTL / TIJUANA INTL | 418 | 0.938166 | 3,483 | 2025:partial_loaded:781h; 2021:partial_loaded:327h; 2000:partial_loaded:252h; 2001:partial_loaded:178h; 2003:partial_loaded:141h; 2018:partial_loaded:136h; 2006:partial_loaded:116h; 2004:partial_loaded:115h |
| 712600-99999 SAULT STE MARIE | 37 | 0.936266 | 3,590 | 2005:terminal_aws_missing:2160h; 2025:partial_loaded:766h; 2003:partial_loaded:140h; 2021:partial_loaded:109h; 2004:complete_loaded:108h; 2000:complete_loaded:38h; 2006:complete_loaded:33h; 2024:complete_loaded:31h |
| 715380-99999 WINDSOR | 256 | 0.935698 | 3,622 | 2005:terminal_aws_missing:2160h; 2025:partial_loaded:765h; 2024:partial_loaded:143h; 2021:partial_loaded:119h; 2003:complete_loaded:103h; 2004:complete_loaded:55h; 2006:complete_loaded:37h; 2000:complete_loaded:36h |
| 718620-99999 ESTEVAN A | 1 | 0.930656 | 3,906 | 2005:terminal_aws_missing:2160h; 2025:partial_loaded:764h; 2016:partial_loaded:211h; 2021:partial_loaded:163h; 2015:complete_loaded:99h; 2004:complete_loaded:98h; 2003:complete_loaded:97h; 2006:complete_loaded:37h |
| 717490-99999 THUNDER BAY A | 21 | 0.922312 | 4,376 | 2013:partial_loaded:1417h; 2012:partial_loaded:1251h; 2025:partial_loaded:766h; 2011:partial_loaded:399h; 2021:partial_loaded:109h; 2004:complete_loaded:61h; 2003:complete_loaded:59h; 2000:complete_loaded:38h |
| 999999-54794 DURHAM 2 N | 638 | 0.914430 | 4,820 | 2000:outside_station_metadata_window:2184h; 2001:partial_loaded:1820h; 2025:partial_loaded:744h; 2002:complete_loaded:41h; 2024:complete_loaded:18h; 2004:complete_loaded:5h; 2005:complete_loaded:3h; 2007:complete_loaded:2h |
| 999999-54795 DURHAM 2 SSW | 52 | 0.907027 | 5,237 | 2000:outside_station_metadata_window:2184h; 2001:partial_loaded:1838h; 2025:partial_loaded:744h; 2002:partial_loaded:382h; 2017:complete_loaded:63h; 2024:complete_loaded:18h; 2005:complete_loaded:3h; 2004:complete_loaded:2h |

## Interpretation

- `outside_station_metadata_window` means NOAA station first/last observation metadata does not overlap that source year's January-February or December DJF windows. Under the strict fixed-period denominator, those hours still count as missing.
- `terminal_aws_missing` means at least one download attempt or manifest row showed a terminal NOAA AWS missing object for that station-year.
- `partial_loaded` and `complete_loaded` are loaded station-years that still have missing hours against the exact fixed-period denominator; `complete_loaded` is complete by the pipeline coverage-status rule, not necessarily 100.000% complete.
- `available_raw_not_loaded` means the latest raw-file inventory found a local NOAA file, but the current canonical DJF coverage has no loaded station-year row; this is a loader/source-root follow-up, not an AWS download follow-up.
- `raw_inventory_missing` means the latest inventory still reports no local raw file for the station-year.
- `no_download_or_manifest_evidence` should be investigated before publication because it means the current audit trail does not explain the station-year gap.
- With the expanded manifest exhausted, this report is the better work queue than bulk retrying NOAA downloads.
