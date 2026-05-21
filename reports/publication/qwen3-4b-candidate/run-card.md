# Run Card: Qwen3 4B Hermes Candidate

## Identity

- Run name: `qwen3-4b-candidate`
- Date: 2026-05-22
- Operator: Codex
- Repo: `github.com/edithatogo/hermes-training`
- Track or ticket: `gemma4/conductor/tracks/qwen3-candidate_20260522`
- Publication target: internal/GitHub documentation only
- Platform lane: Mac/MLX local Hermes agent lane

## Model Provenance

- Base model: `Qwen/Qwen3-4B-MLX-4bit`
- Base revision: HF `main` as cached in `/Volumes/PortableSSD/huggingface/hub`
- Adapter path: `gemma4/experiments/qwen3-4b-candidate/lora_adapter`
- Model family: Qwen3 dense chat/reasoning model
- Redistribution limits: adapter-only publication preferred; do not publish this candidate as a quality artifact

## Training Setup

- Config file: `gemma4/scripts/train_config.qwen3-4b.candidate.yaml`
- Command: `source ../scripts/env.sh && ../.venv/bin/python scripts/train.py --config scripts/train_config.qwen3-4b.candidate.yaml`
- Hardware: MacBook Pro M1 Max, 32GB unified memory
- Runtime: MLX-LM
- Train tokens: 25,094
- Iterations: 60
- Wall time: 192.1 seconds after model load
- Peak memory: 3.962 GB
- Cache / output root: `/Volumes/PortableSSD`

## Evaluation Summary

- Hermes-local benchmark: 100 prompts, no empty responses
- Response-collapse gate: passed with average 91.60 words and 0.000 empty rate
- Validation loss: 2.248 final validation loss
- Latency: 2.49s average over 100 prompts
- Tool-call benchmark: failed strict local tool-call shape; 1/6 pass rate with `/no_think`
- Raw Hermes eval outputs: ignored `gemma4/eval/qwen3-4b-candidate-results.jsonl` and `gemma4/eval/qwen3-4b-candidate-report.html`
- Tool-call outputs: `/Volumes/PortableSSD/hermes-evals/tool-call-benchmark/qwen3-4b-candidate-toolcall-nothink-20260522`

## Runtime Validation

- MLX adapter load: passed through local evaluation script
- Ollama: still blocked for Qwen3 package, as documented in the runtime card
- LM Studio: helper added; endpoint test pending because LM Studio is not installed/running in this environment

## Decision

Do not publish this adapter as a quality model. It is a stronger local training proof than the 2,889-token smoke run, but it does not improve strict tool-call behavior. The next run should add explicit tool-call target examples and use `scripts/run_tool_call_benchmark.py` as an early stopping gate.
