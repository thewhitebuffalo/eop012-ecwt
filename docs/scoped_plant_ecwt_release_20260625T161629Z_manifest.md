# Scoped Plant ECWT Release Manifest

- Release ID: `scoped_plant_ecwt_release_20260625T161629Z`
- Release name: `Scoped plant ECWT release 20260625T161629Z`
- Manifest run ID: `release_manifest_20260625T163910Z`
- Generated UTC: 2026-06-25T16:39:10Z
- Git generation commit: `ba953a9ff420c8ebfeb242c130104fd92a8cd8ef`
- Manifest JSON: `docs/scoped_plant_ecwt_release_20260625T161629Z_manifest.json`
- Manifest JSON SHA-256: `4f2e5eb95b5f2ab3a25bbd0cd2fd7fdc8a6002f7fc70a6b0255b93d092420656`

## Scope

This release publishes non-Alaska plant-level ECWT rows that passed the normalized active-window loaded-year policy or the documented secondary-station fill policy. Alaska rows and reviewed no-station edge cases are excluded from the current scoped denominator and published in the exclusions CSV.

## Run Chain

| Role | Calculation Run ID | Status | Code Commit |
| --- | --- | --- | --- |
| raw inventory | `noaa_raw_file_inventory_20260625T153854Z` | succeeded | `bd3c33c8073c2a66057773e07ae474d2b8eb9be4` |
| backfill manifest | `noaa_backfill_manifest_20260625T154422Z` | succeeded | `bd3c33c8073c2a66057773e07ae474d2b8eb9be4` |
| NOAA DJF load start | `noaa_hourly_djf_load_20260625T154554Z` | succeeded | `bd3c33c8073c2a66057773e07ae474d2b8eb9be4` |
| NOAA DJF load end | `noaa_hourly_djf_load_20260625T155515Z` | succeeded | `bd3c33c8073c2a66057773e07ae474d2b8eb9be4` |
| station-year DJF coverage | `station_year_djf_coverage_20260625T155613Z` | succeeded | `bd3c33c8073c2a66057773e07ae474d2b8eb9be4` |
| station ECWT | `station_ecwt_loaded_20260625T155645Z` | succeeded | `bd3c33c8073c2a66057773e07ae474d2b8eb9be4` |
| fixed-period plant ECWT | `plant_ecwt_provisional_fixed_period_20260625T161041Z` | succeeded | `bd3c33c8073c2a66057773e07ae474d2b8eb9be4` |
| fixed-period readiness | `plant_ecwt_readiness_fixed_period_20260625T161109Z` | succeeded | `bd3c33c8073c2a66057773e07ae474d2b8eb9be4` |
| denominator diagnostic | `fixed_period_denominator_diagnostic_all-plants_20260625T161153Z` | succeeded | `bd3c33c8073c2a66057773e07ae474d2b8eb9be4` |
| policy scenario DB load | `readiness_policy_scenarios_db_load_20260625T161252Z` | succeeded | `bd3c33c8073c2a66057773e07ae474d2b8eb9be4` |
| policy result | `plant_ecwt_policy_result_all_plants_normalized_active_window_loaded_year_20260625T161313Z` | succeeded | `bd3c33c8073c2a66057773e07ae474d2b8eb9be4-dirty` |
| secondary station fill | `secondary_station_fill_ecwt_20260625T161345Z` | succeeded | `bd3c33c8073c2a66057773e07ae474d2b8eb9be4-dirty` |

## Artifact Checksums

| Artifact | Type | Rows | Size Bytes | SHA-256 | Path |
| --- | --- | ---: | ---: | --- | --- |
| release_dataset_csv | csv | 15947 | 9958040 | `3da1fc9ba7e56f6818e83c6a8c5670f46419c1a71b7f6d65de4d994e4bb5c557` | `data/processed/scoped_plant_ecwt_release_20260625T161629Z.csv` |
| release_exclusions_csv | csv | 185 | 77400 | `6c13421a8bbde9082773a62eab4469623b2aa43fdd93deeb999cff0629d59ce5` | `data/processed/scoped_plant_ecwt_release_20260625T161629Z_exclusions.csv` |
| release_report_md | markdown |  | 1528 | `e89fb034b86d97a8fdd5903c3057d57d2c133594a1722f4cc2d8a482bf77c7f5` | `docs/scoped_plant_ecwt_release_20260625T161629Z_report.md` |
| policy_result_csv | csv | 16132 | 12953889 | `78c17d959a0eb9221d5864ca55c9a813cd729ee2918a7854b13dd20cdce8f33d` | `docs/plant_ecwt_policy_result_all_plants_normalized_active_window_loaded_year_20260625T161313Z.csv` |
| policy_result_report_md | markdown |  | 5081 | `5277de9e29c19c3af8db1ba9406c5c288a127e63563109e0d5b4fc89ff0adcf0` | `docs/plant_ecwt_policy_result_all_plants_normalized_active_window_loaded_year_20260625T161313Z_report.md` |
| secondary_fill_plants_csv | csv | 4 | 4277 | `8cb1d496127ca1f367283e526da32d49508fca669293039e974393db6e9faba5` | `docs/secondary_station_fill_ecwt_20260625T161345Z_plants.csv` |
| secondary_fill_candidate_scores_csv | csv | 396 | 246335 | `983b96a76e957b1fc64ed3f9cdeda87def664e73a816bfa12d859744c6bb09ed` | `docs/secondary_station_fill_ecwt_20260625T161345Z_candidate_scores.csv` |
| secondary_fill_report_md | markdown |  | 2414 | `8ade2a1ff71cb95e7d4a58f2b36299e60b6e072a06ace9cacf0c720f305db599` | `docs/secondary_station_fill_ecwt_20260625T161345Z_report.md` |
| station_ecwt_report_md | markdown |  | 2301 | `57fc288543b47e09c32e6433939b3984454263d783542aeb0cca018371d6f9f7` | `docs/station_ecwt_loaded_20260625T155645Z_report.md` |
| station_year_coverage_report_md | markdown |  | 2493 | `4e1a16b67ff648f5ed0cb7e9820d3e79e9e301e09b7df340f043ac646e0e9138` | `docs/station_year_djf_coverage_20260625T155613Z_report.md` |
| plant_ecwt_report_md | markdown |  | 3342 | `ed2a430bc6a2285443fe19160f4cef6b08ca4336bc2b6e5110648ca265f8ad7a` | `docs/plant_ecwt_provisional_fixed_period_20260625T161041Z_report.md` |
| plant_readiness_report_md | markdown |  | 1652 | `76d49900afb030abd03251cf5eafb3b1007183ddebaffc91753973f1d81947fa` | `docs/plant_ecwt_readiness_fixed_period_20260625T161109Z_report.md` |
| denominator_diagnostic_csv | csv | 14264 | 16715503 | `52bf66fa3468c3cbee8103d690705655e20c87568ba2c8138023c2f849650594` | `docs/fixed_period_denominator_diagnostic_all-plants_20260625T161153Z.csv` |
| denominator_diagnostic_report_md | markdown |  | 8175 | `ffd7740f3514e01bcbfe02a0a9bc5ba7f088bbe06a83845ef9ce246bc7f1c47e` | `docs/fixed_period_denominator_diagnostic_all-plants_20260625T161153Z_report.md` |
| policy_scenarios_db_load_report_md | markdown |  | 2051 | `9ca332ced01d2880539d2e26a0be7ec9497d29cb60ede9d0bf15b57a3f0cb8c8` | `docs/readiness_policy_scenarios_db_load_20260625T161252Z_report.md` |
| methodology_md | markdown |  | 12884 | `a77e9c5b82c94cb1e88aae3e7499a5ed89b3c3b70a4cb17829989159d088e625` | `docs/methodology.md` |
| readme_md | markdown |  | 2498 | `677fade462f77a6a39534c05b2658e5a843aac1d0b7750090c60b997452b7c83` | `README.md` |
| audit_schema_sql | sql |  | 22913 | `7dbfebefc31465befd9e6baa4f8d0b3288b4db26ac32f267f2e10ffb103ed928` | `sql/audit_schema.sql` |
| data_dictionary_md | markdown |  | 28072 | `6d9590b1f7f891f525a5ae9fab3865c3695b7777fbcae198e2e3af21690b5c09` | `docs/data_dictionary.md` |
| scoped_export_script_py | python |  | 16984 | `b1775734450c92a8ca906a4ffcedd11b2e27dc5a2977945e3a985ddbf1cf456a` | `scripts/export_scoped_plant_ecwt_dataset.py` |
| manifest_builder_script_py | python |  | 30634 | `87144e5b26798669c031e43cae8f5b01d86807f24ab34609685eafec8cddfc75` | `scripts/build_scoped_release_manifest.py` |
| release_manifest_json | json |  | 16162 | `4f2e5eb95b5f2ab3a25bbd0cd2fd7fdc8a6002f7fc70a6b0255b93d092420656` | `docs/scoped_plant_ecwt_release_20260625T161629Z_manifest.json` |

## Database Evidence

### Raw Inventory

| file_status | station_years |
| --- | --- |
| available | 73979 |
| missing | 59973 |

### Backfill Manifest

_No rows returned._

### Noaa Djf Loads

| file_status | files | loaded_hours | invalid_temp_rows | rejected_source_rows | duplicate_hours |
| --- | --- | --- | --- | --- | --- |
| loaded | 1356 | 2057523 | 107261 | 249852 | 811987 |

### Station Year Coverage

| coverage_status | station_years |
| --- | --- |
| complete | 19528 |
| empty | 2886 |
| partial | 51565 |

### Station Ecwt

| result_status | stations |
| --- | --- |
| blocked | 229 |
| provisional | 4707 |

### Policy Result

| readiness_status | reason_code | plants |
| --- | --- | --- |
| blocked | no_station_candidates | 28 |
| blocked | normalized_active_window_coverage_below_threshold | 14 |
| publication_candidate | passes_current_fixed_period_gate | 1868 |
| publication_candidate | passes_normalized_active_window_policy | 14222 |

### Secondary Fill

| fill_status | plants |
| --- | --- |
| passes_composite_fill | 4 |

## Notes

- This manifest records the current public analytical release, not a final Generator Owner compliance filing.
- Heavy NOAA raw data and the Postgres working cluster are external build inputs and are not committed to Git.
- The Git tag for the release should point to the commit containing this manifest and the release artifacts.
