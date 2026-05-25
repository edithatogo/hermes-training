# Specialist Runtime Preflight

Date: 2026-05-25T18:36:26.646687+00:00
SSD root: `/Volumes/PortableSSD`
Policy: read-only; no installs, downloads, compute creation, or model conversion

## Summary

| Lane | Model | Runtime | Status | Blockers |
|---|---|---|---|---|
| `ktransformers-moe` | `Qwen/Qwen3.6-35B-A3B` | KTransformers | `blocked` | runtime command/module not found; no matching SSD artifact path found |
| `liquid-leap-lfm` | `LiquidAI/LFM2-8B-A1B` | LEAP/LFM specialist runtime | `blocked` | runtime command/module not found |
| `recurrent-ssm-bitnet` | `RWKV/RWKV7-Goose-World3-2.9B-HF` | RWKV native runtime | `blocked` | runtime command/module not found; no matching SSD artifact path found |
| `recurrent-ssm-bitnet` | `microsoft/bitnet-b1.58-2B-4T` | BitNet native runtime | `blocked` | runtime command/module not found |
| `recurrent-ssm-bitnet` | `state-spaces/mamba-family-watchlist` | Mamba/SSM native runtime | `blocked` | runtime command/module not found; no matching SSD artifact path found |

## Details

### KTransformers / `Qwen/Qwen3.6-35B-A3B`

- Minimum pass: KTransformers import/CLI plus prepared Qwen3.6 weights.
- Notes: Do not treat the existing GGUF proof as KTransformers evidence; this lane needs native prepared weights and an invocation contract.
- Status: `blocked`

| Check | Name/path | Present |
|---|---|---:|
| command | `ktransformers` | `false` |
| python module | `ktransformers` | `false` |
| artifact | `/Volumes/PortableSSD/huggingface/hub/models--Qwen--Qwen3.6-35B-A3B` | `false` |
| artifact | `/Volumes/PortableSSD/models/Qwen/Qwen3.6-35B-A3B` | `false` |

### LEAP/LFM specialist runtime / `LiquidAI/LFM2-8B-A1B`

- Minimum pass: LEAP CLI/import plus a cached LFM family checkpoint or package.
- Notes: MLX and GGUF LFM proofs are separate; LEAP remains blocked until its own runtime/package path exists.
- Status: `blocked`

| Check | Name/path | Present |
|---|---|---:|
| command | `leap` | `false` |
| command | `leap-finetune` | `false` |
| python module | `leap` | `false` |
| python module | `leap_finetune` | `false` |
| artifact | `/Volumes/PortableSSD/huggingface/hub/models--LiquidAI--LFM2-8B-A1B` | `false` |
| artifact | `/Volumes/PortableSSD/huggingface/hub/models--LiquidAI--LFM2.5-1.2B-Instruct` | `true` |

### RWKV native runtime / `RWKV/RWKV7-Goose-World3-2.9B-HF`

- Minimum pass: Native RWKV runtime plus exact cached checkpoint.
- Notes: Transformers compatibility alone is not enough for the recurrent runtime lane.
- Status: `blocked`

| Check | Name/path | Present |
|---|---|---:|
| command | `rwkv` | `false` |
| python module | `rwkv` | `false` |
| python module | `rwkvstic` | `false` |
| artifact | `/Volumes/PortableSSD/huggingface/hub/models--RWKV--RWKV7-Goose-World3-2.9B-HF` | `false` |
| artifact | `/Volumes/PortableSSD/models/RWKV` | `false` |

### BitNet native runtime / `microsoft/bitnet-b1.58-2B-4T`

- Minimum pass: BitNet runtime plus exact cached checkpoint or local runtime checkout.
- Notes: Ternary/BitNet claims require the native runtime path, not generic transformer loading.
- Status: `blocked`

| Check | Name/path | Present |
|---|---|---:|
| command | `bitnet` | `false` |
| command | `bitnet-cli` | `false` |
| python module | `bitnet` | `false` |
| artifact | `/Volumes/PortableSSD/huggingface/hub/models--microsoft--bitnet-b1.58-2B-4T` | `false` |
| artifact | `/Volumes/PortableSSD/GitHub/BitNet` | `true` |

### Mamba/SSM native runtime / `state-spaces/mamba-family-watchlist`

- Minimum pass: Mamba/SSM module plus exact checkpoint and invocation contract.
- Notes: Keep as architecture-family evidence until an exact public checkpoint and runtime are selected.
- Status: `blocked`

| Check | Name/path | Present |
|---|---|---:|
| command | `mamba_ssm` | `false` |
| python module | `mamba_ssm` | `false` |
| artifact | `/Volumes/PortableSSD/huggingface/hub/models--state-spaces` | `false` |
| artifact | `/Volumes/PortableSSD/models/mamba` | `false` |

## Decision

No specialist lane is promoted by this preflight. A lane can move to runtime smoke only after its native runtime and exact SSD artifact path are both present.
