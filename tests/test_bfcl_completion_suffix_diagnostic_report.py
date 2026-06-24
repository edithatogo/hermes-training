import json
import tempfile
import unittest
from pathlib import Path

from scripts.build_bfcl_completion_suffix_diagnostic_report import build_report, render_markdown
from scripts.validate_bfcl_completion_suffix_diagnostic_report import validate_payload


class BfclCompletionSuffixDiagnosticReportTests(unittest.TestCase):
    def write_run(self, root: Path, category: str, outputs: list[str]) -> None:
        result_root = root / "results/Qwen_Qwen3-4B-Instruct-2507-FC/non_live"
        result_root.mkdir(parents=True)
        with (result_root / f"BFCL_v4_{category}_result.json").open("w", encoding="utf-8") as handle:
            for index, output in enumerate(outputs):
                handle.write(json.dumps({"id": f"{category}_{index}", "result": output}) + "\n")

    def test_report_records_runtime_bridge_without_score_claim(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            clean = base / "clean"
            serial = base / "serial"
            self.write_run(clean, "multiple", ["\n\n"])
            self.write_run(serial, "multiple", ["\n\n", "\n\n\n"])
            report = build_report(clean, serial)
        self.assertEqual(report["status"], "runtime-bridge-ready-for-bounded-rerun")
        self.assertFalse(report["gate"]["passed"])
        self.assertEqual(report["completion_prompt_suffix"], "<tool_call>")
        self.assertIn("does not create a BFCL score claim", report["publication_boundary"])
        self.assertIn("Completion-Suffix Diagnostic", render_markdown(report))
        failures = validate_payload(report)
        self.assertIn("clean_rerun root must be SSD-backed", "\n".join(failures))


if __name__ == "__main__":
    unittest.main()
