from __future__ import annotations

import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from scripts.build_prompt_profile_repair_experiments import build_experiments, command_for, variants_for


def row(**overrides: object) -> dict[str, object]:
    data: dict[str, object] = {
        "id": "Qwen/Qwen3.5-2B",
        "family": "qwen",
        "environment": "mac-mlx",
        "blocked_reason": "blocked by empty/no-content generation under the strict prompt",
    }
    data.update(overrides)
    return data


class BuildPromptProfileRepairExperimentsTests(unittest.TestCase):
    def test_qwen_empty_candidate_gets_no_think_variant(self) -> None:
        variants = variants_for(row())

        self.assertIn("qwen-no-think-prefill", [variant["id"] for variant in variants])
        command = command_for(row(), next(variant for variant in variants if variant["id"] == "qwen-no-think-prefill"))
        self.assertIn("scripts/run_local_pilot_benchmark.py", command)
        self.assertIn("--user-prefix /no_think", command)
        self.assertIn("--assistant-prefill", command)
        self.assertIn("--require-no-extra-tool-text", command)
        self.assertIn("No download here", command)

    def test_gemma_candidate_gets_analysis_only_normalizer_variant(self) -> None:
        experiments = build_experiments(
            [
                row(
                    id="mlx-community/gemma-4-E4B-it-qat-4bit",
                    family="gemma",
                    blocked_reason="blocked by strict Hermes tool-call formatting failure",
                )
            ]
        )

        normalizer = next(item for item in experiments if item["variant"] == "gemma-native-normalizer-analysis")
        self.assertFalse(normalizer["raw_output_promotion_allowed"])
        self.assertIn("--score-normalizer gemma-native-tool-call", normalizer["command"])

    def test_endpoint_gemma_does_not_emit_unsupported_normalizer_variant(self) -> None:
        variants = variants_for(
            row(
                id="google/gemma-4-E2B-it-qat-q4_0-gguf",
                family="gemma",
                environment="mac-lmstudio",
                blocked_reason="blocked by strict Hermes tool-call formatting failure",
            )
        )

        self.assertNotIn("gemma-native-normalizer-analysis", [variant["id"] for variant in variants])

    def test_gguf_candidate_uses_endpoint_runner_with_placeholder_boundary(self) -> None:
        variant = variants_for(row(id="LiquidAI/LFM2.5-8B-A1B-GGUF", family="lfm", environment="mac-lmstudio"))[0]
        command = command_for(row(id="LiquidAI/LFM2.5-8B-A1B-GGUF", family="lfm", environment="mac-lmstudio"), variant)

        self.assertIn("scripts/run_endpoint_pilot_benchmark.py", command)
        self.assertIn("http://127.0.0.1:<port>/v1", command)
        self.assertIn("--system-suffix", command)

    def test_endpoint_experiments_skip_local_only_score_normalizers(self) -> None:
        experiments = build_experiments(
            [
                row(
                    id="google/gemma-4-E2B-it-qat-q4_0-gguf",
                    family="gemma",
                    environment="mac-lmstudio",
                    blocked_reason="blocked by strict Hermes tool-call formatting failure",
                )
            ]
        )

        self.assertNotIn("--score-normalizer", "\n".join(str(item["command"]) for item in experiments))

    def test_endpoint_route_from_queue_command_overrides_mlx_environment(self) -> None:
        item = row(
            id="LGAI-EXAONE/EXAONE-4.0-1.2B",
            family="exaone",
            environment="mac-mlx",
            repair_hypothesis="test strict JSON envelope prompting on the existing GGUF endpoint",
            next_command="scripts/run_endpoint_pilot_benchmark.py --model lgai-exaone-exaone-4-0-1-2b",
        )
        command = command_for(item, variants_for(item)[0])

        self.assertIn("scripts/run_endpoint_pilot_benchmark.py", command)
        self.assertNotIn("scripts/run_local_pilot_benchmark.py", command)

    def test_cloud_only_candidate_does_not_emit_executable_experiments(self) -> None:
        experiments = build_experiments(
            [
                row(
                    id="Qwen/Qwen3.6-35B-A3B",
                    family="qwen",
                    environment="azure-cuda",
                    blocked_reason="blocked by strict Hermes tool-call formatting failure",
                )
            ]
        )

        self.assertEqual(experiments, [])


if __name__ == "__main__":
    unittest.main()
