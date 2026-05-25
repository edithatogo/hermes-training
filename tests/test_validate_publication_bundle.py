from __future__ import annotations

import json
import tempfile
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.validate_publication_bundle import (
    DEFAULT_REQUIRED_FILES,
    PUBLIC_RELEASE_GATES,
    STANDARD_BENCHMARK_GATE,
    evaluate_bundle,
)


def write_bundle(
    root: Path,
    checked_public_gates: set[str],
    include_required: bool = True,
    model_card_text: str = "# hf-model-card-draft.md\n",
) -> None:
    if include_required:
        for rel in DEFAULT_REQUIRED_FILES:
            path = root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            if path.suffix == ".json":
                path.write_text("{}\n", encoding="utf-8")
            elif rel == "hf-model-card-draft.md":
                path.write_text(model_card_text, encoding="utf-8")
            elif rel != "publish-readiness-checklist.md":
                path.write_text(f"# {rel}\n", encoding="utf-8")

    lines = [
        "# Publish Readiness",
        "",
        "- [x] Held-out strict local tool-call suite passes at `1.000`.",
        "- [x] Mirrored regression suite passes at `1.000`.",
        "- [x] Runtime condition recorded: `/no_think` plus assistant prefill.",
    ]
    for gate in PUBLIC_RELEASE_GATES:
        mark = "x" if gate in checked_public_gates else " "
        lines.append(f"- [{mark}] {gate}")
    (root / "publish-readiness-checklist.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_coverage_report(root: Path) -> Path:
    path = root / "coverage.json"
    path.write_text(
        json.dumps(
            {
                "items": [
                    {"suite": "official-bfcl", "tier": "official-candidate", "status": "missing"},
                    {"suite": "lm-eval-selected", "tier": "official-candidate", "status": "blocked"},
                    {"suite": "official-coding", "tier": "official-candidate", "status": "missing"},
                    {"suite": "safety-refusal", "tier": "official-candidate", "status": "missing"},
                    {"suite": "ruler-long-context", "tier": "official-candidate", "status": "missing"},
                ]
            }
        )
        + "\n",
        encoding="utf-8",
    )
    return path


VALID_MODEL_CARD = """# Model Card

Benchmark support is pilot-only.

This release does not include official BFCL, HumanEval, MBPP, EvalPlus,
BigCodeBench, LiveCodeBench, safety/refusal, or RULER long-context scores.
The selected lm-eval smoke was attempted but is not loglikelihood-compatible,
so no lm-eval score is claimed.
"""


class PublicationBundleTests(unittest.TestCase):
    def test_blocked_bundle_is_valid_but_not_public_ready(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_bundle(root, checked_public_gates=set())

            status = evaluate_bundle(root)

            self.assertEqual(status.status, "blocked")
            self.assertTrue(status.local_quality_ready)
            self.assertFalse(status.public_ready)
            self.assertEqual(set(status.unchecked_public_release_gates), set(PUBLIC_RELEASE_GATES))

    def test_ready_bundle_requires_public_release_gates_and_benchmark_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            coverage = write_coverage_report(root)
            write_bundle(root, checked_public_gates=set(PUBLIC_RELEASE_GATES), model_card_text=VALID_MODEL_CARD)

            status = evaluate_bundle(root, coverage_report=coverage)

            self.assertEqual(status.status, "ready")
            self.assertTrue(status.local_quality_ready)
            self.assertTrue(status.public_ready)

    def test_checked_standard_benchmark_gate_requires_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_bundle(root, checked_public_gates={STANDARD_BENCHMARK_GATE})

            status = evaluate_bundle(root, coverage_report=root / "missing-coverage.json")

            self.assertEqual(status.status, "invalid")
            self.assertTrue(status.benchmark_evidence_errors)

    def test_checked_standard_benchmark_gate_requires_model_card_exclusions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            coverage = write_coverage_report(root)
            write_bundle(root, checked_public_gates={STANDARD_BENCHMARK_GATE})

            status = evaluate_bundle(root, coverage_report=coverage)

            self.assertEqual(status.status, "invalid")
            self.assertIn("official-bfcl", "\n".join(status.benchmark_evidence_errors))

    def test_missing_required_file_is_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_bundle(root, checked_public_gates=set(), include_required=True)
            (root / "release-decision.md").unlink()

            status = evaluate_bundle(root)

            self.assertEqual(status.status, "invalid")
            self.assertIn("release-decision.md", status.missing_files)


if __name__ == "__main__":
    unittest.main()
