# Near-Threshold Remediation Assessment

- Assessment timestamp: `20260625T063050Z`
- Priority run ID: `normalized_active_window_blocker_priority_20260625T060119Z`
- Raw/canonical audit run ID: `near_threshold_raw_canonical_gap_audit_20260625T062134Z`

## Findings

| Slice | Plants | Stations | Eligible alternate candidate count | Minimum gap hours | Maximum gap hours |
| --- | ---: | ---: | ---: | ---: | ---: |
| `gap_le_24h` | 156 | 7 | 0 | 3 | 23 |
| `gap_le_168h` | 848 | 42 | 0 | 28 | 167 |

Every one of the 1,004 near-threshold plant blockers has more than one station
candidate in the priority table, but zero have any candidate that already passes
the normalized active-window coverage eligibility gate.

## Root-Cause Split

| Primary selected-station root cause | Plants | Stations | Eligible alternate candidate count | Minimum gap hours | Maximum gap hours |
| --- | ---: | ---: | ---: | ---: | ---: |
| `loader_invalid_tmp` | 616 | 23 | 0 | 6 | 167 |
| `source_hour_absent` | 388 | 26 | 0 | 3 | 157 |

The raw/canonical audit found no `accepted_raw_not_in_canonical` hours. The
canonical loader is not losing usable observations for this near-threshold set.
The missing hours are source absences or raw rows whose `TMP` value is invalid,
sentinel, malformed, or marked with quality code `9`.

## Implication

This near-threshold queue should not drive more AWS bulk downloads. It also
should not drive a canonical loader rewrite unless the methodology changes the
accepted treatment of NOAA `TMP` quality. The next useful work is one of:

1. Expand station-candidate search or policy, then rerun candidate scoring.
2. Decide whether invalid `TMP` rows can be supplemented from another NOAA
   temperature field or rejected permanently under the compliance method.
3. Decide whether a normalized active-window denominator, year-count gate, or
   manual station-selection policy is acceptable for publication.
