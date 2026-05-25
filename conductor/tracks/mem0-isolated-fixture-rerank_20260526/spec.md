# Spec: mem0 Isolated Fixture Rerank Gate

## Goal

Validate mem0 reranking on a real add/search path with multiple retrieved
candidates, while keeping the default mem0 configuration and collection
unchanged.

## Requirements

- Use only non-sensitive synthetic fixture memories.
- Write a temporary `MEM0_CONFIG_PATH` config for the benchmark run.
- Use an output-local Qdrant path and unique fixture collection.
- Compare vector ordering, `score_plus_created_at_rank_close_margin`, and warm
  `Qwen/Qwen3-Reranker-0.6B`.
- Record candidate counts, pass/top-1 metrics, recency and distractor rates,
  and latency.
- Do not edit `~/.mem0/config.json` or the default `mem0_nomic_768` collection.

## Non-Goals

- Do not promote a default mem0 read path automatically.
- Do not validate BGE-M3, ColBERT, or ONNX reranker runtime in this track.
