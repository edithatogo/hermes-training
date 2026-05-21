# Hermes Training Hub — Conductor Context

> **Role:** Orchestrator. This file defines the current mission, tracks, routing rules, and proof state for the Hermes agent model workspace.
> **Updated:** 2026-05-20

## Mission

Build, benchmark, package, and publish Hermes-ready model adapters, runtime recipes, and evaluation evidence for bleeding-edge model families across practical local and cloud-assisted platforms.

The purpose is **Hermes agents on frontier/edge-capable models**. The MacBook Pro M1 Max with 32GB unified memory is the first local execution lane, not the boundary of the project.

The project is no longer limited to dense models under 10B. It now covers:

- practical local fine-tunes: LFM2.5 1.2B, Qwen3 4B
- Hermes-aligned baselines and teachers: Hermes 4 14B
- frontier runtime targets: Qwen3.6 35B-A3B, Gemma 4 26B-A4B
- research/runtime targets: Qwen3-Next, BitNet, subquadratic/recursive/linear-attention families
- retrieval targets: LFM2-ColBERT and future embedding/reranking tracks
- cloud-assisted benchmark and teacher workflows on Azure when quota and cost guards pass

## Repo Map

```
hermes-training/                 # Hub: orchestration, platform lanes, model radar, benchmark/publication docs
├── CONDUCTOR.md                 # Hub conductor context
├── MODEL_CANDIDATES.yaml        # Machine-readable model radar
├── BENCHMARKING_PLAN.md         # Local benchmark gates
├── STANDARD_BENCHMARKS.md       # Standard benchmark matrix
├── DOCUMENTATION_PLAN.md        # GitHub/HF documentation requirements
├── APPLICATIONS.md              # Downstream uses and product directions
├── scripts/env.sh               # SSD-first runtime/cache defaults
├── scripts/validate_readiness.py
├── scripts/dataset_token_audit.py
│
├── gemma4/                      # Gemma/Qwen/Hermes dense/MoE fine-tune track
├── lfm2/                        # LFM/LFM2.5/Ministral fine-tune track
└── ollama-pack/                 # Ollama, GGUF, LM Studio, Hermes runtime packaging
```

## Tracks

### Track 1: `lfm2` — LFM/LFM2.5 Local Fine-Tune Track

| Attribute | Value |
|---|---|
| Primary proved target | `LiquidAI/LFM2.5-1.2B-Instruct` |
| Status | Smoke training passed, adapter saved locally |
| Proof | 10 MLX LoRA iterations, 5,462 trained tokens, peak ~3.6 GB |
| Next gate | Full-smoke-data run over current 219k-token train split |
| Priority | First practical training track |

### Track 2: `gemma4` — Gemma/Qwen/Hermes Baseline and Fine-Tune Track

| Attribute | Value |
|---|---|
| Practical target | `Qwen/Qwen3-4B-MLX-4bit` |
| Baseline/teacher target | `NousResearch/Hermes-4-14B` |
| Frontier runtime target | `Qwen/Qwen3.6-35B-A3B`, `google/gemma-4-26B-A4B-it` |
| Status | Configs and scripts ready; Qwen3 4B download needs authenticated/prefetched HF retry |
| Priority | Next after LFM full-smoke-data gate |

### Track 3: `ollama-pack` — Runtime Packaging

| Attribute | Value |
|---|---|
| Role | Package adapters/models for Ollama, LM Studio, MLX server, and Hermes |
| Status | Modelfiles and runtime smoke scripts exist |
| Next gate | Validate LFM2.5 smoke adapter through MLX runtime, then Ollama/LM Studio where supported |
| Priority | Begins after each adapter reaches a benchmark gate |

### Cross-Cutting Track: Benchmark and Publication

| Area | Status |
|---|---|
| Local benchmark gates | Documented in `BENCHMARKING_PLAN.md` |
| Standard benchmark matrix | Documented in `STANDARD_BENCHMARKS.md` |
| Documentation/release plan | Documented in `DOCUMENTATION_PLAN.md` |
| Current benchmark set | Seed-only; must expand before quality claims |
| HF/GitHub publication | Planned; no adapter should be published before benchmark promotion |

### Cross-Cutting Track: Platform Abstraction and Frontier Radar

| Area | Status |
|---|---|
| Product abstraction | Planned: separate Hermes-agent purpose from Mac/MLX implementation lane |
| Model radar | Planned: classify candidates by role, platform, feasibility, and promotion gate |
| Research watchlist | Planned: keep speculative models out of runnable tracks until verified |

### Cross-Cutting Track: Azure Scale-Out

| Area | Status |
|---|---|
| Account target | `d.a.mordaunt@gmail.com` Azure for Students, not current health.nsw.gov.au tenant |
| Use first | Benchmarks, teacher/evaluator runs, dataset review |
| Cost policy | Spot/low-priority, max one GPU job, autoscale to zero |
| Safety gate | Azure preflight must pass before any compute creation or job submission |

## Current Proof State

Completed:

- GitHub workspace moved to `/Volumes/PortableSSD/GitHub` with `/Users/doughnut/GitHub` symlink preserved.
- Shared SSD-first environment helper added: `scripts/env.sh`.
- Readiness validation passes.
- Model radar check confirms current candidate model IDs exist on Hugging Face, but role/platform/feasibility classification must be expanded.
- LFM2.5 1.2B smoke adapter trained and saved locally.
- Dataset token audit script added.
- Benchmark and documentation plans added.
- Qwen3 tool-call repair proof completed and documented. Strict benchmark remains blocked at 1/6, but diagnostic empty-think stripping identifies the next runtime-normalization fix.

Next queued track:

- Qwen3.6 and Hermes runtime proof from explicit SSD-backed artifacts or live endpoints. Qwen3.7 remains unsupported as a local lane until official public weights and runtime artifacts exist.

Known constraints:

- Internal disk remains tight; always source `scripts/env.sh` before downloads, training, evals, benchmark runs, and local Azure artifact sync.
- The current dataset is smoke-scale: `lfm2` train split is 461 conversations / 219,354 tokens.
- The successful LFM smoke run is a pipeline proof, not a quality proof.
- Qwen3 4B MLX download stalled unauthenticated; retry with `HF_TOKEN` or prefetch.

## Workflow Rules

1. **Route work to the owning track.**
   - `lfm2`: LFM/LFM2.5/Ministral local training and LFM retrieval planning.
   - `gemma4`: Gemma/Qwen/Hermes baseline, teacher, runtime, and adapter work.
   - `ollama-pack`: runtime packaging and Hermes integration.
   - hub root: benchmark, docs, platform lanes, Azure scale-out, model radar, environment, publication strategy.
2. **Use SSD-first environment defaults.**
   Run `source scripts/env.sh` before training/eval/benchmark work.
3. **Treat smoke results as pipeline proof only.**
   Do not publish quality claims without benchmark gates.
4. **Benchmark before promotion.**
   Hermes-local eval first, then standard suites appropriate to the gate.
5. **Keep artifacts out of Git.**
   Adapters, GGUFs, raw eval outputs, and local experiments stay ignored unless intentionally published.
6. **Commit/push in dependency order.**
   Commit nested track repos first, then update hub submodule pointers and hub docs.
7. **Hold tracks to health >= 9.5.**
   Every plan must include a health checkpoint before completion or publication.

## Key Decisions

| # | Decision | Rationale |
|---|---|---|
| D1 | MLX LoRA first for the Mac lane | Best local training path on Apple Silicon |
| D2 | SSD-first cache/temp/eval roots | Internal disk is too constrained for model work |
| D3 | Adapter-only publication by default | Safer licensing and smaller artifacts |
| D4 | Benchmark gates before publishing | Prevents mistaking smoke runs for quality gains |
| D5 | Hermes 4/Qwen3.6 as baselines/teachers first | Large models are useful locally even before fine-tuning |
| D6 | Keep Ollama, LM Studio, and MLX viable | Hermes should be runtime-flexible |
| D7 | Azure is a scale-out lane, not the product identity | Use cloud for speed, teacher runs, and broader benchmarks without weakening local deployment goals |
| D8 | Watchlist models require verification before track promotion | Bleeding-edge claims must be backed by weights, license, runtime path, and benchmark plan |

## Cross-Reference

| Document | Purpose |
|---|---|
| `README.md` | Quickstart and current state |
| `MODEL_CANDIDATES.yaml` | Model radar |
| `BENCHMARKING_PLAN.md` | Local benchmark gates and promotion criteria |
| `STANDARD_BENCHMARKS.md` | Standard benchmark suite for GitHub/HF reporting |
| `DOCUMENTATION_PLAN.md` | Release docs and model card requirements |
| `APPLICATIONS.md` | Downstream uses and product directions |
| `REPO_MAINTENANCE.md` | Commit/push and artifact policy |
| `NEW_MODEL_WORKFLOW.md` | Adding a model track |
