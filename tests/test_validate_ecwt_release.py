#!/usr/bin/env python3
"""Unit tests for scripts/validate_ecwt_release.py (stdlib only; run directly).

    python tests/test_validate_ecwt_release.py
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import validate_ecwt_release as v  # noqa: E402

_passed = 0


def check(name, cond):
    global _passed
    if not cond:
        raise AssertionError("FAILED: " + name)
    _passed += 1


COLS = v.Cols(state="plant_state", ecwt="ecwt_f", tier="confidence_tier",
              pub=None, cov="coverage", valid=None, exp=None, pid="eia_plant_code")
CFG = {"min_cov": 0.95, "warn_ecwt": 60.0, "fail_ecwt": 70.0, "prior": 2}


def row(pid, state, ecwt, tier, cov):
    return {"eia_plant_code": pid, "plant_state": state, "ecwt_f": ecwt,
            "confidence_tier": tier, "coverage": cov}


def st(checks, name):
    return next(c.status for c in checks if c.name == name)


def clean_rows():
    return [
        row("1", "CA", -20.0, "complete", 1.0),
        row("2", "CA", 38.0, "adequate", 0.97),   # wide CA range
        row("3", "ND", -30.0, "complete", 0.99),
        row("4", "ND", -28.0, "adequate", 0.96),  # narrow ND range
        row("5", "TX", 15.0, "adequate", 0.98),
        row("6", "TX", "", "provisional_review", 0.40),   # held, null ecwt
        row("7", "AK", "", "blocked_no_data", 0.0),       # blocked
    ]


def test_clean():
    c = v.run_checks(clean_rows(), COLS, CFG)
    check("clean coverage", st(c, "coverage_floor") == "PASS")
    check("clean held null", st(c, "held_rows_null") == "PASS")
    check("clean plausible", st(c, "plausible_ecwt") == "PASS")
    check("clean count", st(c, "publishable_count") == "PASS")  # 5 published > prior 2
    check("clean state info", st(c, "state_range") == "INFO")


def test_coverage_fail():
    rows = clean_rows() + [row("8", "NV", 10.0, "adequate", 0.90)]  # published but <95%
    c = v.run_checks(rows, COLS, CFG)
    check("coverage fail", st(c, "coverage_floor") == "FAIL")


def test_overcomplete_ratio_is_complete():
    cols = v.Cols(state="plant_state", ecwt="ecwt_f", tier="confidence_tier",
                  pub=None, cov="coverage_ratio", valid=None, exp=None, pid="plant_id")
    rows = [{"plant_id": "eia860:2024:plant:1", "plant_state": "TX", "ecwt_f": "9.0",
             "confidence_tier": "complete", "coverage_ratio": "1.0017"}]
    c = v.run_checks(rows, cols, CFG)
    check("overcomplete ratio pass", st(c, "coverage_floor") == "PASS")


def test_backslash_n_is_null():
    rows = clean_rows() + [row("12", "TX", "\\N", "provisional_review", 0.80)]
    c = v.run_checks(rows, COLS, CFG)
    check("backslash n null", st(c, "held_rows_null") == "PASS")


def test_held_leak_fail():
    rows = clean_rows() + [row("9", "MT", 5.0, "provisional_review", 0.30)]  # held with a value
    c = v.run_checks(rows, COLS, CFG)
    check("held leak fail", st(c, "held_rows_null") == "FAIL")


def test_warm_fail():
    rows = clean_rows() + [row("10", "TX", 88.2, "adequate", 0.99)]  # the 88F class
    c = v.run_checks(rows, COLS, CFG)
    check("warm fail", st(c, "plausible_ecwt") == "FAIL")


def test_warm_warn():
    rows = clean_rows() + [row("11", "HI", 62.0, "adequate", 0.99)]  # plausible-ish HI
    c = v.run_checks(rows, COLS, CFG)
    check("warm warn", st(c, "plausible_ecwt") == "WARN")


def test_publishable_warn():
    cfg = dict(CFG, prior=10)  # 5 published <= 10
    c = v.run_checks(clean_rows(), COLS, cfg)
    check("count warn", st(c, "publishable_count") == "WARN")


def test_provenance_fail():
    # published pids are 1,2,3,4,5; omit "5" from provenance set
    c = v.run_checks(clean_rows(), COLS, CFG, cold_tail_pids={"1", "2", "3", "4"})
    check("provenance fail", st(c, "provenance") == "FAIL")
    c2 = v.run_checks(clean_rows(), COLS, CFG, cold_tail_pids={"1", "2", "3", "4", "5"})
    check("provenance pass", st(c2, "provenance") == "PASS")


def test_resolve_prefers_stable_plant_id():
    cols = v._resolve_cols(["plant_id", "eia_plant_code", "plant_state", "ecwt_f"])
    check("plant id preferred", cols.pid == "plant_id")


def test_load_split_cold_tail_pids():
    paths = []
    try:
        for pid in ["eia860:2024:plant:1", "eia860:2024:plant:2"]:
            f = tempfile.NamedTemporaryFile("w", newline="", encoding="utf-8", delete=False)
            paths.append(f.name)
            f.write("plant_id,hour_ending_utc\n")
            f.write(f"{pid},2025-01-01T01:00:00Z\n")
            f.close()
        check("split pid load", v._load_pids(paths) == set(["eia860:2024:plant:1",
                                                           "eia860:2024:plant:2"]))
    finally:
        for path in paths:
            os.unlink(path)


def main():
    for fn in [test_clean, test_coverage_fail, test_overcomplete_ratio_is_complete,
               test_backslash_n_is_null, test_held_leak_fail, test_warm_fail,
               test_warm_warn, test_publishable_warn, test_provenance_fail,
               test_resolve_prefers_stable_plant_id, test_load_split_cold_tail_pids]:
        fn()
    print(f"OK - {_passed} checks passed")


if __name__ == "__main__":
    main()
