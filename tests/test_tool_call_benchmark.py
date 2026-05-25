from __future__ import annotations

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from scripts.run_tool_call_benchmark import apply_user_prefix, build_generation_prompt


class ToolCallBenchmarkTests(unittest.TestCase):
    def test_user_prefix_applies_to_first_user_turn_only(self) -> None:
        messages = [
            {"role": "system", "content": "system"},
            {"role": "user", "content": "first"},
            {"role": "user", "content": "second"},
        ]

        updated = apply_user_prefix(messages, "/no_think")

        self.assertEqual(updated[1]["content"], "/no_think first")
        self.assertEqual(updated[2]["content"], "second")
        self.assertEqual(messages[1]["content"], "first")

    def test_assistant_prefill_appends_to_generation_prompt(self) -> None:
        messages = [{"role": "user", "content": "Return a tool call."}]

        prompt = build_generation_prompt(messages, None, "<tool_call>\n")

        self.assertTrue(prompt.endswith("ASSISTANT:<tool_call>\n"))


if __name__ == "__main__":
    unittest.main()
