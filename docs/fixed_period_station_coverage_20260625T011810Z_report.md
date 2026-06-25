# Fixed-Period Coverage Diagnostic for Strict Plant ECWT Candidates

## Technical Summary

The current strict readiness run has `1,964` publication candidates under the active-window denominator. When the same selected stations are tested against a fixed `2000-2025` DJF denominator, only `8` rows pass coverage >= `0.95`. `2` more rows are between `0.90` and `0.95`.

The median fixed-period coverage ratio is `0.1538` with a median of `5` loaded station-years out of `26`. This means the current strict publication-candidate label should remain provisional until the readiness denominator policy is corrected.

## Scope and Source Runs

- Diagnostic run: `fixed_period_station_coverage_20260625T011810Z`
- Generated at UTC: `2026-06-25T01:18:21+00:00`
- Code commit: `6ab210b121a1744568155c601c661c1cc425001b`
- Readiness run: `plant_ecwt_readiness_20260625T005939Z`
- Plant ECWT run: `plant_ecwt_provisional_20260625T005854Z`
- Station-year coverage run: `station_year_djf_coverage_20260625T002229Z`
- Active-window denominator from readiness run: `fixed selected-station active-period DJF hours`
- Fixed denominator: `2000-2025` DJF hours, `56328` hours per selected station.
- Fixed pass gate used in this diagnostic: coverage ratio >= `0.95` and at least `20` loaded station-years.
- Detailed CSV: `fixed_period_station_coverage_20260625T011810Z.csv`

## Fixed-Period Status Counts

| Status | Rows | Share |
| --- | --- | --- |
| fixed_period_low_coverage | 1,954 | 99.5% |
| fixed_period_pass | 8 | 0.4% |
| fixed_period_near_pass | 2 | 0.1% |

## Coverage Distribution

| Metric | Value |
| --- | ---: |
| Minimum fixed-period coverage | 0.0374 |
| Median fixed-period coverage | 0.1538 |
| Maximum fixed-period coverage | 0.9764 |
| Median loaded station-years | 5 |
| Rows with selected station metadata ending before 2010 | 1,224 |

## Rows Passing Fixed-Period Gate

| Plant | State | Station | Active Coverage | Fixed Coverage | Loaded Years | Years | Distance km | ECWT F | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 54476 Sumas Power Plant | WA | 711080-99999 ABBOTSFORD | 0.9895 | 0.9764 | 26 | 2000-2025 | 7.6 | 10.4 | fixed_period_pass |
| 60444 Glacier Battery Storage | WA | 711080-99999 ABBOTSFORD | 0.9895 | 0.9764 | 26 | 2000-2025 | 34.0 | 10.4 | fixed_period_pass |
| 54249 Smith Falls Hydro Project | ID | 717700-99999 CRESTON CAMPBELL SCIENTIFIC  BC | 0.9812 | 0.9682 | 26 | 2000-2025 | 14.4 | -5.1 | fixed_period_pass |
| 2583 Macomb | NY | 717120-99999 ST ANICET 1  QUE | 0.9761 | 0.9632 | 26 | 2000-2025 | 26.7 | -23.6 | fixed_period_pass |
| 62784 Franklin Solar Site | NY | 717120-99999 ST ANICET 1  QUE | 0.9761 | 0.9632 | 26 | 2000-2025 | 27.7 | -23.6 | fixed_period_pass |
| 62785 Malone Solar Site | NY | 717120-99999 ST ANICET 1  QUE | 0.9761 | 0.9632 | 26 | 2000-2025 | 27.4 | -23.6 | fixed_period_pass |
| 65379 OYA State Route 122 | NY | 717120-99999 ST ANICET 1  QUE | 0.9761 | 0.9632 | 26 | 2000-2025 | 21.7 | -23.6 | fixed_period_pass |
| 3750 Canaan | VT | 716110-99999 LENOXVILLE  QUE | 0.9702 | 0.9574 | 26 | 2000-2025 | 46.7 | -24.2 | fixed_period_pass |

## Rows Near Fixed-Period Gate

| Plant | State | Station | Active Coverage | Fixed Coverage | Loaded Years | Years | Distance km | ECWT F | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 58696 Nooksack Hydro | WA | 711130-99999 AGASSIZ CS | 0.9519 | 0.9394 | 26 | 2000-2025 | 38.2 | 1.9 | fixed_period_near_pass |
| 58180 UNH 7.9 MW Plant | NH | 999999-54795 DURHAM 2 SSW | 0.9897 | 0.9070 | 25 | 2001-2025 | 3.2 | -9.0 | fixed_period_near_pass |

## Lowest Fixed-Period Coverage Rows

| Plant | State | Station | Active Coverage | Fixed Coverage | Loaded Years | Years | Distance km | ECWT F | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 6092 Spirit Mound | SD | 720332-99999 HAROLD DAVIDSON FLD | 0.9741 | 0.0374 | 2 | 2024-2025 | 15.5 | -14.8 | fixed_period_low_coverage |
| 68230 SR Des Arc | AR | 720827-99999 CARLISLE MUNI | 0.9792 | 0.0375 | 2 | 2024-2025 | 25.4 | 12.6 | fixed_period_low_coverage |
| 58322 Prairie Breeze | NE | 720846-99999 ANTELOPE CO | 0.9829 | 0.0377 | 2 | 2024-2025 | 18.1 | -22.0 | fixed_period_low_coverage |
| 60262 Prairie Breeze II | NE | 720846-99999 ANTELOPE CO | 0.9829 | 0.0377 | 2 | 2024-2025 | 19.8 | -22.0 | fixed_period_low_coverage |
| 60314 Prairie Breeze III | NE | 720846-99999 ANTELOPE CO | 0.9829 | 0.0377 | 2 | 2024-2025 | 19.8 | -22.0 | fixed_period_low_coverage |
| 61784 Upstream Wind Energy LLC | NE | 720846-99999 ANTELOPE CO | 0.9829 | 0.0377 | 2 | 2024-2025 | 10.1 | -22.0 | fixed_period_low_coverage |
| 62956 Thunderhead Wind Energy LLC | NE | 720846-99999 ANTELOPE CO | 0.9829 | 0.0377 | 2 | 2024-2025 | 17.4 | -22.0 | fixed_period_low_coverage |
| 50961 Slate Creek | CA | 721027-99999 TRINITY CENTER | 0.9870 | 0.0378 | 2 | 2012-2013 | 20.0 | 15.8 | fixed_period_low_coverage |
| 10765 Indeck Jonesboro Energy Center | ME | 998253-99999 CUTLER | 1.5064 | 0.0379 | 2 | 2009-2010 | 19.8 | 5.6 | fixed_period_low_coverage |
| 66664 Dublin Street LLC | ME | 998253-99999 CUTLER | 1.5064 | 0.0379 | 2 | 2009-2010 | 14.6 | 5.6 | fixed_period_low_coverage |
| 55173 Acadia Energy Center | LA | 725257-99999 JENNINGS | 0.9931 | 0.0381 | 2 | 2012-2013 | 32.4 | 32.0 | fixed_period_low_coverage |
| 55433 Bayou Cove Peaking Power | LA | 725257-99999 JENNINGS | 0.9931 | 0.0381 | 2 | 2012-2013 | 8.3 | 32.0 | fixed_period_low_coverage |
| 66558 Mowata Solar | LA | 725257-99999 JENNINGS | 0.9931 | 0.0381 | 2 | 2012-2013 | 30.6 | 32.0 | fixed_period_low_coverage |
| 66615 Eunice LA Plant | LA | 725257-99999 JENNINGS | 0.9931 | 0.0381 | 2 | 2012-2013 | 27.8 | 32.0 | fixed_period_low_coverage |
| 68662 Luicain Solar | LA | 725257-99999 JENNINGS | 0.9931 | 0.0381 | 2 | 2012-2013 | 25.5 | 32.0 | fixed_period_low_coverage |
| 2707 Blewett | NC | 722043-03738 ROCKINGHAM AIRPORT | 1.0042 | 0.0381 | 1 | 2005-2005 | 14.9 | 14.5 | fixed_period_low_coverage |
| 60439 Sellers Farm Solar | NC | 722043-03738 ROCKINGHAM AIRPORT | 1.0042 | 0.0381 | 1 | 2005-2005 | 8.6 | 14.5 | fixed_period_low_coverage |
| 62167 County Home Solar LLC | NC | 722043-03738 ROCKINGHAM AIRPORT | 1.0042 | 0.0381 | 1 | 2005-2005 | 5.1 | 14.5 | fixed_period_low_coverage |
| 63377 ESA Hamlet NC , LLC | NC | 722043-03738 ROCKINGHAM AIRPORT | 1.0042 | 0.0381 | 1 | 2005-2005 | 7.9 | 14.5 | fixed_period_low_coverage |
| 65241 McKinney BESS | NC | 722043-03738 ROCKINGHAM AIRPORT | 1.0042 | 0.0381 | 1 | 2005-2005 | 1.7 | 14.5 | fixed_period_low_coverage |
| ... | 1944 more rows omitted |  |  |  |  |  |  |  |  |

## Largest Active-to-Fixed Coverage Drops

| Plant | State | Station | Active Coverage | Fixed Coverage | Loaded Years | Years | Distance km | ECWT F | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 10765 Indeck Jonesboro Energy Center | ME | 998253-99999 CUTLER | 1.5064 | 0.0379 | 2 | 2009-2010 | 19.8 | 5.6 | fixed_period_low_coverage |
| 66664 Dublin Street LLC | ME | 998253-99999 CUTLER | 1.5064 | 0.0379 | 2 | 2009-2010 | 14.6 | 5.6 | fixed_period_low_coverage |
| 2707 Blewett | NC | 722043-03738 ROCKINGHAM AIRPORT | 1.0042 | 0.0381 | 1 | 2005-2005 | 14.9 | 14.5 | fixed_period_low_coverage |
| 60439 Sellers Farm Solar | NC | 722043-03738 ROCKINGHAM AIRPORT | 1.0042 | 0.0381 | 1 | 2005-2005 | 8.6 | 14.5 | fixed_period_low_coverage |
| 62167 County Home Solar LLC | NC | 722043-03738 ROCKINGHAM AIRPORT | 1.0042 | 0.0381 | 1 | 2005-2005 | 5.1 | 14.5 | fixed_period_low_coverage |
| 63377 ESA Hamlet NC , LLC | NC | 722043-03738 ROCKINGHAM AIRPORT | 1.0042 | 0.0381 | 1 | 2005-2005 | 7.9 | 14.5 | fixed_period_low_coverage |
| 65241 McKinney BESS | NC | 722043-03738 ROCKINGHAM AIRPORT | 1.0042 | 0.0381 | 1 | 2005-2005 | 1.7 | 14.5 | fixed_period_low_coverage |
| 66373 Polk Farm | NC | 722043-03738 ROCKINGHAM AIRPORT | 1.0042 | 0.0381 | 1 | 2005-2005 | 10.2 | 14.5 | fixed_period_low_coverage |
| 56870 Taylor | GA | 720959-99999 BUTLER MUNI | 0.9986 | 0.0387 | 2 | 2011-2012 | 18.1 | 26.6 | fixed_period_low_coverage |
| 59891 Butler Solar Farm 20 | GA | 720959-99999 BUTLER MUNI | 0.9986 | 0.0387 | 2 | 2011-2012 | 6.2 | 26.6 | fixed_period_low_coverage |
| 59894 Pawpaw Solar Plant | GA | 720959-99999 BUTLER MUNI | 0.9986 | 0.0387 | 2 | 2011-2012 | 0.8 | 26.6 | fixed_period_low_coverage |
| 59896 Butler Solar Project 103 | GA | 720959-99999 BUTLER MUNI | 0.9986 | 0.0387 | 2 | 2011-2012 | 2.4 | 26.6 | fixed_period_low_coverage |
| 59897 Taylor County Solar | GA | 720959-99999 BUTLER MUNI | 0.9986 | 0.0387 | 2 | 2011-2012 | 4.6 | 26.6 | fixed_period_low_coverage |
| 60064 White Pine Solar, LLC | GA | 720959-99999 BUTLER MUNI | 0.9986 | 0.0387 | 2 | 2011-2012 | 6.9 | 26.6 | fixed_period_low_coverage |
| 65884 Sandhill Solar 2 | GA | 720959-99999 BUTLER MUNI | 0.9986 | 0.0387 | 2 | 2011-2012 | 8.1 | 26.6 | fixed_period_low_coverage |
| 67755 Little Trout Solar | MI | 727417-99999 PRESQUE ISLE CO | 0.9982 | 0.0387 | 2 | 2004-2005 | 9.0 | -0.4 | fixed_period_low_coverage |
| 62448 Lapetus | TX | 721032-99999 ANDREWS CO | 0.9958 | 0.0382 | 2 | 2012-2013 | 19.6 | 17.6 | fixed_period_low_coverage |
| 62630 Jumbo Hill Wind Project | TX | 721032-99999 ANDREWS CO | 0.9958 | 0.0382 | 2 | 2012-2013 | 39.8 | 17.6 | fixed_period_low_coverage |
| 62755 Prospero Solar | TX | 721032-99999 ANDREWS CO | 0.9958 | 0.0382 | 2 | 2012-2013 | 29.6 | 17.6 | fixed_period_low_coverage |
| 63193 Alira | TX | 721032-99999 ANDREWS CO | 0.9958 | 0.0382 | 2 | 2012-2013 | 41.2 | 17.6 | fixed_period_low_coverage |
| ... | 1944 more rows omitted |  |  |  |  |  |  |  |  |

## Interpretation

The active-window denominator answers a narrow parser question: how complete are the loaded rows during the station's represented active period. It does not answer whether the selected station has adequate coverage across the intended ECWT analysis period.

For a compliance-facing national plant ECWT release, the fixed-period diagnostic is the more conservative publication-control view. The current `publication_candidate` cohort is therefore best treated as a provisional math output, not a release-ready compliance dataset.

## Recommended Next Steps

1. Replace or supplement the current readiness gate with a fixed-period coverage gate before release-candidate export.
2. Decide the required fixed analysis period and minimum loaded-year rule from the EOP-012/EPRI method notes, then encode it in `calc.plant_ecwt_readiness` or a successor release-readiness table.
3. Re-run station selection after applying the fixed-period rule, because many plants may need a different station than the current active-window winner.
