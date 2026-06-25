# Fixed-Coverage Threshold Diagnostic

Generated UTC: 2026-06-25T04:45:35Z

## Scope

- Source blocker CSV: `fixed_period_readiness_blockers_20260625T043609Z.csv`
- Plant ECWT run ID: `plant_ecwt_provisional_fixed_period_20260625T043543Z`
- Readiness run ID: `plant_ecwt_readiness_fixed_period_20260625T043609Z`
- Fixed period: `2000-2025`
- Current publication coverage gate: `0.95`
- Current loaded-year gate: `20`

## Threshold Sensitivity

Additional blocked plants that would pass each alternate fixed-coverage threshold,
while still requiring at least 20 loaded station-years:

| Fixed coverage threshold | Additional blocked plants passing |
| ---: | ---: |
| 0.950 | 0 |
| 0.940 | 0 |
| 0.935 | 96 |
| 0.930 | 98 |
| 0.920 | 119 |
| 0.900 | 173 |
| 0.850 | 482 |
| 0.800 | 2,053 |
| 0.750 | 3,021 |
| 0.500 | 7,418 |
| 0.250 | 13,836 |
| 0.100 | 15,923 |

## Coverage Distribution

| Best fixed coverage ratio band | Blocked plants |
| --- | ---: |
| 0.95-1.00 | 0 |
| 0.94-0.95 | 0 |
| 0.93-0.94 | 98 |
| 0.92-0.93 | 21 |
| 0.90-0.92 | 54 |
| 0.85-0.90 | 309 |
| 0.80-0.85 | 1,571 |
| 0.75-0.80 | 968 |
| 0.50-0.75 | 4,416 |
| 0.25-0.50 | 6,418 |
| 0.10-0.25 | 2,087 |
| 0.00-0.10 | 28 |

## Loaded-Year Distribution

| Loaded station-year threshold | Blocked plants meeting threshold |
| ---: | ---: |
| 26 | 12,559 |
| 25 | 12,921 |
| 24 | 12,960 |
| 23 | 13,350 |
| 22 | 14,133 |
| 21 | 14,985 |
| 20 | 15,923 |

## Interpretation

The 95% fixed-period coverage gate is not merely excluding a near-threshold tail.
No blocked plant has a best candidate station above 94% fixed-period coverage, and
only 173 additional blocked plants would pass even if the threshold dropped to 90%.

This means the remaining 15,923 fixed-coverage blockers cannot be solved by a small
threshold adjustment. They require a methodology decision about the analysis period,
the expected-hour denominator, whether sparse historical years should be excluded, or
whether plant/station selection should use a different representative-station policy.
