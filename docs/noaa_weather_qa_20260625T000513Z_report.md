# NOAA Loaded Weather QA Report

Generated UTC: 2026-06-25T00:06:59+00:00

## Run

- QA report ID: `noaa_weather_qa_20260625T000513Z`
- Code commit: `cf510337201a437077bcbcb8697a0b7d3800a809`
- Station ECWT run ID: `station_ecwt_loaded_20260624T205220Z`
- Strict readiness run ID: `plant_ecwt_readiness_20260624T210010Z`
- Plausibility temperature window C: `-65.0` to `40.0`
- Rejected NOAA SOURCE codes before plausibility reconstruction: `['7']`
- Plausibility reject detail CSV: `noaa_weather_qa_20260625T000513Z_plausibility_rejects.csv`

## Plausibility Rejects

| Metric | Count |
| --- | ---: |
| Loaded files with plausibility rejects | 35 |
| DB counted plausibility rejects | 877 |
| Reconstructed plausibility reject rows | 888 |
| Reconstructed minus DB count | 11 |
| Files with count mismatches | 2 |

### Count Mismatches

| Station | Year | Load Run | DB Rows | Reconstructed Rows | Delta |
| --- | --- | --- | --- | --- | --- |
| 994973-99999 | 2019 | noaa_hourly_djf_load_20260624T025109Z | 65 | 71 | 6 |
| 994973-99999 | 2020 | noaa_hourly_djf_load_20260624T020025Z | 8 | 13 | 5 |

### By Reason

| Reason | Rows |
| --- | --- |
| above_max_temp_c | 803 |
| below_min_temp_c | 65 |
| below_shef_min_temp_c | 20 |

### Top Stations By Rejected Rows

| Station | Rows |
| --- | --- |
| 722133-99999 | 262 |
| 720319-99999 | 193 |
| 700637-27406 | 176 |
| 994973-99999 | 84 |
| 701940-99999 | 80 |
| 720966-00339 | 23 |
| 703830-25310 | 16 |
| 720401-00133 | 13 |
| 690190-99999 | 7 |
| 714630-99999 | 5 |
| 722201-03723 | 4 |
| 720267-23224 | 3 |
| 691334-99999 | 2 |
| 723096-93727 | 2 |
| 726588-04956 | 2 |

### Top Load Runs By Rejected Rows

| Load Run | Rows |
| --- | --- |
| noaa_hourly_djf_load_20260624T114227Z | 262 |
| noaa_hourly_djf_load_20260624T094258Z | 179 |
| noaa_hourly_djf_load_20260624T195519Z | 176 |
| noaa_hourly_djf_load_20260624T124513Z | 80 |
| noaa_hourly_djf_load_20260624T025109Z | 71 |
| noaa_hourly_djf_load_20260624T084828Z | 35 |
| noaa_hourly_djf_load_20260624T020025Z | 15 |
| noaa_hourly_djf_load_20260624T111630Z | 14 |
| noaa_hourly_djf_load_20260624T002205Z | 14 |
| noaa_hourly_djf_load_20260624T133502Z | 7 |

## Canonical Weather Guardrails

| Metric | Count |
| --- | ---: |
| Canonical DJF hourly rows | 50346347 |
| Rows outside absolute C window | 0 |
| SHEF canonical hourly rows | 15655 |
| SHEF rows below SHEF floor | 0 |
| Minimum dry bulb C | -59.000 |
| Maximum dry bulb C | 40.000 |
| Minimum dry bulb F | -74.200 |
| Maximum dry bulb F | 104.000 |

## Loader Policy Audit

| Metric | Count |
| --- | ---: |
| Loaded file rows | 62318 |
| Distinct loader commits represented | 42 |
| Loaded file rows missing source SHA-256 | 0 |
| Historical plausibility reject rows | 877 |
| First load run started UTC | 2026-06-23 15:46:25-07 |
| Last load run started UTC | 2026-06-24 13:33:14-07 |

## Warm Station ECWT Outliers

| Metric | Count |
| --- | ---: |
| Provisional station ECWT rows | 4057 |
| Provisional station rows with < 24 valid hours | 71 |
| Provisional station rows with < 2,000 valid hours | 392 |
| Provisional station rows with ECWT >= 60 F | 23 |
| Provisional station rows with ECWT >= 80 F | 5 |

### Warmest Station ECWT Rows

| Station | Name | State | Valid Hours | Expected Hours | ECWT F | Selected Plants | Strict Candidate Plants |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 727500-99999 | PEQUOT LAKE  MN |  | 1 | 6528 | 100.400 | 0 | 0 |
| 747350-99999 | JAYTON  TX. | TX | 1 | 2160 | 88.160 | 21 | 0 |
| 700365-99999 | SAGWON | AK | 1 | 2160 | 87.980 | 0 | 0 |
| 703880-99999 | CAPE DECISION(AMOS) | AK | 1 | 8688 | 83.120 | 0 | 0 |
| 745000-99999 | SHERIDAN  CA |  | 1 | 2160 | 83.120 | 2 | 0 |
| 911803-99999 | HICKAM AFB | HI | 3 | 15144 | 78.820 | 1 | 0 |
| 912930-99999 | SOUTH KONA  HAWAII   HAWAII |  | 1 | 2184 | 78.800 | 2 | 0 |
| 722330-99999 | SLIDELL/MUN. LA | LA | 1 | 4320 | 73.940 | 0 | 0 |
| 911690-99999 | WAIALEE  OAHU   HAWAII |  | 1 | 2184 | 71.960 | 6 | 0 |
| 725010-99999 | UPTON | NY | 1 | 6480 | 66.020 | 12 | 0 |
| 911975-21510 | KONA INTL AT KEAHOLE ARPT | HI | 3170 | 43320 | 66.020 | 1 | 0 |
| 997173-99999 | KAWAIHAE | HI | 23143 | 28152 | 65.480 | 6 | 0 |
| 911907-99999 | HANA | HI | 657 | 21672 | 64.400 | 1 | 0 |
| 994007-99999 | HONOLULU | HI | 32825 | 36816 | 64.400 | 2 | 0 |
| 998193-99999 | MOKUOLOE | HI | 25523 | 34632 | 64.040 | 0 | 0 |
| 721038-99999 | JORDAN FLD ARPT | NC | 1 | 17352 | 62.600 | 15 | 0 |
| 911760-22519 | KANEOHE MCAS | HI | 17968 | 56328 | 62.600 | 0 | 0 |
| 998191-99999 | HILO | HI | 28376 | 36816 | 62.195 | 5 | 0 |
| 997384-99999 | MOLUOLOE | HI | 32690 | 36816 | 61.700 | 6 | 0 |
| 724870-03163 | CALIENTE (AMOS) | NV | 1 | 2184 | 61.520 | 0 | 0 |

### Highest-ECWT Station Observation Sample

| Station | Hour UTC | Dry Bulb F | Dry Bulb C | Quality Flags | Source File |
| --- | --- | --- | --- | --- | --- |
| 727500-99999 | 2000-02-21 07:00:00-08 | 100.400 | 38.000 | tmp_quality:1|report_type:FM-12|source:4|qc:V020 | noaa_global_hourly_csv_2000_72750099999_3658eeaa6ff373e8 |

## Interpretation

- Plausibility rejects are reconstructed from source CSV files because the canonical loader currently stores reject counts by file, not row-level reject details.
- Reject reconstruction is scoped to files with historical reject counts; it is a reconciliation check, not a full raw-cache scan.
- Count mismatches mean the current parser policy does not reproduce historical per-file load statistics. In this rebuild, the observed mismatches are compatible with earlier load runs that predated the current SHEF-specific temperature floor.
- The canonical weather guardrails test the rows actually available to ECWT. Publication should block if canonical rows violate the absolute temperature window or if SHEF rows below the SHEF floor are present.
- The warmest station ECWT row is driven by a station with one valid DJF hour. The strict plant readiness gate prevents such low-hour stations from becoming publication candidates, but station-level provisional outputs still need QA flags.
- The presence of warm station ECWT outliers reinforces that publication should use `calc.plant_ecwt_readiness` strict candidates, not raw provisional station or plant ECWT rows.
