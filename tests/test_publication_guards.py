from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import export_scoped_plant_ecwt_dataset as scoped_export  # noqa: E402
import build_ecwt_dashboard as ecwt_dashboard  # noqa: E402
import build_readiness_policy_scenarios as policy_scenarios  # noqa: E402
import materialize_policy_ecwt_results as policy_results  # noqa: E402


class PolicyMaterializationGuardTests(unittest.TestCase):
    def test_fixed_period_candidate_materializes_as_publication_candidate(self) -> None:
        row = {
            "scenario_label": "Current fixed-period publication gate",
            "policy_suitability": "current_conservative_gate",
            "candidate_source": "current_fixed_period_publication_candidate",
            "plant_id": "plant:1",
        }

        result = policy_results.candidate_result_row(
            "run",
            "all-plants",
            "fixed_period_current_gate",
            "scenario",
            "denominator",
            row,
        )

        self.assertEqual(result["readiness_status"], "publication_candidate")
        self.assertEqual(result["reason_code"], "passes_current_fixed_period_gate")

    def test_normalized_active_candidate_materializes_as_diagnostic_candidate(self) -> None:
        row = {
            "scenario_label": "Normalized active-window loaded-year gate",
            "policy_suitability": "diagnostic_only_not_publication_gate",
            "candidate_source": "promoted_fixed_period_blocker",
            "plant_id": "plant:1",
        }

        result = policy_results.candidate_result_row(
            "run",
            "all-plants",
            "normalized_active_window_loaded_year",
            "scenario",
            "denominator",
            row,
        )

        self.assertEqual(result["readiness_status"], policy_results.DIAGNOSTIC_CANDIDATE_STATUS)
        self.assertEqual(result["reason_code"], "passes_diagnostic_active_window_policy_only")


class PolicyScenarioGuardTests(unittest.TestCase):
    def test_existing_fixed_candidate_preserves_station_distance(self) -> None:
        row = {
            "plant_id": "plant:1",
            "eia_plant_code": "1",
            "plant_name": "Plant",
            "plant_state": "TX",
            "plant_county": "County",
            "sector_name": "Electric Utility",
            "first_scope_generator_count": "1",
            "first_scope_nameplate_mw": "100",
            "selected_station_id": "station:1",
            "selected_station_name": "Station",
            "selected_station_state": "TX",
            "selected_station_country": "US",
            "selected_station_distance_km": "24.75",
            "ecwt_f": "-12.3",
            "valid_hour_count": "54000",
            "expected_hour_count": "56000",
            "coverage_ratio": "0.964286",
        }

        result = policy_scenarios.existing_candidate_row(
            row,
            "fixed_period_current_gate",
            policy_scenarios.SCENARIOS["fixed_period_current_gate"],
        )

        self.assertEqual(result["selected_station_distance_km"], "24.75")


class DashboardGuardTests(unittest.TestCase):
    def test_dashboard_template_scripts_parse_after_data_injection(self) -> None:
        if shutil.which("node") is None:
            self.skipTest("node is not available for JavaScript syntax check")

        with tempfile.TemporaryDirectory() as tmp:
            release_csv = Path(tmp) / "scoped_plant_ecwt_release_test.csv"
            release_csv.write_text(
                "\n".join(
                    [
                        "plant_latitude,plant_longitude,ecwt_f,plant_state,plant_name,primary_station_distance_km,readiness_status,reason_code",
                        "44.1,-73.2,-12.3,VT,O'Brien Hydro,24.5,publication_candidate,passes_current_fixed_period_gate",
                        ",,,AK,No Candidate Plant,,blocked,no_station_candidates",
                    ]
                ),
                encoding="utf-8",
            )
            payload = ecwt_dashboard.build_payload(release_csv)
            self.assertEqual(payload["kpis"]["plants"], 2)
            self.assertEqual(payload["kpis"]["plotted"], 1)
            self.assertEqual(payload["quality"]["rowsMissingEcwt"], 1)
            self.assertEqual(payload["quality"]["reasonCodes"]["no_station_candidates"], 1)
            template = ecwt_dashboard.DEFAULT_TEMPLATE.read_text(encoding="utf-8")
            html = template.replace(
                ecwt_dashboard.PLACEHOLDER,
                "window.ECWT = " + json.dumps(payload, separators=(",", ":")) + ";",
            )
            scripts = "\n".join(re.findall(r"<script>(.*?)</script>", html, re.S))
            script_path = Path(tmp) / "dashboard.js"
            script_path.write_text(scripts, encoding="utf-8")

            result = subprocess.run(
                ["node", "--check", str(script_path)],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )

        self.assertEqual(result.returncode, 0, result.stderr)


class ScopedExportGuardTests(unittest.TestCase):
    def release_row(self, **overrides: str) -> dict[str, str]:
        row = {
            "method_source": "policy_result",
            "plant_id": "plant:1",
            "primary_station_distance_km": "24.5",
            "coverage_ratio": "0.950000",
            "valid_hour_count": "30000",
            "reason_code": "passes_current_fixed_period_gate",
            "coverage_basis": "fixed_period_station_local_djf_2000_to_calculation_cutoff",
        }
        row.update(overrides)
        return row

    def test_valid_fixed_period_export_row_passes(self) -> None:
        scoped_export.validate_export_rows([self.release_row()])

    def test_export_row_rejects_far_primary_station(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "primary station distance"):
            scoped_export.validate_export_rows(
                [self.release_row(primary_station_distance_km="100.001")]
            )

    def test_export_row_rejects_diagnostic_reason(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "policy reason"):
            scoped_export.validate_export_rows(
                [self.release_row(reason_code="passes_diagnostic_active_window_policy_only")]
            )


if __name__ == "__main__":
    unittest.main()
