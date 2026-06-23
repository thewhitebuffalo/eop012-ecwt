# Database Operations

## Dedicated EOP012 Cluster

The dedicated EOP012 Postgres cluster lives on the external NOAA cache drive:

```text
/Volumes/NOAA_CACHE/EOP012/postgres16
```

Canonical connection:

```text
host=127.0.0.1
port=5436
dbname=eop012
```

## Start

```bash
/opt/homebrew/opt/postgresql@16/bin/pg_ctl \
  -D /Volumes/NOAA_CACHE/EOP012/postgres16 \
  -l /Volumes/NOAA_CACHE/EOP012/logs/postgres16.log \
  start
```

## Stop

```bash
/opt/homebrew/opt/postgresql@16/bin/pg_ctl \
  -D /Volumes/NOAA_CACHE/EOP012/postgres16 \
  stop -m fast
```

## Readiness Check

```bash
/opt/homebrew/opt/postgresql@16/bin/pg_isready -h 127.0.0.1 -p 5436
```

## Apply Schema

```bash
/opt/homebrew/opt/postgresql@16/bin/psql \
  -h 127.0.0.1 -p 5436 -d eop012 \
  -v ON_ERROR_STOP=1 \
  -f /Users/Shared/EOP012/rebuild/sql/audit_schema.sql
```

## Load EIA-860 Assets

```bash
/Users/whitebuffalo/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  /Users/Shared/EOP012/rebuild/scripts/load_eia860_assets_to_postgres.py
```

