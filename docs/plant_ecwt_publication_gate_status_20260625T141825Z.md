# Plant ECWT Publication Gate Status

Generated UTC: 2026-06-25T14:18:25Z

## Current Position

The NOAA AWS backfill queue is not the active blocker. The current latest-attempt retryable station-year count is zero, and the latest NOAA backfill manifest has no planned rows.

The current all-plants policy result is `plant_ecwt_policy_result_all_plants_normalized_active_window_loaded_year_20260625T135248Z`.

## All-Plants Result

| Status | Reason | Rows |
| --- | --- | ---: |
| `publication_candidate` | `passes_current_fixed_period_gate` | 1,641 |
| `publication_candidate` | `passes_normalized_active_window_policy` | 14,448 |
| `blocked` | `no_station_candidates` | 28 |
| `blocked` | `normalized_active_window_coverage_below_threshold` | 15 |

Total all-plants rows: 16,132.

## First-Operable Publication Scope

| Metric | Rows |
| --- | ---: |
| Asset-backed first-operable policy rows | 13,370 |
| First-operable publication candidates | 13,355 |
| First-operable blocked rows | 15 |
| Generator-derived first-operable plant IDs missing `asset.plant` rows | 1 |

The 28 `no_station_candidates` rows are construction-only (`CN`) asset plants with missing coordinates. They remain in the all-plants exception table, but they are not first-operable publication blockers.

The missing generator-derived first-operable asset row is EIA plant `68815`, generator `GAPPV`, utility `Google, Inc.`, status `OP`, 0.9 MW. It appears in `asset.generator` but has no matching `asset.plant` row and no plant-level location.

## Expanded Candidate Search

The refreshed expanded candidate scenario is `expanded_candidate_coverage_scenario_20260625T141738Z`.

| Search radius km | Plants audited | Passing stations found | Not passing |
| ---: | ---: | ---: | ---: |
| 50 | 15 | 0 | 15 |
| 75 | 15 | 0 | 15 |
| 100 | 15 | 0 | 15 |
| 150 | 15 | 0 | 15 |
| 250 | 15 | 0 | 15 |
| 500 | 15 | 0 | 15 |
| 1000 | 15 | 0 | 15 |

The expanded search used the latest coverage run `station_year_djf_coverage_20260625T124149Z` and latest station ECWT run `station_ecwt_loaded_20260625T124223Z`. It searched loaded stations with provisional station ECWT rows and required both normalized active-window coverage ratio and normalized loaded-year ratio to meet the configured thresholds. No station passed for any of the 15 remaining first-operable coverage blockers within 1,000 km.

## Gate Decision

Current publication-gate interpretation:

- `13,355` first-operable plants are ECWT-ready under the normalized active-window loaded-year policy.
- `15` first-operable plants remain blocked by normalized active-window coverage. The refreshed expanded search found no station-selection-only remedy within 1,000 km.
- `1` first-operable generator-derived plant ID is missing from `asset.plant` and must be resolved as an EIA source/asset-ingest scope gap before it can enter station matching.
- `28` construction-only no-coordinate plants are excluded from first-operable publication readiness but retained in the all-plants exception review.

## Next Work

1. Resolve EIA plant `68815` at the source/asset-ingest layer or document it as a non-locatable generator-level exception.
2. For the 15 first-operable coverage blockers, decide whether the publication method allows a documented coverage-threshold exception, a lower threshold, or a different non-station-selection remediation path.
3. If no exception policy is adopted, the current publishable first-operable set is 13,355 plants, with the 15 coverage blockers and one missing asset row explicitly excluded and documented.
