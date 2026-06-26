# Methodology

## Scope

The goal is to calculate a documented Extreme Cold Weather Temperature (ECWT) for U.S. generating plants and, where appropriate, generating units. The national plant universe comes from EIA-860. EOP-012 applicability is a narrower compliance concept, so the project keeps separate layers for:

- all EIA plants
- current operable EIA plants
- EOP-012 candidate units
- reviewed EOP-012 applicable units, if a defensible applicability review is later added

The current public dataset is a scoped plant-level analytical release, not a final Generator Owner compliance filing. It is intended to make the national calculation reproducible, reviewable, and useful for plant-by-plant follow-up. Unit-level compliance determinations, plant-owner representativeness reviews, and entity-specific applicability reviews remain downstream work.

Current publication scope:

- Include non-Alaska EIA-860 plant rows with a publication-ready ECWT under the documented automated methodology.
- Exclude Alaska from the current scoped release by project decision. Alaska plants remain in the database and can be recalculated in a separate Alaska-specific scope.
- Exclude reviewed no-station edge cases from the current publication denominator when the plant record is nonphysical, unsited, unlocatable, or otherwise not usable for automated station assignment.
- Publish the exclusions table beside the release dataset so denominator choices are explicit.

## Standards Basis

The calculation follows the EOP-012 concept of ECWT as the 0.2 percentile of hourly dry-bulb temperatures measured in December, January, and February from 2000-01-01 through the calculation date.

The compliance-facing evidence record for each accepted ECWT should identify:

- the calculation date
- source temperature data and station identifiers
- any source substitutions or adjustments used for missing or invalid hourly temperature data
- coverage evidence showing valid, missing, duplicate, invalid, and rejected observations
- the methodology and code version used for the calculation
- the published release manifest tying output files to checksums and run IDs

The EPRI guidance reviewed for this project emphasizes three operational points:

- Generator owners select the representative weather source.
- Nearby stations are usually preferred, but topography, water bodies, and local observations can justify a different station.
- Missing, duplicate, and excessive-frequency observations must be identified and handled as part of the evidence record.

This project treats the automated station selection as evidence for review, not as a substitute for Generator Owner judgment. A plant owner may choose a different representative station if it documents why that station is more representative.

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

## NOAA Source Quality Policy

NOAA Global Hourly rows are not all equivalent evidence. The canonical loader applies this source-quality policy before an observation can contribute to ECWT:

- `TMP` is parsed as tenths of degrees C. Sentinel values `+9999`, `-9999`, and `9999`, malformed `TMP` values, and TMP quality code `9` are invalid.
- NOAA `SOURCE=7` rows are rejected by default before temperature parsing.
- Other SOURCE codes are retained unless explicitly configured as reject codes for a run; accepted duplicate station-hour observations are ranked with SOURCE `4` ahead of SOURCE `6`, and SOURCE `7` last if it has not been rejected by configuration.
- When multiple accepted observations fall in the same canonical station-hour, the retained row is chosen by TMP quality rank (`1`, then `5`, then `0`, then other codes), FM report-type preference, SOURCE rank, and minute closest to 56.
- Parsed dry-bulb temperatures outside the configured plausibility window are rejected. The current publication QA window is -65 C to 40 C, with an additional SHEF-specific floor of -50 C.
- Rejected source rows, invalid TMP rows, plausibility rejects, duplicate observations, and valid loaded hours are retained as load-file and coverage evidence.

The publication QA report must disclose the exact reject-source-code set used for the run and reconcile plausibility rejects against load-file counters before release.

## Time Window

Include only observations that meet all of these conditions:

- hourly observation
- valid dry-bulb temperature
- month is December, January, or February
- timestamp is within the calculation period beginning 2000-01-01
- timestamp is on or before the calculation cutoff

Timestamp basis:

- Meteorological winter filtering is performed in station-local standard time.
- UTC is retained as the canonical storage, lineage, and de-duplication timestamp.
- `hour_local` stores the station-local hour used for DJF classification.
- `weather.station.local_standard_utc_offset_hours` records the local standard-time offset used by the loader and coverage builders.
- The current implementation derives that offset from station longitude as `round(longitude / 15)`, clamped to `[-12, 14]`. This is a deterministic standard-time approximation, not an IANA time-zone polygon lookup.

This decision is recorded in `docs/adr/0001-station-local-djf-time-basis.md`. Publication runs after this decision must use a methodology version that distinguishes them from earlier UTC-filtered runs.

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

Automated publication readiness is separate from station selection:

- Station selection ranks the candidate weather stations using plant location, station metadata, distance, and representativeness evidence.
- Publication readiness evaluates whether the selected station or documented composite series has enough valid DJF hourly data to support publication.
- A low-coverage primary station does not authorize station shopping. It either remains blocked, receives documented missing-hour treatment, or is escalated for manual review.

Automated publication candidates must pass the gates in `docs/adr/0002-publication-readiness-and-representativeness-gates.md`:

- fixed-period or fixed-composite DJF coverage ratio of at least 0.95
- at least 30,000 valid DJF hours
- selected station no more than 100 km from the plant
- selected station elevation delta no more than 300 m when elevation delta is available
- selected station metadata must not begin after 2000-01-01 for a single-station fixed-period candidate

Rows outside those gates remain analytical/provisional until station review, station segmentation, or missing-hour treatment resolves the issue.

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

Publication-readiness coverage ratios use the fixed DJF calculation period beginning 2000-01-01 through the calculation cutoff. They must not use only station-years that happen to have been loaded already, because that denominator grows during backfill and can make readiness counts move for bookkeeping reasons rather than real coverage gains.

The current national publication gate is the fixed-period current gate:

- The denominator is the full station-local DJF calculation period for the selected station or documented composite series.
- Rows are publication-ready only when fixed-period coverage meets or exceeds the configured threshold, currently 0.95, and all other sufficiency and representativeness gates pass.
- Normalized active-window loaded-year scenarios are retained as diagnostics only; they are not a publication gate.
- Blocked rows preserve the reason code, including no station candidates, no provisional station ECWT, insufficient loaded station-years, and fixed-period coverage below threshold.

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

For automated publication, secondary fill is limited to plants that already have a selected primary station and fail only because of missing valid primary-station hours. It is not used for no-station plants, Alaska exclusions, missing plant coordinates, or unresolved siting problems.

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

Publication-facing CSV exports display ECWT values to 0.1 F because NOAA Global Hourly `TMP` source values are parsed from tenths of degrees C. Higher-precision numeric values may remain in database tables for reproducibility, but public previews and release CSVs must avoid implying false precision. This export policy is recorded in `docs/adr/0003-export-context-precision-and-source-quality.md`.

## Governing ECWT

EOP-012 requires recalculation at least every five years, and the cold-weather design basis should not be raised merely because later recalculations produce a warmer percentile. Store:

- `calculated_ecwt_f` for a specific run
- `governing_ecwt_f` as the lowest accepted ECWT across accepted runs for that plant/unit

The plant-level dataset publishes the calculated ECWT for the current release. A later unit-level compliance layer should store the lowest accepted ECWT for each applicable generating unit and link each accepted calculation to the source release manifest.

## Release Manifests

Every public release should include a release manifest in both file and database form. The manifest should record:

- release ID and release name
- release generation timestamp
- calculation run IDs used for weather inventory, backfill manifest, NOAA DJF loads, coverage, station ECWT, plant ECWT, readiness, policy result, secondary fill, and scoped export
- Git commit used by the calculation run and Git commit that publishes the release artifacts
- row counts for the dataset and exclusions table
- SHA-256 checksum and byte size for each published artifact
- notes describing scope decisions, exclusions, and known limitations

The manifest is the audit bridge between GitHub and the local/Postgres build. GitHub should hold the code, methodology, reports, manifests, checksums, and compact publication files. Heavy NOAA raw data and database clusters should stay in the configured external data root.

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
