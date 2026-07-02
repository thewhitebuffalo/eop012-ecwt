# Validating an ECWT Release

`scripts/validate_ecwt_release.py` checks a regenerated ECWT release CSV against
the ADR-0006 acceptance rules and prints a one-pass PASS / WARN / FAIL / INFO
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

For promoted releases, run the validator against the scoped release CSV so the
release-row provenance checks can inspect `cold_tail_provenance`. Pass the split
cold-tail parts too when checking materialized per-hour provenance coverage:

```bash
python scripts/validate_ecwt_release.py \
  --results-csv data/processed/scoped_plant_ecwt_adr0006_release_<ts>.csv \
  --cold-tail-csv data/processed/plant_ecwt_adr0006_<ts>_cold_tail_hours_part*.csv
```

Exit code is **0** unless a check FAILs, in which case it is **1** (so it can gate
CI or a release step).

## What it checks

| Check | Level | Meaning |
| --- | --- | --- |
| `coverage_floor` | **FAIL** | A published row has coverage below the 95% floor. Publishing requires `>= --min-coverage` (default 0.95) of the expected winter hours populated. |
| `held_rows_null` | **FAIL** | A held row (`provisional_review`, below the floor) still carries a public `ecwt_f`. Held rows must be null in the public field. |
| `plausible_ecwt` | **FAIL / WARN** | FAIL if any published ECWT is above `--fail-ecwt` (default 70 F — impossible for a winter 0.2-percentile, e.g. the old 88 F bug). WARN above `--warn-ecwt` (default 60 F — review; Hawaii/coastal sites can legitimately be high). |
| `marine_low_outlier` | **FAIL** | A published plant is at least `--low-side-warn` F below its state median and more than `--marine-tail-fail-share` of its cold tail comes from excluded marine-platform stations. This is the issue #36 failure class. |
| `state_low_outlier` | **WARN** | A published plant is at least `--low-side-warn` F below its state median; review representativeness even when marine-platform dominance is absent. |
| `tail_dominated_non_primary` | **WARN** | A single non-primary station contributes more than `--single-station-tail-warn-share` of a plant's cold tail. |
| `publishable_count` | **WARN** | Fewer publishable plants than the prior run (`--prior-publishable`, default 123). A count at or below the prior usually means the fill/selection isn't assembling composites. |
| `state_range` | **INFO** | Widest and narrowest per-state ECWT ranges. Sanity expectation: **CA or AZ widest**; ND/MT/MN and FL/HI narrow. If California is narrow, station fill/selection isn't reaching its high-elevation plants. |
| `provenance` | **FAIL** | (Only when `--cold-tail-csv` is given.) A published plant has no cold-tail provenance row. |

## Options

- `--min-coverage` (default `0.95`) — the publish floor.
- `--warn-ecwt` (default `60`), `--fail-ecwt` (default `70`) — winter-plausibility thresholds, in F.
- `--low-side-warn` (default `10`) — state-median low-side review threshold, in F.
- `--marine-tail-fail-share` (default `0.50`) — marine-platform cold-tail share that turns a low-side outlier into a FAIL.
- `--single-station-tail-warn-share` (default `0.80`) — non-primary station cold-tail dominance threshold.
- `--min-state-peers` (default `5`) — minimum published rows before a state median is used.
- `--prior-publishable` (default `123`) — the count from the previous (pre-fix) run.

Column names are auto-detected (e.g. `ecwt_f`, `confidence_tier`/`tier`,
`plant_state`, `coverage`/`coverage_ratio`, `valid_djf_hours` + `expected_djf_hours`,
`eia_plant_code`/`plant_id`). If a coverage column is absent, coverage is derived
from valid ÷ expected hours; if neither is present, `coverage_floor` is skipped
with a WARN. Slightly over-complete coverage ratios are treated as complete. The
provenance check matches plant IDs across the result file and one or more cold-tail
files, so both should expose a comparable plant-id column.

## A good run looks like

- `coverage_floor` PASS, `held_rows_null` PASS, `plausible_ecwt` PASS.
- `marine_low_outlier` PASS.
- `publishable_count` well above 123.
- `state_range` showing CA/AZ near the top, ND/MT/MN near the bottom.
- `provenance` PASS (if checked).

`RESULT: FAIL` on any of the hard checks means the release is not ready — fix the
pipeline and re-run before publishing.
