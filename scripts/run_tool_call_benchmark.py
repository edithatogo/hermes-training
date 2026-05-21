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


def generate_response(model: Any, tokenizer: Any, messages: list[dict[str, Any]], max_tokens: int) -> tuple[str, float]:
    from mlx_lm import generate as mlx_generate

    prompt = build_prompt(messages, tokenizer)
    t0 = time.time()
    response = mlx_generate(model, tokenizer, prompt=prompt, max_tokens=max_tokens, verbose=False)
    return response.strip(), time.time() - t0


def score_case(example: dict[str, Any], response: str) -> dict[str, Any]:
    expected = example["expected"]
    allowed_tools = extract_allowed_tools(example["messages"])
    calls, parse_errors, leftover = extract_tool_calls(response)
    response_lc = response.lower()

    tool_names = [str(call["name"]) for call in calls]
    tool_names_valid = all(name in allowed_tools for name in tool_names) if allowed_tools else True
    json_valid = bool(calls) and not parse_errors and not leftover.strip()

    result: dict[str, Any] = {
        "json_valid": json_valid,
        "tool_name_valid": tool_names_valid,
        "tool_call_count": len(calls),
        "allowed_tools": allowed_tools,
        "parsed_tool_calls": calls,
        "parse_errors": parse_errors,
        "leftover": leftover,
        "pass": False,
        "reason": "",
    }

    mode = expected.get("mode")
    if mode == "tool_calls":
        expected_calls = expected.get("tool_calls", [])
        exact_calls = calls == expected_calls
        result["arguments_correct"] = exact_calls
        result["pass"] = json_valid and tool_names_valid and exact_calls
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
        f"- Invalid-tool handling rate: `{summary['invalid_tool_handling_rate']:.3f}`",
        f"- Multi-turn repair rate: `{summary['multi_turn_repair_rate']:.3f}`",
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
    if not suite:
        raise ValueError(f"{args.suite}: empty benchmark suite")
    for case in suite:
        if not isinstance(case, dict):
            raise ValueError(f"{args.suite}: every case must be an object")
        if "id" not in case or "category" not in case or "messages" not in case or "expected" not in case:
            raise ValueError(f"{args.suite}: each case must contain id, category, messages, and expected")
        if not isinstance(case["messages"], list):
            raise ValueError(f"{case['id']}: messages must be a list")
        if not isinstance(case["expected"], dict):
            raise ValueError(f"{case['id']}: expected must be an object")

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
            response, latency_s = generate_response(model, tokenizer, apply_user_prefix(messages, args.user_prefix), args.max_tokens)
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
    tool_call_rows = [row for row in rows if row["category"] != "invalid_tool_handling"]
    json_valid_count = sum(1 for row in tool_call_rows if row["json_valid"])
    arg_correct_count = sum(1 for row in tool_call_rows if row.get("arguments_correct"))
    invalid_tool_rows = [row for row in rows if row["category"] == "invalid_tool_handling"]
    invalid_tool_ok_count = sum(1 for row in invalid_tool_rows if row["pass"])
    repair_rows = [row for row in rows if row["category"] == "multi_turn_repair"]
    repair_ok_count = sum(1 for row in repair_rows if row["pass"])

    summary = {
        "run_id": run_id,
        "created_at": datetime.now(UTC).isoformat(),
        "suite": str(args.suite),
        "output_dir": str(output_dir),
        "model": args.model,
        "adapter": args.adapter,
        "cases": cases,
        "tool_call_cases": len(tool_call_rows),
        "passed": passed,
        "pass_rate": passed / cases,
        "json_valid_rate": json_valid_count / max(1, len(tool_call_rows)),
        "argument_accuracy_rate": arg_correct_count / max(1, len(tool_call_rows)),
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
