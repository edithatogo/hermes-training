# Hermes Training Hub — Conductor Tracks

> **Role:** Orchestrator. This document defines the mission, tracks, and routing rules for all work in this workspace.
> **Load these skills when working here:** `kanban-orchestrator`, `kanban-worker`, `writing-plans`

---

## Mission

Train Hermes-style fine-tunes of multiple small language models (<10B params) on a MacBook Pro M1 Max (32GB RAM, portable SSD), deploy to Ollama, and publish reproducible artifacts to GitHub and Hugging Face.

## Repo Map

```
hermes-training/                          # Hub — orchestrator docs live here
├── CONDUCTOR.md                          # ← you are here
├── REQUIREMENTS.md                       # MoSCoW requirements
├── DESIGN.md                             # Architecture + Mermaid diagrams
├── CONTRACTS.md                          # Interface contracts
├── README.md                             # Quickstart
│
├── gemma4/                               # Gemma 4 E4B-it fine-tune track
│   ├── CONDUCTOR.md                      # Track-specific conductor
│   ├── scripts/                          # Pipeline scripts
│   ├── data/                             # Training data
│   ├── experiments/                      # Training outputs
│   ├── eval/                             # Eval prompts + results
│   ├── exports/                          # HF publishing artifacts
│   └── modelfiles/                       # Ollama Modelfiles
│
├── lfm2/                                 # LFM2-8B-A1B fine-tune track
│   └── (same structure as gemma4/)
│
└── ollama-pack/                          # Ollama packaging track
    ├── modelfiles/                       # All Modelfiles
    └── scripts/                          # Packaging scripts
```

## Tracks

### Track 1: gemma4 — Gemma 4 E4B-it Hermes Fine-Tune

| Attribute | Value |
|-----------|-------|
| Base model | `google/gemma-4-E4B-it` |
| Params | 4B (all active, MoE) |
| License | Apache 2.0 — publishable |
| Status | Model downloading → training queued |
| Priority | PRIMARY (first to complete) |

**Data:** Hermes-3-Dataset + hermes-function-calling-v1 → deduped → 80/10/10 split

### Track 2: lfm2 — LFM2-8B-A1B Hermes Fine-Tune

| Attribute | Value |
|-----------|-------|
| Base model | `LiquidAI/LFM2-8B-A1B` |
| Params | 8B (1B active, MoE) |
| License | Other — check before publishing weights |
| Status | Scaffolded, dataset downloading |
| Priority | SECONDARY (starts after gemma4 pipeline proven) |

### Track 3: ollama-pack — Packaging & Deployment

| Attribute | Value |
|-----------|-------|
| Role | Takes trained adapters → GGUF → Ollama models |
| Status | Modelfiles ready, export script written |
| Priority | BLOCKED on Track 1/2 completing |

### Future Tracks (see REQUIREMENTS.md > COULD)

| Model | Reason |
|-------|--------|
| Ministral 3 8B | Apache 2.0, edge-optimized, multilingual |
| Qwen3 4B Instruct | Fast to train on 32GB, 9M downloads |
| Qwen2.5 7B Instruct | Community standard for LoRA tutorials |
| Llama 3.1 8B | Broadest community compatibility |

## Workflow Rules

1. **Never execute the work yourself.** Route to the right track repo via `delegate_task` or `kanban_create`.
2. **Data flows left to right:** `raw → clean → train → eval → export → ollama`
3. **Each track is independent.** No cross-track dependencies until the ollama-pack consolidation phase.
4. **Commit after every operation.** Each track repo maintains its own git history.
5. **Verify before reporting done.** Run the verification script, check the output file, read it back. Subagent handoffs that claim "done" are unverified — verify tool outputs before reporting to the user.

## Key Decisions

| # | Decision | Rationale |
|---|----------|-----------|
| D1 | MLX + LoRA over full fine-tune | Only viable path on 32GB RAM |
| D2 | Hermes-3-Dataset + function-calling-v1 over synthetic data | Proven Hermes recipe, real conversations |
| D3 | Portable SSD for models/datasets | Only ~13GB free on main disk |
| D4 | Separate gemma4/lfm2/ollama-pack repos | Isolates churn, clean git history per model |
| D5 | Gemma 4 first, LFM2 second | Gemma is Apache 2.0 (safe to publish), smaller (faster download) |

## Cross-Reference

| Document | Purpose |
|----------|---------|
| `REQUIREMENTS.md` | Complete MoSCoW requirements specification |
| `DESIGN.md` | Architecture with Mermaid diagrams |
| `CONTRACTS.md` | Interface contracts between pipeline stages |
