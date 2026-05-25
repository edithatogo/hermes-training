from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.check_specialist_runtime_preflight import Probe, artifact_status, evaluate_probe, render_markdown


class SpecialistRuntimePreflightTests(unittest.TestCase):
    def test_probe_blocks_when_runtime_and_artifact_are_missing(self) -> None:
        probe = Probe(
            lane_id="ktransformers-moe",
            model="example/model",
            runtime="ExampleRuntime",
            commands=("definitely-missing-runtime-command",),
            modules=("definitely_missing_runtime_module",),
            artifact_paths=(Path("/definitely/missing/artifact"),),
            minimum_pass="runtime plus artifact",
            notes="test",
        )

        result = evaluate_probe(probe)

        self.assertEqual(result["status"], "blocked")
        self.assertIn("runtime command/module not found", result["blockers"])
        self.assertIn("no matching SSD artifact path found", result["blockers"])

    def test_artifact_status_detects_existing_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = artifact_status(Path(tmp))

            self.assertTrue(result["present"])
            self.assertEqual(result["kind"], "directory")

    def test_markdown_records_no_promotion_decision(self) -> None:
        markdown = render_markdown(
            {
                "created_at": "2026-05-26T00:00:00+00:00",
                "ssd_root": "/Volumes/PortableSSD",
                "policy": "read-only",
                "items": [
                    {
                        "lane_id": "recurrent-ssm-bitnet",
                        "model": "microsoft/bitnet-b1.58-2B-4T",
                        "runtime": "BitNet native runtime",
                        "status": "blocked",
                        "blockers": ["runtime command/module not found"],
                        "commands": [{"name": "bitnet", "present": False}],
                        "modules": [{"name": "bitnet", "present": False}],
                        "artifacts": [{"path": "/tmp/missing", "present": False}],
                        "minimum_pass": "runtime plus checkpoint",
                        "notes": "test",
                    }
                ],
            }
        )

        self.assertIn("No specialist lane is promoted", markdown)
        self.assertIn("BitNet native runtime", markdown)


if __name__ == "__main__":
    unittest.main()
