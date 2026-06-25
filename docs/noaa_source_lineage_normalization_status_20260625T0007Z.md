# NOAA Source Lineage Normalization Checkpoint

Generated UTC: 2026-06-25T00:07:00Z

## Summary

This checkpoint records the cleanup of the NOAA Global Hourly source-lineage
audit debt identified by `noaa_weather_qa_20260624T211907Z`.

Before normalization, 27,561 loaded NOAA station-year files and 17,465,507
canonical DJF hourly rows pointed at the coarse
`noaa_global_hourly_local_raw_inventory_3e447b31e3e36679` source record instead
of SHA-256-backed per-file `audit.source_file` records.

The normalization was run in two committed-code passes:

| Run | Purpose | Files mapped | Hourly rows relinked | Exceptions |
| --- | --- | ---: | ---: | ---: |
| `noaa_source_lineage_normalization_20260624T213521Z` | live smoke test | 5 | 3,185 | 0 |
| `noaa_source_lineage_normalization_20260624T213703Z` | full remaining cleanup | 27,556 | 17,462,322 | 0 |
| **Total** |  | **27,561** | **17,465,507** | **0** |

Both runs used code commit `cf510337201a437077bcbcb8697a0b7d3800a809`.

## Verified Post-State

The follow-up NOAA QA run `noaa_weather_qa_20260625T000513Z` verified:

| Metric | Count |
| --- | ---: |
| Loaded NOAA file rows missing source SHA-256 | 0 |
| Canonical DJF hourly rows needing source lineage | 0 |
| Canonical DJF hourly rows | 50,346,347 |
| Rows outside the absolute temperature window | 0 |
| SHEF rows below the SHEF-specific floor | 0 |

## Remaining QA Items

- The QA reconstruction still shows an 11-row historical plausibility-reject
  count mismatch for station `994973-99999` in source years 2019 and 2020.
  The mismatch is compatible with those files having been loaded before the
  current SHEF-specific floor was added; canonical weather guardrails show no
  current ECWT input rows violating that floor.
- Warm station ECWT outliers remain present in provisional station-level
  outputs, but the strict plant readiness gate keeps those low-coverage rows
  out of the current publication-candidate export.
- The current strict plant ECWT preview remains
  `plant_ecwt_publication_candidates_20260624T212003Z` with 1,964 rows.
