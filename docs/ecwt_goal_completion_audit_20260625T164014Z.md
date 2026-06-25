# ECWT Rebuild Goal Completion Audit

Generated UTC: 2026-06-25T16:40:14Z

## Scope Audited

This audit checks the active rebuild goal against the current database and repository state:

- Harden NOAA DJF weather loading.
- Continue missing NOAA public AWS backfill.
- Load available weather data in auditable batches.
- Progress to ECWT-ready coverage and plant result tables.

The user-approved publication scope excludes Alaska and the reviewed no-station edge cases. The current release is a plant-level analytical dataset, not a final Generator Owner unit-level compliance filing.

## Current Release

- Release ID: `scoped_plant_ecwt_release_20260625T161629Z`
- Release tag originally created for the scoped release: `scoped-plant-ecwt-20260625T161629Z`
- Current refreshed manifest run ID: `release_manifest_20260625T163910Z`
- Current manifest JSON SHA-256: `4f2e5eb95b5f2ab3a25bbd0cd2fd7fdc8a6002f7fc70a6b0255b93d092420656`
- Current manifest generation commit: `ba953a9ff420c8ebfeb242c130104fd92a8cd8ef`

## Requirement Evidence

| Requirement | Evidence | Status |
| --- | --- | --- |
| NOAA raw-file inventory refreshed | `noaa_raw_file_inventory_20260625T153854Z` found 73,979 available and 59,973 missing station-years. | Complete for configured NOAA roots |
| Missing NOAA public AWS backfill continued | `noaa_backfill_manifest_20260625T154422Z`; planned rows after active-window and terminal-404 filters: 0. | Complete for current filters |
| Available local weather files loaded | 1,356 previously available-unloaded station-years loaded; file failures: 0. | Complete |
| Available inventory rows without load evidence | Live DB check returned `available_unloaded_station_years = 0`. | Complete |
| Station-year coverage refreshed | `station_year_djf_coverage_20260625T155613Z`; 73,979 station-year rows, 19,528 complete. | Complete |
| Station ECWT refreshed | `station_ecwt_loaded_20260625T155645Z`; 4,936 station ECWT rows. | Complete |
| Plant policy result materialized | `plant_ecwt_policy_result_all_plants_normalized_active_window_loaded_year_20260625T161313Z`; 16,132 policy rows. | Complete |
| Secondary-station fill applied where needed | `secondary_station_fill_ecwt_20260625T161345Z`; 4 Texas plants pass composite fill. | Complete |
| Scoped publication denominator reconciles | Live DB check returned `unresolved_scoped_denominator_plants = 0`. | Complete |
| Published release files are auditable | Release CSV has 15,947 rows; exclusions CSV has 185 rows; both have SHA-256 checksums in `publish.release_artifact`. | Complete |
| Release manifest exists in Git and DB | `audit.release_manifest` has release `scoped_plant_ecwt_release_20260625T161629Z`; `publish.release_artifact` has 23 artifact rows. | Complete |

## Publication Reconciliation

| Item | Count |
| --- | ---: |
| Policy-result plant rows | 16,132 |
| Scoped release rows | 15,947 |
| Alaska exclusions | 157 |
| No-station edge-case exclusions | 28 |
| Scoped release plus exclusions | 16,132 |
| Remaining unresolved plants inside current scoped denominator | 0 |

The four non-Alaska low-coverage policy blockers are the Texas rows resolved by the documented secondary-station fill method.

## Current Limitations

These are not blockers for the current scoped release, but they remain future work:

- Alaska is excluded by user decision and should be handled as a separate scope if needed.
- The 28 no-station rows are excluded edge cases; SPI - Everett can be geocoded but has no first-operable generator under the current scope.
- This is plant-level analytical output. Unit-level EOP-012 applicability and Generator Owner station-representativeness review remain downstream compliance work.
- Heavy NOAA raw data and the Postgres working cluster remain external to Git by design.

## Conclusion

The active rebuild goal is complete for the current user-approved scoped plant release. The NOAA public AWS backfill has no remaining planned rows under the configured filters, all available inventory rows have load evidence, coverage and ECWT tables have been refreshed, and the scoped publication denominator has zero unresolved plants.
