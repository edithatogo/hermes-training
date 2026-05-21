#!/usr/bin/env python3
"""Audit strict tool-call training JSONL files and benchmark overlap."""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


TOOLS_RE = re.compile(r"<tools>\s*(.*?)\s*</tools>", re.DOTALL | re.IGNORECASE)
TOOL_CALL_RE = re.compile(r"<tool_call>\s*(.*?)\s*</tool_call>", re.DOTALL | re.IGNORECASE)
VALID_ROLES = {"system", "user", "assistant"}
REFUSAL_MARKERS = (
    "cannot",
    "can't",
    "not available",
    "unable",
    "do not have",
    "don't have",
    "refuse",
)


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_jsonl(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    with path.open(encoding="utf-8") as handle:
        for lineno, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"{path}:{lineno}: invalid JSON: {exc}")
                continue
            if not isinstance(row, dict):
                errors.append(f"{path}:{lineno}: expected object row")
                continue
            row["_audit_file"] = str(path)
            row["_audit_lineno"] = lineno
            rows.append(row)
    return rows, errors


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
    if not isinstance(data.get("name"), str) or not data["name"]:
        raise ValueError("tool call payload must contain a non-empty string name")
    if "arguments" not in data:
        raise ValueError("tool call payload must contain arguments")
    if not isinstance(data["arguments"], dict):
        raise ValueError("tool call arguments must be an object")
    return {"name": data["name"], "arguments": data["arguments"]}


def extract_tool_calls(text: str) -> tuple[list[dict[str, Any]], list[str], str]:
    calls: list[dict[str, Any]] = []
    errors: list[str] = []
    for block in TOOL_CALL_RE.findall(text):
        try:
            calls.append(parse_tool_call_payload(block))
        except Exception as exc:
            errors.append(str(exc))
    leftover = TOOL_CALL_RE.sub("", text).strip()
    return calls, errors, leftover


def extract_allowed_tools(messages: list[dict[str, Any]]) -> tuple[set[str], list[str]]:
    errors: list[str] = []
    names: set[str] = set()
    for message in messages:
        if message.get("role") != "system":
            continue
        content = str(message.get("content", ""))
        for match in TOOLS_RE.findall(content):
            try:
                tools = json.loads(match)
            except json.JSONDecodeError as exc:
                errors.append(f"invalid <tools> JSON: {exc}")
                continue
            if not isinstance(tools, list):
                errors.append("<tools> block must contain a JSON array")
                continue
            for index, entry in enumerate(tools, 1):
                try:
                    name = entry["function"]["name"]
                except Exception:
                    errors.append(f"tool definition {index} missing function.name")
                    continue
                if not isinstance(name, str) or not name:
                    errors.append(f"tool definition {index} has invalid function.name")
                    continue
                names.add(name)
    return names, errors


def infer_category(row: dict[str, Any]) -> str:
    category = row.get("category")
    if isinstance(category, str) and category:
        return category
    row_id = str(row.get("id", "")).lower()
    if "json-validity" in row_id:
        return "json_validity"
    if "argument-correctness" in row_id:
        return "argument_correctness"
    if "invalid-tool" in row_id:
        return "invalid_tool_handling"
    if "multi-turn" in row_id:
        return "multi_turn_repair"
    return "uncategorized"


def is_refusal(text: str) -> bool:
    lowered = text.lower()
    return bool(text.strip()) and any(marker in lowered for marker in REFUSAL_MARKERS)


def validate_assistant_content(
    content: str,
    allowed_tools: set[str],
) -> tuple[str | None, list[str], list[str]]:
    calls, parse_errors, leftover = extract_tool_calls(content)
    tool_names = [call["name"] for call in calls]
    errors = list(parse_errors)
    if calls:
        if leftover:
            errors.append("assistant tool-call output has non-tool-call leftover text")
        unknown_tools = sorted({name for name in tool_names if allowed_tools and name not in allowed_tools})
        if unknown_tools:
            errors.append(f"assistant used undeclared tools: {unknown_tools}")
        if errors:
            return None, tool_names, errors
        return "tool_calls", tool_names, []

    if "<tool_call" in content.lower() or "</tool_call>" in content.lower():
        errors.append("assistant output contains malformed tool_call tags")
    if is_refusal(content):
        if errors:
            return None, tool_names, errors
        return "refusal", tool_names, []
    errors.append("assistant output is neither strict tool calls nor a valid refusal")
    return None, tool_names, errors


def user_prompts(messages: list[dict[str, Any]]) -> list[str]:
    return [str(message.get("content", "")) for message in messages if message.get("role") == "user"]


def benchmark_fingerprints(path: Path) -> dict[str, Any]:
    data = load_json(path)
    if not isinstance(data, list):
        raise ValueError(f"{path}: expected a JSON array")
    prompts: set[str] = set()
    tools: set[str] = set()
    case_count = 0
    for case in data:
        if not isinstance(case, dict):
            continue
        case_count += 1
        messages = case.get("messages")
        if isinstance(messages, list):
            prompts.update(user_prompts(messages))
            allowed, _ = extract_allowed_tools([msg for msg in messages if isinstance(msg, dict)])
            tools.update(allowed)
        expected = case.get("expected")
        if isinstance(expected, dict):
            for call in expected.get("tool_calls", []) if isinstance(expected.get("tool_calls"), list) else []:
                if isinstance(call, dict) and isinstance(call.get("name"), str):
                    tools.add(call["name"])
    return {"path": str(path), "cases": case_count, "user_prompts": prompts, "tool_names": tools}


def shorten(text: str, limit: int = 120) -> str:
    collapsed = " ".join(text.split())
    if len(collapsed) <= limit:
        return collapsed
    return collapsed[: limit - 3] + "..."


def collect_jsonl_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    return sorted(item for item in path.rglob("*.jsonl") if item.is_file())


def audit_rows(rows: list[dict[str, Any]], max_errors: int) -> dict[str, Any]:
    errors: list[str] = []
    category_counts: Counter[str] = Counter()
    assistant_output_counts: Counter[str] = Counter()
    prompt_to_rows: dict[str, list[str]] = defaultdict(list)
    tool_names: set[str] = set()
    assistant_tool_names: set[str] = set()
    ids: list[str] = []
    ids_by_file: dict[str, list[str]] = defaultdict(list)

    for row in rows:
        audit_file = str(row.get("_audit_file"))
        location = f"{audit_file}:{row.get('_audit_lineno')}"
        row_id = row.get("id")
        if not isinstance(row_id, str) or not row_id:
            errors.append(f"{location}: missing non-empty id")
            row_id = location
        ids.append(row_id)
        ids_by_file[audit_file].append(row_id)
        category_counts[infer_category(row)] += 1

        messages = row.get("messages")
        if not isinstance(messages, list) or not messages:
            errors.append(f"{location} {row_id}: messages must be a non-empty list")
            continue

        clean_messages: list[dict[str, Any]] = []
        for index, message in enumerate(messages, 1):
            if not isinstance(message, dict):
                errors.append(f"{location} {row_id}: message {index} must be an object")
                continue
            role = message.get("role")
            content = message.get("content")
            if role not in VALID_ROLES:
                errors.append(f"{location} {row_id}: message {index} has unsupported role {role!r}")
            if not isinstance(content, str):
                errors.append(f"{location} {row_id}: message {index} content must be a string")
                content = ""
            clean_messages.append({"role": role, "content": content})

        allowed_tools, tool_errors = extract_allowed_tools(clean_messages)
        tool_names.update(allowed_tools)
        errors.extend(f"{location} {row_id}: {error}" for error in tool_errors)
        for prompt in user_prompts(clean_messages):
            prompt_to_rows[prompt].append(row_id)

        assistant_messages = [message for message in clean_messages if message.get("role") == "assistant"]
        if not assistant_messages:
            errors.append(f"{location} {row_id}: row has no assistant messages")
            continue
        if clean_messages[-1].get("role") != "assistant":
            errors.append(f"{location} {row_id}: final message must be assistant")

        for assistant_index, message in enumerate(assistant_messages, 1):
            kind, names, output_errors = validate_assistant_content(str(message.get("content", "")), allowed_tools)
            assistant_tool_names.update(names)
            if kind:
                assistant_output_counts[kind] += 1
            else:
                assistant_output_counts["invalid"] += 1
                errors.extend(
                    f"{location} {row_id}: assistant message {assistant_index}: {error}" for error in output_errors
                )

    duplicate_ids_across_files = sorted(item for item, count in Counter(ids).items() if count > 1)
    duplicate_ids_within_files: dict[str, list[str]] = {}
    for path, file_ids in ids_by_file.items():
        duplicates = sorted(item for item, count in Counter(file_ids).items() if count > 1)
        if duplicates:
            duplicate_ids_within_files[path] = duplicates
            errors.append(f"{path}: duplicate row ids within file: {duplicates}")

    return {
        "rows": len(rows),
        "unique_ids": len(set(ids)),
        "duplicate_ids_across_files": duplicate_ids_across_files,
        "duplicate_ids_within_files": duplicate_ids_within_files,
        "categories": dict(sorted(category_counts.items())),
        "assistant_outputs": dict(sorted(assistant_output_counts.items())),
        "user_prompts": set(prompt_to_rows),
        "tool_names": tool_names,
        "assistant_tool_names": assistant_tool_names,
        "errors": errors[:max_errors],
        "error_count": len(errors),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "data_path",
        nargs="?",
        type=Path,
        default=Path("gemma4/data/strict_tool_call"),
        help="JSONL file or directory of JSONL files to audit.",
    )
    parser.add_argument(
        "--benchmark-suite",
        type=Path,
        default=Path("benchmarks/tool_call_local/suite.json"),
        help="Mirrored/local benchmark suite for overlap checks.",
    )
    parser.add_argument(
        "--heldout-suite",
        type=Path,
        default=Path("benchmarks/tool_call_local/heldout_suite.json"),
        help="Held-out benchmark suite for overlap checks.",
    )
    parser.add_argument("--max-errors", type=int, default=50, help="Maximum validation errors to include in JSON.")
    args = parser.parse_args()

    files = collect_jsonl_files(args.data_path)
    read_errors: list[str] = []
    all_rows: list[dict[str, Any]] = []
    file_summaries: dict[str, dict[str, Any]] = {}
    for path in files:
        rows, errors = load_jsonl(path)
        read_errors.extend(errors)
        all_rows.extend(rows)
        file_summaries[str(path)] = {
            "rows": len(rows),
            "categories": dict(sorted(Counter(infer_category(row) for row in rows).items())),
        }

    audit = audit_rows(all_rows, args.max_errors)
    benchmarks = {
        "suite": benchmark_fingerprints(args.benchmark_suite),
        "heldout_suite": benchmark_fingerprints(args.heldout_suite),
    }

    overlap: dict[str, Any] = {}
    for name, fingerprint in benchmarks.items():
        prompt_overlap = sorted(audit["user_prompts"] & fingerprint["user_prompts"])
        tool_overlap = sorted(audit["tool_names"] & fingerprint["tool_names"])
        assistant_tool_overlap = sorted(audit["assistant_tool_names"] & fingerprint["tool_names"])
        overlap[name] = {
            "path": fingerprint["path"],
            "cases": fingerprint["cases"],
            "user_prompt_overlap_count": len(prompt_overlap),
            "user_prompt_overlap_samples": [shorten(prompt) for prompt in prompt_overlap[:10]],
            "tool_name_overlap_count": len(tool_overlap),
            "tool_name_overlap": tool_overlap,
            "assistant_tool_name_overlap_count": len(assistant_tool_overlap),
            "assistant_tool_name_overlap": assistant_tool_overlap,
        }

    errors = read_errors + audit["errors"]
    summary = {
        "data_path": str(args.data_path),
        "files": file_summaries,
        "jsonl_file_count": len(files),
        "rows": audit["rows"],
        "unique_ids": audit["unique_ids"],
        "duplicate_ids_across_files": audit["duplicate_ids_across_files"],
        "duplicate_ids_within_files": audit["duplicate_ids_within_files"],
        "categories": audit["categories"],
        "assistant_outputs": audit["assistant_outputs"],
        "declared_tool_name_count": len(audit["tool_names"]),
        "assistant_tool_name_count": len(audit["assistant_tool_names"]),
        "overlap": overlap,
        "valid": not read_errors and audit["error_count"] == 0,
        "error_count": len(read_errors) + audit["error_count"],
        "errors": errors[: args.max_errors],
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
