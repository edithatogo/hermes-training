import unittest

from gemma4.data.strict_tool_call.tools.materialize_safety_refusal_repair_splits_v9 import (
    TARGET_RESIDUAL_IDS,
    repair_rows,
    residual_refusal_marker_rows,
    validate_v9_rows,
)


class Qwen3V9RepairDatasetTests(unittest.TestCase):
    def test_v9_rows_target_only_residual_refusal_markers(self) -> None:
        rows = repair_rows()
        self.assertEqual(len(residual_refusal_marker_rows()), 2)
        self.assertEqual(len(rows), 4)
        self.assertEqual({row["repair_lane"] for row in rows}, {"residual-refusal-marker-suppression"})
        targets = {target for row in rows for target in row["targets_residual_ids"]}
        self.assertEqual(targets, set(TARGET_RESIDUAL_IDS))
        validate_v9_rows(rows)

    def test_v9_refusals_do_not_echo_forbidden_markers(self) -> None:
        for row in residual_refusal_marker_rows():
            target = [msg for msg in row["messages"] if msg["role"] == "assistant"][-1]["content"]
            self.assertNotIn("<tool_call>", target)
            self.assertIn("cannot", target.lower())
            for marker in row["forbidden_markers"]:
                self.assertNotIn(marker.lower(), target.lower())


if __name__ == "__main__":
    unittest.main()
