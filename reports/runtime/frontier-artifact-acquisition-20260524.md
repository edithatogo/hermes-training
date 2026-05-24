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

Status at the last check:

- Active process: yes
- Partial file: `/Volumes/PortableSSD/hermes-models/frontier-gguf/hermes-4-14b-q4/.cache/huggingface/download/*.incomplete`
- Approximate downloaded size at last check: `150MiB`

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

Chunk parts are stored in:

`/Volumes/PortableSSD/hermes-models/frontier-gguf/hermes-4-14b-q4/Hermes-4-14B_Q4_k_m.gguf.parts`

## Paused / Resumable

The following acquisition attempts were stopped because concurrent large downloads were moving too slowly. They are resumable and should be restarted one by one after Hermes 4 completes:

```bash
hf download Infatoshi/Qwen3.6-35B-A3B-GGUF \
  Qwen3.6-35B-A3B-Q4_K_M.gguf README.md \
  --local-dir /Volumes/PortableSSD/hermes-models/frontier-gguf/qwen3.6-35b-a3b-q4
```

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

After the Hermes 4 GGUF file is complete:

1. Confirm file size and `llama-server` model load.
2. Serve through `http://127.0.0.1:8092/v1` with alias `hermes-4-14b-q4`.
3. Run `ollama-pack/scripts/runtime_smoke.sh`.
4. Run `scripts/run_endpoint_tool_call_benchmark.py` on `benchmarks/tool_call_local/heldout_suite.json` with `/no_think`.
5. Store raw outputs under `/Volumes/PortableSSD/hermes-evals`.

## Boundary

No partial artifact is runtime evidence. Do not run smoke tests until the target GGUF or MLX snapshot is complete.
