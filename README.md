# EOP012 Database Build

Goal: calculate a documented Extreme Cold Weather Temperature (ECWT) for U.S. generating plants using a clean plant/generator universe, representative weather-source selection, and auditable ECWT calculations.

## Current Approach

1. Use EIA-860 as the primary plant and generator universe.
2. Use NOAA hourly dry-bulb weather data for the ECWT calculation.
3. Keep raw source files immutable.
4. Store all source provenance, station-selection decisions, coverage checks, and calculation outputs explicitly.

## Release outputs

The per-run ECWT outputs are large (the full results, scoped release, per-hour cold-tail provenance, and source tables total roughly 500 MB) and regenerate on every run, so they are **published as GitHub Release assets rather than committed to Git history.** This keeps clones fast while keeping every published value auditable and downloadable.

- **Audit or verify a published value:** download the scoped release CSV (`scoped_plant_ecwt_*_release_*.csv`) from the matching [Release](https://github.com/thewhitebuffalo/eop012-ecwt/releases). Each row carries the plant's ECWT plus its station provenance and coverage.
- **Verify integrity:** the small `*_SHA256SUMS.txt` manifest is kept in the repo under `data/processed/` so any downloaded Release asset can be checksummed against what was published.
- **Reproduce:** regenerate the outputs with the pipeline, then build the dashboard with `scripts/build_ecwt_dashboard.py --release-csv <scoped CSV>`.
- The self-contained dashboard (`build/EOP012_ADR0004_ECWT_dashboard.html`) embeds the published results and stays in the repo as the viewable artifact.

Output CSVs under `data/processed/` are git-ignored (see `.gitignore`); attach them to the tagged Release for each run instead of committing them.

## Local Configuration

Scripts can run from any clone path. Defaults come from environment variables in
`.env.example`, and every important path also has a command-line override.

```bash
cp .env.example .env
set -a
source .env
set +a
```

Key paths:

- `EOP012_PROJECT_ROOT`: local repository clone.
- `EOP012_DATA_ROOT`: external working-data root for raw files, staging files, and local database clusters.
- `EOP012_EIA860_ZIP`: EIA-860 2024 final ZIP.
- `EOP012_STAGING_ROOT`: generated CSV staging directory.
- `EOP012_NOAA_GLOBAL_HOURLY_ROOT`: NOAA Global Hourly raw-file cache.
- `EOP012_NOAA_RAW_ROOTS`: colon-separated NOAA raw-file cache roots used by inventory scans.
- `EOP012_PSQL`: PostgreSQL `psql` client binary.

## Immediate Baseline

The first baseline is EIA-860 2024 final annual data. By default scripts look at:

`$EOP012_EIA860_ZIP`

The 2025 early release is available for comparison/currentness but should remain provisional until EIA publishes final 2025 data.

## Rebuild Outputs

- `data/processed/eia860_*/`: generated normalized CSV extracts.
- `docs/eia860_asset_inventory.md`: generated inventory report for the plant/generator universe.
- `scripts/build_eia860_asset_inventory.py`: reproducible EIA-860 extractor and auditor.

Generated run products such as timestamped CSVs, release extracts, per-run QA reports,
and `data/processed/*` files are working artifacts until they are promoted. When a
run is intentionally published, commit the scoped CSV/results, dashboards, manifests,
status notes, and checksums to Git so the public repository carries the auditable
release surface.

## Publication Model

GitHub is the audit/control plane for this project, not the heavy weather-data warehouse.

- Commit code, schemas, methodology, manifests, checksums, QA reports, release CSVs,
  result CSVs, published dashboards, and small previews.
- Keep heavyweight NOAA hourly data and working databases under `EOP012_DATA_ROOT` or another external cache.
- Publish versioned release artifacts with checksums and enough provenance to reproduce every ECWT value.
- Never commit large raw ZIPs, Postgres clusters, DuckDB files, Parquet bundles, raw NOAA caches, or local database directories directly to Git.

See:

- `docs/REPRODUCING.md`
- `docs/publication_plan.md`
- `docs/methodology.md`
- `docs/audit_schema.md`
- `docs/data_dictionary.md`
- `sql/audit_schema.sql`
