# NOAA Backfill, Load, and Fixed-Period ECWT Status

Generated UTC: 2026-06-25T01:32Z

## Summary

The NOAA public AWS backfill manifest is fully resolved. There are no remaining `planned` manifest rows. Every distinct downloaded or skipped-existing backfill file has a matching `weather.noaa_hourly_load_file` loaded row, and the repo-local downloaded-file loader probe selected zero remaining files.

The fixed-period plant ECWT path is now implemented and has produced a stricter readiness cohort: `162` fixed-period publication candidates and `15,970` blocked plants. The old active-window strict cohort had `1,964` candidates, but the fixed-period diagnostic showed only `8` of those old selected-station assignments passed a full `2000-2025` DJF coverage gate. The new fixed-period selection reruns station choice before readiness and yields `162` candidates that all pass the fixed gate.

## NOAA Backfill Manifest

Manifest run: `noaa_backfill_manifest_20260623T215215Z`

| Manifest Status | Rows |
| --- | ---: |
| `downloaded` | 34,757 |
| `missing` | 44,347 |
| `skipped` | 7,735 |

`missing` means NOAA public AWS returned terminal missing-object results for the station-year object. `skipped` here is the active-window prune class, where station metadata did not support a DJF overlap for that source year.

## Download Attempts and Load Reconciliation

| Check | Value |
| --- | ---: |
| Distinct downloaded/skipped-existing files | 34,757 |
| Distinct downloaded files with loaded-file match | 34,757 |
| Downloaded files not loaded | 0 |
| Loaded NOAA file audit rows | 62,318 |
| Loaded hours from file audit | 50,346,347 |
| Plausibility rejects from file audit | 888 |

Download-attempt audit rows still include historical failed attempts (`failed_http` and `failed_exception`) from before retry/reclassification. They do not represent unresolved manifest rows; the manifest statuses above are the current terminal statuses.

## Loader No-Op Probe

Run: `noaa_hourly_djf_load_20260625T013212Z`

| Metric | Count |
| --- | ---: |
| Candidate files selected | 0 |
| Loaded files | 0 |
| Failed files | 0 |
| Canonical hourly rows staged | 0 |

Report: `docs/noaa_hourly_djf_load_20260625T013212Z_report.md`

## Fixed-Period ECWT Outputs

Plant ECWT run: `plant_ecwt_provisional_fixed_period_20260625T012402Z`

Readiness run: `plant_ecwt_readiness_fixed_period_20260625T012416Z`

Fixed-period candidate export: `plant_ecwt_publication_candidates_20260625T012457Z`

| Output | Rows |
| --- | ---: |
| Plant ECWT rows | 16,132 |
| Fixed-period provisional plant rows | 162 |
| Fixed-period blocked plant rows | 15,970 |
| Fixed-period readiness publication candidates | 162 |
| Fixed-period readiness blocked rows | 15,970 |
| Exported fixed-period preview rows | 162 |

The fixed-period gate uses `2000-2025` DJF hours, minimum coverage ratio `0.95`, and minimum loaded station-years `20`. The fixed-period coverage diagnostic for the selected cohort (`fixed_period_station_coverage_20260625T012645Z`) confirms all `162` selected rows pass.

## Remaining Work

The remaining blocker is no longer unprocessed downloaded NOAA data. The next bottleneck is station-selection quality and weather coverage availability:

- `15,970` plants have no candidate station that currently passes the fixed-period coverage eligibility gate.
- All `162` fixed-period publication candidates still carry at least one station-selection QA review flag.
- The largest review classes are cross-border station selection, high candidate rank, high plant-station distance, shared station concentration, and near-threshold coverage.

The next engineering step should be a release-review/disposition table for station-selection QA, followed by a policy decision on whether Canadian stations and long-distance/high-rank fallback stations are allowed for publication.
