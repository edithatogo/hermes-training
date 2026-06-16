import unittest

from gemma4.data.strict_tool_call.tools.materialize_safety_refusal_repair_splits_v7 import (
    refusal_rows,
    repair_rows,
    strict_wrapper_rows,
    validate_rows,
)


class SafetyRefusalRepairDatasetTests(unittest.TestCase):
    def test_repair_rows_have_expected_lanes(self) -> None:
        rows = repair_rows()
        self.assertEqual(len(strict_wrapper_rows()), 3)
        self.assertEqual(len(refusal_rows()), 4)
        self.assertEqual(len(rows), 14)
        lanes = {row["repair_lane"] for row in rows}
        self.assertEqual(lanes, {"strict-empty-think-wrapper-removal", "refusal-forbidden-name-suppression"})
        validate_rows(rows)

    def test_refusal_targets_do_not_echo_forbidden_markers(self) -> None:
        for row in refusal_rows():
            target = [msg for msg in row["messages"] if msg["role"] == "assistant"][-1]["content"]
            self.assertNotIn("<tool_call>", target)
            for marker in row["forbidden_markers"]:
                self.assertNotIn(marker.lower(), target.lower())


if __name__ == "__main__":
    unittest.main()
