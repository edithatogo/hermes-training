import json
import tempfile
import unittest
from pathlib import Path

from scripts.generate_humaneval_mlx_solutions import (
    build_prompt,
    clean_completion,
    load_existing_task_ids,
    ordered_problem_items,
)


class GenerateHumanEvalMlxSolutionsTests(unittest.TestCase):
    def test_orders_humaneval_tasks_numerically(self) -> None:
        problems = {"HumanEval/10": {}, "HumanEval/2": {}, "HumanEval/1": {}}
        self.assertEqual([task_id for task_id, _ in ordered_problem_items(problems)], ["HumanEval/1", "HumanEval/2", "HumanEval/10"])

    def test_build_prompt_preserves_problem_prefix(self) -> None:
        prompt = build_prompt({"prompt": "def add(a, b):\n    \"\"\"Return sum.\"\"\""})
        self.assertTrue(prompt.startswith("def add"))
        self.assertIn("Return only the code", prompt)

    def test_clean_completion_removes_markdown_fence(self) -> None:
        self.assertEqual(clean_completion("```python\n    return a + b\n```\n"), "    return a + b\n")

    def test_load_existing_task_ids_reads_jsonl(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "generated.jsonl"
            path.write_text(json.dumps({"task_id": "HumanEval/0", "completion": "pass"}) + "\n", encoding="utf-8")
            self.assertEqual(load_existing_task_ids(path), {"HumanEval/0"})


if __name__ == "__main__":
    unittest.main()
