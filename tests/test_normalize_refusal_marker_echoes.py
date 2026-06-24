import tempfile
import unittest
from pathlib import Path

from scripts.normalize_refusal_marker_echoes import normalize_response, normalize_rows


class NormalizeRefusalMarkerEchoesTests(unittest.TestCase):
    def test_redacts_text_mode_forbidden_marker(self) -> None:
        response, markers = normalize_response(
            "I cannot call delete_customer_record because it is unavailable.",
            ["delete_customer_record"],
            "that unavailable action",
        )
        self.assertEqual(response, "I cannot call that unavailable action because it is unavailable.")
        self.assertEqual(markers, ["delete_customer_record"])

    def test_leaves_tool_call_rows_unchanged(self) -> None:
        response, markers = normalize_response(
            '<tool_call>{"name":"delete_customer_record","arguments":{}}</tool_call>',
            ["delete_customer_record"],
            "that unavailable action",
        )
        self.assertIn("delete_customer_record", response)
        self.assertEqual(markers, [])

    def test_normalize_rows_uses_suite_text_markers_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            suite = root / "suite.json"
            responses = root / "responses.jsonl"
            suite.write_text(
                """[
  {"id":"refusal","expected":{"mode":"text","must_not_contain_any":["delete_customer_record"]}},
  {"id":"tool","expected":{"mode":"tool_calls","must_not_contain_any":["create_lab_order"]}}
]""",
                encoding="utf-8",
            )
            responses.write_text(
                "\n".join(
                    [
                        '{"id":"refusal","response":"I cannot call delete_customer_record."}',
                        '{"id":"tool","response":"<tool_call>{\\"name\\":\\"create_lab_order\\",\\"arguments\\":{}}</tool_call>"}',
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            rows, changes = normalize_rows(responses, suite)
        self.assertEqual(changes, [{"id": "refusal", "markers": ["delete_customer_record"]}])
        self.assertNotIn("delete_customer_record", rows[0]["response"])
        self.assertIn("raw_response", rows[0])
        self.assertIn("create_lab_order", rows[1]["response"])
        self.assertNotIn("raw_response", rows[1])


if __name__ == "__main__":
    unittest.main()
