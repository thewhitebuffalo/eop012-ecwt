# ADR-0006 ECWT Status

- ADR-0006 run ID: `plant_ecwt_adr0006_20260702T022442Z`
- Release ID: `scoped_plant_ecwt_adr0006_release_20260702T022442Z`
- Station candidate run ID: `noaa_station_candidates_20260625T065445Z`
- Calculation date: `2025-03-01`
- Expected DJF hours: `55584`
- Publish floor: `95%` (`52805` populated winter hours)
- Git commit: `15d7ec51f91b11a4fff154ce80db379b4c4e2eb1`
- Release CSV: `/Users/Shared/EOP012/rebuild/data/processed/scoped_plant_ecwt_adr0006_release_20260702T022442Z.csv`
- Release CSV SHA-256: `a600f158a8d1477fe417d84e1932902dd0c8a6eee03bcff958a8a01a5dbd9792`
- Published checksum file: `data/processed/adr0006_release_20260702T022442Z_SHA256SUMS.txt`

## Counts

| Metric | Count |
| --- | ---: |
| Result rows | 15975 |
| Rows with public ECWT | 15877 |
| Rows with diagnostic ECWT | 15947 |
| Held rows with null public ECWT | 70 |
| Public ECWT below 95% coverage | 0 |
| Held rows with public ECWT | 0 |
| Cold-tail rows | 1947885 |
| Plants with cold-tail rows | 15947 |

## Confidence Split

| Tier | Plants |
| --- | ---: |
| `complete` | 15840 |
| `adequate` | 37 |
| `provisional_review` | 70 |
| `blocked_no_data` | 28 |

## Coverage Distribution

| Coverage band | Plants |
| --- | ---: |
| `>=99%` | 15840 |
| `95-99%` | 37 |
| `80-95%` | 70 |
| `50-80%` | 0 |
| `0-50%` | 0 |
| `0%` | 28 |

## Notes

- ECWT math was calculated through `scripts/ecwt_core.py`; the script does not reimplement percentile or adequacy math.
- `ecwt_f` is the public value and is null unless `assess_adequacy(...).publishable` is true. Held rows retain `diagnostic_ecwt_f`, coverage, shortfall, and towers tried.
- The release is analytical and is not a Generator Owner compliance filing.
- Existing `weather.hourly_djf.obs_timestamp` is backfilled to the canonical hour where the prior loader did not retain the raw NOAA `DATE` timestamp. Future loads should populate the raw observation timestamp directly.
- Full composite hours are exposed by `calc.plant_ecwt_adr0004_composite_hour`; materialized audit rows are limited to cold-tail hours to avoid duplicating the primary-station series hundreds of millions of times.
- ADR-0006 restricts land-plant composites to land stations; marine/ship platforms are excluded because their air temperatures are water-modulated and FM-13/buoy sensor failures can pass global-plausibility QC.
- Known tiny-sample ECWT anomalies are documented in `docs/findings/adr0004_tiny_sample_ecwt_anomalies.md`; one-hour artifacts cannot publish under ADR-0006, and below-floor rows are held with null public `ecwt_f`.
