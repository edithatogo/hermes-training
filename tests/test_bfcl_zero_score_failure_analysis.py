import json
import tempfile
import unittest
from pathlib import Path

from scripts.build_bfcl_zero_score_failure_analysis import analyze_results


class BFCLZeroScoreFailureAnalysisTests(unittest.TestCase):
    def test_analysis_classifies_contaminated_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rows = [
                {"id": "multiple_0", "result": "Error during inference: Error code: 502 Connection refused"},
                {"id": "multiple_1", "result": "\n\n"},
                {"id": "multiple_2", "result": '<tool_call>{"name":"x","arguments":{}}</tool_call>'},
                {"id": "multiple_3", "result": "plain answer"},
            ]
            (root / "BFCL_v4_multiple_result.json").write_text(
                "\n".join(json.dumps(row) for row in rows) + "\n",
                encoding="utf-8",
            )
            for category in ("parallel", "simple_python"):
                (root / f"BFCL_v4_{category}_result.json").write_text(
                    json.dumps({"id": f"{category}_0", "result": "Error during inference: upstream request failed"}) + "\n",
                    encoding="utf-8",
                )

            report = analyze_results(root)

        self.assertEqual(report["status"], "blocked-clean-regeneration-required")
        self.assertFalse(report["gate"]["promotable"])
        self.assertEqual(report["summary"]["counts"]["upstream_error"], 3)
        self.assertEqual(report["summary"]["counts"]["blank_output"], 1)
        self.assertEqual(report["summary"]["counts"]["tool_call_like"], 1)
        self.assertIn("--num-threads 1", "\n".join(report["gate"]["rerun_contract"]))


if __name__ == "__main__":
    unittest.main()
