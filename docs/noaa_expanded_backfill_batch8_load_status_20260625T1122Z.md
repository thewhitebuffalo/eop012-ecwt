# NOAA Expanded Backfill Batch 8 Load Status

Generated UTC: 2026-06-25T11:22:00Z

## Batch 8 Download

- Run: `noaa_backfill_download_batch8_20260625T111201Z`
- Manifest: `noaa_backfill_manifest_20260625T070923Z`
- Batch number: `8`
- Attempted station-years: `1,000`
- Downloaded: `851`
- Missing on AWS: `149`
- True failures: `0`
- Downloaded bytes: `2,436,159,345`
- Report: `docs/noaa_backfill_download_batch8_20260625T111201Z_report.md`

## Batch 8 Load

- Run: `noaa_hourly_djf_load_20260625T111830Z`
- Loaded files: `851`
- Failed files: `0`
- Canonical DJF hours staged: `1,262,782`
- Rejected source-code rows: `137,238`
- Rejected plausibility rows: `0`
- Duplicate station-hour observations: `259,736`
- Report: `docs/noaa_hourly_djf_load_20260625T111830Z_report.md`

## Compact Coverage Refresh

- Run: `station_year_djf_coverage_20260625T112154Z`
- Coverage table: `weather.station_year_djf_coverage_current`
- Coverage rows: `69,800`
- Complete station-years: `17,830`
- Partial station-years: `49,289`
- Empty station-years: `2,681`
- Valid DJF hours represented: `61,633,010`
- Report: `docs/station_year_djf_coverage_20260625T112154Z_report.md`

## Remaining Expanded Manifest

After batch 8:

| Manifest Status | Rows |
| --- | ---: |
| `downloaded` | 7,482 |
| `missing` | 518 |
| `planned` | 3,432 |

Remaining planned batches:

| Batch | Planned Rows |
| ---: | ---: |
| 9 | 1,000 |
| 10 | 1,000 |
| 11 | 1,000 |
| 12 | 432 |

## Notes

- Batch 8 had no retryable download failures.
- Station and plant ECWT were not recomputed after this batch; the latest full ECWT refresh remains batch 3.
- Compact coverage refresh remains under 10 seconds.
