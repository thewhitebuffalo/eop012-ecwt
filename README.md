# EOP012 Database Build

Goal: calculate a documented Extreme Cold Weather Temperature (ECWT) for U.S. generating plants using a clean plant/generator universe, representative weather-source selection, and auditable ECWT calculations.

## Current Approach

1. Use EIA-860 as the primary plant and generator universe.
2. Use NOAA hourly dry-bulb weather data for the ECWT calculation.
3. Keep raw source files immutable.
4. Store all source provenance, station-selection decisions, coverage checks, and calculation outputs explicitly.

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
and `data/processed/*` files are local artifacts by default. Publish them as release
bundles with checksums when they need to be shared; do not commit them to repo history.

## Publication Model

GitHub is the audit/control plane for this project, not the heavy weather-data warehouse.

- Commit code, schemas, methodology, manifests, checksums, QA reports, and small previews.
- Keep heavyweight NOAA hourly data and working databases under `EOP012_DATA_ROOT` or another external cache.
- Publish versioned release bundles with checksums and enough provenance to reproduce every ECWT value.
- Never commit large raw ZIPs, Postgres clusters, DuckDB files, Parquet bundles, generated CSV runs, release extracts, or generated data directories directly to Git.

See:

- `docs/REPRODUCING.md`
- `docs/publication_plan.md`
- `docs/methodology.md`
- `docs/audit_schema.md`
- `docs/data_dictionary.md`
- `sql/audit_schema.sql`
