"""Golden-output test for the dashboard builder.

Builds the dashboard from a small fixture cut of the published
20260626T235840Z scoped release and asserts:

- the build succeeds and both placeholders are injected
  (__ECWT_DATA__ payload, __SUPPORT_QR_DATA_URI__ QR image),
- the embedded ``window.ECWT`` payload parses as JSON and carries the
  expected shape (kpis / quality / points with the detail-drawer keys),
- published vs held row handling matches the fixture,
- the interactive features' markers are present (search, detail drawer,
  RSAW docx generator, support modal).

Stdlib only. Run directly:  python tests/test_dashboard_build.py
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE = REPO_ROOT / "tests" / "fixtures" / "scoped_release_fixture.csv"
BUILDER = REPO_ROOT / "scripts" / "build_ecwt_dashboard.py"

CHECKS = 0


def check(name: str, cond: bool) -> None:
    global CHECKS
    if not cond:
        raise SystemExit(f"FAIL: {name}")
    CHECKS += 1


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "dash.html"
        proc = subprocess.run(
            [sys.executable, str(BUILDER), "--release-csv", str(FIXTURE), "--output", str(out)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        )
        check("builder exits 0", proc.returncode == 0)
        html = out.read_text(encoding="utf-8")

    check("ECWT placeholder replaced", "__ECWT_DATA__" not in html)
    check("QR placeholder replaced", "__SUPPORT_QR_DATA_URI__" not in html)
    check("QR data URI embedded", "data:image/png;base64," in html)
    check("US outline placeholder replaced", "__US_OUTLINE_DATA__" not in html)
    m_out = re.search(r"var OUTLINE=(\[\[.*?\]\]);", html)
    check("US outline rings embedded", m_out is not None and len(json.loads(m_out.group(1))) > 40)

    m = re.search(r"window\.ECWT = (\{.*?\});</script>", html, re.DOTALL)
    check("embedded payload found", m is not None)
    payload = json.loads(m.group(1))

    for key in ("kpis", "quality", "byState", "hist", "dist", "tiers", "sources", "points"):
        check(f"payload has {key}", key in payload)

    # Fixture: 8 rows -- 4 published (complete tier), 4 blocked_no_data with
    # null public ecwt_f and no coordinates -> 4 plotted points, 4 held rows.
    pts = payload["points"]
    check("held rows excluded from points", len(pts) == 4)
    check("kpis plants counts all policy rows", payload["kpis"]["plants"] == 8)
    check("kpis plotted counts map points", payload["kpis"]["plotted"] == 4)
    check("held rows tracked", payload["kpis"]["heldRows"] == 4)

    detail_keys = {"la", "lo", "e", "s", "n", "d", "sid", "t",
                   "cov", "vh", "eh", "cty", "eia", "ctw", "ctwN", "ctp"}
    check("points carry detail-drawer keys", detail_keys.issubset(set(pts[0].keys())))
    rich = [p for p in pts if p.get("ctw")]
    check("contributing towers embedded", len(rich) >= 4)
    check("ctw pairs are [station, hours]",
          all(isinstance(t, list) and len(t) == 2 and isinstance(t[1], int)
              for p in rich for t in p["ctw"]))

    for marker in ("plantSearch", "searchResults", 'id="detail"', "supportModal",
                   "buildRSAWDocx", "downloadRSAW", "openDetail", "zipStore"):
        check(f"feature marker {marker}", marker in html)

    check("quality carries releaseId", bool(payload["quality"].get("releaseId")))
    check("quality carries coverageBasis", bool(payload["quality"].get("coverageBasis")))

    print(f"OK - {CHECKS} checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
