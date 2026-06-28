#!/usr/bin/env python3
"""Build a self-contained interactive ECWT dashboard from a scoped release CSV.

This is a *visualization* step, not a data step. It reads a published scoped
plant ECWT release CSV (the wide variant that carries plant latitude/longitude,
public ECWT, plant state, and primary-station distance) and renders a single
self-contained HTML file: an interactive U.S. map, an ECWT distribution
histogram, a sortable state ranking, and a station-distance data-quality panel.

Design intent (consistent with docs/publication_plan.md):

- The repository tracks the *builder* (this script + viz/dashboard_template.html),
  never the generated HTML, which embeds ~1 MB of derived data. Publish the
- Rendered dashboards are committed when they are part of a promoted ECWT release.
- The output is fully offline: no CDN, no external fonts, no network calls. All
  charts are hand-rendered with inline SVG/canvas.

Usage:
    python scripts/build_ecwt_dashboard.py \
        --release-csv /path/to/scoped_plant_ecwt_release_<ts>.csv \
        --output build/EOP012_ECWT_dashboard.html

The release CSV must contain these columns:
    plant_latitude, plant_longitude, ecwt_f, plant_state, plant_name
and optionally:
    primary_station_distance_km, confidence_tier, source_channels,
    diagnostic_ecwt_f, publishable
"""

from __future__ import annotations

import argparse
import base64
import csv
import json
import math
import mimetypes
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TEMPLATE = REPO_ROOT / "viz" / "dashboard_template.html"
DEFAULT_OUTPUT = REPO_ROOT / "build" / "EOP012_ECWT_dashboard.html"
DEFAULT_SUPPORT_QR = REPO_ROOT / "viz" / "assets" / "buymeacoffee_qr.png"
PLACEHOLDER = "__ECWT_DATA__"
SUPPORT_QR_PLACEHOLDER = "__SUPPORT_QR_DATA_URI__"

LOWER_48_STATES = {
    "AL", "AR", "AZ", "CA", "CO", "CT", "DE", "FL", "GA", "IA", "ID", "IL",
    "IN", "KS", "KY", "LA", "MA", "MD", "ME", "MI", "MN", "MO", "MS", "MT",
    "NC", "ND", "NE", "NH", "NJ", "NM", "NV", "NY", "OH", "OK", "OR", "PA",
    "RI", "SC", "SD", "TN", "TX", "UT", "VA", "VT", "WA", "WI", "WV", "WY",
}

# Public project names do not always match EIA plant names. Keep this list small
# and explicit so dashboard search can bridge known umbrella/project aliases.
PLANT_ALIASES = {
    "63981": ["Western Spirit Wind", "Western Spirit"],
    "64054": ["Western Spirit Wind", "Western Spirit"],
    "64065": ["Western Spirit Wind", "Western Spirit"],
    "64066": ["Western Spirit Wind", "Western Spirit"],
    "66923": ["Sun Zia"],
    "66924": ["Sun Zia"],
}


def _f(value):
    if value is None:
        return None
    value = value.strip()
    if value in ("", "\\N", "NULL", "None", "none"):
        return None
    try:
        return float(value)
    except ValueError:
        return None


def _int(value):
    f = _f(value)
    return int(round(f)) if f is not None else None


def _top_pairs(value, limit):
    """Parse a {key: count} JSON column into a descending [[key, count], ...]
    list capped at ``limit``; returns (pairs, total_keys)."""
    counts = _json_counts(value)
    pairs = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)
    return [[k, v] for k, v in pairs[:limit]], len(counts)


def _truthy(value) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "t", "yes", "y"}


def _json_counts(value) -> dict[str, int]:
    value = (value or "").strip()
    if value in ("", "\\N"):
        return {}
    try:
        raw = json.loads(value)
    except json.JSONDecodeError:
        return {}
    out: dict[str, int] = {}
    for key, count in raw.items():
        try:
            out[str(key)] = int(count)
        except (TypeError, ValueError):
            continue
    return out


def _add_counts(target: dict[str, int], counts: dict[str, int]) -> None:
    for key, count in counts.items():
        target[key] = target.get(key, 0) + count


def _nice_ticks(lo: float, hi: float) -> list[int]:
    span = max(1.0, hi - lo)
    step = 10 if span <= 90 else 20
    start = int(math.floor(lo / step) * step)
    end = int(math.ceil(hi / step) * step)
    return list(range(start, end + step, step))


def build_payload(release_csv: Path) -> dict:
    points = []
    vals = []
    by_state = {}
    dist = {"a": 0, "b": 0, "c": 0, "d": 0, "e": 0, "u": 0}  # <25,25-50,50-100,100-200,>200,unknown
    statuses = {}
    confidence_tiers = {}
    source_channels = {}
    reason_codes = {}
    reasons = {}
    total_rows = 0
    rows_with_coords = 0
    rows_with_ecwt = 0
    rows_with_diagnostic_ecwt = 0
    held_rows = 0
    plotted_rows = 0
    needs_review_rows = 0
    first_release_id = None
    first_run_id = None
    coverage_basis = None
    publication_caveat = None

    with release_csv.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_rows += 1
            if not first_release_id and row.get("release_id"):
                first_release_id = row["release_id"].strip()
            if not first_run_id and row.get("adr0004_run_id"):
                first_run_id = row["adr0004_run_id"].strip()
            if not coverage_basis and row.get("coverage_basis"):
                coverage_basis = row["coverage_basis"].strip()
            if not publication_caveat and row.get("publication_caveat"):
                publication_caveat = row["publication_caveat"].strip()
            la = _f(row.get("plant_latitude"))
            lo = _f(row.get("plant_longitude"))
            e = _f(row.get("ecwt_f"))
            diagnostic_e = _f(row.get("diagnostic_ecwt_f"))
            state = (row.get("plant_state") or "").strip()
            d = _f(row.get("primary_station_distance_km"))
            if d is None:
                d = _f(row.get("selected_station_distance_km"))
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
            tier = (row.get("confidence_tier") or "").strip()
            status = tier or (row.get("readiness_status") or "").strip()
            reason_code = (row.get("reason_code") or "").strip()
            reason = (row.get("reason") or "").strip()
            if _truthy(row.get("needs_review")):
                needs_review_rows += 1
            if diagnostic_e is not None:
                rows_with_diagnostic_ecwt += 1
            if tier in {"provisional_review", "blocked_no_data"} and e is None:
                held_rows += 1
            if status:
                statuses[status] = statuses.get(status, 0) + 1
            if tier:
                confidence_tiers[tier] = confidence_tiers.get(tier, 0) + 1
            if reason_code:
                reason_codes[reason_code] = reason_codes.get(reason_code, 0) + 1
            if reason:
                reasons[reason] = reasons.get(reason, 0) + 1
            _add_counts(source_channels, _json_counts(row.get("source_channels")))
            if la is not None and lo is not None:
                rows_with_coords += 1
            if e is not None:
                rows_with_ecwt += 1
                vals.append(e)
            if la is not None and lo is not None and e is not None:
                plotted_rows += 1
                cov = _f(row.get("coverage_ratio"))
                dr = _f(row.get("ecwt_discrete_f"))
                ctw_top, ctw_n = _top_pairs(row.get("contributing_towers"), 6)
                ctp_top, _ = _top_pairs(row.get("cold_tail_provenance"), 8)
                eia_code = (row.get("eia_plant_code") or "").strip()
                points.append({
                    "la": round(la, 3),
                    "lo": round(lo, 3),
                    "e": round(e, 1),
                    "s": state,
                    "d": d_out,
                    "n": (row.get("plant_name") or "").strip(),
                    "r": reason_code,
                    "rs": reason,
                    "st": status,
                    "t": tier,
                    "nr": _truthy(row.get("needs_review")),
                    "sid": (row.get("primary_station_id") or "").strip(),
                    # per-plant detail (click-to-open panel)
                    "dr": round(dr, 1) if dr is not None else None,
                    "cov": round(cov * 100, 1) if cov is not None else None,
                    "vh": _int(row.get("valid_hour_count")),
                    "eh": _int(row.get("expected_hour_count")),
                    "fh": _int(row.get("filled_hour_count")),
                    "cty": (row.get("plant_county") or "").strip(),
                    "eia": eia_code,
                    "a": PLANT_ALIASES.get(eia_code, []),
                    "ttc": _int(row.get("towers_tried_count")),
                    "ctw": ctw_top,    # [[station_id, hours], ...] top 6 by hours
                    "ctwN": ctw_n,     # total contributing towers
                    "ctp": ctp_top,    # [["station|source", hours], ...] cold-tail
                })
                by_state.setdefault(state, []).append(e)

    if not vals:
        raise SystemExit(f"No usable rows (need plant_latitude/longitude/ecwt_f) in {release_csv}")

    svals = sorted(vals)
    n = len(svals)
    median = svals[n // 2] if n % 2 else (svals[n // 2 - 1] + svals[n // 2]) / 2
    below32 = sum(1 for v in vals if v < 32)
    kpis = {
        "plants": total_rows,
        "plotted": plotted_rows,
        "rowsWithCoords": rows_with_coords,
        "rowsWithEcwt": rows_with_ecwt,
        "rowsWithDiagnosticEcwt": rows_with_diagnostic_ecwt,
        "rowsMissingEcwt": total_rows - rows_with_ecwt,
        "heldRows": held_rows,
        "states": len(LOWER_48_STATES.intersection(by_state)),
        "minF": round(min(vals), 1),
        "maxF": round(max(vals), 1),
        "meanF": round(sum(vals) / n, 1),
        "medianF": round(median, 1),
        "distinct": len(set(round(v, 1) for v in vals)),
        "below32": below32,
        "below32pct": round(100 * below32 / n, 1),
    }

    release_id = first_release_id or release_csv.stem
    far100 = dist["d"] + dist["e"]
    known_distance = sum(dist[key] for key in ("a", "b", "c", "d", "e"))
    quality = {
        "releaseId": release_id,
        "adrRunId": first_run_id,
        "coverageBasis": coverage_basis,
        "publicationCaveat": publication_caveat,
        "knownDistance": known_distance,
        "far100": far100,
        "far100pct": round(100 * far100 / known_distance, 1) if known_distance else None,
        "within100": dist["a"] + dist["b"] + dist["c"],
        "within25pct": round(100 * dist["a"] / known_distance, 1) if known_distance else None,
        "plottedRows": plotted_rows,
        "rowsWithEcwt": rows_with_ecwt,
        "rowsWithDiagnosticEcwt": rows_with_diagnostic_ecwt,
        "rowsMissingEcwt": total_rows - rows_with_ecwt,
        "heldRows": held_rows,
        "rowsMissingCoords": total_rows - rows_with_coords,
        "needsReviewRows": needs_review_rows,
        "confidenceTiers": confidence_tiers,
        "statuses": statuses,
        "reasonCodes": reason_codes,
        "reasons": reasons,
        "sourceChannels": source_channels,
    }

    state_rows = []
    for s, g in by_state.items():
        if s not in LOWER_48_STATES:
            continue
        b = sum(1 for v in g if v < 32)
        state_rows.append({
            "s": s,
            "n": len(g),
            "mean": round(sum(g) / len(g), 1),
            "min": round(min(g), 1),
            "below32pct": round(100 * b / len(g), 1),
        })

    bin_width = 3
    start = int(math.floor(min(vals) / bin_width) * bin_width)
    end = int(math.ceil(max(vals) / bin_width) * bin_width + bin_width)
    hist = []
    x = start
    while x < end:
        c = sum(1 for v in vals if x <= v < x + 3)
        hist.append({"x0": x, "x1": x + 3, "c": c})
        x += 3

    tier_order = ["complete", "adequate", "provisional_review", "blocked_no_data"]
    tier_rows = [
        {"key": key, "label": key.replace("_", " "), "count": confidence_tiers.get(key, 0)}
        for key in tier_order
        if confidence_tiers.get(key, 0)
    ]
    for key, count in sorted(confidence_tiers.items()):
        if key not in tier_order:
            tier_rows.append({"key": key, "label": key.replace("_", " "), "count": count})
    source_rows = [
        {"key": key, "label": key.replace("_", " "), "count": count}
        for key, count in sorted(source_channels.items(), key=lambda item: item[1], reverse=True)
    ]

    return {
        "kpis": kpis,
        "quality": quality,
        "byState": state_rows,
        "hist": hist,
        "histTicks": _nice_ticks(start, end),
        "dist": dist,
        "tiers": tier_rows,
        "sources": source_rows,
        "points": points,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--release-csv", type=Path, required=True,
                    help="Wide scoped_plant_ecwt_release_*.csv (with lat/lon/distance).")
    ap.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    ap.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    ap.add_argument("--support-qr", type=Path, default=DEFAULT_SUPPORT_QR,
                    help="QR image embedded in the dashboard support prompt.")
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
    if SUPPORT_QR_PLACEHOLDER in html:
        if not args.support_qr.exists():
            raise SystemExit(f"Support QR asset not found: {args.support_qr}")
        mime_type = mimetypes.guess_type(args.support_qr.name)[0] or "image/png"
        qr_data = base64.b64encode(args.support_qr.read_bytes()).decode("ascii")
        html = html.replace(SUPPORT_QR_PLACEHOLDER, f"data:{mime_type};base64,{qr_data}")

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
