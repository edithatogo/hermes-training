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
    @mock.patch("scripts.build_official_candidate_execution_matrix.SAFETY_MANIFEST")
    def test_matrix_records_blocked_and_ready_suites(self, mocked_safety_manifest: mock.Mock) -> None:
        mocked_safety_manifest.exists.return_value = True
        with tempfile.TemporaryDirectory() as tmp:
            matrix = build_matrix(self.write_queue(Path(tmp)))
        rows = {row["suite"]: row for row in matrix["rows"]}
        self.assertEqual(rows["official-bfcl"]["execution_status"], "blocked-preflight")
        self.assertEqual(rows["official-coding"]["execution_status"], "blocked-preflight")
        self.assertEqual(rows["safety-refusal"]["execution_status"], "ready-for-runtime")
        self.assertEqual(rows["ruler-long-context"]["execution_status"], "blocked-preflight")
        self.assertEqual(validate_payload(matrix, Path("matrix.json")), [])

    @mock.patch("scripts.build_official_candidate_execution_matrix.PREFLIGHTS", {})
    @mock.patch("scripts.build_official_candidate_execution_matrix.SAFETY_MANIFEST")
    def test_markdown_preserves_claim_boundary(self, mocked_safety_manifest: mock.Mock) -> None:
        mocked_safety_manifest.exists.return_value = True
        with tempfile.TemporaryDirectory() as tmp:
            markdown = render_markdown(build_matrix(self.write_queue(Path(tmp))))
        self.assertIn("No public broad benchmark claim", markdown)
        self.assertIn("official-bfcl", markdown)
        self.assertIn("safety-refusal", markdown)


if __name__ == "__main__":
    unittest.main()
