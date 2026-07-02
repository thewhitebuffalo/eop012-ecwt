# Pipeline map — which script does what

The `scripts/` directory holds both the **release spine** (the scripts a run
actually flows through) and a larger set of **diagnostics and one-off audits**
that were built to investigate specific questions along the way. This page maps
every script to its stage so a reader can tell pipeline from archaeology.

> Maintainer note: classifications below were derived from the scripts
> themselves (docstrings, arguments, and the audit schema). If a run log shows a
> different order or an additional required step, correct this page in the same
> PR that changes the step.

## The release spine

```
EIA-860 universe          NOAA stations & raw data
      |                          |
      v                          v
[1] load plants           [2] station catalog + coverage
      \                          /
       \                        /
        v                      v
   [3] DJF hourly load (per-hour provenance)
                 |
                 v
   [4] station selection (nearest-first candidates)
                 |
                 v
   [5] plant ECWT rebuild  — composite fill + 0.2-percentile + tiers
                 |
                 v
   [6] scoped export  — release CSV(s) with provenance columns
                 |
                 v
   [7] manifest + validation  — SHA-256 manifest, ADR-0005 acceptance checks
                 |
                 v
   [8] publish  — tagged GitHub Release (data) + dashboard rebuild (viz)
```

| Stage | Script | Role |
| --- | --- | --- |
| shared | `eop012_config.py` | Environment-backed path defaults for every CLI script |
| shared | `ecwt_core.py` | Pure, tested helpers: `PERCENTILE.INC`-equivalent percentile, expected DJF hours, ADR-0005 adequacy gates |
| 1 | `build_eia860_asset_inventory.py` | Extract + audit the EIA-860 plant/generator universe |
| 1 | `load_eia860_assets_to_postgres.py` | Load the universe into Postgres |
| 2 | `load_noaa_station_candidates.py` | Station catalog + plant–station distance candidates |
| 2 | `load_noaa_weather_coverage_audit.py` | Station coverage audit tables |
| 2 | `build_station_year_djf_coverage.py` | Station-year DJF coverage rollups |
| 3 | `inventory_noaa_raw_files.py` | Inventory local NOAA raw caches |
| 3 | `build_noaa_backfill_manifest.py` | Decide which station-years still need downloading |
| 3 | `download_noaa_backfill_batch.py` | Fetch a backfill batch from NOAA |
| 3 | `load_noaa_hourly_djf.py` | Load DJF hourly observations with source lineage |
| 4 | `build_station_selection_review.py` / `apply_station_selection_review_updates.py` | Station-selection review and applied corrections |
| 5 | `rebuild_adr0004_ecwt_layer.py` | **The calculation**: nearest-first composite fill of all winter hours, per-hour provenance, 0.2-percentile ECWT, confidence tiers (ADR-0004/0005) |
| 6 | `export_scoped_plant_ecwt_dataset.py` | Export the wide scoped release CSV (ECWT + provenance per plant) |
| 7 | `build_scoped_release_manifest.py` | Auditable release manifest (run ids, checksums) |
| 7 | `validate_ecwt_release.py` | One-pass PASS/WARN/FAIL acceptance checks ([usage](validating_ecwt_release.md)) |
| 8 | `build_ecwt_dashboard.py` | Self-contained dashboard from the scoped CSV ([details](visualization.md)) |
| 8 | (release) | Tag + attach outputs as GitHub Release assets ([convention](releasing.md)) |

## Supporting / situational

Used when their situation arises, not on every run:

`backfill_station_year_hourly_summary.py`,
`prune_noaa_manifest_active_window.py`, `reclassify_noaa_404_missing.py`,
`normalize_noaa_source_lineage.py`, `refresh_noaa_load_file_policy_stats.py`,
`build_station_ecwt_from_loaded.py`, `build_secondary_station_fill_ecwt.py`,
`build_provisional_plant_ecwt.py`, `materialize_policy_ecwt_results.py`,
`build_plant_ecwt_readiness.py`, `build_readiness_policy_scenarios.py`,
`load_readiness_policy_scenarios_to_db.py`,
`export_plant_ecwt_release_ready.py`,
`export_plant_ecwt_publication_candidates.py`.

## Diagnostics and one-off audits

Report builders created to answer specific data-quality questions; they read
the database and write reports, and are not required to produce a release:

`audit_near_threshold_raw_canonical_gaps.py`,
`build_expanded_candidate_coverage_scenario.py`,
`build_fixed_period_denominator_diagnostic.py`,
`build_fixed_period_gap_cause_report.py`,
`build_fixed_period_readiness_blocker_report.py`,
`build_fixed_period_station_coverage_report.py`,
`build_near_threshold_station_year_gap_audit.py`,
`build_noaa_weather_qa_report.py`,
`build_normalized_coverage_blocker_priority.py`,
`build_policy_exception_review.py`, `build_scope_readiness_audit.py`,
`build_station_selection_policy_review_worksheet.py`,
`build_station_selection_policy_scenarios.py`,
`build_station_selection_qa_report.py`.

Several of these produced the findings written up in
[`docs/findings/`](findings/) and [`docs/whitepaper/`](whitepaper/).

## Conventions

- All scripts are Python standard library only and talk to Postgres through
  `psql` (path from `EOP012_PSQL`); defaults come from `scripts/eop012_config.py`
  and can be overridden per-flag.
- Methodology changes (anything that alters a published number) require an ADR
  in [`docs/adr/`](adr/) before the code change.
