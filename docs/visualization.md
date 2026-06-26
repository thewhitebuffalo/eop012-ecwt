# ECWT Visualization

This repository tracks a reproducible **dashboard builder**, not the rendered
dashboard. The builder turns a published scoped plant ECWT release CSV into a
single, self-contained, offline HTML dashboard.

## What it produces

One HTML file with four linked views:

- **U.S. map** — every plant plotted at its coordinates, colored by ECWT, with
  three modes (ECWT temperature, highlight `ECWT < 32 F`, station distance) and
  hover tooltips (plant, state, ECWT, primary-station distance).
- **Distribution histogram** — 3 F bins with the 32 F EOP-012 applicability line.
- **State ranking** — sortable by mean ECWT, coldest plant, `% < 32 F`, or count.
- **Data-quality panel** — the primary-station distance breakdown, to keep the
  representativeness caveat attached to the picture.

The output is fully offline: no CDN, no external fonts, no network calls. Charts
are rendered with inline SVG and `<canvas>`.

## Inputs

A wide scoped release CSV (`data/processed/scoped_plant_ecwt_release_<ts>.csv`)
containing at least:

- `plant_latitude`, `plant_longitude`, `ecwt_f`, `plant_state`, `plant_name`
- optional: `primary_station_distance_km` (drives the data-quality panel)

## Build

```bash
python scripts/build_ecwt_dashboard.py \
  --release-csv data/processed/scoped_plant_ecwt_release_<ts>.csv \
  --output build/EOP012_ECWT_dashboard.html
```

Standard library only — no third-party dependencies. Open the resulting file in
any browser, or double-click it.

## Files

- `scripts/build_ecwt_dashboard.py` — reads the release CSV, computes aggregates,
  embeds the data, and writes the standalone HTML.
- `viz/dashboard_template.html` — the markup/CSS/JS template with a single
  `__ECWT_DATA__` placeholder where the embedded dataset is injected.

## Publication policy

The generated HTML embeds roughly 1 MB of derived plant data, so per
`docs/publication_plan.md` and the repository hygiene rules it is **not committed**
(`build/` is git-ignored). Publish the rendered dashboard as:

- a **GitHub Pages** page (e.g. a `gh-pages` branch or `/docs` site), or
- a **release asset** alongside the release bundle, with a SHA-256 checksum.

## Caveat

The dashboard reflects whatever release CSV it is given. The generated page
surfaces source release, readiness reason codes, and station-distance buckets so
older diagnostic releases and stricter fixed-period publication-candidate
releases do not get visually conflated. Regenerate it after any release that
changes the readiness or representativeness gates (see `docs/adr/`).
