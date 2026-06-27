# ADR-0004 ECWT Status

- ADR-0004 run ID: `plant_ecwt_adr0004_20260626T235840Z`
- Release ID: `scoped_plant_ecwt_adr0004_release_20260626T235840Z`
- Station candidate run ID: `noaa_station_candidates_20260625T065445Z`
- Calculation date: `2025-03-01`
- Expected DJF hours: `55584`
- Git commit: `30e4e223bbc0f2c7a693962aafc01205042a02da-dirty`
- Release CSV: `/Users/Shared/EOP012/rebuild/data/processed/scoped_plant_ecwt_adr0004_release_20260626T235840Z.csv`
- Release CSV SHA-256: `8c10fdb3e33d6d332e372790ae99d3ed70cc56cdca5f70dacc9b7d463a68b246`
- Published checksum file: `data/processed/adr0004_release_20260626T235840Z_SHA256SUMS.txt`

## Counts

| Metric | Count |
| --- | ---: |
| Result rows | 15975 |
| Rows with ECWT | 15947 |
| Cold-tail rows | 464239 |
| Plants with cold-tail rows | 15947 |
| Unexpected null ECWT rows | 0 |

## Confidence Split

| Tier | Plants |
| --- | ---: |
| `complete` | 3 |
| `adequate` | 120 |
| `provisional_review` | 15824 |
| `blocked_no_data` | 28 |

## Notes

- ECWT math was calculated through `scripts/ecwt_core.py`; the script does not reimplement percentile or adequacy math.
- The release is analytical and is not a Generator Owner compliance filing.
- Existing `weather.hourly_djf.obs_timestamp` is backfilled to the canonical hour where the prior loader did not retain the raw NOAA `DATE` timestamp. Future loads should populate the raw observation timestamp directly.
- Full composite hours are exposed by `calc.plant_ecwt_adr0004_composite_hour`; materialized audit rows are limited to cold-tail hours to avoid duplicating the primary-station series hundreds of millions of times.
- The cold-tail artifact is published as four CSV parts because the original monolithic export is `102562323` bytes, above GitHub's normal blob limit. The original monolithic SHA-256 is `ea3e063777f95663b3c7e32d3625f2ec5d5678670538b96dbef6565ba833e9f1`; the part checksums are listed in `data/processed/adr0004_release_20260626T235840Z_SHA256SUMS.txt`.
- Known tiny-sample ECWT anomalies are documented in `docs/findings/adr0004_tiny_sample_ecwt_anomalies.md`.
