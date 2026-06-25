# NOAA Expanded Backfill Batch 10 Load Status

Generated UTC: 2026-06-25T11:50:00Z

## Batch 10 Download

- Run: `noaa_backfill_download_batch10_20260625T113541Z`
- Manifest: `noaa_backfill_manifest_20260625T070923Z`
- Batch number: `10`
- Attempted station-years: `1,000`
- Downloaded: `851`
- Missing on AWS: `149`
- True failures: `0`
- Downloaded bytes: `1,839,544,363`
- Report: `docs/noaa_backfill_download_batch10_20260625T113541Z_report.md`

## Batch 10 Load

- Run: `noaa_hourly_djf_load_20260625T114130Z`
- Loaded files: `851`
- Failed files: `0`
- Canonical DJF hours staged: `998,337`
- Rejected source-code rows: `6,470`
- Rejected plausibility rows: `3`
- Duplicate station-hour observations: `131,799`
- Report: `docs/noaa_hourly_djf_load_20260625T114130Z_report.md`

## Compact Coverage Refresh

- Run: `station_year_djf_coverage_20260625T114942Z`
- Coverage table: `weather.station_year_djf_coverage_current`
- Coverage rows: `71,367`
- Complete station-years: `18,441`
- Partial station-years: `50,168`
- Empty station-years: `2,758`
- Valid DJF hours represented: `63,670,946`
- Report: `docs/station_year_djf_coverage_20260625T114942Z_report.md`

## Remaining Expanded Manifest

After batch 10:

| Manifest Status | Rows |
| --- | ---: |
| `downloaded` | 9,049 |
| `missing` | 951 |
| `planned` | 1,432 |

Remaining planned batches:

| Batch | Planned Rows |
| ---: | ---: |
| 11 | 1,000 |
| 12 | 432 |

## Notes

- Batch 10 had no retryable download failures.
- Station and plant ECWT were not recomputed after this batch; the latest full ECWT refresh remains batch 3.
- Compact coverage refresh remains operationally fast enough for the batch loop.
