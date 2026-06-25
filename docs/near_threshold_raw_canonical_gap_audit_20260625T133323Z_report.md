# Near-Threshold Raw vs Canonical Gap Audit

- Raw/canonical audit run ID: `near_threshold_raw_canonical_gap_audit_20260625T133323Z`
- Gap audit run ID: `near_threshold_station_year_gap_audit_20260625T133312Z`
- Rejected NOAA source codes: `['7']`
- Plausible temperature range C: `-65.0` to `40.0`
- Station-year CSV: `near_threshold_raw_canonical_gap_audit_20260625T133323Z_station_years.csv`
- Station summary CSV: `near_threshold_raw_canonical_gap_audit_20260625T133323Z_stations.csv`

## Scope

| Metric | Value |
| --- | ---: |
| Station-year rows audited | 38 |
| Stations audited | 5 |
| Gap-table missing hours | 82,363 |
| Canonical missing hours inside selected expected windows | 4,929 |
| Window missing minus gap-table missing hours | -77,434 |
| Station-years with expected-window count mismatch | 0 |
| Station-years with accepted raw rows absent from canonical table | 0 |

## Missing-Hour Classification

| Reason | Hours |
| --- | --- |
| source_hour_absent | 3,834 |
| loader_invalid_tmp | 1,095 |
| loader_rejected_source | 0 |
| loader_rejected_plausibility | 0 |
| accepted_raw_not_in_canonical | 0 |
| raw_present_unclassified | 0 |

## Top Stations

| Station | Name | State | Years | Window Missing | Gap Missing | Primary | Top Years |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 999999-26655 | RED DOG MINE 3 SSW | AK | 16 | 2,266 | 34,655 | source_hour_absent | 2010:1416h; 2025:743h; 2017:86h; 2024:19h; 2021:1h; 2022:1h; 2011:0h; 2012:0h |
| 723528-99999 | FREDERICK MUNI | OK | 6 | 715 | 13,007 | loader_invalid_tmp | 2001:206h; 2005:148h; 2003:140h; 2004:103h; 2000:65h; 2002:53h |
| 722539-99999 | SAN MARCOS MUNI | TX | 6 | 686 | 13,007 | loader_invalid_tmp | 2005:185h; 2001:170h; 2000:160h; 2003:74h; 2002:60h; 2004:37h |
| 702460-99999 | MINCHUMINA | AK | 5 | 667 | 10,847 | source_hour_absent | 2002:401h; 2000:99h; 2001:59h; 2003:57h; 2004:51h |
| 703430-99999 | MIDDLETON ISLAND | AK | 5 | 595 | 10,847 | source_hour_absent | 2000:386h; 2001:105h; 2002:45h; 2004:32h; 2003:27h |

## Interpretation

- `source_hour_absent` means no raw NOAA Global Hourly row exists in the local raw file for the expected canonical UTC hour.
- `loader_rejected_source` means raw rows exist, but all rows for the hour use a source code rejected by the current loader configuration.
- `loader_invalid_tmp` means raw rows exist after source filtering, but the NOAA `TMP` value is missing, sentinel, malformed, or quality code `9`.
- `loader_rejected_plausibility` means a parsed temperature exists but is outside the configured loader plausibility range.
- `accepted_raw_not_in_canonical` is the red-flag class: at least one raw row would pass the current loader rules, but `weather.hourly_djf` does not contain the expected station-hour.
- A nonzero window/gap delta means the prior station-year gap table is count-based: it compares normalized active-window expected hours to full station-year valid hours, not to canonical hours clipped to that exact expected window.
