# ADR 0001: Station-Local DJF Time Basis

## Status

Accepted

## Date

2026-06-25

## Context

EOP-012 ECWT is based on December, January, and February hourly dry-bulb temperatures. That is a local meteorological winter concept: a station's pre-dawn cold tail belongs to the station's local calendar day and month, even though NOAA Global Hourly timestamps are stored in UTC.

The earlier loader filtered DJF months using UTC timestamps and left `hour_local` empty. That could move boundary hours at the start and end of December, January, and February into or out of scope for stations outside UTC.

## Decision

Use station-local standard time for DJF month and source-year classification. Keep UTC as the canonical storage and de-duplication key.

Implementation rules:

- `weather.hourly_djf.hour_ending_utc` remains the canonical station-hour key.
- `weather.hourly_djf.hour_local` stores the station-local standard-time hour used for DJF filtering.
- `weather.station.local_standard_utc_offset_hours` stores the local standard offset used by the loader and coverage builders.
- Current offset values are derived deterministically from station longitude as `round(longitude / 15)`, clamped to `[-12, 14]`.
- Station-year summaries group by `extract(year from hour_local)` and include only rows where `extract(month from hour_local)` is in December, January, or February.
- Station-year expected-hour denominators use the same local standard offset so numerator and denominator share the same calendar basis.

## Consequences

This changes ECWT values for stations with observations near DJF month boundaries and requires a new methodology version for regenerated results.

The longitude-derived offset is intentionally deterministic and dependency-free. It is not a full IANA time zone model and does not apply daylight-saving transitions. That is acceptable for this ECWT policy because DJF is evaluated in standard time and the cold tail is not defined by civil daylight-saving rules. A future methodology version may replace this with a true time-zone polygon lookup if the project adopts that dependency and records the source.

Historical runs using UTC filtering remain traceable under their original methodology version. New publication candidates must be regenerated under the station-local DJF policy before release.
