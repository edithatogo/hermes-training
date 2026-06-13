from __future__ import annotations

import unittest

from scripts.build_runtime_proof_action_queue import build_queue, lane_for, next_command


def candidate(**overrides: object) -> dict[str, object]:
    data: dict[str, object] = {
        "id": "example/model",
        "family": "example",
        "role": "local-runtime",
        "environment": "mac-mlx",
        "parameters": "4B",
        "feasibility": "ready",
        "first_runtime": "MLX smoke",
        "notes": "",
    }
    data.update(overrides)
    return data


class RuntimeProofActionQueueTests(unittest.TestCase):
    def test_runtime_support_blocker_gets_distinct_lane(self) -> None:
        item = candidate()

        lane = lane_for(item, "blocked", "blocked by current local runtime support")

        self.assertEqual(lane, "runtime-support-upgrade")

    def test_runtime_support_upgrade_command_avoids_repeat_candidate_run(self) -> None:
        item = candidate(id="google/gemma-4-E2B")

        command = next_command(item, "runtime-support-upgrade")

        self.assertIn("Do not rerun the same candidate", command)
        self.assertNotIn("run_local_pilot_benchmark.py", command)

    def test_hf_transformers_runtime_proof_uses_bounded_transformers_pilot(self) -> None:
        item = candidate(id="google/gemma-4-E4B-it-qat-mobile-transformers", environment="hf-transformers")

        command = next_command(item, "mac-runtime-proof")

        self.assertIn("scripts/run_transformers_pilot_benchmark.py", command)
        self.assertIn("--device auto", command)
        self.assertIn("--require-no-extra-tool-text", command)
        self.assertIn("SSD-backed Hugging Face cache", command)

    def test_hf_transformers_command_is_not_overridden_by_gguf_runtime_text(self) -> None:
        item = candidate(
            id="DJLougen/Harmonic-9B",
            environment="hf-transformers",
            first_runtime="Transformers or GGUF smoke",
        )

        command = next_command(item, "mac-runtime-proof")

        self.assertIn("scripts/run_transformers_pilot_benchmark.py", command)
        self.assertNotIn("scripts/run_endpoint_pilot_benchmark.py", command)

    def test_lmstudio_non_gguf_command_uses_runtime_neutral_artifact_hint(self) -> None:
        item = candidate(
            id="openbmb/MiniCPM-V-4.6-GPTQ",
            environment="mac-lmstudio",
            first_runtime="LM Studio local smoke",
        )

        command = next_command(item, "mac-runtime-proof")

        self.assertIn("scripts/run_endpoint_pilot_benchmark.py", command)
        self.assertIn("smallest compatible local artifact", command)
        self.assertNotIn("smallest compatible GGUF", command)
        self.assertIn("--require-no-extra-tool-text", command)

    def test_lmstudio_gguf_command_uses_strict_endpoint_scoring(self) -> None:
        item = candidate(
            id="DJLougen/Harmonic-Hermes-9B-GGUF",
            environment="mac-lmstudio",
            first_runtime="llama.cpp / LM Studio / Ollama GGUF smoke",
        )

        command = next_command(item, "mac-runtime-proof")

        self.assertIn("scripts/run_endpoint_pilot_benchmark.py", command)
        self.assertIn("smallest compatible GGUF", command)
        self.assertIn("--require-no-extra-tool-text", command)

    def test_mlx_runtime_proof_uses_strict_local_scoring(self) -> None:
        item = candidate(id="deepsweet/Qwen3.6-35B-A3B-MLX-oQ4", environment="mac-mlx")

        command = next_command(item, "mac-runtime-proof")

        self.assertIn("scripts/run_local_pilot_benchmark.py", command)
        self.assertIn("--require-no-extra-tool-text", command)

    def test_prompt_profile_repair_uses_strict_local_scoring(self) -> None:
        item = candidate(id="mlx-community/gemma-4-E4B-it-qat-4bit", environment="mac-mlx")

        command = next_command(item, "prompt-profile-repair")

        self.assertIn("scripts/run_local_pilot_benchmark.py", command)
        self.assertIn("strict-profile-repair", command)
        self.assertIn("--require-no-extra-tool-text", command)

    def test_jina_mlx_support_command_uses_default_ssd_repo_dir_without_placeholder(self) -> None:
        item = candidate(
            id="jinaai/jina-embeddings-v5-omni-small-text-matching-mlx",
            family="jina",
            role="retrieval",
            environment="mac-mlx",
            first_runtime="Jina MLX embedding smoke",
            notes="Jina MLX text-matching support lane",
        )

        command = next_command(item, "support-model-proof")

        self.assertIn("scripts/run_jina_mlx_embedding_benchmark.py", command)
        self.assertIn("--task-type text-matching", command)
        self.assertIn("--local-files-only", command)
        self.assertIn("memory_retrieval_differentiation_suite.json", command)
        self.assertIn("default SSD repo-dir", command)
        self.assertNotIn("--repo-dir", command)
        self.assertNotIn("<repo-dir>", command)

    def test_jina_mlx_support_command_defaults_to_retrieval_task(self) -> None:
        item = candidate(
            id="jinaai/jina-embeddings-v5-omni-small-mlx",
            family="jina",
            role="retrieval",
            environment="mac-mlx",
            first_runtime="Jina MLX embedding smoke",
            notes="Jina MLX retrieval support lane",
        )

        command = next_command(item, "support-model-proof")

        self.assertIn("--task-type retrieval", command)
        self.assertNotIn("<repo-dir>", command)

    def test_runtime_support_upgrade_sorts_after_real_runtime_proofs(self) -> None:
        rows = build_queue(
            [
                candidate(id="blocked/runtime", environment="hf-transformers"),
                candidate(id="missing/artifact", environment="mac-mlx", feasibility="needs-runtime-proof"),
            ],
            [
                {
                    "project": "hermes",
                    "id": "blocked/runtime",
                    "coverage_state": "blocked",
                    "blocked_reason": "blocked by current local runtime support",
                },
                {
                    "project": "hermes",
                    "id": "missing/artifact",
                    "coverage_state": "blocked",
                    "blocked_reason": "blocked until runtime artifact/load proof exists",
                },
            ],
        )

        self.assertEqual(rows[0]["id"], "missing/artifact")
        self.assertEqual(rows[1]["lane"], "runtime-support-upgrade")

    def test_runtime_proofs_sort_by_acquisition_size_before_active_size(self) -> None:
        rows = build_queue(
            [
                candidate(id="huge/moe", parameters="80B total / 3B active", environment="hf-transformers"),
                candidate(id="small/dense", parameters="4B", environment="mac-mlx"),
            ],
            [
                {
                    "project": "hermes",
                    "id": "huge/moe",
                    "coverage_state": "blocked",
                    "blocked_reason": "blocked until runtime artifact/load proof exists",
                },
                {
                    "project": "hermes",
                    "id": "small/dense",
                    "coverage_state": "blocked",
                    "blocked_reason": "blocked until runtime artifact/load proof exists",
                },
            ],
        )

        self.assertEqual(rows[0]["id"], "small/dense")
        self.assertEqual(rows[1]["id"], "huge/moe")


if __name__ == "__main__":
    unittest.main()
