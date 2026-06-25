# Station-Year Hourly Summary Backfill Report

Generated UTC: 2026-06-25T09:10:33+00:00

## Database

- Host: `127.0.0.1`
- Port: `5436`
- Database: `eop012`

## Run

- Calculation run ID: `station_year_hourly_summary_backfill_20260625T090647Z`
- Methodology version: `eop012-ecwt-method-v0.1.0`
- Code commit: `2b09d4f02c9280bc9bed41c41390e1131e7a8a32`
- Year range: `2000-2025`

## Summary

| Relation or Check | Rows / Value |
| --- | ---: |
| `summary station-years` | 61847 |
| `summary stations` | 4525 |
| `summary valid DJF hours` | 53192557 |
| `minimum source year` | 2000 |
| `maximum source year` | 2025 |

## Summary By Year

| Year | Station-Years | Valid DJF Hours |
| ---: | ---: | ---: |
| 2025 | 3092 | 1711201 |
| 2024 | 2768 | 2393065 |
| 2023 | 3199 | 2622751 |
| 2022 | 3209 | 2531119 |
| 2021 | 3229 | 2623223 |
| 2020 | 2946 | 2100837 |
| 2019 | 2789 | 1960143 |
| 2018 | 2784 | 1850073 |
| 2017 | 2785 | 1857478 |
| 2016 | 2438 | 1334345 |
| 2015 | 2769 | 1829693 |
| 2014 | 2785 | 2114926 |
| 2013 | 2813 | 2331271 |
| 2012 | 2770 | 2260433 |
| 2011 | 2737 | 2264509 |
| 2010 | 2680 | 2012082 |
| 2009 | 2529 | 1840799 |
| 2008 | 2395 | 1641711 |
| 2007 | 2075 | 2217742 |
| 2006 | 1972 | 1989126 |
| 2005 | 1488 | 1822731 |
| 2004 | 1425 | 2340405 |
| 2003 | 1126 | 2074261 |
| 2002 | 1106 | 1980163 |
| 2001 | 1026 | 1780508 |
| 2000 | 912 | 1707962 |

## Interpretation

- This is an operational summary of canonical loaded DJF weather rows, not a final ECWT result.
- The table lets station-year coverage refreshes read one row per station-year instead of rescanning `weather.hourly_djf`.
- Future NOAA DJF loads refresh touched station-years in this table automatically.
