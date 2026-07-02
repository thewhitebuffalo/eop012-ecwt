# EOP-012 ECWT — Extreme Cold Weather Temperatures for U.S. Generating Plants

An open, auditable calculation of the NERC **EOP-012 Extreme Cold Weather
Temperature (ECWT)** — the lowest 0.2 percentile of December–February hourly
dry-bulb temperatures since 2000 — for ~16,000 U.S. generating plants in the
EIA-860 universe, computed from NOAA observational hourly data with per-hour
station provenance.

- **~15,900 plants** with a published ECWT at ≥95% winter-hour coverage
  (ADR-0005 publication floor); rows below the floor are held, not guessed.
- Every published value traces to its NOAA stations, hour counts, and coverage.
- MIT licensed. Analytical output — **not a compliance filing** (see
  [Disclaimers](#disclaimers)).

## Get the ECWT for your plant

- **Interactive dashboard:**
  [thewhitebuffalo.github.io/eop012-ecwt](https://thewhitebuffalo.github.io/eop012-ecwt/) —
  or download the self-contained
  [`build/EOP012_ADR0004_ECWT_dashboard.html`](build/EOP012_ADR0004_ECWT_dashboard.html)
  and open it locally (fully offline, no network calls). Search your plant by
  name or click it on the map; the detail panel shows the ECWT, coverage,
  contributing weather stations and distances, and the stations that set the
  coldest tail.
- **Full data:** download the scoped release CSV
  (`scoped_plant_ecwt_*_release_*.csv`) from the matching
  [Release](https://github.com/thewhitebuffalo/eop012-ecwt/releases). Each row
  carries the plant's ECWT plus its complete provenance. Verify downloads
  against the `*_SHA256SUMS.txt` manifest kept in
  [`data/processed/`](data/processed/).

## Generate a NERC RSAW R1 worksheet

Select a plant in the dashboard and click **Generate RSAW R1 worksheet** to
download an editable Word document pre-filling the EOP-012-3 Requirement R1
Registered Entity Response (ECWT value, calculation date, temperature-data
sources, missing-data adjustments, compliance narrative) from the published
record. R1 is the only requirement this dataset can document; review before
submission. See [`docs/rsaw/`](docs/rsaw/) for the NERC source worksheet and
the field-by-field mapping.

## Methodology and auditability

- **Method:** for each plant, populate all ~55,000 winter hours from the
  nearest NOAA stations outward, keep per-hour provenance, then take the
  lowest 0.2 percentile (Excel `PERCENTILE.INC` / `percentile_cont` at 0.002).
  Details: [`docs/methodology.md`](docs/methodology.md).
- **Decisions:** the ADR series in [`docs/adr/`](docs/adr/) records every
  methodological decision, including the
  [ADR-0005 publication floor](docs/adr/0005-ecwt-publication-floor.md).
- **Validation:** every release is checked by
  [`scripts/validate_ecwt_release.py`](scripts/validate_ecwt_release.py)
  ([how to run](docs/validating_ecwt_release.md)) and checksummed.
- **Findings:** data-integrity issues are documented openly in
  [`docs/findings/`](docs/findings/) and [`docs/whitepaper/`](docs/whitepaper/).

## Repository layout

| Path | What it is |
| --- | --- |
| `scripts/` | Pipeline and analysis scripts (Python stdlib + Postgres via `psql`) |
| `docs/` | Methodology, ADRs, data dictionary, findings, RSAW mapping |
| `viz/` + `build/` | Dashboard template, builder assets, and the built dashboard |
| `data/processed/` | Release checksum manifests (data CSVs live in Releases) |
| `tests/` | Test suite — run `python tests/run_all.py` |
| `sql/` | Audit schema |

## Reproduce

The pipeline runs on Python 3.10+ (standard library; `openpyxl` only for the
Excel export) against a local PostgreSQL loaded from EIA-860 and NOAA Global
Hourly. Setup and data loading: [`docs/REPRODUCING.md`](docs/REPRODUCING.md).
Rebuild the dashboard from any scoped release CSV:

```bash
python scripts/build_ecwt_dashboard.py \
  --release-csv scoped_plant_ecwt_<...>_release_<ts>.csv \
  --output build/EOP012_ADR0004_ECWT_dashboard.html
```

Release outputs are large (~500 MB/run) and regenerate on every run, so they
are published as **GitHub Release assets**, never committed
(`data/processed/*.csv` is git-ignored).

## Contribute or report a data error

The most valuable contribution is a **data error report** from someone who
knows a site: if a plant's ECWT, location, or station assignment looks wrong,
[open a data-error issue](https://github.com/thewhitebuffalo/eop012-ecwt/issues/new/choose)
with the plant name, EIA code, and what you expected. Code and docs PRs are
welcome — see [`CONTRIBUTING.md`](CONTRIBUTING.md). CI runs the test suite on
every PR.

## Support the project

If the dashboard or an RSAW worksheet saved you real time, you can
[give back what it was worth](https://www.buymeacoffee.com/whitebuffalo) —
contributions keep the dataset current and free for everyone.

## Disclaimers

This project is analytical. Generated worksheets and published values are not,
by themselves, compliance filings; registered entities must review values and
documentation before use. The NERC RSAW template in `docs/rsaw/` is NERC's
property, included with attribution to support compliance preparation — always
confirm the current version at [nerc.com](https://www.nerc.com/).
