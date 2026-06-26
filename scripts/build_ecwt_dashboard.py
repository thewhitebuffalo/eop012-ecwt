#!/usr/bin/env python3
"""Build a self-contained interactive ECWT dashboard from a scoped release CSV.

This is a *visualization* step, not a data step. It reads a published scoped
plant ECWT release CSV (the wide variant that carries plant latitude/longitude,
ECWT, plant state, and primary-station distance) and renders a single
self-contained HTML file: an interactive U.S. map, an ECWT distribution
histogram, a sortable state ranking, and a station-distance data-quality panel.

Design intent (consistent with docs/publication_plan.md):

- The repository tracks the *builder* (this script + viz/dashboard_template.html),
  never the generated HTML, which embeds ~1 MB of derived data. Publish the
  rendered dashboard as a GitHub Pages page or a release asset with a checksum.
- The output is fully offline: no CDN, no external fonts, no network calls. All
  charts are hand-rendered with inline SVG/canvas.

Usage:
    python scripts/build_ecwt_dashboard.py \
        --release-csv /path/to/scoped_plant_ecwt_release_<ts>.csv \
        --output build/EOP012_ECWT_dashboard.html

The release CSV must contain these columns:
    plant_latitude, plant_longitude, ecwt_f, plant_state, plant_name
and optionally:
    primary_station_distance_km
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TEMPLATE = REPO_ROOT / "viz" / "dashboard_template.html"
DEFAULT_OUTPUT = REPO_ROOT / "build" / "EOP012_ECWT_dashboard.html"
PLACEHOLDER = "__ECWT_DATA__"


def _f(value):
    if value is None:
        return None
    value = value.strip()
    if value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def build_payload(release_csv: Path) -> dict:
    points = []
    vals = []
    by_state = {}
    dist = {"a": 0, "b": 0, "c": 0, "d": 0, "e": 0, "u": 0}  # <25,25-50,50-100,100-200,>200,unknown
    statuses = {}
    reason_codes = {}

    with release_csv.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            la = _f(row.get("plant_latitude"))
            lo = _f(row.get("plant_longitude"))
            e = _f(row.get("ecwt_f"))
            if la is None or lo is None or e is None:
                continue
            state = (row.get("plant_state") or "").strip()
            d = _f(row.get("primary_station_distance_km"))
            if d is None:
                dist["u"] += 1
                d_out = None
            else:
                d_out = round(d)
                if d < 25:
                    dist["a"] += 1
                elif d < 50:
                    dist["b"] += 1
                elif d < 100:
                    dist["c"] += 1
                elif d < 200:
                    dist["d"] += 1
                else:
                    dist["e"] += 1
            status = (row.get("readiness_status") or "").strip()
            reason_code = (row.get("reason_code") or "").strip()
            if status:
                statuses[status] = statuses.get(status, 0) + 1
            if reason_code:
                reason_codes[reason_code] = reason_codes.get(reason_code, 0) + 1
            points.append({
                "la": round(la, 3),
                "lo": round(lo, 3),
                "e": round(e, 1),
                "s": state,
                "d": d_out,
                "n": (row.get("plant_name") or "").strip(),
            })
            vals.append(e)
            by_state.setdefault(state, []).append(e)

    if not vals:
        raise SystemExit(f"No usable rows (need plant_latitude/longitude/ecwt_f) in {release_csv}")

    svals = sorted(vals)
    n = len(svals)
    median = svals[n // 2] if n % 2 else (svals[n // 2 - 1] + svals[n // 2]) / 2
    below32 = sum(1 for v in vals if v < 32)
    kpis = {
        "plants": n,
        "states": len(by_state),
        "minF": round(min(vals), 1),
        "maxF": round(max(vals), 1),
        "meanF": round(sum(vals) / n, 1),
        "medianF": round(median, 1),
        "distinct": len(set(round(v, 1) for v in vals)),
        "below32": below32,
        "below32pct": round(100 * below32 / n, 1),
    }

    release_id = release_csv.stem
    far100 = dist["d"] + dist["e"]
    known_distance = sum(dist[key] for key in ("a", "b", "c", "d", "e"))
    quality = {
        "releaseId": release_id,
        "knownDistance": known_distance,
        "far100": far100,
        "far100pct": round(100 * far100 / known_distance, 1) if known_distance else None,
        "within100": dist["a"] + dist["b"] + dist["c"],
        "within25pct": round(100 * dist["a"] / known_distance, 1) if known_distance else None,
        "statuses": statuses,
        "reasonCodes": reason_codes,
    }

    state_rows = []
    for s, g in by_state.items():
        b = sum(1 for v in g if v < 32)
        state_rows.append({
            "s": s,
            "n": len(g),
            "mean": round(sum(g) / len(g), 1),
            "min": round(min(g), 1),
            "below32pct": round(100 * b / len(g), 1),
        })

    hist = []
    x = -42
    while x < 42:
        c = sum(1 for v in vals if x <= v < x + 3)
        hist.append({"x0": x, "x1": x + 3, "c": c})
        x += 3

    return {"kpis": kpis, "quality": quality, "byState": state_rows, "hist": hist, "dist": dist, "points": points}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--release-csv", type=Path, required=True,
                    help="Wide scoped_plant_ecwt_release_*.csv (with lat/lon/distance).")
    ap.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    ap.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = ap.parse_args()

    if not args.release_csv.exists():
        raise SystemExit(f"release CSV not found: {args.release_csv}")
    if not args.template.exists():
        raise SystemExit(f"template not found: {args.template}")

    payload = build_payload(args.release_csv)
    template = args.template.read_text(encoding="utf-8")
    if PLACEHOLDER not in template:
        raise SystemExit(f"template missing {PLACEHOLDER} placeholder")
    data_js = "window.ECWT = " + json.dumps(payload, separators=(",", ":")) + ";"
    html = template.replace(PLACEHOLDER, data_js)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(html, encoding="utf-8")

    k = payload["kpis"]
    print(json.dumps({
        "output": str(args.output),
        "size_kb": round(args.output.stat().st_size / 1024),
        "plants": k["plants"],
        "states": k["states"],
        "below32pct": k["below32pct"],
        "min_max_f": [k["minF"], k["maxF"]],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
