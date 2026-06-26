# Finding: Insufficiency of Raw NOAA Dry-Bulb Data for National ECWT

Status: Recorded finding (whitepaper source)
Date: 2026-06-26

## Purpose

This memo consolidates, in one citable location, the project's finding that **raw
NOAA Global Hourly dry-bulb temperature data is insufficient — in both integrity
and completeness — to compute a compliance-grade Extreme Cold Weather Temperature
(ECWT) for the U.S. generating-plant fleet from station observations alone.**

It is intended as a stable reference for a forthcoming whitepaper. The underlying
evidence is distributed across the methodology, the architecture decision records,
and several status reports; this document states the finding and points to that
evidence. Quantitative figures below are from the runs cited in
`docs/noaa_hardened_load_and_provisional_ecwt_status.md` and
`docs/noaa_parallel_download_and_djf_load_status.md`; exact values are reproducible
from the recorded calculation-run IDs.

## Why ECWT is sensitive to data quality and completeness

EOP-012 defines ECWT as the 0.2 percentile of hourly dry-bulb temperatures in
December, January, and February from 2000-01-01 through the calculation date. For a
full 2000-present DJF period that is roughly the **113th-coldest hour out of
~56,000** expected hours. Two consequences follow:

- **Integrity sensitivity.** A single erroneous cold-tail observation can move the
  0.2 percentile by several degrees. The statistic is defined precisely on the part
  of the distribution most exposed to bad data.
- **Completeness sensitivity.** A defensible percentile requires a near-complete,
  long hourly record. Sparse or short records make the tail unstable and the result
  unreproducible.

## Finding 1 — Integrity defects in raw NOAA Global Hourly dry-bulb rows

NOAA Global Hourly (ISD-derived) rows are not uniform-quality evidence:

- **Implausible `SOURCE=7` temperatures.** A QA probe found `SOURCE=7` rows whose
  `TMP` field is Fahrenheit-like / physically impossible — e.g. station
  `720267-23224` (Auburn Municipal Airport, KS) reporting `TMP` of **55.0 C and
  56.0 C in February 2025**, with a Fahrenheit-like `REM` field. Parsed as the
  documented tenths-of-degrees-C, such rows silently corrupt the cold tail.
- **Sentinels and quality flags.** `TMP` sentinels (`+9999`, `-9999`, `9999`),
  malformed values, and TMP quality code `9` must be excluded; suspect/erroneous
  quality codes degrade reliability.
- **Duplicate and excess station-hour observations** require a deterministic
  ranking rule, or the same hour can be represented by conflicting values.

**Mitigation in place.** The canonical loader now rejects `SOURCE=7` before parsing
`TMP`, applies a physical/climatological plausibility window (publication QA window
-65 C to 40 C, with a SHEF-specific floor of -50 C), ranks duplicate station-hours
deterministically (TMP quality rank, FM report type, SOURCE rank, minute closest to
56), and preserves rejected-row counts as load-file evidence. In the hardened reload,
**9,958,996 SOURCE rows were rejected** before they could contribute to ECWT. This
policy is recorded in `docs/methodology.md` ("NOAA Source Quality Policy") and
`docs/adr/0003-export-context-precision-and-source-quality.md`.

## Finding 2 — The observational network is too incomplete for a national census

Hardened loading does not solve coverage. After loading 4,000 station-source files
into the canonical table (~1.89M valid DJF hours across 2,012 stations):

- **Only 175 of 4,000 station-years were "complete";** 3,774 were partial and 51
  empty.
- The public NOAA AWS backfill is far from finished: **4,521 station-years
  downloaded, 2,479 HTTP-404 (absent upstream), and 79,839 still planned.**
- The publication gates (`docs/adr/0002-...`) require **>=0.95 fixed-period DJF
  coverage, >=30,000 valid DJF hours, a station <=100 km away, and <=300 m elevation
  delta**, with the station not beginning after 2000-01-01 for a single-station
  fixed-period candidate.

The structural problem: **most of the ~16,132 EIA-860 plants have no weather station
within 100 km that holds a 95%-complete hourly DJF record across all 26 winters
since 2000.** This is not primarily a backfill-progress issue. It is a property of
the observational network — stations are spatially sparse in many regions, have
outages and gaps, and frequently begin after 2000. Completing the backfill raises
coverage but cannot make a complete 26-winter record exist where stations never
recorded one.

## Consequence

Computing a national ECWT census from raw NOAA station observations alone forces an
unacceptable choice:

- **Relax the denominator** (score coverage only against station-years that happen
  to be loaded) — which produces deceptively high "coverage" and over-includes
  plants, exactly the artifact this project removed; or
- **Apply honest fixed-period gates** — which correctly block the large fraction of
  plants that lack adequate nearby observations, leaving the national census
  incomplete.

Neither yields a complete, compliance-grade, auditable ECWT for every plant from raw
station data.

## Implication for methodology

This finding motivates a tiered, provenance-tagged weather-source hierarchy in which
gap-free, version-controlled gridded reanalysis (bias-corrected to the nearest
reliable station) serves as an auditable backstop for plants without adequate station
coverage, while pure-observation and documented-composite station series remain the
preferred tiers. That design decision is to be recorded separately (planned
`docs/adr/0004`) and is the subject of the forthcoming whitepaper. A built-in
validation — comparing station-derived ECWT against bias-corrected reanalysis ECWT
where both exist — is the evidence basis for the backstop tier.

## References

- `docs/methodology.md` — Standards Basis, NOAA Source Quality Policy, gates
- `docs/adr/0002-publication-readiness-and-representativeness-gates.md`
- `docs/adr/0003-export-context-precision-and-source-quality.md`
- `docs/noaa_hardened_load_and_provisional_ecwt_status.md` — hardened-load and coverage figures
- `docs/noaa_parallel_download_and_djf_load_status.md` — original `SOURCE=7` discovery
- NOAA Integrated Surface Database (ISD) / Global Hourly format documentation (`TMP`, `SOURCE`, quality codes)
- NERC EOP-012-3 R1, NAGF guidance "Determining Extreme Cold Weather Temperature"
