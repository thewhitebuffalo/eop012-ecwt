# Validating an ECWT Release

`scripts/validate_ecwt_release.py` checks a regenerated ECWT release CSV against
the ADR-0005 acceptance rules and prints a one-pass PASS / WARN / FAIL / INFO
readout. Use it right after a rebuild, before treating the results as good.

Standard library only — no third-party packages, no database, no network.

## Run it

```bash
python scripts/validate_ecwt_release.py \
  --results-csv data/processed/<plant_ecwt_results>.csv
```

Add the cold-tail file to also check provenance:

```bash
python scripts/validate_ecwt_release.py \
  --results-csv data/processed/<results>.csv \
  --cold-tail-csv data/processed/<cold_tail_hours>.csv
```

Exit code is **0** unless a check FAILs, in which case it is **1** (so it can gate
CI or a release step).

## What it checks

| Check | Level | Meaning |
| --- | --- | --- |
| `coverage_floor` | **FAIL** | A published row has coverage below the 95% floor. Publishing requires `>= --min-coverage` (default 0.95) of the expected winter hours populated (ADR-0005). |
| `held_rows_null` | **FAIL** | A held row (`provisional_review`, below the floor) still carries a public `ecwt_f`. Held rows must be null in the public field. |
| `plausible_ecwt` | **FAIL / WARN** | FAIL if any published ECWT is above `--fail-ecwt` (default 70 F — impossible for a winter 0.2-percentile, e.g. the old 88 F bug). WARN above `--warn-ecwt` (default 60 F — review; Hawaii/coastal sites can legitimately be high). |
| `publishable_count` | **WARN** | Fewer publishable plants than the prior run (`--prior-publishable`, default 123). A count at or below the prior usually means the fill/selection isn't assembling composites. |
| `state_range` | **INFO** | Widest and narrowest per-state ECWT ranges. Sanity expectation: **CA or AZ widest**; ND/MT/MN and FL/HI narrow. If California is narrow, station fill/selection isn't reaching its high-elevation plants. |
| `provenance` | **FAIL** | (Only when `--cold-tail-csv` is given.) A published plant has no cold-tail provenance row. |

## Options

- `--min-coverage` (default `0.95`) — the ADR-0005 publish floor.
- `--warn-ecwt` (default `60`), `--fail-ecwt` (default `70`) — winter-plausibility thresholds, in F.
- `--prior-publishable` (default `123`) — the count from the previous (pre-fix) run.

Column names are auto-detected (e.g. `ecwt_f`, `confidence_tier`/`tier`,
`plant_state`, `coverage`/`coverage_ratio`, `valid_djf_hours` + `expected_djf_hours`,
`eia_plant_code`/`plant_id`). If a coverage column is absent, coverage is derived
from valid ÷ expected hours; if neither is present, `coverage_floor` is skipped
with a WARN. The provenance check matches plant IDs across the two files, so both
should expose a comparable plant-id column.

## A good run looks like

- `coverage_floor` PASS, `held_rows_null` PASS, `plausible_ecwt` PASS.
- `publishable_count` well above 123.
- `state_range` showing CA/AZ near the top, ND/MT/MN near the bottom.
- `provenance` PASS (if checked).

`RESULT: FAIL` on any of the hard checks means the release is not ready — fix the
pipeline and re-run before publishing.
