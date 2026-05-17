# Requirements — Hermes Training Hub

> **Method:** MoSCoW (Must, Should, Could, Won't)
> **Scope:** Multi-model Hermes-style fine-tuning on MacBook Pro M1 Max (32GB RAM)
> **Status:** Active

---

## M — Must Have

These are non-negotiable. The system is incomplete without them.

| ID | Requirement | Track | Verification |
|----|-------------|-------|-------------|
| M1 | Reproducible MLX LoRA training pipeline | gemma4, lfm2 | `train.py --dry-run` exits 0 |
| M2 | Download real Hermes datasets from Nous Research | gemma4, lfm2 | `download_hermes_dataset.py` produces non-empty `data/splits/` |
| M3 | Train on Hermes-3-Dataset + hermes-function-calling-v1 | gemma4, lfm2 | Training completes without error |
| M4 | Save LoRA adapter weights to `experiments/{model}/lora_adapter/` | gemma4, lfm2 | `adapters.safetensors` and `adapter_config.json` exist |
| M5 | Export trained model to Ollama (GGUF format) | ollama-pack | `ollama list` shows the model |
| M6 | Model is selectable in Hermes model picker | ollama-pack | Hermes config resolves custom:ollama provider |
| M7 | All code lives in GitHub repos with clean git history | hub | `git push` succeeds, `git log` shows commits |
| M8 | Dataset pipeline deduplicates conversations by hash | gemma4, lfm2 | `build_dataset.py --dedup` removes exact duplicates |
| M9 | Training runs on Apple Silicon via MLX | gemma4, lfm2 | Script uses `mlx` backend, not CUDA |
| M10 | Models/datasets download to portable SSD | hub | `HF_HOME=/Volumes/PortableSSD/...` set on all downloads |
| M11 | Conductor system documents tracks, requirements, design, contracts | hub | Files exist: CONDUCTOR.md, REQUIREMENTS.md, DESIGN.md, CONTRACTS.md |

## S — Should Have

Important but not blocking. The system works without these but is significantly better with them.

| ID | Requirement | Track | Priority |
|----|-------------|-------|----------|
| S1 | Side-by-side eval comparison (base vs fine-tuned) | gemma4, lfm2 | HIGH |
| S2 | Bakeoff harness for pre-training model selection | gemma4 | HIGH |
| S3 | Push adapter + dataset to HuggingFace Hub | gemma4, lfm2 | MEDIUM |
| S4 | HTML report generation from eval results | gemma4, lfm2 | MEDIUM |
| S5 | Training on both Hermes datasets (instruction + function-calling) | gemma4, lfm2 | MEDIUM |
| S6 | At least 500 training conversations per model | gemma4, lfm2 | MEDIUM |
| S7 | llama.cpp built and ready for GGUF conversion | ollama-pack | HIGH (done) |
| S8 | Training runs at least 20 iterations as smoke test | gemma4, lfm2 | HIGH (in progress) |
| S9 | Gemma 4 E4B-it model cached on SSD | gemma4 | HIGH (in progress) |
| S10 | LFM2-8B-A1B model cached on SSD | lfm2 | HIGH (in progress) |

## C — Could Have

Desirable but not essential. Only pursue after all M and S requirements are met.

| ID | Requirement | Track | Value |
|----|-------------|-------|-------|
| C1 | Train more models (Ministral 3 8B, Qwen3 4B, Qwen2.5 7B, Llama 3.1 8B) | future | HIGH |
| C2 | Automated eval leaderboard across all trained models | hub | MEDIUM |
| C3 | Multi-run training with different hyperparameters | gemma4, lfm2 | MEDIUM |
| C4 | Preference tuning (DPO/ORPO) on top of LoRA SFT | gemma4, lfm2 | HIGH |
| C5 | Quantization-aware training (Q-LoRA) | gemma4, lfm2 | MEDIUM |
| C6 | CI pipeline for training on GitHub Actions | hub | LOW |
| C7 | Docker image with pre-built environment | hub | LOW |
| C8 | Web dashboard for training progress | hub | LOW |
| C9 | Periodic re-training on updated Hermes datasets | gemma4, lfm2 | MEDIUM |
| C10 | Export to multiple quantization levels (Q4_K_M, Q5_K_M, Q8_0) | ollama-pack | MEDIUM |

## W — Won't Have (this iteration)

Explicitly out of scope. Keeps the project focused.

| ID | Requirement | Reason |
|----|-------------|--------|
| W1 | Full model pre-training from scratch | Requires 100+ GPUs. Not feasible on Mac. |
| W2 | CUDA/ROCm-based training | Apple Silicon only. MLX is the right backend. |
| W3 | Distributed/multi-node training | Single MacBook Pro. No network of machines. |
| W4 | Custom dataset collection/generation | Rely on existing Hermes datasets. |
| W5 | Web UI for the training pipeline | CLI-first. Terminal tools are sufficient. |
| W6 | Fine-tuning models larger than 10B params | M1 Max 32GB cannot load 16B+ models for training. |
| W7 | Real-time training metrics dashboard | Logs + checkpoint files are sufficient. |
| W8 | A/B testing framework for model variants | Manual comparison via compare.py is enough. |

## Requirements Traceability Matrix

```
┌──────────────────────┬──────────┬──────────┬──────────────┐
│ Requirement          │ gemma4   │ lfm2     │ ollama-pack  │
├──────────────────────┼──────────┼──────────┼──────────────┤
│ M1 MLX LoRA pipeline │ ✅ done  │ ✅ done  │              │
│ M2 Download dataset  │ 🔄 active│ ✅ done  │              │
│ M3 Train on Hermes   │ 🔄 queue │ 📋 planned│              │
│ M4 Save adapter      │ 🔄 queue │ 📋 planned│              │
│ M5 Export to Ollama  │          │          │ ✅ script    │
│ M6 Hermes picker     │          │          │ 📋 planned   │
│ M7 GitHub repos      │ ✅ done  │ ✅ done  │ ✅ done      │
│ M8 Dataset dedup     │ ✅ done  │ ✅ done  │              │
│ M9 Apple Silicon MLX │ ✅ done  │ ✅ done  │              │
│ M10 SSD caching      │ 🔄 active│ 🔄 active│              │
│ M11 Conductor system │ 🔄 active│ 📋 planned│ 📋 planned  │
└──────────────────────┴──────────┴──────────┴──────────────┘

Legend: ✅ complete | 🔄 in progress | 📋 planned
```
