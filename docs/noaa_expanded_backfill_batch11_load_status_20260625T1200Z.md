# NOAA Expanded Backfill Batch 11 Load Status

Generated UTC: 2026-06-25T12:00:00Z

## Batch 11 Download

- Run: `noaa_backfill_download_batch11_20260625T115105Z`
- Manifest: `noaa_backfill_manifest_20260625T070923Z`
- Batch number: `11`
- Attempted station-years: `1,000`
- Downloaded: `892`
- Missing on AWS: `108`
- True failures: `0`
- Downloaded bytes: `1,851,802,178`
- Report: `docs/noaa_backfill_download_batch11_20260625T115105Z_report.md`

## Batch 11 Load

- Run: `noaa_hourly_djf_load_20260625T115629Z`
- Loaded files: `892`
- Failed files: `0`
- Canonical DJF hours staged: `1,031,670`
- Rejected source-code rows: `0`
- Rejected plausibility rows: `11`
- Duplicate station-hour observations: `47,800`
- Report: `docs/noaa_hourly_djf_load_20260625T115629Z_report.md`

## Compact Coverage Refresh

- Run: `station_year_djf_coverage_20260625T115920Z`
- Coverage table: `weather.station_year_djf_coverage_current`
- Coverage rows: `72,259`
- Complete station-years: `18,653`
- Partial station-years: `50,803`
- Empty station-years: `2,803`
- Valid DJF hours represented: `64,702,616`
- Report: `docs/station_year_djf_coverage_20260625T115920Z_report.md`

## Remaining Expanded Manifest

After batch 11:

| Manifest Status | Rows |
| --- | ---: |
| `downloaded` | 9,941 |
| `missing` | 1,059 |
| `planned` | 432 |

Remaining planned batches:

| Batch | Planned Rows |
| ---: | ---: |
| 12 | 432 |

## Notes

- Batch 11 had no retryable download failures.
- Station and plant ECWT were not recomputed after this batch; the latest full ECWT refresh remains batch 3.
- Batch 12 is the final planned batch in the expanded manifest.
