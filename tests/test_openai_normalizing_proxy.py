import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from scripts.openai_normalizing_proxy import (
    add_completions_prompt_suffix,
    cap_completions_max_tokens,
    extract_first_tool_call_block,
    normalize_completions_reasoning_content,
    prefix_completions_text,
    promote_chat_reasoning_tool_call_content,
    promote_completions_reasoning_tool_call_text,
)


class OpenAINormalizingProxyTests(unittest.TestCase):
    def test_completion_prompt_suffix_appends_to_string_prompt_once(self) -> None:
        payload, count = add_completions_prompt_suffix({"prompt": "assistant\n"}, "<tool_call>")
        self.assertEqual(count, 1)
        self.assertEqual(payload["prompt"], "assistant\n<tool_call>")
        payload, count = add_completions_prompt_suffix(payload, "<tool_call>")
        self.assertEqual(count, 0)
        self.assertEqual(payload["prompt"], "assistant\n<tool_call>")

    def test_completion_prompt_suffix_appends_to_prompt_list(self) -> None:
        payload, count = add_completions_prompt_suffix({"prompt": ["a", "b<tool_call>", 3]}, "<tool_call>")
        self.assertEqual(count, 1)
        self.assertEqual(payload["prompt"], ["a<tool_call>", "b<tool_call>", 3])

    def test_completion_reasoning_content_fills_blank_text_only(self) -> None:
        payload = {
            "choices": [
                {"text": "", "reasoning_content": "{\"name\":\"demo.tool\"}"},
                {"text": "already visible", "reasoning_content": "hidden"},
            ]
        }
        updated, count = normalize_completions_reasoning_content(payload, "<tool_call>\n")
        self.assertEqual(count, 1)
        self.assertEqual(updated["choices"][0]["text"], "<tool_call>\n{\"name\":\"demo.tool\"}")
        self.assertEqual(updated["choices"][1]["text"], "already visible")

    def test_completion_max_tokens_cap_is_opt_in(self) -> None:
        payload, count = cap_completions_max_tokens({"max_tokens": 4096}, 512)
        self.assertEqual(count, 1)
        self.assertEqual(payload["max_tokens"], 512)
        payload, count = cap_completions_max_tokens({"max_tokens": 128}, 512)
        self.assertEqual(count, 0)
        self.assertEqual(payload["max_tokens"], 128)

    def test_completion_text_prefix_prepends_visible_text_once(self) -> None:
        payload = {"choices": [{"text": "{\"name\":\"demo.tool\"}"}, {"text": ""}]}
        updated, count = prefix_completions_text(payload, "<tool_call>\n")
        self.assertEqual(count, 1)
        self.assertEqual(updated["choices"][0]["text"], "<tool_call>\n{\"name\":\"demo.tool\"}")
        updated, count = prefix_completions_text(updated, "<tool_call>\n")
        self.assertEqual(count, 0)

    def test_completion_reasoning_tool_call_text_promotes_over_prose(self) -> None:
        payload = {
            "choices": [
                {
                    "text": "The requested action is complete.",
                    "reasoning_content": '<tool_call>\n{"name":"demo.tool","arguments":{}}\n</tool_call>',
                },
                {
                    "text": '<tool_call>\n{"name":"already.visible","arguments":{}}\n</tool_call>',
                    "reasoning_content": '<tool_call>\n{"name":"hidden.tool","arguments":{}}\n</tool_call>',
                },
            ]
        }
        updated, count = promote_completions_reasoning_tool_call_text(payload)
        self.assertEqual(count, 1)
        self.assertEqual(
            updated["choices"][0]["text"],
            '<tool_call>\n{"name":"demo.tool","arguments":{}}\n</tool_call>',
        )
        self.assertIn("already.visible", updated["choices"][1]["text"])

    def test_extract_first_tool_call_block(self) -> None:
        text = 'prefix <tool_call>\n{"name":"demo.one"}\n</tool_call> suffix <tool_call>{}</tool_call>'
        self.assertEqual(extract_first_tool_call_block(text), '<tool_call>\n{"name":"demo.one"}\n</tool_call>')
        self.assertEqual(extract_first_tool_call_block("<tool_call>{}"), "")

    def test_chat_reasoning_tool_call_content_promotes_when_content_is_not_tool_call(self) -> None:
        payload = {
            "choices": [
                {
                    "message": {
                        "content": "The answer is ready.",
                        "reasoning_content": '<tool_call>\n{"name":"demo.tool","arguments":{}}\n</tool_call>\nDone.',
                    }
                },
                {
                    "message": {
                        "content": '<tool_call>\n{"name":"already.visible","arguments":{}}\n</tool_call>',
                        "reasoning_content": '<tool_call>\n{"name":"hidden.tool","arguments":{}}\n</tool_call>',
                    }
                },
            ]
        }
        updated, count = promote_chat_reasoning_tool_call_content(payload)
        self.assertEqual(count, 1)
        self.assertEqual(
            updated["choices"][0]["message"]["content"],
            '<tool_call>\n{"name":"demo.tool","arguments":{}}\n</tool_call>',
        )
        self.assertIn("already.visible", updated["choices"][1]["message"]["content"])


if __name__ == "__main__":
    unittest.main()
