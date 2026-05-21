# Run Card: Qwen3 4B Strict Tool-Call Heldout

## Identity

- Run name: `qwen3-4b-strict-toolcall`
- Date: 2026-05-22
- Operator: Codex
- Repo: `github.com/edithatogo/hermes-training`
- Publication target: GitHub documentation only
- Platform lane: Mac/MLX local Hermes agent lane

## Model Provenance

- Base model: `Qwen/Qwen3-4B-MLX-4bit`
- Adapter path: `gemma4/experiments/qwen3-4b-strict-toolcall/lora_adapter`
- Adapter type: MLX LoRA
- Redistribution status: local artifact only, not publishable

## Training Setup

- Config file: `gemma4/scripts/train_config.qwen3-4b.strict-toolcall.yaml`
- Training data: `gemma4/data/strict_tool_call/splits`
- Train split: 8 rows
- Validation split: 1 row
- Test split: 1 row
- Command: `source scripts/env.sh && cd gemma4 && ../.venv/bin/python scripts/train.py --config scripts/train_config.qwen3-4b.strict-toolcall.yaml`
- Iterations: 80
- Effective trained tokens: 28,020
- Final validation loss: 0.949
- Best observed validation loss: 0.762 at iteration 40
- Peak memory: 3.785 GB
- Wall time: 119.6 seconds
- Cache / output root: `/Volumes/PortableSSD`

## Evaluation Summary

Mirrored regression suite:

- Command: `source scripts/env.sh && ./.venv/bin/python scripts/run_tool_call_benchmark.py --model Qwen/Qwen3-4B-MLX-4bit --adapter gemma4/experiments/qwen3-4b-strict-toolcall/lora_adapter --suite benchmarks/tool_call_local/suite.json --user-prefix /no_think --run-id qwen3-4b-strict-toolcall-mirrored-nothink-20260522 --max-tokens 512`
- Raw output: `/Volumes/PortableSSD/hermes-evals/tool-call-benchmark/qwen3-4b-strict-toolcall-mirrored-nothink-20260522`
- Strict pass rate: 0.167
- Diagnostic empty-think-stripped pass rate: 1.000
- Strict failures rescued only by empty-think stripping: 5

Held-out publication gate:

- Command: `source scripts/env.sh && ./.venv/bin/python scripts/run_tool_call_benchmark.py --model Qwen/Qwen3-4B-MLX-4bit --adapter gemma4/experiments/qwen3-4b-strict-toolcall/lora_adapter --suite benchmarks/tool_call_local/heldout_suite.json --user-prefix /no_think --run-id qwen3-4b-strict-toolcall-heldout-nothink-20260522 --max-tokens 512`
- Raw output: `/Volumes/PortableSSD/hermes-evals/tool-call-benchmark/qwen3-4b-strict-toolcall-heldout-nothink-20260522`
- Strict pass rate: 0.250
- Strict JSON validity rate: 0.000
- Strict argument correctness rate: 0.667
- Invalid-tool handling rate: 1.000
- Multi-turn repair rate: 0.000
- Diagnostic empty-think-stripped pass rate: 0.750
- Diagnostic JSON validity after empty-think stripping: 0.833
- Strict failures rescued only by empty-think stripping: 4

## Decision

Do not publish this adapter to Hugging Face. The run proves the runtime normalizer can make mirrored regression outputs parseable, but it does not generalize enough for the held-out publication gate.

Primary blockers:

- Qwen still emits a leading empty `<think></think>` wrapper in every held-out response.
- One held-out multi-turn repair case emitted malformed JSON containing an invalid stray character.
- One held-out argument-correctness case used semantically similar text that did not exactly match the expected argument.
- Held-out strict pass rate is 0.250, far below the required 1.000.

Next implementation should expand strict training data beyond 10 examples, add held-out-like repair cases to training without contaminating the held-out suite, and consider stopping around the earlier validation-loss minimum rather than the final overfit checkpoint.
