import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts.build_official_candidate_execution_matrix import build_matrix, render_markdown
from scripts.validate_official_candidate_execution_matrix import validate_payload


class OfficialCandidateExecutionMatrixTests(unittest.TestCase):
    def write_queue(self, root: Path) -> Path:
        items = []
        for suite, output in (
            ("official-bfcl", "bfcl/qwen3-v4-peft-official-bfcl-20260616"),
            ("official-coding", "coding/qwen3-v4-peft-official-coding-20260616"),
            ("safety-refusal", "safety/qwen3-v4-peft-safety-refusal-20260616"),
            ("ruler-long-context", "ruler/qwen3-v4-peft-ruler-long-context-20260616"),
        ):
            items.append(
                {
                    "suite": suite,
                    "status": "missing",
                    "run_id": f"qwen3-v4-peft-{suite}-20260616",
                    "output_root": f"/Volumes/PortableSSD/hermes-evals/standard-benchmarks/{output}",
                    "local_command": f"run {suite}",
                    "next_action": f"next {suite}",
                }
            )
        path = root / "queue.json"
        path.write_text(
            json.dumps(
                {
                    "candidate": "qwen3-4b-strict-toolcall-v4-targeted",
                    "adapter": "adapter/path",
                    "items": items,
                }
            ),
            encoding="utf-8",
        )
        return path

    @mock.patch("scripts.build_official_candidate_execution_matrix.PREFLIGHTS", {})
    @mock.patch("scripts.build_official_candidate_execution_matrix.RUNTIME_ATTEMPTS", {})
    @mock.patch("scripts.build_official_candidate_execution_matrix.SAFETY_SUMMARY")
    @mock.patch("scripts.build_official_candidate_execution_matrix.SAFETY_MANIFEST")
    def test_matrix_records_blocked_and_ready_suites(
        self,
        mocked_safety_manifest: mock.Mock,
        mocked_safety_summary: mock.Mock,
    ) -> None:
        mocked_safety_summary.exists.return_value = False
        mocked_safety_manifest.exists.return_value = True
        with tempfile.TemporaryDirectory() as tmp:
            matrix = build_matrix(self.write_queue(Path(tmp)))
        rows = {row["suite"]: row for row in matrix["rows"]}
        self.assertEqual(rows["official-bfcl"]["execution_status"], "blocked-preflight")
        self.assertEqual(rows["official-coding"]["execution_status"], "blocked-preflight")
        self.assertEqual(rows["safety-refusal"]["execution_status"], "ready-for-runtime")
        self.assertEqual(rows["ruler-long-context"]["execution_status"], "blocked-preflight")
        self.assertIn("safety-refusal should record the scored artifact", "\n".join(validate_payload(matrix, Path("matrix.json"))))

    @mock.patch("scripts.build_official_candidate_execution_matrix.PREFLIGHTS", {})
    @mock.patch("scripts.build_official_candidate_execution_matrix.RUNTIME_ATTEMPTS", {})
    @mock.patch("scripts.build_official_candidate_execution_matrix.SAFETY_SUMMARY")
    def test_matrix_records_scored_safety_artifact(self, mocked_safety_summary: mock.Mock) -> None:
        mocked_safety_summary.exists.return_value = True
        mocked_safety_summary.read_text.return_value = json.dumps({"pass_rate": 0.125})
        with tempfile.TemporaryDirectory() as tmp:
            matrix = build_matrix(self.write_queue(Path(tmp)))
        rows = {row["suite"]: row for row in matrix["rows"]}
        self.assertEqual(rows["safety-refusal"]["execution_status"], "scored-artifact-present")
        self.assertIn("strict pass rate is 0.125", rows["safety-refusal"]["blocker"])
        self.assertEqual(validate_payload(matrix, Path("matrix.json")), [])

    @mock.patch("scripts.build_official_candidate_execution_matrix.SAFETY_SUMMARY")
    def test_matrix_records_ruler_runtime_attempt_blocker(
        self,
        mocked_safety_summary: mock.Mock,
    ) -> None:
        mocked_safety_summary.exists.return_value = True
        mocked_safety_summary.read_text.return_value = json.dumps({"pass_rate": 0.125})
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            preflight_path = root / "ruler-preflight.json"
            preflight_path.write_text(json.dumps({"status": "ready-to-run", "blockers": []}), encoding="utf-8")
            attempt_path = root / "ruler-runtime-attempt.json"
            attempt_path.write_text(
                json.dumps(
                    {
                        "status": "blocked-runtime",
                        "blocker": "HF/Xet model acquisition stalled",
                        "next_action": "Move Hugging Face caches to the SSD and prefetch before retry.",
                    }
                ),
                encoding="utf-8",
            )
            with (
                mock.patch(
                    "scripts.build_official_candidate_execution_matrix.PREFLIGHTS",
                    {"ruler-long-context": preflight_path},
                ),
                mock.patch(
                    "scripts.build_official_candidate_execution_matrix.RUNTIME_ATTEMPTS",
                    {"ruler-long-context": attempt_path},
                ),
            ):
                matrix = build_matrix(self.write_queue(root))
        rows = {row["suite"]: row for row in matrix["rows"]}
        self.assertEqual(rows["ruler-long-context"]["execution_status"], "blocked-runtime")
        self.assertIn("HF/Xet model acquisition", rows["ruler-long-context"]["blocker"])
        self.assertIn("SSD", rows["ruler-long-context"]["next_action"])

    @mock.patch("scripts.build_official_candidate_execution_matrix.PREFLIGHTS", {})
    @mock.patch("scripts.build_official_candidate_execution_matrix.RUNTIME_ATTEMPTS", {})
    @mock.patch("scripts.build_official_candidate_execution_matrix.SAFETY_SUMMARY")
    @mock.patch("scripts.build_official_candidate_execution_matrix.SAFETY_MANIFEST")
    def test_markdown_preserves_claim_boundary(
        self,
        mocked_safety_manifest: mock.Mock,
        mocked_safety_summary: mock.Mock,
    ) -> None:
        mocked_safety_summary.exists.return_value = False
        mocked_safety_manifest.exists.return_value = True
        with tempfile.TemporaryDirectory() as tmp:
            markdown = render_markdown(build_matrix(self.write_queue(Path(tmp))))
        self.assertIn("No public broad benchmark claim", markdown)
        self.assertIn("official-bfcl", markdown)
        self.assertIn("safety-refusal", markdown)


if __name__ == "__main__":
    unittest.main()
