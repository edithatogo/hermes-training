# Run Card: Qwen3 4B Tool-Call Repair Proof

## Identity

- Run name: `qwen3-4b-toolcall-repair`
- Date: 2026-05-22
- Operator: Codex
- Repo: `github.com/edithatogo/hermes-training`
- Publication target: GitHub documentation only
- Platform lane: Mac/MLX local Hermes agent lane

## Model Provenance

- Base model: `Qwen/Qwen3-4B-MLX-4bit`
- Adapter path: `gemma4/experiments/qwen3-4b-toolcall-repair/lora_adapter`
- Adapter type: MLX LoRA
- Redistribution status: local artifact only, not publishable

## Training Setup

- Config file: `gemma4/scripts/train_config.qwen3-4b.toolcall-repair.yaml`
- Data path: `gemma4/data/tool_call_splits`
- Data source: generated from `benchmarks/tool_call_local/suite.json`
- Iterations: 40
- Effective trained tokens: 10,603
- Final validation loss: 0.140
- Peak memory: 3.417 GB
- Wall time: 59.0 seconds
- Cache / output root: `/Volumes/PortableSSD`

## Evaluation Summary

- Benchmark command: `source scripts/env.sh && ./.venv/bin/python scripts/run_tool_call_benchmark.py --model Qwen/Qwen3-4B-MLX-4bit --adapter gemma4/experiments/qwen3-4b-toolcall-repair/lora_adapter --user-prefix /no_think --run-id qwen3-4b-toolcall-repair-nothink-20260522 --max-tokens 512`
- Strict local tool-call pass rate: 1/6, 0.167
- Strict JSON validity rate: 0.000
- Strict argument correctness rate: 0.800
- Invalid-tool handling rate: 1.000
- Multi-turn repair rate: 0.000
- Diagnostic pass rate after stripping only an empty leading `<think></think>` wrapper: 5/6, 0.833
- Diagnostic JSON validity after empty-think stripping: 0.800
- Diagnostic argument correctness after empty-think stripping: 0.800
- Raw output: `/Volumes/PortableSSD/hermes-evals/tool-call-benchmark/qwen3-4b-toolcall-repair-nothink-20260522`
- Rescore output with diagnostic metrics: `/Volumes/PortableSSD/hermes-evals/tool-call-benchmark/qwen3-4b-toolcall-repair-nothink-20260522-rescore`

## Decision

This run demonstrates that the model can learn the target tool arguments from a tiny strict set, but it is not publishable. The strict gate still fails because Qwen emits an empty thinking wrapper and one multi-call case emits malformed tags.

Next implementation should add a Hermes runtime normalizer that removes only empty leading thinking wrappers before tool-call parsing, then train against the richer `gemma4/data/strict_tool_call` lane and evaluate on `benchmarks/tool_call_local/heldout_suite.json`.
