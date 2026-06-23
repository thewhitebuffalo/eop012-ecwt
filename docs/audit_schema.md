# Audit Schema

## Purpose

The audit schema defines the minimum data model needed to publish ECWT values that can be traced back to source files, code, station decisions, coverage checks, and calculation runs.

The heavy database should live on `/Volumes/NOAA_CACHE`. The GitHub repository contains this schema, migration files, documentation, manifests, and small QA outputs.

## Schemas

| Schema | Purpose |
| --- | --- |
| `audit` | Run metadata, methodology versions, source manifests, release manifests. |
| `asset` | EIA-860 plant, generator, utility, and field dictionary tables. |
| `weather` | NOAA station metadata, hourly observations or references to hourly partitions, coverage audits. |
| `link` | Plant-to-station candidates, selections, station segments, manual decisions. |
| `calc` | Station, plant, and generator ECWT outputs. |
| `publish` | Stable release-facing views and export manifests. |

## Core Lineage Pattern

Every derived table should include:

- `calculation_run_id`
- `methodology_version`
- `created_at_utc`

Rows that come from a source file should include:

- `source_file_id`
- source row identifier where available
- source year or release year

Published outputs should include:

- `release_id`
- `code_commit`
- `source_manifest_sha256`
- bundle checksum

## Key Tables

### `audit.source_file`

One row per source artifact. Examples:

- EIA ZIP file
- NOAA hourly file
- NOAA station metadata file
- external normalized source bundle

### `audit.calculation_run`

One row per pipeline run. Captures code commit, methodology version, parameters, and run status.

### `asset.plant`

Normalized EIA plant records. This is the plant-level spatial anchor for station matching.

### `asset.generator`

Normalized EIA generator records. This supports unit-level ECWT output and later EOP-012 applicability review.

### `weather.station`

Weather station identity and metadata.

### `weather.hourly_djf`

Lean hourly DJF dry-bulb observations. This table may be partitioned or represented by external Parquet files if size requires.

### `weather.station_coverage_audit`

Expected versus observed DJF hours by station and period.

### `link.station_candidate`

Candidate stations for each plant, including distance and coverage metrics.

### `link.station_selection`

The selected station path for each plant. A station selection can have one or more date segments.

### `calc.plant_ecwt`

Final plant-level ECWT values and audit fields.

### `calc.generator_ecwt`

Generator-level ECWT values inherited from plant selection unless a unit-specific selection is documented.

### `audit.exception_log`

Published inventory of known problems, unresolved cases, and manual-review requirements.

## Non-Negotiable Rules

- Do not overwrite prior calculation runs.
- Do not mutate released results.
- Do not silently fill missing weather data.
- Do not collapse station-candidate evidence into only the final selected station.
- Do not publish ECWT values without coverage counts.
- Do not treat EIA plant universe and EOP-012 applicability as the same thing.

