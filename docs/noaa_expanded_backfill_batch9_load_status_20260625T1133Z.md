# NOAA Expanded Backfill Batch 9 Load Status

Generated UTC: 2026-06-25T11:33:00Z

## Batch 9 Download

- Run: `noaa_backfill_download_batch9_20260625T112307Z`
- Manifest: `noaa_backfill_manifest_20260625T070923Z`
- Batch number: `9`
- Attempted station-years: `1,000`
- Downloaded: `716`
- Missing on AWS: `284`
- True failures: `0`
- Downloaded bytes: `2,021,443,427`
- Report: `docs/noaa_backfill_download_batch9_20260625T112307Z_report.md`

## Batch 9 Load

- Run: `noaa_hourly_djf_load_20260625T112906Z`
- Loaded files: `716`
- Failed files: `0`
- Canonical DJF hours staged: `1,039,599`
- Rejected source-code rows: `49,751`
- Rejected plausibility rows: `4`
- Duplicate station-hour observations: `249,745`
- Report: `docs/noaa_hourly_djf_load_20260625T112906Z_report.md`

## Compact Coverage Refresh

- Run: `station_year_djf_coverage_20260625T113234Z`
- Coverage table: `weather.station_year_djf_coverage_current`
- Coverage rows: `70,516`
- Complete station-years: `18,172`
- Partial station-years: `49,632`
- Empty station-years: `2,712`
- Valid DJF hours represented: `62,672,609`
- Report: `docs/station_year_djf_coverage_20260625T113234Z_report.md`

## Remaining Expanded Manifest

After batch 9:

| Manifest Status | Rows |
| --- | ---: |
| `downloaded` | 8,198 |
| `missing` | 802 |
| `planned` | 2,432 |

Remaining planned batches:

| Batch | Planned Rows |
| ---: | ---: |
| 10 | 1,000 |
| 11 | 1,000 |
| 12 | 432 |

## Notes

- Batch 9 had no retryable download failures.
- Station and plant ECWT were not recomputed after this batch; the latest full ECWT refresh remains batch 3.
- Compact coverage refresh remains under 10 seconds.
