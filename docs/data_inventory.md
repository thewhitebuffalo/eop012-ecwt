# EIA-860 Asset Inventory

Generated UTC: 2026-06-23T19:35:54+00:00

## Source

- ZIP: `/Users/Shared/EOP012/EIA_860_raw_downloads/intake/eia8602024.zip`
- Release label: `eia8602024`
- SHA-256: `0aaae04812cd4ab87a3e346bdf93848a3cc15053fd4dc2a4cf82d2aeac95f12b`
- Baseline use: 2024 final annual data should be treated as the current authoritative baseline until final 2025 EIA-860 data is published.

## ZIP Members Used

- plant: `2___Plant_Y2024.xlsx`
- generator: `3_1_Generator_Y2024.xlsx`
- utility: `1___Utility_Y2024.xlsx`
- layout: `LayoutY2024.xlsx`

## Core Counts

| Metric | Count |
| --- | ---: |
| Plant rows | 16132 |
| Distinct plant codes | 16132 |
| Utility rows | 6643 |
| Field dictionary rows | 376 |
| Generator rows, all sheets | 34855 |
| Operable generator rows | 26855 |
| Plants with at least one operable generator | 13371 |
| Plant rows without operable generator | 2762 |

## Coordinate Quality

| Coordinate check | Count |
| --- | ---: |
| Valid numeric lat/lon | 16104 |
| Missing/non-numeric lat/lon | 28 |
| Outside valid lat/lon range | 0 |

## Generator Sheets

| Sheet | Rows | Distinct plants | Missing plant code | Missing generator ID |
| --- | ---: | ---: | ---: | ---: |
| Operable | 26855 | 13371 | 0 | 0 |
| Proposed | 2408 | 1831 | 0 | 0 |
| Retired and Canceled | 5592 | 2110 | 0 | 0 |

## Operable Generator Status Counts

| Value | Count |
| --- | ---: |
| `OP` | 24662 |
| `SB` | 1511 |
| `OS` | 479 |
| `OA` | 203 |

## Plant Sector Counts

| Value | Count |
| --- | ---: |
| `IPP Non-CHP` | 10470 |
| `Electric Utility` | 4078 |
| `Commercial Non-CHP` | 493 |
| `Industrial CHP` | 451 |
| `Industrial Non-CHP` | 230 |
| `Commercial CHP` | 219 |
| `IPP CHP` | 191 |

## Plant State Counts

| Value | Count |
| --- | ---: |
| `CA` | 2171 |
| `TX` | 1368 |
| `NY` | 1215 |
| `NC` | 988 |
| `MN` | 837 |
| `MA` | 700 |
| `IL` | 566 |
| `NJ` | 427 |
| `FL` | 405 |
| `CO` | 342 |
| `MI` | 332 |
| `IA` | 331 |
| `PA` | 324 |
| `OR` | 321 |
| `VA` | 317 |
| `GA` | 315 |
| `WI` | 292 |
| `ME` | 269 |
| `IN` | 269 |
| `OH` | 262 |
| `SC` | 259 |
| `MD` | 246 |
| `AZ` | 231 |
| `KS` | 212 |
| `CT` | 201 |
| `NM` | 182 |
| `WA` | 172 |
| `OK` | 167 |
| `MO` | 164 |
| `ID` | 160 |
| `AK` | 157 |
| `NV` | 147 |
| `UT` | 147 |
| `AR` | 145 |
| `NE` | 141 |
| `LA` | 128 |
| `VT` | 124 |
| `TN` | 124 |
| `RI` | 109 |
| `AL` | 104 |
| `HI` | 93 |
| `KY` | 92 |
| `WY` | 90 |
| `MS` | 88 |
| `MT` | 83 |
| `ND` | 71 |
| `SD` | 62 |
| `NH` | 61 |
| `WV` | 56 |
| `DE` | 43 |
| `DC` | 22 |

## Top Operable Technologies

| Value | Count |
| --- | ---: |
| `Solar Photovoltaic` | 7142 |
| `Conventional Hydroelectric` | 3978 |
| `Petroleum Liquids` | 3864 |
| `Natural Gas Fired Combustion Turbine` | 2225 |
| `Natural Gas Fired Combined Cycle` | 1941 |
| `Natural Gas Internal Combustion Engine` | 1789 |
| `Onshore Wind Turbine` | 1560 |
| `Landfill Gas` | 1227 |
| `Batteries` | 777 |
| `Natural Gas Steam Turbine` | 556 |
| `Conventional Steam Coal` | 459 |
| `Wood/Wood Waste Biomass` | 288 |
| `Other Waste Biomass` | 192 |
| `Other Natural Gas` | 181 |
| `Geothermal` | 163 |
| `Hydroelectric Pumped Storage` | 150 |
| `Nuclear` | 96 |
| `All Other` | 79 |
| `Municipal Solid Waste` | 74 |
| `Other Gases` | 70 |
| `Petroleum Coke` | 20 |
| `Solar Thermal without Energy Storage` | 9 |
| `Flywheels` | 5 |
| `Coal Integrated Gasification Combined Cycle` | 3 |
| `Solar Thermal with Energy Storage` | 3 |
| `Offshore Wind Turbine` | 3 |
| `Natural Gas with Compressed Air Storage` | 1 |

## Top Operable Prime Movers

| Value | Count |
| --- | ---: |
| `PV` | 7142 |
| `IC` | 6404 |
| `HY` | 3978 |
| `GT` | 2793 |
| `ST` | 1734 |
| `WT` | 1560 |
| `CT` | 1249 |
| `BA` | 777 |
| `CA` | 685 |
| `FC` | 186 |
| `PS` | 150 |
| `BT` | 101 |
| `CS` | 65 |
| `OT` | 19 |
| `FW` | 5 |
| `CP` | 3 |
| `WS` | 3 |
| `CE` | 1 |

## Reconciliation Checks

- Generator plant codes not found in plant table: 1
  - First 25: `68815`
- Operable plant codes not found in plant table: 1
  - First 25: `68815`

## ECWT Implications

- Use `Plant Code` as the primary plant key for station matching.
- Use plant latitude/longitude for initial NOAA station candidate generation.
- Use the Operable generator sheet as the first current equipment universe; refine EOP-012 applicability later.
- Keep retired/canceled and proposed units out of the main current ECWT output, but retain them as separate auditable layers.
- Before ECWT calculation, every included plant must have a coordinate, selected representative weather station path, expected-hour count, valid-hour count, and missing/excess-data flag.
