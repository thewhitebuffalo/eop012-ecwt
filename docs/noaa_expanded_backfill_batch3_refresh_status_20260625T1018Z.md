# NOAA Expanded Backfill Batch 3 Refresh Status

Generated UTC: 2026-06-25T10:18:00Z

## Scope

This checkpoint covers NOAA expanded backfill batch 3, the corresponding DJF hourly load, compact current coverage refresh, station ECWT refresh, and active-window plant ECWT refresh.

## Performance Hardening Applied First

- Added `weather.station_year_hourly_summary` and backfilled it from `weather.hourly_djf`.
- Updated the NOAA DJF loader so future loads refresh touched station-year summaries automatically.
- Added compact `weather.station_year_djf_coverage_current` for iterative batch refreshes.
- Kept `weather.station_year_djf_coverage` as the historical/milestone snapshot table.
- Updated station and plant ECWT builders to read compact current coverage when that is the latest coverage surface.

## Batch 3 Download

- Run: `noaa_backfill_download_batch3_20260625T093037Z`
- Manifest: `noaa_backfill_manifest_20260625T070923Z`
- Batch number: `3`
- Attempted station-years: `1,000`
- Downloaded: `964`
- Missing on AWS: `36`
- True failures: `0`
- Downloaded bytes: `3,734,049,068`
- Report: `docs/noaa_backfill_download_batch3_20260625T093037Z_report.md`

## Batch 3 Load

- Run: `noaa_hourly_djf_load_20260625T094018Z`
- Loaded files: `964`
- Failed files: `0`
- Canonical DJF hours staged: `1,507,735`
- Rejected source-code rows: `275,541`
- Rejected plausibility rows: `133`
- Duplicate station-hour observations: `768,379`
- Report: `docs/noaa_hourly_djf_load_20260625T094018Z_report.md`

## Coverage And ECWT Refresh

- Compact coverage run: `station_year_djf_coverage_20260625T094519Z`
- Coverage table: `weather.station_year_djf_coverage_current`
- Coverage rows: `65,257`
- Complete station-years: `15,335`
- Partial station-years: `47,431`
- Empty station-years: `2,491`
- Valid DJF hours represented: `54,700,292`

- Station ECWT run: `station_ecwt_loaded_20260625T094708Z`
- Station ECWT rows: `4,747`
- Provisional station rows: `4,532`
- Blocked station rows: `215`
- Minimum station ECWT F: `-62.500`
- Maximum station ECWT F: `100.400`

- Active-window plant ECWT run: `plant_ecwt_provisional_20260625T100901Z`
- Plant ECWT rows: `16,132`
- Provisional plant rows: `16,104`
- Blocked plant rows: `28`
- Minimum plant ECWT F: `-58.000`
- Maximum plant ECWT F: `88.160`

## Remaining Expanded Manifest

After batch 3:

| Manifest Status | Rows |
| --- | ---: |
| `downloaded` | 2,939 |
| `missing` | 61 |
| `planned` | 8,432 |

Remaining planned batches:

| Batch | Planned Rows |
| ---: | ---: |
| 4 | 1,000 |
| 5 | 1,000 |
| 6 | 1,000 |
| 7 | 1,000 |
| 8 | 1,000 |
| 9 | 1,000 |
| 10 | 1,000 |
| 11 | 1,000 |
| 12 | 432 |

## Operational Notes

- Batch 3 had no retryable download failures. The 36 404 outcomes are terminal `missing_on_aws` records.
- Compact coverage refresh is now fast enough for batch iteration, roughly 9 seconds in this checkpoint.
- Full station ECWT still took about 11 minutes, and active-window plant ECWT took about 9 minutes. The next performance hardening target is incremental/carry-forward station ECWT and/or materialized candidate scoring before running ECWT after every remaining batch.
