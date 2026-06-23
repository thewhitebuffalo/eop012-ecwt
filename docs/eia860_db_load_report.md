# EIA-860 Database Load Report

Generated UTC: 2026-06-23T20:21:12+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`
- Cluster path: `/Volumes/NOAA_CACHE/EOP012/postgres16`

## Run

- Calculation run ID: `eia860_2024_asset_load_20260623T202109Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `897af0202a1d5284f6d3c8e9ba2ba297f155fdc1`
- Source release: `eia8602024`

## Source Files

| Source file ID | File | Size bytes | SHA-256 |
| --- | --- | ---: | --- |
| `eia860_2024_zip` | `eia8602024.zip` | 22100342 | `0aaae04812cd4ab87a3e346bdf93848a3cc15053fd4dc2a4cf82d2aeac95f12b` |
| `eia860_2024_utility_xlsx` | `1___Utility_Y2024.xlsx` | 529925 | `1007d4f80b3b4d396a571f6d8a189c1ee133bd8e7810cfeb6970143432fe0fd9` |
| `eia860_2024_plant_xlsx` | `2___Plant_Y2024.xlsx` | 4314211 | `a7b4db94a337b1a7a0f29505a5aad9981b16173c366fbf94ad52c0b0a935f71d` |
| `eia860_2024_generator_xlsx` | `3_1_Generator_Y2024.xlsx` | 10724073 | `249607e986846dcc9326b6583cef5d376f1c2421339957a75b93546d133b76c8` |
| `eia860_2024_layout_xlsx` | `LayoutY2024.xlsx` | 130662 | `f2e1cd7b3a4752e39adde230de803c35e4327484c781c9649df53a6ed3237b73` |

## Mapped Row Counts

| Mapped table | Rows |
| --- | ---: |
| `utility` | 6643 |
| `plant` | 16132 |
| `generator` | 34855 |
| `exceptions` | 29 |

## Database Row Counts

| Database relation | Rows |
| --- | ---: |
| `audit.source_file` | 5 |
| `audit.calculation_run` | 1 |
| `asset.utility` | 6643 |
| `asset.plant` | 16132 |
| `asset.generator` | 34855 |
| `audit.exception_log` | 29 |

## Exceptions Loaded

| Reason code | Count |
| --- | ---: |
| `plant_missing_coordinates` | 28 |
| `generator_plant_code_not_in_plant_table` | 1 |

## Notes

- The database contains the EIA-860 2024 final asset universe only; NOAA station matching has not been loaded yet.
- The known generator anomaly is plant code `68815`, which appears in the generator file but not the plant file.
- Plants with missing coordinates are loaded but cannot enter automated NOAA station matching until resolved.
