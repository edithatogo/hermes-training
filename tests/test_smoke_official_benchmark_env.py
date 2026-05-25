from __future__ import annotations

import unittest

from scripts.smoke_official_benchmark_env import MODES, package_versions


class OfficialBenchmarkEnvSmokeTests(unittest.TestCase):
    def test_modes_cover_general_and_bfcl(self) -> None:
        self.assertIn("general", MODES)
        self.assertIn("bfcl", MODES)
        self.assertIn("lm_eval", MODES["general"]["imports"])
        self.assertIn("bfcl_eval", MODES["bfcl"]["imports"])

    def test_package_versions_reports_missing_without_raising(self) -> None:
        versions = package_versions(("definitely-not-installed-hermes-package",))

        self.assertEqual(versions["definitely-not-installed-hermes-package"], "missing")


if __name__ == "__main__":
    unittest.main()
