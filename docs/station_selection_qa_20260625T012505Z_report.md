# Station Selection QA for Strict Plant ECWT Candidates

## Technical Summary

This read-only QA pass reviewed `162` strict plant ECWT publication candidates from readiness run `plant_ecwt_readiness_fixed_period_20260625T012416Z`. The script found `162` rows with at least one review flag. Flags are not rejection decisions; they identify selected plant-to-station assignments that should be reviewed before any compliance-facing release.

The strict candidates use `19` distinct selected NOAA stations. The maximum selected station distance is `149.5` km, and the largest single-station concentration is `52` strict candidate plants.

## Scope and Source Runs

- QA run: `station_selection_qa_20260625T012505Z`
- Generated at UTC: `2026-06-25T01:25:05+00:00`
- Code commit: `d8aa9cfed64c5af96f8330223a12b1f5652676bb`
- Readiness run: `plant_ecwt_readiness_fixed_period_20260625T012416Z`
- Plant ECWT run: `plant_ecwt_provisional_fixed_period_20260625T012402Z`
- Strict readiness threshold: `2000` valid hours and coverage ratio >= `0.95`
- Coverage denominator: `plant ECWT row valid/expected DJF hours`
- Detailed CSV: `station_selection_qa_20260625T012505Z.csv`

## QA Flag Definitions

- Distance review: selected station is more than `50` km from the plant.
- High distance review: selected station is more than `75` km from the plant.
- Rank review: selected station was not the rank-1 candidate, or was worse than rank 3.
- Cross-border/state review: selected station country is not US, station country/state is missing, or US station state differs from plant state.
- Coverage review: strict candidate coverage is below `0.97` even though it passes the publication gate.
- Old station review: selected station metadata ends before `2010`.
- Warm ECWT review: governing ECWT is above `35` F, or mainland governing ECWT is above `32` F.
- Shared station review: one selected station governs more than `10` strict candidate plants.

## Aggregate Counts

| Metric | Count |
| --- | ---: |
| Strict publication candidates reviewed | 162 |
| Distinct selected stations | 19 |
| Rows with at least one QA flag | 162 |
| Selected station assignments with rank > 1 | 154 |
| Non-US selected stations | 110 |
| US plant/station state mismatches | 2 |
| Selected stations with last observation before 2010 | 0 |
| Mainland warm ECWT rows > 32 F | 0 |
| Near-threshold coverage rows below 0.97 | 153 |

## Risk Flag Counts

| Flag | Rows | Share |
| --- | --- | --- |
| coverage_below_0_97 | 153 | 94.4% |
| station_country_not_us | 110 | 67.9% |
| station_state_missing | 110 | 67.9% |
| selected_rank_gt_3 | 110 | 67.9% |
| shared_station_gt_25_plants | 93 | 57.4% |
| distance_gt_75km | 54 | 33.3% |
| selected_rank_gt_1 | 44 | 27.2% |
| distance_gt_50km | 43 | 26.5% |
| shared_station_gt_10_plants | 11 | 6.8% |
| plant_station_state_mismatch | 2 | 1.2% |

## Top Selected Stations by Plant Count

| Station | State | Country | Strict Candidate Plants | Max Distance km | Min Coverage | ECWT F |
| --- | --- | --- | --- | --- | --- | --- |
| 724797-23176 MILFORD MUNI BRISCOE | UT | US | 52 | 149.5 | 0.9514 | -9.9 |
| 717120-99999 ST ANICET 1  QUE |  | CA | 41 | 100.8 | 0.9632 | -23.6 |
| 716140-99999 STE CLOTHILDE  QUE |  | CA | 11 | 38.4 | 0.9569 | -23.1 |
| 711080-99999 ABBOTSFORD |  | CA | 9 | 70.0 | 0.9764 | 10.4 |
| 713720-99999 L'ACADIE  QUE |  | CA | 6 | 58.3 | 0.9597 | -21.1 |
| 715160-99999 CORONACH SPC  SASK |  | CA | 5 | 134.2 | 0.9501 | -32.8 |
| 717700-99999 CRESTON CAMPBELL SCIENTIFIC  BC |  | CA | 5 | 114.7 | 0.9682 | -5.1 |
| 711540-99999 WATERTON PARK GATE |  | CA | 4 | 120.9 | 0.9535 | -32.8 |
| 716100-99999 SHERBROOKE |  | CA | 4 | 112.1 | 0.9677 | -25.6 |
| 711140-99999 HOPE (AUT)  BC |  | CA | 4 | 78.8 | 0.9603 | -4.0 |
| 711480-99999 PILOT MOUND (AUT) |  | CA | 4 | 74.9 | 0.9606 | -31.0 |
| 716110-99999 LENOXVILLE  QUE |  | CA | 4 | 56.5 | 0.9574 | -24.2 |
| 712150-99999 OSOYOOS CS  BC |  | CA | 3 | 124.9 | 0.9596 | -3.4 |
| 712000-99999 VICTORIA GONZALES CS  BC |  | CA | 3 | 49.0 | 0.9646 | 3.9 |
| 713230-99999 BEAUCEVILLE  QUE |  | CA | 2 | 108.8 | 0.9538 | -24.2 |
| 717760-99999 NELSON  BC |  | CA | 2 | 69.5 | 0.9650 | -3.1 |
| 711160-99999 ONEFOUR CDA  ALTA |  | CA | 1 | 100.3 | 0.9630 | -28.6 |
| 712610-99999 GODERICH  ONT |  | CA | 1 | 75.0 | 0.9577 | -12.5 |
| 711470-99999 CARMAN U OF M CS  MAN |  | CA | 1 | 66.6 | 0.9697 | -31.0 |

## Farthest Selected Station Assignments

| Plant | Plant State | Station | Station State | Country | Distance km | Rank | Coverage | ECWT F | Flags |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 68017 Cooper Canyon Renewable Energy | NV | 724797-23176 MILFORD MUNI BRISCOE | UT | US | 149.5 | 9 | 0.9514 | -9.9 | distance_gt_75km;selected_rank_gt_3;plant_station_state_mismatch;coverage_below_0_97;shared_station_gt_25_plants |
| 57192 Spring Valley Wind Project | NV | 724797-23176 MILFORD MUNI BRISCOE | UT | US | 149.0 | 9 | 0.9514 | -9.9 | distance_gt_75km;selected_rank_gt_3;plant_station_state_mismatch;coverage_below_0_97;shared_station_gt_25_plants |
| 60421 Veyo Heat Recovery Project | UT | 724797-23176 MILFORD MUNI BRISCOE | UT | US | 135.8 | 10 | 0.9514 | -9.9 | distance_gt_75km;selected_rank_gt_3;coverage_below_0_97;shared_station_gt_25_plants |
| 6623 Fort Peck | MT | 715160-99999 CORONACH SPC  SASK |  | CA | 134.2 | 8 | 0.9501 | -32.8 | distance_gt_75km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 60595 Sand Creek Wind Farm | MT | 715160-99999 CORONACH SPC  SASK |  | CA | 126.7 | 7 | 0.9501 | -32.8 | distance_gt_75km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 3886 Wells | WA | 712150-99999 OSOYOOS CS  BC |  | CA | 124.9 | 9 | 0.9596 | -3.4 | distance_gt_75km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 56606 Culbertson Generation Station | MT | 715160-99999 CORONACH SPC  SASK |  | CA | 123.1 | 10 | 0.9501 | -32.8 | distance_gt_75km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 56833 OREG 1 Inc | MT | 715160-99999 CORONACH SPC  SASK |  | CA | 122.5 | 10 | 0.9501 | -32.8 | distance_gt_75km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 56880 OREG 2 Inc | MT | 715160-99999 CORONACH SPC  SASK |  | CA | 122.5 | 10 | 0.9501 | -32.8 | distance_gt_75km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 66684 Intermountain Pumped Storage Project | UT | 724797-23176 MILFORD MUNI BRISCOE | UT | US | 121.6 | 10 | 0.9514 | -9.9 | distance_gt_75km;selected_rank_gt_3;coverage_below_0_97;shared_station_gt_25_plants |
| 6459 Big Fork | MT | 711540-99999 WATERTON PARK GATE |  | CA | 120.9 | 5 | 0.9535 | -32.8 | distance_gt_75km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 3921 Chief Joseph | WA | 712150-99999 OSOYOOS CS  BC |  | CA | 116.4 | 7 | 0.9596 | -3.4 | distance_gt_75km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 6172 Libby | MT | 717700-99999 CRESTON CAMPBELL SCIENTIFIC  BC |  | CA | 114.7 | 7 | 0.9682 | -5.1 | distance_gt_75km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 66962 ME Novel Lighthouse - Carrabassett | ME | 716100-99999 SHERBROOKE |  | CA | 112.1 | 6 | 0.9677 | -25.6 | distance_gt_75km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 1492 Harris Hydro | ME | 713230-99999 BEAUCEVILLE  QUE |  | CA | 108.8 | 7 | 0.9538 | -24.2 | distance_gt_75km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 550 Kettle Falls Generating Station | WA | 712150-99999 OSOYOOS CS  BC |  | CA | 107.1 | 9 | 0.9596 | -3.4 | distance_gt_75km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 68371 Red Butte Solar and Storage | UT | 724797-23176 MILFORD MUNI BRISCOE | UT | US | 104.9 | 9 | 0.9514 | -9.9 | distance_gt_75km;selected_rank_gt_3;coverage_below_0_97;shared_station_gt_25_plants |
| 50650 ReEnergy Stratton LLC | ME | 716100-99999 SHERBROOKE |  | CA | 104.4 | 6 | 0.9677 | -25.6 | distance_gt_75km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 62469 Cove Mountain Solar | UT | 724797-23176 MILFORD MUNI BRISCOE | UT | US | 102.8 | 9 | 0.9514 | -9.9 | distance_gt_75km;selected_rank_gt_3;coverage_below_0_97;shared_station_gt_25_plants |
| 58598 Beryl Solar Plant | UT | 724797-23176 MILFORD MUNI BRISCOE | UT | US | 102.5 | 9 | 0.9514 | -9.9 | distance_gt_75km;selected_rank_gt_3;coverage_below_0_97;shared_station_gt_25_plants |

## Candidate Rank Outliers

| Plant | Plant State | Station | Station State | Country | Distance km | Rank | Coverage | ECWT F | Flags |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 56499 Tiber Dam Hydroelectric Plant | MT | 711160-99999 ONEFOUR CDA  ALTA |  | CA | 100.3 | 10 | 0.9630 | -28.6 | distance_gt_75km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 56606 Culbertson Generation Station | MT | 715160-99999 CORONACH SPC  SASK |  | CA | 123.1 | 10 | 0.9501 | -32.8 | distance_gt_75km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 56833 OREG 1 Inc | MT | 715160-99999 CORONACH SPC  SASK |  | CA | 122.5 | 10 | 0.9501 | -32.8 | distance_gt_75km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 56880 OREG 2 Inc | MT | 715160-99999 CORONACH SPC  SASK |  | CA | 122.5 | 10 | 0.9501 | -32.8 | distance_gt_75km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 10220 Sissonville Hydro | NY | 717120-99999 ST ANICET 1  QUE |  | CA | 74.3 | 10 | 0.9632 | -23.6 | distance_gt_50km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97;shared_station_gt_25_plants |
| 2551 Colton | NY | 717120-99999 ST ANICET 1  QUE |  | CA | 79.7 | 10 | 0.9632 | -23.6 | distance_gt_75km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97;shared_station_gt_25_plants |
| 2571 Hannawa | NY | 717120-99999 ST ANICET 1  QUE |  | CA | 77.6 | 10 | 0.9632 | -23.6 | distance_gt_75km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97;shared_station_gt_25_plants |
| 2616 Sugar Island | NY | 717120-99999 ST ANICET 1  QUE |  | CA | 76.0 | 10 | 0.9632 | -23.6 | distance_gt_75km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97;shared_station_gt_25_plants |
| 60421 Veyo Heat Recovery Project | UT | 724797-23176 MILFORD MUNI BRISCOE | UT | US | 135.8 | 10 | 0.9514 | -9.9 | distance_gt_75km;selected_rank_gt_3;coverage_below_0_97;shared_station_gt_25_plants |
| 66684 Intermountain Pumped Storage Project | UT | 724797-23176 MILFORD MUNI BRISCOE | UT | US | 121.6 | 10 | 0.9514 | -9.9 | distance_gt_75km;selected_rank_gt_3;coverage_below_0_97;shared_station_gt_25_plants |
| 59445 St. Albans SPEED Project | VT | 713720-99999 L'ACADIE  QUE |  | CA | 58.3 | 10 | 0.9597 | -21.1 | distance_gt_50km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 56605 Langdon Renewables, LLC | ND | 711480-99999 PILOT MOUND (AUT) |  | CA | 74.9 | 9 | 0.9606 | -31.0 | distance_gt_50km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 56912 Langdon Wind II LLC | ND | 711480-99999 PILOT MOUND (AUT) |  | CA | 74.9 | 9 | 0.9606 | -31.0 | distance_gt_50km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 57033 Langdon Wind Energy Center | ND | 711480-99999 PILOT MOUND (AUT) |  | CA | 74.8 | 9 | 0.9606 | -31.0 | distance_gt_50km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 57192 Spring Valley Wind Project | NV | 724797-23176 MILFORD MUNI BRISCOE | UT | US | 149.0 | 9 | 0.9514 | -9.9 | distance_gt_75km;selected_rank_gt_3;plant_station_state_mismatch;coverage_below_0_97;shared_station_gt_25_plants |
| 68017 Cooper Canyon Renewable Energy | NV | 724797-23176 MILFORD MUNI BRISCOE | UT | US | 149.5 | 9 | 0.9514 | -9.9 | distance_gt_75km;selected_rank_gt_3;plant_station_state_mismatch;coverage_below_0_97;shared_station_gt_25_plants |
| 2561 East Norfolk | NY | 717120-99999 ST ANICET 1  QUE |  | CA | 65.6 | 9 | 0.9632 | -23.6 | distance_gt_50km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97;shared_station_gt_25_plants |
| 2590 Norfolk | NY | 717120-99999 ST ANICET 1  QUE |  | CA | 66.0 | 9 | 0.9632 | -23.6 | distance_gt_50km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97;shared_station_gt_25_plants |
| 2598 Piercefield | NY | 717120-99999 ST ANICET 1  QUE |  | CA | 100.8 | 9 | 0.9632 | -23.6 | distance_gt_75km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97;shared_station_gt_25_plants |
| 2611 South Colton | NY | 717120-99999 ST ANICET 1  QUE |  | CA | 82.1 | 9 | 0.9632 | -23.6 | distance_gt_75km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97;shared_station_gt_25_plants |
| ... | 134 more rows omitted |  |  |  |  |  |  |  |  |

## Cross-Border or Non-US Station Assignments

| Plant | Plant State | Station | Station State | Country | Distance km | Rank | Coverage | ECWT F | Flags |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 54249 Smith Falls Hydro Project | ID | 717700-99999 CRESTON CAMPBELL SCIENTIFIC  BC |  | CA | 14.4 | 1 | 0.9682 | -5.1 | station_country_not_us;station_state_missing;coverage_below_0_97 |
| 6506 Moyie Springs | ID | 717700-99999 CRESTON CAMPBELL SCIENTIFIC  BC |  | CA | 45.5 | 2 | 0.9682 | -5.1 | selected_rank_gt_1;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 10555 Brassua Hydroelectric Project | ME | 713230-99999 BEAUCEVILLE  QUE |  | CA | 96.1 | 4 | 0.9538 | -24.2 | distance_gt_75km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 1492 Harris Hydro | ME | 713230-99999 BEAUCEVILLE  QUE |  | CA | 108.8 | 7 | 0.9538 | -24.2 | distance_gt_75km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 50650 ReEnergy Stratton LLC | ME | 716100-99999 SHERBROOKE |  | CA | 104.4 | 6 | 0.9677 | -25.6 | distance_gt_75km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 50999 Aziscohos Hydroelectric Project | ME | 716100-99999 SHERBROOKE |  | CA | 77.4 | 5 | 0.9677 | -25.6 | distance_gt_75km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 56829 Kibby Wind Facility | ME | 716100-99999 SHERBROOKE |  | CA | 91.1 | 3 | 0.9677 | -25.6 | distance_gt_75km;selected_rank_gt_1;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 66962 ME Novel Lighthouse - Carrabassett | ME | 716100-99999 SHERBROOKE |  | CA | 112.1 | 6 | 0.9677 | -25.6 | distance_gt_75km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 1731 Harbor Beach | MI | 712610-99999 GODERICH  ONT |  | CA | 75.0 | 8 | 0.9577 | -12.5 | distance_gt_50km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 2203 Hungry Horse | MT | 711540-99999 WATERTON PARK GATE |  | CA | 89.2 | 5 | 0.9535 | -32.8 | distance_gt_75km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 56499 Tiber Dam Hydroelectric Plant | MT | 711160-99999 ONEFOUR CDA  ALTA |  | CA | 100.3 | 10 | 0.9630 | -28.6 | distance_gt_75km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 56606 Culbertson Generation Station | MT | 715160-99999 CORONACH SPC  SASK |  | CA | 123.1 | 10 | 0.9501 | -32.8 | distance_gt_75km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 56833 OREG 1 Inc | MT | 715160-99999 CORONACH SPC  SASK |  | CA | 122.5 | 10 | 0.9501 | -32.8 | distance_gt_75km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 56880 OREG 2 Inc | MT | 715160-99999 CORONACH SPC  SASK |  | CA | 122.5 | 10 | 0.9501 | -32.8 | distance_gt_75km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 58523 Stoltze CoGen1 | MT | 711540-99999 WATERTON PARK GATE |  | CA | 88.5 | 5 | 0.9535 | -32.8 | distance_gt_75km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 60595 Sand Creek Wind Farm | MT | 715160-99999 CORONACH SPC  SASK |  | CA | 126.7 | 7 | 0.9501 | -32.8 | distance_gt_75km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 6172 Libby | MT | 717700-99999 CRESTON CAMPBELL SCIENTIFIC  BC |  | CA | 114.7 | 7 | 0.9682 | -5.1 | distance_gt_75km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 64505 Flathead Landfill to Gas Energy Facility | MT | 711540-99999 WATERTON PARK GATE |  | CA | 99.0 | 5 | 0.9535 | -32.8 | distance_gt_75km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 6459 Big Fork | MT | 711540-99999 WATERTON PARK GATE |  | CA | 120.9 | 5 | 0.9535 | -32.8 | distance_gt_75km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 6623 Fort Peck | MT | 715160-99999 CORONACH SPC  SASK |  | CA | 134.2 | 8 | 0.9501 | -32.8 | distance_gt_75km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97 |
| ... | 90 more rows omitted |  |  |  |  |  |  |  |  |

## US Plant/Station State Mismatches

| Plant | Plant State | Station | Station State | Country | Distance km | Rank | Coverage | ECWT F | Flags |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 57192 Spring Valley Wind Project | NV | 724797-23176 MILFORD MUNI BRISCOE | UT | US | 149.0 | 9 | 0.9514 | -9.9 | distance_gt_75km;selected_rank_gt_3;plant_station_state_mismatch;coverage_below_0_97;shared_station_gt_25_plants |
| 68017 Cooper Canyon Renewable Energy | NV | 724797-23176 MILFORD MUNI BRISCOE | UT | US | 149.5 | 9 | 0.9514 | -9.9 | distance_gt_75km;selected_rank_gt_3;plant_station_state_mismatch;coverage_below_0_97;shared_station_gt_25_plants |

## Selected Stations Ending Before 2010

_None._

## Warm Mainland ECWT Rows

_None._

## Near-Threshold Coverage Rows

| Plant | Plant State | Station | Station State | Country | Distance km | Rank | Coverage | ECWT F | Flags |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 56606 Culbertson Generation Station | MT | 715160-99999 CORONACH SPC  SASK |  | CA | 123.1 | 10 | 0.9501 | -32.8 | distance_gt_75km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 56833 OREG 1 Inc | MT | 715160-99999 CORONACH SPC  SASK |  | CA | 122.5 | 10 | 0.9501 | -32.8 | distance_gt_75km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 56880 OREG 2 Inc | MT | 715160-99999 CORONACH SPC  SASK |  | CA | 122.5 | 10 | 0.9501 | -32.8 | distance_gt_75km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 60595 Sand Creek Wind Farm | MT | 715160-99999 CORONACH SPC  SASK |  | CA | 126.7 | 7 | 0.9501 | -32.8 | distance_gt_75km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 6623 Fort Peck | MT | 715160-99999 CORONACH SPC  SASK |  | CA | 134.2 | 8 | 0.9501 | -32.8 | distance_gt_75km;selected_rank_gt_3;station_country_not_us;station_state_missing;coverage_below_0_97 |
| 57192 Spring Valley Wind Project | NV | 724797-23176 MILFORD MUNI BRISCOE | UT | US | 149.0 | 9 | 0.9514 | -9.9 | distance_gt_75km;selected_rank_gt_3;plant_station_state_mismatch;coverage_below_0_97;shared_station_gt_25_plants |
| 68017 Cooper Canyon Renewable Energy | NV | 724797-23176 MILFORD MUNI BRISCOE | UT | US | 149.5 | 9 | 0.9514 | -9.9 | distance_gt_75km;selected_rank_gt_3;plant_station_state_mismatch;coverage_below_0_97;shared_station_gt_25_plants |
| 299 Blundell | UT | 724797-23176 MILFORD MUNI BRISCOE | UT | US | 16.3 | 3 | 0.9514 | -9.9 | selected_rank_gt_1;coverage_below_0_97;shared_station_gt_25_plants |
| 3643 Upper Beaver | UT | 724797-23176 MILFORD MUNI BRISCOE | UT | US | 49.6 | 3 | 0.9514 | -9.9 | selected_rank_gt_1;coverage_below_0_97;shared_station_gt_25_plants |
| 57079 Milford Wind Corridor I LLC | UT | 724797-23176 MILFORD MUNI BRISCOE | UT | US | 15.0 | 3 | 0.9514 | -9.9 | selected_rank_gt_1;coverage_below_0_97;shared_station_gt_25_plants |
| 57107 Milford Wind Corridor Stage II LLC | UT | 724797-23176 MILFORD MUNI BRISCOE | UT | US | 20.1 | 3 | 0.9514 | -9.9 | selected_rank_gt_1;coverage_below_0_97;shared_station_gt_25_plants |
| 57353 Thermo No 1 | UT | 724797-23176 MILFORD MUNI BRISCOE | UT | US | 32.4 | 2 | 0.9514 | -9.9 | selected_rank_gt_1;coverage_below_0_97;shared_station_gt_25_plants |
| 58130 Blue Mountain Biogas | UT | 724797-23176 MILFORD MUNI BRISCOE | UT | US | 36.5 | 2 | 0.9514 | -9.9 | selected_rank_gt_1;coverage_below_0_97;shared_station_gt_25_plants |
| 58570 Cove Fort | UT | 724797-23176 MILFORD MUNI BRISCOE | UT | US | 41.1 | 3 | 0.9514 | -9.9 | selected_rank_gt_1;coverage_below_0_97;shared_station_gt_25_plants |
| 58598 Beryl Solar Plant | UT | 724797-23176 MILFORD MUNI BRISCOE | UT | US | 102.5 | 9 | 0.9514 | -9.9 | distance_gt_75km;selected_rank_gt_3;coverage_below_0_97;shared_station_gt_25_plants |
| 58599 Cedar Valley Solar Plant | UT | 724797-23176 MILFORD MUNI BRISCOE | UT | US | 68.0 | 4 | 0.9514 | -9.9 | distance_gt_50km;selected_rank_gt_3;coverage_below_0_97;shared_station_gt_25_plants |
| 58600 Buckhorn Solar Plant | UT | 724797-23176 MILFORD MUNI BRISCOE | UT | US | 50.4 | 3 | 0.9514 | -9.9 | distance_gt_50km;selected_rank_gt_1;coverage_below_0_97;shared_station_gt_25_plants |
| 58601 Milford Flat Solar Plant | UT | 724797-23176 MILFORD MUNI BRISCOE | UT | US | 14.0 | 2 | 0.9514 | -9.9 | selected_rank_gt_1;coverage_below_0_97;shared_station_gt_25_plants |
| 58602 Laho Solar Plant | UT | 724797-23176 MILFORD MUNI BRISCOE | UT | US | 14.1 | 2 | 0.9514 | -9.9 | selected_rank_gt_1;coverage_below_0_97;shared_station_gt_25_plants |
| 58603 Greenville Solar Plant | UT | 724797-23176 MILFORD MUNI BRISCOE | UT | US | 30.4 | 3 | 0.9514 | -9.9 | selected_rank_gt_1;coverage_below_0_97;shared_station_gt_25_plants |
| ... | 133 more rows omitted |  |  |  |  |  |  |  |  |

## Method Notes

- This script does not write to the database.
- Selected station IDs come from `calc.plant_ecwt_readiness.selected_station_id` and are cross-checked against `link.station_selection_segment`.
- Candidate rank, distance, elevation delta, and candidate coverage come from `link.station_candidate` for the candidate run embedded in the plant ECWT run parameters.
- Station metadata comes from `weather.station`, and plant metadata comes from `asset.plant`.
- Shared station counts are computed only across the strict publication-candidate cohort in this QA run.

## Recommended Next Steps

1. Review all rows with distance, cross-border/state, old-station, or warm-mainland flags before marking any ECWT output as compliance-ready.
2. Decide whether to encode review dispositions in a database table, likely a new audited station-selection review table rather than editing provisional algorithmic rows.
3. After review policy is defined, rebuild a release-candidate export that includes both ECWT values and station-selection review status.
