from __future__ import annotations

import tempfile
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.validate_publication_bundle import (
    DEFAULT_REQUIRED_FILES,
    PUBLIC_RELEASE_GATES,
    evaluate_bundle,
)


def write_bundle(root: Path, checked_public_gates: set[str], include_required: bool = True) -> None:
    if include_required:
        for rel in DEFAULT_REQUIRED_FILES:
            path = root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            if path.suffix == ".json":
                path.write_text("{}\n", encoding="utf-8")
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

    def test_ready_bundle_requires_public_release_gates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_bundle(root, checked_public_gates=set(PUBLIC_RELEASE_GATES))

            status = evaluate_bundle(root)

            self.assertEqual(status.status, "ready")
            self.assertTrue(status.local_quality_ready)
            self.assertTrue(status.public_ready)

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
