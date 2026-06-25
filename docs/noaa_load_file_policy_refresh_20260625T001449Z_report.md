# NOAA Load-File Policy Stats Refresh Report

Generated UTC: 2026-06-25T00:14:51+00:00

## Run

- Calculation run ID: `noaa_load_file_policy_refresh_20260625T001449Z`
- Code commit: `420a25e89da66f00ce7f480b1d336ef2f91d3478`
- Dry run: `False`
- Station-years: `994973-99999:2019, 994973-99999:2020`
- Detail CSV: `noaa_load_file_policy_refresh_20260625T001449Z.csv`

## Summary

| Metric | Count |
| --- | ---: |
| Load-file rows checked | 2 |
| Load-file rows changed | 2 |

## Changed Rows

| Station | Year | Old Rejects | New Rejects | Old Valid | New Valid | Old Duplicates | New Duplicates | Old Loaded Hours | New Loaded Hours |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 994973-99999 | 2019 | 65 | 71 | 1197 | 1191 | 103 | 96 | 1094 | 1095 |
| 994973-99999 | 2020 | 8 | 13 | 1027 | 1022 | 15 | 11 | 1012 | 1011 |

## Interpretation

- This refresh updates only `weather.noaa_hourly_load_file` parser counters and records old/new counters in `audit.noaa_load_file_policy_refresh`.
- It does not modify `weather.hourly_djf`, station coverage, station ECWT, plant ECWT, or plant readiness rows.
- The targeted rows were originally loaded before the current SHEF-specific plausibility floor was added; the refreshed counters now match the current parser policy.
