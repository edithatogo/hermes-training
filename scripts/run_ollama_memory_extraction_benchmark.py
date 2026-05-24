#!/usr/bin/env python3
"""Benchmark an Ollama chat model as a mem0-style memory extractor."""
from __future__ import annotations

import argparse
import json
import os
import re
import statistics
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import requests


DEFAULT_SYSTEM_PROMPT_FILE = Path(__file__).resolve().parents[1] / "mem0" / "extraction" / "system_prompt.md"


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def save_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def validate_suite(suite: list[Any], suite_path: Path) -> None:
    if not suite:
        raise ValueError(f"{suite_path}: empty suite")
    seen_ids: set[str] = set()
    for index, case in enumerate(suite, 1):
        if not isinstance(case, dict):
            raise ValueError(f"{suite_path}:{index}: case must be an object")
        missing = {"id", "category", "conversation", "expected"} - set(case)
        if missing:
            raise ValueError(f"{suite_path}:{index}: missing keys {sorted(missing)}")
        case_id = case["id"]
        if not isinstance(case_id, str) or not case_id:
            raise ValueError(f"{suite_path}:{index}: id must be non-empty")
        if case_id in seen_ids:
            raise ValueError(f"{suite_path}: duplicate id {case_id}")
        seen_ids.add(case_id)
        conversation = case["conversation"]
        if not isinstance(conversation, list) or not conversation:
            raise ValueError(f"{case_id}: conversation must be non-empty")
        for message in conversation:
            if not isinstance(message, dict) or message.get("role") not in {"user", "assistant", "system"}:
                raise ValueError(f"{case_id}: invalid message")
            if not isinstance(message.get("content"), str):
                raise ValueError(f"{case_id}: message content must be a string")
        expected = case["expected"]
        if not isinstance(expected, dict):
            raise ValueError(f"{case_id}: expected must be an object")
        for key in ("must_extract_any", "must_extract_all", "must_not_extract_any"):
            value = expected.get(key, [])
            if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
                raise ValueError(f"{case_id}: expected.{key} must be a list of strings")


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


def endpoint_chat(base_url: str, model: str, messages: list[dict[str, str]], timeout_s: float) -> tuple[str, float]:
    url = base_url.rstrip("/") + "/chat/completions"
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0,
        "max_tokens": 256,
        "stream": False,
    }
    started = time.time()
    response = requests.post(url, json=payload, timeout=timeout_s)
    latency_s = time.time() - started
    response.raise_for_status()
    data = response.json()
    choices = data.get("choices")
    if not isinstance(choices, list) or not choices:
        raise ValueError("endpoint response missing choices")
    message = choices[0].get("message") if isinstance(choices[0], dict) else None
    if not isinstance(message, dict) or not isinstance(message.get("content"), str):
        raise ValueError("endpoint response missing message.content")
    return message["content"], latency_s


def parse_memories(text: str) -> tuple[list[str], str | None]:
    candidate = text.strip()
    candidate = re.sub(r"^```(?:json)?", "", candidate).strip()
    candidate = re.sub(r"```$", "", candidate).strip()
    decoder = json.JSONDecoder()
    for index, char in enumerate(candidate):
        if char != "{":
            continue
        try:
            value, _ = decoder.raw_decode(candidate[index:])
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            memories = value.get("memories")
            if isinstance(memories, list) and all(isinstance(item, str) for item in memories):
                return memories, None
            return [], "json object missing string-list memories"
    return [], "no parseable JSON object"


def score_case(case: dict[str, Any], memories: list[str], parse_error: str | None) -> dict[str, Any]:
    text = "\n".join(memories).lower()
    expected = case["expected"]
    must_extract_any = [item.lower() for item in expected.get("must_extract_any", [])]
    must_extract_all = [item.lower() for item in expected.get("must_extract_all", [])]
    must_not = [item.lower() for item in expected.get("must_not_extract_any", [])]
    any_ok = True if not must_extract_any else any(item in text for item in must_extract_any)
    all_ok = all(item in text for item in must_extract_all)
    extracted_expected = any_ok and all_ok
    forbidden_hit = any(item in text for item in must_not)
    no_memory_expected = not must_extract_any and not must_extract_all
    empty_ok = True if not no_memory_expected else len(memories) == 0
    passed = parse_error is None and extracted_expected and not forbidden_hit and empty_ok
    return {
        "pass": passed,
        "json_valid": parse_error is None,
        "parse_error": parse_error,
        "extracted_expected": extracted_expected,
        "forbidden_hit": forbidden_hit,
        "empty_ok": empty_ok,
        "memory_count": len(memories),
    }


def render_summary_markdown(summary: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# Ollama Memory Extraction Benchmark: {summary['run_id']}",
        "",
        f"Date: {summary['created_at']}",
        f"Model: `{summary['model']}`",
        "",
        "## Result",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Cases | {summary['cases']} |",
        f"| Pass rate | {summary['pass_rate']:.3f} |",
        f"| JSON validity rate | {summary['json_validity_rate']:.3f} |",
        f"| Expected extraction rate | {summary['expected_extraction_rate']:.3f} |",
        f"| Forbidden hit rate | {summary['forbidden_hit_rate']:.3f} |",
        f"| Empty-case pass rate | {summary['empty_case_pass_rate']:.3f} |",
        f"| Latency p50 | {summary['latency_p50_s']:.3f}s |",
        f"| Latency p95 | {summary['latency_p95_s']:.3f}s |",
        "",
        "## Cases",
        "",
        "| Case | Category | Pass | Memories |",
        "|---|---|---:|---:|",
    ]
    for row in rows:
        lines.append(f"| {row['id']} | {row['category']} | {row['pass']} | {row['memory_count']} |")
    lines.append("")
    return "\n".join(lines)


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    if len(values) == 1:
        return values[0]
    ordered = sorted(values)
    index = (len(ordered) - 1) * pct
    lower = int(index)
    upper = min(lower + 1, len(ordered) - 1)
    weight = index - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", type=Path, default=Path(__file__).resolve().parents[1] / "benchmarks" / "mem0_extraction" / "smoke_suite.json")
    parser.add_argument("--model", required=True)
    parser.add_argument("--base-url", default="http://127.0.0.1:11434/v1")
    parser.add_argument("--system-prompt-file", type=Path, default=DEFAULT_SYSTEM_PROMPT_FILE)
    parser.add_argument("--timeout-s", type=float, default=120.0)
    parser.add_argument("--run-id")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    suite = load_json(args.suite)
    if not isinstance(suite, list):
        raise ValueError(f"{args.suite}: expected JSON array")
    validate_suite(suite, args.suite)

    run_id = args.run_id or f"memory-extraction-{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}"
    output_dir = args.output_dir or (resolve_default_output_root() / "mem0-extraction-benchmark" / run_id)
    system_prompt = load_text(args.system_prompt_file)

    if args.dry_run:
        print(f"suite: {args.suite}")
        print(f"cases: {len(suite)}")
        print(f"model: {args.model}")
        print(f"base_url: {args.base_url}")
        print(f"system_prompt_file: {args.system_prompt_file}")
        print(f"output_dir: {output_dir}")
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    response_rows: list[dict[str, Any]] = []
    latencies: list[float] = []

    for index, case in enumerate(suite, 1):
        print(f"  [{index}/{len(suite)}] {case['id']}")
        messages = [{"role": "system", "content": system_prompt}, *case["conversation"]]
        response, latency_s = endpoint_chat(args.base_url, args.model, messages, args.timeout_s)
        latencies.append(latency_s)
        memories, parse_error = parse_memories(response)
        scored = score_case(case, memories, parse_error)
        response_rows.append({"id": case["id"], "response": response, "latency_s": round(latency_s, 3)})
        rows.append(
            {
                "id": case["id"],
                "category": case["category"],
                "latency_s": round(latency_s, 3),
                "memories": memories,
                "response": response,
                **scored,
            }
        )

    cases = len(rows)
    expected_by_id = {case["id"]: case["expected"] for case in suite}
    empty_rows = [row for row in rows if not expected_by_id[row["id"]].get("must_extract_any")]
    summary = {
        "run_id": run_id,
        "created_at": datetime.now(UTC).isoformat(),
        "suite": str(args.suite),
        "output_dir": str(output_dir),
        "model": args.model,
        "base_url": args.base_url,
        "system_prompt_file": str(args.system_prompt_file),
        "cases": cases,
        "passed": sum(1 for row in rows if row["pass"]),
        "pass_rate": sum(1 for row in rows if row["pass"]) / max(1, cases),
        "json_validity_rate": sum(1 for row in rows if row["json_valid"]) / max(1, cases),
        "expected_extraction_rate": sum(1 for row in rows if row["extracted_expected"]) / max(1, cases),
        "forbidden_hit_rate": sum(1 for row in rows if row["forbidden_hit"]) / max(1, cases),
        "empty_case_pass_rate": sum(1 for row in empty_rows if row["empty_ok"]) / max(1, len(empty_rows)),
        "latency_mean_s": statistics.fmean(latencies) if latencies else 0.0,
        "latency_p50_s": percentile(latencies, 0.50),
        "latency_p95_s": percentile(latencies, 0.95),
    }

    save_jsonl(output_dir / "responses.jsonl", response_rows)
    save_jsonl(output_dir / "results.jsonl", rows)
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (output_dir / "summary.md").write_text(render_summary_markdown(summary, rows), encoding="utf-8")

    print(json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"results: {output_dir / 'results.jsonl'}")
    print(f"summary: {output_dir / 'summary.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
