import unittest

from gemma4.data.strict_tool_call.tools.materialize_safety_refusal_repair_splits_v10 import (
    FORBIDDEN_MARKER,
    TARGET_RESIDUAL_ID,
    customer_delete_rows,
    repair_rows,
    validate_v10_rows,
)


class Qwen3V10RepairDatasetTests(unittest.TestCase):
    def test_v10_rows_target_only_customer_delete_marker(self) -> None:
        rows = repair_rows()
        self.assertEqual(len(customer_delete_rows()), 4)
        self.assertEqual(len(rows), 8)
        self.assertEqual({row["repair_lane"] for row in rows}, {"customer-delete-marker-suppression"})
        targets = {target for row in rows for target in row["targets_residual_ids"]}
        self.assertEqual(targets, {TARGET_RESIDUAL_ID})
        validate_v10_rows(rows)

    def test_v10_refusals_do_not_echo_forbidden_marker(self) -> None:
        for row in customer_delete_rows():
            target = [msg for msg in row["messages"] if msg["role"] == "assistant"][-1]["content"]
            self.assertNotIn("<tool_call>", target)
            self.assertIn("cannot", target.lower())
            self.assertNotIn(FORBIDDEN_MARKER, target)


if __name__ == "__main__":
    unittest.main()
