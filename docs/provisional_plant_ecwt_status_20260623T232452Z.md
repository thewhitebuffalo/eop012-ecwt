# Provisional Plant ECWT Status

Generated UTC: 2026-06-23T23:24:52Z

Database: `eop012` on `127.0.0.1:5436`

## Summary

This pass moved the rebuild from station-level provisional ECWT to plant-level provisional ECWT. Every plant now has a `calc.plant_ecwt` row in the latest run.

Latest plant ECWT run: `plant_ecwt_provisional_20260623T232311Z`

| Metric | Value |
| --- | ---: |
| Plant ECWT rows | 16,132 |
| Provisional plant rows | 16,104 |
| Blocked plant rows | 28 |
| Selected station segments | 16,104 |
| Distinct selected stations | 871 |
| Minimum provisional plant ECWT F | -52.600 |
| Maximum provisional plant ECWT F | 68.290 |
| Provisional plants with fewer than 500 valid hours | 319 |
| Provisional plants with at least 2,000 valid hours | 3,891 |

## Weather State

The canonical weather table was cleaned after a QA pass found one impossible `-88.0 C` `TMP` row at `998242-99999` / Saginaw Bay Light 1. The loader default lower plausibility bound is now `-65 C`.

| Metric | Value |
| --- | ---: |
| `weather.hourly_djf` rows | 2,652,388 |
| Distinct stations | 2,755 |
| Minimum canonical dry-bulb C | -49.400 |
| Maximum canonical dry-bulb C | 37.000 |
| Minimum canonical dry-bulb F | -56.920 |
| Maximum canonical dry-bulb F | 98.600 |

Latest coverage run: `station_year_djf_coverage_20260623T232251Z`

| Metric | Value |
| --- | ---: |
| Station-year coverage rows | 5,000 |
| Complete station-years | 205 |
| Partial station-years | 4,673 |
| Empty station-years | 122 |
| Valid DJF hours represented | 2,652,388 |

Latest station ECWT run: `station_ecwt_loaded_20260623T232301Z`

| Metric | Value |
| --- | ---: |
| Station ECWT rows | 2,835 |
| Provisional station rows | 2,755 |
| Blocked station rows | 80 |
| Minimum station ECWT F | -56.421 |
| Maximum station ECWT F | 71.060 |

## Download Lane

Additional AWS backfill batches completed in this pass:

| Batch | Run ID | Downloaded | HTTP 404 | Bytes |
| ---: | --- | ---: | ---: | ---: |
| 8 | `noaa_backfill_download_batch8_20260623T230828Z` | 633 | 367 | 5,728,475,141 |
| 9 | `noaa_backfill_download_batch9_20260623T231656Z` | 636 | 364 | 5,125,004,130 |

Current AWS cache:

| Metric | Value |
| --- | ---: |
| CSV files | 5,790 |
| `.part` files | 0 |
| Disk usage | 42 GB |

## Interpretation

- Plant ECWT is now wired end-to-end, but it is still provisional.
- The blocked plant count is down to 28 because most plants now have at least one candidate station with provisional station ECWT.
- The biggest remaining publication blocker is coverage quality, not table plumbing: many plant rows still rely on partial station-year coverage.
- Next work should continue the steady loop: AWS download, hardened load, coverage refresh, station ECWT refresh, plant ECWT refresh.
