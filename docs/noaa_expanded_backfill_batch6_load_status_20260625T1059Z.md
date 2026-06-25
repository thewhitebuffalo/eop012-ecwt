# NOAA Expanded Backfill Batch 6 Load Status

Generated UTC: 2026-06-25T10:59:00Z

## Batch 6 Download

- Run: `noaa_backfill_download_batch6_20260625T104644Z`
- Manifest: `noaa_backfill_manifest_20260625T070923Z`
- Batch number: `6`
- Attempted station-years: `1,000`
- Downloaded: `915`
- Missing on AWS: `85`
- True failures: `0`
- Downloaded bytes: `2,949,283,352`
- Report: `docs/noaa_backfill_download_batch6_20260625T104644Z_report.md`

## Batch 6 Load

- Run: `noaa_hourly_djf_load_20260625T105436Z`
- Loaded files: `915`
- Failed files: `0`
- Canonical DJF hours staged: `1,407,077`
- Rejected source-code rows: `120,966`
- Rejected plausibility rows: `0`
- Duplicate station-hour observations: `457,971`
- Report: `docs/noaa_hourly_djf_load_20260625T105436Z_report.md`

## Compact Coverage Refresh

- Run: `station_year_djf_coverage_20260625T105829Z`
- Coverage table: `weather.station_year_djf_coverage_current`
- Coverage rows: `68,018`
- Complete station-years: `16,919`
- Partial station-years: `48,501`
- Empty station-years: `2,598`
- Valid DJF hours represented: `59,036,583`
- Report: `docs/station_year_djf_coverage_20260625T105829Z_report.md`

## Remaining Expanded Manifest

After batch 6:

| Manifest Status | Rows |
| --- | ---: |
| `downloaded` | 5,700 |
| `missing` | 300 |
| `planned` | 5,432 |

Remaining planned batches:

| Batch | Planned Rows |
| ---: | ---: |
| 7 | 1,000 |
| 8 | 1,000 |
| 9 | 1,000 |
| 10 | 1,000 |
| 11 | 1,000 |
| 12 | 432 |

## Notes

- Batch 6 had no retryable download failures.
- Station and plant ECWT were not recomputed after this batch; the latest full ECWT refresh remains batch 3.
- Compact coverage refresh remains under 10 seconds.
