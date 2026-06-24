import json
import tempfile
import unittest
from pathlib import Path

from scripts.build_bfcl_clean_rerun_report import build_report


class BFCLCleanRerunReportTests(unittest.TestCase):
    def test_report_blocks_on_blank_outputs_after_upstream_clears(self) -> None:
        with tempfile.TemporaryDirectory(dir="/Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl") as tmp:
            root = Path(tmp)
            result_dir = root / "results/Qwen_Qwen3-4B-Instruct-2507-FC/non_live"
            result_dir.mkdir(parents=True)
            rows = [
                {"id": "multiple_0", "result": "\n\n"},
                {"id": "multiple_1", "result": "\n\n"},
            ]
            (result_dir / "BFCL_v4_multiple_result.json").write_text(
                "\n".join(json.dumps(row) for row in rows) + "\n",
                encoding="utf-8",
            )

            report = build_report(root)

        self.assertEqual(report["status"], "blocked-blank-output-gate")
        self.assertFalse(report["gate"]["passed"])
        self.assertEqual(report["summary"]["upstream_error_rows"], 0)
        self.assertEqual(report["summary"]["blank_output_rows"], 2)

    def test_report_blocks_on_upstream_errors_first(self) -> None:
        with tempfile.TemporaryDirectory(dir="/Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl") as tmp:
            root = Path(tmp)
            result_dir = root / "results/Qwen_Qwen3-4B-Instruct-2507-FC/non_live"
            result_dir.mkdir(parents=True)
            (result_dir / "BFCL_v4_multiple_result.json").write_text(
                json.dumps({"id": "multiple_0", "result": "Error during inference: Error code: 502"}) + "\n",
                encoding="utf-8",
            )

            report = build_report(root)

        self.assertEqual(report["status"], "blocked-upstream-error-gate")
        self.assertEqual(report["summary"]["upstream_error_rows"], 1)


if __name__ == "__main__":
    unittest.main()
