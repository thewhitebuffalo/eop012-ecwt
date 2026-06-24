# NOAA Backfill Queue Drained And ECWT Refresh Status

Generated UTC: 2026-06-24T21:01Z

## Scope

This checkpoint covers NOAA public AWS backfill batches 82 through 87, retry of the remaining historical failed manifest rows, final DJF hourly loads, and the final refreshed coverage/station/plant ECWT readiness outputs for the fully classified current manifest.

## Current State

| Metric | Value |
| --- | ---: |
| Total manifest batches | 87 |
| Remaining planned manifest rows | 0 |
| Remaining failed manifest rows | 0 |
| Raw NOAA CSV files in cache | 34,757 |
| Partial `.part` files in cache | 0 |
| NOAA raw cache size | 251 GB |
| Postgres database size | 21 GB |
| Loaded canonical DJF hours | 50,346,347 |

## Manifest Status

| Status | Rows |
| --- | ---: |
| `downloaded` | 34,757 |
| `missing` | 44,347 |
| `skipped` | 94,574 |
| `planned` | 0 |
| `failed` | 0 |

`missing` means NOAA public AWS returned terminal 404 for the station-year object. `skipped` includes rows pruned from the backfill queue, including active-window-pruned rows that cannot contain DJF observations for the station-year.

## Batch 82-87 Results

| Batch | Attempted | Downloaded | Missing On AWS | True Failures | Downloaded Bytes |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 82 | 538 | 508 | 30 | 0 | 4,313,162,098 |
| 83 | 284 | 242 | 42 | 0 | 2,355,961,421 |
| 84 | 424 | 383 | 41 | 0 | 4,308,629,858 |
| 85 | 316 | 254 | 62 | 0 | 1,454,045,607 |
| 86 | 87 | 0 | 87 | 0 | 0 |
| 87 | 107 | 0 | 107 | 0 | 0 |
| **Total** | **1,756** | **1,387** | **369** | **0** | **12,431,798,984** |

## Historical Failure Retry

The 10 remaining historical retryable failures were requeued and retried after the main queue drained.

| Retry Batch | Attempted | Downloaded | Missing On AWS | True Failures | Downloaded Bytes |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 8 | 1 | 1 | 0 | 0 | 8,807,488 |
| 23 | 1 | 1 | 0 | 0 | 7,703,681 |
| 25 | 1 | 1 | 0 | 0 | 7,690,341 |
| 28 | 2 | 2 | 0 | 0 | 17,029,200 |
| 31 | 1 | 0 | 1 | 0 | 0 |
| 34 | 2 | 0 | 2 | 0 | 0 |
| 37 | 1 | 0 | 1 | 0 | 0 |
| 43 | 1 | 0 | 1 | 0 | 0 |
| **Total** | **10** | **5** | **5** | **0** | **41,230,710** |

Net result: all historical `failed` manifest rows were resolved. Five downloaded successfully and five resolved to terminal `missing_on_aws`.

## DJF Hourly Loads

Run: `noaa_hourly_djf_load_20260624T195519Z`

| Metric | Count |
| --- | ---: |
| Candidate files selected | 1,387 |
| Loaded files | 1,387 |
| Failed files | 0 |
| Source bytes parsed | 12,431,798,984 |
| Raw rows seen | 31,420,444 |
| DJF rows seen | 7,859,632 |
| Rejected source-code rows | 1,691,543 |
| Valid DJF temperature rows | 5,956,488 |
| Invalid DJF temperature rows | 211,425 |
| Rejected plausibility rows | 176 |
| Duplicate station-hour observations | 4,296,503 |
| Canonical hourly rows staged | 1,659,985 |

Run: `noaa_hourly_djf_load_20260624T203310Z`

| Metric | Count |
| --- | ---: |
| Candidate files selected | 5 |
| Loaded files | 5 |
| Failed files | 0 |
| Source bytes parsed | 41,230,710 |
| Raw rows seen | 80,599 |
| DJF rows seen | 21,360 |
| Rejected source-code rows | 13,448 |
| Valid DJF temperature rows | 7,464 |
| Invalid DJF temperature rows | 448 |
| Rejected plausibility rows | 0 |
| Duplicate station-hour observations | 2,447 |
| Canonical hourly rows staged | 5,017 |

Combined final-slice load result: 1,392 files loaded, zero failed files, and 1,665,002 canonical DJF hours staged.

## Final Coverage Refresh

Run: `station_year_djf_coverage_20260624T203330Z`

| Metric | Count |
| --- | ---: |
| Coverage rows | 62,318 |
| Complete station-years | 14,161 |
| Partial station-years | 45,804 |
| Empty station-years | 2,353 |
| Valid DJF hours represented | 50,346,347 |
| Rejected source rows represented | 137,976,668 |

## Final ECWT Refresh

Station run: `station_ecwt_loaded_20260624T205220Z`

| Metric | Value |
| --- | ---: |
| Station ECWT rows | 4,250 |
| Provisional station rows | 4,057 |
| Blocked station rows | 193 |
| Minimum station ECWT F | -58.216 |
| Maximum station ECWT F | 100.400 |

Plant run: `plant_ecwt_provisional_20260624T205856Z`

| Metric | Value |
| --- | ---: |
| Plant ECWT rows | 16,132 |
| Provisional plant ECWT rows | 16,104 |
| Blocked plant ECWT rows | 28 |
| Minimum plant ECWT F | -58.000 |
| Maximum plant ECWT F | 88.160 |

Strict readiness run: `plant_ecwt_readiness_20260624T210010Z`

| Metric | Count |
| --- | ---: |
| Publication candidates | 1,964 |
| Provisional low coverage | 14,140 |
| Blocked | 28 |
| Median coverage ratio | 0.2517 |

Diagnostic readiness run: `plant_ecwt_readiness_20260624T210028Z`

| Metric | Count |
| --- | ---: |
| Publication candidates at 0.25 coverage threshold | 7,910 |
| Provisional low coverage | 8,194 |
| Blocked | 28 |
| Median coverage ratio | 0.2517 |

## Movement Since Previous Checkpoint

Previous checkpoint: `docs/noaa_backfill_load_refresh_status_20260624T1926Z.md`

| Metric | Previous | Current | Delta |
| --- | ---: | ---: | ---: |
| Raw NOAA CSV files | 33,365 | 34,757 | +1,392 |
| Manifest `downloaded` rows | 33,365 | 34,757 | +1,392 |
| Manifest `missing` rows | 43,973 | 44,347 | +374 |
| Manifest `failed` rows | 10 | 0 | -10 |
| Manifest `planned` rows | 1,756 | 0 | -1,756 |
| Loaded canonical DJF hours | 48,681,345 | 50,346,347 | +1,665,002 |
| Complete station-years | 13,593 | 14,161 | +568 |
| Provisional station ECWT rows | 4,051 | 4,057 | +6 |
| Strict publication candidates | 1,666 | 1,964 | +298 |
| Diagnostic publication candidates | 7,837 | 7,910 | +73 |

## QA Notes

- The NOAA backfill manifest is fully classified: no `planned` rows and no `failed` rows remain.
- The final load introduced 176 additional plausibility rejects from batch 82-87 files. These should be sampled before compliance publication.
- The `100.400 F` maximum station ECWT remains a QA flag to investigate before any compliance publication.
- Current plant ECWT rows remain provisional. Strict publication candidates are not final accepted compliance values.
- The next meaningful engineering work is no longer bulk backfill. It is QA: plausibility rejects, high warm-tail station ECWT outliers, station-selection review, and publication/export rules.

## Reports Produced

- `docs/noaa_backfill_download_batch82_report.md`
- `docs/noaa_backfill_download_batch83_report.md`
- `docs/noaa_backfill_download_batch84_report.md`
- `docs/noaa_backfill_download_batch85_report.md`
- `docs/noaa_backfill_download_batch86_report.md`
- `docs/noaa_backfill_download_batch87_report.md`
- `docs/noaa_backfill_download_batch8_20260624T203225Z_report.md`
- `docs/noaa_backfill_download_batch23_20260624T203233Z_report.md`
- `docs/noaa_backfill_download_batch25_20260624T203236Z_report.md`
- `docs/noaa_backfill_download_batch28_20260624T203239Z_report.md`
- `docs/noaa_backfill_download_batch31_20260624T203243Z_report.md`
- `docs/noaa_backfill_download_batch34_20260624T203244Z_report.md`
- `docs/noaa_backfill_download_batch37_20260624T203245Z_report.md`
- `docs/noaa_backfill_download_batch43_20260624T203246Z_report.md`
- `docs/noaa_hourly_djf_load_20260624T195519Z_report.md`
- `docs/noaa_hourly_djf_load_20260624T203310Z_report.md`
- `docs/station_year_djf_coverage_20260624T200228Z_report.md`
- `docs/station_year_djf_coverage_20260624T203330Z_report.md`
- `docs/station_ecwt_loaded_20260624T202030Z_report.md`
- `docs/station_ecwt_loaded_20260624T205220Z_report.md`
- `docs/plant_ecwt_provisional_20260624T203051Z_report.md`
- `docs/plant_ecwt_provisional_20260624T205856Z_report.md`
- `docs/plant_ecwt_readiness_20260624T203120Z_report.md`
- `docs/plant_ecwt_readiness_20260624T203130Z_report.md`
- `docs/plant_ecwt_readiness_20260624T210010Z_report.md`
- `docs/plant_ecwt_readiness_20260624T210028Z_report.md`

## Next Step

Move from bulk loading to QA and publication hardening. Start with the 176 plausibility rejects from the final large load and the persistent `100.400 F` maximum station ECWT outlier, then produce an export candidate limited to strict `publication_candidate` rows.
