# NOAA Expanded Backfill Batch 4 Load Status

Generated UTC: 2026-06-25T10:33:00Z

## Batch 4 Download

- Run: `noaa_backfill_download_batch4_20260625T101910Z`
- Manifest: `noaa_backfill_manifest_20260625T070923Z`
- Batch number: `4`
- Attempted station-years: `1,000`
- Downloaded: `937`
- Missing on AWS: `63`
- True failures: `0`
- Downloaded bytes: `3,744,542,762`
- Report: `docs/noaa_backfill_download_batch4_20260625T101910Z_report.md`

## Batch 4 Load

- Run: `noaa_hourly_djf_load_20260625T102825Z`
- Loaded files: `937`
- Failed files: `0`
- Canonical DJF hours staged: `1,500,085`
- Rejected source-code rows: `289,798`
- Rejected plausibility rows: `0`
- Duplicate station-hour observations: `761,621`
- Report: `docs/noaa_hourly_djf_load_20260625T102825Z_report.md`

## Compact Coverage Refresh

- Run: `station_year_djf_coverage_20260625T103221Z`
- Coverage table: `weather.station_year_djf_coverage_current`
- Coverage rows: `66,194`
- Complete station-years: `15,884`
- Partial station-years: `47,784`
- Empty station-years: `2,526`
- Valid DJF hours represented: `56,200,377`
- Report: `docs/station_year_djf_coverage_20260625T103221Z_report.md`

## Remaining Expanded Manifest

After batch 4:

| Manifest Status | Rows |
| --- | ---: |
| `downloaded` | 3,876 |
| `missing` | 124 |
| `planned` | 7,432 |

Remaining planned batches:

| Batch | Planned Rows |
| ---: | ---: |
| 5 | 1,000 |
| 6 | 1,000 |
| 7 | 1,000 |
| 8 | 1,000 |
| 9 | 1,000 |
| 10 | 1,000 |
| 11 | 1,000 |
| 12 | 432 |

## Notes

- Batch 4 had no retryable download failures.
- Station and plant ECWT were not recomputed after this batch; the latest full ECWT refresh remains batch 3 (`station_ecwt_loaded_20260625T094708Z` and `plant_ecwt_provisional_20260625T100901Z`).
- Compact coverage continues to refresh quickly from `weather.station_year_hourly_summary`.
