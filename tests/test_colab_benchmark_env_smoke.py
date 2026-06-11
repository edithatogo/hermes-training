from __future__ import annotations

import unittest
from unittest import mock

from scripts.colab_benchmark_env_smoke import INSTALL_PROFILES, install_profile


class ColabBenchmarkEnvSmokeTests(unittest.TestCase):
    def test_general_profile_includes_lm_eval(self) -> None:
        self.assertIn("lm_eval", INSTALL_PROFILES["general-core"])
        self.assertIn("sentence-transformers", INSTALL_PROFILES["general-core"])

    def test_none_profile_skips_install(self) -> None:
        result = install_profile("none", timeout_s=1)

        self.assertEqual(result["returncode"], 0)
        self.assertTrue(result["skipped"])
        self.assertEqual(result["packages"], [])

    def test_install_profile_uses_current_interpreter(self) -> None:
        with mock.patch("scripts.colab_benchmark_env_smoke.run_command") as run_command:
            run_command.return_value = {"returncode": 0}

            result = install_profile("bfcl-core", timeout_s=123)

        self.assertEqual(result["returncode"], 0)
        command = run_command.call_args.args[0]
        self.assertIn("-m", command)
        self.assertIn("pip", command)
        self.assertIn("bfcl-eval", command)
        self.assertEqual(run_command.call_args.kwargs["timeout_s"], 123)


if __name__ == "__main__":
    unittest.main()
