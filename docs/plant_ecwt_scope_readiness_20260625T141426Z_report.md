# Plant ECWT Scope Readiness Audit

Generated UTC: 2026-06-25T14:14:27+00:00

## Run

- Scope audit run ID: `plant_ecwt_scope_readiness_20260625T141426Z`
- Policy result run ID: `plant_ecwt_policy_result_all_plants_normalized_active_window_loaded_year_20260625T135248Z`
- Exception review run ID: `plant_ecwt_exception_review_20260625T140741Z`
- Code commit: `0107aed32768b2b3afefa10011fad5f86511e70f`
- Summary CSV: `plant_ecwt_scope_readiness_20260625T141426Z_summary.csv`
- Scope gap CSV: `plant_ecwt_scope_readiness_20260625T141426Z_scope_gaps.csv`

## Scope Counts

| Metric | Value | Notes |
| --- | ---: | --- |
| `asset.plant rows` | 16132 |  |
| `generator-derived first-operable plant ids` | 13371 |  |
| `generator-derived first-operable ids with asset.plant rows` | 13370 |  |
| `generator-derived first-operable ids missing asset.plant rows` | 1 | These first-operable generator plant IDs cannot be station-matched until plant identity/location is resolved. |
| `policy result rows` | 16132 |  |
| `policy result first-operable rows` | 13370 |  |
| `first-operable publication candidates` | 13355 |  |
| `first-operable blocked rows` | 15 |  |
| `exception review plant_geocode_required` | 28 | These are all construction-only asset.plant rows, not first-operable publication blockers. |
| `exception review coverage_threshold_exception_review` | 15 | These are the remaining first-operable ECWT blockers after normalized active-window policy materialization. |

## First-Operable Gap Rows

| EIA Plant | Generator | Utility | Status | MW | Action |
| --- | --- | --- | --- | ---: | --- |
| `68815` | `GAPPV` | Google, Inc. | `OP` | 0.9 | Resolve missing plant-level EIA identity/location before including this first-operable generator in station matching or publication denominator. |

## Interpretation

- The all-plants policy result covers every row in `asset.plant`.
- The generator-derived first-operable denominator has one extra plant ID that is absent from `asset.plant` and therefore absent from station matching and ECWT policy results.
- The 28 geocode-required exception-review rows are construction-only (`CN`) asset rows with no first-operable generators; they should not be confused with active ECWT weather blockers.
- After separating that missing asset row, the current first-operable policy state is 13,355 publication candidates and 15 coverage-threshold blockers.

## Key Numbers

- Asset-backed first-operable policy rows: `13370`
- First-operable publication candidates: `13355`
- First-operable blocked rows: `15`
- First-operable generator IDs missing asset rows: `1`
