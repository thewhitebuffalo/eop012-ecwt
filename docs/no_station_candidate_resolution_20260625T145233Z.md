# No-Station Candidate Resolution

Generated UTC: 2026-06-25T14:52:33Z

## Scope Decision

- Alaska is excluded from the current publication analysis scope by user direction.
- After excluding Alaska, the all-plants policy result has 32 blocked rows:
  - 28 no-station-candidate rows.
  - 4 normalized active-window coverage rows, all in Texas.
- Of the 28 no-station-candidate rows, 27 are nonphysical, unsited, unlocatable, or otherwise unsuitable for station matching under the current EIA asset record.
- The remaining no-station-candidate row with enough information to repair is SPI - Everett, EIA plant code 56281.

## SPI - Everett Geocode Repair Candidate

Loaded EIA asset row:

- EIA plant code: 56281
- Plant name: SPI - Everett
- Utility: Sierra Pacific Industries
- Sector: Industrial Non-CHP
- Address: 515 East Marine View Drive, Everett, WA 98206
- County: Snohomish
- Loaded latitude/longitude: blank
- First-scope generator count: 0
- First-scope nameplate MW: 0.000

Generator scope caveat:

- `asset.generator` has one SPI - Everett row, generator GEN1.
- Generator status is `CN`.
- Generator sheet is `Retired and Canceled`.
- Nameplate capacity is 28 MW, but this generator is not in the first-operable status set `OP`, `SB`, `OA`, `OS`.

Geocode evidence:

- Source: U.S. Census Geocoder, `Public_AR_Current` benchmark.
- Input address: 515 East Marine View Drive, Everett, WA 98206
- Matched address: 515 E MARINE VIEW DR, EVERETT, WA, 98201
- Latitude: 48.010056618695
- Longitude: -122.189465912616
- TIGER line ID: 617115938

Interpretation:

- SPI - Everett can be geocoded and assigned nearby NOAA station candidates.
- Because the loaded EIA generator is retired/canceled, SPI - Everett should not be treated as a first-operable publication blocker unless the scope policy is changed.
- If retained in an all-plants informational output, calculate ECWT with a documented geocode override and station-selection decision.

## Nearby NOAA Candidates For SPI - Everett

Nearest currently loaded station ECWT rows within 100 km:

| Station | Name | Country | Distance km | ECWT F | Valid Hours | Expected Hours | Coverage Ratio | Active Window |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| `727937-24222` | SNOHOMISH CO (PAINE FD) AP | US | 11.925 | 21.2 | 5,316 | 43,320 | 0.122715 | 2005-12-31 to 2025-08-26 |
| `727945-04205` | ARLINGTON MUNICIPAL ARPT | US | 16.936 | 14.0 | 5,523 | 43,320 | 0.127493 | 2005-12-31 to 2025-08-24 |
| `994350-99999` | WEST POINT WA | US/blank state | 42.854 | 23.54 | 45,190 | 47,664 | 0.948095 | 1985-04-30 to 2025-08-23 |
| `994025-99999` | PORT TOWNSEND | US | 43.745 | 21.38 | 33,312 | 36,816 | 0.904824 | 2007-12-31 to 2025-08-23 |
| `994014-99999` | SEATTLE | US | 46.386 | 24.08 | 21,198 | 23,808 | 0.890373 | 2007-12-31 to 2019-01-01 |
| `720749-24255` | WHIDBEY ISLAND NAS | US | 51.792 | 17.6 | 14,702 | 45,480 | 0.323263 | 2004-12-31 to 2025-08-24 |
| `727935-99999` | BOEING FLD KING CO | US | 55.444 | 28.4 | 8,524 | 8,664 | 0.983841 | 1999-12-31 to 2003-12-30 |
| `712000-99999` | VICTORIA GONZALES CS BC | CA | 94.138 | 3.92 | 54,335 | 56,328 | 0.964618 | 1955-07-01 to 2025-08-23 |
| `717830-99999` | VICTORIA UNIVERSITY CS | CA | 95.705 | 3.92 | 47,941 | 49,824 | 0.962207 | 1995-04-22 to 2025-08-23 |
| `742060-99999` | MC CHORD FIELD | US | 99.979 | 21.2 | 10,357 | 10,848 | 0.954738 | 1999-12-31 to 2004-12-30 |

Station-selection caveat:

- The nearest modern airport stations have low loaded full-period coverage in the current ECWT table.
- The nearest station passing a 0.95 coverage threshold is an older Boeing Field station whose active window ends in 2003.
- Canadian stations near Victoria have strong coverage and much colder ECWT values, but cross-border station use should be an explicit policy decision.

## No-Station Rows Recommended For Exclusion Or Separate Nonphysical Review

These 27 rows have zero first-scope generators, zero first-scope nameplate MW, and no usable coordinates in the loaded EIA asset table.

| EIA Plant Code | Plant Name | State | County | Loaded Address/Location | Reason |
| --- | --- | --- | --- | --- | --- |
| 7708 | APC1 | AL |  | unsited, AL 0 | nonphysical_or_unlocatable |
| 7876 | APC2 | AL |  | unsited, AL | nonphysical_or_unlocatable |
| 7877 | APC3 | AL |  | unsited, AL | nonphysical_or_unlocatable |
| 56354 | Tampa Electric Co NA 4 | FL |  | Unknown, FL 0 | nonphysical_or_unlocatable |
| 7744 | Unsited | FL |  | FL 0 | nonphysical_or_unlocatable |
| 7889 | NA 1 | FL |  | FL | nonphysical_or_unlocatable |
| 7890 | Unnamed | FL |  | FL | nonphysical_or_unlocatable |
| 7893 | Midway | FL | Taylor | Taylor County, FL | nonphysical_or_unlocatable |
| 7711 | GPC3 | GA |  | GA 0 | nonphysical_or_unlocatable |
| 7712 | GPC4 | GA |  | GA 0 | nonphysical_or_unlocatable |
| 7713 | GPC5 | GA |  | GA 0 | nonphysical_or_unlocatable |
| 7714 | GPC6 | GA |  | GA 0 | nonphysical_or_unlocatable |
| 7879 | MEAG1 | GA |  | unsited, GA | nonphysical_or_unlocatable |
| 7880 | MEAG2 | GA |  | unsited, GA | nonphysical_or_unlocatable |
| 7881 | MEAG3 | GA |  | unsited, GA | nonphysical_or_unlocatable |
| 7228 | NA 1 (IN) | IN | NOT IN FILE | NOT IN FILE, IN 0 | nonphysical_or_unlocatable |
| 7894 | Unknown | KY |  | KY | nonphysical_or_unlocatable |
| 7875 | MPC1 | MS |  | unknown, unknown, MS | nonphysical_or_unlocatable |
| 7539 | NA 1 (NC) | NC | NOT IN FILE | unsited, unsited, NC 0 | nonphysical_or_unlocatable |
| 7727 | Future Gen Plant 1 | NC |  | unsited, unsited, NC 0 | nonphysical_or_unlocatable |
| 7728 | Future Gen Plant 2 | NC |  | unsited, unsited, NC 0 | nonphysical_or_unlocatable |
| 55252 | Eddy County Generating Station | NM | Eddy | Eddy County, NM | nonphysical_or_unlocatable |
| 7106 | NA 1 (SC) | SC | NOT IN FILE | unsited, unsited, SC 0 | nonphysical_or_unlocatable |
| 7253 | NA 5 | SC | NOT IN FILE | unsited, unsited, SC 0 | nonphysical_or_unlocatable |
| 7300 | NA 8 | SC | NOT IN FILE | unsited, unsited, SC 0 | nonphysical_or_unlocatable |
| 7732 | Turbine | TX | El Paso | NA, El Paso, TX 79938 | nonphysical_or_unlocatable |
| 60203 | Wheaton Solar | WI | Chippewa | TBD, Wheaton, WI | nonphysical_or_unlocatable |

## Remaining Non-Alaska Weather Blockers

After Alaska exclusion and no-station classification, four Texas low-coverage rows remain:

| EIA Plant Code | Plant Name | County | Selected Station | Distance km | ECWT F | Coverage Ratio |
| --- | --- | --- | --- | ---: | ---: | ---: |
| 58048 | BayWa r.e Mozart LLC | Kent | `723528-99999` FREDERICK MUNI | 209.620 | 14.0 | 0.945034 |
| 62142 | Amadeus Wind Farm | Fisher | `723528-99999` FREDERICK MUNI | 212.354 | 14.0 | 0.945034 |
| 63223 | Brightside | Bee | `722539-99999` SAN MARCOS MUNI | 163.362 | 24.8 | 0.947263 |
| 65644 | Lumina II Solar Project | Scurry | `723528-99999` FREDERICK MUNI | 230.847 | 14.0 | 0.945034 |

## Recommended Next Actions

1. Add an auditable plant geocode override for SPI - Everett using the Census result above.
2. Rerun station-candidate generation, candidate coverage enrichment, and policy materialization.
3. Publish SPI - Everett either as an informational all-plants ECWT row or exclude it from first-operable scope because the only generator is retired/canceled.
4. Exclude Alaska from the current publication scope.
5. Move the 27 nonphysical/unlocatable no-station rows out of the weather-blocker bucket and into a denominator-exclusion or nonphysical-review bucket.
6. Review the four Texas low-coverage rows as the remaining non-Alaska weather blockers.
