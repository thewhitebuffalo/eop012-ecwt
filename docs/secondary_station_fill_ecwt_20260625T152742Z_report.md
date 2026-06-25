# Secondary Station Fill ECWT

- Calculation run ID: `secondary_station_fill_ecwt_20260625T152742Z`
- Policy result run ID: `plant_ecwt_policy_result_all_plants_normalized_active_window_loaded_year_20260625T135248Z`
- Station candidate run ID: `noaa_station_candidates_20260625T065445Z`
- Station ECWT run ID: `station_ecwt_loaded_20260625T124223Z`
- Database: `eop012` on `127.0.0.1:5436`
- Coverage threshold: `0.950000`
- Percentile target: `0.002000`
- Selected fallback rows: `/Users/Shared/EOP012/rebuild/docs/secondary_station_fill_ecwt_20260625T152742Z_plants.csv`
- Candidate score audit: `/Users/Shared/EOP012/rebuild/docs/secondary_station_fill_ecwt_20260625T152742Z_candidate_scores.csv`

## Method

The selected primary station remains the representative station. For each fallback candidate, the calculation builds the UTC DJF expected-hour set for the primary station's loaded-year window, uses the primary dry-bulb value wherever it exists, fills only missing primary hours from the fallback station, and recalculates ECWT on that composite series.

The chosen fallback is the nearest candidate station that satisfies all of these checks:

1. generated expected hours equal the policy-result expected hours
2. recomputed primary valid hours equal the policy-result primary valid hours
3. fallback adds at least one valid missing primary hour
4. composite valid hours meet or exceed the coverage threshold

## Selected Rows

| EIA Plant | Plant | Primary Station | Fallback Station | Filled Hours | Composite Coverage | Composite ECWT F | Status |
| ---: | --- | --- | --- | ---: | ---: | ---: | --- |
| 58048 | BayWa r.e Mozart LLC | `723528-99999` | `722122-99999` | 144 | 0.95610393603936039360 | 14 | `passes_composite_fill` |
| 62142 | Amadeus Wind Farm | `723528-99999` | `722122-99999` | 144 | 0.95610393603936039360 | 14 | `passes_composite_fill` |
| 63223 | Brightside | `722539-99999` | `720316-99999` | 173 | 0.96056273062730627306 | 24.8 | `passes_composite_fill` |
| 65644 | Lumina II Solar Project | `723528-99999` | `722122-99999` | 144 | 0.95610393603936039360 | 14 | `passes_composite_fill` |

## Best-Row Status Counts

| Status | Plants |
| --- | ---: |
| `passes_composite_fill` | 4 |

## Candidate Score Counts

| Status | Candidate Rows |
| --- | ---: |
| `blocked_composite_below_threshold` | 30 |
| `blocked_no_missing_hours_filled` | 196 |
| `passes_composite_fill` | 170 |
