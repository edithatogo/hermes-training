import unittest

from gemma4.data.strict_tool_call.tools.materialize_safety_refusal_repair_splits_v7 import (
    refusal_rows,
    repair_rows,
    strict_wrapper_rows,
    validate_rows,
)
from gemma4.data.strict_tool_call.tools.materialize_safety_refusal_repair_splits_v8 import (
    exact_free_text_copy_rows,
    repair_rows as v8_repair_rows,
    security_refusal_rows,
    validate_rows as validate_v8_rows,
    wrapper_removal_rows,
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

    def test_v8_repair_rows_have_expected_lanes(self) -> None:
        rows = v8_repair_rows()
        self.assertEqual(len(wrapper_removal_rows()), 2)
        self.assertEqual(len(exact_free_text_copy_rows()), 3)
        self.assertEqual(len(security_refusal_rows()), 4)
        self.assertEqual(len(rows), 18)
        lanes = {row["repair_lane"] for row in rows}
        self.assertEqual(
            lanes,
            {
                "strict-empty-think-wrapper-removal",
                "exact-free-text-argument-copying",
                "security-exfiltration-contrastive-refusal",
            },
        )
        validate_v8_rows(rows)

    def test_v8_security_refusals_do_not_echo_forbidden_markers(self) -> None:
        for row in security_refusal_rows():
            target = [msg for msg in row["messages"] if msg["role"] == "assistant"][-1]["content"]
            self.assertNotIn("<tool_call>", target)
            self.assertIn("cannot", target.lower())
            for marker in row["forbidden_markers"]:
                self.assertNotIn(marker.lower(), target.lower())

    def test_v8_exact_free_text_copy_preserves_note_argument(self) -> None:
        row = next(row for row in exact_free_text_copy_rows() if row["id"] == "exp-v8-copy-002-free-text-note")
        target = [msg for msg in row["messages"] if msg["role"] == "assistant"][-1]["content"]
        self.assertIn("Patient asked: can we move review to Friday?", target)


if __name__ == "__main__":
    unittest.main()
