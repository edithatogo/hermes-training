# Qwen3 4B Hermes Smoke Adapter

## Model Details

- Model name: `qwen3-4b-hermes-smoke`
- Base model: `Qwen/Qwen3-4B-MLX-4bit`
- Adapter type: LoRA
- Base revision: HF `main` as cached in `/Volumes/PortableSSD/huggingface/hub`
- Adapter revision: local smoke artifact, not published
- Platform lane: Mac/MLX local Hermes agent lane
- License: check upstream Qwen model card before derivative publication
- Intended use: local Hermes-agent smoke validation and runtime packaging development
- Not intended for: quality claims, production use, public benchmark claims, or merged-weight redistribution

## Training Summary

- Training config: `gemma4/scripts/train_config.qwen3-4b.smoke.yaml`
- Dataset card: pending
- Dataset revision: repo-local smoke splits
- Train tokens: 2,889
- Iterations: 10
- Hardware: MacBook Pro M1 Max, 32GB unified memory
- Runtime: MLX-LM
- Peak memory: 3.944 GB
- Wall time: 20.0 seconds after model download

## Evaluation

| Benchmark | Result | Notes |
|---|---:|---|
| Hermes-local | pass | 100 prompts, no empty responses |
| Standard benchmark suite | not run | Required before any quality claim |
| Tool-call / JSON validity | pass | MLX server JSON smoke passed with `/no_think` |
| Validation loss | 2.386 | Smoke run only |
| Latency | 2.397s avg | Adapter eval over 100 prompts |

- Benchmark command: see `gemma4/eval/qwen3-4b-smoke-summary.md`
- Benchmark harness version / commit: `gemma4` `5e94491`
- Prompt set hash or revision: summary hash `46cb480d1739ee45f6bd72838709b3af1c7221224dae350e15894f49fc6eacc6`
- Raw outputs or eval artifacts: `gemma4/eval/qwen3-4b-*-results.jsonl`, `gemma4/eval/qwen3-4b-*-report.html`

## Runtime Instructions

- MLX: `python -m mlx_lm.server --model Qwen/Qwen3-4B-MLX-4bit --adapter-path gemma4/experiments/qwen3-4b-smoke/lora_adapter --host 127.0.0.1 --port 8088`
- Ollama: not validated for this package; safetensors and GGUF paths both failed on this machine
- LM Studio: load `/Volumes/PortableSSD/hermes-exports/ollama/qwen3-4b-hermes-smoke/qwen3-4b-hermes-smoke-q4_K_M.gguf`
- Other runtime: direct llama.cpp `llama-completion` passed
- Smoke command: `BASE_URL=http://127.0.0.1:8088/v1 SMOKE_PROMPT='/no_think Return exactly this JSON object and nothing else: {"ok": true}' ollama-pack/scripts/runtime_smoke.sh Qwen/Qwen3-4B-MLX-4bit`

## Dataset and Provenance

- Dataset source: repo-local Hermes smoke data
- Filters: smoke-only prompt/response curation
- Split counts: see `gemma4/data/splits/`
- Token counts: 2,889 trained tokens
- Corpus or index digest: not applicable
- Artifact links: local only

## Limitations

- This is a smoke proof, not a publishable model-quality run.
- Training data volume is intentionally tiny.
- Standard benchmarks were not run.
- Qwen3 thinking mode needs `/no_think` for strict JSON runtime smoke.
- Ollama is not validated for this Qwen3 package yet.
- Upstream license must be checked before public adapter or GGUF publication.

## Publication Notes

- GitHub commit: pending next hub commit
- Hugging Face repo: not created
- Human review status: pending

## Citation

- Repository: `github.com/edithatogo/hermes-training`
- Paper or report: not applicable
- Contact: repo owner
