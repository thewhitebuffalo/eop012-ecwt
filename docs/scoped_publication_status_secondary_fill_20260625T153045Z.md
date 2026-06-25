# Scoped Publication Status After Secondary Station Fill

Generated UTC: 2026-06-25T15:30:45Z

## Source Runs

- Policy result run ID: `plant_ecwt_policy_result_all_plants_normalized_active_window_loaded_year_20260625T135248Z`
- Secondary station fill run ID: `secondary_station_fill_ecwt_20260625T152742Z`
- Station candidate run ID: `noaa_station_candidates_20260625T065445Z`
- Station ECWT run ID: `station_ecwt_loaded_20260625T124223Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`

## Scope Decision

The current publication scope excludes:

1. Alaska plants, by user direction.
2. The 28 non-Alaska `no_station_candidates` rows, because they are nonphysical, unsited, unlocatable, or out of first-operable scope under the current EIA asset/generator evidence.

The four remaining non-Alaska low-coverage weather blockers are resolved by documented secondary-station fill. The fill uses the primary station wherever a valid primary dry-bulb observation exists and uses the fallback station only where the primary station is missing a valid hourly dry-bulb value.

## Current Counts

| Metric | Rows |
| --- | ---: |
| All policy-result rows | 16,132 |
| Alaska rows excluded from current publication scope | 157 |
| Non-Alaska rows | 15,975 |
| Non-Alaska policy publication candidates before secondary fill | 15,943 |
| Non-Alaska no-station rows excluded from current publication scope | 28 |
| Non-Alaska low-coverage rows before secondary fill | 4 |
| Non-Alaska low-coverage rows resolved by secondary fill | 4 |
| Current scoped denominator | 15,947 |
| Current scoped ready rows | 15,947 |

## Secondary Fill Rows

| EIA Plant | Plant | Primary Station | Fallback Station | Fallback km | Filled Hours | Composite Hours | Expected Hours | Composite Coverage | ECWT F |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 58048 | BayWa r.e Mozart LLC | `723528-99999` FREDERICK MUNI | `722122-99999` WINSTON FLD | 49.824 | 144 | 12,437 | 13,008 | 0.956104 | 14.000 |
| 62142 | Amadeus Wind Farm | `723528-99999` FREDERICK MUNI | `722122-99999` WINSTON FLD | 46.718 | 144 | 12,437 | 13,008 | 0.956104 | 14.000 |
| 63223 | Brightside | `722539-99999` SAN MARCOS MUNI | `720316-99999` UECES CO | 74.847 | 173 | 12,495 | 13,008 | 0.960563 | 24.800 |
| 65644 | Lumina II Solar Project | `723528-99999` FREDERICK MUNI | `722122-99999` WINSTON FLD | 27.905 | 144 | 12,437 | 13,008 | 0.956104 | 14.000 |

## Interpretation

Under the current scope and documented secondary-fill methodology, the non-Alaska publishable plant set is complete: 15,947 of 15,947 scoped plant rows have an ECWT result and publication-gate coverage evidence.

This does not mean the national project is finished. It means the current scoped plant-level ECWT calculation has no remaining weather-coverage blockers after excluding Alaska and the documented no-station edge cases.

## Remaining Work

1. Convert this scoped status into a release artifact or release-readiness table that downstream users can consume directly.
2. Decide whether the public release should include the excluded Alaska and no-station edge cases as a separate exception file.
3. Export the scoped ready plant ECWT dataset with source run IDs, station IDs, coverage counts, ECWT values, and exception notes.
4. Add a reproducibility note explaining how to rerun the policy result and secondary-fill steps from raw EIA and NOAA inputs.
