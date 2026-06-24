# Plant Station Selection Stability Status

Generated UTC: 2026-06-24T04:37Z

Database: `eop012` on `127.0.0.1:5436`

## Summary

The provisional plant station-selection rule was changed from coverage-maximizing to rank/distance-first.

The old rule selected the candidate station with the largest currently loaded valid-hour count. That made the selected plant station unstable as NOAA backfill progressed and could pick a farther station merely because it had more downloaded data. The corrected rule selects the lowest-rank candidate station with provisional station ECWT, using distance, loaded valid-hour count, and station id only as tie-breakers.

This correction materially lowers current publication readiness counts. That is expected and desirable: weather coverage should decide whether a result is ready to publish, not which station represents the plant.

## Code Change

| Item | Value |
| --- | --- |
| Code commit | `23e67f27d52beebddc77612cf270c48939242097` |
| Updated script | `scripts/build_provisional_plant_ecwt.py` |
| Updated docs | `docs/database_operations.md`, `docs/methodology.md` |

## Corrected Result Runs

| Layer | Run ID | Result |
| --- | --- | ---: |
| Plant ECWT | `plant_ecwt_provisional_20260624T043636Z` | 16,104 provisional, 28 blocked |
| Strict readiness, 0.95 coverage | `plant_ecwt_readiness_20260624T043649Z` | 357 publication candidates |
| Diagnostic readiness, 0.25 coverage | `plant_ecwt_readiness_20260624T043655Z` | 4,225 diagnostic candidates |

## Impact Versus Previous Coverage-Maximizing Run

Previous plant run: `plant_ecwt_provisional_20260624T043007Z`

Previous strict readiness run: `plant_ecwt_readiness_20260624T043029Z`

| Change | Plants |
| --- | ---: |
| Selected station changed | 14,025 |
| Selected station unchanged | 2,107 |
| Strict candidate remained candidate | 285 |
| Strict candidate became low coverage | 2,327 |
| Low coverage became strict candidate | 72 |
| Low coverage remained low coverage | 13,420 |
| Blocked remained blocked | 28 |

## Selected Candidate Rank Distribution

| Candidate rank | Selected plants |
| ---: | ---: |
| 1 | 13,213 |
| 2 | 2,592 |
| 3 | 250 |
| 4 | 29 |
| 5 | 14 |
| 6 | 5 |
| 7 | 1 |

## Interpretation

- The earlier strict count of `2,612` was materially inflated by station substitution toward higher-coverage stations.
- The corrected strict count is `357` publication candidates.
- The corrected diagnostic count is `4,225` candidates at the relaxed `0.25` coverage threshold.
- The dominant remaining work is now nearest/ranked-station weather coverage: most selected representative stations still need more NOAA hourly data loaded.
- The next download/load cycles should continue, but readiness should be tracked using the corrected station-selection run family.
