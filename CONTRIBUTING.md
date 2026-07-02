# Contributing

Thanks for helping make the ECWT dataset more accurate and useful.

## The most valuable contribution: data error reports

If you know a generating site and something looks wrong — the ECWT value, the
plant location, the assigned weather stations, the coverage — please
[open a data-error issue](https://github.com/thewhitebuffalo/eop012-ecwt/issues/new/choose).
Include the plant name, EIA plant code, what you expected, and any evidence
(design docs, local station knowledge, operating history). Reports from people
who know their sites are this project's QA program.

## Code and docs

- **Tests must pass:** `python tests/run_all.py` (Python 3.10+, stdlib only).
  CI runs the same suite plus a dashboard build check on every PR.
- **Methodology changes require an ADR** in `docs/adr/` (see ADR-0001…0005 for
  the format). The ECWT definition and publication gates only change through a
  reviewed ADR.
- **Template edits** (`viz/dashboard_template.html`): rebuild the dashboard
  from a scoped release CSV and commit the regenerated
  `build/EOP012_ADR0004_ECWT_dashboard.html` in the same PR. The output must
  stay fully self-contained and offline (no CDN, no external requests).
- **Data files:** never commit release output CSVs (`data/processed/*.csv` is
  git-ignored). Per-run outputs are published as GitHub Release assets with a
  SHA-256 manifest.
- **Dependencies:** the pipeline is deliberately standard-library-only (plus
  `openpyxl` for the Excel export). PRs adding runtime dependencies need a
  strong justification.

## Branch protection

`main` requires one approving review and green CI. Keep PRs focused; describe
what changed and how you verified it.
