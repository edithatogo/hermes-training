from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.validate_official_benchmark_manifests import ManifestRule, ScorecardPlanRule, validate_manifest, validate_scorecard_plan


class ValidateOfficialBenchmarkManifestTests(unittest.TestCase):
    def test_validate_manifest_accepts_required_and_rejects_forbidden(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "manifest.md"
            path.write_text("use bfcl generate and bfcl evaluate with --skip-server-setup\n", encoding="utf-8")
            rule = ManifestRule(
                rel_path=str(path),
                required=("bfcl generate", "bfcl evaluate", "--skip-server-setup"),
                forbidden=("python -m bfcl_eval",),
            )

            self.assertEqual(validate_manifest(rule), [])

            path.write_text("python -m bfcl_eval\n", encoding="utf-8")
            errors = validate_manifest(rule)
            self.assertTrue(any("missing required" in error for error in errors))
            self.assertTrue(any("stale/forbidden" in error for error in errors))

    def test_validate_scorecard_plan_requires_full_ssd_backed_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "plan.yaml"
            run_id = "run-full"
            path.write_text(
                "\n".join(
                    [
                        "run_id: run-full",
                        "suite: lm-eval-selected",
                        "status: planned",
                        "publish_boundary: internal-candidate",
                        "model: Qwen/Qwen3-4B-MLX-4bit",
                        "adapter: gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter",
                        "tasks:",
                        "  - arc_challenge",
                        "  - hellaswag",
                        "limit: null",
                        "artifact_root: /Volumes/PortableSSD/hermes-evals/standard-benchmarks",
                        "output_dir: /Volumes/PortableSSD/hermes-evals/standard-benchmarks/lm-eval/run-full",
                        "report: reports/benchmark/lm-eval/run-full.md",
                        "command: |",
                        "  python scripts/run_mlx_lm_eval.py --run-id run-full --tasks arc_challenge,hellaswag --output-dir \"$OUT\"",
                        "completion_criteria:",
                        "  - summary.json status is scored",
                        "  - results.json contains every selected task",
                        "  - coverage report no longer marks lm-eval-selected missing",
                        "blocked_public_claims_until_complete:",
                        "  - full selected-task lm-eval scorecard",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            rule = ScorecardPlanRule(rel_path=str(path), run_id=run_id, required_tasks=("arc_challenge", "hellaswag"))

            self.assertEqual(validate_scorecard_plan(rule), [])

            path.write_text(path.read_text(encoding="utf-8").replace("limit: null", "limit: 25"), encoding="utf-8")
            errors = validate_scorecard_plan(rule)
            self.assertTrue(any("limit: null" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
