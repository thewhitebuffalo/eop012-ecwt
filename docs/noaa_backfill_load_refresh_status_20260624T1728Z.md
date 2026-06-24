# NOAA Backfill, Load, And ECWT Refresh Status

Generated UTC: 2026-06-24T17:28Z

## Scope

This checkpoint covers NOAA Global Hourly public AWS backfill batches 65 through 69, the subsequent DJF hourly load, and refreshed station/plant ECWT readiness outputs.

## Current State

| Metric | Value |
| --- | ---: |
| Total manifest batches | 87 |
| Processed/classified batches | 69 |
| Remaining planned batch range | 70-87 |
| Remaining planned manifest rows | 17,839 |
| Raw NOAA CSV files in cache | 30,094 |
| Partial `.part` files in cache | 0 |
| NOAA raw cache size | 213 GB |
| Postgres database size | 19 GB |
| Loaded canonical DJF hours | 45,515,001 |

## Manifest Status

| Status | Rows |
| --- | ---: |
| `downloaded` | 30,094 |
| `missing` | 38,896 |
| `failed` | 10 |
| `planned` | 17,839 |
| `skipped` | 86,839 |

The 38,896 `missing` rows are terminal NOAA AWS 404s for planned station-year objects. They are not local corruption and are not retryable as ordinary download failures.

## Batch Results

| Batch | Downloaded | Missing On AWS | True Failures | Downloaded Bytes |
| ---: | ---: | ---: | ---: | ---: |
| 65 | 281 | 719 | 0 | 2,566,368,493 |
| 66 | 502 | 498 | 0 | 3,893,847,315 |
| 67 | 239 | 761 | 0 | 2,103,161,099 |
| 68 | 398 | 602 | 0 | 3,690,018,448 |
| 69 | 366 | 634 | 0 | 2,598,390,933 |
| **Total** | **1,786** | **3,214** | **0** | **14,851,786,288** |

Net result: the planned queue dropped by 5,000 rows. 1,786 new source files were downloaded and 3,214 rows were classified as missing from NOAA AWS.

## DJF Hourly Load

Run: `noaa_hourly_djf_load_20260624T165738Z`

| Metric | Count |
| --- | ---: |
| Candidate files selected | 1,786 |
| Loaded files | 1,786 |
| Failed files | 0 |
| Source bytes parsed | 14,851,786,288 |
| Raw rows seen | 34,399,406 |
| DJF rows seen | 8,662,435 |
| Rejected source-code rows | 3,825,414 |
| Valid DJF temperature rows | 4,579,074 |
| Invalid DJF temperature rows | 257,947 |
| Rejected plausibility rows | 0 |
| Duplicate station-hour observations | 2,939,966 |
| Canonical hourly rows staged | 1,639,108 |

## Coverage Refresh

Run: `station_year_djf_coverage_20260624T170430Z`

| Metric | Count |
| --- | ---: |
| Coverage rows | 57,655 |
| Complete station-years | 12,629 |
| Partial station-years | 42,885 |
| Empty station-years | 2,141 |
| Valid DJF hours represented | 45,515,001 |
| Rejected source rows represented | 130,129,180 |

## ECWT Refresh

Station run: `station_ecwt_loaded_20260624T171509Z`

| Metric | Value |
| --- | ---: |
| Station ECWT rows | 4,239 |
| Provisional station rows | 4,043 |
| Blocked station rows | 196 |
| Minimum station ECWT F | -58.216 |
| Maximum station ECWT F | 100.400 |

Plant run: `plant_ecwt_provisional_20260624T172405Z`

| Metric | Value |
| --- | ---: |
| Plant ECWT rows | 16,132 |
| Provisional plant ECWT rows | 16,104 |
| Blocked plant ECWT rows | 28 |
| Minimum plant ECWT F | -58.000 |
| Maximum plant ECWT F | 88.160 |

Strict readiness run: `plant_ecwt_readiness_20260624T172534Z`

| Metric | Count |
| --- | ---: |
| Publication candidates | 1,662 |
| Provisional low coverage | 14,442 |
| Blocked | 28 |
| Median coverage ratio | 0.2448 |

Diagnostic readiness run: `plant_ecwt_readiness_20260624T172556Z`

| Metric | Count |
| --- | ---: |
| Publication candidates at 0.25 coverage threshold | 7,747 |
| Provisional low coverage | 8,357 |
| Blocked | 28 |
| Median coverage ratio | 0.2448 |

## Movement Since Previous Checkpoint

Previous checkpoint: `docs/noaa_backfill_load_refresh_status_20260624T1627Z.md`

| Metric | Previous | Current | Delta |
| --- | ---: | ---: | ---: |
| Raw NOAA CSV files | 28,308 | 30,094 | +1,786 |
| Manifest `downloaded` rows | 28,308 | 30,094 | +1,786 |
| Manifest `missing` rows | 35,682 | 38,896 | +3,214 |
| Manifest `planned` rows | 22,839 | 17,839 | -5,000 |
| Loaded canonical DJF hours | 43,875,893 | 45,515,001 | +1,639,108 |
| Complete station-years | 12,095 | 12,629 | +534 |
| Provisional station ECWT rows | 4,043 | 4,043 | 0 |
| Strict publication candidates | 1,655 | 1,662 | +7 |
| Diagnostic publication candidates | 7,733 | 7,747 | +14 |

## QA Notes

- Batches 65 through 69 produced zero true download failures.
- The remaining manifest `failed` count is 10 historical retryable/non-terminal failures outside this batch set.
- The `100.400 F` maximum station ECWT remains a QA flag to investigate before any compliance publication. It is not currently blocking the bulk backfill/load path.
- Current plant ECWT rows remain provisional. Strict publication candidates are limited by the current station coverage gate.

## Reports Produced

- `docs/noaa_backfill_download_batch65_report.md`
- `docs/noaa_backfill_download_batch66_report.md`
- `docs/noaa_backfill_download_batch67_report.md`
- `docs/noaa_backfill_download_batch68_report.md`
- `docs/noaa_backfill_download_batch69_report.md`
- `docs/noaa_hourly_djf_load_20260624T165738Z_report.md`
- `docs/station_year_djf_coverage_20260624T170430Z_report.md`
- `docs/station_ecwt_loaded_20260624T171509Z_report.md`
- `docs/plant_ecwt_provisional_20260624T172405Z_report.md`
- `docs/plant_ecwt_readiness_20260624T172534Z_report.md`
- `docs/plant_ecwt_readiness_20260624T172556Z_report.md`

## Next Step

Continue NOAA public AWS backfill at batch 70. After the next batch group is classified, load only newly downloaded files, then refresh coverage, station ECWT, plant ECWT, and readiness.
