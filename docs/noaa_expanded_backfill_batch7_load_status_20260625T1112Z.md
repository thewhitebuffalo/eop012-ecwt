# NOAA Expanded Backfill Batch 7 Load Status

Generated UTC: 2026-06-25T11:12:00Z

## Batch 7 Download

- Run: `noaa_backfill_download_batch7_20260625T105934Z`
- Manifest: `noaa_backfill_manifest_20260625T070923Z`
- Batch number: `7`
- Attempted station-years: `1,000`
- Downloaded: `931`
- Missing on AWS: `69`
- True failures: `0`
- Downloaded bytes: `2,732,835,180`
- Report: `docs/noaa_backfill_download_batch7_20260625T105934Z_report.md`

## Batch 7 Load

- Run: `noaa_hourly_djf_load_20260625T110659Z`
- Loaded files: `931`
- Failed files: `0`
- Canonical DJF hours staged: `1,333,645`
- Rejected source-code rows: `132,644`
- Rejected plausibility rows: `7`
- Duplicate station-hour observations: `345,378`
- Report: `docs/noaa_hourly_djf_load_20260625T110659Z_report.md`

## Compact Coverage Refresh

- Run: `station_year_djf_coverage_20260625T111104Z`
- Coverage table: `weather.station_year_djf_coverage_current`
- Coverage rows: `68,949`
- Complete station-years: `17,384`
- Partial station-years: `48,910`
- Empty station-years: `2,655`
- Valid DJF hours represented: `60,370,228`
- Report: `docs/station_year_djf_coverage_20260625T111104Z_report.md`

## Remaining Expanded Manifest

After batch 7:

| Manifest Status | Rows |
| --- | ---: |
| `downloaded` | 6,631 |
| `missing` | 369 |
| `planned` | 4,432 |

Remaining planned batches:

| Batch | Planned Rows |
| ---: | ---: |
| 8 | 1,000 |
| 9 | 1,000 |
| 10 | 1,000 |
| 11 | 1,000 |
| 12 | 432 |

## Notes

- Batch 7 had no retryable download failures.
- Station and plant ECWT were not recomputed after this batch; the latest full ECWT refresh remains batch 3.
- Compact coverage refresh remains under 10 seconds.
