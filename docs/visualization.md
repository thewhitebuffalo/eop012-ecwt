# ECWT Visualization

This repository tracks a reproducible **dashboard builder**, not the rendered
dashboard. The builder turns a published scoped plant ECWT release CSV,
including the ADR-0004 release shape, into a single, self-contained, offline
HTML dashboard.

## What it produces

One HTML file with four linked views:

- **U.S. map** — every plant plotted at its coordinates, colored by ECWT, with
  three modes (ECWT temperature, highlight `ECWT < 32 F`, station distance) and
  hover tooltips (plant, state, ECWT, primary-station distance).
- **Distribution histogram** — 3 F bins with the 32 F EOP-012 applicability line.
- **State ranking** — sortable by mean ECWT, coldest plant, `% < 32 F`, or count.
- **Confidence and provenance** — ADR-0004 confidence-tier split plus
  source-channel contributions across plant composites.
- **Data-quality panel** — the primary-station distance breakdown, to keep the
  representativeness caveat attached to the picture.

The output is fully offline: no CDN, no external fonts, no network calls. Charts
are rendered with inline SVG and `<canvas>`.

## Inputs

A wide scoped release CSV (`data/processed/scoped_plant_ecwt*_release_<ts>.csv`)
containing at least:

- `plant_latitude`, `plant_longitude`, `ecwt_f`, `plant_state`, `plant_name`
- optional: `primary_station_distance_km` (drives the data-quality panel)
- optional ADR-0004 fields: `confidence_tier`, `needs_review`, `reason`,
  `source_channels`, `coverage_basis`, `publication_caveat`

## Build

```bash
python scripts/build_ecwt_dashboard.py \
  --release-csv data/processed/scoped_plant_ecwt_adr0004_release_<ts>.csv \
  --output build/EOP012_ADR0004_ECWT_dashboard.html
```

Standard library only — no third-party dependencies. Open the resulting file in
any browser, or double-click it.

## Files

- `scripts/build_ecwt_dashboard.py` — reads the release CSV, computes aggregates,
  embeds the data, and writes the standalone HTML.
- `viz/dashboard_template.html` — the markup/CSS/JS template with a single
  `__ECWT_DATA__` placeholder where the embedded dataset is injected.

## Publication policy

The generated HTML embeds derived plant data and is part of the published ECWT
release surface when a run is promoted. Commit the rendered dashboard alongside
the release CSV and checksum manifest, or additionally publish it as:

- a **GitHub Pages** page (e.g. a `gh-pages` branch or `/docs` site), or
- a **release asset** alongside the release bundle, with a SHA-256 checksum.

## Caveat

The dashboard reflects whatever release CSV it is given. The generated page
surfaces source release, confidence tiers, review reasons, source-channel
contributions, and station-distance buckets so diagnostic releases and
ADR-0004 analytical releases do not get visually conflated. Regenerate it after
any release that changes the adequacy or representativeness treatment
(see `docs/adr/`).
