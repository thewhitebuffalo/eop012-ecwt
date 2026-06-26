# Publication Plan

## Goal

Publish a reproducible, auditable ECWT dataset for U.S. generating plants. The public repository should let a reviewer trace each published ECWT value back to its asset source, weather source, station-selection decision, hourly coverage check, calculation method, code version, and release bundle checksum.

This repository is the audit/control plane. It is not the storage location for hundreds of gigabytes of hourly weather observations.

## Storage Boundaries

| Layer | Location | Published in Git? | Notes |
| --- | --- | --- | --- |
| Code, SQL, docs, methodology | GitHub repo | Yes | Primary public audit surface. |
| Small QA reports and manifests | GitHub repo | Yes | CSV/Markdown/JSON should stay small and reviewable. |
| Raw EIA ZIPs | Local raw intake, upstream EIA URLs | No | Publish URL, retrieval date, size, and SHA-256. |
| Raw NOAA hourly files/cache | `/Volumes/NOAA_CACHE` and upstream NOAA URLs | No | Publish source manifests and hashes where practical. |
| Working Postgres database | `/Volumes/NOAA_CACHE/EOP012` | No | Rebuildable local/CI artifact, not a Git artifact. |
| Release data bundles | GitHub Releases or external object storage | Not in repo history | Use split compressed Parquet/CSV bundles plus checksums. |
| Timestamped run products | Local `docs/`, `data/processed/`, or staging roots | No | CSVs, JSON manifests, and per-run reports are regenerated locally or attached to a release bundle. |

## Release Structure

Use explicit release names:

```text
vYYYY.MM.DD-asset-inventory
vYYYY.MM.DD-ecwt-alpha
vYYYY.MM.DD-ecwt-national
```

Each ECWT release should include:

- `README.md`
- `METHODOLOGY.md`
- `DATA_DICTIONARY.md`
- `SOURCE_MANIFEST.csv`
- `SHA256SUMS.txt`
- `QA_REPORT.md`
- `asset_plant.parquet`
- `asset_generator.parquet`
- `weather_station.parquet`
- `station_candidate.parquet`
- `station_selection_decision.parquet`
- `station_coverage_audit.parquet`
- `station_ecwt.parquet`
- `plant_ecwt.parquet`
- `generator_ecwt.parquet`
- `exceptions.parquet`

If release artifacts exceed practical GitHub Release limits, publish large bundles in object storage or Zenodo and include immutable URLs plus SHA-256 hashes in the GitHub release.

## Versioning Rules

Every published row must carry:

- `release_id`
- `calculation_run_id`
- `methodology_version`
- `source_file_id` or equivalent source lineage
- `source_sha256` where the row derives directly from a file
- `code_commit`
- `created_at_utc`

Release IDs are immutable. If a data issue is found, publish a new release and document the change. Do not mutate prior released bundles in place.

## Publication Tiers

### Tier 1: Asset Inventory

Purpose: publish the EIA-860 plant/generator universe before weather matching.

Outputs:

- asset tables
- EIA source manifest
- coordinate quality report
- generator status counts
- unresolved asset exceptions

### Tier 2: Station Candidate Inventory

Purpose: publish candidate NOAA stations for each plant.

Outputs:

- nearest/candidate station rankings
- distance and elevation deltas where available
- station operational coverage
- obvious non-representative flags

### Tier 3: ECWT Alpha

Purpose: publish first full ECWT results with known caveats.

Outputs:

- station selections
- coverage audits
- ECWT values
- exception list
- limitations and not-yet-manual-reviewed decisions

### Tier 4: ECWT National Release

Purpose: publish a stable national dataset with documented QA thresholds and review status.

Outputs:

- all Tier 3 outputs
- manual review decisions where required
- final QA report
- reproducibility instructions

## Repository Hygiene

Keep Git history clean:

- Do not commit raw data ZIPs.
- Do not commit database files.
- Do not commit generated Parquet bundles.
- Do not commit files larger than 50 MB.
- Do not commit generated CSV runs, timestamped QA reports, release extracts, or local `data/processed/*` outputs.
- Keep only stable, curated documentation in `docs/`; generated per-run artifacts must stay local unless they are packaged as release assets.
- Store checksums and source manifests for large files instead of the files themselves.

The repository `.gitignore` enforces this boundary for the known generated-output patterns. If a generated artifact is intentionally published, attach it to a versioned release and include its checksum in the release manifest rather than force-adding it into normal repo history.
