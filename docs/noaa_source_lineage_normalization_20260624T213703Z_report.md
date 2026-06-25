# NOAA Source Lineage Normalization Report

Generated UTC: 2026-06-25T00:02:25+00:00

## Run

- Calculation run ID: `noaa_source_lineage_normalization_20260624T213703Z`
- Code commit: `cf510337201a437077bcbcb8697a0b7d3800a809`
- Dry run: `False`
- Hourly relink skipped: `False`
- Candidate file limit: `none`
- Source year filter: `none`
- Mapping CSV: `noaa_source_lineage_normalization_20260624T213703Z_mapping.csv`

## Summary

| Metric | Count |
| --- | ---: |
| Candidate loaded file rows selected | 27556 |
| Files hashed and mapped | 27556 |
| Distinct new source_file rows | 27556 |
| Exceptions | 0 |
| Hourly rows relinked | 17462322 |

## Before Counts

| Metric | Count |
| --- | ---: |
| Loaded file rows | 62318 |
| Loaded file rows needing lineage | 27556 |
| Paths needing lineage | 27556 |
| Canonical hourly rows | 50346347 |
| Canonical hourly rows needing lineage | 17462322 |

## After Counts

| Metric | Count |
| --- | ---: |
| Loaded file rows | 62318 |
| Loaded file rows needing lineage | 0 |
| Paths needing lineage | 0 |
| Canonical hourly rows | 50346347 |
| Canonical hourly rows needing lineage | 0 |
| Mapping rows for this run | 27556 |
| Distinct new source files for this run | 27556 |
| Hourly rows relinked for this run | 17462322 |

## Files Hashed By Source Year

| Source Year | Files |
| ---: | ---: |
| 2006 | 1999 |
| 2012 | 1978 |
| 2013 | 2021 |
| 2014 | 2035 |
| 2015 | 2837 |
| 2016 | 1867 |
| 2017 | 2104 |
| 2018 | 1973 |
| 2019 | 1968 |
| 2020 | 1978 |
| 2021 | 1973 |
| 2022 | 1983 |
| 2024 | 2840 |

## Hourly Relink By Source Year

| Source Year | Hourly Rows Relinked |
| ---: | ---: |
| 2006 | 1985941 |
| 2012 | 1238113 |
| 2013 | 1321443 |
| 2014 | 1238485 |
| 2015 | 1829693 |
| 2016 | 830235 |
| 2017 | 1141502 |
| 2018 | 1066296 |
| 2019 | 1137972 |
| 2020 | 1063475 |
| 2021 | 1157948 |
| 2022 | 1058154 |
| 2024 | 2393065 |

## Interpretation

- This script does not change temperatures, station-hour selection, coverage, or ECWT values.
- It replaces coarse local-inventory source IDs with SHA-256-backed per-file NOAA Global Hourly source records.
- Relinking `weather.hourly_djf` closes the audit gap for the rows actually used by ECWT calculations.
- Any remaining rows needing lineage after this run should be treated as explicit source-audit debt before a compliance-facing release.
