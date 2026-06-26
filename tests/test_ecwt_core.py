#!/usr/bin/env python3
"""Unit tests for scripts/ecwt_core.py (standard library only; run directly).

    python tests/test_ecwt_core.py

Exits non-zero on any failure.
"""

import os
import sys
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import ecwt_core as core  # noqa: E402

_passed = 0


def check(name, cond):
    global _passed
    if not cond:
        raise AssertionError("FAILED: " + name)
    _passed += 1


def approx(a, b, tol=1e-9):
    return abs(a - b) <= tol


def test_ecwt_percentile():
    # PERCENTILE.INC([1..1000], 0.002): rank = 0.002*999 = 1.998 ->
    # interpolate between xs[1]=2 and xs[2]=3 -> 2.998
    check("percentile 1..1000", approx(core.ecwt_percentile(range(1, 1001)), 2.998))
    # single value
    check("percentile single", approx(core.ecwt_percentile([7.0]), 7.0))
    # ignores None
    check("percentile drops None",
          approx(core.ecwt_percentile([None] + list(range(1, 1001))), 2.998))


def test_discrete_rank():
    # ceil(0.002 * 1000) = 2 -> 2nd coldest = 2
    check("discrete 1..1000", approx(core.ecwt_discrete_rank_temp(range(1, 1001)), 2.0))
    # small series: ceil(0.002*3)=1 -> coldest
    check("discrete tiny", approx(core.ecwt_discrete_rank_temp([5, 8, 10]), 5.0))


def test_expected_hours():
    # Reproduces the companion document's worked example exactly.
    check("expected hours 2024-03-01", core.expected_djf_hours(date(2024, 3, 1)) == 53424)
    # Year 2000 alone through March: Jan 31 + Feb 29 = 60 days * 24
    check("expected hours 2000-03-01", core.expected_djf_hours(date(2000, 3, 1)) == 60 * 24)


def test_adequacy_tiers():
    temps = list(range(1, 1001))
    a = core.assess_adequacy(temps, expected_hours=1000)
    check("adequacy complete tier", a.confidence_tier == "complete")
    check("adequacy complete no review", a.needs_review is False)
    check("adequacy ecwt rounded", approx(a.ecwt_f, 3.0))
    check("adequacy tail count", a.tail_hours == 2)  # temps 1 and 2 are <= 2.998

    a2 = core.assess_adequacy(temps, expected_hours=1100)  # ~9% missing
    check("adequacy adequate tier", a2.confidence_tier == "adequate")

    a3 = core.assess_adequacy(temps, expected_hours=2000)  # 50% missing
    check("adequacy provisional tier", a3.confidence_tier == "provisional_review")
    check("adequacy provisional needs review", a3.needs_review is True)

    a4 = core.assess_adequacy([], expected_hours=53424)
    check("adequacy blocked no data", a4.confidence_tier == "blocked_no_data")


def test_composite_and_provenance():
    H = core.HourObs
    primary = [
        H("2020-12-01T06:00Z", 10.0, "A", "noaa_global_hourly_aws"),
        H("2020-12-01T07:00Z", 8.0, "A", "noaa_global_hourly_aws"),
    ]
    fills = [[
        H("2020-12-01T07:00Z", 99.0, "B", "asos_iem"),  # duplicate hour: primary kept
        H("2020-12-01T08:00Z", 5.0, "B", "asos_iem"),   # new hour: filled from B
    ]]
    comp = core.build_composite(primary, fills)
    check("composite length", len(comp) == 3)
    by_hour = {o.hour_ending_utc: o for o in comp}
    check("primary not overwritten", approx(by_hour["2020-12-01T07:00Z"].dry_bulb_f, 8.0))
    check("primary not filled", by_hour["2020-12-01T07:00Z"].filled is False)
    check("fill flagged", by_hour["2020-12-01T08:00Z"].filled is True)
    check("fill tower", by_hour["2020-12-01T08:00Z"].station_id == "B")

    ecwt = core.ecwt_percentile([o.dry_bulb_f for o in comp])  # ~5.012
    summary = core.provenance_summary(comp, ecwt_f=ecwt)
    check("prov towers", summary["towers"] == {"A": 2, "B": 1})
    check("prov filled count", summary["filled_hours"] == 1)
    # the cold-tail hour came from the fill station B -> audit trail captures it
    check("cold-tail provenance", summary["cold_tail_provenance"] == {"B|asos_iem": 1})


def main():
    for fn in [test_ecwt_percentile, test_discrete_rank, test_expected_hours,
               test_adequacy_tiers, test_composite_and_provenance]:
        fn()
    print(f"OK - {_passed} checks passed")


if __name__ == "__main__":
    main()
