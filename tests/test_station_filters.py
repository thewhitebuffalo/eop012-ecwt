#!/usr/bin/env python3
"""Unit tests for ADR-0006 station eligibility helpers."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import station_filters as f  # noqa: E402

_passed = 0


def check(name, cond):
    global _passed
    if not cond:
        raise AssertionError("FAILED: " + name)
    _passed += 1


def main():
    check("997 marine", f.is_marine_platform_station_id("997994-99999"))
    check("998 marine", f.is_marine_platform_station_id("998203-99999"))
    check("999 placeholder marine", f.is_marine_platform_station_id("999123-99999"))
    check("999 real wban stays eligible", not f.is_marine_platform_station_id("999123-13743"))
    check("ordinary land station", f.is_land_plant_station_eligible("724050-13743"))
    check("fm13 marine report type", f.is_marine_platform_report_type("FM-13"))
    check("fm15 not marine report type", not f.is_marine_platform_report_type("FM-15"))
    check("land obs eligible", f.is_land_plant_observation_eligible("724050-13743", "FM-15"))
    check("fm13 obs ineligible", not f.is_land_plant_observation_eligible("724050-13743", "FM-13"))
    check("marine station obs ineligible", not f.is_land_plant_observation_eligible("997994-99999", "FM-15"))
    print(f"OK - {_passed} checks passed")


if __name__ == "__main__":
    main()
