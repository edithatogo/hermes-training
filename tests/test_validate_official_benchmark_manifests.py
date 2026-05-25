from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.validate_official_benchmark_manifests import ManifestRule, validate_manifest


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


if __name__ == "__main__":
    unittest.main()
