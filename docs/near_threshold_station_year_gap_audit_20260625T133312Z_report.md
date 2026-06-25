# Near-Threshold Station-Year Gap Audit

Generated UTC: 2026-06-25T13:33:14+00:00

## Run

- Gap audit run ID: `near_threshold_station_year_gap_audit_20260625T133312Z`
- Priority run ID: `normalized_active_window_blocker_priority_20260625T133017Z`
- Station-year coverage run ID: `station_year_djf_coverage_20260625T124149Z`
- Raw inventory run ID: `noaa_raw_file_inventory_20260625T070816Z`
- Code commit: `aa416c5160e97385c7b1a171d00b27d46df48c8b`
- Max plant gap hours included: `720`
- Station-year CSV: `near_threshold_station_year_gap_audit_20260625T133312Z_station_years.csv`
- Station summary CSV: `near_threshold_station_year_gap_audit_20260625T133312Z_stations.csv`

## Loaded DB Counts

| Check | Rows |
| --- | --- |
| calc.coverage_blocker_station_year_gap | 38 |
| calc.coverage_blocker_station_gap_summary | 5 |

## Station-Year Status Counts

| Coverage Status | Rows |
| --- | --- |
| missing_coverage_row | 38 |

## Raw File Status Counts

| Raw File Status | Rows |
| --- | --- |
| available | 28 |
| missing | 10 |

## Latest Download Status Counts

| Latest Download Status | Rows |
| --- | --- |
| downloaded | 36 |
| (blank) | 2 |

## Top Stations By Impacted Plants

| Station | Name | Plants | Gap Hours | Missing Years | Missing Hours | Raw Missing Years | Top Missing Years |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 702460-99999 | MINCHUMINA | 7 | 126 | 5 | 10847 | 5 | 2000:2184h;2004:2183h;2001:2160h;2002:2160h;2003:2160h |
| 723528-99999 | FREDERICK MUNI | 3 | 65 | 6 | 13007 | 0 | 2000:2184h;2004:2184h;2001:2160h;2002:2160h;2003:2160h;2005:2159h |
| 999999-26655 | RED DOG MINE 3 SSW | 3 | 535 | 16 | 34655 | 0 | 2012:2184h;2016:2184h;2020:2184h;2024:2184h;2010:2160h;2011:2160h;2013:2160h;2014:2160h |
| 722539-99999 | SAN MARCOS MUNI | 1 | 36 | 6 | 13007 | 0 | 2000:2184h;2004:2184h;2001:2160h;2002:2160h;2003:2160h;2005:2159h |
| 703430-99999 | MIDDLETON ISLAND | 1 | 53 | 5 | 10847 | 5 | 2000:2184h;2004:2183h;2001:2160h;2002:2160h;2003:2160h |

## Top Station-Year Gaps

| Station | Year | Plants | Missing Hours | Valid | Expected | Coverage | Raw File | Download |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 702460-99999 | 2000 | 7 | 2184 | 0 | 2184 | missing_coverage_row | missing | downloaded |
| 702460-99999 | 2004 | 7 | 2183 | 0 | 2183 | missing_coverage_row | missing | downloaded |
| 702460-99999 | 2001 | 7 | 2160 | 0 | 2160 | missing_coverage_row | missing | downloaded |
| 702460-99999 | 2002 | 7 | 2160 | 0 | 2160 | missing_coverage_row | missing | downloaded |
| 702460-99999 | 2003 | 7 | 2160 | 0 | 2160 | missing_coverage_row | missing | downloaded |
| 723528-99999 | 2000 | 3 | 2184 | 0 | 2184 | missing_coverage_row | available | downloaded |
| 723528-99999 | 2004 | 3 | 2184 | 0 | 2184 | missing_coverage_row | available | downloaded |
| 999999-26655 | 2012 | 3 | 2184 | 0 | 2184 | missing_coverage_row | available | downloaded |
| 999999-26655 | 2016 | 3 | 2184 | 0 | 2184 | missing_coverage_row | available | downloaded |
| 999999-26655 | 2020 | 3 | 2184 | 0 | 2184 | missing_coverage_row | available | downloaded |
| 999999-26655 | 2024 | 3 | 2184 | 0 | 2184 | missing_coverage_row | available |  |
| 723528-99999 | 2001 | 3 | 2160 | 0 | 2160 | missing_coverage_row | available | downloaded |
| 723528-99999 | 2002 | 3 | 2160 | 0 | 2160 | missing_coverage_row | available | downloaded |
| 723528-99999 | 2003 | 3 | 2160 | 0 | 2160 | missing_coverage_row | available | downloaded |
| 999999-26655 | 2010 | 3 | 2160 | 0 | 2160 | missing_coverage_row | available | downloaded |
| 999999-26655 | 2011 | 3 | 2160 | 0 | 2160 | missing_coverage_row | available | downloaded |
| 999999-26655 | 2013 | 3 | 2160 | 0 | 2160 | missing_coverage_row | available | downloaded |
| 999999-26655 | 2014 | 3 | 2160 | 0 | 2160 | missing_coverage_row | available | downloaded |
| 999999-26655 | 2015 | 3 | 2160 | 0 | 2160 | missing_coverage_row | available |  |
| 999999-26655 | 2017 | 3 | 2160 | 0 | 2160 | missing_coverage_row | available | downloaded |
| 999999-26655 | 2018 | 3 | 2160 | 0 | 2160 | missing_coverage_row | available | downloaded |
| 999999-26655 | 2019 | 3 | 2160 | 0 | 2160 | missing_coverage_row | available | downloaded |
| 999999-26655 | 2021 | 3 | 2160 | 0 | 2160 | missing_coverage_row | available | downloaded |
| 999999-26655 | 2022 | 3 | 2160 | 0 | 2160 | missing_coverage_row | available | downloaded |
| 999999-26655 | 2023 | 3 | 2160 | 0 | 2160 | missing_coverage_row | available | downloaded |
| 723528-99999 | 2005 | 3 | 2159 | 0 | 2159 | missing_coverage_row | available | downloaded |
| 999999-26655 | 2025 | 3 | 2159 | 0 | 2159 | missing_coverage_row | available | downloaded |
| 703430-99999 | 2000 | 1 | 2184 | 0 | 2184 | missing_coverage_row | missing | downloaded |
| 722539-99999 | 2000 | 1 | 2184 | 0 | 2184 | missing_coverage_row | available | downloaded |
| 722539-99999 | 2004 | 1 | 2184 | 0 | 2184 | missing_coverage_row | available | downloaded |
| ... | 8 more rows omitted | | | | | | | |

## Interpretation

- This audit is restricted to plants whose best normalized-active candidate is within the configured valid-hour gap threshold.
- Rows are station-years where the normalized active-window denominator expects DJF hours but the loaded canonical coverage has fewer valid hours.
- If raw files are available and coverage is partial, the issue is likely source sparsity, parsing rejection, or source-observation gaps rather than a missing AWS object.
- If raw files are missing with prior `missing_on_aws`, the public AWS object has already been tested and should not be blindly retried.
- This diagnostic does not alter plant readiness or release status.
