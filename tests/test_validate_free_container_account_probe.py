from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.validate_free_container_account_probe import validate_report


VALID_REPORT = """# Free Container Account Probe - 2026-06-13

This probe checked candidate free-tier or credit-backed container backends
without launching jobs, creating resources, uploading artifacts, or using paid
compute.

## Modal

- Auth state: authenticated.
- Remaining gates:
  - confirm free credits.

## Kaggle

- Auth state: authenticated.
- GPU quota is visible.

## Lightning AI

- Blocker: Teamspace owner error.

## Current Decision

Kaggle is prepared, Modal still needs credit proof, and Lightning needs a
Teamspace owner.
"""


class ValidateFreeContainerAccountProbeTests(unittest.TestCase):
    def test_valid_probe_report_passes(self) -> None:
        with TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "probe.md"
            path.write_text(VALID_REPORT, encoding="utf-8")

            self.assertEqual(validate_report(path), [])

    def test_missing_boundary_and_secret_are_rejected(self) -> None:
        with TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "probe.md"
            path.write_text(VALID_REPORT.replace("without launching jobs, creating resources, uploading artifacts, or using paid\ncompute.", "") + "\nHF_TOKEN=secret\n", encoding="utf-8")

            failures = validate_report(path)

        self.assertTrue(any("without launching jobs" in failure for failure in failures))
        self.assertTrue(any("HF_TOKEN=" in failure for failure in failures))


if __name__ == "__main__":
    unittest.main()
