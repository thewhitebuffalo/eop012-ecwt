# Reproducing The Current Build

This guide explains how a collaborator can reproduce the current auditable EIA-860 asset database from the public code and official source data.

Current reproducible scope:

- EIA-860 2024 final source download.
- EIA source hash verification.
- EIA plant/generator/utility inventory generation.
- Dedicated Postgres database creation.
- Audit schema creation.
- EIA asset load into `audit.*` and `asset.*`.
- Known EIA exceptions.

Not yet implemented:

- NOAA hourly weather loading into the new EOP012 database.
- Station selection decisions.
- ECWT calculation.
- Release bundle export.

## Prerequisites

Install:

- Git
- Python 3.11 or newer
- PostgreSQL 16 command-line tools: `initdb`, `pg_ctl`, `createdb`, `psql`

On macOS with Homebrew:

```bash
brew install postgresql@16
```

The commands below assume a Unix-like shell. They use local variables so the repository can be cloned anywhere.

## Clone

```bash
git clone https://github.com/thewhitebuffalo/eop012-ecwt.git
cd eop012-ecwt
export REPO="$PWD"
```

## Install Python Dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Configure Local Paths

The repository does not commit raw source files, NOAA hourly weather caches, or
database clusters. Copy the example environment file and edit it for your
machine:

```bash
cp .env.example .env
set -a
source .env
set +a
```

The scripts use these environment variables as defaults, and command-line flags
still take precedence for one-off runs.

| Variable | Purpose |
| --- | --- |
| `EOP012_PROJECT_ROOT` | Local clone of this repository. |
| `EOP012_DATA_ROOT` | External working-data root for raw files, staging files, logs, and local database clusters. |
| `EOP012_EIA860_ZIP` | EIA-860 2024 final ZIP downloaded from EIA. |
| `EOP012_STAGING_ROOT` | Generated CSV staging directory used before database loads. |
| `EOP012_NOAA_GLOBAL_HOURLY_ROOT` | NOAA Global Hourly raw CSV/GZ cache. |
| `EOP012_NOAA_RAW_ROOTS` | Optional colon-separated list of NOAA raw roots for inventory scans. |
| `EOP012_STATION_HISTORY_CSV` | NOAA ISD station-history CSV cache path. |
| `EOP012_SOURCE_CLUSTER_PATH` | Optional legacy/source Postgres cluster used by coverage-audit bridge scripts. |
| `EOP012_PSQL` | PostgreSQL `psql` client binary; use an absolute path if it is not on `PATH`. |

## Choose A Local Data Root

Use an external drive if available. The current asset-only build is small, but future NOAA hourly data will be large.

```bash
export EOP012_DATA_ROOT="/Volumes/NOAA_CACHE/EOP012_REPRO"
mkdir -p "$EOP012_DATA_ROOT/raw/eia860/intake"
mkdir -p "$EOP012_DATA_ROOT/postgres16"
mkdir -p "$EOP012_DATA_ROOT/logs"
mkdir -p "$EOP012_DATA_ROOT/staging"
```

If you do not have `/Volumes/NOAA_CACHE`, choose another path:

```bash
export EOP012_DATA_ROOT="$HOME/eop012_data"
mkdir -p "$EOP012_DATA_ROOT/raw/eia860/intake" "$EOP012_DATA_ROOT/postgres16" "$EOP012_DATA_ROOT/logs" "$EOP012_DATA_ROOT/staging"
```

## Download EIA-860 2024 Final

```bash
export EIA860_ZIP="$EOP012_DATA_ROOT/raw/eia860/intake/eia8602024.zip"

curl -L --fail --remote-time \
  -o "$EIA860_ZIP" \
  https://www.eia.gov/electricity/data/eia860/xls/eia8602024.zip
```

Verify the ZIP hash:

```bash
shasum -a 256 "$EIA860_ZIP"
```

Expected SHA-256:

```text
0aaae04812cd4ab87a3e346bdf93848a3cc15053fd4dc2a4cf82d2aeac95f12b
```

Test the ZIP:

```bash
unzip -t "$EIA860_ZIP"
```

## Build The EIA Asset Inventory

```bash
python "$REPO/scripts/build_eia860_asset_inventory.py" \
  --zip "$EIA860_ZIP" \
  --project-root "$REPO"
```

Expected generated files:

```text
data/processed/eia8602024/plant.csv
data/processed/eia8602024/utility.csv
data/processed/eia8602024/generator_operable.csv
data/processed/eia8602024/generator_proposed.csv
data/processed/eia8602024/generator_retired_and_canceled.csv
data/processed/eia8602024/generator_all.csv
data/processed/eia8602024/field_dictionary.csv
data/processed/eia8602024/source_manifest.csv
data/processed/eia8602024/inventory_summary.json
docs/eia860_asset_inventory.md
docs/data_inventory.md
```

The generated `data/processed` directory is intentionally ignored by Git.

Expected 2024 inventory counts:

| Metric | Count |
| --- | ---: |
| Plant rows | 16,132 |
| Utility rows | 6,643 |
| Operable generator rows | 26,855 |
| Generator rows, all sheets | 34,855 |
| Plants with valid numeric coordinates | 16,104 |
| Plants missing/non-numeric coordinates | 28 |

## Create A Local Postgres Database

Find your PostgreSQL 16 binary directory.

On Apple Silicon Homebrew:

```bash
export PG_BIN="/opt/homebrew/opt/postgresql@16/bin"
```

On Intel Homebrew:

```bash
export PG_BIN="/usr/local/opt/postgresql@16/bin"
```

Or use tools from `PATH`:

```bash
export PG_BIN="$(dirname "$(command -v psql)")"
```

Initialize the database cluster if it does not already exist:

```bash
if [ ! -f "$EOP012_DATA_ROOT/postgres16/PG_VERSION" ]; then
  "$PG_BIN/initdb" -D "$EOP012_DATA_ROOT/postgres16"
fi
```

Start Postgres on port `5436`:

```bash
"$PG_BIN/pg_ctl" \
  -D "$EOP012_DATA_ROOT/postgres16" \
  -o "-p 5436 -h 127.0.0.1" \
  -l "$EOP012_DATA_ROOT/logs/postgres16.log" \
  start
```

Create the database:

```bash
"$PG_BIN/createdb" -h 127.0.0.1 -p 5436 eop012
```

If the database already exists, this command may report an error. That is fine if you are intentionally reusing the same database.

Apply the audit schema:

```bash
"$PG_BIN/psql" \
  -h 127.0.0.1 -p 5436 -d eop012 \
  -v ON_ERROR_STOP=1 \
  -f "$REPO/sql/audit_schema.sql"
```

## Load EIA-860 Assets Into Postgres

```bash
python "$REPO/scripts/load_eia860_assets_to_postgres.py" \
  --project-root "$REPO" \
  --zip "$EIA860_ZIP" \
  --processed-dir "$REPO/data/processed/eia8602024" \
  --staging-root "$EOP012_DATA_ROOT/staging" \
  --psql "$PG_BIN/psql" \
  --host 127.0.0.1 \
  --port 5436 \
  --dbname eop012
```

Expected database counts:

| Relation | Rows |
| --- | ---: |
| `audit.source_file` | 5 |
| `audit.calculation_run` | 1 |
| `asset.utility` | 6,643 |
| `asset.plant` | 16,132 |
| `asset.generator` | 34,855 |
| `audit.exception_log` | 29 |

Verify:

```bash
"$PG_BIN/psql" -h 127.0.0.1 -p 5436 -d eop012 -P pager=off -c "
select 'asset.utility' as relation, count(*) from asset.utility
union all select 'asset.plant', count(*) from asset.plant
union all select 'asset.generator', count(*) from asset.generator
union all select 'audit.source_file', count(*) from audit.source_file
union all select 'audit.calculation_run', count(*) from audit.calculation_run
union all select 'audit.exception_log', count(*) from audit.exception_log
order by relation;
"
```

Expected exception categories:

```bash
"$PG_BIN/psql" -h 127.0.0.1 -p 5436 -d eop012 -P pager=off -c "
select reason_code, severity, resolution_status, count(*)
from audit.exception_log
group by reason_code, severity, resolution_status
order by reason_code;
"
```

Expected:

| Reason code | Count |
| --- | ---: |
| `plant_missing_coordinates` | 28 |
| `generator_plant_code_not_in_plant_table` | 1 |

## Load NOAA Station Metadata And Distance Candidates

This step downloads NOAA ISD station history metadata and generates distance-only station candidates for every loaded EIA plant with valid coordinates. Hourly weather coverage is not attached yet.

```bash
python "$REPO/scripts/load_noaa_station_candidates.py" \
  --project-root "$REPO" \
  --station-history-csv "$EOP012_DATA_ROOT/raw/noaa/isd-history.csv" \
  --staging-root "$EOP012_DATA_ROOT/staging" \
  --psql "$PG_BIN/psql" \
  --host 127.0.0.1 \
  --port 5436 \
  --dbname eop012
```

Expected outputs:

```text
docs/noaa_station_candidate_report.md
weather.station
link.station_candidate
```

The candidate layer intentionally leaves these fields blank until the NOAA hourly coverage phase:

```text
valid_djf_hours
expected_djf_hours
coverage_ratio
```

## Load NOAA Weather Coverage Audit

This step enriches the station candidates with fast NOAA coverage metrics from the legacy NOAA cache's station-level sample-hour table.

The source cluster must be running separately on port `5435`:

```bash
"$PG_BIN/pg_ctl" \
  -D /Volumes/NOAA_CACHE/postgres16_weather_build_5435 \
  -l /Volumes/NOAA_CACHE/postgres16_weather_build_5435/server.log \
  -o "-p 5435 -h 127.0.0.1" \
  start
```

Then run:

```bash
python "$REPO/scripts/load_noaa_weather_coverage_audit.py" \
  --project-root "$REPO" \
  --staging-root "$EOP012_DATA_ROOT/staging" \
  --psql "$PG_BIN/psql" \
  --host 127.0.0.1 \
  --port 5436 \
  --dbname eop012 \
  --source-host 127.0.0.1 \
  --source-port 5435 \
  --source-dbname noaa_djf_hourly_bytower \
  --source-user Athena
```

Expected outputs:

```text
docs/noaa_weather_coverage_audit_report.md
weather.station_coverage_audit
link.station_candidate.valid_djf_hours
link.station_candidate.expected_djf_hours
link.station_candidate.coverage_ratio
```

This is a fast coverage triage step. It uses `public.ecwt_raw_station.sample_hours` in the legacy NOAA cache and does not replace the later full NOAA hourly rebuild/recount needed for compliance-grade missing-hour, duplicate-hour, and invalid-temperature evidence.

## Inventory Local NOAA Raw Files

This step inventories local NOAA Global Hourly station-year CSV files for the candidate stations. It does not parse hourly observations yet.

```bash
python "$REPO/scripts/inventory_noaa_raw_files.py" \
  --project-root "$REPO" \
  --staging-root "$EOP012_DATA_ROOT/staging" \
  --psql "$PG_BIN/psql" \
  --host 127.0.0.1 \
  --port 5436 \
  --dbname eop012 \
  --start-year 2000 \
  --end-year 2025
```

Default raw roots, in priority order:

```text
/Volumes/NOAA_CACHE/noaa-global-hourly-pds-full
/Volumes/NOAA_CACHE/noaa-global-hourly-year-staging
/Volumes/NOAA_CACHE/noaa-global-hourly-unified
/Volumes/NOAA_CACHE/BACKUP_TO_DELETE_LATER_noaa-cache_2026-02-19
```

Expected outputs:

```text
docs/noaa_raw_file_inventory_report.md
weather.noaa_raw_file_inventory
```

The inventory maps station IDs from `USAF-WBAN` to NOAA raw file names by removing the hyphen. For example, `725117-04827` maps to `72511704827.csv`.

## Build NOAA Backfill Manifest

This step converts missing raw-file inventory rows into a planned NOAA download queue. It does not download files.

```bash
python "$REPO/scripts/build_noaa_backfill_manifest.py" \
  --project-root "$REPO" \
  --staging-root "$EOP012_DATA_ROOT/staging" \
  --target-root "$EOP012_DATA_ROOT/raw/noaa/global-hourly" \
  --psql "$PG_BIN/psql" \
  --host 127.0.0.1 \
  --port 5436 \
  --dbname eop012 \
  --batch-size 1000
```

Expected outputs:

```text
docs/noaa_backfill_manifest_report.md
weather.noaa_raw_backfill_manifest
```

Manifest URLs use the public AWS S3 bucket for NOAA Global Hourly CSV:

```text
https://noaa-global-hourly-pds.s3.amazonaws.com/{year}/{USAFWBAN}.csv
```

Rows are prioritized by missing whole years first, newer years first, and candidate stations linked to the most plants first. Batch 1 is the first manageable downloader test set.

## Download One NOAA Backfill Batch

This step consumes one manifest batch and records every attempt. Files are written through temporary `.part` files and moved into place only after a complete stream. Existing target files are not overwritten unless `--overwrite` is explicitly supplied.

```bash
python "$REPO/scripts/download_noaa_backfill_batch.py" \
  --project-root "$REPO" \
  --staging-root "$EOP012_DATA_ROOT/staging" \
  --psql "$PG_BIN/psql" \
  --host 127.0.0.1 \
  --port 5436 \
  --dbname eop012 \
  --batch-number 1 \
  --max-workers 4
```

Expected outputs:

```text
docs/noaa_backfill_download_batch1_report.md
weather.noaa_raw_download_attempt
audit.source_file rows for successful or pre-existing files
```

## Stop Postgres

```bash
"$PG_BIN/pg_ctl" \
  -D "$EOP012_DATA_ROOT/postgres16" \
  stop -m fast
```

## Reproducibility Notes

The load script records the current Git commit in `audit.calculation_run.code_commit`. A collaborator running from a later commit should expect the row counts to match, but the recorded commit hash and run ID will differ.

The current database load report in this repository documents the load performed on the maintainer machine:

```text
docs/eia860_db_load_report.md
```

Future NOAA and ECWT phases should follow the same pattern:

1. Commit code and methodology first.
2. Run the database pipeline from committed code.
3. Record source hashes, row counts, exceptions, and the producing Git commit.
4. Publish small reports and manifests to Git.
5. Keep heavy raw/weather/database artifacts outside Git.
