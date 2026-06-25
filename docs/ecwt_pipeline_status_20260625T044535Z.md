# ECWT Pipeline Status

Generated UTC: 2026-06-25T06:09:08Z

## Current Checkpoint

| Layer | Current run ID | Rows / status |
| --- | --- | ---: |
| NOAA raw inventory | `noaa_raw_file_inventory_20260625T043845Z` | 62,318 available station-years |
| NOAA AWS backfill manifest | `noaa_backfill_manifest_20260625T043945Z` | 0 planned downloads |
| Station-year DJF coverage | `station_year_djf_coverage_20260625T035921Z` | 62,318 station-years |
| Station ECWT | `station_ecwt_loaded_20260625T042423Z` | 4,250 stations |
| Fixed-period plant ECWT | `plant_ecwt_provisional_fixed_period_20260625T043543Z` | 16,132 plants |
| Fixed-period readiness | `plant_ecwt_readiness_fixed_period_20260625T043609Z` | 162 all-plant candidates; 144 first-operable candidates |
| Readiness policy scenario DB load | `readiness_policy_scenarios_db_load_20260625T054908Z` | 5 scenarios; 20,039 candidate rows |
| Station-selection review seed | `station_selection_review_seed_20260625T055346Z` | 162 review rows; 0 release-ready rows |
| Station-selection policy scenarios | `station_selection_policy_scenarios_20260625T055356Z` | 8 scenarios; 162 current fixed-period candidates |
| Normalized coverage blocker priority | `normalized_active_window_blocker_priority_20260625T060119Z` | 7,234 plant blockers; 639 station summaries; 50 state summaries |
| Near-threshold station-year gap audit | `near_threshold_station_year_gap_audit_20260625T060905Z` | 1,004 plants; 49 stations; 279 station-year gaps |

## Plant Readiness

| Status | Plants |
| --- | ---: |
| Publication candidate, all-plant readiness run | 162 |
| Publication candidate, first-operable export scope | 144 |
| Current release-ready under station-review gate | 0 |
| Blocked | 15,970 |

## NOAA Backfill State

The corrected NOAA inventory includes every local NOAA raw root observed in the loader audit:

- `/Volumes/NOAA_CACHE/EOP012/raw/noaa/global-hourly`
- `/Volumes/NOAA_CACHE/noaa-global-hourly-pds-full`
- `/Volumes/NOAA_CACHE/noaa-global-hourly-year-staging`
- `/Volumes/NOAA_CACHE/BACKUP_TO_DELETE_LATER_noaa-cache_2026-02-19/gh_2012_2022_p1_1000`

With those roots included, there are no remaining station-years that are all of:

- missing locally,
- active during the EOP-012 DJF weather window, and
- not already proven missing from the NOAA public AWS bucket.

The current AWS backfill queue is therefore exhausted under the active ECWT-targeted manifest policy.

## Remaining Blockers

| Blocker class | Plants |
| --- | ---: |
| `fixed_coverage_below_threshold` | 15,923 |
| `fixed_coverage_and_loaded_years_below_threshold` | 19 |
| `no_station_candidates` | 28 |

The next useful work is no longer bulk AWS download. It is station-selection and coverage-policy work:

1. Decide the publication denominator policy: full fixed `2000-2025` DJF hours versus station-active-window DJF hours, and define how active-window metadata must be normalized before it can drive readiness.
2. Prioritize the 15,923 fixed-coverage blockers by best available coverage, distance, NERC region, and plant criticality.
3. Resolve the 28 no-candidate plants by fixing missing plant coordinates or excluding placeholder/unsited plant records from the publication universe.
4. Decide how to publish the 144 first-operable current publication candidates: as preview candidates, not final compliance output, until station-selection review is complete.

The first-operable scoped publication-candidate export is
`plant_ecwt_publication_candidates_first_operable_20260625T045722Z.csv`,
with report `plant_ecwt_publication_candidates_first_operable_20260625T045722Z_report.md`.
It filters the 162 all-plant readiness candidates to plants with at least one
`OP`, `SB`, `OA`, or `OS` generator status, matching the documented first ECWT
plant-scope rule.

The first-operable scope itself is summarized in
`first_operable_scope_diagnostic_20260625T045945Z.md`. The current database has
13,370 first-scope plant rows covered by readiness, plus one open upstream EIA
exception for generator plant code `68815`, which appears in the generator table
but not the plant table.

The 28 no-candidate plants are itemized in `no_candidate_plants_20260625T044535Z.csv`
and summarized in `no_candidate_plants_20260625T044535Z_report.md`. All 28 lack
plant coordinates and have only `CN` generator status.

The fixed-coverage blockers are summarized in
`fixed_coverage_threshold_diagnostic_20260625T044535Z.md`. No blocked plant has
best-candidate fixed-period coverage above 94%, so small coverage-threshold
relaxations do not materially change readiness.

The first-operable denominator diagnostic is
`fixed_period_denominator_diagnostic_first-operable_20260625T052146Z_report.md`,
with detail rows in
`fixed_period_denominator_diagnostic_first-operable_20260625T052146Z.csv`. It
shows that all 13,226 first-operable blockers are fixed-period coverage
blockers under the current full-period gate: 13,219 fail only the fixed-period
coverage threshold and 7 fail both fixed-period coverage and the loaded-year
threshold.

The same diagnostic shows that station-active-window denominators would make
10,968 of those first-operable blockers pass an active-window coverage plus
active-loaded-year-ratio screen. That is not yet a recommendation to switch the
gate: 2,794 best active-window candidates have more valid loaded DJF hours than
their station metadata active window expects, including 36 with active-window
coverage ratios above 1.05 and a maximum ratio of 8.0. Those overfilled rows
show that station active-window metadata needs a normalization rule before it
can safely become the publication denominator.

The normalized first-operable denominator diagnostic is
`fixed_period_denominator_diagnostic_first-operable_20260625T053208Z_report.md`,
with detail rows in
`fixed_period_denominator_diagnostic_first-operable_20260625T053208Z.csv`. It
adds a conservative loaded-year normalization rule: each station active window
is expanded to the union of NOAA station metadata bounds and full loaded
station-years from `weather.station_year_djf_coverage`. This removes the
active-window overfill problem in the best-candidate rows: normalized
active-window overfill count is 0, no best normalized active-window ratio
exceeds 1.00, and the maximum best normalized active-window ratio is 0.994.

Under that conservative normalization, 5,992 of the 13,226 first-operable
blockers would pass normalized active-window coverage plus normalized
active-loaded-year-ratio. The remaining 7,234 still fail normalized
active-window coverage. This gives a defensible intermediate policy option
between the current full fixed-period gate, which yields 144 first-operable
publication candidates, and the raw metadata active-window gate, which is too
permissive because some station metadata windows understate loaded observations.

The first-operable readiness policy scenarios are summarized in
`readiness_policy_scenarios_first_operable_20260625T053723Z_report.md`, with
the matrix in `readiness_policy_scenarios_first_operable_20260625T053723Z_matrix.csv`
and scenario candidate rows in
`readiness_policy_scenarios_first_operable_20260625T053723Z_candidates.csv`.
The scenario matrix keeps the current Postgres readiness gate unchanged while
quantifying policy alternatives:

- current fixed-period gate: 144 candidates, 13,226 blocked
- raw station-metadata active-window gate: 11,112 candidates, but 2,794 promoted
  rows have overfilled denominators, so this remains diagnostic-only
- normalized active-window loaded-year gate: 6,136 candidates, 7,234 blocked,
  and 0 promoted overfill rows
- normalized active-window plus current absolute 20 loaded station-year rule:
  577 candidates and 12,793 blocked

Those scenario artifacts are now loaded into Postgres under
`calc.readiness_policy_scenario` and
`calc.readiness_policy_scenario_candidate` by calculation run
`readiness_policy_scenarios_db_load_20260625T054908Z`. The load report is
`readiness_policy_scenarios_db_load_20260625T054908Z_report.md`; it records 5
scenario rows, 20,039 scenario-candidate rows, and 2 hashed `audit.source_file`
registrations.

The station-selection review/release-readiness layer has been refreshed against
the current fixed-period readiness run in
`station_selection_review_seed_20260625T055346Z_report.md`, with review rows in
`station_selection_review_seed_20260625T055346Z.csv`. The refreshed gate is
intentionally conservative: all 162 current fixed-period publication candidates
remain `needs_review`, so `publish.plant_ecwt_release_readiness` has 0
`release_ready` rows for that run and 15,970 upstream readiness-blocked rows.
The blocker split is 110 cross-border-station policy decisions, 24
near-threshold-coverage reviews, 20 high-distance reviews, and 8 high-rank
candidate reviews.

The current station-selection policy decision surface is summarized in
`station_selection_policy_scenarios_20260625T055356Z_report.md`, with scenario
summary rows in `station_selection_policy_scenarios_20260625T055356Z.csv` and a
row-level matrix in `station_selection_policy_scenarios_20260625T055356Z_matrix.csv`.
This report is read-only and applies no policy override. It shows that the
current gate accepts 0 rows, `us_ca_practical` would accept 108 rows, and
`us_ca_distance_cap_150` or `fixed_coverage_only` would accept all 162 current
fixed-period candidates if the methodology explicitly allowed those policies.

The remaining 7,234 first-operable plants that still fail the conservative
normalized active-window coverage screen are now prioritized in
`normalized_active_window_blocker_priority_20260625T060119Z_report.md`, with
detail rows in `normalized_active_window_blocker_priority_20260625T060119Z_plants.csv`,
station summaries in `normalized_active_window_blocker_priority_20260625T060119Z_stations.csv`,
and state summaries in `normalized_active_window_blocker_priority_20260625T060119Z_states.csv`.
The same rows are queryable in Postgres under `calc.coverage_blocker_priority`,
`calc.coverage_blocker_station_summary`, and `calc.coverage_blocker_state_summary`.
The priority gap buckets show 156 plants within 24 valid DJF hours of the 0.95
normalized active-window threshold, 848 more within 168 hours, 1,351 within 720
hours, 3,047 within 2,160 hours, and 1,832 above 2,160 hours. This is a triage
queue for coverage/methodology remediation; it does not change readiness or
release status.

The near-threshold subset is now audited at station-year grain in
`near_threshold_station_year_gap_audit_20260625T060905Z_report.md`, with
station-year rows in `near_threshold_station_year_gap_audit_20260625T060905Z_station_years.csv`
and station summaries in `near_threshold_station_year_gap_audit_20260625T060905Z_stations.csv`.
The same data is queryable in Postgres under
`calc.coverage_blocker_station_year_gap` and
`calc.coverage_blocker_station_gap_summary`. Scope is the 1,004 plant blockers
within 168 valid DJF hours of the normalized active-window threshold. The audit
found 279 station-year gaps across 49 stations. All 279 station-year gaps have
available local raw NOAA files, 0 raw-missing years, and 0 latest AWS 404 years;
247 have an explicit `downloaded` attempt and 32 are present from an existing
local raw root without a corresponding downloader attempt row. This is therefore
not a bulk-download queue. The next remediation question is whether the missing
valid hours are true source-observation gaps, parser/QA rejections, or a
methodology threshold decision.

That remediation question is now answered for the near-threshold subset in
`near_threshold_raw_canonical_gap_audit_20260625T062134Z_report.md`, with
station-year detail in `near_threshold_raw_canonical_gap_audit_20260625T062134Z_station_years.csv`
and station summaries in `near_threshold_raw_canonical_gap_audit_20260625T062134Z_stations.csv`.
The same data is loaded in Postgres under
`calc.coverage_blocker_raw_canonical_gap_summary` and
`calc.coverage_blocker_raw_canonical_station_summary`. The audit re-read the
279 local raw station-year files and compared selected normalized expected-window
hours with `weather.hourly_djf` using the current loader rules
(`SOURCE=7` rejected, `TMP` quality `9` or sentinel values invalid, plausible
temperature range `-65 C` to `40 C`). It found 50,563 missing expected-window
hours, only 34 above the prior count-based gap table. Of those hours, 34,254 are
true raw source-hour absences and 16,309 have raw rows but invalid/missing NOAA
`TMP`. There are 0 hours where a raw row would pass the current loader rules but
is absent from `weather.hourly_djf`, 0 source-code rejection blockers, and 0
plausibility rejection blockers. For this near-threshold set, the issue is NOAA
source sparsity/invalid temperature observations, not corrupted downloads,
missing AWS bulk objects, or canonical-loader loss.

## Guardrail Added

`scripts/inventory_noaa_raw_files.py` now auto-includes existing NOAA raw roots referenced by `weather.noaa_hourly_load_file`, unless `--no-include-loaded-roots` is supplied. This prevents an incremental rebuild from omitting a cache root and creating duplicate AWS download work.
