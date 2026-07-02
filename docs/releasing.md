# Publishing an ECWT release

Per-run outputs are large (~500 MB) and regenerate on every run, so the data
is published as **assets on a tagged GitHub Release**, never committed
(`data/processed/*.csv` is git-ignored). The repository carries the code, the
docs, the SHA-256 manifest, and the built dashboard.

## Convention

- **Tag name:** `ecwt-adr0004-<ts>` where `<ts>` is the run timestamp shared by
  the run id and release id (example: `ecwt-adr0004-20260626T235840Z`).
- **Release title:** `ADR-0004 ECWT Release <ts>` (bump the ADR label when the
  governing methodology changes).
- **Assets** (all produced by the release build step):
  - `scoped_plant_ecwt_*_release_<ts>.csv` — the audit record: per-plant ECWT + provenance
  - `plant_ecwt_*_<ts>_results.csv` — full results table
  - `plant_ecwt_*_<ts>_sources.csv` — source/lineage table
  - `plant_ecwt_*_<ts>_cold_tail_hours_part*.csv` — per-hour cold-tail provenance, split under GitHub's 2 GB/asset and repo 100 MB blob limits
  - `*_SHA256SUMS.txt` — the manifest (also committed under `data/processed/`)
- **Release notes:** link the validator output summary and the ADR(s) in force.

## Commands

With the [GitHub CLI](https://cli.github.com/):

```bash
TS=20260626T235840Z
TARGET_COMMIT=87c447b877e9f172d3a8a0cb5b36258147c3e323
gh release create "ecwt-adr0004-$TS" \
  --target "$TARGET_COMMIT" \
  --title "ADR-0004 ECWT Release $TS" \
  --notes "ADR-0005 publication floor in force. Validator: PASS. See docs/adr/." \
  data/processed/scoped_plant_ecwt_adr0004_release_${TS}.csv \
  data/processed/plant_ecwt_adr0004_${TS}_results.csv \
  data/processed/plant_ecwt_adr0004_${TS}_sources.csv \
  data/processed/plant_ecwt_adr0004_${TS}_cold_tail_hours_part*.csv \
  data/processed/adr0004_release_${TS}_SHA256SUMS.txt
```

Add assets to an existing release with `gh release upload <tag> <files...>`.

## Manifest policy

The `*_SHA256SUMS.txt` manifest covers the **immutable data CSVs only**. It
must not contain a hash for `build/EOP012_*_dashboard.html`: the dashboard is
a living UI artifact rebuilt for template changes unrelated to the data, so a
manifest entry for it goes stale immediately. CI rejects manifests that
reference `build/`. The dashboard's integrity anchor is the checksummed scoped
release CSV embedded inside it.

## Verifying a download

```bash
sha256sum -c adr0004_release_<ts>_SHA256SUMS.txt --ignore-missing
```

(Windows: `CertUtil -hashfile <file> SHA256` and compare.)

## Checklist

1. `validate_ecwt_release.py` reports no FAIL.
2. Manifest built; covers every data CSV; no `build/` entries.
3. Tag + Release created; all assets attached; sizes sane.
4. Manifest committed under `data/processed/`.
5. Dashboard rebuilt from the scoped CSV and committed (Pages deploys it).
6. Spot-check one asset download against the manifest.
