#!/usr/bin/env python3
"""Pure, dependency-free core helpers for the observational ECWT calculation.

These implement the calculation exactly as described in NERC's "Calculating
Extreme Cold Weather Temperature" (Dec 2024) companion document and the
EOP-012-3 technical rationale (Project 2024-03, March 2025), using only the
Python standard library so they are trivially unit-testable and cheap to run.

Scope is set by docs/adr/0004-observational-source-hierarchy-and-adequacy.md:

- Observational station data only (NOAA Global Hourly / LCD / ASOS). No
  reanalysis or modeled data.
- ECWT = continuous 0.2 percentile of hourly DJF dry-bulb temperatures since
  2000-01-01, matching Excel ``PERCENTILE.INC(range, 0.002)`` and SQL
  ``percentile_cont(0.002)``.
- Publication adequacy (docs/adr/0005): every expected winter hour counts equally
  (no time-of-day weighting); an ECWT is publishable only when at least
  MIN_PUBLISH_COVERAGE (default 0.95) of the expected DJF hours are populated.
  Below that floor the plant is held, not published.
- Every contributing hour carries provenance: tower/station id, timestamp, and
  source channel, so any published ECWT hour is traceable to a checksummed file.

None of these functions touch a database or the network; the DB/ingestion glue
lives in the pipeline scripts that call them.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import date, timedelta

DJF_MONTHS = (12, 1, 2)
ECWT_PERCENTILE = 0.002  # lowest 0.2 percentile
CALC_PERIOD_START = date(2000, 1, 1)

# ADR-0005 publication floor. Every expected DJF winter hour counts equally (no
# time-of-day weighting); an ECWT is publishable only when at least this fraction
# of the expected winter hours is populated. Below the floor the plant is held.
COMPLETE_COVERAGE = 0.99
MIN_PUBLISH_COVERAGE = 0.95


# --------------------------------------------------------------------------- #
# ECWT statistic
# --------------------------------------------------------------------------- #
def ecwt_percentile(temps) -> float:
    """Continuous 0.2-percentile ECWT.

    Matches Excel ``PERCENTILE.INC(range, 0.002)`` and SQL
    ``percentile_cont(0.002)``: linear interpolation between the two closest
    ranks of the ascending series (0-indexed rank = p * (n - 1)).
    """
    xs = sorted(t for t in temps if t is not None)
    n = len(xs)
    if n == 0:
        raise ValueError("ecwt_percentile: empty series")
    if n == 1:
        return float(xs[0])
    rank = ECWT_PERCENTILE * (n - 1)
    lo = math.floor(rank)
    frac = rank - lo
    if lo + 1 < n:
        return float(xs[lo] + frac * (xs[lo + 1] - xs[lo]))
    return float(xs[lo])


def ecwt_discrete_rank_temp(temps) -> float:
    """Temperature at the discrete cold rank ``ceil(0.002 * n)`` (1-indexed
    coldest). Mirrors the companion doc's "lowest ~100 of ~50,000" audit value.
    """
    xs = sorted(t for t in temps if t is not None)
    n = len(xs)
    if n == 0:
        raise ValueError("ecwt_discrete_rank_temp: empty series")
    k = max(1, math.ceil(ECWT_PERCENTILE * n))
    return float(xs[k - 1])


# --------------------------------------------------------------------------- #
# Expected DJF hours (data-sufficiency denominator)
# --------------------------------------------------------------------------- #
def expected_djf_hours(calc_date: date, start: date = CALC_PERIOD_START) -> int:
    """Expected DJF hours from ``start`` through ``calc_date`` inclusive.

    Defined as (number of calendar days in December/January/February within
    ``[start, calc_date]``) * 24. This reproduces the companion document's
    worked example exactly: ``expected_djf_hours(date(2024, 3, 1))`` == 53424.

    Runs once per calculation (not per plant-hour), so the simple day walk is
    intentionally readable rather than micro-optimized.
    """
    days = 0
    d = start
    step = timedelta(days=1)
    while d <= calc_date:
        if d.month in DJF_MONTHS:
            days += 1
        d += step
    return days * 24


# --------------------------------------------------------------------------- #
# Adequacy / missing-data assessment (confidence tiers, not a rigid gate)
# --------------------------------------------------------------------------- #
@dataclass
class Adequacy:
    n: int
    expected_hours: int
    missing_hours: int
    coverage: float            # populated / expected, capped at 1.0
    ecwt_f: float
    ecwt_discrete_f: float
    tail_hours: int            # observed hours <= ecwt_f (the cold tail that sets ECWT)
    confidence_tier: str       # complete | adequate | provisional_review | blocked_no_data
    publishable: bool          # True only when coverage meets the publish floor
    needs_review: bool
    reason: str


def assess_adequacy(
    temps,
    expected_hours: int,
    *,
    min_publish_coverage: float = MIN_PUBLISH_COVERAGE,
    complete_coverage: float = COMPLETE_COVERAGE,
) -> Adequacy:
    """Assess winter-hour coverage and decide whether the ECWT is publishable.

    Per docs/adr/0005: the goal for every plant is to populate ALL expected winter
    (DJF) hours since 2000 -- every hour, with no time-of-day weighting. An ECWT is
    publishable only when coverage (populated / expected) meets the publish floor
    (default 0.95). Below the floor the plant is HELD: the diagnostic value is
    still returned, but ``publishable`` is False and it must NOT be written to the
    public ECWT field. Zero data is blocked. This replaces ADR-0004's permissive
    "every plant with any valid data receives an ECWT value".
    """
    xs = [t for t in temps if t is not None]
    n = len(xs)
    if expected_hours <= 0:
        raise ValueError("assess_adequacy: expected_hours must be positive")
    if n == 0:
        return Adequacy(0, expected_hours, expected_hours, 0.0,
                        float("nan"), float("nan"), 0,
                        "blocked_no_data", False, True, "no valid DJF hours")
    ecwt = ecwt_percentile(xs)
    disc = ecwt_discrete_rank_temp(xs)
    missing = max(0, expected_hours - n)
    coverage = min(1.0, n / expected_hours)
    tail = sum(1 for t in xs if t <= ecwt)
    if coverage >= complete_coverage:
        tier, publishable, reason = ("complete", True,
                                     "winter hours essentially fully populated")
    elif coverage >= min_publish_coverage:
        tier, publishable, reason = ("adequate", True,
                                     "winter hours populated at or above the publish floor")
    else:
        tier, publishable, reason = ("provisional_review", False,
                                     f"only {coverage:.1%} of expected winter hours populated; "
                                     f"below the {min_publish_coverage:.0%} publish floor -- held, not published")
    return Adequacy(n, expected_hours, missing, round(coverage, 4),
                    round(ecwt, 1), round(disc, 1), tail, tier, publishable,
                    not publishable, reason)


# --------------------------------------------------------------------------- #
# Composite series + per-hour provenance (audit trail)
# --------------------------------------------------------------------------- #
@dataclass
class HourObs:
    """One canonical station-hour with full provenance.

    hour_ending_utc is the canonical de-dup key; source_file_id resolves to
    audit.source_file (SHA-256 + download/load run + git commit).
    """
    hour_ending_utc: str
    dry_bulb_f: float
    station_id: str            # "tower number", e.g. USAF-WBAN 720267-23224
    source_channel: str        # e.g. noaa_global_hourly_aws | noaa_lcd_cdo | asos_iem
    source_code: str = ""      # NOAA ISD SOURCE code (e.g. 4, 7)
    report_type: str = ""      # e.g. FM-15
    source_file_id: int | None = None
    filled: bool = False       # True if contributed by a fallback (fill) station


def build_composite(primary, fills):
    """Merge a primary station's hours with prioritized fallback hours.

    Rule (EOP-012 secondary-fill / segmentation, methodology + ADR-0002): the
    primary station's valid hours are never overwritten; a fallback contributes
    only hours that the primary (and higher-priority fallbacks) lack. Each output
    hour retains its own provenance and a ``filled`` flag.

    ``primary`` is an iterable of HourObs; ``fills`` is an ordered iterable of
    iterables of HourObs, highest priority first. Returns a list of HourObs
    sorted by ``hour_ending_utc``.
    """
    by_hour: dict[str, HourObs] = {}
    for o in primary:
        by_hour.setdefault(o.hour_ending_utc, _as_obs(o, filled=False))
    for tier_list in fills:
        for o in tier_list:
            if o.hour_ending_utc not in by_hour:
                by_hour[o.hour_ending_utc] = _as_obs(o, filled=True)
    return [by_hour[h] for h in sorted(by_hour)]


def _as_obs(o: HourObs, *, filled: bool) -> HourObs:
    return HourObs(o.hour_ending_utc, o.dry_bulb_f, o.station_id, o.source_channel,
                   o.source_code, o.report_type, o.source_file_id, filled)


def provenance_summary(composite, ecwt_f: float | None = None) -> dict:
    """Summarize the audit trail for a composite series.

    Reports contributing towers and source channels (with hour counts), the
    number of filled hours, and -- when ``ecwt_f`` is supplied -- the provenance
    of the cold-tail hours (<= ECWT) that actually determine the value. The
    cold-tail provenance is the key audit artifact.
    """
    towers: dict[str, int] = {}
    sources: dict[str, int] = {}
    filled = 0
    tail: dict[tuple, int] = {}
    for o in composite:
        towers[o.station_id] = towers.get(o.station_id, 0) + 1
        sources[o.source_channel] = sources.get(o.source_channel, 0) + 1
        if o.filled:
            filled += 1
        if ecwt_f is not None and o.dry_bulb_f <= ecwt_f:
            key = (o.station_id, o.source_channel)
            tail[key] = tail.get(key, 0) + 1
    return {
        "n_hours": len(composite),
        "towers": towers,
        "sources": sources,
        "filled_hours": filled,
        "cold_tail_provenance": {f"{s}|{c}": v for (s, c), v in sorted(tail.items())},
    }
