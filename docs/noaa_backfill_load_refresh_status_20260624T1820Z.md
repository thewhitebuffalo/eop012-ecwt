# NOAA Backfill, Load, And ECWT Refresh Status

Generated UTC: 2026-06-24T18:20Z

## Scope

This checkpoint covers NOAA Global Hourly public AWS backfill batches 70 through 74, the subsequent DJF hourly load, and refreshed station/plant ECWT readiness outputs.

## Current State

| Metric | Value |
| --- | ---: |
| Total manifest batches | 87 |
| Processed/classified batches | 74 |
| Remaining planned batch range | 75-87 |
| Remaining planned manifest rows | 12,839 |
| Raw NOAA CSV files in cache | 31,723 |
| Partial `.part` files in cache | 0 |
| NOAA raw cache size | 225 GB |
| Postgres database size | 19 GB |
| Loaded canonical DJF hours | 47,007,437 |

## Manifest Status

| Status | Rows |
| --- | ---: |
| `downloaded` | 31,723 |
| `missing` | 42,267 |
| `failed` | 10 |
| `planned` | 12,839 |
| `skipped` | 86,839 |

The 42,267 `missing` rows are terminal NOAA AWS 404s for planned station-year objects. They are not local corruption and are not retryable as ordinary download failures.

## Batch Results

| Batch | Downloaded | Missing On AWS | True Failures | Downloaded Bytes |
| ---: | ---: | ---: | ---: | ---: |
| 70 | 305 | 695 | 0 | 2,661,841,415 |
| 71 | 481 | 519 | 0 | 3,653,392,108 |
| 72 | 210 | 790 | 0 | 1,724,930,177 |
| 73 | 416 | 584 | 0 | 3,163,056,209 |
| 74 | 217 | 783 | 0 | 1,646,341,452 |
| **Total** | **1,629** | **3,371** | **0** | **12,849,561,361** |

Net result: the planned queue dropped by 5,000 rows. 1,629 new source files were downloaded and 3,371 rows were classified as missing from NOAA AWS.

## DJF Hourly Load

Run: `noaa_hourly_djf_load_20260624T174932Z`

| Metric | Count |
| --- | ---: |
| Candidate files selected | 1,629 |
| Loaded files | 1,629 |
| Failed files | 0 |
| Source bytes parsed | 12,849,561,361 |
| Raw rows seen | 29,915,004 |
| DJF rows seen | 7,453,452 |
| Rejected source-code rows | 3,281,822 |
| Valid DJF temperature rows | 3,924,190 |
| Invalid DJF temperature rows | 247,440 |
| Rejected plausibility rows | 0 |
| Duplicate station-hour observations | 2,431,754 |
| Canonical hourly rows staged | 1,492,436 |

## Coverage Refresh

Run: `station_year_djf_coverage_20260624T175650Z`

| Metric | Count |
| --- | ---: |
| Coverage rows | 59,284 |
| Complete station-years | 13,119 |
| Partial station-years | 43,945 |
| Empty station-years | 2,220 |
| Valid DJF hours represented | 47,007,437 |
| Rejected source rows represented | 133,411,002 |

## ECWT Refresh

Station run: `station_ecwt_loaded_20260624T180803Z`

| Metric | Value |
| --- | ---: |
| Station ECWT rows | 4,240 |
| Provisional station rows | 4,043 |
| Blocked station rows | 197 |
| Minimum station ECWT F | -58.216 |
| Maximum station ECWT F | 100.400 |

Plant run: `plant_ecwt_provisional_20260624T181825Z`

| Metric | Value |
| --- | ---: |
| Plant ECWT rows | 16,132 |
| Provisional plant ECWT rows | 16,104 |
| Blocked plant ECWT rows | 28 |
| Minimum plant ECWT F | -58.000 |
| Maximum plant ECWT F | 88.160 |

Strict readiness run: `plant_ecwt_readiness_20260624T181957Z`

| Metric | Count |
| --- | ---: |
| Publication candidates | 1,673 |
| Provisional low coverage | 14,431 |
| Blocked | 28 |
| Median coverage ratio | 0.2464 |

Diagnostic readiness run: `plant_ecwt_readiness_20260624T182007Z`

| Metric | Count |
| --- | ---: |
| Publication candidates at 0.25 coverage threshold | 7,756 |
| Provisional low coverage | 8,348 |
| Blocked | 28 |
| Median coverage ratio | 0.2464 |

## Movement Since Previous Checkpoint

Previous checkpoint: `docs/noaa_backfill_load_refresh_status_20260624T1728Z.md`

| Metric | Previous | Current | Delta |
| --- | ---: | ---: | ---: |
| Raw NOAA CSV files | 30,094 | 31,723 | +1,629 |
| Manifest `downloaded` rows | 30,094 | 31,723 | +1,629 |
| Manifest `missing` rows | 38,896 | 42,267 | +3,371 |
| Manifest `planned` rows | 17,839 | 12,839 | -5,000 |
| Loaded canonical DJF hours | 45,515,001 | 47,007,437 | +1,492,436 |
| Complete station-years | 12,629 | 13,119 | +490 |
| Provisional station ECWT rows | 4,043 | 4,043 | 0 |
| Strict publication candidates | 1,662 | 1,673 | +11 |
| Diagnostic publication candidates | 7,747 | 7,756 | +9 |

## QA Notes

- Batches 70 through 74 produced zero true download failures.
- The remaining manifest `failed` count is 10 historical retryable/non-terminal failures outside this batch set.
- The `100.400 F` maximum station ECWT remains a QA flag to investigate before any compliance publication. It is not currently blocking the bulk backfill/load path.
- Current plant ECWT rows remain provisional. Strict publication candidates are limited by the current station coverage gate.

## Reports Produced

- `docs/noaa_backfill_download_batch70_report.md`
- `docs/noaa_backfill_download_batch71_report.md`
- `docs/noaa_backfill_download_batch72_report.md`
- `docs/noaa_backfill_download_batch73_report.md`
- `docs/noaa_backfill_download_batch74_report.md`
- `docs/noaa_hourly_djf_load_20260624T174932Z_report.md`
- `docs/station_year_djf_coverage_20260624T175650Z_report.md`
- `docs/station_ecwt_loaded_20260624T180803Z_report.md`
- `docs/plant_ecwt_provisional_20260624T181825Z_report.md`
- `docs/plant_ecwt_readiness_20260624T181957Z_report.md`
- `docs/plant_ecwt_readiness_20260624T182007Z_report.md`

## Next Step

Continue NOAA public AWS backfill at batch 75. After the next batch group is classified, load only newly downloaded files, then refresh coverage, station ECWT, plant ECWT, and readiness.
