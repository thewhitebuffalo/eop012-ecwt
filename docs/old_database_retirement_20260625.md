# Old Database Retirement - 2026-06-25

## Decision

The old local Postgres clusters on the NOAA cache drive are retired. Retirement
means stopped, renamed, and removed from default project configuration. It does
not mean deleted.

The current source of truth is the rebuilt EOP012 database:

```text
data_directory=/Volumes/NOAA_CACHE/EOP012/postgres16
host=127.0.0.1
port=5436
dbname=eop012
logical_size=31 GB
physical_cluster_size=32G
```

Current release evidence in the rebuilt database:

```text
release_id=scoped_plant_ecwt_release_20260625T161629Z
calculation_run_id=release_manifest_20260625T163910Z
source_manifest_sha256=4f2e5eb95b5f2ab3a25bbd0cd2fd7fdc8a6002f7fc70a6b0255b93d092420656
release_created_at_utc=2026-06-25T16:39:10Z
```

The release completion audit is `docs/ecwt_goal_completion_audit_20260625T164014Z.md`.

## Retired Clusters

| Former path | Retired path | Size | State at retirement |
| --- | --- | ---: | --- |
| `/Volumes/NOAA_CACHE/postgres16_weather_build` | `/Volumes/NOAA_CACHE/postgres16_weather_build_RETIRED_20260625` | 1.1G | already stopped |
| `/Volumes/NOAA_CACHE/postgres16_weather_build_5435` | `/Volumes/NOAA_CACHE/postgres16_weather_build_5435_RETIRED_20260625` | 277G | stopped cleanly before rename |

The retired `5435` cluster contained:

| Database | Approximate size | Notes |
| --- | ---: | --- |
| `noaa_djf_hourly_bytower` | 276 GB | old derived/intermediate NOAA weather cache |
| `domestic_utility_data_core` | 19 MB | old non-authoritative database |
| `postgres` | 7615 kB | cluster maintenance database |

Only the `Athena` role was present in the retired `5435` cluster.

## Why It Was Retired

The old `domestic_utility_data_core` database was previously audited and found
not to be a reliable EOP012 domain source of truth. The audit found that the
expected EOP012 core tables were missing and that the database mainly contained
out-of-scope metadata schemas. The pre-retirement dump remains available as
evidence:

```text
/Users/Shared/EOP012/db_audit/domestic_utility_data_core_scope_audit_20260623.md
/Users/Shared/EOP012/db_audit/domestic_utility_data_core_precleanup_20260623.dump
```

The large `noaa_djf_hourly_bytower` database was a legacy weather cache used for
fast triage during the rebuild. It is no longer the publication source of truth.
The rebuilt `eop012` database has the normalized weather, station coverage,
station ECWT, plant ECWT policy result, release manifest, and publish artifact
tables used by the completed scoped release.

## Actions Performed

1. Verified rebuilt `eop012` on port `5436` was accepting connections.
2. Verified legacy cluster on port `5435` was accepting connections before
   retirement.
3. Stopped the legacy `5435` cluster with:

   ```bash
   /opt/homebrew/Cellar/postgresql@16/16.14/bin/pg_ctl \
     -D /Volumes/NOAA_CACHE/postgres16_weather_build_5435 \
     -m fast stop
   ```

4. Verified `5435` no longer responded and `pg_controldata` reported the
   retired cluster state as `shut down`.
5. Renamed the legacy directories in place:

   ```bash
   mv /Volumes/NOAA_CACHE/postgres16_weather_build_5435 \
      /Volumes/NOAA_CACHE/postgres16_weather_build_5435_RETIRED_20260625

   mv /Volumes/NOAA_CACHE/postgres16_weather_build \
      /Volumes/NOAA_CACHE/postgres16_weather_build_RETIRED_20260625
   ```

6. Updated project defaults so the legacy source cluster path is no longer the
   active old directory name.

The leftover log file `/Volumes/NOAA_CACHE/postgres16_weather_build_5435.log`
was left in place.

## Restore Procedure If Historical Replay Is Needed

Do not restore the retired cluster for normal ECWT production work. If a
historical replay is required:

1. Stop any process already using the target port.
2. Move the retired directory back to a deliberate working path.
3. Start it on an explicit, non-conflicting port.
4. Set `EOP012_SOURCE_CLUSTER_PATH` explicitly instead of relying on defaults.
5. Treat results as legacy evidence, not as the current publication source of
   truth.

Deletion of the retired directories would reclaim about 278G, but that should be
a separate explicit decision after any desired archival window.
