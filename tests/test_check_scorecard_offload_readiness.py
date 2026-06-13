from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.check_scorecard_offload_readiness import build_report


class ScorecardOffloadReadinessTests(unittest.TestCase):
    def test_mlx_adapter_blocks_exact_cuda_offload(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plan = root / "plan.yaml"
            adapter = root / "adapter"
            adapter.mkdir()
            plan.write_text(
                "\n".join(
                    [
                        "run_id: run",
                        "candidate: candidate",
                        "model: Qwen/Qwen3-4B-MLX-4bit",
                        "limit: null",
                        "output_dir: /Volumes/PortableSSD/hermes-evals/standard-benchmarks/lm-eval/run",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            (adapter / "adapter_config.json").write_text(json.dumps({"model": "Qwen/Qwen3-4B-MLX-4bit"}), encoding="utf-8")
            (adapter / "adapters.safetensors").write_bytes(b"weights")

            report = build_report(plan, adapter / "adapter_config.json")

            self.assertEqual(report["status"], "blocked")
            self.assertEqual(report["adapter_classification"]["framework"], "mlx-native")
            self.assertFalse(report["exact_adapter_portable"])
            self.assertTrue(any("MLX-native" in blocker for blocker in report["blockers"]))

    def test_peft_adapter_is_ready_when_plan_is_full_and_ssd_backed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plan = root / "plan.yaml"
            adapter = root / "adapter"
            adapter.mkdir()
            plan.write_text(
                "\n".join(
                    [
                        "run_id: run",
                        "candidate: candidate",
                        "model: Qwen/Qwen3-4B-Instruct",
                        "limit: null",
                        "output_dir: /Volumes/PortableSSD/hermes-evals/standard-benchmarks/lm-eval/run",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            (adapter / "adapter_config.json").write_text(json.dumps({"model": "Qwen/Qwen3-4B-Instruct", "peft_type": "LORA"}), encoding="utf-8")
            (adapter / "adapter_model.safetensors").write_bytes(b"weights")

            report = build_report(plan, adapter / "adapter_config.json")

            self.assertEqual(report["status"], "ready")
            self.assertEqual(report["adapter_classification"]["framework"], "hf-peft")
            self.assertTrue(report["exact_adapter_portable"])
