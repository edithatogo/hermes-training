#!/usr/bin/env python3
"""Run or score a local BFCL-style tool-call benchmark."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from normalize_tool_response import strip_empty_think_prefix


TOOLS_RE = re.compile(r"<tools>\s*(.*?)\s*</tools>", re.DOTALL | re.IGNORECASE)
TOOL_CALL_RE = re.compile(r"<tool_call>\s*(.*?)\s*</tool_call>", re.DOTALL | re.IGNORECASE)
REFUSAL_MARKERS = (
    "cannot",
    "can't",
    "not available",
    "unable",
    "do not have",
    "don't have",
    "won't",
    "refuse",
    "clarify",
)
REQUIRED_CATEGORIES = {
    "json_validity",
    "argument_correctness",
    "invalid_tool_handling",
    "multi_turn_repair",
}
VALID_ROLES = {"system", "user", "assistant"}
VALID_EXPECTED_MODES = {"tool_calls", "text"}


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for lineno, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{lineno}: invalid JSON: {exc}") from exc
            if not isinstance(row, dict):
                raise ValueError(f"{path}:{lineno}: expected object rows")
            rows.append(row)
    return rows


def save_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def extract_allowed_tools(messages: list[dict[str, Any]]) -> list[str]:
    for message in messages:
        if message.get("role") != "system":
            continue
        content = str(message.get("content", ""))
        match = TOOLS_RE.search(content)
        if not match:
            continue
        try:
            tools = json.loads(match.group(1))
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid <tools> block: {exc}") from exc
        names: list[str] = []
        for entry in tools:
            try:
                name = entry["function"]["name"]
            except Exception as exc:  # pragma: no cover - defensive
                raise ValueError("tool definition missing function.name") from exc
            names.append(str(name))
        return names
    return []


def validate_suite(suite: list[Any], suite_path: Path) -> None:
    """Validate suite shape and scorer-relevant invariants."""
    if not suite:
        raise ValueError(f"{suite_path}: empty benchmark suite")

    seen_ids: set[str] = set()
    categories: set[str] = set()
    for index, case in enumerate(suite, 1):
        if not isinstance(case, dict):
            raise ValueError(f"{suite_path}:{index}: every case must be an object")

        missing_keys = {"id", "category", "messages", "expected"} - set(case)
        if missing_keys:
            raise ValueError(f"{suite_path}:{index}: missing required keys {sorted(missing_keys)}")

        case_id = case["id"]
        if not isinstance(case_id, str) or not case_id:
            raise ValueError(f"{suite_path}:{index}: id must be a non-empty string")
        if case_id in seen_ids:
            raise ValueError(f"{suite_path}: duplicate case id {case_id}")
        seen_ids.add(case_id)

        category = case["category"]
        if category not in REQUIRED_CATEGORIES:
            raise ValueError(f"{case_id}: unsupported category {category!r}")
        categories.add(category)

        messages = case["messages"]
        if not isinstance(messages, list) or not messages:
            raise ValueError(f"{case_id}: messages must be a non-empty list")
        for message_index, message in enumerate(messages, 1):
            if not isinstance(message, dict):
                raise ValueError(f"{case_id}: message {message_index} must be an object")
            role = message.get("role")
            if role not in VALID_ROLES:
                raise ValueError(f"{case_id}: message {message_index} has unsupported role {role!r}")
            if not isinstance(message.get("content"), str):
                raise ValueError(f"{case_id}: message {message_index} content must be a string")

        allowed_tools = extract_allowed_tools(messages)
        expected = case["expected"]
        if not isinstance(expected, dict):
            raise ValueError(f"{case_id}: expected must be an object")
        mode = expected.get("mode")
        if mode not in VALID_EXPECTED_MODES:
            raise ValueError(f"{case_id}: unsupported expected.mode={mode!r}")

        if category == "invalid_tool_handling" and mode != "text":
            raise ValueError(f"{case_id}: invalid_tool_handling cases must use expected.mode='text'")
        if category != "invalid_tool_handling" and mode != "tool_calls":
            raise ValueError(f"{case_id}: {category} cases must use expected.mode='tool_calls'")

        if mode == "tool_calls":
            expected_calls = expected.get("tool_calls")
            if not isinstance(expected_calls, list) or not expected_calls:
                raise ValueError(f"{case_id}: tool-call cases must contain at least one expected tool call")
            for call_index, call in enumerate(expected_calls, 1):
                if not isinstance(call, dict):
                    raise ValueError(f"{case_id}: expected tool call {call_index} must be an object")
                if not isinstance(call.get("name"), str) or not call.get("name"):
                    raise ValueError(f"{case_id}: expected tool call {call_index} must have a non-empty name")
                if allowed_tools and call["name"] not in allowed_tools:
                    raise ValueError(
                        f"{case_id}: expected tool {call['name']!r} is not declared in the <tools> block"
                    )
                if not isinstance(call.get("arguments"), dict):
                    raise ValueError(f"{case_id}: expected tool call {call_index} arguments must be an object")
        else:
            if expected.get("must_not_have_tool_calls", True) is not True:
                raise ValueError(f"{case_id}: text-mode cases must require no tool calls")
            markers = expected.get("must_contain_any")
            if not isinstance(markers, list) or not all(isinstance(marker, str) and marker for marker in markers):
                raise ValueError(f"{case_id}: text-mode cases must define non-empty must_contain_any strings")

        if category == "multi_turn_repair":
            has_assistant_context = any(message.get("role") == "assistant" for message in messages[:-1])
            has_correction_turn = any(
                message.get("role") == "user"
                and any(
                    marker in message.get("content", "").lower()
                    for marker in ("correct", "re-issue", "incomplete", "left out")
                )
                for message in messages
            )
            if not has_assistant_context and not has_correction_turn:
                raise ValueError(f"{case_id}: multi_turn_repair cases need malformed assistant context or a correction turn")

    missing_categories = REQUIRED_CATEGORIES - categories
    if missing_categories:
        raise ValueError(f"{suite_path}: missing required categories {sorted(missing_categories)}")


def strip_code_fences(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if len(lines) >= 2 and lines[0].startswith("```") and lines[-1].strip() == "```":
            return "\n".join(lines[1:-1]).strip()
    return stripped


def parse_tool_call_payload(payload: str) -> dict[str, Any]:
    data = json.loads(strip_code_fences(payload))
    if not isinstance(data, dict):
        raise ValueError("tool call payload must be a JSON object")
    if "name" not in data or "arguments" not in data:
        raise ValueError("tool call payload must contain name and arguments")
    if not isinstance(data["arguments"], dict):
        raise ValueError("tool call arguments must be an object")
    return {"name": data["name"], "arguments": data["arguments"]}


def extract_tool_calls(text: str) -> tuple[list[dict[str, Any]], list[str], str]:
    calls: list[dict[str, Any]] = []
    errors: list[str] = []
    clean_text = text.strip()

    for block in TOOL_CALL_RE.findall(text):
        try:
            calls.append(parse_tool_call_payload(block))
        except Exception as exc:
            errors.append(str(exc))

    if calls:
        leftover = TOOL_CALL_RE.sub("", text).strip()
        return calls, errors, leftover

    candidate = strip_code_fences(clean_text)
    if candidate.startswith("{") or candidate.startswith("["):
        try:
            data = json.loads(candidate)
            if isinstance(data, dict) and {"name", "arguments"} <= set(data):
                calls.append(parse_tool_call_payload(candidate))
                return calls, errors, ""
            if isinstance(data, list):
                for item in data:
                    if not isinstance(item, dict):
                        raise ValueError("raw JSON tool-call list must contain objects")
                    if "name" not in item or "arguments" not in item:
                        raise ValueError("raw JSON tool-call item missing name or arguments")
                    if not isinstance(item["arguments"], dict):
                        raise ValueError("raw JSON tool-call arguments must be objects")
                    calls.append({"name": item["name"], "arguments": item["arguments"]})
                return calls, errors, ""
        except Exception as exc:
            errors.append(str(exc))

    return calls, errors, clean_text


def build_prompt(messages: list[dict[str, Any]], tokenizer: Any | None) -> str:
    if tokenizer is not None and hasattr(tokenizer, "apply_chat_template"):
        try:
            return tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True,
            )
        except Exception:
            pass

    lines = []
    for message in messages:
        role = str(message.get("role", "unknown")).upper()
        content = str(message.get("content", ""))
        lines.append(f"{role}: {content}")
    lines.append("ASSISTANT:")
    return "\n".join(lines)


def apply_user_prefix(messages: list[dict[str, Any]], prefix: str) -> list[dict[str, Any]]:
    if not prefix:
        return messages
    updated: list[dict[str, Any]] = []
    prefixed = False
    for message in messages:
        copied = dict(message)
        if not prefixed and copied.get("role") == "user":
            copied["content"] = f"{prefix.strip()} {copied.get('content', '')}".strip()
            prefixed = True
        updated.append(copied)
    return updated


def build_generation_prompt(messages: list[dict[str, Any]], tokenizer: Any | None, assistant_prefill: str = "") -> str:
    return build_prompt(messages, tokenizer) + assistant_prefill


def generate_response(
    model: Any,
    tokenizer: Any,
    messages: list[dict[str, Any]],
    max_tokens: int,
    assistant_prefill: str = "",
) -> tuple[str, float]:
    from mlx_lm import generate as mlx_generate

    prompt = build_generation_prompt(messages, tokenizer, assistant_prefill)
    t0 = time.time()
    response = mlx_generate(model, tokenizer, prompt=prompt, max_tokens=max_tokens, verbose=False)
    return response.strip(), time.time() - t0


def score_case(example: dict[str, Any], response: str) -> dict[str, Any]:
    expected = example["expected"]
    allowed_tools = extract_allowed_tools(example["messages"])
    calls, parse_errors, leftover = extract_tool_calls(response)
    normalized_response = strip_empty_think_prefix(response)
    normalized_calls, normalized_parse_errors, normalized_leftover = extract_tool_calls(normalized_response)
    response_lc = response.lower()

    tool_names = [str(call["name"]) for call in calls]
    tool_names_valid = all(name in allowed_tools for name in tool_names) if allowed_tools else True
    json_valid = bool(calls) and not parse_errors and not leftover.strip()
    normalized_tool_names = [str(call["name"]) for call in normalized_calls]
    normalized_tool_names_valid = (
        all(name in allowed_tools for name in normalized_tool_names) if allowed_tools else True
    )
    normalized_json_valid = (
        bool(normalized_calls) and not normalized_parse_errors and not normalized_leftover.strip()
    )

    result: dict[str, Any] = {
        "expected_mode": expected.get("mode"),
        "json_valid": json_valid,
        "tool_name_valid": tool_names_valid,
        "tool_call_count": len(calls),
        "allowed_tools": allowed_tools,
        "parsed_tool_calls": calls,
        "parse_errors": parse_errors,
        "leftover": leftover,
        "empty_think_stripped_response": normalized_response if normalized_response != response.strip() else "",
        "json_valid_after_empty_think_strip": normalized_json_valid,
        "tool_name_valid_after_empty_think_strip": normalized_tool_names_valid,
        "parsed_tool_calls_after_empty_think_strip": normalized_calls,
        "parse_errors_after_empty_think_strip": normalized_parse_errors,
        "leftover_after_empty_think_strip": normalized_leftover,
        "pass": False,
        "strict_failure_rescued_by_empty_think_strip": False,
        "reason": "",
    }

    mode = expected.get("mode")
    if mode == "tool_calls":
        expected_calls = expected.get("tool_calls", [])
        exact_calls = calls == expected_calls
        normalized_exact_calls = normalized_calls == expected_calls
        result["arguments_correct"] = exact_calls
        result["arguments_correct_after_empty_think_strip"] = normalized_exact_calls
        result["pass_after_empty_think_strip"] = (
            normalized_json_valid and normalized_tool_names_valid and normalized_exact_calls
        )
        result["pass"] = json_valid and tool_names_valid and exact_calls
        result["strict_failure_rescued_by_empty_think_strip"] = (
            not result["pass"] and bool(result["pass_after_empty_think_strip"])
        )
        if not result["pass"]:
            result["reason"] = expected.get("fail_reason", "tool-call output did not match the expected JSON schema")
        return result

    if mode == "text":
        must_contain_any = [str(item).lower() for item in expected.get("must_contain_any", [])]
        must_not_have_tool_calls = expected.get("must_not_have_tool_calls", True)
        text_ok = True
        if must_not_have_tool_calls and calls:
            text_ok = False
            result["reason"] = "tool call emitted where plain text was required"
        if must_contain_any and not any(marker in response_lc for marker in must_contain_any):
            text_ok = False
            result["reason"] = expected.get("fail_reason", "response did not contain a refusal or clarification marker")
        if expected.get("must_not_contain_any"):
            forbidden = [str(item).lower() for item in expected.get("must_not_contain_any", [])]
            if any(marker in response_lc for marker in forbidden):
                text_ok = False
                result["reason"] = expected.get("fail_reason", "response contained a forbidden marker")
        result["pass"] = text_ok
        result["pass_after_empty_think_strip"] = text_ok
        return result

    raise ValueError(f"{example['id']}: unsupported expected.mode={mode!r}")


def resolve_default_output_root() -> Path:
    env_eval_root = os.environ.get("HERMES_EVAL_ROOT")
    if env_eval_root:
        return Path(env_eval_root)
    storage_root = os.environ.get("HERMES_STORAGE_ROOT")
    if storage_root:
        return Path(storage_root) / "hermes-evals"
    if Path("/Volumes/PortableSSD").exists():
        return Path("/Volumes/PortableSSD") / "hermes-evals"
    return Path.cwd() / ".local-storage" / "hermes-evals"


def render_summary_markdown(summary: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Tool-Call Benchmark Summary",
        "",
        f"- Run id: `{summary['run_id']}`",
        f"- Created at: `{summary['created_at']}`",
        f"- Suite: `{summary['suite']}`",
        f"- Output root: `{summary['output_dir']}`",
        f"- Model: `{summary.get('model') or '(responses only)'}`",
        f"- Adapter: `{summary.get('adapter') or '(none)'}`",
        f"- Cases: `{summary['cases']}`",
        f"- Pass rate: `{summary['pass_rate']:.3f}`",
        f"- JSON validity rate: `{summary['json_valid_rate']:.3f}`",
        f"- Argument correctness rate: `{summary['argument_accuracy_rate']:.3f}`",
        f"- Diagnostic pass rate after empty-think stripping: `{summary['empty_think_stripped_pass_rate']:.3f}`",
        f"- Diagnostic JSON validity after empty-think stripping: `{summary['empty_think_stripped_json_valid_rate']:.3f}`",
        f"- Diagnostic argument correctness after empty-think stripping: `{summary['empty_think_stripped_argument_accuracy_rate']:.3f}`",
        f"- Responses with leading empty-think wrapper: `{summary['empty_think_prefix_cases']}`",
        f"- Strict failures rescued only by empty-think stripping: `{summary['strict_failures_rescued_by_empty_think_strip']}`",
        f"- Invalid-tool handling rate: `{summary['invalid_tool_handling_rate']:.3f}`",
        f"- Multi-turn repair rate: `{summary['multi_turn_repair_rate']:.3f}`",
        "",
        "Diagnostic empty-think stripping is reported only to separate Qwen-style wrapper noise from malformed tool calls. It does not change the strict pass/fail gate.",
        "",
        "## Category Breakdown",
        "",
        "| Category | Cases | Pass rate |",
        "|---|---:|---:|",
    ]
    category_totals = Counter(row["category"] for row in rows)
    category_passes = Counter(row["category"] for row in rows if row["pass"])
    for category in sorted(category_totals):
        lines.append(
            f"| {category} | {category_totals[category]} | {category_passes[category] / category_totals[category]:.3f} |"
        )
    lines.extend(
        [
            "",
            "## Output Location",
            "",
            f"Raw outputs, scorecards, and summaries live under `{summary['output_dir']}`.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--suite",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "benchmarks" / "tool_call_local" / "suite.json",
        help="Benchmark suite JSON file.",
    )
    parser.add_argument(
        "--responses",
        type=Path,
        help="Score an existing JSONL response file instead of generating outputs.",
    )
    parser.add_argument("--model", help="Model name or path for generation runs.")
    parser.add_argument("--adapter", help="Optional adapter path for generation runs.")
    parser.add_argument("--max-tokens", type=int, default=256, help="Maximum generation tokens.")
    parser.add_argument(
        "--user-prefix",
        default="",
        help="Optional prefix for the first user turn, e.g. /no_think for Qwen3 strict-format checks.",
    )
    parser.add_argument(
        "--assistant-prefill",
        default="",
        help="Optional assistant-side prefill appended to the prompt but not counted as generated output.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Output directory. Defaults to an SSD-backed run directory under HERMES_EVAL_ROOT.",
    )
    parser.add_argument("--run-id", help="Optional explicit run id.")
    parser.add_argument("--dry-run", action="store_true", help="Validate the suite and exit.")
    args = parser.parse_args()

    suite = load_json(args.suite)
    if not isinstance(suite, list):
        raise ValueError(f"{args.suite}: expected a JSON array of benchmark cases")
    validate_suite(suite, args.suite)

    run_id = args.run_id or f"toolcall-{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}"
    output_dir = args.output_dir or (resolve_default_output_root() / "tool-call-benchmark" / run_id)

    if args.dry_run:
        categories = Counter(str(case.get("category", "unknown")) for case in suite)
        print(f"suite: {args.suite}")
        print(f"cases: {len(suite)}")
        print(f"categories: {dict(categories)}")
        print(f"output_dir: {output_dir}")
        return 0

    if args.responses and args.model:
        raise ValueError("choose either --responses or --model, not both")
    if not args.responses and not args.model:
        raise ValueError("provide --model for generation or --responses for scoring")

    output_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []

    if args.responses:
        responses = load_jsonl(args.responses)
        response_map: dict[str, str] = {}
        for row in responses:
            case_id = str(row.get("id", ""))
            response = row.get("response")
            if not case_id or not isinstance(response, str):
                raise ValueError(f"{args.responses}: each row must contain id and response")
            if case_id in response_map:
                raise ValueError(f"{args.responses}: duplicate response id {case_id}")
            response_map[case_id] = response

        suite_ids = [str(case["id"]) for case in suite]
        missing = [case_id for case_id in suite_ids if case_id not in response_map]
        extra = [case_id for case_id in response_map if case_id not in suite_ids]
        if missing:
            raise ValueError(f"{args.responses}: missing responses for {missing}")
        if extra:
            raise ValueError(f"{args.responses}: extra responses for {extra}")

        for case in suite:
            response = response_map[str(case["id"])]
            rows.append(
                {
                    "id": case["id"],
                    "category": case.get("category", "unknown"),
                    "response": response,
                    "latency_s": None,
                    **score_case(case, response),
                }
            )
    else:
        print(f"Loading model: {args.model}")
        from mlx_lm import load

        t0 = time.time()
        model, tokenizer = load(args.model, adapter_path=args.adapter)
        load_s = time.time() - t0
        print(f"  loaded in {load_s:.1f}s")
        for index, case in enumerate(suite, 1):
            messages = case.get("messages", [])
            if not isinstance(messages, list):
                raise ValueError(f"{case['id']}: messages must be a list")
            print(f"  [{index}/{len(suite)}] {case.get('category', 'unknown')} {case['id']}")
            response, latency_s = generate_response(
                model,
                tokenizer,
                apply_user_prefix(messages, args.user_prefix),
                args.max_tokens,
                args.assistant_prefill,
            )
            rows.append(
                {
                    "id": case["id"],
                    "category": case.get("category", "unknown"),
                    "response": response,
                    "latency_s": round(latency_s, 3),
                    **score_case(case, response),
                }
            )

        save_jsonl(output_dir / "responses.jsonl", rows)

    cases = len(rows)
    passed = sum(1 for row in rows if row["pass"])
    tool_call_rows = [row for row in rows if row.get("expected_mode") == "tool_calls"]
    json_valid_count = sum(1 for row in tool_call_rows if row["json_valid"])
    arg_correct_count = sum(1 for row in tool_call_rows if row.get("arguments_correct"))
    normalized_passed = sum(1 for row in rows if row.get("pass_after_empty_think_strip"))
    normalized_json_valid_count = sum(
        1 for row in tool_call_rows if row.get("json_valid_after_empty_think_strip")
    )
    normalized_arg_correct_count = sum(
        1 for row in tool_call_rows if row.get("arguments_correct_after_empty_think_strip")
    )
    invalid_tool_rows = [row for row in rows if row["category"] == "invalid_tool_handling"]
    invalid_tool_ok_count = sum(1 for row in invalid_tool_rows if row["pass"])
    repair_rows = [row for row in rows if row["category"] == "multi_turn_repair"]
    repair_ok_count = sum(1 for row in repair_rows if row["pass"])
    empty_think_prefix_rows = [row for row in rows if row.get("empty_think_stripped_response")]
    empty_think_rescued_rows = [row for row in rows if row.get("strict_failure_rescued_by_empty_think_strip")]
    residual_failure_rows = [
        row
        for row in rows
        if not row["pass"] and not row.get("strict_failure_rescued_by_empty_think_strip")
    ]

    summary = {
        "run_id": run_id,
        "created_at": datetime.now(UTC).isoformat(),
        "suite": str(args.suite),
        "output_dir": str(output_dir),
        "model": args.model,
        "adapter": args.adapter,
        "user_prefix": args.user_prefix,
        "assistant_prefill": args.assistant_prefill,
        "cases": cases,
        "tool_call_cases": len(tool_call_rows),
        "passed": passed,
        "pass_rate": passed / cases,
        "json_valid_rate": json_valid_count / max(1, len(tool_call_rows)),
        "argument_accuracy_rate": arg_correct_count / max(1, len(tool_call_rows)),
        "empty_think_stripped_pass_rate": normalized_passed / cases,
        "empty_think_stripped_json_valid_rate": normalized_json_valid_count
        / max(1, len(tool_call_rows)),
        "empty_think_stripped_argument_accuracy_rate": normalized_arg_correct_count
        / max(1, len(tool_call_rows)),
        "empty_think_prefix_cases": len(empty_think_prefix_rows),
        "strict_failures_rescued_by_empty_think_strip": len(empty_think_rescued_rows),
        "strict_failures_rescued_by_empty_think_strip_ids": [row["id"] for row in empty_think_rescued_rows],
        "residual_strict_failure_count": len(residual_failure_rows),
        "residual_strict_failure_ids": [row["id"] for row in residual_failure_rows],
        "residual_strict_failure_reasons": {
            row["id"]: row.get("reason", "") for row in residual_failure_rows
        },
        "invalid_tool_handling_rate": invalid_tool_ok_count / max(1, len(invalid_tool_rows)),
        "multi_turn_repair_rate": repair_ok_count / max(1, len(repair_rows)),
    }

    save_jsonl(output_dir / "results.jsonl", rows)
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (output_dir / "summary.md").write_text(render_summary_markdown(summary, rows), encoding="utf-8")

    print(json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"results: {output_dir / 'results.jsonl'}")
    print(f"summary: {output_dir / 'summary.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
