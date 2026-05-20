# Run Card: Qwen3 4B Hermes Smoke

## Identity

- Run name: `qwen3-4b-smoke`
- Date: 2026-05-21
- Operator: Codex
- Repo: `github.com/edithatogo/hermes-training`
- Git commit: hub `bf0664c` before this documentation pass, `gemma4` `5e94491`, `ollama-pack` `19c84fd`
- Track or ticket: `qwen3-smoke_20260520`, `runtime-packaging_20260520`
- Publication target: GitHub documentation first; Hugging Face adapter publication only after a non-smoke benchmark gate
- Platform lane: Mac/MLX local Hermes agent lane

## Model Provenance

- Base model: `Qwen/Qwen3-4B-MLX-4bit`
- Base revision: HF `main` as cached in `/Volumes/PortableSSD/huggingface/hub`
- Adapter or checkpoint path: `gemma4/experiments/qwen3-4b-smoke/lora_adapter`
- Adapter revision: local smoke artifact, not published
- Model family: Qwen3 dense chat/reasoning model
- License: check upstream Qwen model card before derivative publication
- Redistribution limits: adapter-only publication preferred; merged weights/GGUF only if upstream license allows

## Training Setup

- Config file: `gemma4/scripts/train_config.qwen3-4b.smoke.yaml`
- Command: `source scripts/env.sh && cd gemma4 && ../.venv/bin/python scripts/train.py --config scripts/train_config.qwen3-4b.smoke.yaml`
- Hardware: MacBook Pro M1 Max, 32GB unified memory
- Runtime: MLX-LM
- Precision: 4-bit MLX base with LoRA adapter
- Batch size: see config
- Gradient accumulation: see config
- Max sequence length: see config
- Train tokens: 2,889
- Iterations: 10
- Wall time: 20.0 seconds after model download
- Peak memory: 3.944 GB
- Cache / output root: `/Volumes/PortableSSD`

## Dataset Provenance

- Dataset name: Hermes smoke dataset
- Dataset revision: repo-local smoke splits
- Dataset card: planned before HF dataset publication
- Split counts: see `gemma4/data/splits/`
- Token counts: training run recorded 2,889 trained tokens
- Filters applied: smoke-only Hermes prompt/response curation
- Known limitations: too small for quality claims or publication-grade fine-tuning

## Evaluation Summary

- Hermes-local benchmark: 100 prompts, base and adapter both completed without empty responses
- Standard benchmark suite: not run for this smoke artifact
- Base-vs-adapter comparison: adapter average latency `2.397s`; base average latency `2.151s`
- Benchmark command: recorded in `gemma4/eval/qwen3-4b-smoke-summary.md`
- Benchmark harness version / commit: repo `gemma4` `5e94491`
- Prompt set hash or revision: `gemma4/eval/prompts.jsonl`; summary hash `46cb480d1739ee45f6bd72838709b3af1c7221224dae350e15894f49fc6eacc6`
- Validation loss: 2.386
- Tool-call / JSON validity: response-collapse gate passed; runtime JSON smoke passed through MLX server with `/no_think`
- Latency: adapter average `2.397s` over 100 prompts
- Throughput: GGUF direct llama.cpp smoke reported about `332` prompt tok/s and `69` generation tok/s
- Raw output location: `gemma4/eval/qwen3-4b-*-results.jsonl` and `gemma4/eval/qwen3-4b-*-report.html`
- Manual review notes: smoke proof only; no quality claim

## Runtime Validation

- MLX: passed through `python -m mlx_lm.server --model Qwen/Qwen3-4B-MLX-4bit --adapter-path gemma4/experiments/qwen3-4b-smoke/lora_adapter --host 127.0.0.1 --port 8088`
- Ollama: blocked; safetensors chat produced HTTP 500, GGUF create dropped the daemon during model creation
- LM Studio: ready to test from validated GGUF artifact
- Other runtime: direct llama.cpp `llama-completion` passed against Q4_K_M GGUF
- Smoke command: `BASE_URL=http://127.0.0.1:8088/v1 SMOKE_PROMPT='/no_think Return exactly this JSON object and nothing else: {"ok": true}' ollama-pack/scripts/runtime_smoke.sh Qwen/Qwen3-4B-MLX-4bit`
- Runtime notes: see `ollama-pack/runtime-card.qwen3-4b-mlx-smoke.md`

## Publication Notes

- GitHub commit or release: committed/pushed track commits exist; this run card should be committed with the next hub update
- Hugging Face repo: not created for this smoke adapter
- Artifact locations: adapter under ignored `gemma4/experiments/`; GGUFs under `/Volumes/PortableSSD/hermes-exports/ollama/qwen3-4b-hermes-smoke`
- Files published: documentation only
- Score provenance recorded: yes, for smoke metrics only
- License notes: upstream license check required before HF adapter or GGUF publication
- Human review status: pending

## Follow-Up

- [x] Confirm all paths and revisions are exact
- [x] Attach raw outputs or links to reports
- [x] Verify publication target is permitted by license before release
- [x] Record next decision: expand training only after early response gate remains stable
