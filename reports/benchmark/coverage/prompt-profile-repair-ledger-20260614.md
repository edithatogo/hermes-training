# Prompt/Profile Repair Execution Ledger

Run ID: `prompt-profile-repair-ledger-20260614`
Created: `2026-06-14T03:10:00+00:00`

Purpose: track which prompt/profile repair candidates are runnable locally, endpoint-gated, or blocked before execution.

## Ledger

| Priority | Candidate | Environment | Status | Experiments | Next action |
|---:|---|---|---|---:|---|
| 1 | `LGAI-EXAONE/EXAONE-4.0-1.2B` | `mac-mlx` | `completed-no-promotion` | 1 | stop single-variant EXAONE prompt repair; use constrained output or a different endpoint-gated candidate next |
| 2 | `google/gemma-4-E2B-it-qat-q4_0-gguf` | `mac-lmstudio` | `completed-no-promotion` | 1 | stop single-variant Gemma E2B GGUF prompt repair; use Gemma-native formatting or another endpoint-gated candidate next |
| 3 | `mkadrlik/hermes-Qwen3.5-0.8B-SFT-v7-fresh` | `mac-lmstudio` | `completed-no-promotion` | 3 | stop prompt-only Hermes-Qwen3.5 0.8B fresh variants; use constrained decoding or a runtime-wrapper proof if revisited |
| 4 | `LiquidAI/LFM2.5-8B-A1B-GGUF` | `mac-lmstudio` | `completed-no-promotion` | 1 | stop single-variant LFM2.5 8B A1B prompt repair; move to the next endpoint-gated candidate |
| 5 | `openbmb/MiniCPM5-1B-GGUF` | `mac-lmstudio` | `completed-no-promotion` | 2 | stop prompt-only MiniCPM5 1B GGUF endpoint repairs; use constrained decoding or a runtime-wrapper proof if revisited |
| 6 | `openbmb/MiniCPM5-1B-MLX` | `mac-mlx` | `completed-no-promotion` | 3 | stop prompt-only MiniCPM5 1B MLX repairs; use a grammar/envelope-constrained path or move to the next candidate |
| 7 | `Qwen/Qwen3.5-0.8B` | `mac-mlx` | `completed-no-promotion` | 3 | stop prompt-only Qwen3.5 0.8B repairs; use a grammar/envelope-constrained path or move to the next candidate |
| 8 | `Qwen/Qwen3.5-2B` | `mac-mlx` | `completed-no-promotion` | 3 | stop prompt-only Qwen3.5 2B repairs; use a grammar/envelope-constrained path or move to the next candidate |
| 9 | `mlx-community/gemma-4-E4B-it-qat-4bit` | `mac-mlx` | `completed-no-promotion` | 2 | stop prompt/normalizer-only Gemma E4B repairs; use a grammar/envelope-constrained path or move to the next candidate |
| 10 | `ibm-granite/granite-4.1-3b` | `mac-mlx` | `completed-no-promotion` | 2 | stop prompt/normalizer-only Granite repairs; use a grammar/envelope-constrained path or move to the next candidate |
| 11 | `mkadrlik/Hermes-Qwen3.5-4B-SFT-v7` | `mac-lmstudio` | `completed-no-promotion` | 2 | stop prompt-only Hermes-Qwen3.5 4B variants; use constrained decoding or a runtime-wrapper proof if revisited |
| 12 | `Mungert/Nanbeige4.1-3B-GGUF` | `mac-lmstudio` | `completed-no-promotion` | 2 | stop prompt-only Mungert Nanbeige variants; use constrained decoding or a runtime-wrapper proof if revisited |
| 13 | `Nanbeige/Nanbeige4.1-3B` | `hf-transformers` | `completed-no-promotion` | 1 | stop single-variant Nanbeige prompt repair; use no-think or grammar/envelope-constrained output if revisited |
| 14 | `mlx-community/NVIDIA-Nemotron-3-Nano-4B-OptiQ-4bit` | `mac-mlx` | `completed-no-promotion` | 1 | stop single-variant Nemotron prompt repair; use grammar/envelope-constrained output or endpoint-gated candidates next |
| 15 | `nvidia/NVIDIA-Nemotron-3-Nano-4B-GGUF` | `mac-lmstudio` | `completed-no-promotion` | 1 | stop single-variant Nemotron GGUF prompt repair; use constrained decoding or DSML-to-Hermes runtime normalization only with held-out proof |
| 16 | `ManiacLabs/Qwen3.6-35B-A3B-2bit` | `mac-lmstudio` | `completed-no-promotion` | 3 | stop prompt-only ManiacLabs variants; use constrained decoding or a runtime-wrapper proof if revisited |
| 17 | `Qwen/Qwen3.6-35B-A3B` | `azure-cuda` | `blocked-non-local` | 0 | candidate environment is not locally runnable; wait for the relevant cloud/offload track |
| 18 | `mkadrlik/Hermes-Qwen3.5-9B-SFT-v7` | `mac-lmstudio` | `completed-no-promotion` | 2 | stop prompt-only Hermes-Qwen3.5 9B variants; use constrained decoding or a runtime-wrapper proof if revisited |

## Gates

- Run one experiment at a time and write result reports under the SSD-backed evaluation root.
- Leave `result_report` blank until a real benchmark report exists; completed rows must point to a tracked report.
- `pending-endpoint` means a local OpenAI-compatible endpoint must be started manually for the existing artifact.
- `blocked-non-local` is not runnable on this Mac lane; use the matching cloud/offload track.
- Analysis-only normalizer variants can diagnose formatting but cannot promote a candidate.
