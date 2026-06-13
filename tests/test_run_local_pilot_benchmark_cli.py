from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RunLocalPilotBenchmarkCliTests(unittest.TestCase):
    def test_dry_run_reports_system_affixes_without_loading_model(self) -> None:
        suite = [
            {
                "id": "case-1",
                "category": "tool_call_exact",
                "messages": [{"role": "system", "content": "Use tools."}, {"role": "user", "content": "Ping"}],
                "expected": {"tool_calls": []},
            }
        ]
        with tempfile.TemporaryDirectory() as tmp:
            suite_path = Path(tmp) / "suite.json"
            suite_path.write_text(json.dumps(suite), encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/run_local_pilot_benchmark.py",
                    "--suite",
                    str(suite_path),
                    "--model",
                    "example/model",
                    "--system-prefix",
                    "PREFIX ",
                    "--system-suffix",
                    " SUFFIX",
                    "--dry-run",
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("system_prefix: PREFIX ", result.stdout)
        self.assertIn("system_suffix:  SUFFIX", result.stdout)
        self.assertIn("model: example/model", result.stdout)


if __name__ == "__main__":
    unittest.main()
