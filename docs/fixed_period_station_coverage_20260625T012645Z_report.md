# Fixed-Period Coverage Diagnostic for Strict Plant ECWT Candidates

## Technical Summary

The current readiness run has `162` publication candidates under its recorded denominator (`plant ECWT row valid/expected DJF hours`). When the same selected stations are tested against a fixed `2000-2025` DJF denominator, `162` rows pass coverage >= `0.95`. `0` more rows are between `0.90` and `0.95`.

The median fixed-period coverage ratio is `0.9596` with a median of `26` loaded station-years out of `26`. This fixed-period-selected cohort satisfies the fixed coverage gate. The remaining publication risk is no longer the denominator itself; it is station-selection review, especially distance, rank, and cross-border assignments.

## Scope and Source Runs

- Diagnostic run: `fixed_period_station_coverage_20260625T012645Z`
- Generated at UTC: `2026-06-25T01:26:56+00:00`
- Code commit: `66ddcb9ea5b2b19f69f72150ca414ac4840ca969`
- Readiness run: `plant_ecwt_readiness_fixed_period_20260625T012416Z`
- Plant ECWT run: `plant_ecwt_provisional_fixed_period_20260625T012402Z`
- Station-year coverage run: `station_year_djf_coverage_20260625T002229Z`
- Readiness denominator from run: `plant ECWT row valid/expected DJF hours`
- Fixed denominator: `2000-2025` DJF hours, `56328` hours per selected station.
- Fixed pass gate used in this diagnostic: coverage ratio >= `0.95` and at least `20` loaded station-years.
- Detailed CSV: `fixed_period_station_coverage_20260625T012645Z.csv`

## Fixed-Period Status Counts

| Status | Rows | Share |
| --- | --- | --- |
| fixed_period_pass | 162 | 100.0% |

## Coverage Distribution

| Metric | Value |
| --- | ---: |
| Minimum fixed-period coverage | 0.9501 |
| Median fixed-period coverage | 0.9596 |
| Maximum fixed-period coverage | 0.9764 |
| Median loaded station-years | 26 |
| Rows with selected station metadata ending before 2010 | 0 |

## Rows Passing Fixed-Period Gate

| Plant | State | Station | Active Coverage | Fixed Coverage | Loaded Years | Years | Distance km | ECWT F | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3855 Lower Baker | WA | 711080-99999 ABBOTSFORD | 0.9764 | 0.9764 | 26 | 2000-2025 | 70.0 | 10.4 | fixed_period_pass |
| 3861 Upper Baker | WA | 711080-99999 ABBOTSFORD | 0.9764 | 0.9764 | 26 | 2000-2025 | 64.6 | 10.4 | fixed_period_pass |
| 54267 Koma Kulshan | WA | 711080-99999 ABBOTSFORD | 0.9764 | 0.9764 | 26 | 2000-2025 | 60.5 | 10.4 | fixed_period_pass |
| 54476 Sumas Power Plant | WA | 711080-99999 ABBOTSFORD | 0.9764 | 0.9764 | 26 | 2000-2025 | 7.6 | 10.4 | fixed_period_pass |
| 54537 Ferndale Generating Station | WA | 711080-99999 ABBOTSFORD | 0.9764 | 0.9764 | 26 | 2000-2025 | 32.1 | 10.4 | fixed_period_pass |
| 58696 Nooksack Hydro | WA | 711080-99999 ABBOTSFORD | 0.9764 | 0.9764 | 26 | 2000-2025 | 42.1 | 10.4 | fixed_period_pass |
| 60444 Glacier Battery Storage | WA | 711080-99999 ABBOTSFORD | 0.9764 | 0.9764 | 26 | 2000-2025 | 34.0 | 10.4 | fixed_period_pass |
| 6120 Whitehorn | WA | 711080-99999 ABBOTSFORD | 0.9764 | 0.9764 | 26 | 2000-2025 | 32.3 | 10.4 | fixed_period_pass |
| 7870 Encogen | WA | 711080-99999 ABBOTSFORD | 0.9764 | 0.9764 | 26 | 2000-2025 | 32.3 | 10.4 | fixed_period_pass |
| 55638 Walhalla | ND | 711470-99999 CARMAN U OF M CS  MAN | 0.9697 | 0.9697 | 26 | 2000-2025 | 66.6 | -31.0 | fixed_period_pass |
| 54249 Smith Falls Hydro Project | ID | 717700-99999 CRESTON CAMPBELL SCIENTIFIC  BC | 0.9682 | 0.9682 | 26 | 2000-2025 | 14.4 | -5.1 | fixed_period_pass |
| 6506 Moyie Springs | ID | 717700-99999 CRESTON CAMPBELL SCIENTIFIC  BC | 0.9682 | 0.9682 | 26 | 2000-2025 | 45.5 | -5.1 | fixed_period_pass |
| 6172 Libby | MT | 717700-99999 CRESTON CAMPBELL SCIENTIFIC  BC | 0.9682 | 0.9682 | 26 | 2000-2025 | 114.7 | -5.1 | fixed_period_pass |
| 3891 Box Canyon | WA | 717700-99999 CRESTON CAMPBELL SCIENTIFIC  BC | 0.9682 | 0.9682 | 26 | 2000-2025 | 75.0 | -5.1 | fixed_period_pass |
| 773 Sullivan CR | WA | 717700-99999 CRESTON CAMPBELL SCIENTIFIC  BC | 0.9682 | 0.9682 | 26 | 2000-2025 | 66.4 | -5.1 | fixed_period_pass |
| 50650 ReEnergy Stratton LLC | ME | 716100-99999 SHERBROOKE | 0.9677 | 0.9677 | 26 | 2000-2025 | 104.4 | -25.6 | fixed_period_pass |
| 50999 Aziscohos Hydroelectric Project | ME | 716100-99999 SHERBROOKE | 0.9677 | 0.9677 | 26 | 2000-2025 | 77.4 | -25.6 | fixed_period_pass |
| 56829 Kibby Wind Facility | ME | 716100-99999 SHERBROOKE | 0.9677 | 0.9677 | 26 | 2000-2025 | 91.1 | -25.6 | fixed_period_pass |
| 66962 ME Novel Lighthouse - Carrabassett | ME | 716100-99999 SHERBROOKE | 0.9677 | 0.9677 | 26 | 2000-2025 | 112.1 | -25.6 | fixed_period_pass |
| 50091 Sheep Creek Hydro | WA | 717760-99999 NELSON  BC | 0.9650 | 0.9650 | 26 | 2000-2025 | 69.5 | -3.1 | fixed_period_pass |
| ... | 142 more rows omitted |  |  |  |  |  |  |  |  |

## Rows Near Fixed-Period Gate

_None._

## Lowest Fixed-Period Coverage Rows

| Plant | State | Station | Active Coverage | Fixed Coverage | Loaded Years | Years | Distance km | ECWT F | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 56606 Culbertson Generation Station | MT | 715160-99999 CORONACH SPC  SASK | 0.9501 | 0.9501 | 26 | 2000-2025 | 123.1 | -32.8 | fixed_period_pass |
| 56833 OREG 1 Inc | MT | 715160-99999 CORONACH SPC  SASK | 0.9501 | 0.9501 | 26 | 2000-2025 | 122.5 | -32.8 | fixed_period_pass |
| 56880 OREG 2 Inc | MT | 715160-99999 CORONACH SPC  SASK | 0.9501 | 0.9501 | 26 | 2000-2025 | 122.5 | -32.8 | fixed_period_pass |
| 60595 Sand Creek Wind Farm | MT | 715160-99999 CORONACH SPC  SASK | 0.9501 | 0.9501 | 26 | 2000-2025 | 126.7 | -32.8 | fixed_period_pass |
| 6623 Fort Peck | MT | 715160-99999 CORONACH SPC  SASK | 0.9501 | 0.9501 | 26 | 2000-2025 | 134.2 | -32.8 | fixed_period_pass |
| 57192 Spring Valley Wind Project | NV | 724797-23176 MILFORD MUNI BRISCOE | 0.9514 | 0.9514 | 26 | 2000-2025 | 149.0 | -9.9 | fixed_period_pass |
| 68017 Cooper Canyon Renewable Energy | NV | 724797-23176 MILFORD MUNI BRISCOE | 0.9514 | 0.9514 | 26 | 2000-2025 | 149.5 | -9.9 | fixed_period_pass |
| 299 Blundell | UT | 724797-23176 MILFORD MUNI BRISCOE | 0.9514 | 0.9514 | 26 | 2000-2025 | 16.3 | -9.9 | fixed_period_pass |
| 3643 Upper Beaver | UT | 724797-23176 MILFORD MUNI BRISCOE | 0.9514 | 0.9514 | 26 | 2000-2025 | 49.6 | -9.9 | fixed_period_pass |
| 57079 Milford Wind Corridor I LLC | UT | 724797-23176 MILFORD MUNI BRISCOE | 0.9514 | 0.9514 | 26 | 2000-2025 | 15.0 | -9.9 | fixed_period_pass |
| 57107 Milford Wind Corridor Stage II LLC | UT | 724797-23176 MILFORD MUNI BRISCOE | 0.9514 | 0.9514 | 26 | 2000-2025 | 20.1 | -9.9 | fixed_period_pass |
| 57353 Thermo No 1 | UT | 724797-23176 MILFORD MUNI BRISCOE | 0.9514 | 0.9514 | 26 | 2000-2025 | 32.4 | -9.9 | fixed_period_pass |
| 58130 Blue Mountain Biogas | UT | 724797-23176 MILFORD MUNI BRISCOE | 0.9514 | 0.9514 | 26 | 2000-2025 | 36.5 | -9.9 | fixed_period_pass |
| 58570 Cove Fort | UT | 724797-23176 MILFORD MUNI BRISCOE | 0.9514 | 0.9514 | 26 | 2000-2025 | 41.1 | -9.9 | fixed_period_pass |
| 58598 Beryl Solar Plant | UT | 724797-23176 MILFORD MUNI BRISCOE | 0.9514 | 0.9514 | 26 | 2000-2025 | 102.5 | -9.9 | fixed_period_pass |
| 58599 Cedar Valley Solar Plant | UT | 724797-23176 MILFORD MUNI BRISCOE | 0.9514 | 0.9514 | 26 | 2000-2025 | 68.0 | -9.9 | fixed_period_pass |
| 58600 Buckhorn Solar Plant | UT | 724797-23176 MILFORD MUNI BRISCOE | 0.9514 | 0.9514 | 26 | 2000-2025 | 50.4 | -9.9 | fixed_period_pass |
| 58601 Milford Flat Solar Plant | UT | 724797-23176 MILFORD MUNI BRISCOE | 0.9514 | 0.9514 | 26 | 2000-2025 | 14.0 | -9.9 | fixed_period_pass |
| 58602 Laho Solar Plant | UT | 724797-23176 MILFORD MUNI BRISCOE | 0.9514 | 0.9514 | 26 | 2000-2025 | 14.1 | -9.9 | fixed_period_pass |
| 58603 Greenville Solar Plant | UT | 724797-23176 MILFORD MUNI BRISCOE | 0.9514 | 0.9514 | 26 | 2000-2025 | 30.4 | -9.9 | fixed_period_pass |
| ... | 142 more rows omitted |  |  |  |  |  |  |  |  |

## Largest Active-to-Fixed Coverage Drops

| Plant | State | Station | Active Coverage | Fixed Coverage | Loaded Years | Years | Distance km | ECWT F | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3855 Lower Baker | WA | 711080-99999 ABBOTSFORD | 0.9764 | 0.9764 | 26 | 2000-2025 | 70.0 | 10.4 | fixed_period_pass |
| 3861 Upper Baker | WA | 711080-99999 ABBOTSFORD | 0.9764 | 0.9764 | 26 | 2000-2025 | 64.6 | 10.4 | fixed_period_pass |
| 54267 Koma Kulshan | WA | 711080-99999 ABBOTSFORD | 0.9764 | 0.9764 | 26 | 2000-2025 | 60.5 | 10.4 | fixed_period_pass |
| 54476 Sumas Power Plant | WA | 711080-99999 ABBOTSFORD | 0.9764 | 0.9764 | 26 | 2000-2025 | 7.6 | 10.4 | fixed_period_pass |
| 54537 Ferndale Generating Station | WA | 711080-99999 ABBOTSFORD | 0.9764 | 0.9764 | 26 | 2000-2025 | 32.1 | 10.4 | fixed_period_pass |
| 58696 Nooksack Hydro | WA | 711080-99999 ABBOTSFORD | 0.9764 | 0.9764 | 26 | 2000-2025 | 42.1 | 10.4 | fixed_period_pass |
| 60444 Glacier Battery Storage | WA | 711080-99999 ABBOTSFORD | 0.9764 | 0.9764 | 26 | 2000-2025 | 34.0 | 10.4 | fixed_period_pass |
| 6120 Whitehorn | WA | 711080-99999 ABBOTSFORD | 0.9764 | 0.9764 | 26 | 2000-2025 | 32.3 | 10.4 | fixed_period_pass |
| 7870 Encogen | WA | 711080-99999 ABBOTSFORD | 0.9764 | 0.9764 | 26 | 2000-2025 | 32.3 | 10.4 | fixed_period_pass |
| 55638 Walhalla | ND | 711470-99999 CARMAN U OF M CS  MAN | 0.9697 | 0.9697 | 26 | 2000-2025 | 66.6 | -31.0 | fixed_period_pass |
| 54249 Smith Falls Hydro Project | ID | 717700-99999 CRESTON CAMPBELL SCIENTIFIC  BC | 0.9682 | 0.9682 | 26 | 2000-2025 | 14.4 | -5.1 | fixed_period_pass |
| 6506 Moyie Springs | ID | 717700-99999 CRESTON CAMPBELL SCIENTIFIC  BC | 0.9682 | 0.9682 | 26 | 2000-2025 | 45.5 | -5.1 | fixed_period_pass |
| 6172 Libby | MT | 717700-99999 CRESTON CAMPBELL SCIENTIFIC  BC | 0.9682 | 0.9682 | 26 | 2000-2025 | 114.7 | -5.1 | fixed_period_pass |
| 3891 Box Canyon | WA | 717700-99999 CRESTON CAMPBELL SCIENTIFIC  BC | 0.9682 | 0.9682 | 26 | 2000-2025 | 75.0 | -5.1 | fixed_period_pass |
| 773 Sullivan CR | WA | 717700-99999 CRESTON CAMPBELL SCIENTIFIC  BC | 0.9682 | 0.9682 | 26 | 2000-2025 | 66.4 | -5.1 | fixed_period_pass |
| 50650 ReEnergy Stratton LLC | ME | 716100-99999 SHERBROOKE | 0.9677 | 0.9677 | 26 | 2000-2025 | 104.4 | -25.6 | fixed_period_pass |
| 50999 Aziscohos Hydroelectric Project | ME | 716100-99999 SHERBROOKE | 0.9677 | 0.9677 | 26 | 2000-2025 | 77.4 | -25.6 | fixed_period_pass |
| 56829 Kibby Wind Facility | ME | 716100-99999 SHERBROOKE | 0.9677 | 0.9677 | 26 | 2000-2025 | 91.1 | -25.6 | fixed_period_pass |
| 66962 ME Novel Lighthouse - Carrabassett | ME | 716100-99999 SHERBROOKE | 0.9677 | 0.9677 | 26 | 2000-2025 | 112.1 | -25.6 | fixed_period_pass |
| 50091 Sheep Creek Hydro | WA | 717760-99999 NELSON  BC | 0.9650 | 0.9650 | 26 | 2000-2025 | 69.5 | -3.1 | fixed_period_pass |
| ... | 142 more rows omitted |  |  |  |  |  |  |  |  |

## Interpretation

The active-window denominator answers a narrow parser question: how complete are the loaded rows during the station's represented active period. It does not answer whether the selected station has adequate coverage across the intended ECWT analysis period.

For a compliance-facing national plant ECWT release, the fixed-period diagnostic is the more conservative publication-control view. The current `publication_candidate` cohort is therefore best treated as a provisional math output, not a release-ready compliance dataset.

## Recommended Next Steps

1. Replace or supplement the current readiness gate with a fixed-period coverage gate before release-candidate export.
2. Decide the required fixed analysis period and minimum loaded-year rule from the EOP-012/EPRI method notes, then encode it in `calc.plant_ecwt_readiness` or a successor release-readiness table.
3. Re-run station selection after applying the fixed-period rule, because many plants may need a different station than the current active-window winner.
