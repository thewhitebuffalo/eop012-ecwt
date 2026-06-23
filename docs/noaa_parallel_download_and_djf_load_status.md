# NOAA Parallel Download And DJF Load Status

Generated UTC: 2026-06-23T22:38:00Z

Database: `eop012` on `127.0.0.1:5436`

## Summary

The NOAA work is now split into two independent lanes:

1. Continue downloading missing NOAA Global Hourly station-year CSV files from the public AWS bucket.
2. Parse available local CSV files into the normalized `weather.hourly_djf` table in bounded, auditable batches.

This lets the ECWT build start finding schema, parser, and source-quality issues without waiting for the full NOAA backfill to complete.

## Download Lane

Active AWS manifest: `noaa_backfill_manifest_20260623T215215Z`

| Batch | Run ID | Downloaded | HTTP 404 | Bytes |
| ---: | --- | ---: | ---: | ---: |
| 3 | `noaa_backfill_download_batch3_20260623T222202Z` | 640 | 360 | 4,075,064,091 |
| 4 | `noaa_backfill_download_batch4_20260623T222846Z` | 623 | 377 | 3,590,769,094 |

Current AWS manifest status:

| Status | Rows |
| --- | ---: |
| downloaded | 2,574 |
| failed | 1,426 |
| planned | 82,839 |

Current raw AWS cache:

| Metric | Value |
| --- | ---: |
| CSV files | 2,574 |
| `.part` files | 0 |
| Disk usage | 15 GB |

## DJF Load Lane

Target table: `weather.hourly_djf`

Runs completed:

| Run ID | Source | Files | Staged DJF Hours |
| --- | --- | ---: | ---: |
| `noaa_hourly_djf_load_20260623T222744Z` | downloaded | 5 | 4,810 |
| `noaa_hourly_djf_load_20260623T222807Z` | downloaded | 250 | 326,155 |
| `noaa_hourly_djf_load_20260623T222937Z` | inventory | 100 | 163,885 |
| `noaa_hourly_djf_load_20260623T223108Z` | inventory | 500 | 971,073 |

Current parsed weather state:

| Metric | Value |
| --- | ---: |
| `weather.hourly_djf` rows | 1,465,923 |
| Distinct stations loaded | 596 |
| Loaded downloaded-source files | 255 |
| Loaded inventory-source files | 600 |
| Downloaded-source loaded hours | 330,965 |
| Inventory-source loaded hours | 1,134,958 |
| Invalid DJF temp rows observed | 75,909 |
| Duplicate station-hour observations collapsed | 2,064,343 |
| Database size | 1,051 MB |

## QA Finding

The parser and table path are working, but the loaded data is not yet compliance-grade. A first QA pass found two impossible high DJF temperatures at `720267-23224` / Auburn Municipal Airport in February 2025:

| Station | Hour UTC | Parsed TMP |
| --- | --- | ---: |
| `720267-23224` | `2025-02-21T22:00:00Z` | 55.0 C |
| `720267-23224` | `2025-02-21T23:00:00Z` | 56.0 C |

The raw NOAA CSV contains these `TMP` values. The same raw records' `REM` field appears Fahrenheit-like, so NOAA `SOURCE=7` rows need a source-quality decision before final ECWT calculation. This does not break the database architecture, but it blocks compliance-grade ECWT publication until resolved.

## Next Decision

Before loading all remaining raw files, decide whether the production loader should:

1. Exclude selected NOAA source codes, especially `SOURCE=7`, from final ECWT weather input.
2. Prefer `SOURCE=4` observations over `SOURCE=7` when both exist in the same station-hour.
3. Add physical and climatological plausibility filters with exception rows for rejected observations.
4. Preserve a raw parsed observation table separately from the canonical `weather.hourly_djf` table.

The likely production answer is both 2 and 3, plus a raw-observation table if we want complete forensic traceability.
