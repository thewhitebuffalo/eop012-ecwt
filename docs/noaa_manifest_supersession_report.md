# NOAA Manifest Supersession Report

Generated UTC: 2026-06-23T22:11:33Z

Database: `eop012` on `127.0.0.1:5436`

## Summary

The stale NOAA Global Hourly backfill manifest that referenced the NCEI HTTPS access endpoint has been superseded. No download attempts were made from that manifest. The active manifest remains the public AWS bulk manifest using `https://noaa-global-hourly-pds.s3.amazonaws.com/`.

## Superseded Manifest

| Field | Value |
| --- | --- |
| calculation_run_id | `noaa_backfill_manifest_20260623T214301Z` |
| previous base_url | `https://www.ncei.noaa.gov/data/global-hourly/access/` |
| new run_status | `superseded` |
| superseded_by | `noaa_backfill_manifest_20260623T215215Z` |
| rows marked skipped | 86,839 |
| reason | NCEI HTTPS access endpoint is not the required public AWS bulk source. |

## Active AWS Manifest

| Field | Value |
| --- | --- |
| calculation_run_id | `noaa_backfill_manifest_20260623T215215Z` |
| base_url | `https://noaa-global-hourly-pds.s3.amazonaws.com/` |
| run_status | `succeeded` |
| total rows | 86,839 |
| batch count | 87 |

## Current Manifest Status Counts

| calculation_run_id | manifest_status | rows |
| --- | ---: | ---: |
| `noaa_backfill_manifest_20260623T214301Z` | skipped | 86,839 |
| `noaa_backfill_manifest_20260623T215215Z` | downloaded | 1,311 |
| `noaa_backfill_manifest_20260623T215215Z` | failed | 689 |
| `noaa_backfill_manifest_20260623T215215Z` | planned | 84,839 |

## Audit Note

The stale NCEI manifest metadata is retained for auditability, but every row has been removed from the active download queue by setting `manifest_status = 'skipped'`. The active download path is the NOAA Global Hourly public AWS bucket.
