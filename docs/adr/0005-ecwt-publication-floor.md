# ADR 0005: ECWT Publication Floor — Populate All Winter Hours, Publish at >= 95% Coverage

## Status

Accepted

## Date

2026-06-27

## Context

The first ADR-0004 rebuild produced impossible results — e.g. an ECWT of 88 F at
JAYTON TX — because a value was computed from a single recorded winter hour. The
diagnosis is recorded in `docs/findings/adr0004_tiny_sample_ecwt_anomalies.md`:
station selection accepted any station with more than zero loaded hours,
`assess_adequacy` blocked only zero-data, and the export wrote `ecwt_f` for every
non-empty row. 23 published values exceeded 80 F, all from exactly one valid hour.

ADR-0004's wording — *"every plant with any valid DJF data receives an ECWT value
and a confidence tier; only zero-data is blocked"* — was too permissive and is
hereby void.

NERC defines the ECWT as the lowest 0.2 percentile of the hourly winter
(December/January/February) temperatures since 2000-01-01. That number is only
meaningful, and only auditable, when the winter record is essentially complete. A
value built from a handful of hours is not a valid ECWT.

## Decision

For every plant:

1. **Goal: populate all expected winter hours** — every hour of December, January,
   and February from 2000-01-01 through the calculation date (~55,000 hours).
   **Every hour counts equally.** There is no time-of-day weighting and no
   assumption that any hour is "too warm to matter": a cold snap can make any
   hour, midday included, the coldest of its day.

2. **Build the record by filling outward from towers.** Start with the closest
   representative tower; pull its winter hours; fill every still-missing hour from
   the next-closest representative tower; repeat outward. A tower's real reading is
   never overwritten. Each hour keeps its provenance (tower, date/time,
   temperature, source) per ADR-0004.

3. **Publish floor (95%).** An ECWT is published only when at least **95%** of the
   expected winter hours are populated:
   - `complete` (>= 99% populated) and `adequate` (>= 95%) → **published**:
     `ecwt_f` is written to the public field.
   - `provisional_review` (< 95%) → **held**: no value in the public `ecwt_f`
     field; the diagnostic value, the coverage, and the shortfall (hours short,
     towers tried) are still recorded.
   - `blocked_no_data` (no hours) → blocked.

4. **The ECWT** is the lowest 0.2 percentile (≈ the 110th-coldest of ~55,000) of
   the populated set, computed via `scripts/ecwt_core.py` (`ecwt_percentile`).

5. **Station selection** must not let a near-empty nearest tower outrank a farther
   tower that yields a fuller record. Selection is judged on the record a tower (or
   composite) can actually produce, not on raw distance to a tower with almost no
   data.

6. **Run-fail sanity checks** (the regenerate must hard-fail, not merely report):
   - no published `ecwt_f` from coverage below the 95% floor;
   - no held / `provisional_review` row carrying a public `ecwt_f`;
   - the coverage distribution and tier counts are printed in the run summary.

## Consequences

- The tiny-sample artifacts become impossible: at >= 95% of ~55,000 hours, an 88 F
  winter 0.2-percentile cannot occur.
- "Coverage" now means real, fillable winter hours — not a relaxed denominator.
  With the full NOAA dataset loaded on the build machine, most sites should reach
  >= 95% via tower fill; genuinely isolated sites are honestly **held** with a
  documented reason rather than given a fabricated number.
- `scripts/ecwt_core.py::assess_adequacy` enforces the floor (it returns
  `coverage` and `publishable`; `MIN_PUBLISH_COVERAGE = 0.95`,
  `COMPLETE_COVERAGE = 0.99`). `tests/test_ecwt_core.py` covers the floor,
  including the held one-reading case.
- Per-hour provenance (ADR-0004) is retained: the coldest ~100 hours that set each
  published ECWT remain individually traceable to a tower, time, and source.
- This supersedes the permissive publication wording in ADR-0004.
