# NOAA Expanded Backfill Completion Status

Generated UTC: 2026-06-25T12:20:00Z

## Expanded Manifest Final Status

Manifest: `noaa_backfill_manifest_20260625T070923Z`

| Manifest Status | Rows |
| --- | ---: |
| `downloaded` | 10,282 |
| `missing` | 1,150 |
| `planned` | 0 |

All planned expanded NOAA AWS backfill rows have been attempted. No retryable download failures remain in the expanded manifest run.

## Final Batch 12

- Download run: `noaa_backfill_download_batch12_20260625T120041Z`
- Attempted station-years: `432`
- Downloaded: `341`
- Missing on AWS: `91`
- True failures: `0`
- Downloaded bytes: `765,687,029`
- Load run: `noaa_hourly_djf_load_20260625T120307Z`
- Loaded files: `341`
- Failed files: `0`
- Canonical DJF hours staged: `427,496`

## Final Compact Coverage

- Run: `station_year_djf_coverage_20260625T120423Z`
- Coverage table: `weather.station_year_djf_coverage_current`
- Coverage rows: `72,600`
- Complete station-years: `18,775`
- Partial station-years: `51,011`
- Empty station-years: `2,814`
- Valid DJF hours represented: `65,130,112`

## Final Station ECWT

- Run: `station_ecwt_loaded_20260625T120444Z`
- Station ECWT rows: `4,936`
- Provisional station rows: `4,707`
- Blocked station rows: `229`
- Minimum station ECWT F: `-64.300`
- Maximum station ECWT F: `100.400`

## Final Plant ECWT

Active-window run: `plant_ecwt_provisional_20260625T121704Z`

- Plant ECWT rows: `16,132`
- Provisional plant rows: `16,104`
- Blocked plant rows: `28`
- Minimum plant ECWT F: `-58.000`
- Maximum plant ECWT F: `88.160`

Fixed-period run: `plant_ecwt_provisional_fixed_period_20260625T121752Z`

- Plant ECWT rows: `16,132`
- Provisional plant rows: `1,346`
- Blocked plant rows: `14,786`
- Minimum plant ECWT F: `-39.280`
- Maximum plant ECWT F: `10.400`

Fixed-period readiness run: `plant_ecwt_readiness_fixed_period_20260625T121909Z`

- Readiness rows: `16,132`
- Publication candidates: `1,346`
- Provisional low coverage: `0`
- Blocked: `14,786`
- Minimum coverage ratio among ready rows: `0.9501`
- Median coverage ratio among ready rows: `0.9596`

## Operational Notes

- The expanded NOAA AWS backfill queue is exhausted: remaining missing files are terminal AWS 404 records, not retryable failures.
- Compact coverage refreshes are now supported by `weather.station_year_hourly_summary` and `weather.station_year_djf_coverage_current`.
- The active-window plant result gives provisional ECWT values for almost every plant in the current EIA-860 plant universe.
- The fixed-period result is much stricter and remains coverage-blocked for most plants under the 2000-2025 fixed-period denominator.
- Remaining work before publication should focus on blocker diagnostics, station-selection review, final methodology decisions on fixed versus active-window denominator, and release packaging.
