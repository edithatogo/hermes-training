#!/usr/bin/env python3
"""Smoke a mem0 profile by adding and searching one or more raw memories."""
from __future__ import annotations

import argparse
import json
import os
import site
import sys
import time
from pathlib import Path
from typing import Any


def prepare_import_path() -> None:
    mem0_dir = Path.home() / ".mem0"
    if mem0_dir.exists():
        sys.path.insert(0, str(mem0_dir))
    user_site = site.getusersitepackages()
    if user_site and user_site not in sys.path:
        sys.path.append(user_site)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--user-id", default="profile_smoke_user")
    parser.add_argument("--agent-id", default="embeddinggemma_profile_smoke")
    parser.add_argument(
        "--memory",
        action="append",
        default=[],
        help="Memory text to add. Can be repeated.",
    )
    parser.add_argument("--query", required=True)
    parser.add_argument("--must-contain", action="append", default=[])
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def normalize_results(raw: Any) -> list[dict[str, Any]]:
    if isinstance(raw, dict) and isinstance(raw.get("results"), list):
        return [item for item in raw["results"] if isinstance(item, dict)]
    if isinstance(raw, list):
        return [item for item in raw if isinstance(item, dict)]
    return []


def main() -> int:
    args = parse_args()
    if not args.memory:
        raise SystemExit("at least one --memory is required")
    os.environ["MEM0_CONFIG_PATH"] = str(args.config)
    prepare_import_path()
    from mem0_wrapper import add_memory, search_memory  # type: ignore

    started = time.perf_counter()
    add_latencies: list[float] = []
    for index, memory in enumerate(args.memory):
        add_started = time.perf_counter()
        add_memory(
            memory,
            user_id=args.user_id,
            agent_id=args.agent_id,
            metadata={"smoke_index": index, "source": "smoke_mem0_profile"},
            infer=False,
        )
        add_latencies.append(time.perf_counter() - add_started)
    search_started = time.perf_counter()
    raw_results = search_memory(args.query, user_id=args.user_id, agent_id=args.agent_id, limit=args.limit)
    search_latency = time.perf_counter() - search_started
    results = normalize_results(raw_results)
    memories = [str(item.get("memory", "")) for item in results if isinstance(item, dict)]
    joined = "\n".join(memories).lower()
    missing = [needle for needle in args.must_contain if needle.lower() not in joined]
    summary: dict[str, Any] = {
        "status": "failed" if missing else "passed",
        "config": str(args.config),
        "user_id": args.user_id,
        "agent_id": args.agent_id,
        "added": len(args.memory),
        "query": args.query,
        "result_count": len(results),
        "must_contain": args.must_contain,
        "missing": missing,
        "latency": {
            "total_s": time.perf_counter() - started,
            "add_s": add_latencies,
            "search_s": search_latency,
        },
        "results": results,
    }
    text = json.dumps(summary, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
