# NOAA Hardened Load And Provisional ECWT Status

Generated UTC: 2026-06-23T23:05:47Z

Database: `eop012` on `127.0.0.1:5436`

## Canonical Load Rule

The permissive exploratory `weather.hourly_djf` population was cleared and reloaded under hardened canonical rules:

- Reject NOAA `SOURCE=7` before interpreting `TMP`.
- Accept parsed dry-bulb temperatures only from `-90 C` through `50 C`.
- Preserve rejected-row counts in `weather.noaa_hourly_load_file`.

This rule is intentionally conservative. The earlier QA probe found `SOURCE=7` rows where `TMP` appeared Fahrenheit-like, which can materially corrupt cold-tail ECWT.

## Hardened Loads Completed

| Run ID | Source | Files | Canonical DJF Hours | Rejected SOURCE Rows | Rejected Plausibility Rows |
| --- | --- | ---: | ---: | ---: | ---: |
| `noaa_hourly_djf_load_20260623T224435Z` | downloaded | 1,000 | 334,681 | 2,260,266 | 0 |
| `noaa_hourly_djf_load_20260623T224655Z` | inventory | 1,000 | 773,512 | 2,839,884 | 0 |
| `noaa_hourly_djf_load_20260623T225702Z` | downloaded | 1,000 | 262,008 | 1,979,457 | 0 |
| `noaa_hourly_djf_load_20260623T230025Z` | inventory | 1,000 | 515,735 | 2,879,389 | 0 |

Current canonical weather:

| Metric | Value |
| --- | ---: |
| `weather.hourly_djf` rows | 1,885,936 |
| Distinct stations | 2,012 |
| Loaded downloaded-source files | 2,000 |
| Loaded inventory-source files | 2,000 |
| Total SOURCE rows rejected | 9,958,996 |

## Coverage And ECWT

Latest station-year coverage run: `station_year_djf_coverage_20260623T230407Z`

| Metric | Value |
| --- | ---: |
| Coverage rows | 4,000 |
| Complete station-years | 175 |
| Partial station-years | 3,774 |
| Empty station-years | 51 |
| Valid DJF hours represented | 1,885,936 |

Latest provisional station ECWT run: `station_ecwt_loaded_20260623T230415Z`

| Metric | Value |
| --- | ---: |
| Station ECWT rows | 2,024 |
| Provisional rows | 2,012 |
| Blocked rows | 12 |
| Minimum provisional ECWT F | -56.421 |
| Maximum provisional ECWT F | 75.204 |

## Download Lane

Additional AWS backfill batches completed in this pass:

| Batch | Run ID | Downloaded | HTTP 404 | Bytes |
| ---: | --- | ---: | ---: | ---: |
| 5 | `noaa_backfill_download_batch5_20260623T224117Z` | 629 | 371 | 4,401,775,178 |
| 6 | `noaa_backfill_download_batch6_20260623T224814Z` | 652 | 348 | 6,091,165,197 |
| 7 | `noaa_backfill_download_batch7_20260623T225737Z` | 666 | 334 | 6,354,032,458 |

Current AWS manifest status:

| Status | Rows |
| --- | ---: |
| downloaded | 4,521 |
| failed | 2,479 |
| planned | 79,839 |

Current raw AWS cache:

| Metric | Value |
| --- | ---: |
| CSV files | 4,521 |
| `.part` files | 0 |
| Disk usage | 31 GB |

Current database size: 1,207 MB.

## Remaining Work

- Continue AWS backfill batches.
- Continue hardened loading from downloaded and inventory sources.
- Refresh station-year coverage after each meaningful load block.
- Rebuild provisional station ECWT after coverage refresh.
- Add plant station selection and populate `calc.plant_ecwt`.
