# Plant ECWT Exception Review

Generated UTC: 2026-06-25T14:07:41+00:00

## Run

- Exception review run ID: `plant_ecwt_exception_review_20260625T140741Z`
- Policy result run ID: `plant_ecwt_policy_result_all_plants_normalized_active_window_loaded_year_20260625T135248Z`
- Code commit: `b29d87b8d97bd1781a2f287366b5e216e6aa31b6`
- Review CSV: `plant_ecwt_exception_review_20260625T140741Z.csv`
- Station summary CSV: `plant_ecwt_exception_review_20260625T140741Z_stations.csv`

## Loaded DB Counts

| Check | Rows |
| --- | ---: |
| `calc.plant_ecwt_exception_review` | 43 |
| `distinct plants` | 43 |
| `plant_geocode_required` | 28 |
| `coverage_threshold_exception_review` | 15 |

## Resolution Categories

| Category | Rows |
| --- | --- |
| plant_geocode_required | 28 |
| coverage_threshold_exception_review | 15 |

## Reason Codes

| Reason | Rows |
| --- | --- |
| no_station_candidates | 28 |
| normalized_active_window_coverage_below_threshold | 15 |

## Blocked Rows By State

| State | Rows |
| --- | --- |
| AK | 11 |
| GA | 7 |
| TX | 5 |
| FL | 5 |
| AL | 3 |
| NC | 3 |
| SC | 3 |
| IN | 1 |
| KY | 1 |
| MS | 1 |
| NM | 1 |
| WA | 1 |
| WI | 1 |

## Coverage Stations

| Station | Name | Plants | Median Coverage | Total Gap Hours | Retryable Failures |
| --- | --- | --- | --- | --- | --- |
| 702460-99999 | MINCHUMINA | 7 | 0.938422 | 882 | 0 |
| 723528-99999 | FREDERICK MUNI | 3 | 0.945034 | 195 | 0 |
| 999999-26655 | RED DOG MINE 3 SSW | 3 | 0.934586 | 1605 | 0 |
| 703430-99999 | MIDDLETON ISLAND | 1 | 0.945151 | 53 | 0 |
| 722539-99999 | SAN MARCOS MUNI | 1 | 0.947263 | 36 | 0 |

## Coverage Threshold Blockers

| Plant | State | Station | Coverage | Gap Hours | Action |
| --- | --- | --- | --- | --- | --- |
| Brightside | TX | 722539-99999 | 0.947263 | 36 | Review station selection, station-year coverage gaps, or approve a documented coverage-threshold exception. |
| Yakutat | AK | 703430-99999 | 0.945151 | 53 | Review station selection, station-year coverage gaps, or approve a documented coverage-threshold exception. |
| BayWa r.e Mozart LLC | TX | 723528-99999 | 0.945034 | 65 | Review station selection, station-year coverage gaps, or approve a documented coverage-threshold exception. |
| Amadeus Wind Farm | TX | 723528-99999 | 0.945034 | 65 | Review station selection, station-year coverage gaps, or approve a documented coverage-threshold exception. |
| Lumina II Solar Project | TX | 723528-99999 | 0.945034 | 65 | Review station selection, station-year coverage gaps, or approve a documented coverage-threshold exception. |
| Kotzebue Hybrid | AK | 702460-99999 | 0.938422 | 126 | Review station selection, station-year coverage gaps, or approve a documented coverage-threshold exception. |
| Kiana | AK | 702460-99999 | 0.938422 | 126 | Review station selection, station-year coverage gaps, or approve a documented coverage-threshold exception. |
| NSB Atqasuk Utility | AK | 702460-99999 | 0.938422 | 126 | Review station selection, station-year coverage gaps, or approve a documented coverage-threshold exception. |
| NSB Point Lay Utility | AK | 702460-99999 | 0.938422 | 126 | Review station selection, station-year coverage gaps, or approve a documented coverage-threshold exception. |
| NSB Wainwright Utility | AK | 702460-99999 | 0.938422 | 126 | Review station selection, station-year coverage gaps, or approve a documented coverage-threshold exception. |
| Noatak | AK | 702460-99999 | 0.938422 | 126 | Review station selection, station-year coverage gaps, or approve a documented coverage-threshold exception. |
| Ambler | AK | 702460-99999 | 0.938422 | 126 | Review station selection, station-year coverage gaps, or approve a documented coverage-threshold exception. |
| Barrow | AK | 999999-26655 | 0.934586 | 535 | Review station selection, station-year coverage gaps, or approve a documented coverage-threshold exception. |
| NSB Point Hope Utility | AK | 999999-26655 | 0.934586 | 535 | Review station selection, station-year coverage gaps, or approve a documented coverage-threshold exception. |
| Kivalina | AK | 999999-26655 | 0.934586 | 535 | Review station selection, station-year coverage gaps, or approve a documented coverage-threshold exception. |

## Geocode-Required Plants

| Plant | State | EIA Plant Code | Utility | Action |
| --- | --- | --- | --- | --- |
| APC1 | AL | 7708 | Alabama Power Co | Resolve EIA plant coordinates or approve a non-locatable/unsited plant exception before station matching. |
| APC2 | AL | 7876 | Alabama Power Co | Resolve EIA plant coordinates or approve a non-locatable/unsited plant exception before station matching. |
| APC3 | AL | 7877 | Alabama Power Co | Resolve EIA plant coordinates or approve a non-locatable/unsited plant exception before station matching. |
| Unsited | FL | 7744 | Florida Power & Light Co | Resolve EIA plant coordinates or approve a non-locatable/unsited plant exception before station matching. |
| NA 1 | FL | 7889 | Tampa Electric Co | Resolve EIA plant coordinates or approve a non-locatable/unsited plant exception before station matching. |
| Unnamed | FL | 7890 | Seminole Electric Cooperative Inc | Resolve EIA plant coordinates or approve a non-locatable/unsited plant exception before station matching. |
| Midway | FL | 7893 | Florida Power & Light Co | Resolve EIA plant coordinates or approve a non-locatable/unsited plant exception before station matching. |
| Tampa Electric Co NA 4 | FL | 56354 | Tampa Electric Co | Resolve EIA plant coordinates or approve a non-locatable/unsited plant exception before station matching. |
| GPC3 | GA | 7711 | Georgia Power Co | Resolve EIA plant coordinates or approve a non-locatable/unsited plant exception before station matching. |
| GPC4 | GA | 7712 | Georgia Power Co | Resolve EIA plant coordinates or approve a non-locatable/unsited plant exception before station matching. |
| GPC5 | GA | 7713 | Georgia Power Co | Resolve EIA plant coordinates or approve a non-locatable/unsited plant exception before station matching. |
| GPC6 | GA | 7714 | Georgia Power Co | Resolve EIA plant coordinates or approve a non-locatable/unsited plant exception before station matching. |
| MEAG1 | GA | 7879 | Municipal Electric Authority | Resolve EIA plant coordinates or approve a non-locatable/unsited plant exception before station matching. |
| MEAG2 | GA | 7880 | Municipal Electric Authority | Resolve EIA plant coordinates or approve a non-locatable/unsited plant exception before station matching. |
| MEAG3 | GA | 7881 | Municipal Electric Authority | Resolve EIA plant coordinates or approve a non-locatable/unsited plant exception before station matching. |
| NA 1 (IN) | IN | 7228 | Duke Energy Indiana, LLC | Resolve EIA plant coordinates or approve a non-locatable/unsited plant exception before station matching. |
| Unknown | KY | 7894 | Louisville Gas & Electric Co | Resolve EIA plant coordinates or approve a non-locatable/unsited plant exception before station matching. |
| MPC1 | MS | 7875 | Mississippi Power Co | Resolve EIA plant coordinates or approve a non-locatable/unsited plant exception before station matching. |
| NA 1 (NC) | NC | 7539 | Duke Energy Progress - (NC) | Resolve EIA plant coordinates or approve a non-locatable/unsited plant exception before station matching. |
| Future Gen Plant 1 | NC | 7727 | Duke Energy Progress - (NC) | Resolve EIA plant coordinates or approve a non-locatable/unsited plant exception before station matching. |
| Future Gen Plant 2 | NC | 7728 | Duke Energy Progress - (NC) | Resolve EIA plant coordinates or approve a non-locatable/unsited plant exception before station matching. |
| Eddy County Generating Station | NM | 55252 | Public Service Co of NM | Resolve EIA plant coordinates or approve a non-locatable/unsited plant exception before station matching. |
| NA 1 (SC) | SC | 7106 | Dominion Energy South Carolina, Inc | Resolve EIA plant coordinates or approve a non-locatable/unsited plant exception before station matching. |
| NA 5 | SC | 7253 | Dominion Energy South Carolina, Inc | Resolve EIA plant coordinates or approve a non-locatable/unsited plant exception before station matching. |
| NA 8 | SC | 7300 | Dominion Energy South Carolina, Inc | Resolve EIA plant coordinates or approve a non-locatable/unsited plant exception before station matching. |
| Turbine | TX | 7732 | El Paso Electric Co | Resolve EIA plant coordinates or approve a non-locatable/unsited plant exception before station matching. |
| SPI - Everett | WA | 56281 | Sierra Pacific Industries | Resolve EIA plant coordinates or approve a non-locatable/unsited plant exception before station matching. |
| Wheaton Solar | WI | 60203 | Northern States Power Co - Minnesota | Resolve EIA plant coordinates or approve a non-locatable/unsited plant exception before station matching. |

## Interpretation

- `plant_geocode_required` rows cannot enter station matching because EIA plant latitude/longitude is blank.
- `coverage_threshold_exception_review` rows already have candidate stations and no current retryable NOAA transport failure; the remaining issue is station selection, sparse source coverage, or policy exception treatment.
- This review does not change the policy result table. It creates a separate exception table so blocked plants stay explicit and auditable.
