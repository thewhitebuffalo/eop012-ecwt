# ADR 0004: Observational Source Hierarchy, Standard-Aligned Adequacy, and Per-Hour Audit Trail

## Status

Proposed

## Date

2026-06-26

## Context

Two source documents were read in full for this decision: the EOP-012-3
Technical Rationale (Project 2024-03, March 2025) and the companion "Calculating
Extreme Cold Weather Temperature" (December 2024). Together they establish that
the standard's ECWT method is:

- **Observational.** Temperatures are "measured" from a "recording location."
  Every named source is a weather-station network (NWS, NOAA, FAA/ASOS, ECCC) or
  NOAA Climate Data Online / Local Climatological Data. Reanalysis or modeled
  gridded data is never contemplated.
- **Tolerant of missing data, by documentation rather than a threshold.** The SDT
  "chose not to establish a requirement regarding the size of the data set." The
  percentile is robust to missing hours *above* the ECWT; only missing hours *at
  or below* the cold tail can move it. Where a single station is incomplete, the
  prescribed remedy is to **append nearby stations / combine NOAA and ASOS** and
  **document** the approach.

This supersedes the assumption (explored in ADR-0002) that a rigid 0.95 / 30,000-
hour gate is required. Those gates are stricter than the standard; treating them
as a hard block under-covers the fleet for a reason the standard does not impose.

The project also recorded a separate finding that raw NOAA Global Hourly data has
integrity defects (e.g. `SOURCE=7` Fahrenheit-like values) — see
`docs/findings/noaa_dry_bulb_data_integrity.md`. Catching such defects and
defending any composite series both require **per-hour provenance**.

## Decision

### 1. Observational-only source hierarchy

ECWT is computed from observed station data only. There is **no reanalysis /
modeled-data tier**. The hierarchy, in preference order, is:

1. **Single representative station** passing the high-confidence gates.
2. **Documented composite** — the primary station's missing hours filled from the
   nearest representative fallback station(s) and/or NOAA+ASOS combination, per
   the standard's prescribed remedy. The primary station is never overwritten.

(Reanalysis is explicitly out of scope. If ever revisited, it would be a separate
ADR and labeled non-observational; it is not part of this build.)

### 2. Adequacy as a confidence model, not a rigid gate

Every plant with any valid DJF data receives an ECWT value and a **confidence
tier**; only zero-data is blocked. Tiers (defaults, tunable):

| Tier | Meaning |
| --- | --- |
| `complete` | near-complete observed coverage (the former high-confidence gate) |
| `adequate` | missing hours present but the cold tail is populated and the missing fraction is within the adequate band |
| `provisional_review` | missing fraction high enough that missing hours could fall at/below the ECWT; confirm against the gap calendar |
| `blocked_no_data` | no valid DJF hours; reason-coded |

The authoritative adequacy question is the standard's: *could the missing hours
have fallen at or below the ECWT?* The automated tier is a coarse proxy
(`scripts/ecwt_core.py: assess_adequacy`); the precise check is refined downstream
against the per-plant gap calendar (which needs the actual missing timestamps).

The expected-hours denominator is the fixed DJF calendar period from 2000-01-01
through the calculation date (`expected_djf_hours`), which reproduces the
companion document's worked example (`2024-03-01 -> 53,424`).

### 3. ECWT statistic

`ecwt_f = percentile_cont(0.002)` over the composite DJF dry-bulb series, equal to
Excel `PERCENTILE.INC(range, 0.002)`; plus `ecwt_discrete_f` at discrete cold rank
`ceil(0.002 * n)`. Published to 0.1 F (ADR-0003). Implemented and unit-tested in
`scripts/ecwt_core.py` (`tests/test_ecwt_core.py`).

### 4. Per-hour audit trail (provenance)

Every canonical DJF hour — and every hour in the composite series the percentile
is computed on — carries:

- **Tower number:** `station_id` (e.g. USAF-WBAN `720267-23224`).
- **Date/time:** `hour_ending_utc` (canonical de-dup key) + `hour_local` (DJF
  basis, ADR-0001) + raw `obs_timestamp`.
- **Source:** `source_channel` (enum, e.g. `noaa_global_hourly_aws`,
  `noaa_lcd_cdo`, `asos_iem`) + NOAA ISD `source_code` (e.g. 4, 7) + `report_type`
  (e.g. FM-15) + `source_file_id` → `audit.source_file` (SHA-256 + load run + git
  commit).

For composites each hour keeps its **own** tower and source, so the published
per-plant evidence reports the contributing towers/sources and date ranges, and
specifically the **provenance of the cold-tail hours (<= ECWT) that set the
value** (`provenance_summary`). Provenance is stored as compact keys/enums/FKs,
not free text.

### 5. Implementation contract (kept token-lean for the executing model)

- **Pure core is provided and tested.** `scripts/ecwt_core.py` ships the percentile,
  discrete rank, expected-hours, adequacy, composite-builder, and
  provenance-summary functions with passing unit tests. The implementer wires
  these to Postgres; it does not re-derive them.
- **Schema additions:** per-hour provenance columns above on the canonical and
  composite-series tables; `confidence_tier`, `needs_review`, and the reason codes
  on the plant ECWT result.
- **Incremental + idempotent:** process only new station-years against a load
  ledger; never full-reload.
- **No report churn:** a single overwritten summary table + one rolling status
  doc replace per-run timestamped reports; scripts print terse counts, not table
  dumps. (The prior iterative/exploratory approach and per-run report churn were
  the dominant token cost; this design removes both.)
- **Deprecated diagnostics removed:** normalized active-window scenarios are not a
  publication path (already diagnostics-only in the methodology).

## Consequences

- The fleet is covered with **observational** ECWT values aligned to the standard;
  the coverage gap created by a stricter-than-standard gate closes without adding
  a non-observational data source.
- Every published ECWT hour is traceable to a checksummed source file, and the
  cold-tail provenance is explicit — the core audit and whitepaper artifact.
- ADR-0002's gates are retained as the `complete` (high-confidence) tier rather
  than a global block; `adequate` and `provisional_review` extend coverage with
  documented confidence, consistent with the standard's documentation-based
  adequacy.
- A later unit-level compliance layer and any Generator-Owner-specific station
  selection remain downstream; this is the national analytical layer.
