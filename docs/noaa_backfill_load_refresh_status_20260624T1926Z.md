# NOAA Backfill, Active-Window Prune, Load, And ECWT Refresh Status

Generated UTC: 2026-06-24T19:26Z

## Scope

This checkpoint covers the response to the `999999-12989` station-year issue, active-window pruning of the NOAA backfill manifest, NOAA public AWS backfill batches 75 through 81, the subsequent DJF hourly load, and refreshed station/plant ECWT readiness outputs.

## Current State

| Metric | Value |
| --- | ---: |
| Total manifest batches | 87 |
| Processed/classified batches | 81 |
| Remaining planned batch range | 82-87 |
| Remaining planned manifest rows | 1,756 |
| Raw NOAA CSV files in cache | 33,365 |
| Partial `.part` files in cache | 0 |
| NOAA raw cache size | 239 GB |
| Postgres database size | 20 GB |
| Loaded canonical DJF hours | 48,681,345 |

## Manifest Status

| Status | Rows |
| --- | ---: |
| `downloaded` | 33,365 |
| `missing` | 43,973 |
| `failed` | 10 |
| `planned` | 1,756 |
| `skipped` | 94,574 |

Remaining planned rows by batch:

| Batch | Planned Rows |
| ---: | ---: |
| 82 | 538 |
| 83 | 284 |
| 84 | 424 |
| 85 | 316 |
| 86 | 87 |
| 87 | 107 |

## Active-Window Prune

Run: `noaa_manifest_active_window_prune_20260624T183548Z`

| Metric | Count |
| --- | ---: |
| Planned rows before prune | 10,839 |
| Rows skipped by no station active DJF overlap | 7,735 |
| Distinct stations affected | 2,332 |
| Planned `999999-*` rows before prune | 1,030 |
| `999999-*` rows skipped by active window | 648 |
| Candidate plant links represented by skipped rows | 257,943 |

The manifest builder was also hardened so future backfill manifests exclude station-years where station metadata proves there is no January-February or December observation overlap for that source year. Rows with unknown station first/last observation dates remain eligible rather than being dropped.

`999999-*` station IDs are not globally invalid. NOAA Global Hourly includes valid WBAN-only station files with the `999999` USAF placeholder; this local cache already contains 2,121 downloaded `999999*.csv` files. The specific `999999-12989` row was different: it is Cameron Heliport, Louisiana, with station metadata spanning 2005-05-31 through 2005-09-11, no current plant ECWT selection, and zero coverage on its candidate links. Its 2016 object first returned a retryable 503, then returned a terminal 404 on retry and was classified as `missing_on_aws`.

## Batch Results

| Batch / Run | Attempted | Downloaded | Missing On AWS | True Failures | Downloaded Bytes |
| --- | ---: | ---: | ---: | ---: | ---: |
| 75 initial | 1,000 | 216 | 783 | 1 | 2,198,862,366 |
| 75 retry | 1 | 0 | 1 | 0 | 0 |
| 76 | 1,000 | 255 | 745 | 0 | 2,176,863,854 |
| 77 | 27 | 0 | 27 | 0 | 0 |
| 78 | 182 | 144 | 38 | 0 | 1,184,672,435 |
| 79 | 369 | 326 | 43 | 0 | 3,012,564,279 |
| 80 | 466 | 428 | 38 | 0 | 3,049,924,130 |
| 81 | 304 | 273 | 31 | 0 | 2,749,102,968 |
| **Total after retry** | **3,349** | **1,642** | **1,706** | **0** | **14,371,990,032** |

The one true failure in the initial batch 75 run was HTTP 503 for `999999-12989` year 2016. It was requeued and retried immediately; the retry returned HTTP 404 and is now terminal `missing_on_aws`, not retryable failure.

## DJF Hourly Load

Run: `noaa_hourly_djf_load_20260624T185113Z`

| Metric | Count |
| --- | ---: |
| Candidate files selected | 1,642 |
| Loaded files | 1,642 |
| Failed files | 0 |
| Source bytes parsed | 14,371,990,032 |
| Raw rows seen | 34,435,637 |
| DJF rows seen | 8,980,334 |
| Rejected source-code rows | 2,860,675 |
| Valid DJF temperature rows | 5,870,022 |
| Invalid DJF temperature rows | 249,632 |
| Rejected plausibility rows | 5 |
| Duplicate station-hour observations | 4,196,114 |
| Canonical hourly rows staged | 1,673,908 |

## Coverage Refresh

Run: `station_year_djf_coverage_20260624T185925Z`

| Metric | Count |
| --- | ---: |
| Coverage rows | 60,926 |
| Complete station-years | 13,593 |
| Partial station-years | 45,049 |
| Empty station-years | 2,284 |
| Valid DJF hours represented | 48,681,345 |
| Rejected source rows represented | 136,271,677 |

## ECWT Refresh

Station run: `station_ecwt_loaded_20260624T191537Z`

| Metric | Value |
| --- | ---: |
| Station ECWT rows | 4,244 |
| Provisional station rows | 4,051 |
| Blocked station rows | 193 |
| Minimum station ECWT F | -58.216 |
| Maximum station ECWT F | 100.400 |

Plant run: `plant_ecwt_provisional_20260624T192247Z`

| Metric | Value |
| --- | ---: |
| Plant ECWT rows | 16,132 |
| Provisional plant ECWT rows | 16,104 |
| Blocked plant ECWT rows | 28 |
| Minimum plant ECWT F | -58.000 |
| Maximum plant ECWT F | 88.160 |

Strict readiness run: `plant_ecwt_readiness_20260624T192409Z`

| Metric | Count |
| --- | ---: |
| Publication candidates | 1,666 |
| Provisional low coverage | 14,438 |
| Blocked | 28 |
| Median coverage ratio | 0.2503 |

Diagnostic readiness run: `plant_ecwt_readiness_20260624T192459Z`

| Metric | Count |
| --- | ---: |
| Publication candidates at 0.25 coverage threshold | 7,837 |
| Provisional low coverage | 8,267 |
| Blocked | 28 |
| Median coverage ratio | 0.2503 |

## Movement Since Previous Checkpoint

Previous checkpoint: `docs/noaa_backfill_load_refresh_status_20260624T1820Z.md`

| Metric | Previous | Current | Delta |
| --- | ---: | ---: | ---: |
| Raw NOAA CSV files | 31,723 | 33,365 | +1,642 |
| Manifest `downloaded` rows | 31,723 | 33,365 | +1,642 |
| Manifest `missing` rows | 42,267 | 43,973 | +1,706 |
| Manifest `planned` rows | 12,839 | 1,756 | -11,083 |
| Manifest `skipped` rows | 86,839 | 94,574 | +7,735 |
| Loaded canonical DJF hours | 47,007,437 | 48,681,345 | +1,673,908 |
| Complete station-years | 13,119 | 13,593 | +474 |
| Provisional station ECWT rows | 4,043 | 4,051 | +8 |
| Strict publication candidates | 1,673 | 1,666 | -7 |
| Diagnostic publication candidates | 7,756 | 7,837 | +81 |

## QA Notes

- The high `missing_on_aws` count remains mostly terminal NOAA AWS 404s, not corrupted local files.
- The active-window prune removed 7,735 planned rows before spending AWS requests on station-years that cannot contain DJF observations.
- The loader rejected 5 rows as physically implausible under the configured `-65 C` to `40 C` plausibility window. These should be sampled before publication QA is closed.
- The `100.400 F` maximum station ECWT remains a QA flag to investigate before any compliance publication.
- Strict publication candidates fell by 7 even though loaded weather increased. That reflects current station-selection/readiness gate behavior and should be investigated before treating strict readiness as monotonic.
- Current plant ECWT rows remain provisional. Strict publication candidates are still limited by station coverage and QA gates.

## Reports Produced

- `docs/noaa_backfill_download_batch75_report.md`
- `docs/noaa_backfill_download_batch75_20260624T182643Z_report.md`
- `docs/noaa_backfill_download_batch76_report.md`
- `docs/noaa_backfill_download_batch77_report.md`
- `docs/noaa_backfill_download_batch78_report.md`
- `docs/noaa_backfill_download_batch79_report.md`
- `docs/noaa_backfill_download_batch80_report.md`
- `docs/noaa_backfill_download_batch81_report.md`
- `docs/noaa_manifest_active_window_prune_20260624T183457Z_report.md`
- `docs/noaa_manifest_active_window_prune_20260624T183548Z_report.md`
- `docs/noaa_hourly_djf_load_20260624T185113Z_report.md`
- `docs/station_year_djf_coverage_20260624T185925Z_report.md`
- `docs/station_ecwt_loaded_20260624T191537Z_report.md`
- `docs/plant_ecwt_provisional_20260624T192247Z_report.md`
- `docs/plant_ecwt_readiness_20260624T192409Z_report.md`
- `docs/plant_ecwt_readiness_20260624T192459Z_report.md`

## Next Step

Continue NOAA public AWS backfill at batch 82. The remaining planned queue is now only 1,756 rows after active-window pruning.
