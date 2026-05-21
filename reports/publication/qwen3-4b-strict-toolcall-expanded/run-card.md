# Run Card: Qwen3 4B Strict Tool-Call Expanded Retrain

## Identity

- Run name: `qwen3-4b-strict-toolcall-expanded`
- Date: 2026-05-22
- Operator: Codex
- Repo: `github.com/edithatogo/hermes-training`
- Publication target: GitHub documentation only
- Platform lane: Mac/MLX local Hermes agent lane
- Current status: BLOCKED

## Model Provenance

- Base model: `Qwen/Qwen3-4B-MLX-4bit`
- Adapter path: `gemma4/experiments/qwen3-4b-strict-toolcall-expanded/lora_adapter`
- Adapter type: MLX LoRA
- Redistribution status: local artifact only until publication gate passes

## Expanded Data Audit

- Data path: `gemma4/data/strict_tool_call`
- Split generation command: `cd gemma4 && python3 data/strict_tool_call/tools/materialize_expanded_splits.py`
- Data revision or commit: `d242265` in `hermes-gemma-lab`
- Train rows: 33
- Validation rows: 4
- Test rows: 5
- Dataset token audit command: `source scripts/env.sh && HF_HUB_OFFLINE=1 ./.venv/bin/python scripts/dataset_token_audit.py --model Qwen/Qwen3-4B-MLX-4bit --data gemma4/data/strict_tool_call/expanded_splits_v1 --splits train val valid test --output reports/publication/qwen3-4b-strict-toolcall-expanded/dataset-token-audit.json`
- Dataset token audit output: `reports/publication/qwen3-4b-strict-toolcall-expanded/dataset-token-audit.json`
- Dataset token summary: train 9,081; val 1,026; valid 1,026; test 1,314
- Training token evidence: MLX training run recorded 33,133 effective tokens
- Tool coverage summary: 78 declared tool names across expanded split audit
- Behavior buckets covered: `json_validity`, `argument_correctness`, `invalid_tool_handling`, `multi_turn_repair`
- Held-out overlap check against `benchmarks/tool_call_local/heldout_suite.json`: 0 user prompt overlap, 0 declared tool-name overlap, 0 assistant tool-name overlap for `raw/expansion_seed_v1.jsonl`
- License and redistribution notes: `reports/publication/qwen3-4b-strict-toolcall-expanded/license-review.md`
- Audit decision: passed for local retraining

## Training Setup

- Config file: `gemma4/scripts/train_config.qwen3-4b.strict-toolcall-expanded.yaml`
- Training data: `gemma4/data/strict_tool_call/expanded_splits_v1`
- Command: `source scripts/env.sh && cd gemma4 && ../.venv/bin/python scripts/train.py --config scripts/train_config.qwen3-4b.strict-toolcall-expanded.yaml`
- Iterations: 120
- Effective trained tokens: 33,133
- Final validation loss: 0.917
- Best observed validation loss: 0.795 at iteration 50
- Peak memory: 3.785 GB
- Wall time: 172.6 seconds
- Cache / output root: `/Volumes/PortableSSD`
- Raw training log path: terminal transcript only

## Evaluation Summary

Held-out publication gate:

- Command: `source scripts/env.sh && ./.venv/bin/python scripts/run_tool_call_benchmark.py --model Qwen/Qwen3-4B-MLX-4bit --adapter gemma4/experiments/qwen3-4b-strict-toolcall-expanded/lora_adapter --suite benchmarks/tool_call_local/heldout_suite.json --user-prefix /no_think --run-id qwen3-4b-strict-toolcall-expanded-heldout-nothink-20260522 --max-tokens 512`
- Raw output: `/Volumes/PortableSSD/hermes-evals/tool-call-benchmark/qwen3-4b-strict-toolcall-expanded-heldout-nothink-20260522`
- Strict pass rate: 0.250
- Strict JSON validity rate: 0.000
- Strict argument correctness rate: 1.000
- Invalid-tool handling rate: 1.000
- Multi-turn repair rate: 0.000
- Diagnostic empty-think-stripped pass rate: informational only, 0.750
- Strict failures rescued only by empty-think stripping: informational only, 4

Best validation-loss checkpoint:

- Adapter path: `gemma4/experiments/qwen3-4b-strict-toolcall-expanded/lora_adapter_iter50`
- Held-out strict pass rate: 0.125
- Held-out diagnostic empty-think-stripped pass rate: 0.500
- Decision: final checkpoint was better on held-out strict pass.

## Decision

Publication status: BLOCKED. Expanded training completed, but held-out strict pass rate was 0.250.

Primary blockers:

- Strict JSON validity is still 0.000 because empty thinking wrappers remain in tool-call outputs.
- Multi-turn repair remains 0.000.
- Held-out strict pass rate is below the required `1.000`.
- Dataset publication scope is not approved.
- License and redistribution review blocks Hugging Face publication pending upstream and mirrored-seed review.
