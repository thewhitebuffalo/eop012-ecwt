# EOP-012-3 RSAW — source worksheet and field mapping

This folder holds the NERC **Reliability Standard Audit Worksheet (RSAW)** for
**EOP-012-3 — Extreme Cold Weather Preparedness and Operations**, and documents
how the dashboard's "Generate RSAW R1 worksheet" feature maps release data onto
the worksheet's Requirement R1 section.

## Source document

- [`rsaw-eop-012-3_2025_v1.docx`](rsaw-eop-012-3_2025_v1.docx) — the official RSAW
  template published by NERC (2025, v1).

NERC publishes RSAWs openly so registered entities can prepare and demonstrate
compliance; it is included here, with attribution, to support that purpose. It
is the property of the North American Electric Reliability Corporation (NERC);
all rights remain with NERC. Always confirm you are using the current version
from [nerc.com](https://www.nerc.com/) before relying on it for an engagement —
this copy is a point-in-time snapshot.

## What the dashboard generates

The detail drawer's **Generate RSAW R1 worksheet** button (see
[`viz/dashboard_template.html`](../../viz/dashboard_template.html), function
`buildRSAWDocx`) produces a self-contained, editable Word `.docx` worksheet that
pre-fills the **R1 Registered Entity Response** for a single generating unit. It covers
**Requirement R1 only** — the ECWT calculation. R2–R9 (freeze-protection
measures, Corrective Action Plans, declarations, generating-unit minimums, etc.)
require entity documentation that is outside this dataset.

The generated worksheet is **analytical** and is not, by itself, a compliance
filing. Values should be reviewed by the registered entity before submission.

## R1 field mapping

| RSAW R1 field | Source in the release data |
| --- | --- |
| Extreme Cold Weather Temperature (ECWT) | `ecwt_f` (and `ecwt_discrete_f`) |
| ECWT calculation date | parsed from the release id (`release_id` / `adr0004_run_id` timestamp) |
| Calculation method | lowest 0.2 percentile (Excel `PERCENTILE.INC` / `percentile_cont` at 0.002) of hourly dry-bulb temperatures, meteorological winter (DJF) |
| Calculation basis (period) | `coverage_basis` (e.g., fixed-period DJF since 2000-01-01 through the calc date) |
| Source(s) of temperature data | NOAA Global Hourly (Integrated Surface Database); `primary_station_id` + `primary_station_distance_km`; `contributing_towers`; `cold_tail_provenance` |
| Assembled winter-hour coverage | `valid_hour_count` / `expected_hour_count` and `coverage_ratio`; `confidence_tier`; `needs_review` |
| Adjustments for missing / invalid data (Yes/No + explanation) | `Yes` when `filled_hour_count > 0`; explanation derived from the nearest-first composite fill (`filled_hour_count`, `coverage_ratio`) |
| Registered Entity, NCR number | left blank for the Generator Owner to complete |
| Registered Entity evidence row | references `release_id` (file/source), `adr0004_run_id` (version), and the calculation date |

## Regenerating

The worksheet is built entirely in the browser from the data already embedded in
the dashboard HTML. The browser creates the WordprocessingML `.docx` package
locally — no server, no external requests. To rebuild the dashboard after
editing the template, see [`docs/REPRODUCING.md`](../REPRODUCING.md).
