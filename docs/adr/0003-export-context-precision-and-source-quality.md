# ADR 0003: Export Context, Precision, And Source Quality

## Status

Accepted

## Date

2026-06-25

## Context

Plant-level ECWT exports were previously easy to misread as compliance-ready final values because the CSV emphasized plant, station, ECWT, and coverage fields without carrying enough row-level caveat text. Some exports also displayed ECWT to three decimal places even though NOAA Global Hourly `TMP` values are parsed from tenths of degrees C.

That creates two avoidable review risks:

- a downstream user can separate a row from the methodology document and lose the denominator, representativeness, and compliance-use caveats
- three-decimal Fahrenheit display precision implies more source precision than the NOAA temperature field supports

## Decision

Publication-facing ECWT exports must carry row-level context fields:

- `coverage_basis`
- `ecwt_precision_basis`
- `selected_station_representativeness_basis` when the export has a selected or composite station basis
- `publication_caveat`

Publication-facing ECWT values are displayed to 0.1 F. The database may retain higher-precision numeric calculation results for reproducibility and sensitivity checks, but exported preview and release CSVs should not display spurious precision.

Export caveats must state that project output is analytical and is not a Generator Owner EOP-012 compliance filing input without station representativeness review and source QA acceptance.

The source-quality policy used by the loader and QA report must be documented in methodology text. At minimum, that documentation must identify:

- NOAA `TMP` sentinel and quality-code rejection rules
- configured NOAA `SOURCE` rejection codes
- duplicate station-hour ranking rules
- plausibility temperature bounds
- SHEF-specific cold-row guardrail

## Consequences

CSV consumers can see the calculation denominator basis, precision basis, and compliance-use caveat without joining to a separate report.

Rounding exported values to 0.1 F can make two records with slightly different internal percentile values display identically. That is acceptable because the displayed CSV is a publication artifact, not the only audit record. Run IDs and source lineage still allow the exact numeric database result to be reproduced when needed.
