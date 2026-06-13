# Prompt/Profile Repair Execution Ledger

Run ID: `prompt-profile-repair-ledger-20260614`
Created: `2026-06-14T03:10:00+00:00`

Purpose: track which prompt/profile repair candidates are runnable locally, endpoint-gated, or blocked before execution.

## Ledger

| Priority | Candidate | Environment | Status | Experiments | Next action |
|---:|---|---|---|---:|---|
| 1 | `LGAI-EXAONE/EXAONE-4.0-1.2B` | `mac-mlx` | `pending-endpoint` | 1 | start the existing local endpoint for the SSD-backed artifact, then run one experiment |
| 2 | `google/gemma-4-E2B-it-qat-q4_0-gguf` | `mac-lmstudio` | `pending-endpoint` | 1 | start the existing local endpoint for the SSD-backed artifact, then run one experiment |
| 3 | `mkadrlik/hermes-Qwen3.5-0.8B-SFT-v7-fresh` | `mac-lmstudio` | `pending-endpoint` | 3 | start the existing local endpoint for the SSD-backed artifact, then run one experiment |
| 4 | `LiquidAI/LFM2.5-8B-A1B-GGUF` | `mac-lmstudio` | `pending-endpoint` | 1 | start the existing local endpoint for the SSD-backed artifact, then run one experiment |
| 5 | `openbmb/MiniCPM5-1B-GGUF` | `mac-lmstudio` | `pending-endpoint` | 2 | start the existing local endpoint for the SSD-backed artifact, then run one experiment |
| 6 | `openbmb/MiniCPM5-1B-MLX` | `mac-mlx` | `pending-local` | 3 | run one local MLX/Transformers experiment and capture the report path |
| 7 | `Qwen/Qwen3.5-0.8B` | `mac-mlx` | `completed-no-promotion` | 3 | try the qwen-no-think-prefill or empty-output-retry variant before any promotion claim |
| 8 | `Qwen/Qwen3.5-2B` | `mac-mlx` | `pending-local` | 3 | run one local MLX/Transformers experiment and capture the report path |
| 9 | `mlx-community/gemma-4-E4B-it-qat-4bit` | `mac-mlx` | `pending-local-with-analysis-variant` | 2 | run raw-output variants first; analysis-only normalizer variants cannot promote |
| 10 | `ibm-granite/granite-4.1-3b` | `mac-mlx` | `pending-local-with-analysis-variant` | 2 | run raw-output variants first; analysis-only normalizer variants cannot promote |
| 11 | `mkadrlik/Hermes-Qwen3.5-4B-SFT-v7` | `mac-lmstudio` | `pending-endpoint` | 2 | start the existing local endpoint for the SSD-backed artifact, then run one experiment |
| 12 | `Mungert/Nanbeige4.1-3B-GGUF` | `mac-lmstudio` | `pending-endpoint` | 2 | start the existing local endpoint for the SSD-backed artifact, then run one experiment |
| 13 | `Nanbeige/Nanbeige4.1-3B` | `hf-transformers` | `pending-local` | 1 | run one local MLX/Transformers experiment and capture the report path |
| 14 | `mlx-community/NVIDIA-Nemotron-3-Nano-4B-OptiQ-4bit` | `mac-mlx` | `pending-local` | 1 | run one local MLX/Transformers experiment and capture the report path |
| 15 | `nvidia/NVIDIA-Nemotron-3-Nano-4B-GGUF` | `mac-lmstudio` | `pending-endpoint` | 1 | start the existing local endpoint for the SSD-backed artifact, then run one experiment |
| 16 | `ManiacLabs/Qwen3.6-35B-A3B-2bit` | `mac-lmstudio` | `pending-endpoint` | 3 | start the existing local endpoint for the SSD-backed artifact, then run one experiment |
| 17 | `Qwen/Qwen3.6-35B-A3B` | `azure-cuda` | `blocked-non-local` | 0 | candidate environment is not locally runnable; wait for the relevant cloud/offload track |
| 18 | `mkadrlik/Hermes-Qwen3.5-9B-SFT-v7` | `mac-lmstudio` | `pending-endpoint` | 2 | start the existing local endpoint for the SSD-backed artifact, then run one experiment |

## Gates

- Run one experiment at a time and write result reports under the SSD-backed evaluation root.
- Leave `result_report` blank until a real benchmark report exists; completed rows must point to a tracked report.
- `pending-endpoint` means a local OpenAI-compatible endpoint must be started manually for the existing artifact.
- `blocked-non-local` is not runnable on this Mac lane; use the matching cloud/offload track.
- Analysis-only normalizer variants can diagnose formatting but cannot promote a candidate.
