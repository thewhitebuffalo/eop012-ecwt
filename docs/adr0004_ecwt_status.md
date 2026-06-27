# ADR-0005 ECWT Status

- ADR-0005 run ID: `plant_ecwt_adr0004_20260626T235840Z`
- Release ID: `scoped_plant_ecwt_adr0004_release_20260626T235840Z`
- Station candidate run ID: `noaa_station_candidates_20260625T065445Z`
- Calculation date: `2025-03-01`
- Expected DJF hours: `55584`
- Publish floor: `95%` (`52805` populated winter hours)
- Git commit: `50e2d1aeedfbbf1c9f88605835a10fd194d3833e`
- Release CSV: `/Users/Shared/EOP012/rebuild/data/processed/scoped_plant_ecwt_adr0004_release_20260626T235840Z.csv`
- Release CSV SHA-256: `d6a81136aa8a869644868f7589ed7df9002703bfcd16ea3e944efbe55fc6b4d6`
- Published checksum file: `data/processed/adr0004_release_20260626T235840Z_SHA256SUMS.txt`

## Counts

| Metric | Count |
| --- | ---: |
| Result rows | 15975 |
| Rows with public ECWT | 15932 |
| Rows with diagnostic ECWT | 15947 |
| Held rows with null public ECWT | 15 |
| Public ECWT below 95% coverage | 0 |
| Held rows with public ECWT | 0 |
| Cold-tail rows | 1961043 |
| Plants with cold-tail rows | 15947 |

## Confidence Split

| Tier | Plants |
| --- | ---: |
| `complete` | 15932 |
| `adequate` | 0 |
| `provisional_review` | 15 |
| `blocked_no_data` | 28 |

## Coverage Distribution

| Coverage band | Plants |
| --- | ---: |
| `>=99%` | 15932 |
| `95-99%` | 0 |
| `80-95%` | 15 |
| `50-80%` | 0 |
| `0-50%` | 0 |
| `0%` | 28 |

## Notes

- ECWT math was calculated through `scripts/ecwt_core.py`; the script does not reimplement percentile or adequacy math.
- `ecwt_f` is the public value and is null unless `assess_adequacy(...).publishable` is true. Held rows retain `diagnostic_ecwt_f`, coverage, shortfall, and towers tried.
- The release is analytical and is not a Generator Owner compliance filing.
- Existing `weather.hourly_djf.obs_timestamp` is backfilled to the canonical hour where the prior loader did not retain the raw NOAA `DATE` timestamp. Future loads should populate the raw observation timestamp directly.
- Full composite hours are exposed by `calc.plant_ecwt_adr0004_composite_hour`; materialized audit rows are limited to cold-tail hours to avoid duplicating the primary-station series hundreds of millions of times.
- The cold-tail artifact is published as 10 split CSV parts; the monolithic local export is not committed because it exceeds GitHub's normal blob limit. Part checksums are listed in `data/processed/adr0004_release_20260626T235840Z_SHA256SUMS.txt`.
- Known tiny-sample ECWT anomalies are documented in `docs/findings/adr0004_tiny_sample_ecwt_anomalies.md`; the prior one-hour 88 F artifacts no longer exist in this composite run, and all remaining below-floor rows are held with null public `ecwt_f`.
