#!/usr/bin/env python3
"""Run a fail-closed Transformers.js smoke for Qwen3 0.6B ONNX reranking."""
from __future__ import annotations

import argparse
import json
import os
import shutil
import statistics
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

try:
    from run_fixed_reranking_benchmark import ndcg_at_k, reciprocal_rank, validate_suite
except ModuleNotFoundError:
    from scripts.run_fixed_reranking_benchmark import ndcg_at_k, reciprocal_rank, validate_suite


ROOT = Path(__file__).resolve().parents[1]
JS_SMOKE = ROOT / "scripts" / "qwen3_onnx_transformersjs_smoke.mjs"
DEFAULT_MODEL = "onnx-community/Qwen3-Reranker-0.6B-ONNX"
DEFAULT_NPM_PACKAGE = "@huggingface/transformers@4.2.0"
DEFAULT_SUITE = ROOT / "benchmarks" / "mem0_reranking" / "fixed_candidate_suite.json"


def storage_root() -> Path:
    if os.environ.get("HERMES_STORAGE_ROOT"):
        return Path(os.environ["HERMES_STORAGE_ROOT"])
    if Path("/Volumes/PortableSSD").exists():
        return Path("/Volumes/PortableSSD")
    return ROOT / ".local-storage"


def default_tool_root() -> Path:
    return storage_root() / "hermes-tools" / "transformersjs-qwen3-reranker"


def default_eval_root() -> Path:
    if os.environ.get("HERMES_EVAL_ROOT"):
        return Path(os.environ["HERMES_EVAL_ROOT"])
    return storage_root() / "hermes-evals"


def repo_contains(path: Path) -> bool:
    try:
        path.resolve().relative_to(ROOT.resolve())
    except ValueError:
        return False
    return True


def load_suite(path: Path) -> list[Any]:
    suite = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(suite, list):
        raise ValueError(f"{path}: expected JSON array")
    validate_suite(suite, path)
    return suite


def ensure_tool_root(tool_root: Path, install: bool, npm_package: str) -> list[str]:
    if repo_contains(tool_root):
        raise ValueError(f"Refusing to create Node tooling under the repo: {tool_root}")
    tool_root.mkdir(parents=True, exist_ok=True)
    commands: list[str] = []
    package_json = tool_root / "package.json"
    node_modules = tool_root / "node_modules" / "@huggingface" / "transformers"
    if install:
        if not package_json.exists():
            commands.append("npm init -y")
            subprocess.run(["npm", "init", "-y"], cwd=tool_root, check=True)
        commands.append(f"npm install --save-exact {npm_package}")
        subprocess.run(["npm", "install", "--save-exact", npm_package], cwd=tool_root, check=True)
    elif not node_modules.exists():
        raise FileNotFoundError(
            f"{node_modules} is missing. Re-run with --install to install {npm_package} outside the repo."
        )
    return commands


def build_env(tool_root: Path, cache_root: Path) -> dict[str, str]:
    env = os.environ.copy()
    env.setdefault("HERMES_STORAGE_ROOT", str(storage_root()))
    env.setdefault("HF_HOME", str(storage_root() / "huggingface"))
    env.setdefault("HF_HUB_CACHE", str(Path(env["HF_HOME"]) / "hub"))
    env.setdefault("TRANSFORMERS_CACHE", str(Path(env["HF_HOME"]) / "transformers"))
    env.setdefault("XDG_CACHE_HOME", str(storage_root() / "cache"))
    env.setdefault("TMPDIR", str(storage_root() / "tmp"))
    env["NODE_PATH"] = str(tool_root / "node_modules")
    env["HERMES_TRANSFORMERSJS_MODULE"] = str(
        tool_root / "node_modules" / "@huggingface" / "transformers" / "dist" / "transformers.node.mjs"
    )
    env["TRANSFORMERS_CACHE"] = str(cache_root)
    env["HF_HUB_DISABLE_XET"] = env.get("HF_HUB_DISABLE_XET", "1")
    for key in ("HF_HOME", "HF_HUB_CACHE", "TRANSFORMERS_CACHE", "XDG_CACHE_HOME", "TMPDIR"):
        Path(env[key]).mkdir(parents=True, exist_ok=True)
    return env


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


def summarize_rows(rows: list[dict[str, Any]], run_id: str, args: argparse.Namespace, output_dir: Path) -> dict[str, Any]:
    cases = len(rows)
    recency_rows = [row for row in rows if row["category"] == "recency_conflict"]
    distractor_rows = [row for row in rows if row["category"] == "distractor_resistance"]
    latencies = [float(row.get("rerank_latency_s", 0.0) or 0.0) for row in rows]
    return {
        "run_id": run_id,
        "created_at": datetime.now(UTC).isoformat(),
        "status": "passed" if rows and all(row["top1_pass"] for row in rows) else "failed",
        "suite": str(args.suite),
        "output_dir": str(output_dir),
        "model": args.model_id,
        "runtime": "transformers.js",
        "npm_package": args.npm_package,
        "device": args.device,
        "dtype": args.dtype,
        "max_length": args.max_length,
        "limit_cases": args.limit_cases,
        "cases": cases,
        "top1_accuracy": sum(1 for row in rows if row["top1_pass"]) / max(1, cases),
        "recall_at_3": statistics.fmean(row["recall_at_3"] for row in rows) if rows else 0.0,
        "mrr": statistics.fmean(row["reciprocal_rank"] for row in rows) if rows else 0.0,
        "ndcg_at_3": statistics.fmean(row["ndcg_at_3"] for row in rows) if rows else 0.0,
        "recency_conflict_pass_rate": sum(1 for row in recency_rows if row["top1_pass"]) / max(1, len(recency_rows)),
        "distractor_resistance_pass_rate": sum(1 for row in distractor_rows if row["top1_pass"])
        / max(1, len(distractor_rows)),
        "rerank_latency_p50_s": percentile(latencies, 0.50),
        "rerank_latency_p95_s": percentile(latencies, 0.95),
    }


def render_markdown(summary: dict[str, Any], rows: list[dict[str, Any]], install_commands: list[str], error: str = "") -> str:
    lines = [
        f"# Qwen3 ONNX Transformers.js Smoke: {summary['run_id']}",
        "",
        f"Status: `{summary['status']}`",
        f"Model: `{summary['model']}`",
        f"Runtime: `{summary['runtime']}` / `{summary['npm_package']}`",
        f"Device: `{summary['device']}`",
        f"Dtype: `{summary['dtype']}`",
        f"Output: `{summary['output_dir']}`",
        "",
        "## Result",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Cases | {summary['cases']} |",
        f"| Top-1 accuracy | {summary['top1_accuracy']:.3f} |",
        f"| Recall@3 | {summary['recall_at_3']:.3f} |",
        f"| MRR | {summary['mrr']:.3f} |",
        f"| nDCG@3 | {summary['ndcg_at_3']:.3f} |",
        f"| Rerank latency p50 | {summary['rerank_latency_p50_s']:.3f}s |",
        "",
    ]
    if install_commands:
        lines.extend(["## Install Commands", "", "```bash", *install_commands, "```", ""])
    if error:
        lines.extend(["## Blocker", "", "```text", error.strip()[:4000], "```", ""])
    if rows:
        lines.extend(["## Cases", "", "| Case | Category | Top candidate | Pass |", "|---|---|---|---:|"])
        for row in rows:
            lines.append(f"| {row['id']} | {row['category']} | {row['top_candidate_id']} | {row['top1_pass']} |")
        lines.append("")
    return "\n".join(lines)


def enriched_rows(node_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in node_rows:
        ranked = row["ranked_candidates"]
        rows.append(
            {
                **row,
                "reciprocal_rank": reciprocal_rank(ranked),
                "ndcg_at_3": ndcg_at_k(ranked, 3),
                "recall_at_3": 1.0 if any(item["relevant"] for item in ranked[:3]) else 0.0,
                "rerank_latency_s": float(row.get("rerank_latency_s", 0.0) or 0.0),
            }
        )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", type=Path, default=DEFAULT_SUITE)
    parser.add_argument("--model-id", default=DEFAULT_MODEL)
    parser.add_argument("--tool-root", type=Path, default=default_tool_root())
    parser.add_argument("--output-root", type=Path, default=default_eval_root() / "mem0-reranking-benchmark")
    parser.add_argument("--cache-root", type=Path, default=storage_root() / "huggingface" / "transformers")
    parser.add_argument("--run-id")
    parser.add_argument("--install", action="store_true")
    parser.add_argument("--npm-package", default=DEFAULT_NPM_PACKAGE)
    parser.add_argument("--device", default="cpu", choices=("cpu", "webgpu"))
    parser.add_argument("--dtype", default="q4", choices=("q4", "q8", "fp32", "fp16"))
    parser.add_argument("--max-length", type=int, default=8192)
    parser.add_argument("--limit-cases", type=int, default=1)
    parser.add_argument("--instruction", default="Retrieve relevant memory")
    parser.add_argument("--timeout-s", type=float, default=900.0)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    node = shutil.which("node")
    npm = shutil.which("npm")
    run_id = args.run_id or f"qwen3-0-6b-onnx-transformersjs-bridge-{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}"
    output_dir = args.output_root / run_id
    plan = {
        "run_id": run_id,
        "node": node or "",
        "npm": npm or "",
        "suite": str(args.suite),
        "model": args.model_id,
        "tool_root": str(args.tool_root),
        "output_root": str(args.output_root),
        "output_dir": str(output_dir),
        "cache_root": str(args.cache_root),
        "install": args.install,
        "npm_package": args.npm_package,
        "device": args.device,
        "dtype": args.dtype,
        "limit_cases": args.limit_cases,
    }
    if args.dry_run:
        print(json.dumps(plan, indent=2))
        return 0 if node and npm else 2
    if not node or not npm:
        raise SystemExit("Node and npm are required for the Transformers.js bridge smoke.")

    suite = load_suite(args.suite)
    if args.limit_cases < 1 or args.limit_cases > len(suite):
        raise SystemExit(f"--limit-cases must be between 1 and {len(suite)}")

    output_dir.mkdir(parents=True, exist_ok=True)
    install_commands: list[str] = []
    started = time.time()
    status_code = 0
    error = ""
    rows: list[dict[str, Any]] = []
    summary: dict[str, Any]
    try:
        install_commands = ensure_tool_root(args.tool_root, args.install, args.npm_package)
        env = build_env(args.tool_root, args.cache_root)
        cmd = [
            node,
            str(JS_SMOKE),
            "--suite",
            str(args.suite),
            "--model-id",
            args.model_id,
            "--dtype",
            args.dtype,
            "--device",
            args.device,
            "--max-length",
            str(args.max_length),
            "--limit-cases",
            str(args.limit_cases),
            "--instruction",
            args.instruction,
            "--cache-dir",
            str(args.cache_root),
        ]
        completed = subprocess.run(
            cmd,
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            timeout=args.timeout_s,
            check=False,
        )
        (output_dir / "stdout.txt").write_text(completed.stdout, encoding="utf-8")
        (output_dir / "stderr.txt").write_text(completed.stderr, encoding="utf-8")
        if completed.returncode != 0:
            status_code = 3
            error = completed.stderr or completed.stdout or f"node exited {completed.returncode}"
            raise RuntimeError(error)
        payload = json.loads(completed.stdout)
        rows = enriched_rows(payload["cases"])
        summary = summarize_rows(rows, run_id, args, output_dir)
        summary["node_load_and_score_latency_s"] = payload.get("load_and_score_latency_s", 0.0)
        summary["token_yes"] = payload.get("token_yes")
        summary["token_no"] = payload.get("token_no")
    except Exception as exc:  # noqa: BLE001
        status_code = status_code or 3
        error = str(exc)
        summary = {
            "run_id": run_id,
            "created_at": datetime.now(UTC).isoformat(),
            "status": "blocked",
            "suite": str(args.suite),
            "output_dir": str(output_dir),
            "model": args.model_id,
            "runtime": "transformers.js",
            "npm_package": args.npm_package,
            "device": args.device,
            "dtype": args.dtype,
            "max_length": args.max_length,
            "limit_cases": args.limit_cases,
            "cases": 0,
            "top1_accuracy": 0.0,
            "recall_at_3": 0.0,
            "mrr": 0.0,
            "ndcg_at_3": 0.0,
            "recency_conflict_pass_rate": 0.0,
            "distractor_resistance_pass_rate": 0.0,
            "rerank_latency_p50_s": 0.0,
            "rerank_latency_p95_s": 0.0,
            "blocker": error,
        }
    summary["elapsed_s"] = round(time.time() - started, 6)
    summary["tool_root"] = str(args.tool_root)
    summary["cache_root"] = str(args.cache_root)
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (output_dir / "results.json").write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (output_dir / "summary.md").write_text(render_markdown(summary, rows, install_commands, error), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return status_code


if __name__ == "__main__":
    sys.exit(main())
