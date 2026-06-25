# Near-Threshold Station-Year Gap Audit

Generated UTC: 2026-06-25T06:09:08+00:00

## Run

- Gap audit run ID: `near_threshold_station_year_gap_audit_20260625T060905Z`
- Priority run ID: `normalized_active_window_blocker_priority_20260625T060119Z`
- Station-year coverage run ID: `station_year_djf_coverage_20260625T035921Z`
- Raw inventory run ID: `noaa_raw_file_inventory_20260625T043845Z`
- Code commit: `91ee4573222883b4af5ef2849478aa46acdb117c`
- Max plant gap hours included: `168`
- Station-year CSV: `near_threshold_station_year_gap_audit_20260625T060905Z_station_years.csv`
- Station summary CSV: `near_threshold_station_year_gap_audit_20260625T060905Z_stations.csv`

## Loaded DB Counts

| Check | Rows |
| --- | --- |
| calc.coverage_blocker_station_year_gap | 279 |
| calc.coverage_blocker_station_gap_summary | 49 |

## Station-Year Status Counts

| Coverage Status | Rows |
| --- | --- |
| complete | 164 |
| partial | 115 |

## Raw File Status Counts

| Raw File Status | Rows |
| --- | --- |
| available | 279 |

## Latest Download Status Counts

| Latest Download Status | Rows |
| --- | --- |
| downloaded | 247 |
| (blank) | 32 |

## Top Stations By Impacted Plants

| Station | Name | Plants | Gap Hours | Missing Years | Missing Hours | Raw Missing Years | Top Missing Years |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 723898-99999 | HANFORD MUNI | 265 | 83 | 6 | 732 | 0 | 2003:397h;2004:164h;2000:90h;2001:38h;2005:23h;2002:20h |
| 999999-03758 | DURHAM 11 W | 76 | 141 | 6 | 2198 | 0 | 2007:1425h;2025:743h;2024:20h;2017:4h;2009:3h;2020:3h |
| 724085-99999 | NORTHEAST PHILADELPH | 63 | 23 | 4 | 455 | 0 | 2003:360h;2000:54h;2002:28h;2001:13h |
| 725046-99999 | GROTON NEW LONDON | 61 | 151 | 4 | 583 | 0 | 2001:295h;2002:114h;2003:89h;2000:85h |
| 724008-99999 | HALIFAX CO | 56 | 6 | 6 | 655 | 0 | 2002:338h;2000:126h;2004:77h;2003:71h;2005:22h;2001:21h |
| 724096-99999 | MC GUIRE AFB | 32 | 118 | 5 | 659 | 0 | 2002:198h;2003:157h;2001:128h;2004:90h;2000:86h |
| 723116-99999 | DARLINGTON CO JETPOR | 32 | 126 | 6 | 775 | 0 | 2001:372h;2003:113h;2002:102h;2000:98h;2004:79h;2005:11h |
| 725327-99999 | PORTER CO MUNI | 30 | 167 | 6 | 816 | 0 | 2005:251h;2004:213h;2003:147h;2002:126h;2000:53h;2001:26h |
| 727130-99999 | PRESQUE ISLE (AWOS) | 28 | 123 | 4 | 555 | 0 | 2000:306h;2003:147h;2001:73h;2002:29h |
| 722068-53860 | JACKSONVILLE/CRAIG | 26 | 150 | 6 | 907 | 0 | 2010:744h;2004:52h;2007:50h;2006:44h;2005:13h;2009:4h |
| 723528-99999 | FREDERICK MUNI | 25 | 65 | 6 | 714 | 0 | 2001:206h;2005:147h;2003:140h;2004:103h;2000:65h;2002:53h |
| 723104-99999 | COLUMBIA OWENS APT | 23 | 29 | 6 | 678 | 0 | 2000:194h;2003:147h;2001:110h;2004:96h;2005:68h;2002:63h |
| 722539-99999 | SAN MARCOS MUNI | 22 | 36 | 6 | 685 | 0 | 2005:184h;2001:170h;2000:160h;2003:74h;2002:60h;2004:37h |
| 722034-99999 | CHARLOTTE CO | 20 | 58 | 6 | 707 | 0 | 2004:261h;2003:165h;2002:99h;2000:87h;2001:64h;2005:31h |
| 999999-03074 | LAS CRUCES 20 N | 20 | 157 | 10 | 2214 | 0 | 2007:1410h;2025:743h;2021:22h;2024:19h;2010:4h;2011:4h;2012:4h;2009:3h |
| 724116-99999 | DUBLIN/NEW RIV VLLY | 19 | 162 | 4 | 594 | 0 | 2000:236h;2003:185h;2001:106h;2002:67h |
| 725686-99999 | CONVERSE CO | 18 | 131 | 6 | 780 | 0 | 2000:279h;2005:157h;2002:149h;2003:105h;2001:45h;2004:45h |
| 999999-54903 | NECEDAH 5 WNW | 18 | 139 | 8 | 2521 | 0 | 2004:1440h;2025:743h;2022:175h;2006:113h;2009:27h;2024:19h;2007:3h;2005:1h |
| 724388-99999 | GOSHEN MUNI | 16 | 15 | 4 | 447 | 0 | 2003:141h;2000:112h;2001:100h;2002:94h |
| 726667-99999 | SOUTH BIG HORN CO | 14 | 79 | 6 | 728 | 0 | 2004:240h;2000:144h;2002:118h;2003:118h;2001:73h;2005:35h |
| ... | 29 more rows omitted | | | | | | |

## Top Station-Year Gaps

| Station | Year | Plants | Missing Hours | Valid | Expected | Coverage | Raw File | Download |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 723898-99999 | 2003 | 265 | 397 | 1763 | 2160 | partial | available | downloaded |
| 723898-99999 | 2004 | 265 | 164 | 2020 | 2184 | partial | available | downloaded |
| 723898-99999 | 2000 | 265 | 90 | 2094 | 2184 | complete | available | downloaded |
| 723898-99999 | 2001 | 265 | 38 | 2122 | 2160 | complete | available | downloaded |
| 723898-99999 | 2005 | 265 | 23 | 2136 | 2159 | complete | available | downloaded |
| 723898-99999 | 2002 | 265 | 20 | 2140 | 2160 | complete | available | downloaded |
| 999999-03758 | 2007 | 76 | 1425 | 735 | 2160 | partial | available | downloaded |
| 999999-03758 | 2025 | 76 | 743 | 1416 | 2159 | partial | available | downloaded |
| 999999-03758 | 2024 | 76 | 20 | 2164 | 2184 | complete | available |  |
| 999999-03758 | 2017 | 76 | 4 | 2156 | 2160 | complete | available |  |
| 999999-03758 | 2009 | 76 | 3 | 2157 | 2160 | complete | available | downloaded |
| 999999-03758 | 2020 | 76 | 3 | 2181 | 2184 | complete | available |  |
| 724085-99999 | 2003 | 63 | 360 | 1799 | 2159 | partial | available | downloaded |
| 724085-99999 | 2000 | 63 | 54 | 2130 | 2184 | complete | available | downloaded |
| 724085-99999 | 2002 | 63 | 28 | 2132 | 2160 | complete | available | downloaded |
| 724085-99999 | 2001 | 63 | 13 | 2147 | 2160 | complete | available | downloaded |
| 725046-99999 | 2001 | 61 | 295 | 1865 | 2160 | partial | available | downloaded |
| 725046-99999 | 2002 | 61 | 114 | 2046 | 2160 | partial | available | downloaded |
| 725046-99999 | 2003 | 61 | 89 | 2070 | 2159 | complete | available | downloaded |
| 725046-99999 | 2000 | 61 | 85 | 2099 | 2184 | complete | available | downloaded |
| 724008-99999 | 2002 | 56 | 338 | 1822 | 2160 | partial | available | downloaded |
| 724008-99999 | 2000 | 56 | 126 | 2058 | 2184 | partial | available | downloaded |
| 724008-99999 | 2004 | 56 | 77 | 2107 | 2184 | complete | available | downloaded |
| 724008-99999 | 2003 | 56 | 71 | 2089 | 2160 | complete | available | downloaded |
| 724008-99999 | 2005 | 56 | 22 | 2137 | 2159 | complete | available | downloaded |
| 724008-99999 | 2001 | 56 | 21 | 2139 | 2160 | complete | available | downloaded |
| 723116-99999 | 2001 | 32 | 372 | 1788 | 2160 | partial | available | downloaded |
| 724096-99999 | 2002 | 32 | 198 | 1962 | 2160 | partial | available | downloaded |
| 724096-99999 | 2003 | 32 | 157 | 2003 | 2160 | partial | available | downloaded |
| 724096-99999 | 2001 | 32 | 128 | 2032 | 2160 | partial | available | downloaded |
| ... | 249 more rows omitted | | | | | | | |

## Interpretation

- This audit is restricted to plants whose best normalized-active candidate is within the configured valid-hour gap threshold.
- Rows are station-years where the normalized active-window denominator expects DJF hours but the loaded canonical coverage has fewer valid hours.
- If raw files are available and coverage is partial, the issue is likely source sparsity, parsing rejection, or source-observation gaps rather than a missing AWS object.
- If raw files are missing with prior `missing_on_aws`, the public AWS object has already been tested and should not be blindly retried.
- This diagnostic does not alter plant readiness or release status.
