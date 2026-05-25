# Spec: Qwen3 0.6B Live mem0 Rerank Wrapper

## Goal

Extend the read-only mem0 rerank wrapper so it can run live `mem0 search`
results through the validated `Qwen/Qwen3-Reranker-0.6B` causal-LM scorer.

## Requirements

- Keep the live mem0 defaults unchanged.
- Keep Hugging Face, Ollama, and benchmark artifacts on `/Volumes/PortableSSD`.
- Preserve the existing heuristic wrapper strategies.
- Require an explicit model id for learned reranking.
- Report mem0 search latency, rerank scoring latency, and total one-shot
  latency separately.
- Document whether the path is ready for promotion.

## Non-Goals

- Do not switch `~/.mem0/config.json`.
- Do not promote the ONNX artifact until a real ONNX/Transformers.js bridge is
  proven.
- Do not treat one-shot CLI latency as representative of a warm service.
