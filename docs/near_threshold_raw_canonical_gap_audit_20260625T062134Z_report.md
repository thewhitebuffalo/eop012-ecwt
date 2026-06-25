# Near-Threshold Raw vs Canonical Gap Audit

- Raw/canonical audit run ID: `near_threshold_raw_canonical_gap_audit_20260625T062134Z`
- Gap audit run ID: `near_threshold_station_year_gap_audit_20260625T060905Z`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Station-year CSV: `near_threshold_raw_canonical_gap_audit_20260625T062134Z_station_years.csv`
- Station summary CSV: `near_threshold_raw_canonical_gap_audit_20260625T062134Z_stations.csv`

## Scope

| Metric | Value |
| --- | ---: |
| Station-year rows audited | 279 |
| Stations audited | 49 |
| Gap-table missing hours | 50,529 |
| Canonical missing hours inside selected expected windows | 50,563 |
| Window missing minus gap-table missing hours | 34 |
| Station-years with expected-window count mismatch | 0 |
| Station-years with accepted raw rows absent from canonical table | 0 |

## Missing-Hour Classification

| Reason | Hours |
| --- | --- |
| source_hour_absent | 34,254 |
| loader_invalid_tmp | 16,309 |
| loader_rejected_source | 0 |
| loader_rejected_plausibility | 0 |
| accepted_raw_not_in_canonical | 0 |
| raw_present_unclassified | 0 |

## Top Stations

| Station | Name | State | Years | Window Missing | Gap Missing | Primary | Top Years |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 999999-54903 | NECEDAH 5 WNW | WI | 8 | 2,521 | 2,521 | source_hour_absent | 2004:1440h; 2025:743h; 2022:175h; 2006:113h; 2009:27h; 2024:19h; 2007:3h; 2005:1h |
| 999999-94080 | MEDORA 7 E | ND | 5 | 2,412 | 2,412 | source_hour_absent | 2004:1440h; 2025:743h; 2010:149h; 2024:78h; 2005:2h |
| 999999-94085 | PIERRE 24 S | SD | 7 | 2,310 | 2,310 | source_hour_absent | 2006:1416h; 2025:743h; 2009:55h; 2010:36h; 2022:26h; 2024:19h; 2008:15h |
| 999999-63896 | SCOTTSBORO 2 NE | AL | 12 | 2,287 | 2,287 | source_hour_absent | 2006:1416h; 2025:746h; 2012:40h; 2011:37h; 2024:20h; 2010:13h; 2013:4h; 2007:3h |
| 999999-63895 | RUSSELLVILLE 4 SSE | AL | 10 | 2,223 | 2,223 | source_hour_absent | 2006:1416h; 2025:743h; 2015:26h; 2024:20h; 2007:10h; 2008:3h; 2013:2h; 2009:1h |
| 999999-63869 | FAIRHOPE 3 NE | AL | 12 | 2,219 | 2,219 | source_hour_absent | 2006:1416h; 2025:747h; 2024:19h; 2011:7h; 2014:6h; 2019:5h; 2020:5h; 2010:4h |
| 999999-03074 | LAS CRUCES 20 N | NM | 10 | 2,214 | 2,214 | source_hour_absent | 2007:1410h; 2025:743h; 2021:22h; 2024:19h; 2010:4h; 2011:4h; 2012:4h; 2009:3h |
| 999999-03758 | DURHAM 11 W | NC | 6 | 2,198 | 2,198 | source_hour_absent | 2007:1425h; 2025:743h; 2024:20h; 2017:4h; 2009:3h; 2020:3h |
| 999999-63891 | CLANTON 2 NE | AL | 8 | 2,196 | 2,196 | source_hour_absent | 2007:1418h; 2025:744h; 2024:19h; 2010:6h; 2008:4h; 2017:3h; 2012:1h; 2015:1h |
| 999999-03759 | CHARLOTTESVILLE 2 SSE | VA | 5 | 2,189 | 2,189 | source_hour_absent | 2007:1416h; 2025:743h; 2024:18h; 2016:11h; 2013:1h |
| 999999-53149 | TORREY 7 E | UT | 5 | 2,181 | 2,181 | source_hour_absent | 2007:1416h; 2025:743h; 2024:19h; 2022:2h; 2010:1h |
| 999999-04138 | BRIGHAM CITY 28 WNW | UT | 3 | 2,178 | 2,178 | source_hour_absent | 2007:1416h; 2025:743h; 2024:19h |
| 722068-53860 | JACKSONVILLE/CRAIG | FL | 6 | 907 | 907 | source_hour_absent | 2010:744h; 2004:52h; 2007:50h; 2006:44h; 2005:13h; 2009:4h |
| 725327-99999 | PORTER CO MUNI | IN | 6 | 817 | 816 | loader_invalid_tmp | 2005:252h; 2004:213h; 2003:147h; 2002:126h; 2000:53h; 2001:26h |
| 723754-99999 | ST JOHNS INDUSTRIAL | AZ | 6 | 789 | 788 | loader_invalid_tmp | 2005:377h; 2001:159h; 2003:77h; 2002:68h; 2000:56h; 2004:52h |
| 725686-99999 | CONVERSE CO | WY | 6 | 781 | 780 | loader_invalid_tmp | 2000:279h; 2005:158h; 2002:149h; 2003:105h; 2001:45h; 2004:45h |
| 722347-13833 | HAGLER AAF | MS | 6 | 777 | 777 | source_hour_absent | 2010:745h; 2009:12h; 2006:8h; 2008:6h; 2005:4h; 2007:2h |
| 723116-99999 | DARLINGTON CO JETPOR | SC | 6 | 776 | 775 | loader_invalid_tmp | 2001:372h; 2003:113h; 2002:102h; 2000:98h; 2004:79h; 2005:12h |
| 726777-99999 | BAKER MUNI | MT | 6 | 766 | 765 | loader_invalid_tmp | 2004:294h; 2000:198h; 2003:128h; 2001:65h; 2002:58h; 2005:23h |
| 747540-99999 | ALEXANDRIA INT | LA | 6 | 751 | 750 | loader_invalid_tmp | 2001:318h; 2004:122h; 2000:107h; 2002:104h; 2003:81h; 2005:19h |

## Interpretation

- `source_hour_absent` means no raw NOAA Global Hourly row exists in the local raw file for the expected canonical UTC hour.
- `loader_rejected_source` means raw rows exist, but all rows for the hour use a source code rejected by the current loader configuration.
- `loader_invalid_tmp` means raw rows exist after source filtering, but the NOAA `TMP` value is missing, sentinel, malformed, or quality code `9`.
- `loader_rejected_plausibility` means a parsed temperature exists but is outside the configured loader plausibility range.
- `accepted_raw_not_in_canonical` is the red-flag class: at least one raw row would pass the current loader rules, but `weather.hourly_djf` does not contain the expected station-hour.
- A nonzero window/gap delta means the prior station-year gap table is count-based: it compares normalized active-window expected hours to full station-year valid hours, not to canonical hours clipped to that exact expected window.
