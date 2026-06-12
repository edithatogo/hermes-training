# Support Lane Proof Queue - 2026-06-12

This report converts the support-lane scan into an execution queue. It is a
proof-state artifact, not a promotion claim.

## Smallest Useful Proofs

| Candidate | Status | Smallest useful proof | Evidence / blocker |
|---|---|---|---|
| `openbmb/MiniCPM5-1B-MLX` | runtime/load proven | Existing MLX loglikelihood smoke plus tiny-helper Hermes-local benchmark | `reports/benchmark/mlx-loglikelihood/minicpm5-1b-mlx-loglikelihood-smoke-20260612.md`, `reports/benchmark/local-pilots/tiny-helper-standard-benchmark-execution-20260612.md` |
| `deepseek-ai/DeepSeek-V4-Pro` | cloud-teacher only | Hosted API or specialist CUDA comparison fixture | No local-fit path; keep out of 32GB Mac lane |
| `nvidia/LocateAnything-3B` | proof pending | Colab visual-helper smoke on sanitized fixtures | Runtime proof still needed |
| `bosonai/higgs-audio-v3-tts-4b` | proof pending | Colab audio fixture smoke on sanitized data | Runtime proof still needed |
| `Qwen/Qwen3-ASR-1.7B` | proof pending | Colab or specialist ASR smoke on sanitized audio | Runtime proof still needed |
| `Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign` | proof pending | Colab or MLX audio smoke on sanitized audio | Runtime proof still needed |
| `mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-bf16` | proof pending | MLX audio smoke on sanitized audio | Runtime proof still needed |
| `Qwen/Qwen3-Omni-30B-A3B-Instruct` | proof pending | Colab multimodal fixture smoke | Too large for local-first proof |
| `microsoft/Phi-4-multimodal-instruct` | proof pending | Colab multimodal fixture smoke | Runtime proof still needed |
| `jinaai/jina-embeddings-v5-omni-small` | proof pending | Colab or MLX multimodal retrieval smoke | Retrieval-first support lane; proof still needed |
| `nvidia/NVIDIA-Nemotron-3-Nano-4B-GGUF` | proof pending | llama.cpp or LM Studio smoke after artifact acquisition | NGC / packaging gates still open |

## Backend Restrictions

- Azure remains blocked until login, subscription, region, quota, and cost gates pass.
- NGC remains blocked until API key, entitlement, and model/container checks pass.
- Colab is the default offload path for sanitized support proofs.
- Keep any restricted or private outputs out of public artifacts until an explicit
  publication review approves them.

## Interpretation

The support-lane set is now role-classified and backend-routed. The next real
work is a lane-by-lane proof pass, starting with the smallest available local
or Colab-friendly fixture and recording exact blockers for the rest.
