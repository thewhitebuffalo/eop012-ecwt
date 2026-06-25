# NOAA Policy Refresh and ECWT Chain Checkpoint

Generated UTC: 2026-06-25T01:01:00Z

## Summary

This checkpoint closes the NOAA plausibility-reject reconciliation gap that
remained after source-lineage normalization.

The stale rows were limited to station `994973-99999` for source years 2019 and
2020. They had been loaded before the current SHEF-specific plausibility floor
was added. The canonical hourly table already satisfied the current weather
guardrails, so the cleanup refreshed only `weather.noaa_hourly_load_file`
parser counters and recorded old/new values in
`audit.noaa_load_file_policy_refresh`.

## Policy Refresh

| Run | Rows checked | Rows changed | Notes |
| --- | ---: | ---: | --- |
| `noaa_load_file_policy_refresh_20260625T001449Z` | 2 | 2 | Refreshed load-file counters only; `weather.hourly_djf` unchanged |

Affected counter changes:

| Station | Year | Rejects old | Rejects new | Valid old | Valid new | Loaded hours old | Loaded hours new |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `994973-99999` | 2019 | 65 | 71 | 1,197 | 1,191 | 1,094 | 1,095 |
| `994973-99999` | 2020 | 8 | 13 | 1,027 | 1,022 | 1,012 | 1,011 |

## QA Post-State

Fresh QA run: `noaa_weather_qa_20260625T001858Z`

| Metric | Count |
| --- | ---: |
| Loaded files with plausibility rejects | 35 |
| DB counted plausibility rejects | 888 |
| Reconstructed plausibility reject rows | 888 |
| Reconstructed minus DB count | 0 |
| Files with count mismatches | 0 |
| Loaded file rows missing source SHA-256 | 0 |
| Rows outside absolute C window | 0 |
| SHEF rows below SHEF floor | 0 |

## Refreshed ECWT Chain

The downstream audit chain was rebuilt after the load-file counter refresh:

| Stage | Run | Key count |
| --- | --- | ---: |
| Station-year DJF coverage | `station_year_djf_coverage_20260625T002229Z` | 62,318 station-years |
| Station ECWT | `station_ecwt_loaded_20260625T004335Z` | 4,250 station rows |
| Plant ECWT | `plant_ecwt_provisional_20260625T005854Z` | 16,132 plant rows |
| Strict readiness | `plant_ecwt_readiness_20260625T005939Z` | 1,964 publication candidates |
| Diagnostic readiness at 0.25 coverage | `plant_ecwt_readiness_20260625T005951Z` | 7,910 publication candidates |
| Strict candidate export | `plant_ecwt_publication_candidates_20260625T010006Z` | 1,964 exported rows |

## Remaining Work

- Warm provisional station-level ECWT outliers remain visible in QA, but strict
  plant readiness excludes those low-coverage selections from the publication
  candidate export.
- The next publication-hardening step is station-selection review for the 1,964
  strict candidates, especially shared station assignments and warm-region edge
  cases.
