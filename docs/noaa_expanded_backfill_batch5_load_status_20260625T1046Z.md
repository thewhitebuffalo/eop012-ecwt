# NOAA Expanded Backfill Batch 5 Load Status

Generated UTC: 2026-06-25T10:46:00Z

## Batch 5 Download

- Run: `noaa_backfill_download_batch5_20260625T103323Z`
- Manifest: `noaa_backfill_manifest_20260625T070923Z`
- Batch number: `5`
- Attempted station-years: `1,000`
- Downloaded: `909`
- Missing on AWS: `91`
- True failures: `0`
- Downloaded bytes: `3,278,543,244`
- Report: `docs/noaa_backfill_download_batch5_20260625T103323Z_report.md`

## Batch 5 Load

- Run: `noaa_hourly_djf_load_20260625T104206Z`
- Loaded files: `909`
- Failed files: `0`
- Canonical DJF hours staged: `1,429,129`
- Rejected source-code rows: `166,830`
- Rejected plausibility rows: `0`
- Duplicate station-hour observations: `623,052`
- Report: `docs/noaa_hourly_djf_load_20260625T104206Z_report.md`

## Compact Coverage Refresh

- Run: `station_year_djf_coverage_20260625T104547Z`
- Coverage table: `weather.station_year_djf_coverage_current`
- Coverage rows: `67,103`
- Complete station-years: `16,413`
- Partial station-years: `48,134`
- Empty station-years: `2,556`
- Valid DJF hours represented: `57,629,506`
- Report: `docs/station_year_djf_coverage_20260625T104547Z_report.md`

## Remaining Expanded Manifest

After batch 5:

| Manifest Status | Rows |
| --- | ---: |
| `downloaded` | 4,785 |
| `missing` | 215 |
| `planned` | 6,432 |

Remaining planned batches:

| Batch | Planned Rows |
| ---: | ---: |
| 6 | 1,000 |
| 7 | 1,000 |
| 8 | 1,000 |
| 9 | 1,000 |
| 10 | 1,000 |
| 11 | 1,000 |
| 12 | 432 |

## Notes

- Batch 5 had no retryable download failures.
- Station and plant ECWT were not recomputed after this batch; the latest full ECWT refresh remains batch 3.
- Compact coverage remains suitable for per-batch weather coverage tracking.
