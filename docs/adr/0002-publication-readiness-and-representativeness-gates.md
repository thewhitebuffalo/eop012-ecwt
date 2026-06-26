# ADR 0002: Publication Readiness And Representativeness Gates

## Status

Accepted

## Date

2026-06-25

## Context

The ECWT 0.2 percentile is a deep-tail statistic. For a 2000-2025 DJF period it is approximately the 113th coldest hour out of 56,000+ expected DJF hours. A single bad source row, a short observation period, or a distant station can materially change the result.

Earlier publication candidates could pass based on coverage denominators that did not fully represent the fixed calculation period, and station distance was visible in some diagnostics but not enforced as a publication gate.

## Decision

Automated `publication_candidate` status requires all of the following gates:

- fixed-period or fixed-composite DJF coverage ratio >= 0.95
- valid DJF hour count >= 30,000
- selected station distance <= 100 km
- selected station elevation delta <= 300 m when an elevation delta is available
- selected station metadata must not begin after 2000-01-01 for a fixed-period single-station publication candidate
- station-local DJF time basis from ADR 0001

Rows that fail any gate must not be exported as ordinary publication candidates. They remain auditable with reason codes such as:

- `fixed_period_coverage_below_threshold`
- `valid_hours_below_threshold`
- `station_distance_exceeds_representativeness_gate`
- `station_elevation_delta_exceeds_representativeness_gate`
- `station_starts_after_fixed_period_start`

## Station Segmentation Trigger

Station segmentation or documented secondary-station fill is required when the nearest representative station does not cover the fixed calculation period well enough, including when:

- the selected station starts after 2000-01-01
- fixed-period coverage is below 0.95
- station distance exceeds 100 km and no nearer adequate station exists
- station elevation delta exceeds 300 m and the difference could affect cold-tail representativeness

Segmentation must record each station, date span, reason code, and whether the segment is algorithmic or manually reviewed. A distant station may not be substituted merely because it produces a complete or colder ECWT.

## Consequences

This policy will block many rows that previously appeared publication-ready. That is the correct outcome: they may still be useful analytical rows, but they are not suitable for a compliance-facing national release without additional station review, missing-hour treatment, or segmentation.

The 100 km and 300 m thresholds are conservative automated gates, not proof that every station inside the threshold is representative. Plant-owner review may still reject a nearby station because of topography, large water bodies, siting, or known local climate effects.
