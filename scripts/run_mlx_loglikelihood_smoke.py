#!/usr/bin/env python3
"""Score prompt/continuation pairs with direct MLX causal-LM loglikelihood."""
from __future__ import annotations

import argparse
import json
import math
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_ROOT = Path("/Volumes/PortableSSD/hermes-evals/standard-benchmarks/mlx-loglikelihood")


@dataclass(frozen=True)
class LoglikelihoodCase:
    case_id: str
    prompt: str
    continuation: str


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                row = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no}: invalid JSONL row: {exc}") from exc
            if not isinstance(row, dict):
                raise ValueError(f"{path}:{line_no}: expected JSON object")
            rows.append(row)
    return rows


def parse_cases(path: Path) -> list[LoglikelihoodCase]:
    cases: list[LoglikelihoodCase] = []
    for idx, row in enumerate(load_jsonl(path), start=1):
        prompt = row.get("prompt")
        continuation = row.get("continuation")
        if not isinstance(prompt, str) or not isinstance(continuation, str):
            raise ValueError(f"{path}:{idx}: rows require string prompt and continuation")
        case_id = str(row.get("id") or f"case-{idx}")
        if not continuation:
            raise ValueError(f"{path}:{idx}: continuation must be non-empty")
        cases.append(LoglikelihoodCase(case_id, prompt, continuation))
    if not cases:
        raise ValueError(f"{path}: no cases found")
    return cases


def encode_text(tokenizer: Any, text: str) -> list[int]:
    try:
        tokens = tokenizer.encode(text, add_special_tokens=False)
    except TypeError:
        tokens = tokenizer.encode(text)
    if not isinstance(tokens, list):
        tokens = list(tokens)
    return [int(token) for token in tokens]


def continuation_span(tokenizer: Any, prompt: str, continuation: str) -> tuple[list[int], int]:
    prompt_ids = encode_text(tokenizer, prompt)
    full_ids = encode_text(tokenizer, prompt + continuation)
    if not prompt_ids:
        raise ValueError("prompt must encode to at least one token for causal loglikelihood scoring")
    if len(full_ids) <= len(prompt_ids):
        raise ValueError("continuation did not add any tokens after prompt tokenization")
    return full_ids, len(prompt_ids)


def logprob_from_row(row: Any, token_id: int) -> float:
    try:
        import mlx.core as mx
    except ModuleNotFoundError as exc:
        raise RuntimeError("mlx is required for direct MLX loglikelihood scoring") from exc

    token_logit = row[token_id]
    return float((token_logit - mx.logsumexp(row)).item())


def score_tokens_from_logits(logits: Any, token_ids: list[int], continuation_start: int) -> tuple[float, list[float]]:
    """Score continuation tokens from causal-LM logits.

    `logits[position - 1]` predicts `token_ids[position]`, so continuation
    scoring starts at the first token after the prompt.
    """
    token_logprobs: list[float] = []
    for position in range(continuation_start, len(token_ids)):
        token_logprobs.append(logprob_from_row(logits[0, position - 1], token_ids[position]))
    return float(sum(token_logprobs)), token_logprobs


def uniform_mock_score(case: LoglikelihoodCase, tokenizer: Any, vocab_size: int) -> dict[str, Any]:
    full_ids, continuation_start = continuation_span(tokenizer, case.prompt, case.continuation)
    continuation_count = len(full_ids) - continuation_start
    token_logprob = -math.log(vocab_size)
    return {
        "id": case.case_id,
        "prompt_tokens": continuation_start,
        "continuation_tokens": continuation_count,
        "loglikelihood": token_logprob * continuation_count,
        "avg_logprob": token_logprob,
        "greedy_match": False,
        "mode": "mock-uniform",
    }


def score_case(model: Any, tokenizer: Any, case: LoglikelihoodCase, max_length: int) -> dict[str, Any]:
    try:
        import mlx.core as mx
    except ModuleNotFoundError as exc:
        raise RuntimeError("mlx is required for direct MLX loglikelihood scoring") from exc

    full_ids, continuation_start = continuation_span(tokenizer, case.prompt, case.continuation)
    if len(full_ids) > max_length:
        raise ValueError(f"{case.case_id}: tokenized length {len(full_ids)} exceeds max length {max_length}")
    input_ids = mx.array([full_ids], dtype=mx.int32)
    logits = model(input_ids)
    mx.eval(logits)
    total, token_logprobs = score_tokens_from_logits(logits, full_ids, continuation_start)
    avg = total / len(token_logprobs)
    greedy = True
    for offset, position in enumerate(range(continuation_start, len(full_ids))):
        pred = int(mx.argmax(logits[0, position - 1]).item())
        if pred != full_ids[position]:
            greedy = False
            break
    return {
        "id": case.case_id,
        "prompt_tokens": continuation_start,
        "continuation_tokens": len(token_logprobs),
        "loglikelihood": total,
        "avg_logprob": avg,
        "greedy_match": greedy,
        "mode": "mlx-direct",
    }


def render_markdown(summary: dict[str, Any], results: Iterable[dict[str, Any]]) -> str:
    lines = [
        "# MLX Direct Loglikelihood Smoke",
        "",
        f"Run ID: `{summary['run_id']}`",
        f"Created: {summary['created_at']}",
        f"Model: `{summary['model']}`",
        f"Adapter: `{summary.get('adapter_path', '')}`",
        f"Suite: `{summary['suite']}`",
        f"Mode: `{summary['mode']}`",
        "",
        "## Result",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Cases | {summary['cases']} |",
        f"| Total continuation tokens | {summary['continuation_tokens']} |",
        f"| Mean avg logprob | {summary['mean_avg_logprob']:.6f} |",
        f"| Greedy match rate | {summary['greedy_match_rate']:.3f} |",
        f"| Load latency seconds | {summary['load_latency_s']:.3f} |",
        f"| Score latency seconds | {summary['score_latency_s']:.3f} |",
        "",
        "## Cases",
        "",
        "| Case | Continuation tokens | Loglikelihood | Avg logprob | Greedy match |",
        "|---|---:|---:|---:|---|",
    ]
    for row in results:
        lines.append(
            f"| `{row['id']}` | {row['continuation_tokens']} | {row['loglikelihood']:.6f} | {row['avg_logprob']:.6f} | `{str(row['greedy_match']).lower()}` |"
        )
    lines.extend(
        [
            "",
            "## Decision",
            "",
            "This proves the direct MLX prompt/continuation scoring path and output schema.",
            "It is not an official lm-eval scorecard until wrapped against the selected lm-eval task documents and run without mock scoring.",
            "",
        ]
    )
    return "\n".join(lines)


def write_outputs(output_dir: Path, summary: dict[str, Any], results: list[dict[str, Any]]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "results.jsonl").write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in results),
        encoding="utf-8",
    )
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (output_dir / "summary.md").write_text(render_markdown(summary, results), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", type=Path, default=ROOT / "benchmarks" / "lm_loglikelihood" / "smoke.jsonl")
    parser.add_argument("--model", default="Qwen/Qwen3-4B-MLX-4bit")
    parser.add_argument("--adapter-path")
    parser.add_argument("--run-id", default=f"mlx-loglikelihood-smoke-{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}")
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--max-cases", type=int, default=0)
    parser.add_argument("--max-length", type=int, default=2048)
    parser.add_argument("--mock-uniform", action="store_true", help="Use deterministic uniform mock scoring without loading MLX weights.")
    parser.add_argument("--mock-vocab-size", type=int, default=32000)
    args = parser.parse_args()

    cases = parse_cases(args.suite)
    if args.max_cases > 0:
        cases = cases[: args.max_cases]

    load_started = time.time()
    if args.mock_uniform:
        class WhitespaceTokenizer:
            def encode(self, text: str, *_args: Any, **_kwargs: Any) -> list[int]:
                return list(range(1, len(text.split()) + 1))

        model = None
        tokenizer = WhitespaceTokenizer()
        load_latency_s = time.time() - load_started
    else:
        from mlx_lm import load

        model, tokenizer = load(args.model, adapter_path=args.adapter_path)
        model.eval()
        load_latency_s = time.time() - load_started

    score_started = time.time()
    if args.mock_uniform:
        results = [uniform_mock_score(case, tokenizer, args.mock_vocab_size) for case in cases]
    else:
        results = [score_case(model, tokenizer, case, args.max_length) for case in cases]
    score_latency_s = time.time() - score_started

    continuation_tokens = sum(int(row["continuation_tokens"]) for row in results)
    greedy_matches = sum(1 for row in results if row["greedy_match"])
    summary = {
        "run_id": args.run_id,
        "created_at": datetime.now(UTC).isoformat(),
        "suite": str(args.suite),
        "output_dir": str(args.output_root / args.run_id),
        "model": args.model,
        "adapter_path": args.adapter_path or "",
        "mode": "mock-uniform" if args.mock_uniform else "mlx-direct",
        "cases": len(results),
        "continuation_tokens": continuation_tokens,
        "mean_avg_logprob": sum(float(row["avg_logprob"]) for row in results) / len(results),
        "greedy_match_rate": greedy_matches / len(results),
        "load_latency_s": load_latency_s,
        "score_latency_s": score_latency_s,
        "max_length": args.max_length,
    }
    write_outputs(args.output_root / args.run_id, summary, results)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
