# Station Selection QA for Strict Plant ECWT Candidates

## Technical Summary

This read-only QA pass reviewed `1,964` strict plant ECWT publication candidates from readiness run `plant_ecwt_readiness_20260625T005939Z`. The script found `1,614` rows with at least one review flag. Flags are not rejection decisions; they identify selected plant-to-station assignments that should be reviewed before any compliance-facing release.

The strict candidates use `421` distinct selected NOAA stations. The maximum selected station distance is `84.6` km, and the largest single-station concentration is `49` strict candidate plants.

## Scope and Source Runs

- QA run: `station_selection_qa_20260625T011125Z`
- Generated at UTC: `2026-06-25T01:11:25+00:00`
- Code commit: `55409b40f5fc1964f8f1b60e6b6381b856654a30`
- Readiness run: `plant_ecwt_readiness_20260625T005939Z`
- Plant ECWT run: `plant_ecwt_provisional_20260625T005854Z`
- Strict readiness threshold: `2000` valid hours and coverage ratio >= `0.95`
- Coverage denominator: `fixed selected-station active-period DJF hours`
- Detailed CSV: `station_selection_qa_20260625T011125Z.csv`

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
| Strict publication candidates reviewed | 1,964 |
| Distinct selected stations | 421 |
| Rows with at least one QA flag | 1,614 |
| Selected station assignments with rank > 1 | 16 |
| Non-US selected stations | 27 |
| US plant/station state mismatches | 149 |
| Selected stations with last observation before 2010 | 1,224 |
| Mainland warm ECWT rows > 32 F | 55 |
| Near-threshold coverage rows below 0.97 | 551 |

## Risk Flag Counts

| Flag | Rows | Share |
| --- | --- | --- |
| station_last_observation_before_2010 | 1,224 | 62.3% |
| coverage_below_0_97 | 551 | 28.1% |
| shared_station_gt_10_plants | 538 | 27.4% |
| plant_station_state_mismatch | 149 | 7.6% |
| shared_station_gt_25_plants | 108 | 5.5% |
| distance_gt_50km | 73 | 3.7% |
| warm_mainland_ecwt_gt_32f | 55 | 2.8% |
| warm_ecwt_gt_35f | 51 | 2.6% |
| station_state_missing | 35 | 1.8% |
| station_country_not_us | 27 | 1.4% |
| selected_rank_gt_1 | 16 | 0.8% |
| distance_gt_75km | 10 | 0.5% |

## Top Selected Stations by Plant Count

| Station | State | Country | Strict Candidate Plants | Max Distance km | Min Coverage | ECWT F |
| --- | --- | --- | --- | --- | --- | --- |
| 726418-99999 L O SIMENSTAD MUNI | WI | US | 49 | 23.6 | 0.9702 | -20.2 |
| 720644-99999 BUCKEYE MUNI | AZ | US | 32 | 84.6 | 0.9900 | 28.4 |
| 724095-99999 TRENTON MERCER | NJ | US | 27 | 29.5 | 0.9749 | 8.6 |
| 725107-99999 FITCHBURG MUNI | MA | US | 23 | 19.7 | 0.9716 | -2.6 |
| 720972-99999 ST MARY HOSPITAL HELIPORT | MN | US | 22 | 33.6 | 0.9826 | -16.6 |
| 722126-99999 LANSING MUNI | IL | US | 21 | 26.2 | 1.0014 | -0.4 |
| 999999-94644 OLD TOWN 2 W | ME | US | 20 | 44.0 | 0.9558 | -17.6 |
| 740001-99999 SUSSEX | NJ | US | 19 | 26.9 | 0.9684 | -9.4 |
| 723820-99999 PALMDALE PRODUCTION | CA | US | 19 | 16.3 | 0.9836 | 21.2 |
| 999999-03047 MONAHANS 6 ENE | TX | US | 18 | 73.5 | 0.9509 | 11.8 |
| 710366-99999 COVEY HILL |  | CA | 18 | 38.0 | 0.9869 | -18.4 |
| 723079-99999 TRI CO | NC | US | 18 | 29.7 | 0.9765 | 12.2 |
| 722527-99999 BRAZORIA CO | TX | US | 18 | 25.7 | 0.9623 | 26.6 |
| 723109-99999 MAXTON | NC | US | 18 | 17.8 | 0.9732 | 15.8 |
| 720271-99999 BIG SPRING MCMAHON | TX | US | 17 | 67.5 | 1.0014 | 13.6 |
| 725060-14704 OTIS ANGB AIRPORT | MA | US | 17 | 17.2 | 0.9792 | 10.4 |
| 999999-92827 SEBRING 23 SSE | FL | US | 16 | 73.7 | 0.9976 | 27.9 |
| 726837-99999 ONTARIA MUNI | OR | US | 16 | 49.8 | 0.9605 | 12.2 |
| 744915-99999 BARNES MUNI | MA | US | 16 | 29.2 | 0.9672 | -7.6 |
| 999999-03072 BRONTE 11 NNE | TX | US | 15 | 57.8 | 0.9958 | 10.0 |
| ... | 401 more rows omitted |  |  |  |  |  |

## Farthest Selected Station Assignments

| Plant | Plant State | Station | Station State | Country | Distance km | Rank | Coverage | ECWT F | Flags |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 68321 Atlas BESS IV LLC | AZ | 720644-99999 BUCKEYE MUNI | AZ | US | 84.6 | 1 | 0.9900 | 28.4 | distance_gt_75km;shared_station_gt_25_plants |
| 68322 Atlas VII | AZ | 720644-99999 BUCKEYE MUNI | AZ | US | 84.6 | 1 | 0.9900 | 28.4 | distance_gt_75km;shared_station_gt_25_plants |
| 68323 Atlas VIII | AZ | 720644-99999 BUCKEYE MUNI | AZ | US | 84.6 | 1 | 0.9900 | 28.4 | distance_gt_75km;shared_station_gt_25_plants |
| 68324 Atlas IX | AZ | 720644-99999 BUCKEYE MUNI | AZ | US | 84.6 | 1 | 0.9900 | 28.4 | distance_gt_75km;shared_station_gt_25_plants |
| 69054 ATLAS II | AZ | 720644-99999 BUCKEYE MUNI | AZ | US | 84.6 | 1 | 0.9900 | 28.4 | distance_gt_75km;shared_station_gt_25_plants |
| 69055 ATLAS SOLAR IV | AZ | 720644-99999 BUCKEYE MUNI | AZ | US | 84.6 | 1 | 0.9900 | 28.4 | distance_gt_75km;shared_station_gt_25_plants |
| 3020 Clearwater 1 | OR | 726904-99999 ROSEBURG RGNL | OR | US | 82.0 | 1 | 0.9679 | 28.4 | distance_gt_75km;coverage_below_0_97;station_last_observation_before_2010 |
| 68466 Centennial Flats | AZ | 720644-99999 BUCKEYE MUNI | AZ | US | 80.3 | 1 | 0.9900 | 28.4 | distance_gt_75km;shared_station_gt_25_plants |
| 6421 Lemolo 2 | OR | 726904-99999 ROSEBURG RGNL | OR | US | 76.9 | 1 | 0.9679 | 28.4 | distance_gt_75km;coverage_below_0_97;station_last_observation_before_2010 |
| 3021 Clearwater 2 | OR | 726904-99999 ROSEBURG RGNL | OR | US | 76.2 | 1 | 0.9679 | 28.4 | distance_gt_75km;coverage_below_0_97;station_last_observation_before_2010 |
| 58997 SRF Pulp Processing Facility | FL | 999999-92827 SEBRING 23 SSE | FL | US | 73.7 | 2 | 0.9976 | 27.9 | distance_gt_50km;selected_rank_gt_1;shared_station_gt_10_plants |
| 62561 Roadrunner, LLC Hybrid | TX | 999999-03047 MONAHANS 6 ENE | TX | US | 73.5 | 1 | 0.9509 | 11.8 | distance_gt_50km;coverage_below_0_97;shared_station_gt_10_plants |
| 3040 Toketee Falls | OR | 726904-99999 ROSEBURG RGNL | OR | US | 73.2 | 1 | 0.9679 | 28.4 | distance_gt_50km;coverage_below_0_97;station_last_observation_before_2010 |
| 3026 Fish Creek | OR | 726904-99999 ROSEBURG RGNL | OR | US | 73.1 | 1 | 0.9679 | 28.4 | distance_gt_50km;coverage_below_0_97;station_last_observation_before_2010 |
| 3036 Slide Creek | OR | 726904-99999 ROSEBURG RGNL | OR | US | 71.4 | 1 | 0.9679 | 28.4 | distance_gt_50km;coverage_below_0_97;station_last_observation_before_2010 |
| 55581 King Mountain Wind Ranch 1 | TX | 999999-03047 MONAHANS 6 ENE | TX | US | 70.6 | 1 | 0.9509 | 11.8 | distance_gt_50km;coverage_below_0_97;shared_station_gt_10_plants |
| 58131 Outback Solar At Christmas Valley | OR | 999999-04128 RILEY 10 WSW | OR | US | 69.6 | 1 | 0.9542 | -9.9 | distance_gt_50km;coverage_below_0_97 |
| 3037 Soda Springs | OR | 726904-99999 ROSEBURG RGNL | OR | US | 69.2 | 1 | 0.9679 | 28.4 | distance_gt_50km;coverage_below_0_97;station_last_observation_before_2010 |
| 63349 OE_AZ1 | AZ | 999999-53172 LAKE HAVASU CITY 19 SE | AZ | US | 68.9 | 1 | 1.0000 | 30.7 | distance_gt_50km |
| 66637 McFarland B Solar and Storage | AZ | 999999-53154 YUMA 27 ENE | AZ | US | 67.9 | 1 | 0.9989 | 30.7 | distance_gt_50km |

## Candidate Rank Outliers

| Plant | Plant State | Station | Station State | Country | Distance km | Rank | Coverage | ECWT F | Flags |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 56676 Margarita Energy Center | CA | 722977-99999 JOHN WAYNE ARPT ORA | CA | US | 25.7 | 3 | 0.9845 | 39.2 | selected_rank_gt_1;station_last_observation_before_2010;warm_ecwt_gt_35f;warm_mainland_ecwt_gt_32f;shared_station_gt_10_plants |
| 62515 Hybrid Holdings 1 Capistrano | CA | 722977-99999 JOHN WAYNE ARPT ORA | CA | US | 25.7 | 3 | 0.9845 | 39.2 | selected_rank_gt_1;station_last_observation_before_2010;warm_ecwt_gt_35f;warm_mainland_ecwt_gt_32f;shared_station_gt_10_plants |
| 6637 Yakutat | AK | 999999-25382 YAKUTAT 3 SSE | AK | US | 4.5 | 2 | 0.9990 | -0.6 | selected_rank_gt_1 |
| 61721 Baldwin (CA) | CA | 722977-99999 JOHN WAYNE ARPT ORA | CA | US | 20.4 | 2 | 0.9845 | 39.2 | selected_rank_gt_1;station_last_observation_before_2010;warm_ecwt_gt_35f;warm_mainland_ecwt_gt_32f;shared_station_gt_10_plants |
| 61723 HEBT Irvine 2 | CA | 722977-99999 JOHN WAYNE ARPT ORA | CA | US | 9.1 | 2 | 0.9845 | 39.2 | selected_rank_gt_1;station_last_observation_before_2010;warm_ecwt_gt_35f;warm_mainland_ecwt_gt_32f;shared_station_gt_10_plants |
| 63610 Baker | CA | 722977-99999 JOHN WAYNE ARPT ORA | CA | US | 17.0 | 2 | 0.9845 | 39.2 | selected_rank_gt_1;station_last_observation_before_2010;warm_ecwt_gt_35f;warm_mainland_ecwt_gt_32f;shared_station_gt_10_plants |
| 63614 LAWRP | CA | 722977-99999 JOHN WAYNE ARPT ORA | CA | US | 14.6 | 2 | 0.9845 | 39.2 | selected_rank_gt_1;station_last_observation_before_2010;warm_ecwt_gt_35f;warm_mainland_ecwt_gt_32f;shared_station_gt_10_plants |
| 58997 SRF Pulp Processing Facility | FL | 999999-92827 SEBRING 23 SSE | FL | US | 73.7 | 2 | 0.9976 | 27.9 | distance_gt_50km;selected_rank_gt_1;shared_station_gt_10_plants |
| 62631 Blue Heron Solar | FL | 999999-92827 SEBRING 23 SSE | FL | US | 55.5 | 2 | 0.9976 | 27.9 | distance_gt_50km;selected_rank_gt_1;shared_station_gt_10_plants |
| 65871 Caloosahatchee | FL | 999999-92827 SEBRING 23 SSE | FL | US | 47.9 | 2 | 0.9976 | 27.9 | selected_rank_gt_1;shared_station_gt_10_plants |
| 65909 Hendry Isles | FL | 999999-92827 SEBRING 23 SSE | FL | US | 48.2 | 2 | 0.9976 | 27.9 | selected_rank_gt_1;shared_station_gt_10_plants |
| 68276 Swamp Cabbage | FL | 999999-92827 SEBRING 23 SSE | FL | US | 45.0 | 2 | 0.9976 | 27.9 | selected_rank_gt_1;shared_station_gt_10_plants |
| 68831 Cocoplum | FL | 999999-92827 SEBRING 23 SSE | FL | US | 46.9 | 2 | 0.9976 | 27.9 | selected_rank_gt_1;shared_station_gt_10_plants |
| 52028 Puna Geothermal Venture I | HI | 999999-21515 HILO 5 S | HI | US | 27.5 | 2 | 0.9991 | 55.9 | selected_rank_gt_1;warm_ecwt_gt_35f |
| 3408 Melton Hill | TN | 723246-53868 OAK RIDGE | TN | US | 16.4 | 2 | 0.9908 | 10.9 | selected_rank_gt_1 |
| 64669 Notch Peak Solar LLC | UT | 999999-53165 DELTA 4 NE | UT | US | 19.6 | 2 | 1.0000 | -15.5 | selected_rank_gt_1 |

## Cross-Border or Non-US Station Assignments

| Plant | Plant State | Station | Station State | Country | Distance km | Rank | Coverage | ECWT F | Flags |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 54249 Smith Falls Hydro Project | ID | 717700-99999 CRESTON CAMPBELL SCIENTIFIC  BC |  | CA | 14.4 | 1 | 0.9812 | -5.1 | station_country_not_us;station_state_missing |
| 2550 Chasm | NY | 710366-99999 COVEY HILL |  | CA | 38.0 | 1 | 0.9869 | -18.4 | station_country_not_us;station_state_missing;station_last_observation_before_2010;shared_station_gt_10_plants |
| 2583 Macomb | NY | 717120-99999 ST ANICET 1  QUE |  | CA | 26.7 | 1 | 0.9761 | -23.6 | station_country_not_us;station_state_missing |
| 50093 Chateaugay High Falls Hydro | NY | 710366-99999 COVEY HILL |  | CA | 18.8 | 1 | 0.9869 | -18.4 | station_country_not_us;station_state_missing;station_last_observation_before_2010;shared_station_gt_10_plants |
| 50315 Chasm Hydro Partnership | NY | 710366-99999 COVEY HILL |  | CA | 19.6 | 1 | 0.9869 | -18.4 | station_country_not_us;station_state_missing;station_last_observation_before_2010;shared_station_gt_10_plants |
| 56618 Clinton | NY | 710366-99999 COVEY HILL |  | CA | 15.5 | 1 | 0.9869 | -18.4 | station_country_not_us;station_state_missing;station_last_observation_before_2010;shared_station_gt_10_plants |
| 56619 Ellenburg | NY | 710366-99999 COVEY HILL |  | CA | 15.5 | 1 | 0.9869 | -18.4 | station_country_not_us;station_state_missing;station_last_observation_before_2010;shared_station_gt_10_plants |
| 56857 Marble River Wind Farm | NY | 710366-99999 COVEY HILL |  | CA | 4.6 | 1 | 0.9869 | -18.4 | station_country_not_us;station_state_missing;station_last_observation_before_2010;shared_station_gt_10_plants |
| 56904 Chateaugay | NY | 710366-99999 COVEY HILL |  | CA | 16.7 | 1 | 0.9869 | -18.4 | station_country_not_us;station_state_missing;station_last_observation_before_2010;shared_station_gt_10_plants |
| 59629 Jericho Rise Wind Farm LLC | NY | 710366-99999 COVEY HILL |  | CA | 21.3 | 1 | 0.9869 | -18.4 | station_country_not_us;station_state_missing;station_last_observation_before_2010;shared_station_gt_10_plants |
| 62507 County Route 11 Community Solar Farm | NY | 710366-99999 COVEY HILL |  | CA | 17.7 | 1 | 0.9869 | -18.4 | station_country_not_us;station_state_missing;station_last_observation_before_2010;shared_station_gt_10_plants |
| 62530 Boas Rd #1 Community Solar Farm | NY | 710366-99999 COVEY HILL |  | CA | 18.1 | 1 | 0.9869 | -18.4 | station_country_not_us;station_state_missing;station_last_observation_before_2010;shared_station_gt_10_plants |
| 62531 Boas Rd #2 Community Solar Farm | NY | 710366-99999 COVEY HILL |  | CA | 18.2 | 1 | 0.9869 | -18.4 | station_country_not_us;station_state_missing;station_last_observation_before_2010;shared_station_gt_10_plants |
| 62532 Boas Rd #3 Community Solar Farm | NY | 710366-99999 COVEY HILL |  | CA | 18.4 | 1 | 0.9869 | -18.4 | station_country_not_us;station_state_missing;station_last_observation_before_2010;shared_station_gt_10_plants |
| 62533 Boas Rd #4 Community Solar Farm | NY | 710366-99999 COVEY HILL |  | CA | 18.8 | 1 | 0.9869 | -18.4 | station_country_not_us;station_state_missing;station_last_observation_before_2010;shared_station_gt_10_plants |
| 62784 Franklin Solar Site | NY | 717120-99999 ST ANICET 1  QUE |  | CA | 27.7 | 1 | 0.9761 | -23.6 | station_country_not_us;station_state_missing |
| 62785 Malone Solar Site | NY | 717120-99999 ST ANICET 1  QUE |  | CA | 27.4 | 1 | 0.9761 | -23.6 | station_country_not_us;station_state_missing |
| 63238 Willis Battery Storage | NY | 710366-99999 COVEY HILL |  | CA | 22.3 | 1 | 0.9869 | -18.4 | station_country_not_us;station_state_missing;station_last_observation_before_2010;shared_station_gt_10_plants |
| 63772 Adirondack Solar | NY | 710366-99999 COVEY HILL |  | CA | 12.3 | 1 | 0.9869 | -18.4 | station_country_not_us;station_state_missing;station_last_observation_before_2010;shared_station_gt_10_plants |
| 65379 OYA State Route 122 | NY | 717120-99999 ST ANICET 1  QUE |  | CA | 21.7 | 1 | 0.9761 | -23.6 | station_country_not_us;station_state_missing |
| ... | 7 more rows omitted |  |  |  |  |  |  |  |  |

## US Plant/Station State Mismatches

| Plant | Plant State | Station | Station State | Country | Distance km | Rank | Coverage | ECWT F | Flags |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 6001 Joseph M Farley | AL | 720257-99999 EARLY CO | GA | US | 28.1 | 1 | 1.0017 | 26.2 | plant_station_state_mismatch;station_last_observation_before_2010 |
| 10606 Georgia-Pacific Crossett LLC | AR | 999999-53961 MONROE 26 N | LA | US | 31.7 | 1 | 0.9502 | 14.9 | plant_station_state_mismatch;coverage_below_0_97 |
| 193 Municipal Light | AR | 720331-99999 KENNETT MEM | MO | US | 22.3 | 1 | 0.9803 | 6.8 | plant_station_state_mismatch |
| 67515 Crossett SD | AR | 999999-53961 MONROE 26 N | LA | US | 32.1 | 1 | 0.9502 | 14.9 | plant_station_state_mismatch;coverage_below_0_97 |
| 67915 Crossett Solar | AR | 999999-53961 MONROE 26 N | LA | US | 28.5 | 1 | 0.9502 | 14.9 | plant_station_state_mismatch;coverage_below_0_97 |
| 68937 Roadrunner Reserve Phase 2 | AZ | 999999-03072 BRONTE 11 NNE | TX | US | 53.9 | 1 | 0.9958 | 10.0 | distance_gt_50km;plant_station_state_mismatch;shared_station_gt_10_plants |
| 447 Parker Dam | CA | 999999-53172 LAKE HAVASU CITY 19 SE | AZ | US | 4.7 | 1 | 1.0000 | 30.7 | plant_station_state_mismatch |
| 68907 Vidal Energy Center | CA | 999999-53172 LAKE HAVASU CITY 19 SE | AZ | US | 36.2 | 1 | 1.0000 | 30.7 | plant_station_state_mismatch |
| 541 Bulls Bridge | CT | 999999-64756 MILLBROOK 3 W | NY | US | 25.1 | 1 | 0.9993 | -8.0 | plant_station_state_mismatch;shared_station_gt_10_plants |
| 560 Falls Village | CT | 999999-64756 MILLBROOK 3 W | NY | US | 36.3 | 1 | 0.9993 | -8.0 | plant_station_state_mismatch;shared_station_gt_10_plants |
| 63262 Becton Canaan | CT | 999999-64756 MILLBROOK 3 W | NY | US | 41.9 | 1 | 0.9993 | -8.0 | plant_station_state_mismatch;shared_station_gt_10_plants |
| 67478 Sand Road | CT | 999999-64756 MILLBROOK 3 W | NY | US | 43.5 | 1 | 0.9993 | -8.0 | plant_station_state_mismatch;shared_station_gt_10_plants |
| 67506 Bunce | CT | 999999-64756 MILLBROOK 3 W | NY | US | 43.9 | 1 | 0.9993 | -8.0 | plant_station_state_mismatch;shared_station_gt_10_plants |
| 50473 Suwannee River Chemical Complex | FL | 722166-99999 VALDOSTA RGNL | GA | US | 59.6 | 1 | 0.9536 | 21.2 | distance_gt_50km;plant_station_state_mismatch;coverage_below_0_97;station_last_observation_before_2010 |
| 65424 First City Solar Energy Center | FL | 999999-63899 BREWTON 3 NNE | AL | US | 37.1 | 1 | 0.9977 | 18.8 | plant_station_state_mismatch |
| 65911 Mitchell Creek | FL | 999999-63899 BREWTON 3 NNE | AL | US | 31.4 | 1 | 0.9977 | 18.8 | plant_station_state_mismatch |
| 68627 Chattooga Gore | GA | 999999-63862 VALLEY HEAD 1 SSW | AL | US | 17.0 | 1 | 0.9905 | 7.6 | plant_station_state_mismatch |
| 1047 Lansing | IA | 720663-99999 VIROQUA MUNI | WI | US | 34.0 | 1 | 0.9833 | -10.6 | plant_station_state_mismatch |
| 1082 Walter Scott Jr Energy Center | IA | 725540-99999 OFFUTT AFB | NE | US | 8.6 | 1 | 0.9701 | -5.8 | plant_station_state_mismatch;station_last_observation_before_2010 |
| 66330 Weiser BESS | ID | 726837-99999 ONTARIA MUNI | OR | US | 25.8 | 1 | 0.9605 | 12.2 | plant_station_state_mismatch;coverage_below_0_97;station_last_observation_before_2010;shared_station_gt_10_plants |
| ... | 129 more rows omitted |  |  |  |  |  |  |  |  |

## Selected Stations Ending Before 2010

| Plant | Plant State | Station | Station State | Country | Last Obs | Coverage | ECWT F | Flags |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 50234 San Antonio Regional Hospital | CA | 722865-99999 ONTARIO | CA | US | 2001-05-15 | 0.9878 | 37.4 | station_last_observation_before_2010;warm_ecwt_gt_35f;warm_mainland_ecwt_gt_32f |
| 60371 Legoland Solar | FL | 722017-99999 WINTER HAVEN | FL | US | 2001-05-15 | 0.9572 | 30.2 | coverage_below_0_97;station_last_observation_before_2010 |
| 66128 Lake Mabel Solar and Battery Storage | FL | 722017-99999 WINTER HAVEN | FL | US | 2001-05-15 | 0.9572 | 30.2 | coverage_below_0_97;station_last_observation_before_2010 |
| 56097 New Mexico Wind Energy Center | NM | 722018-99999 CLOVIS(NEXRAD) | NM | US | 2001-05-15 | 0.9536 | 21.2 | coverage_below_0_97;station_last_observation_before_2010 |
| 61925 Casa Mesa Wind Energy Center Hybrid | NM | 722018-99999 CLOVIS(NEXRAD) | NM | US | 2001-05-15 | 0.9536 | 21.2 | coverage_below_0_97;station_last_observation_before_2010 |
| 7182 Aniak | AK | 702320-99999 ANIAK | AK | US | 2003-12-30 | 0.9568 | -43.6 | coverage_below_0_97;station_last_observation_before_2010 |
| 7721 Theodore Cogen Facility | AL | 722235-99999 MOBILE DOWNTOWN | AL | US | 2003-12-30 | 0.9623 | 23.0 | coverage_below_0_97;station_last_observation_before_2010 |
| 56489 Elkins Generating Center | AR | 723445-99999 DRAKE FLD | AR | US | 2003-12-30 | 0.9787 | 6.8 | station_last_observation_before_2010 |
| 66590 C&L | AR | 723417-99999 GRIDER FLD | AR | US | 2003-12-30 | 0.9720 | 14.0 | station_last_observation_before_2010 |
| 67513 ADC Varner | AR | 723417-99999 GRIDER FLD | AR | US | 2003-12-30 | 0.9720 | 14.0 | station_last_observation_before_2010 |
| 67518 Fayetteville Public Schools (Ozarks) | AR | 723445-99999 DRAKE FLD | AR | US | 2003-12-30 | 0.9787 | 6.8 | station_last_observation_before_2010 |
| 68710 Ozark Solar Park | AR | 723445-99999 DRAKE FLD | AR | US | 2003-12-30 | 0.9787 | 6.8 | station_last_observation_before_2010 |
| 68722 Star City School District | AR | 723417-99999 GRIDER FLD | AR | US | 2003-12-30 | 0.9720 | 14.0 | station_last_observation_before_2010 |
| 66925 SR McNeal | AZ | 722720-99999 BISBEE DOUGLAS INTL | AZ | US | 2003-12-30 | 0.9760 | 13.8 | station_last_observation_before_2010 |
| 335 AES Huntington Beach LLC | CA | 722977-99999 JOHN WAYNE ARPT ORA | CA | US | 2003-12-30 | 0.9845 | 39.2 | station_last_observation_before_2010;warm_ecwt_gt_35f;warm_mainland_ecwt_gt_32f;shared_station_gt_10_plants |
| 375 Magnolia | CA | 722880-99999 BURBANK/GLENDALE | CA | US | 2003-12-30 | 0.9852 | 35.6 | station_last_observation_before_2010;warm_ecwt_gt_35f;warm_mainland_ecwt_gt_32f |
| 377 Grayson | CA | 722880-99999 BURBANK/GLENDALE | CA | US | 2003-12-30 | 0.9852 | 35.6 | station_last_observation_before_2010;warm_ecwt_gt_35f;warm_mainland_ecwt_gt_32f |
| 52099 Plant No 2 Orange County | CA | 722977-99999 JOHN WAYNE ARPT ORA | CA | US | 2003-12-30 | 0.9845 | 39.2 | station_last_observation_before_2010;warm_ecwt_gt_35f;warm_mainland_ecwt_gt_32f;shared_station_gt_10_plants |
| 54327 Toyon Power Station | CA | 722880-99999 BURBANK/GLENDALE | CA | US | 2003-12-30 | 0.9852 | 35.6 | station_last_observation_before_2010;warm_ecwt_gt_35f;warm_mainland_ecwt_gt_32f |
| 56046 Magnolia Power Project | CA | 722880-99999 BURBANK/GLENDALE | CA | US | 2003-12-30 | 0.9852 | 35.6 | station_last_observation_before_2010;warm_ecwt_gt_35f;warm_mainland_ecwt_gt_32f |
| ... | 1204 more rows omitted |  |  |  |  |  |  |  |

## Warm Mainland ECWT Rows

| Plant | Plant State | Station | Station State | Country | Distance km | Rank | Coverage | ECWT F | Flags |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 335 AES Huntington Beach LLC | CA | 722977-99999 JOHN WAYNE ARPT ORA | CA | US | 10.7 | 1 | 0.9845 | 39.2 | station_last_observation_before_2010;warm_ecwt_gt_35f;warm_mainland_ecwt_gt_32f;shared_station_gt_10_plants |
| 52099 Plant No 2 Orange County | CA | 722977-99999 JOHN WAYNE ARPT ORA | CA | US | 8.6 | 1 | 0.9845 | 39.2 | station_last_observation_before_2010;warm_ecwt_gt_35f;warm_mainland_ecwt_gt_32f;shared_station_gt_10_plants |
| 56676 Margarita Energy Center | CA | 722977-99999 JOHN WAYNE ARPT ORA | CA | US | 25.7 | 3 | 0.9845 | 39.2 | selected_rank_gt_1;station_last_observation_before_2010;warm_ecwt_gt_35f;warm_mainland_ecwt_gt_32f;shared_station_gt_10_plants |
| 57122 UCI Facilities Management Central Plant | CA | 722977-99999 JOHN WAYNE ARPT ORA | CA | US | 2.8 | 1 | 0.9845 | 39.2 | station_last_observation_before_2010;warm_ecwt_gt_35f;warm_mainland_ecwt_gt_32f;shared_station_gt_10_plants |
| 58223 Hoag Hospital Cogen Plant | CA | 722977-99999 JOHN WAYNE ARPT ORA | CA | US | 8.1 | 1 | 0.9845 | 39.2 | station_last_observation_before_2010;warm_ecwt_gt_35f;warm_mainland_ecwt_gt_32f;shared_station_gt_10_plants |
| 61721 Baldwin (CA) | CA | 722977-99999 JOHN WAYNE ARPT ORA | CA | US | 20.4 | 2 | 0.9845 | 39.2 | selected_rank_gt_1;station_last_observation_before_2010;warm_ecwt_gt_35f;warm_mainland_ecwt_gt_32f;shared_station_gt_10_plants |
| 61723 HEBT Irvine 2 | CA | 722977-99999 JOHN WAYNE ARPT ORA | CA | US | 9.1 | 2 | 0.9845 | 39.2 | selected_rank_gt_1;station_last_observation_before_2010;warm_ecwt_gt_35f;warm_mainland_ecwt_gt_32f;shared_station_gt_10_plants |
| 62116 AES Huntington Beach Energy Project | CA | 722977-99999 JOHN WAYNE ARPT ORA | CA | US | 10.7 | 1 | 0.9845 | 39.2 | station_last_observation_before_2010;warm_ecwt_gt_35f;warm_mainland_ecwt_gt_32f;shared_station_gt_10_plants |
| 62515 Hybrid Holdings 1 Capistrano | CA | 722977-99999 JOHN WAYNE ARPT ORA | CA | US | 25.7 | 3 | 0.9845 | 39.2 | selected_rank_gt_1;station_last_observation_before_2010;warm_ecwt_gt_35f;warm_mainland_ecwt_gt_32f;shared_station_gt_10_plants |
| 63609 Allergan | CA | 722977-99999 JOHN WAYNE ARPT ORA | CA | US | 1.4 | 1 | 0.9845 | 39.2 | station_last_observation_before_2010;warm_ecwt_gt_35f;warm_mainland_ecwt_gt_32f;shared_station_gt_10_plants |
| 63610 Baker | CA | 722977-99999 JOHN WAYNE ARPT ORA | CA | US | 17.0 | 2 | 0.9845 | 39.2 | selected_rank_gt_1;station_last_observation_before_2010;warm_ecwt_gt_35f;warm_mainland_ecwt_gt_32f;shared_station_gt_10_plants |
| 63614 LAWRP | CA | 722977-99999 JOHN WAYNE ARPT ORA | CA | US | 14.6 | 2 | 0.9845 | 39.2 | selected_rank_gt_1;station_last_observation_before_2010;warm_ecwt_gt_35f;warm_mainland_ecwt_gt_32f;shared_station_gt_10_plants |
| 65614 Orange Coast College PH2 Solar Project | CA | 722977-99999 JOHN WAYNE ARPT ORA | CA | US | 4.3 | 1 | 0.9845 | 39.2 | station_last_observation_before_2010;warm_ecwt_gt_35f;warm_mainland_ecwt_gt_32f;shared_station_gt_10_plants |
| 50234 San Antonio Regional Hospital | CA | 722865-99999 ONTARIO | CA | US | 4.0 | 1 | 0.9878 | 37.4 | station_last_observation_before_2010;warm_ecwt_gt_35f;warm_mainland_ecwt_gt_32f |
| 484 Red Mountain | CA | 999999-53151 FALLBROOK 5 NE | CA | US | 5.0 | 1 | 0.9979 | 35.9 | warm_ecwt_gt_35f;warm_mainland_ecwt_gt_32f |
| 56914 Orange Grove Peaking Facility | CA | 999999-53151 FALLBROOK 5 NE | CA | US | 11.5 | 1 | 0.9979 | 35.9 | warm_ecwt_gt_35f;warm_mainland_ecwt_gt_32f |
| 60426 RCWD PV Project | CA | 999999-53151 FALLBROOK 5 NE | CA | US | 9.3 | 1 | 0.9979 | 35.9 | warm_ecwt_gt_35f;warm_mainland_ecwt_gt_32f |
| 60516 NLP Granger | CA | 999999-53151 FALLBROOK 5 NE | CA | US | 22.4 | 1 | 0.9979 | 35.9 | warm_ecwt_gt_35f;warm_mainland_ecwt_gt_32f |
| 60566 Pala Energy Storage Yard | CA | 999999-53151 FALLBROOK 5 NE | CA | US | 11.6 | 1 | 0.9979 | 35.9 | warm_ecwt_gt_35f;warm_mainland_ecwt_gt_32f |
| 61365 Fallbrook Energy Storage | CA | 999999-53151 FALLBROOK 5 NE | CA | US | 7.4 | 1 | 0.9979 | 35.9 | warm_ecwt_gt_35f;warm_mainland_ecwt_gt_32f |
| ... | 35 more rows omitted |  |  |  |  |  |  |  |  |

## Near-Threshold Coverage Rows

| Plant | Plant State | Station | Station State | Country | Distance km | Rank | Coverage | ECWT F | Flags |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 10606 Georgia-Pacific Crossett LLC | AR | 999999-53961 MONROE 26 N | LA | US | 31.7 | 1 | 0.9502 | 14.9 | plant_station_state_mismatch;coverage_below_0_97 |
| 67515 Crossett SD | AR | 999999-53961 MONROE 26 N | LA | US | 32.1 | 1 | 0.9502 | 14.9 | plant_station_state_mismatch;coverage_below_0_97 |
| 67915 Crossett Solar | AR | 999999-53961 MONROE 26 N | LA | US | 28.5 | 1 | 0.9502 | 14.9 | plant_station_state_mismatch;coverage_below_0_97 |
| 52048 Vanderbilt University Power Plant | TN | 723271-99999 JOHN C TUNE | TN | US | 8.5 | 1 | 0.9504 | 5.0 | coverage_below_0_97 |
| 62468 Music City Community Solar | TN | 723271-99999 JOHN C TUNE | TN | US | 14.6 | 1 | 0.9504 | 5.0 | coverage_below_0_97 |
| 6418 Cheatham | TN | 723271-99999 JOHN C TUNE | TN | US | 33.8 | 1 | 0.9504 | 5.0 | coverage_below_0_97 |
| 10121 High Shoals Hydro (GA) | GA | 999999-63850 WATKINSVILLE 5 SSE | GA | US | 11.2 | 1 | 0.9506 | 15.6 | coverage_below_0_97 |
| 701 Barnett Shoals | GA | 999999-63850 WATKINSVILLE 5 SSE | GA | US | 9.6 | 1 | 0.9506 | 15.6 | coverage_below_0_97 |
| 60047 Middlebury Solar | IN | 724388-99999 GOSHEN MUNI | IN | US | 20.5 | 1 | 0.9508 | -7.6 | coverage_below_0_97;station_last_observation_before_2010 |
| 60721 Green Cow Power | IN | 724388-99999 GOSHEN MUNI | IN | US | 10.6 | 1 | 0.9508 | -7.6 | coverage_below_0_97;station_last_observation_before_2010 |
| 3494 Permian Basin | TX | 999999-03047 MONAHANS 6 ENE | TX | US | 15.4 | 1 | 0.9509 | 11.8 | coverage_below_0_97;shared_station_gt_10_plants |
| 55581 King Mountain Wind Ranch 1 | TX | 999999-03047 MONAHANS 6 ENE | TX | US | 70.6 | 1 | 0.9509 | 11.8 | distance_gt_50km;coverage_below_0_97;shared_station_gt_10_plants |
| 56961 Notrees Windpower Hybrid | TX | 999999-03047 MONAHANS 6 ENE | TX | US | 41.5 | 1 | 0.9509 | 11.8 | coverage_below_0_97;shared_station_gt_10_plants |
| 60123 Castle Gap Solar Hybrid | TX | 999999-03047 MONAHANS 6 ENE | TX | US | 65.1 | 1 | 0.9509 | 11.8 | distance_gt_50km;coverage_below_0_97;shared_station_gt_10_plants |
| 60581 Upton County Solar | TX | 999999-03047 MONAHANS 6 ENE | TX | US | 64.7 | 1 | 0.9509 | 11.8 | distance_gt_50km;coverage_below_0_97;shared_station_gt_10_plants |
| 61906 Phoebe Solar | TX | 999999-03047 MONAHANS 6 ENE | TX | US | 25.3 | 1 | 0.9509 | 11.8 | coverage_below_0_97;shared_station_gt_10_plants |
| 62561 Roadrunner, LLC Hybrid | TX | 999999-03047 MONAHANS 6 ENE | TX | US | 73.5 | 1 | 0.9509 | 11.8 | distance_gt_50km;coverage_below_0_97;shared_station_gt_10_plants |
| 62932 Oberon IB | TX | 999999-03047 MONAHANS 6 ENE | TX | US | 13.0 | 1 | 0.9509 | 11.8 | coverage_below_0_97;shared_station_gt_10_plants |
| 62933 Oberon IA | TX | 999999-03047 MONAHANS 6 ENE | TX | US | 13.5 | 1 | 0.9509 | 11.8 | coverage_below_0_97;shared_station_gt_10_plants |
| 63519 Crane Solar Project | TX | 999999-03047 MONAHANS 6 ENE | TX | US | 62.3 | 1 | 0.9509 | 11.8 | distance_gt_50km;coverage_below_0_97;shared_station_gt_10_plants |
| ... | 531 more rows omitted |  |  |  |  |  |  |  |  |

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
