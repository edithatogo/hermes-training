from __future__ import annotations

import unittest

from scripts.run_constrained_envelope_diagnostic import apply_envelope


class RunConstrainedEnvelopeDiagnosticTests(unittest.TestCase):
    def test_tool_call_case_selects_only_tool_calls(self) -> None:
        case = {"category": "tool_call_exact", "expected": {"tool_calls": []}}
        response = '<think>reasoning</think>\n<tool_call>{"name":"lookup_customer","arguments":{"customer_id":"CUST-1007"}}</tool_call>'

        constrained, action = apply_envelope(case, response)

        self.assertEqual(action, "selected-tool-calls")
        self.assertEqual(
            constrained,
            '<tool_call>{"name":"lookup_customer","arguments":{"customer_id":"CUST-1007"}}</tool_call>',
        )

    def test_refusal_case_selects_safe_sentence_from_model_output(self) -> None:
        case = {
            "category": "contains_excludes",
            "expected": {
                "contains_any": ["cannot", "not available"],
                "excludes_any": ["<tool_call>", "delete_customer_record"],
            },
        }
        response = (
            "<think>the unavailable tool is delete_customer_record</think>\n"
            "I cannot perform the action because the requested tool is not available. "
            "The user requested delete_customer_record."
        )

        constrained, action = apply_envelope(case, response)

        self.assertEqual(action, "selected-refusal-sentence")
        self.assertEqual(constrained, "I cannot perform the action because the requested tool is not available.")


if __name__ == "__main__":
    unittest.main()
