from __future__ import annotations

import contextlib
import io
import unittest
from unittest.mock import patch

from scripts.run_mlx_lm_eval import continuation_token_ids, main, run_self_test


class ToyTokenizer:
    def encode(self, text: str, add_special_tokens: bool = False) -> list[int]:
        del add_special_tokens
        return [ord(char) % 17 for char in text]


class RunMlxLmEvalTests(unittest.TestCase):
    def test_continuation_token_ids_preserves_context_prefix(self) -> None:
        ids, start = continuation_token_ids(ToyTokenizer(), "ab", "c")

        self.assertEqual(start, 2)
        self.assertEqual(len(ids), 3)

    def test_self_test_passes(self) -> None:
        run_self_test()

    def test_dry_run_prints_target_paths(self) -> None:
        argv = ["run_mlx_lm_eval.py", "--dry-run", "--run-id", "dry-test", "--tasks", "arc_challenge"]
        stdout = io.StringIO()
        with patch("sys.argv", argv), contextlib.redirect_stdout(stdout):
            self.assertEqual(main(), 0)

        self.assertIn("arc_challenge", stdout.getvalue())
        self.assertIn("dry-test", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
