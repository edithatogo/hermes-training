#!/usr/bin/env python3
"""Run lm-eval tasks through a direct MLX loglikelihood adapter."""
from __future__ import annotations

import argparse
import json
import os
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


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


def save_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def token_ids(tokenizer: Any, text: str) -> list[int]:
    return list(tokenizer.encode(text, add_special_tokens=False))


def continuation_token_ids(tokenizer: Any, context: str, continuation: str) -> tuple[list[int], int]:
    context_ids = token_ids(tokenizer, context)
    full_ids = token_ids(tokenizer, context + continuation)
    if len(full_ids) >= len(context_ids) and full_ids[: len(context_ids)] == context_ids:
        return full_ids, len(context_ids)
    continuation_ids = token_ids(tokenizer, continuation)
    return context_ids + continuation_ids, len(context_ids)


def extract_logits(output: Any) -> Any:
    return getattr(output, "logits", output[0] if isinstance(output, tuple) else output)


def score_continuation(model: Any, tokenizer: Any, context: str, continuation: str, max_length: int) -> tuple[float, bool]:
    import mlx.core as mx

    ids, continuation_start = continuation_token_ids(tokenizer, context, continuation)
    if len(ids) < 2 or continuation_start >= len(ids):
        return 0.0, True

    if len(ids) > max_length:
        overflow = len(ids) - max_length
        ids = ids[overflow:]
        continuation_start = max(0, continuation_start - overflow)
    if continuation_start == 0:
        continuation_start = 1

    input_ids = mx.array([ids[:-1]], dtype=mx.int32)
    targets = ids[1:]
    logits = extract_logits(model(input_ids))
    score = 0.0
    greedy = True
    for target_pos in range(continuation_start, len(ids)):
        logits_pos = logits[0, target_pos - 1]
        target_id = int(ids[target_pos])
        score += float((logits_pos[target_id] - mx.logsumexp(logits_pos)).item())
        greedy = greedy and int(mx.argmax(logits_pos).item()) == target_id
    mx.eval(logits)
    return score, greedy


def run_self_test() -> None:
    class ToyTokenizer:
        def encode(self, text: str, add_special_tokens: bool = False) -> list[int]:
            del add_special_tokens
            return [ord(char) % 17 for char in text]

    class ToyModel:
        def __call__(self, input_ids: Any) -> Any:
            import mlx.core as mx

            batch, seq = input_ids.shape
            logits = mx.zeros((batch, seq, 17))
            return logits

    score, greedy = score_continuation(ToyModel(), ToyTokenizer(), "ab", "c", 32)
    if not isinstance(score, float) or not isinstance(greedy, bool):
        raise AssertionError("self-test did not return (float, bool)")


def render_report(summary: dict[str, Any]) -> str:
    lines = [
        f"# MLX lm-eval Direct Run: {summary['run_id']}",
        "",
        f"Date: {summary['created_at']}",
        f"Model: `{summary['model']}`",
        f"Adapter: `{summary.get('adapter', '')}`",
        f"Tasks: `{','.join(summary['tasks'])}`",
        f"Limit: `{summary['limit']}`",
        "",
        "## Result",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Status | {summary['status']} |",
        f"| Output | `{summary['output_dir']}` |",
        f"| Load latency | {summary['load_latency_s']:.3f}s |",
        f"| Total latency | {summary['total_latency_s']:.3f}s |",
    ]
    if summary.get("error"):
        lines.extend(["", "## Error", "", "```text", str(summary["error"]), "```"])
    lines.append("")
    return "\n".join(lines)


class MlxLmEvalAdapter:  # concrete methods match lm_eval.api.model.LM
    def __init__(self, model_name: str, adapter_path: str | None, max_length: int) -> None:
        from lm_eval.api.model import LM
        from mlx_lm import load

        self.__class__ = type("MlxLmEvalAdapter", (self.__class__, LM), {})
        LM.__init__(self)
        self.model_name = model_name
        self.adapter_path = adapter_path or ""
        self.max_length = max_length
        started = time.time()
        self.model, self.tokenizer = load(model_name, adapter_path=adapter_path)
        self.load_latency_s = time.time() - started

    @property
    def tokenizer_name(self) -> str:
        return self.model_name

    def get_model_info(self) -> dict[str, Any]:
        return {
            "model_name": self.model_name,
            "adapter_path": self.adapter_path,
            "max_length": self.max_length,
            "runtime": "mlx-direct-loglikelihood",
        }

    def loglikelihood(self, requests: list[Any]) -> list[tuple[float, bool]]:
        rows: list[tuple[float, bool]] = []
        for request in requests:
            context, continuation = request.args
            rows.append(score_continuation(self.model, self.tokenizer, str(context), str(continuation), self.max_length))
        return rows

    def loglikelihood_rolling(self, requests: list[Any]) -> list[float]:
        rows: list[float] = []
        for request in requests:
            (text,) = request.args
            score, _ = score_continuation(self.model, self.tokenizer, "", str(text), self.max_length)
            rows.append(score)
        return rows

    def generate_until(self, requests: list[Any]) -> list[str]:
        raise NotImplementedError("This direct MLX adapter is for loglikelihood-only lm-eval tasks.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="Qwen/Qwen3-4B-MLX-4bit")
    parser.add_argument("--adapter", default="gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter")
    parser.add_argument("--tasks", default="arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande")
    parser.add_argument("--limit", type=int, default=1)
    parser.add_argument("--batch-size", default="1")
    parser.add_argument("--max-length", type=int, default=4096)
    parser.add_argument("--run-id", default=f"mlx-lm-eval-{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        run_self_test()
        print("ok: direct MLX loglikelihood self-test")
        return 0

    tasks = [item.strip() for item in args.tasks.split(",") if item.strip()]
    output_dir = args.output_dir or (resolve_default_output_root() / "standard-benchmarks" / "lm-eval" / args.run_id)
    report_path = args.report or (Path("reports/benchmark/lm-eval") / f"{args.run_id}.md")
    if args.dry_run:
        print(f"model: {args.model}")
        print(f"adapter: {args.adapter}")
        print(f"tasks: {tasks}")
        print(f"limit: {args.limit}")
        print(f"output_dir: {output_dir}")
        print(f"report: {report_path}")
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    started = time.time()
    summary: dict[str, Any] = {
        "run_id": args.run_id,
        "created_at": datetime.now(UTC).isoformat(),
        "model": args.model,
        "adapter": args.adapter,
        "tasks": tasks,
        "limit": args.limit,
        "output_dir": str(output_dir),
        "report": str(report_path),
        "max_length": args.max_length,
        "status": "started",
        "load_latency_s": 0.0,
        "total_latency_s": 0.0,
    }
    try:
        from lm_eval import evaluator

        adapter = MlxLmEvalAdapter(args.model, args.adapter or None, args.max_length)
        summary["load_latency_s"] = adapter.load_latency_s
        results = evaluator.simple_evaluate(
            model=adapter,
            tasks=tasks,
            limit=args.limit,
            batch_size=args.batch_size,
            bootstrap_iters=0,
            log_samples=True,
            verbosity="INFO",
        )
        summary["status"] = "scored"
        summary["results"] = results or {}
        save_json(output_dir / "results.json", results or {})
    except Exception as exc:  # noqa: BLE001
        summary["status"] = "blocked"
        summary["error"] = f"{type(exc).__name__}: {exc}"
    summary["total_latency_s"] = time.time() - started
    save_json(output_dir / "summary.json", summary)
    report_path.write_text(render_report(summary), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0 if summary["status"] == "scored" else 1


if __name__ == "__main__":
    raise SystemExit(main())
