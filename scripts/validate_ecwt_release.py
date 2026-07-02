#!/usr/bin/env python3
"""Validate a regenerated ECWT release CSV against the ADR-0006 acceptance rules.

Run this against the committed results CSV after a rebuild to get a one-pass
PASS / WARN / FAIL / INFO readout. Standard library only; no DB or network.

Usage:
    python scripts/validate_ecwt_release.py --results-csv data/processed/<results>.csv
    python scripts/validate_ecwt_release.py --results-csv <results>.csv \
        --cold-tail-csv data/processed/<cold_tail>.csv
    python scripts/validate_ecwt_release.py --results-csv <results>.csv \
        --cold-tail-csv data/processed/<cold_tail_part*.csv>

Exit code is non-zero if any hard check FAILs. See
docs/validating_ecwt_release.md for the full write-up.

Checks:
  1. coverage_floor    FAIL if any PUBLISHED row has coverage < --min-coverage (0.95)
  2. held_rows_null    FAIL if any HELD row carries a public ecwt_f
  3. plausible_ecwt    FAIL if any published ecwt_f > --fail-ecwt (70 F);
                       WARN above --warn-ecwt (60 F)
  4. publishable_count WARN if publishable rows <= --prior-publishable (123)
  5. state_range       INFO: widest / narrowest states (expect CA/AZ widest)
  6. provenance        FAIL if a cold-tail CSV is given and a published plant
                       has no provenance row (best-effort plant-id match)
  7. marine_low_outlier FAIL if release-row cold-tail provenance shows marine
                       dominance on a plant far below its state median
  8. tail_dominated_non_primary
                       WARN if one non-primary station sets most cold-tail hours

Column names are auto-detected from a list of candidates so the script tolerates
minor schema drift; coverage falls back to valid/expected hours if no coverage
column is present.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass
from statistics import median

from station_filters import is_marine_platform_station_id

C_STATE = ["plant_state", "state"]
C_ECWT = ["ecwt_f", "ecwt", "ecwt_fahrenheit"]
C_TIER = ["confidence_tier", "tier"]
C_PUB = ["publishable", "is_publishable"]
C_COV = ["coverage", "coverage_ratio", "fixed_period_coverage"]
C_VALID = ["valid_hour_count", "valid_djf_hours", "valid_hours"]
C_EXP = ["expected_hour_count", "expected_djf_hours", "expected_hours"]
C_PID = ["plant_id", "eia_plant_code", "plant_code", "plant_name"]
C_PRIMARY = ["primary_station_id", "selected_station_id"]
C_COLD_TAIL = ["cold_tail_provenance", "cold_tail_provenance_json"]

PUBLISHED_TIERS = {"complete", "adequate"}


@dataclass
class Cols:
    state: str | None
    ecwt: str
    tier: str | None
    pub: str | None
    cov: str | None
    valid: str | None
    exp: str | None
    pid: str | None
    primary: str | None = None
    cold_tail: str | None = None


@dataclass
class Check:
    name: str
    status: str  # PASS | WARN | FAIL | INFO
    msg: str


def find_col(fieldnames, candidates):
    fset = {f.lower(): f for f in (fieldnames or [])}
    for c in candidates:
        if c.lower() in fset:
            return fset[c.lower()]
    return None


def fnum(v):
    if v is None:
        return None
    v = str(v).strip()
    if v == "" or v.lower() in ("na", "nan", "null", "none", "\\n"):
        return None
    try:
        return float(v)
    except ValueError:
        return None


def normalize_coverage(v):
    """Return coverage as a 0..1 ratio.

    Composite fills can legitimately produce slightly more rows than the fixed
    expected-hour denominator because duplicate source observations collapse
    later in the calculation. Treat small overages as complete, while still
    accepting percent-form values like 95 or 100.
    """
    if v is None:
        return None
    if v <= 1.0:
        return v
    if v <= 1.25:
        return 1.0
    return min(v / 100.0, 1.0)


def pid(row, cols):
    return str(row.get(cols.pid, "?")).strip() if cols.pid else "?"


def coverage_of(row, cols):
    if cols.cov:
        c = fnum(row.get(cols.cov))
        if c is not None:
            return normalize_coverage(c)
    if cols.valid and cols.exp:
        v, e = fnum(row.get(cols.valid)), fnum(row.get(cols.exp))
        if v is not None and e:
            return normalize_coverage(v / e)
    return None


def _json_counts(value):
    value = (value or "").strip()
    if value in ("", r"\N"):
        return {}
    try:
        raw = json.loads(value)
    except json.JSONDecodeError:
        return {}
    out = {}
    for key, count in raw.items():
        try:
            n = int(count)
        except (TypeError, ValueError):
            continue
        if n > 0:
            out[str(key)] = n
    return out


def _station_from_tail_key(key: str) -> str:
    return str(key).split("|", 1)[0].strip()


def cold_tail_station_counts(row, cols):
    if not cols.cold_tail:
        return {}
    counts = {}
    for key, count in _json_counts(row.get(cols.cold_tail)).items():
        station_id = _station_from_tail_key(key)
        if not station_id:
            continue
        counts[station_id] = counts.get(station_id, 0) + count
    return counts


def status_of(row, cols):
    """published | held | blocked."""
    if cols.pub:
        p = str(row.get(cols.pub, "")).strip().lower()
        if p in ("true", "1", "yes", "t"):
            return "published"
        if p in ("false", "0", "no", "f"):
            if cols.tier and str(row.get(cols.tier, "")).strip().lower() == "blocked_no_data":
                return "blocked"
            return "held"
    if cols.tier:
        t = str(row.get(cols.tier, "")).strip().lower()
        if t in PUBLISHED_TIERS:
            return "published"
        if t == "blocked_no_data":
            return "blocked"
        if t:
            return "held"
    return "published" if fnum(row.get(cols.ecwt)) is not None else "held"


def run_checks(rows, cols, cfg, cold_tail_pids=None):
    cfg = {
        "min_cov": 0.95,
        "warn_ecwt": 60.0,
        "fail_ecwt": 70.0,
        "prior": 123,
        "low_side_warn": 10.0,
        "min_state_peers": 5,
        "marine_tail_fail_share": 0.50,
        "single_tail_warn_share": 0.80,
        **cfg,
    }
    out = []
    published = [r for r in rows if status_of(r, cols) == "published"]
    held = [r for r in rows if status_of(r, cols) == "held"]

    # 1. coverage floor
    if cols.cov is None and not (cols.valid and cols.exp):
        out.append(Check("coverage_floor", "WARN", "no coverage column found; check skipped"))
    else:
        below = [r for r in published
                 if (coverage_of(r, cols) is not None and coverage_of(r, cols) < cfg["min_cov"])]
        if below:
            ex = ", ".join(pid(r, cols) for r in below[:5])
            out.append(Check("coverage_floor", "FAIL",
                             f"{len(below)} published rows below {cfg['min_cov']:.0%} coverage (e.g. {ex})"))
        else:
            out.append(Check("coverage_floor", "PASS",
                             f"all {len(published)} published rows >= {cfg['min_cov']:.0%} coverage"))

    # 2. held rows must have a null public ECWT
    leaked = [r for r in held if fnum(r.get(cols.ecwt)) is not None]
    if leaked:
        ex = ", ".join(pid(r, cols) for r in leaked[:5])
        out.append(Check("held_rows_null", "FAIL",
                         f"{len(leaked)} held rows carry a public ecwt_f (e.g. {ex})"))
    else:
        out.append(Check("held_rows_null", "PASS",
                         f"all {len(held)} held rows have a null public ecwt_f"))

    # 3. plausible winter ECWT
    vals = [(r, fnum(r.get(cols.ecwt))) for r in published]
    vals = [(r, v) for r, v in vals if v is not None]
    hard = [(r, v) for r, v in vals if v > cfg["fail_ecwt"]]
    soft = [(r, v) for r, v in vals if cfg["warn_ecwt"] < v <= cfg["fail_ecwt"]]
    if hard:
        ex = ", ".join(f"{pid(r, cols)}={v:.1f}F" for r, v in hard[:5])
        out.append(Check("plausible_ecwt", "FAIL",
                         f"{len(hard)} published ECWT > {cfg['fail_ecwt']:.0f}F "
                         f"(impossible winter 0.2-pct): {ex}"))
    elif soft:
        ex = ", ".join(f"{pid(r, cols)}={v:.1f}F" for r, v in soft[:5])
        out.append(Check("plausible_ecwt", "WARN",
                         f"{len(soft)} published ECWT > {cfg['warn_ecwt']:.0f}F "
                         f"(review; HI/coastal can legitimately be high): {ex}"))
    else:
        out.append(Check("plausible_ecwt", "PASS",
                         f"all published ECWT <= {cfg['warn_ecwt']:.0f}F"))

    # 4. publishable count vs the prior run
    n = len(published)
    if n <= cfg["prior"]:
        out.append(Check("publishable_count", "WARN",
                         f"{n} publishable plants <= prior {cfg['prior']} "
                         f"(fill/selection may not be assembling composites)"))
    else:
        out.append(Check("publishable_count", "PASS", f"{n} publishable plants (prior {cfg['prior']})"))

    # 5. per-state ECWT range (informational sanity)
    state_medians = {}
    if cols.state and vals:
        bystate = {}
        for r, v in vals:
            s = str(r.get(cols.state, "")).strip()
            if s:
                bystate.setdefault(s, []).append(v)
        state_medians = {
            state: median(state_vals)
            for state, state_vals in bystate.items()
            if len(state_vals) >= cfg["min_state_peers"]
        }
        ranges = sorted(((s, max(vs) - min(vs), len(vs)) for s, vs in bystate.items() if len(vs) >= 2),
                        key=lambda x: x[1], reverse=True)
        if ranges:
            top = "; ".join(f"{s} {r:.0f}F(n={k})" for s, r, k in ranges[:5])
            bot = "; ".join(f"{s} {r:.0f}F" for s, r, k in ranges[-5:])
            out.append(Check("state_range", "INFO",
                             f"widest: {top} | narrowest: {bot} | "
                             f"expect CA/AZ widest, ND/MT/MN/FL/HI narrow"))

    # 6. low-side state median and marine-platform tail dominance
    if cols.state and cols.cold_tail and state_medians:
        low_rows = []
        marine_fail = []
        for r, v in vals:
            state = str(r.get(cols.state, "")).strip()
            med = state_medians.get(state)
            if med is None:
                continue
            delta = med - v
            if delta < cfg["low_side_warn"]:
                continue
            counts = cold_tail_station_counts(r, cols)
            total = sum(counts.values())
            marine = sum(
                count for station_id, count in counts.items()
                if is_marine_platform_station_id(station_id)
            )
            marine_share = marine / total if total else 0.0
            low_rows.append((r, v, state, med, delta, marine_share))
            if marine_share > cfg["marine_tail_fail_share"]:
                marine_fail.append((r, v, state, med, delta, marine_share))
        if marine_fail:
            ex = ", ".join(
                f"{pid(r, cols)} {state} {v:.1f}F vs median {med:.1f}F, "
                f"marine tail {share:.0%}"
                for r, v, state, med, delta, share in marine_fail[:5]
            )
            out.append(Check("marine_low_outlier", "FAIL",
                             f"{len(marine_fail)} published plants are >="
                             f"{cfg['low_side_warn']:.0f}F below state median with >"
                             f"{cfg['marine_tail_fail_share']:.0%} marine-platform cold-tail hours: {ex}"))
        else:
            out.append(Check("marine_low_outlier", "PASS",
                             "no low-side state-median outlier is dominated by marine-platform cold-tail hours"))
        if low_rows:
            ex = ", ".join(
                f"{pid(r, cols)} {state} {v:.1f}F vs median {med:.1f}F"
                for r, v, state, med, delta, share in low_rows[:5]
            )
            out.append(Check("state_low_outlier", "WARN",
                             f"{len(low_rows)} published plants are >="
                             f"{cfg['low_side_warn']:.0f}F below state median; review representativeness: {ex}"))
        else:
            out.append(Check("state_low_outlier", "PASS",
                             f"no published plant is >= {cfg['low_side_warn']:.0f}F below its state median"))

    # 7. single non-primary station dominance in the cold tail
    if cols.cold_tail and cols.primary:
        dominated = []
        for r in published:
            counts = cold_tail_station_counts(r, cols)
            total = sum(counts.values())
            if not total:
                continue
            station_id, count = max(counts.items(), key=lambda kv: kv[1])
            share = count / total
            primary = str(r.get(cols.primary, "")).strip()
            if station_id != primary and share > cfg["single_tail_warn_share"]:
                dominated.append((r, station_id, share, count, total))
        if dominated:
            ex = ", ".join(
                f"{pid(r, cols)} {station_id} {share:.0%} ({count}/{total})"
                for r, station_id, share, count, total in dominated[:5]
            )
            out.append(Check("tail_dominated_non_primary", "WARN",
                             f"{len(dominated)} published plants have >"
                             f"{cfg['single_tail_warn_share']:.0%} of cold-tail hours from one non-primary station: {ex}"))
        else:
            out.append(Check("tail_dominated_non_primary", "PASS",
                             "no published plant cold tail is dominated by one non-primary station"))

    # 8. provenance (optional)
    if cold_tail_pids is not None:
        missing = [r for r in published if pid(r, cols) not in cold_tail_pids]
        if missing:
            ex = ", ".join(pid(r, cols) for r in missing[:5])
            out.append(Check("provenance", "FAIL",
                             f"{len(missing)} published plants have no cold-tail provenance (e.g. {ex})"))
        else:
            out.append(Check("provenance", "PASS",
                             f"all {len(published)} published plants have cold-tail provenance"))

    return out


def _resolve_cols(fieldnames):
    ecwt = find_col(fieldnames, C_ECWT)
    if not ecwt:
        sys.exit(f"ERROR: no ECWT column found in results CSV (looked for {C_ECWT}).")
    return Cols(state=find_col(fieldnames, C_STATE), ecwt=ecwt,
                tier=find_col(fieldnames, C_TIER), pub=find_col(fieldnames, C_PUB),
                cov=find_col(fieldnames, C_COV), valid=find_col(fieldnames, C_VALID),
                exp=find_col(fieldnames, C_EXP), pid=find_col(fieldnames, C_PID),
                primary=find_col(fieldnames, C_PRIMARY),
                cold_tail=find_col(fieldnames, C_COLD_TAIL))


def _load_pids(paths):
    out = set()
    for path in paths:
        with open(path, newline="", encoding="utf-8-sig") as f:
            r = csv.DictReader(f)
            c = find_col(r.fieldnames, C_PID)
            if not c:
                sys.exit(f"ERROR: cold-tail CSV has no plant-id column ({C_PID}).")
            out.update(str(row[c]).strip() for row in r)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--results-csv", required=True)
    ap.add_argument("--cold-tail-csv", action="append", nargs="+",
                    help="optional; enables the provenance check; accepts split files")
    ap.add_argument("--min-coverage", type=float, default=0.95)
    ap.add_argument("--warn-ecwt", type=float, default=60.0)
    ap.add_argument("--fail-ecwt", type=float, default=70.0)
    ap.add_argument("--prior-publishable", type=int, default=123)
    ap.add_argument("--low-side-warn", type=float, default=10.0,
                    help="WARN when a plant ECWT is this many F below its state median")
    ap.add_argument("--min-state-peers", type=int, default=5,
                    help="minimum published rows needed before using a state's median")
    ap.add_argument("--marine-tail-fail-share", type=float, default=0.50,
                    help="FAIL low-side outliers when marine-platform stations exceed this cold-tail share")
    ap.add_argument("--single-station-tail-warn-share", type=float, default=0.80,
                    help="WARN when one non-primary station exceeds this cold-tail share")
    a = ap.parse_args()

    with open(a.results_csv, newline="", encoding="utf-8-sig") as f:
        rd = csv.DictReader(f)
        rows = list(rd)
        cols = _resolve_cols(rd.fieldnames)
    cold_paths = [p for group in (a.cold_tail_csv or []) for p in group]
    cold = _load_pids(cold_paths) if cold_paths else None
    cfg = {"min_cov": a.min_coverage, "warn_ecwt": a.warn_ecwt,
           "fail_ecwt": a.fail_ecwt, "prior": a.prior_publishable,
           "low_side_warn": a.low_side_warn,
           "min_state_peers": a.min_state_peers,
           "marine_tail_fail_share": a.marine_tail_fail_share,
           "single_tail_warn_share": a.single_station_tail_warn_share}

    checks = run_checks(rows, cols, cfg, cold)
    print(f"ECWT release validation: {a.results_csv}  ({len(rows)} rows)")
    rank = {"PASS": 0, "INFO": 0, "WARN": 1, "FAIL": 2}
    worst = "PASS"
    for c in checks:
        print(f"  [{c.status:4}] {c.name}: {c.msg}")
        if rank[c.status] > rank[worst]:
            worst = c.status
    print(f"RESULT: {worst}")
    sys.exit(1 if worst == "FAIL" else 0)


if __name__ == "__main__":
    main()
