#!/usr/bin/env python3
"""Normalize local model responses before Hermes tool-call parsing.

The strict benchmark remains the release gate. This helper exists for runtime
integration where Qwen-family models may emit an empty leading thinking block
even when `/no_think` is used.
"""
from __future__ import annotations

import argparse
import re
import sys


EMPTY_THINK_RE = re.compile(r"^\s*<think>\s*</think>\s*", re.DOTALL | re.IGNORECASE)


def strip_empty_think_prefix(text: str) -> str:
    """Strip one leading empty <think></think> block and nothing else."""
    return EMPTY_THINK_RE.sub("", text, count=1).strip()


def run_self_test() -> None:
    cases = {
        "<think></think><tool_call>{}</tool_call>": "<tool_call>{}</tool_call>",
        "\n<think>\n</think>\n<tool_call>{}</tool_call>\n": "<tool_call>{}</tool_call>",
        "<think>reasoning</think><tool_call>{}</tool_call>": "<think>reasoning</think><tool_call>{}</tool_call>",
        "prefix <think></think><tool_call>{}</tool_call>": "prefix <think></think><tool_call>{}</tool_call>",
    }
    for raw, expected in cases.items():
        actual = strip_empty_think_prefix(raw)
        if actual != expected:
            raise AssertionError(f"normalize mismatch: {raw!r} -> {actual!r}, expected {expected!r}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "text",
        nargs="?",
        help="Response text. If omitted, the response is read from stdin.",
    )
    parser.add_argument("--self-test", action="store_true", help="Run built-in normalization checks.")
    args = parser.parse_args()

    if args.self_test:
        run_self_test()
        print("normalize_tool_response self-test passed")
        return 0

    text = args.text if args.text is not None else sys.stdin.read()
    sys.stdout.write(strip_empty_think_prefix(text))
    if not text.endswith("\n"):
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
