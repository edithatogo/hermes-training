from __future__ import annotations

import contextlib
import io
import json
import math
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.run_mlx_loglikelihood_smoke import (
    LoglikelihoodCase,
    continuation_span,
    main,
    parse_cases,
    uniform_mock_score,
)


class SimpleTokenizer:
    def encode(self, text: str, *_args: object, **_kwargs: object) -> list[int]:
        return list(range(1, len(text.split()) + 1))


class RunMlxLoglikelihoodSmokeTests(unittest.TestCase):
    def test_parse_cases_requires_prompt_and_continuation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            suite = Path(tmp) / "suite.jsonl"
            suite.write_text('{"id":"a","prompt":"A","continuation":" B"}\n', encoding="utf-8")

            cases = parse_cases(suite)

        self.assertEqual(cases, [LoglikelihoodCase("a", "A", " B")])

    def test_continuation_span_uses_full_prompt_continuation_tokens(self) -> None:
        full_ids, start = continuation_span(SimpleTokenizer(), "The answer is", " yes")

        self.assertEqual(start, 3)
        self.assertEqual(len(full_ids), 4)

    def test_uniform_mock_score_is_deterministic(self) -> None:
        row = uniform_mock_score(LoglikelihoodCase("a", "The answer is", " yes"), SimpleTokenizer(), 100)

        self.assertEqual(row["continuation_tokens"], 1)
        self.assertAlmostEqual(row["loglikelihood"], -math.log(100))
        self.assertEqual(row["mode"], "mock-uniform")

    def test_main_mock_uniform_writes_schema(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            suite = root / "suite.jsonl"
            output_root = root / "out"
            suite.write_text('{"id":"a","prompt":"A","continuation":" B"}\n', encoding="utf-8")
            argv = [
                "run_mlx_loglikelihood_smoke.py",
                "--suite",
                str(suite),
                "--output-root",
                str(output_root),
                "--run-id",
                "mock-run",
                "--mock-uniform",
            ]
            with patch("sys.argv", argv), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main(), 0)

            summary = json.loads((output_root / "mock-run" / "summary.json").read_text(encoding="utf-8"))

        self.assertEqual(summary["run_id"], "mock-run")
        self.assertEqual(summary["mode"], "mock-uniform")
        self.assertEqual(summary["cases"], 1)


if __name__ == "__main__":
    unittest.main()
