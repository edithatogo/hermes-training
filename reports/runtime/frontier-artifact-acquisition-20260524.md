# Frontier Artifact Acquisition

Date: 2026-05-24

## SSD Policy

All model acquisition paths are SSD-backed:

- Hugging Face cache: `/Volumes/PortableSSD/huggingface/hub`
- Frontier GGUF root: `/Volumes/PortableSSD/hermes-models/frontier-gguf`
- Frontier MLX root: `/Volumes/PortableSSD/models`
- Temporary files: `/Volumes/PortableSSD/tmp`

SSD free space before acquisition was approximately `390GiB`.

## Current Priority

The first runtime artifact to complete should be Hermes 4 14B Q4_K_M GGUF:

```bash
hf download SandLogicTechnologies/Hermes-4-14B-GGUF \
  Hermes-4-14B_Q4_k_m.gguf README.md \
  --local-dir /Volumes/PortableSSD/hermes-models/frontier-gguf/hermes-4-14b-q4
```

Final status:

- Complete artifact: `/Volumes/PortableSSD/hermes-models/frontier-gguf/hermes-4-14b-q4/Hermes-4-14B_Q4_k_m.gguf`
- Size: `9001753248` bytes
- Runtime proof: `reports/runtime/hermes4-14b-q4-llamacpp-smoke-20260524.md`
- Held-out benchmark: `reports/benchmark/endpoint-tool-call/hermes4-14b-q4-llamacpp-heldout-20260524.md`
- Endpoint pilots: `reports/benchmark/endpoint-pilots/hermes4-14b-q4-llamacpp-pilots-20260524.md`

The Hugging Face CLI/Xet path stalled, then the standard HTTP path progressed slowly. A resumable ranged downloader was added at `scripts/download_hf_file_ranges.py` and is now the preferred large-GGUF acquisition method for this artifact:

```bash
source scripts/env.sh
./.venv/bin/python scripts/download_hf_file_ranges.py \
  --repo-id SandLogicTechnologies/Hermes-4-14B-GGUF \
  --filename Hermes-4-14B_Q4_k_m.gguf \
  --output /Volumes/PortableSSD/hermes-models/frontier-gguf/hermes-4-14b-q4/Hermes-4-14B_Q4_k_m.gguf \
  --chunk-mib 64 \
  --workers 4 \
  --attempts 4
```

Chunk parts were stored in:

`/Volumes/PortableSSD/hermes-models/frontier-gguf/hermes-4-14b-q4/Hermes-4-14B_Q4_k_m.gguf.parts`

After the final GGUF was assembled and validated, the redundant chunk directory was removed to recover SSD space.

## Completed Qwen3.6 Acquisition

Qwen3.6 35B-A3B Q4_K_M acquisition completed on the SSD:

- Artifact: `/Volumes/PortableSSD/hermes-models/frontier-gguf/qwen3.6-35b-a3b-q4/Qwen3.6-35B-A3B-Q4_K_M.gguf`
- Size: `21166757888` bytes
- Runtime proof: `reports/runtime/qwen36-35b-a3b-q4-llamacpp-proof-20260525.md`
- Held-out strict tool-call pass: `0.000`
- Decision: runtime baseline only, not promotion-ready.

The post-download watcher ran the proof automatically after exact-size assembly.
The redundant chunk directory was removed after the proof to recover SSD space.

## Paused / Resumable

The following acquisition attempts were stopped because concurrent large downloads were moving too slowly. They are resumable and should be restarted one by one after the completed Qwen3.6 proof:

```bash
hf download DuoNeural/Gemma-4-26B-A4B-it-GGUF \
  Gemma-4-26B-A4B-it.Q3_K_M.gguf README.md \
  --local-dir /Volumes/PortableSSD/hermes-models/frontier-gguf/gemma-4-26b-a4b-q3
```

```python
from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="baa-ai/Qwen3.6-35B-A3B-RAM-19GB-MLX",
    local_dir="/Volumes/PortableSSD/models/baa-ai/Qwen3.6-35B-A3B-RAM-19GB-MLX",
)
```

## Next Runtime Proof

Hermes 4, Qwen3.6 Q4_K_M, and LFM2 24B-A2B Q4_K_M are complete as runtime
proofs. LFM2 proof details:

- Artifact: `/Volumes/PortableSSD/hermes-models/frontier-gguf/lfm2-24b-a2b-q4/LFM2-24B-A2B-Q4_K_M.gguf`
- Size: `14415473952` bytes
- Runtime proof: `reports/runtime/lfm2-24b-a2b-q4-llamacpp-proof-20260525.md`
- Held-out strict tool-call pass: `0.375`
- Decision: runtime baseline only, not promotion-ready.

Next candidates:

1. Resume `DuoNeural/Gemma-4-26B-A4B-it-GGUF` Q3_K_M.
2. Consider `baa-ai/Qwen3.6-35B-A3B-RAM-19GB-MLX` only if the GGUF path is blocked or the MLX runtime is specifically needed.

## Boundary

No partial artifact is runtime evidence. Do not run smoke tests until the target GGUF or MLX snapshot is complete.
