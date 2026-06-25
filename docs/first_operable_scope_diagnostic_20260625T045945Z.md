# First-Operable Scope Diagnostic

Generated UTC: 2026-06-25T04:59:45Z

## Scope Rule

The documented first ECWT plant scope is plants with at least one EIA-860
generator status in:

- `OP`
- `SB`
- `OA`
- `OS`

This report compares that first-operable scope with the current all-plant
fixed-period readiness run.

## Current Counts

| Population | Plants | Publication candidates | Blocked |
| --- | ---: | ---: | ---: |
| First-operable scope | 13,370 | 144 | 13,226 |
| Outside first-operable scope | 2,762 | 18 | 2,744 |
| All plant readiness rows | 16,132 | 162 | 15,970 |

## Candidate Exports

| Export | Scope | Rows |
| --- | --- | ---: |
| `plant_ecwt_publication_candidates_20260625T043628Z.csv` | all readiness publication candidates | 162 |
| `plant_ecwt_publication_candidates_first_operable_20260625T045722Z.csv` | first-operable publication candidates | 144 |

The scoped export uses `--plant-scope first-operable` and includes generator
status/count/capacity columns so the scope decision is visible in the CSV.

## Open Upstream Plant-Universe Exception

One operable generator plant code is present in `asset.generator` but absent
from `asset.plant`:

| EIA plant code | Generator | Status | Utility | Technology | Nameplate MW |
| --- | --- | --- | --- | --- | ---: |
| `68815` | `GAPPV` | `OP` | Google, Inc. | Solar Photovoltaic | 0.9 |

This is already logged in `audit.exception_log`:

- Calculation run ID: `eia860_2024_asset_load_20260623T202109Z`
- Entity: `eia860:2024:generator:operable:68815:GAPPV`
- Severity: `error`
- Reason code: `generator_plant_code_not_in_plant_table`
- Resolution status: `open`

Because there is no plant row, this generator cannot currently enter plant
station-candidate generation or plant ECWT readiness.

## Interpretation

The full plant readiness table remains useful for audit and diagnostics, but
the first publication-candidate export should use the first-operable scope until
a broader publication policy is explicitly approved.

The remaining first-operable blocker count is 13,226. These are not NOAA AWS
download blockers under the corrected inventory; they are fixed-period coverage,
station-selection, and methodology-policy blockers.
