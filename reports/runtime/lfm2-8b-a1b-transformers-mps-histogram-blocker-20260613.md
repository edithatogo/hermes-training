# LFM2 8B-A1B Transformers MPS Runtime Blocker - 2026-06-13

## Summary

`LiquidAI/LFM2-8B-A1B` was acquired to the SSD-backed Hugging Face cache and
loaded with the generic Transformers pilot runner on MPS with `float16`.

The model loaded successfully, but generation failed on the first strict BFCL
pilot case before any benchmark row could be scored.

Status: `runtime-load-complete; generation-blocked`.

## Artifact

- Repo: `LiquidAI/LFM2-8B-A1B`
- Local cache: `/Volumes/PortableSSD/huggingface/hub/models--LiquidAI--LFM2-8B-A1B`
- Cache size after acquisition: `16G`
- Runtime: Hugging Face Transformers
- Device: MPS
- Dtype: `float16`
- Load time reported by runner: `1618.9s`

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_transformers_pilot_benchmark.py \
  --model LiquidAI/LFM2-8B-A1B \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --run-id lfm2-8b-a1b-transformers-mps-fp16-strict-bfcl-pilot-20260613 \
  --device mps \
  --dtype float16 \
  --max-tokens 256 \
  --require-no-extra-tool-text
```

## Failure

The run failed during `model.generate(...)` on the first BFCL case. The stack
entered `transformers.models.lfm2_moe.modeling_lfm2_moe`, then the MoE
integration called `torch.histc(...)` for expert routing.

Observed terminal error:

```text
NotImplementedError: "histogram_mps" not implemented for 'Int'
```

## Decision

- Do not treat this as a model quality failure; no generation was scored.
- Do not promote this lane for Hermes on the current Mac MPS stack.
- Keep the SSD cache because the expensive acquisition is complete.
- Next viable proof paths:
  - CPU-only micro-smoke with very small token cap, if latency is acceptable.
  - Patched PyTorch/MPS or Transformers path that avoids integer `histc` on MPS.
  - MLX, LEAP, ONNX, Ollama, or GGUF conversion path for the same architecture.
  - Cloud GPU/TPU proof if the local path remains blocked.
