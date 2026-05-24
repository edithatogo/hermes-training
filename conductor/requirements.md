# Requirements — Hermes Training Hub

## Scope

Organize, train, benchmark, package, and publish Hermes-ready model adapters and runtime recipes across constrained local platforms and cloud-assisted scale-out lanes.

## Must Have

| ID | Requirement | Owner | Verification |
|---|---|---|---|
| M1 | Proper Conductor structure for hub and nested tracks | hub | `scripts/validate_readiness.py` checks core Conductor files |
| M2 | SSD-first model, dataset, temp, benchmark caches, and source/artifact separation | hub | `source scripts/env.sh` points paths at `/Volumes/PortableSSD`; `scripts/check_storage_layout.py` validates Git checkouts stay under `GitHub` |
| M3 | MLX LoRA training pipeline for practical local models | `lfm2`, `gemma4` | smoke training reaches adapter save |
| M4 | Dataset token audit before training claims | hub, tracks | `scripts/dataset_token_audit.py` output recorded |
| M5 | Benchmark gate before publishing | hub, tracks | local and standard benchmark results attached to run/model card |
| M6 | Adapter artifacts excluded from Git | all tracks | `.gitignore` covers `experiments/`, `*.safetensors`, exports |
| M7 | Runtime path for Hermes | `ollama-pack` | MLX/Ollama/LM Studio smoke documented |
| M8 | GitHub/Hugging Face publication plan | hub | `DOCUMENTATION_PLAN.md` and track release docs |
| M9 | Platform lanes separate purpose from environment | hub | docs and model radar classify Mac, Azure, runtime, retrieval, and research lanes |
| M10 | Azure preflight before cloud work | hub | account, subscription, region, quota, extension, and cost policy checked before compute |

## Should Have

| ID | Requirement | Owner | Priority |
|---|---|---|---|
| S1 | Expanded 100+ prompt Hermes-local benchmark | hub | High |
| S2 | Standard benchmark matrix with `lm-eval`, BFCL, IFEval, coding, RULER, safety | hub | High |
| S3 | LFM2.5 full-smoke-data training over current checked-in data | `lfm2` | High |
| S4 | Qwen3 4B authenticated/prefetched smoke training | `gemma4` | High |
| S5 | Run-card and model-card templates | hub | High |
| S6 | Runtime cards for MLX, Ollama, LM Studio | `ollama-pack` | Medium |
| S7 | Retrieval track plan for LFM2-ColBERT | future | Medium |
| S8 | Frontier model radar with role/platform/feasibility fields | hub | High |
| S9 | Cloud teacher/evaluator workflow for Hermes 4/Qwen3.6/Gemma | hub | High |

## Could Have

| ID | Requirement | Owner | Value |
|---|---|---|---|
| C1 | Teacher/evaluator workflow using Hermes 4 or Qwen3.6 | hub | High |
| C2 | Long-context benchmark track for recursive/subquadratic models | hub | Medium |
| C3 | Automated model radar refresh | hub | Medium |
| C4 | MTEB/retrieval benchmark track | future retrieval repo | Medium |
| C5 | Runtime bakeoff across MLX/Ollama/LM Studio | `ollama-pack` | Medium |
| C6 | Watchlist for speculative recursive/subquadratic/MTP/MoE releases | hub | Medium |

## Won't Have For Current Iteration

| ID | Requirement | Reason |
|---|---|
| W1 | Full pretraining from scratch | Not feasible on this hardware |
| W2 | Publishing smoke adapters as quality-improved models | Smoke proves plumbing only |
| W3 | Local fine-tuning large MoE frontier models by default | Runtime/teacher first until memory proof exists |
| W4 | Large artifacts committed to Git | Use SSD/Hugging Face release paths |
| W5 | Cloud spend without explicit preflight and cost caps | Azure hours do not guarantee GPU quota or capacity |
