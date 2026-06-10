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

try:
    from lm_eval.api.model import LM as LmEvalBase
except ModuleNotFoundError:  # keep repo py_compile/unit tests independent from benchmark env
    LmEvalBase = object  # type: ignore[assignment,misc]


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
    path.write_text(json.dumps(json_safe(payload), indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")


def json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_safe(item) for item in value]
    if isinstance(value, tuple):
        return [json_safe(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


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


def trim_until(text: str, until: Any) -> str:
    stops: list[str]
    if until is None:
        return text
    if isinstance(until, str):
        stops = [until]
    elif isinstance(until, list):
        stops = [str(item) for item in until]
    else:
        stops = [str(until)]
    cut = len(text)
    for stop in stops:
        if not stop:
            continue
        index = text.find(stop)
        if index >= 0:
            cut = min(cut, index)
    return text[:cut]


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


def collect_task_metrics(results: dict[str, Any]) -> dict[str, dict[str, Any]]:
    task_results = results.get("results", {}) if isinstance(results, dict) else {}
    if not isinstance(task_results, dict):
        return {}
    metrics: dict[str, dict[str, Any]] = {}
    for task, payload in task_results.items():
        if not isinstance(payload, dict):
            continue
        task_metrics = {
            key: value
            for key, value in payload.items()
            if ("," in key or key in {"acc", "acc_norm", "exact_match"}) and "stderr" not in key
        }
        if task_metrics:
            metrics[str(task)] = task_metrics
    return metrics


def render_report(summary: dict[str, Any]) -> str:
    limit_display = summary["limit"] if summary["limit"] is not None else "full"
    lines = [
        f"# MLX lm-eval Direct Run: {summary['run_id']}",
        "",
        f"Date: {summary['created_at']}",
        f"Model: `{summary['model']}`",
        f"Adapter: `{summary.get('adapter', '')}`",
        f"Tasks: `{','.join(summary['tasks'])}`",
        f"Limit: `{limit_display}`",
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
    completed_tasks = summary.get("completed_tasks")
    current_task = summary.get("current_task")
    pending_tasks = summary.get("pending_tasks")
    if isinstance(completed_tasks, list) or current_task or (isinstance(pending_tasks, list) and pending_tasks):
        total_tasks = len(summary.get("tasks", [])) if isinstance(summary.get("tasks"), list) else 0
        lines.extend(["", "| Progress | Value |", "|---|---|"])
        if isinstance(completed_tasks, list):
            display = f"{len(completed_tasks)}/{total_tasks}" if total_tasks else str(len(completed_tasks))
            lines.append(f"| Completed tasks | `{display}` |")
        if current_task:
            lines.append(f"| Current task | `{current_task}` |")
        if isinstance(pending_tasks, list) and pending_tasks:
            lines.append(f"| Pending tasks | `{','.join(str(task) for task in pending_tasks)}` |")
    task_metrics = summary.get("task_metrics")
    if isinstance(task_metrics, dict) and task_metrics:
        lines.extend(["", "## Metrics", "", "| Task | Metric | Value |", "|---|---|---:|"])
        for task, metrics in task_metrics.items():
            if not isinstance(metrics, dict):
                continue
            for metric, value in metrics.items():
                display = f"{float(value):.6f}" if isinstance(value, (int, float)) else str(value)
                lines.append(f"| `{task}` | `{metric}` | {display} |")
    lines.append("")
    return "\n".join(lines)


def persist_run_state(summary: dict[str, Any], output_dir: Path, report_path: Path, started: float) -> None:
    summary["total_latency_s"] = time.time() - started
    save_json(output_dir / "summary.json", summary)
    report_path.write_text(render_report(summary), encoding="utf-8")


def collect_task_result(task_name: str, results: dict[str, Any]) -> dict[str, Any]:
    task_results = results.get("results", {}) if isinstance(results, dict) else {}
    payload = task_results.get(task_name, {}) if isinstance(task_results, dict) else {}
    if not isinstance(payload, dict):
        return {}
    return {task_name: payload}


def build_results_payload(
    run_id: str,
    model: str,
    adapter: str,
    tasks: list[str],
    limit: int | None,
    task_order: list[str],
    raw_results: dict[str, Any],
) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "model": model,
        "adapter": adapter,
        "tasks": tasks,
        "limit": limit,
        "task_order": task_order,
        "task_metrics": collect_task_metrics(raw_results),
        "results": raw_results.get("results", {}),
        "task_runs": raw_results.get("task_runs", {}),
        "mode": "incremental-full-run" if limit is None else "limit-smoke",
    }


def load_json_payload(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def load_resumable_full_run_state(
    output_dir: Path,
    run_id: str,
    model: str,
    adapter: str,
    tasks: list[str],
) -> dict[str, Any] | None:
    summary_path = output_dir / "summary.json"
    results_path = output_dir / "results.json"
    if not summary_path.exists():
        return None

    summary = load_json_payload(summary_path)
    if not summary:
        return None
    if summary.get("run_id") != run_id:
        raise ValueError(f"existing run_id {summary.get('run_id')!r} does not match {run_id!r}")
    if summary.get("model") != model or summary.get("adapter") != adapter:
        raise ValueError("existing run configuration does not match requested model or adapter")
    if summary.get("tasks") != tasks:
        raise ValueError("existing task list does not match requested task list")
    if summary.get("limit") is not None:
        return None

    results = load_json_payload(results_path)
    completed_tasks = [str(task) for task in summary.get("completed_tasks", []) if str(task) in tasks]
    pending_tasks = [task for task in tasks if task not in completed_tasks]
    task_metrics = summary.get("task_metrics", {})
    raw_results: dict[str, Any] = {
        "results": results.get("results", {}) if isinstance(results.get("results", {}), dict) else {},
        "task_runs": results.get("task_runs", {}) if isinstance(results.get("task_runs", {}), dict) else {},
    }
    started_at = summary.get("started_at")
    if not isinstance(started_at, (int, float)):
        started_at = time.time()

    summary["started_at"] = started_at
    summary["status"] = "running" if pending_tasks else "scored"
    summary["completed_tasks"] = completed_tasks
    summary["pending_tasks"] = pending_tasks
    summary["task_metrics"] = task_metrics if isinstance(task_metrics, dict) else {}
    summary.pop("error", None)
    return {
        "summary": summary,
        "raw_results": raw_results,
        "started_at": float(started_at),
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "results": results,
    }


def run_full_selected_tasks(
    adapter: Any,
    tasks: list[str],
    batch_size: str,
    started: float,
    summary: dict[str, Any],
    output_dir: Path,
    report_path: Path,
    run_id: str,
    model: str,
    adapter_path: str,
    raw_results: dict[str, Any] | None = None,
    completed_tasks: list[str] | None = None,
) -> None:
    from lm_eval import evaluator

    raw_results = raw_results or {"results": {}, "task_runs": {}}
    completed_tasks = list(completed_tasks or [])
    summary["status"] = "running"
    summary["completed_tasks"] = completed_tasks
    summary["pending_tasks"] = [task for task in tasks if task not in completed_tasks]
    summary.pop("current_task", None)
    summary["task_metrics"] = collect_task_metrics(raw_results)
    persist_run_state(summary, output_dir, report_path, started)
    save_json(
        output_dir / "results.json",
        build_results_payload(run_id, model, adapter_path, tasks, None, list(completed_tasks), raw_results),
    )

    pending_tasks = [task for task in tasks if task not in completed_tasks]
    for task in pending_tasks:
        summary["current_task"] = task
        persist_run_state(summary, output_dir, report_path, started)
        task_results = evaluator.simple_evaluate(
            model=adapter,
            tasks=[task],
            limit=None,
            batch_size=batch_size,
            bootstrap_iters=0,
            log_samples=False,
            verbosity="INFO",
        )
        safe_task_results = json_safe(task_results or {})
        task_result = collect_task_result(task, safe_task_results)
        if task_result:
            raw_results["results"].update(task_result)
        raw_results["task_runs"][task] = safe_task_results
        summary["task_metrics"] = collect_task_metrics(raw_results)
        completed_tasks.append(task)
        summary["completed_tasks"] = completed_tasks
        summary["pending_tasks"] = [item for item in tasks if item not in completed_tasks]
        persist_run_state(summary, output_dir, report_path, started)
        save_json(
            output_dir / "results.json",
            build_results_payload(run_id, model, adapter_path, tasks, None, list(completed_tasks), raw_results),
        )

    summary["status"] = "scored"
    summary.pop("current_task", None)
    summary["pending_tasks"] = []
    summary["task_metrics"] = collect_task_metrics(raw_results)
    persist_run_state(summary, output_dir, report_path, started)
    save_json(
        output_dir / "results.json",
        build_results_payload(run_id, model, adapter_path, tasks, None, list(tasks), raw_results),
    )


class MlxLmEvalAdapter(LmEvalBase):  # concrete methods match lm_eval.api.model.LM
    def __init__(self, model_name: str, adapter_path: str | None, max_length: int) -> None:
        from mlx_lm import load

        super().__init__()
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
        from mlx_lm import generate as mlx_generate

        rows: list[str] = []
        for request in requests:
            context, kwargs = request.args
            if not isinstance(kwargs, dict):
                kwargs = {}
            max_tokens = int(kwargs.get("max_gen_toks") or kwargs.get("max_tokens") or 256)
            response = mlx_generate(
                self.model,
                self.tokenizer,
                prompt=str(context),
                max_tokens=max_tokens,
                verbose=False,
            )
            rows.append(trim_until(str(response), kwargs.get("until")).strip())
        return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="Qwen/Qwen3-4B-MLX-4bit")
    parser.add_argument("--adapter", default="gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter")
    parser.add_argument("--tasks", default="arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande")
    parser.add_argument("--limit", type=int)
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
    limit = None if args.limit == 0 else args.limit
    output_dir = args.output_dir or (resolve_default_output_root() / "standard-benchmarks" / "lm-eval" / args.run_id)
    report_path = args.report or (Path("reports/benchmark/lm-eval") / f"{args.run_id}.md")
    if args.dry_run:
        print(f"model: {args.model}")
        print(f"adapter: {args.adapter}")
        print(f"tasks: {tasks}")
        print(f"limit: {limit}")
        print(f"output_dir: {output_dir}")
        print(f"report: {report_path}")
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    summary: dict[str, Any] = {
        "run_id": args.run_id,
        "created_at": datetime.now(UTC).isoformat(),
        "model": args.model,
        "adapter": args.adapter,
        "tasks": tasks,
        "limit": limit,
        "output_dir": str(output_dir),
        "report": str(report_path),
        "max_length": args.max_length,
        "status": "started",
        "load_latency_s": 0.0,
        "total_latency_s": 0.0,
        "started_at": time.time(),
    }
    try:
        adapter = MlxLmEvalAdapter(args.model, args.adapter or None, args.max_length)
        summary["load_latency_s"] = adapter.load_latency_s
        if limit is None:
            resume_state = load_resumable_full_run_state(output_dir, args.run_id, args.model, args.adapter, tasks)
            if resume_state:
                summary = resume_state["summary"]
                summary["load_latency_s"] = adapter.load_latency_s
                started = float(resume_state["started_at"])
                raw_results = resume_state["raw_results"]
                completed_tasks = resume_state["completed_tasks"]
                if not resume_state["pending_tasks"]:
                    summary["status"] = "scored"
                    summary.pop("current_task", None)
                    persist_run_state(summary, output_dir, report_path, started)
                    save_json(
                        output_dir / "results.json",
                        build_results_payload(args.run_id, args.model, args.adapter, tasks, None, list(completed_tasks), raw_results),
                    )
                else:
                    run_full_selected_tasks(
                        adapter,
                        tasks,
                        args.batch_size,
                        started,
                        summary,
                        output_dir,
                        report_path,
                        args.run_id,
                        args.model,
                        args.adapter,
                        raw_results=raw_results,
                        completed_tasks=completed_tasks,
                    )
            else:
                started = float(summary["started_at"])
                run_full_selected_tasks(
                    adapter,
                    tasks,
                    args.batch_size,
                    started,
                    summary,
                    output_dir,
                    report_path,
                    args.run_id,
                    args.model,
                    args.adapter,
                )
        else:
            started = float(summary["started_at"])
            from lm_eval import evaluator

            results = evaluator.simple_evaluate(
                model=adapter,
                tasks=tasks,
                limit=limit,
                batch_size=args.batch_size,
                bootstrap_iters=0,
                log_samples=True,
                verbosity="INFO",
            )
            summary["status"] = "scored"
            raw_results = results or {}
            summary["task_metrics"] = collect_task_metrics(raw_results)
            save_json(output_dir / "results.json", results or {})
    except Exception as exc:  # noqa: BLE001
        summary["status"] = "blocked"
        summary["error"] = f"{type(exc).__name__}: {exc}"
    persist_run_state(summary, output_dir, report_path, started)
    print(json.dumps(json_safe(summary), indent=2, ensure_ascii=False))
    return 0 if summary["status"] == "scored" else 1


if __name__ == "__main__":
    raise SystemExit(main())
