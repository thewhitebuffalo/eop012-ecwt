# Methodology

## Scope

The goal is to calculate a documented Extreme Cold Weather Temperature (ECWT) for U.S. generating plants and, where appropriate, generating units. The national plant universe comes from EIA-860. EOP-012 applicability is a narrower compliance concept, so the project keeps separate layers for:

- all EIA plants
- current operable EIA plants
- EOP-012 candidate units
- reviewed EOP-012 applicable units, if a defensible applicability review is later added

## Standards Basis

The calculation follows the EOP-012 concept of ECWT as the 0.2 percentile of hourly dry-bulb temperatures measured in December, January, and February from 2000-01-01 through the calculation date.

The EPRI guidance reviewed for this project emphasizes three operational points:

- Generator owners select the representative weather source.
- Nearby stations are usually preferred, but topography, water bodies, and local observations can justify a different station.
- Missing, duplicate, and excessive-frequency observations must be identified and handled as part of the evidence record.

## Asset Universe

Primary source:

- EIA-860 annual plant and generator data.

Current baseline:

- EIA-860 2024 final annual data.

Provisional overlay:

- EIA-860 2025 early release.

Primary keys:

- `plant_code` for plants.
- `plant_code`, `generator_id`, and source year for generator records.

Initial current plant universe:

- Plants with at least one generator in the EIA-860 `Operable` generator sheet.

Generator statuses are preserved rather than collapsed. The first ECWT plant run should include plants with `OP`, `SB`, `OA`, or `OS` operable-sheet generator records, while downstream compliance views may apply stricter filters.

## Weather Source

Primary source:

- NOAA hourly dry-bulb observations.

Weather data must preserve:

- station identifier
- observation timestamp
- temperature value
- temperature units
- source file or source table
- parse/quality flags where available

The canonical calculation temperature is Fahrenheit for publication, with Celsius retained when it is the source or intermediate value.

## Time Window

Include only observations that meet all of these conditions:

- hourly observation
- valid dry-bulb temperature
- month is December, January, or February
- timestamp is within the calculation period beginning 2000-01-01
- timestamp is on or before the calculation cutoff

The timestamp basis must be explicit. If the source timestamp is UTC, the calculation layer must define whether meteorological winter month filtering is performed in station-local time or UTC. The preferred approach is station-local time for month/day/hour coverage audits, with UTC retained as the canonical timestamp.

## Station Candidate Generation

For every included plant:

1. Generate nearby weather-station candidates from plant latitude/longitude.
2. Compute distance from plant to station.
3. Add station coverage metrics for the ECWT time window.
4. Add quality flags for missing data, duplicate hours, and invalid temperatures.
5. Retain multiple candidates per plant for audit.

Candidate ranking should initially use:

- distance
- valid DJF hourly coverage since 2000-01-01
- station start/end dates
- station data completeness
- state/region sanity checks

Later ranking can add:

- elevation difference
- coastal or large-water-body mismatch
- topographic barriers
- manual review status

## Station Selection

The default selected station is the nearest reliable representative station with adequate coverage. A farther station can be selected when documented evidence makes it more representative.

For automated provisional rebuilds, station rank and distance are treated as representative-station evidence. Loaded weather coverage is measured downstream in readiness gates and should not be used to pick a farther station merely because that station currently has more downloaded hourly observations.

If the best representative station begins after 2000-01-01, the station selection may be segmented:

- use the best representative station for its active period
- use the next-best representative station for earlier missing periods
- repeat with additional stations if needed

Every segment must be recorded with:

- plant
- station
- start timestamp
- end timestamp
- reason code
- reviewer or algorithm version

No silent station substitution is allowed.

## Missing And Excess Data

For each selected station or station segment, calculate:

- expected DJF hours
- observed valid DJF hours
- missing hours
- duplicate or excess observations
- invalid dry-bulb values
- coverage percentage
- monthly and yearly coverage breakdowns

Missing-data treatment must be explicit:

- `none`: no fill was required
- `drop`: missing hours remain missing
- `segment_substitution`: another representative station was used for a date range
- `manual_correction`: a documented correction was applied
- `not_resolved`: ECWT result is provisional or blocked

The project should publish both the ECWT result and the coverage evidence used to judge that result.

Publication-readiness coverage ratios should use a fixed selected-station active-period DJF denominator for the ECWT calculation window. They should not use only station-years that happen to have been loaded already, because that denominator grows during backfill and can make readiness counts move for bookkeeping reasons rather than real coverage gains.

## Secondary Station Fill For Missing Primary Hours

EOP-012-3 requires the calculation record to identify the ECWT calculation date, the source or sources of temperature data, and any adjustments used for missing or invalid hourly temperature data. The EPRI ECWT guidance also allows missing data from the most representative station to be supplemented from the next most representative station, provided the owner documents the station choice and missing-data treatment.

This project therefore allows a secondary weather station fill only under a documented policy:

1. The primary selected station remains the representative station.
2. Valid primary-station hourly dry-bulb observations are never overwritten.
3. A fallback station may contribute only timestamps where the primary station is missing a valid dry-bulb value.
4. The fallback station must come from the documented candidate-station set and should be the nearest candidate that makes the composite series satisfy the publication coverage threshold, unless a manual review documents a better representative choice.
5. The ECWT must be recalculated on the composite hourly series, not copied from either station's standalone ECWT.
6. The output must record primary station ID, fallback station ID, primary valid hours, fallback-filled hours, composite valid hours, expected hours, coverage before and after fill, ECWT before and after fill, and the reason for the fill.

This is an adjustment for missing or invalid data, not station shopping. A farther or colder station cannot be substituted merely to change the ECWT. If no documented fallback station resolves the missing-hour problem, the plant remains blocked or requires manual review.

## ECWT Calculation

For each selected plant or station series:

1. Build the valid hourly dry-bulb temperature series for December, January, and February from 2000-01-01 through the calculation cutoff.
2. Sort temperatures ascending.
3. Compute the continuous 0.2 percentile.
4. Also compute a discrete cold-rank audit value.

Preferred SQL expression:

```sql
percentile_cont(0.002) within group (order by dry_bulb_f)
```

Discrete audit rank:

```text
ceil(0.002 * valid_hour_count)
```

The published table should include both:

- `ecwt_f`: continuous percentile value
- `ecwt_discrete_f`: temperature at the discrete audit rank

## Governing ECWT

EOP-012 requires recalculation at least every five years, and the cold-weather design basis should not be raised merely because later recalculations produce a warmer percentile. Store:

- `calculated_ecwt_f` for a specific run
- `governing_ecwt_f` as the lowest accepted ECWT across accepted runs for that plant/unit

## Exceptions

Exceptions are not failures. They are evidence that the pipeline is honest.

Examples:

- plant has missing coordinates
- generator plant code has no plant-table match
- no station within threshold distance
- nearest station lacks sufficient coverage
- station segment decision required
- ECWT result depends on unresolved missing data

All exceptions should be published with reason codes and resolution status.
