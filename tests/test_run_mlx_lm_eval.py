from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import run_mlx_lm_eval
from scripts.run_mlx_lm_eval import collect_task_metrics, continuation_token_ids, json_safe, render_report, token_ids, trim_until


class ToyTokenizer:
    def encode(self, text: str, add_special_tokens: bool = False) -> list[int]:
        del add_special_tokens
        return [ord(char) for char in text]


class NonPrefixTokenizer:
    def encode(self, text: str, add_special_tokens: bool = False) -> list[int]:
        del add_special_tokens
        if text == "hello world":
            return [1, 99, 3]
        if text == "hello":
            return [1, 2]
        if text == " world":
            return [3]
        return [ord(char) for char in text]


class RunMlxLmEvalTests(unittest.TestCase):
    def test_token_ids_disables_special_tokens(self) -> None:
        self.assertEqual(token_ids(ToyTokenizer(), "ab"), [97, 98])

    def test_continuation_token_ids_uses_full_prefix_when_stable(self) -> None:
        ids, start = continuation_token_ids(ToyTokenizer(), "ab", "c")

        self.assertEqual(ids, [97, 98, 99])
        self.assertEqual(start, 2)

    def test_continuation_token_ids_falls_back_when_token_boundary_merges(self) -> None:
        ids, start = continuation_token_ids(NonPrefixTokenizer(), "hello", " world")

        self.assertEqual(ids, [1, 2, 3])
        self.assertEqual(start, 2)

    def test_trim_until_removes_earliest_stop_sequence(self) -> None:
        self.assertEqual(trim_until("answer\n\nQuestion: next", ["Question:", "\n\n"]), "answer")

    def test_json_safe_stringifies_non_json_values(self) -> None:
        payload = {"fn": lambda: None, "nested": (1, object())}

        safe = json_safe(payload)

        self.assertIsInstance(safe["fn"], str)
        self.assertEqual(safe["nested"][0], 1)
        self.assertIsInstance(safe["nested"][1], str)

    def test_collect_task_metrics_ignores_stderr(self) -> None:
        metrics = collect_task_metrics(
            {
                "results": {
                    "arc": {
                        "acc,none": 1.0,
                        "acc_stderr,none": "N/A",
                        "sample_len": 1,
                    }
                }
            }
        )

        self.assertEqual(metrics, {"arc": {"acc,none": 1.0}})

    def test_render_report_includes_task_metrics(self) -> None:
        report = render_report(
            {
                "run_id": "run",
                "created_at": "now",
                "model": "model",
                "adapter": "adapter",
                "tasks": ["arc"],
                "limit": 1,
                "status": "scored",
                "output_dir": "/tmp/out",
                "load_latency_s": 1.0,
                "total_latency_s": 2.0,
                "task_metrics": {"arc": {"acc,none": 1.0}},
            }
        )

        self.assertIn("## Metrics", report)
        self.assertIn("acc,none", report)

    def test_render_report_shows_full_when_limit_is_none(self) -> None:
        report = render_report(
            {
                "run_id": "run",
                "created_at": "now",
                "model": "model",
                "adapter": "adapter",
                "tasks": ["arc"],
                "limit": None,
                "status": "scored",
                "output_dir": "/tmp/out",
                "load_latency_s": 1.0,
                "total_latency_s": 2.0,
            }
        )

        self.assertIn("Limit: `full`", report)

    def test_main_runs_full_mode_incrementally_and_flushes_after_each_task(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "out"
            report_path = Path(tmpdir) / "report.md"
            calls: list[dict[str, object]] = []

            class FakeAdapter:
                def __init__(self, model_name: str, adapter_path: str | None, max_length: int) -> None:
                    self.model_name = model_name
                    self.adapter_path = adapter_path or ""
                    self.max_length = max_length
                    self.load_latency_s = 0.125

            def simple_evaluate(*, model, tasks, limit, batch_size, bootstrap_iters, log_samples, verbosity):
                call_index = len(calls) + 1
                task = tasks[0]
                summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))
                report = report_path.read_text(encoding="utf-8")
                results = json.loads((output_dir / "results.json").read_text(encoding="utf-8"))
                if call_index == 1:
                    self.assertEqual(summary["status"], "running")
                    self.assertEqual(summary["completed_tasks"], [])
                    self.assertEqual(summary["pending_tasks"], ["arc_challenge", "hellaswag"])
                    self.assertEqual(summary["current_task"], "arc_challenge")
                    self.assertIn("Current task | `arc_challenge`", report)
                    self.assertIn("Completed tasks | `0/2`", report)
                    self.assertEqual(results["task_order"], [])
                    self.assertEqual(results["results"], {})
                calls.append(
                    {
                        "model": model,
                        "tasks": list(tasks),
                        "limit": limit,
                        "batch_size": batch_size,
                        "bootstrap_iters": bootstrap_iters,
                        "log_samples": log_samples,
                        "verbosity": verbosity,
                    }
                )
                if call_index == 2:
                    self.assertEqual(summary["status"], "running")
                    self.assertEqual(summary["completed_tasks"], ["arc_challenge"])
                    self.assertEqual(summary["pending_tasks"], ["hellaswag"])
                    self.assertEqual(summary["current_task"], "hellaswag")
                    self.assertIn("Current task | `hellaswag`", report)
                    self.assertIn("Completed tasks | `1/2`", report)
                    self.assertEqual(results["task_order"], ["arc_challenge"])
                    self.assertEqual(sorted(results["results"]), ["arc_challenge"])

                return {"results": {task: {"acc,none": float(call_index), "acc_stderr,none": 0.0}}}

            fake_lm_eval = types.ModuleType("lm_eval")
            fake_evaluator = types.ModuleType("lm_eval.evaluator")
            fake_evaluator.simple_evaluate = simple_evaluate
            fake_lm_eval.evaluator = fake_evaluator

            argv = [
                "run_mlx_lm_eval.py",
                "--tasks",
                "arc_challenge,hellaswag",
                "--batch-size",
                "1",
                "--output-dir",
                str(output_dir),
                "--report",
                str(report_path),
            ]
            with patch.object(run_mlx_lm_eval, "MlxLmEvalAdapter", FakeAdapter), patch.dict(
                sys.modules,
                {"lm_eval": fake_lm_eval, "lm_eval.evaluator": fake_evaluator},
            ), patch.object(sys, "argv", argv), contextlib.redirect_stdout(io.StringIO()):
                exit_code = run_mlx_lm_eval.main()

            self.assertEqual(exit_code, 0)
            self.assertEqual([call["tasks"] for call in calls], [["arc_challenge"], ["hellaswag"]])
            self.assertEqual([call["limit"] for call in calls], [None, None])
            self.assertEqual([call["log_samples"] for call in calls], [False, False])

            summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))
            report = report_path.read_text(encoding="utf-8")
            results = json.loads((output_dir / "results.json").read_text(encoding="utf-8"))

            self.assertEqual(summary["status"], "scored")
            self.assertEqual(summary["completed_tasks"], ["arc_challenge", "hellaswag"])
            self.assertEqual(summary["pending_tasks"], [])
            self.assertNotIn("current_task", summary)
            self.assertIn("Limit: `full`", report)
            self.assertIn("Completed tasks | `2/2`", report)
            self.assertEqual(results["task_order"], ["arc_challenge", "hellaswag"])
            self.assertEqual(sorted(results["results"]), ["arc_challenge", "hellaswag"])
            self.assertEqual(sorted(results["task_runs"]), ["arc_challenge", "hellaswag"])

    def test_main_keeps_limit_smoke_batch_behavior(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "out"
            report_path = Path(tmpdir) / "report.md"
            calls: list[dict[str, object]] = []

            class FakeAdapter:
                def __init__(self, model_name: str, adapter_path: str | None, max_length: int) -> None:
                    self.model_name = model_name
                    self.adapter_path = adapter_path or ""
                    self.max_length = max_length
                    self.load_latency_s = 0.25

            def simple_evaluate(*, model, tasks, limit, batch_size, bootstrap_iters, log_samples, verbosity):
                calls.append(
                    {
                        "tasks": list(tasks),
                        "limit": limit,
                        "batch_size": batch_size,
                        "bootstrap_iters": bootstrap_iters,
                        "log_samples": log_samples,
                        "verbosity": verbosity,
                    }
                )
                return {"results": {tasks[0]: {"acc,none": 1.0, "acc_stderr,none": 0.0}}}

            fake_lm_eval = types.ModuleType("lm_eval")
            fake_evaluator = types.ModuleType("lm_eval.evaluator")
            fake_evaluator.simple_evaluate = simple_evaluate
            fake_lm_eval.evaluator = fake_evaluator

            argv = [
                "run_mlx_lm_eval.py",
                "--tasks",
                "arc_challenge,hellaswag",
                "--limit",
                "1",
                "--batch-size",
                "1",
                "--output-dir",
                str(output_dir),
                "--report",
                str(report_path),
            ]
            with patch.object(run_mlx_lm_eval, "MlxLmEvalAdapter", FakeAdapter), patch.dict(
                sys.modules,
                {"lm_eval": fake_lm_eval, "lm_eval.evaluator": fake_evaluator},
            ), patch.object(sys, "argv", argv), contextlib.redirect_stdout(io.StringIO()):
                exit_code = run_mlx_lm_eval.main()

            self.assertEqual(exit_code, 0)
            self.assertEqual(len(calls), 1)
            self.assertEqual(calls[0]["tasks"], ["arc_challenge", "hellaswag"])
            self.assertEqual(calls[0]["limit"], 1)
            self.assertTrue(calls[0]["log_samples"])
            summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))
            self.assertEqual(summary["status"], "scored")
            self.assertEqual(summary["limit"], 1)

    def test_render_report_includes_completed_tasks(self) -> None:
        report = render_report(
            {
                "run_id": "run",
                "created_at": "now",
                "model": "model",
                "adapter": "adapter",
                "tasks": ["arc", "gsm8k"],
                "limit": None,
                "status": "running",
                "output_dir": "/tmp/out",
                "load_latency_s": 1.0,
                "total_latency_s": 2.0,
                "completed_tasks": ["arc"],
                "pending_tasks": ["gsm8k"],
                "current_task": "gsm8k",
            }
        )

        self.assertIn("Completed tasks | `1/2`", report)
        self.assertIn("Current task | `gsm8k`", report)
        self.assertIn("Pending tasks | `gsm8k`", report)


if __name__ == "__main__":
    unittest.main()
