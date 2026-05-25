import unittest

from scripts.create_mem0_run_card import decision_for


class CreateMem0RunCardTests(unittest.TestCase):
    def test_extraction_pass_gate_gets_positive_decision_reason(self) -> None:
        decision, reason = decision_for(
            "extraction",
            {
                "pass_rate": 1.0,
                "json_validity_rate": 1.0,
                "forbidden_hit_rate": 0.0,
                "empty_case_pass_rate": 1.0,
            },
        )

        self.assertEqual(decision, "keep testing")
        self.assertIn("passed the strict JSON", reason)
        self.assertNotIn("did not reach", reason)

    def test_extraction_failure_keeps_fail_closed_reason(self) -> None:
        decision, reason = decision_for(
            "extraction",
            {
                "pass_rate": 0.9,
                "json_validity_rate": 1.0,
                "forbidden_hit_rate": 0.0,
                "empty_case_pass_rate": 1.0,
            },
        )

        self.assertEqual(decision, "keep testing")
        self.assertIn("did not reach", reason)


if __name__ == "__main__":
    unittest.main()
