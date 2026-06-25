# NOAA Source Lineage Normalization Report

Generated UTC: 2026-06-24T21:36:36+00:00

## Run

- Calculation run ID: `noaa_source_lineage_normalization_20260624T213521Z`
- Code commit: `cf510337201a437077bcbcb8697a0b7d3800a809`
- Dry run: `False`
- Hourly relink skipped: `False`
- Candidate file limit: `5`
- Source year filter: `none`
- Mapping CSV: `noaa_source_lineage_normalization_20260624T213521Z_mapping.csv`

## Summary

| Metric | Count |
| --- | ---: |
| Candidate loaded file rows selected | 5 |
| Files hashed and mapped | 5 |
| Distinct new source_file rows | 5 |
| Exceptions | 0 |
| Hourly rows relinked | 3185 |

## Before Counts

| Metric | Count |
| --- | ---: |
| Loaded file rows | 62318 |
| Loaded file rows needing lineage | 27561 |
| Paths needing lineage | 27561 |
| Canonical hourly rows | 50346347 |
| Canonical hourly rows needing lineage | 17465507 |

## After Counts

| Metric | Count |
| --- | ---: |
| Loaded file rows | 62318 |
| Loaded file rows needing lineage | 27556 |
| Paths needing lineage | 27556 |
| Canonical hourly rows | 50346347 |
| Canonical hourly rows needing lineage | 17462322 |
| Mapping rows for this run | 5 |
| Distinct new source files for this run | 5 |
| Hourly rows relinked for this run | 3185 |

## Files Hashed By Source Year

| Source Year | Files |
| ---: | ---: |
| 2006 | 5 |

## Hourly Relink By Source Year

| Source Year | Hourly Rows Relinked |
| ---: | ---: |
| 2006 | 3185 |

## Interpretation

- This script does not change temperatures, station-hour selection, coverage, or ECWT values.
- It replaces coarse local-inventory source IDs with SHA-256-backed per-file NOAA Global Hourly source records.
- Relinking `weather.hourly_djf` closes the audit gap for the rows actually used by ECWT calculations.
- Any remaining rows needing lineage after this run should be treated as explicit source-audit debt before a compliance-facing release.
