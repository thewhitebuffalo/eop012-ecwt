# Finding: ADR-0004 Tiny-Sample ECWT Anomalies

Status: Diagnostic finding; do not publish affected ECWT rows as final values
Date: 2026-06-27

## Purpose

This memo records a diagnostic failure found in the local ADR-0004 rebuild run:

- ADR-0004 run ID: `plant_ecwt_adr0004_20260626T235840Z`
- Local release ID: `scoped_plant_ecwt_adr0004_release_20260626T235840Z`
- Local release SHA-256: `8c10fdb3e33d6d332e372790ae99d3ed70cc56cdca5f70dacc9b7d463a68b246`

The run has **not** been published as a GitHub release or committed CSV. The
diagnostic finding is being published so the failure is visible before any
ADR-0004 release is promoted.

## Finding

The local ADR-0004 release file includes ECWT values for plants whose selected
weather station has only one or a few valid DJF observations. Those values are
not defensible ECWTs. They are sparse-sample artifacts: with one valid hour, the
0.2-percentile ECWT is simply the only observed temperature.

The issue was first observed around Texas Solar Nova 1 and Post Wind Farm LP:

| Plant | State | Station | Station name | Valid DJF hours | ECWT F | Tier |
| --- | --- | --- | --- | ---: | ---: | --- |
| Post Wind Farm LP | TX | `747350-99999` | JAYTON TX | 1 | 88.2 | `provisional_review` |
| Texas Solar Nova 1 | TX | `747350-99999` | JAYTON TX | 1 | 88.2 | `provisional_review` |

For station `747350-99999`, the cold-tail provenance resolves to a single
loaded NOAA Global Hourly row:

| Field | Value |
| --- | --- |
| Hour ending | `2007-01-26 13:00:00-08` |
| Dry bulb | `88.16 F` |
| Source channel | `noaa_global_hourly_aws` |
| NOAA source code | `4` |
| Report type | `FM-12` |
| Source file ID | `noaa_global_hourly_csv_2007_74735099999_25e6136f7a24531c` |

That one observation was enough for the current implementation to compute and
export `88.2 F`. That is a calculation-layer failure, not a valid cold-weather
result.

## Scope of the anomaly

Diagnostic counts from the local ADR-0004 release:

| Metric | Count |
| --- | ---: |
| Total rows | 15,975 |
| Rows with non-null ECWT | 15,947 |
| `complete` rows | 3 |
| `adequate` rows | 120 |
| `provisional_review` rows | 15,824 |
| `blocked_no_data` rows | 28 |
| Rows with exactly 1 valid DJF hour | 129 |
| Rows with ECWT `> 80 F` | 23 |
| Rows with ECWT `> 60 F` | 88 |

All 23 ECWT values above `80 F` are based on exactly one valid DJF hour. Among
rows with ECWT above `60 F`, the median valid-hour count is one.

The high-ECWT anomalies are concentrated in a small number of sparse stations:

| Condition | Stations | Plants | Dominant sparse stations |
| --- | ---: | ---: | --- |
| ECWT `> 80 F` | 2 | 23 | `747350-99999`, `745000-99999` |
| ECWT `> 60 F` | 16 | 88 | `747350-99999`, `721038-99999`, `725010-99999`, `911690-99999` |
| Exactly 1 valid DJF hour | 20 | 129 | `725860-99999`, `747350-99999`, `721038-99999`, `725010-99999` |

By contrast, the `complete` and `adequate` rows do not exhibit this high-ECWT
artifact:

| Tier group | Rows with ECWT | Max ECWT F | Min valid DJF hours |
| --- | ---: | ---: | ---: |
| `complete` + `adequate` | 123 | 20.5 | 47,499 |
| `provisional_review` | 15,824 | 88.2 | 1 |

## Root cause

The failure has three layers.

First, primary station selection currently accepts the nearest station with any
loaded DJF data. In `scripts/rebuild_adr0004_ecwt_layer.py`, the candidate filter
uses `sy.valid_djf_hours > 0`. This admits stations with only one valid hour.

Second, `scripts/ecwt_core.py::assess_adequacy()` intentionally blocks only
zero-data series. Any non-empty series receives an ECWT and a confidence tier.
That implementation matches the literal wording of ADR-0004's provisional tier,
but it is too permissive for release semantics.

Third, the export writes `ecwt_f` for all nonzero-data rows, including
`provisional_review`. This makes a diagnostic placeholder look like a publishable
plant ECWT unless the consumer notices the confidence tier and valid-hour count.

## Interpretation

The local ADR-0004 CSV should be treated as a diagnostic artifact, not a
publishable ECWT release. A row with one valid hour can be traceable and still be
analytically invalid. Provenance answers "where did this number come from"; it
does not make a one-hour percentile meaningful.

The wording "every plant with any valid DJF data receives an ECWT value" is unsafe
without an additional publication boundary. ADR-0004's `provisional_review` tier
cannot be allowed to put sparse-sample artifacts into the same `ecwt_f` field used
for complete or adequate results.

## Required follow-up before publication

Before any ADR-0004 ECWT dataset is published:

1. Define a minimum evidence floor for station selection and/or ECWT emission.
   The current `valid_djf_hours > 0` filter is invalid for a 0.2-percentile
   statistic.
2. Separate diagnostic estimates from publishable ECWT values. Complete and
   adequate rows can populate the public ECWT field; sparse provisional rows
   should either be null in the public ECWT field or explicitly exported as
   diagnostic-only values.
3. Refine primary station choice so a one-hour nearest station cannot beat a
   slightly farther station with thousands of valid DJF hours.
4. Add sanity checks that fail the run when high ECWT values are paired with tiny
   sample sizes, including at least:
   - no published ECWT with `valid_hour_count = 1`
   - no published ECWT above a plausible regional threshold without adequate
     valid-hour evidence
   - tier counts and valid-hour distributions printed in the run summary
5. Re-run ADR-0004 after the publication boundary is corrected, then regenerate
   the release export and visualization.
