from __future__ import annotations

import unittest

from scripts.run_constrained_envelope_diagnostic import apply_envelope, score_enveloped_case, scorer_for_suite


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

    def test_heldout_tool_call_case_uses_tool_call_scorer(self) -> None:
        case = {
            "id": "heldout-json-validity-inventory",
            "category": "json_validity",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        'Return only tool calls. <tools>[{"type":"function","function":'
                        '{"name":"check_inventory_level","parameters":{"type":"object","properties":{},'
                        '"required":[]}}}]</tools>'
                    ),
                }
            ],
            "expected": {
                "mode": "tool_calls",
                "tool_calls": [
                    {
                        "name": "check_inventory_level",
                        "arguments": {"sku": "GLV-884", "warehouse_id": "WH-SYD-02"},
                    }
                ],
            },
        }
        response = (
            '<think>reasoning</think><tool_call>{"name":"check_inventory_level",'
            '"arguments":{"sku":"GLV-884","warehouse_id":"WH-SYD-02"}}</tool_call>'
        )

        constrained, action = apply_envelope(case, response)
        scored = score_enveloped_case(case, constrained, require_no_extra_tool_text=True)

        self.assertEqual(scorer_for_suite([case]), "tool-call-heldout")
        self.assertEqual(action, "selected-tool-calls")
        self.assertTrue(scored["pass"])

    def test_heldout_text_case_uses_must_contain_markers(self) -> None:
        case = {
            "id": "heldout-invalid-tool-handling-payroll",
            "category": "invalid_tool_handling",
            "messages": [{"role": "system", "content": "<tools>[]</tools>"}],
            "expected": {
                "mode": "text",
                "must_not_have_tool_calls": True,
                "must_contain_any": ["cannot", "not available"],
                "must_not_contain_any": ["reset_payroll_direct_deposit"],
            },
        }
        response = "<think>reset_payroll_direct_deposit is missing</think>I cannot perform that action."

        constrained, action = apply_envelope(case, response)
        scored = score_enveloped_case(case, constrained, require_no_extra_tool_text=True)

        self.assertEqual(action, "selected-refusal-sentence")
        self.assertEqual(constrained, "I cannot perform that action.")
        self.assertTrue(scored["pass"])


if __name__ == "__main__":
    unittest.main()
