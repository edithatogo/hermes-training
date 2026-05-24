# Frontier GGUF Acquisition

Date: 2026-05-24

## SSD Root

```text
/Volumes/PortableSSD/hermes-models/frontier-gguf/
```

## Target Artifacts

| Model | Repo | File | Size | Status |
|---|---|---|---:|---|
| Hermes 4 14B | `SandLogicTechnologies/Hermes-4-14B-GGUF` | `Hermes-4-14B_Q4_k_m.gguf` | 8.38 GiB | resumable partial on SSD |
| Qwen3.6 35B-A3B | `Infatoshi/Qwen3.6-35B-A3B-GGUF` | `Qwen3.6-35B-A3B-Q4_K_M.gguf` | 19.71 GiB | target resolved; partial HF download on SSD |
| Gemma 4 26B-A4B | `DuoNeural/Gemma-4-26B-A4B-it-GGUF` | `Gemma-4-26B-A4B-it.Q3_K_M.gguf` | 12.37 GiB | target resolved; partial HF download on SSD |

## Commands

Hermes 4 14B:

```bash
source scripts/env.sh
./.venv/bin/python scripts/download_hf_file_ranges.py \
  --repo-id SandLogicTechnologies/Hermes-4-14B-GGUF \
  --filename Hermes-4-14B_Q4_k_m.gguf \
  --output /Volumes/PortableSSD/hermes-models/frontier-gguf/hermes-4-14b-q4/Hermes-4-14B_Q4_k_m.gguf \
  --chunk-mib 64 \
  --workers 8
```

Qwen3.6 35B-A3B:

```bash
source scripts/env.sh
hf download Infatoshi/Qwen3.6-35B-A3B-GGUF \
  Qwen3.6-35B-A3B-Q4_K_M.gguf README.md \
  --local-dir /Volumes/PortableSSD/hermes-models/frontier-gguf/qwen3.6-35b-a3b-q4
```

Gemma 4 26B-A4B:

```bash
source scripts/env.sh
hf download DuoNeural/Gemma-4-26B-A4B-it-GGUF \
  Gemma-4-26B-A4B-it.Q3_K_M.gguf README.md \
  --local-dir /Volumes/PortableSSD/hermes-models/frontier-gguf/gemma-4-26b-a4b-q3
```

## Decision

The artifact blocker is no longer an unknown-model blocker: exact repos, filenames, sizes, SSD roots, and resumable commands are recorded. The remaining constraint is transfer time/bandwidth. No public model-quality claim should mention these artifacts until each file is complete and has a runtime smoke card.
