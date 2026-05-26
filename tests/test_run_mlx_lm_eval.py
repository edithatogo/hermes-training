from __future__ import annotations

import unittest

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


if __name__ == "__main__":
    unittest.main()
