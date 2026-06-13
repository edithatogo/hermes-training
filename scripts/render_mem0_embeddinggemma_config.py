#!/usr/bin/env python3
"""Render an opt-in mem0 config for EmbeddingGemma over an OpenAI endpoint."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

DEFAULT_MODEL = "embeddinggemma-300m-qat-Q4_0.gguf"
DEFAULT_BASE_URL = "http://127.0.0.1:8105/v1"
DEFAULT_COLLECTION = "mem0_embeddinggemma_300m_768"
DEFAULT_DIMS = 768


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected JSON object")
    return data


def resolve_eval_root() -> Path:
    if os.environ.get("HERMES_EVAL_ROOT"):
        return Path(os.environ["HERMES_EVAL_ROOT"])
    if os.environ.get("HERMES_STORAGE_ROOT"):
        return Path(os.environ["HERMES_STORAGE_ROOT"]) / "hermes-evals"
    if Path("/Volumes/PortableSSD").exists():
        return Path("/Volumes/PortableSSD") / "hermes-evals"
    return Path.cwd() / ".local-storage" / "hermes-evals"


def render_config(
    base_config: dict[str, Any],
    *,
    collection_name: str,
    qdrant_path: Path,
    history_db_path: Path,
    base_url: str,
    model: str,
    dims: int,
    api_key: str,
) -> dict[str, Any]:
    config = dict(base_config)
    vector_store = dict(config.get("vector_store") or {})
    vector_config = dict(vector_store.get("config") or {})
    vector_store["provider"] = "qdrant"
    vector_config.update(
        {
            "collection_name": collection_name,
            "embedding_model_dims": dims,
            "path": str(qdrant_path),
            "on_disk": True,
        }
    )
    vector_store["config"] = vector_config
    config["vector_store"] = vector_store
    config["embedder"] = {
        "provider": "openai",
        "config": {
            "model": model,
            "embedding_dims": dims,
            "openai_base_url": base_url.rstrip("/"),
            "api_key": api_key,
        },
    }
    config["history_db_path"] = str(history_db_path)
    config["version"] = str(config.get("version") or "v1.1")
    return config


def parse_args() -> argparse.Namespace:
    default_root = resolve_eval_root() / "mem0-profiles" / "embeddinggemma-300m-qat-gguf"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-config", type=Path, default=Path.home() / ".mem0" / "config.json")
    parser.add_argument("--output", type=Path, default=default_root / "config.json")
    parser.add_argument("--collection-name", default=DEFAULT_COLLECTION)
    parser.add_argument("--qdrant-path", type=Path, default=default_root / "qdrant")
    parser.add_argument("--history-db-path", type=Path, default=default_root / "history.db")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--embedding-dims", type=int, default=DEFAULT_DIMS)
    parser.add_argument("--api-key", default="local-profile")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.embedding_dims <= 0:
        raise SystemExit("--embedding-dims must be > 0")
    base_config = load_json(args.base_config)
    config = render_config(
        base_config,
        collection_name=args.collection_name,
        qdrant_path=args.qdrant_path,
        history_db_path=args.history_db_path,
        base_url=args.base_url,
        model=args.model,
        dims=args.embedding_dims,
        api_key=args.api_key,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
