#!/usr/bin/env python3
"""Patch BFCL's local Qwen handler to score reasoning-side tool calls.

The BFCL Qwen FC handler can parse tool calls from the full completion text for
chat history while still returning only the text after ``</think>`` as the
scored ``model_responses`` field. Some local MLX/OpenAI-compatible completion
runs put valid ``<tool_call>`` blocks inside reasoning and leave the visible
content blank or prose. This guarded local patch promotes those reasoning-side
tool-call blocks into the scored response only when the visible response has no
tool-call block.
"""
from __future__ import annotations

import argparse
import importlib.util
import shutil
import sys
from pathlib import Path


MARKER = "# HERMES_REASONING_TOOL_CALL_BRIDGE"

OLD = '''        if "</think>" in model_response:
            parts = model_response.split("</think>")
            reasoning_content = parts[0].rstrip("\\n").split("<think>")[-1].lstrip("\\n")
            cleaned_response = parts[-1].lstrip("\\n")

        if len(extracted_tool_calls) > 0:
'''

NEW = '''        if "</think>" in model_response:
            parts = model_response.split("</think>")
            reasoning_content = parts[0].rstrip("\\n").split("<think>")[-1].lstrip("\\n")
            cleaned_response = parts[-1].lstrip("\\n")

        # HERMES_REASONING_TOOL_CALL_BRIDGE: keep BFCL scoring aligned with the
        # tool calls already parsed for chat history when local runtimes emit
        # complete tool calls inside reasoning and leave visible content blank.
        if "<tool_call>" not in cleaned_response and "<tool_call>" in reasoning_content:
            reasoning_tool_calls = re.findall(
                r"<tool_call>\\s*(.*?)\\s*</tool_call>",
                reasoning_content,
                re.DOTALL,
            )
            if reasoning_tool_calls:
                cleaned_response = "\\n".join(
                    f"<tool_call>\\n{tool_call.strip()}\\n</tool_call>"
                    for tool_call in reasoning_tool_calls
                )
                extracted_tool_calls = self._extract_tool_calls(cleaned_response)

        if len(extracted_tool_calls) > 0:
'''


def default_handler_path() -> Path:
    spec = importlib.util.find_spec("bfcl_eval.model_handler.local_inference.qwen_fc")
    if spec is None or spec.origin is None:
        raise RuntimeError("could not locate bfcl_eval.model_handler.local_inference.qwen_fc")
    return Path(spec.origin)


def patch(path: Path, *, check: bool) -> int:
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        print(f"already patched: {path}")
        return 0
    if OLD not in text:
        print(f"not patchable: expected parser block not found in {path}", file=sys.stderr)
        return 1
    if check:
        print(f"patch needed: {path}")
        return 1

    backup = path.with_suffix(path.suffix + ".hermes-backup")
    if not backup.exists():
        shutil.copy2(path, backup)
        print(f"backup written: {backup}")
    path.write_text(text.replace(OLD, NEW), encoding="utf-8")
    print(f"patched: {path}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--handler-path", type=Path, default=None)
    parser.add_argument("--check", action="store_true", help="exit non-zero if the patch is not already applied")
    args = parser.parse_args()

    path = args.handler_path or default_handler_path()
    if args.check:
        text = path.read_text(encoding="utf-8")
        if MARKER in text:
            print(f"patched: {path}")
            return 0
    return patch(path, check=args.check)


if __name__ == "__main__":
    raise SystemExit(main())
