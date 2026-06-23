# EOP012 Rebuild

Goal: calculate a documented Extreme Cold Weather Temperature (ECWT) for U.S. generating plants using a clean plant/generator universe, representative weather-source selection, and auditable ECWT calculations.

## Current Approach

1. Use EIA-860 as the primary plant and generator universe.
2. Use NOAA hourly dry-bulb weather data for the ECWT calculation.
3. Keep raw source files immutable.
4. Store all source provenance, station-selection decisions, coverage checks, and calculation outputs explicitly.

## Immediate Baseline

The first baseline is EIA-860 2024 final annual data:

`/Users/Shared/EOP012/EIA_860_raw_downloads/intake/eia8602024.zip`

The 2025 early release is available for comparison/currentness but should remain provisional until EIA publishes final 2025 data.

## Rebuild Outputs

- `data/processed/eia860_*/`: generated normalized CSV extracts.
- `docs/eia860_asset_inventory.md`: generated inventory report for the plant/generator universe.
- `scripts/build_eia860_asset_inventory.py`: reproducible EIA-860 extractor and auditor.

## Publication Model

GitHub is the audit/control plane for this project, not the heavy weather-data warehouse.

- Commit code, schemas, methodology, manifests, checksums, QA reports, and small previews.
- Keep heavyweight NOAA hourly data and working databases on `/Volumes/NOAA_CACHE`.
- Publish versioned release bundles with checksums and enough provenance to reproduce every ECWT value.
- Never commit large raw ZIPs, Postgres clusters, DuckDB files, Parquet bundles, or generated data directories directly to Git.

See:

- `docs/publication_plan.md`
- `docs/methodology.md`
- `docs/audit_schema.md`
- `docs/data_dictionary.md`
- `sql/audit_schema.sql`
