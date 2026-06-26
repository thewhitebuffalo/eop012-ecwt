# NOAA Hourly Source Sufficiency Findings For EOP-012 ECWT

- Status: analysis snapshot for future white paper drafting
- Snapshot date: 2026-06-26
- Repository: `thewhitebuffalo/eop012-ecwt`
- Latest policy result run reviewed: `plant_ecwt_policy_result_all_plants_fixed_period_current_gate_20260626T115343Z`

## Finding

The current NOAA public hourly weather source set as ingested by this project is not sufficient, by itself, to support a national automated auditable ECWT dataset for NERC EOP-012 under the current fixed-period gates.

This does not mean every NOAA product has been exhausted. It means the current NOAA Global Hourly / ISD-based build, using the current single-primary-station fixed-period methodology, produces too few auditable plant-level ECWT records and leaves too many plants dependent on distant stations, incomplete fixed-period records, or unresolved station candidates.

The current run covers 16,132 plant rows. Only 278 rows pass the current automated fixed-period gates using the 100 km station-distance threshold. Only 22 rows pass when the primary station is required to be within 25 km.

The practical conclusion for the white paper is direct: a compliance-facing national ECWT product cannot be supported from the current ingested NOAA hourly dataset alone without adding more weather sources, documented station segmentation, secondary-source fill, entity-provided records, or another auditable missing-data methodology.

## NERC Context

The NERC EOP-012 technical rationale describes ECWT as a winter-season low-tail temperature statistic and recognizes that acceptable temperature sources may include, for example, NWS/NOAA weather stations, FAA weather stations, and Environment and Climate Change Canada locations for Canadian entities.

It also points to NOAA/NCEI Climate Data Online and climate normals as public resources, but it does not require that every ECWT record come from the single nearest NOAA station or from NOAA alone.

For white paper purposes, the important interpretation is:

- EOP-012 needs a temperature record that is defensible for the generating site.
- Source identity alone is not enough. The weather source must also be spatially representative, complete enough for the ECWT period, and auditable.
- When the nearest or most representative station has missing data, the method must document the source selection and any missing-data treatment. Silent substitution with a farther complete station is not acceptable.

Primary source for this requirement context:

- NERC Project 2024-03 technical rationale PDF: https://www.nerc.com/globalassets/standards/projects/2024-03/2024-03-_technical-rationale_clean_321-posting---updated_021025.pdf

## Current Automated Gates

The current repository policy is documented in `docs/adr/0002-publication-readiness-and-representativeness-gates.md` and `docs/methodology.md`.

A row passes the current automated fixed-period gate only when:

- fixed-period or fixed-composite DJF coverage ratio is at least 0.95
- valid DJF hour count is at least 30,000
- selected station distance is no more than 100 km
- selected station elevation delta is no more than 300 m when an elevation delta is available
- selected station metadata does not begin after 2000-01-01 for a single-station fixed-period candidate
- the row uses the station-local DJF time basis

Rows outside those gates may still have diagnostic ECWT values. They are not release-ready compliance outputs under the current method.

## Latest Run Summary

Policy result run:

`plant_ecwt_policy_result_all_plants_fixed_period_current_gate_20260626T115343Z`

Summary counts:

| Measure | Count | Share of all rows |
|---|---:|---:|
| Total plant rows | 16,132 | 100.0% |
| Rows with an ECWT value | 16,104 | 99.8% |
| Rows passing current automated gates, <=100 km | 278 | 1.7% |
| Rows passing coverage/hour gates and <=25 km | 22 | 0.1% |
| Rows with selected station >100 km | 12,182 | 75.5% |

Reason-code breakdown:

| Readiness status | Reason code | Rows | Interpretation |
|---|---|---:|---|
| `blocked` | `fixed_period_coverage_below_threshold` | 14,236 | Selected station has an ECWT value but fails the full fixed-period DJF coverage gate. |
| `blocked` | `station_distance_exceeds_representativeness_gate` | 1,590 | Selected station passes coverage/hour gates but is more than 100 km from the plant. |
| `publication_candidate` | `passes_current_fixed_period_gate` | 278 | Row passes the current automated fixed-period gates. |
| `blocked` | `no_station_candidates` | 28 | No station candidate was available in the current source set. |

Distance and coverage intersection:

| Distance bucket | Coverage bucket | Rows |
|---|---|---:|
| `<=25km` | coverage pass | 22 |
| `<=25km` | coverage fail | 265 |
| `25-100km` | coverage pass | 256 |
| `25-100km` | coverage fail | 3,379 |
| `>100km` | coverage pass | 1,590 |
| `>100km` | coverage fail | 10,592 |
| no station or distance | no ECWT | 28 |

Among the 278 rows passing the current 100 km gate:

| Selected station distance | Passing rows |
|---|---:|
| `<=25 km` | 22 |
| `25-50 km` | 43 |
| `50-100 km` | 213 |

## Interpretation

The current run fails as a national compliance-ready product for two separate reasons.

First, many stations are too far from the generating site. The current result has 12,182 rows with selected station distance greater than 100 km. Even though those rows may have diagnostic ECWT values, that distance profile is not defensible as an automated national publication result without additional representativeness review, documented source substitution, or a better nearby source.

Second, many closer stations do not have complete enough fixed-period DJF data. There are 3,644 rows within 100 km that fail the coverage/hour gates, including 265 rows within 25 km. This means the problem is not only station density; it is also fixed-period hourly record completeness.

The 278 passing rows should therefore be described as "rows passing the current automated gates," not as a final compliance universe. The label `publication_candidate` is an internal status in the current code and should not be used in white paper prose without definition.

## White Paper Claim Supported By This Snapshot

Supported claim:

> In the current EOP-012 ECWT build, the publicly available NOAA hourly data source set ingested by the project is not sufficient on its own to produce an auditable national plant-level ECWT dataset under conservative fixed-period coverage and station-distance gates. Of 16,132 plant rows, only 278 pass the current automated 100 km fixed-period gates, and only 22 pass when the primary station is required to be within 25 km.

Important qualification:

> This finding applies to the current ingested NOAA hourly source set and current single-primary-station fixed-period method. It does not prove that all NOAA/NCEI products are insufficient, nor does it evaluate all possible FAA, ECCC, mesonet, entity-owned, or composite-station approaches.

## Source Expansion Required

The next phase should evaluate additional data sources and methods against the same audit gates rather than relaxing the gates to increase the count.

Recommended source layers:

| Source layer | Why it matters | Audit concern |
|---|---|---|
| NOAA/NCEI GHCNh | NOAA describes GHCNh as a next-generation hourly climate dataset intended to integrate and improve hourly station records. | Must compare station IDs, continuity, QA flags, and overlap with existing ISD/Global Hourly records. |
| NOAA/NCEI LCD / ASOS / AWOS | LCD and ASOS/AWOS may improve usable hourly airport station coverage and FAA-relevant observations. | Must verify fixed-period completeness, temperature field definitions, station moves, and lineage. |
| ECCC hourly climate data | Canadian stations may be closer and more representative for northern U.S. border plants and Canadian entities. | Must normalize units, timestamps, station metadata, and missing-data flags. |
| FAA station data not already represented in NCEI products | Some FAA/AWOS sources may fill gaps where NOAA hourly archives are incomplete. | Must prove public availability, lineage, QA treatment, and station continuity. |
| MADIS / mesonet data | Could materially increase station density. | Provider restrictions, QA levels, continuity, siting, and auditability need strict review. |
| Entity-owned or site-specific weather records | May be the most representative data for specific plants. | Requires owner documentation, calibration/QA evidence, and repeatable missing-data treatment. |

Reference starting points:

- NOAA/NCEI Local Climatological Data: https://www.ncei.noaa.gov/products/land-based-station/local-climatological-data
- NOAA/NCEI ASOS/AWOS: https://www.ncei.noaa.gov/products/land-based-station/automated-surface-weather-observing-systems
- NOAA/NCEI GHCNh article: https://www.ncei.noaa.gov/news/next-generation-climate-dataset-built-seamless-integration
- ECCC Historical Climate Data: https://climate.weather.gc.ca/historical_data/search_historic_data_e.html
- NOAA MADIS surface data: https://madis.ncep.noaa.gov/madis_sfc.shtml

## Recommended Next Analytical Artifacts

The white paper should not rely only on the aggregate 278 count. The following artifacts should be generated and preserved:

1. A station-source coverage comparison table by source family: NOAA Global Hourly/ISD, GHCNh, LCD/ASOS/AWOS, ECCC, MADIS, and any entity-provided data.
2. A plant-level pass/fail matrix showing how many plants pass under each source layer and distance threshold.
3. A distance-to-nearest-qualified-station distribution for 25 km, 50 km, and 100 km thresholds.
4. A fixed-period DJF coverage distribution for the nearest station, selected primary station, and best available station within each radius.
5. A documented composite-station experiment that preserves the primary representative station and fills only missing periods with auditable secondary sources.
6. A state and NERC-region summary to show where NOAA-only gaps are concentrated.

## Reproduction Queries

The following SQL was used against the local EOP012 PostgreSQL database on port 5436.

Reason-code breakdown:

```sql
select
  readiness_status,
  reason_code,
  count(*) rows,
  count(*) filter (where selected_station_distance_km > 100) station_over_100km,
  count(*) filter (where selected_station_distance_km <= 25) station_within_25km,
  count(*) filter (where selected_station_distance_km <= 100) station_within_100km,
  count(*) filter (where fixed_coverage_ratio >= 0.95) fixed_coverage_pass,
  count(*) filter (where ecwt_f is not null) has_ecwt
from calc.plant_ecwt_policy_result
where policy_result_run_id = 'plant_ecwt_policy_result_all_plants_fixed_period_current_gate_20260626T115343Z'
group by readiness_status, reason_code
order by rows desc;
```

Distance and coverage intersection:

```sql
select
  case
    when selected_station_distance_km is null then 'no_station_or_distance'
    when selected_station_distance_km <= 25 then '<=25km'
    when selected_station_distance_km <= 100 then '25-100km'
    else '>100km'
  end as distance_bucket,
  case
    when fixed_coverage_ratio >= 0.95 and valid_hour_count >= 30000 then 'coverage_pass'
    when ecwt_f is null then 'no_ecwt'
    else 'coverage_fail'
  end as coverage_bucket,
  count(*) rows
from calc.plant_ecwt_policy_result
where policy_result_run_id = 'plant_ecwt_policy_result_all_plants_fixed_period_current_gate_20260626T115343Z'
group by 1, 2
order by distance_bucket, coverage_bucket;
```

Headline count query:

```sql
select
  count(*) total_rows,
  count(*) filter (where ecwt_f is not null) rows_with_ecwt,
  count(*) filter (
    where readiness_status = 'publication_candidate'
      and reason_code = 'passes_current_fixed_period_gate'
  ) automated_gate_pass,
  count(*) filter (
    where selected_station_distance_km <= 25
      and fixed_coverage_ratio >= 0.95
      and valid_hour_count >= 30000
      and ecwt_f is not null
  ) pass_within_25km,
  count(*) filter (
    where selected_station_distance_km <= 100
      and fixed_coverage_ratio >= 0.95
      and valid_hour_count >= 30000
      and ecwt_f is not null
  ) pass_within_100km,
  count(*) filter (where selected_station_distance_km > 100) station_over_100km
from calc.plant_ecwt_policy_result
where policy_result_run_id = 'plant_ecwt_policy_result_all_plants_fixed_period_current_gate_20260626T115343Z';
```

## Open Issues

- The current source sufficiency finding has not yet been tested against GHCNh, LCDv2, ECCC, MADIS, or entity-provided site data.
- The current run does not by itself resolve whether a documented composite-station method can raise the auditable count while staying defensible.
- The current 100 km gate is an automated representativeness threshold, not a guarantee that every station inside 100 km is representative.
- A stricter 25 km gate yields only 22 passing rows and should be treated as a sensitivity result, not the current repository publication policy unless formally adopted.
