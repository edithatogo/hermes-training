# Runtime Proof Action Queue

Run ID: `runtime-proof-action-queue-20260613`
Created: `2026-06-12T14:59:10.290633+00:00`

Purpose: convert the broad Hermes candidate radar into an executable queue. This file does not promote models; it identifies the next proof needed before spending local SSD space, Colab quota, or Azure hours.

## Immediate Local Queue

| Priority | Candidate | Lane | Params | Environment | Coverage | Next proof |
|---:|---|---|---|---|---|---|
| 1 | `Qwen/Qwen3.5-0.8B` | `mac-runtime-proof` | 0.9B | `mac-mlx` | `blocked` | blocked by empty/no-content generation under the strict prompt |
| 2 | `Qwen/Qwen3.5-2B` | `mac-runtime-proof` | 2B | `mac-mlx` | `blocked` | blocked by empty/no-content generation under the strict prompt |
| 3 | `google/gemma-4-E2B` | `mac-runtime-proof` | E2B | `hf-transformers` | `blocked` | blocked until runtime artifact/load proof exists |
| 4 | `google/gemma-4-E2B-it` | `mac-runtime-proof` | E2B | `hf-transformers` | `blocked` | blocked until runtime artifact/load proof exists |
| 5 | `google/gemma-4-E2B-it-qat-mobile-transformers` | `mac-runtime-proof` | 2B | `hf-transformers` | `blocked` | blocked until runtime artifact/load proof exists |
| 6 | `mkadrlik/hermes-Qwen3.5-0.8B-SFT-v7-fresh` | `mac-runtime-proof` | 0.8B | `mac-lmstudio` | `blocked` | blocked until runtime artifact/load proof exists |
| 7 | `mkadrlik/hermes-Qwen3.5-2B-SFT-v7` | `mac-runtime-proof` | 2B | `mac-lmstudio` | `blocked` | blocked until runtime artifact/load proof exists |
| 8 | `mlx-community/gemma-4-e2b-it-4bit` | `mac-runtime-proof` | E2B | `mac-mlx` | `blocked` | blocked by current local runtime support |
| 9 | `openbmb/MiniCPM-V-4.6-BNB` | `mac-runtime-proof` | 1B | `hf-transformers` | `blocked` | blocked until runtime artifact/load proof exists |
| 10 | `openbmb/MiniCPM5-1B-GGUF` | `mac-runtime-proof` | 1B | `mac-lmstudio` | `blocked` | blocked until runtime artifact/load proof exists |
| 11 | `openbmb/MiniCPM5-1B-MLX` | `mac-runtime-proof` | 1B | `mac-mlx` | `blocked` | blocked by empty/no-content generation under the strict prompt |
| 12 | `CohereLabs/North-Mini-Code-1.0` | `mac-runtime-proof` | 30B total / 3B active | `mac-lmstudio` | `blocked` | blocked by current local runtime support |
| 13 | `ManiacLabs/Qwen3.6-35B-A3B-2bit-maniac-nonstreaming` | `mac-runtime-proof` | 35B total / 3B active | `mac-mlx` | `blocked` | blocked until runtime artifact/load proof exists |
| 14 | `Mungert/Nanbeige4.1-3B-GGUF` | `mac-runtime-proof` | 3B | `mac-lmstudio` | `blocked` | blocked until runtime artifact/load proof exists |
| 15 | `Nanbeige/Nanbeige4.1-3B` | `mac-runtime-proof` | 3B | `hf-transformers` | `blocked` | blocked until runtime artifact/load proof exists |
| 16 | `Qwen/Qwen3-Coder-Next` | `mac-runtime-proof` | 80B total / 3B active | `hf-transformers` | `blocked` | blocked until runtime artifact/load proof exists |
| 17 | `Qwen/Qwen3-Coder-Next-GGUF` | `mac-runtime-proof` | 80B total / 3B active | `mac-lmstudio` | `blocked` | blocked until runtime artifact/load proof exists |
| 18 | `baa-ai/Qwen3.6-35B-A3B-RAM-19GB-MLX` | `mac-runtime-proof` | 35B total / 3B active | `mac-mlx` | `blocked` | blocked until runtime artifact/load proof exists |
| 19 | `byteshape/Qwen3.6-35B-A3B-MTP-GGUF` | `mac-runtime-proof` | 35B total / 3B active | `mac-lmstudio` | `blocked` | blocked until runtime artifact/load proof exists |
| 20 | `deepsweet/Qwen3.6-35B-A3B-MLX-oQ4` | `mac-runtime-proof` | 35B total / 3B active | `mac-mlx` | `blocked` | blocked until runtime artifact/load proof exists |
| 21 | `google/gemma-4-E4B-it-qat-mobile-transformers` | `mac-runtime-proof` | 3B | `hf-transformers` | `blocked` | blocked until runtime artifact/load proof exists |
| 22 | `localweights/Qwen3.6-35B-A3B-MTP-IQ4_XS-GGUF` | `mac-runtime-proof` | 35B total / 3B active | `mac-lmstudio` | `blocked` | blocked until runtime artifact/load proof exists |
| 23 | `microsoft/Phi-4-mini-instruct` | `mac-runtime-proof` | 4B | `hf-transformers` | `blocked` | blocked until runtime artifact/load proof exists |
| 24 | `mkadrlik/Hermes-Qwen3.5-4B-SFT-v7` | `mac-runtime-proof` | 4B | `mac-lmstudio` | `blocked` | blocked until runtime artifact/load proof exists |
| 25 | `mlx-community/NVIDIA-Nemotron-3-Nano-4B-OptiQ-4bit` | `mac-runtime-proof` | 4B | `mac-mlx` | `blocked` | blocked until runtime artifact/load proof exists |

## Lane Counts

| Lane | Count |
|---|---:|
| `cloud-teacher-proof` | 12 |
| `mac-runtime-proof` | 59 |
| `prompt-profile-repair` | 5 |
| `specialist-runtime-proof` | 9 |
| `support-model-proof` | 65 |
| `watchlist` | 5 |

## Command Templates

### Qwen/Qwen3.5-0.8B

- Lane: `mac-runtime-proof`
- Coverage: `blocked`
- Blocker: blocked by empty/no-content generation under the strict prompt

```bash
source scripts/env.sh
# Acquire the smallest compatible GGUF to /Volumes/PortableSSD first, then run a bounded endpoint pilot.
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \
  --model qwen-qwen3-5-0-8b \
  --base-url http://127.0.0.1:<port>/v1 \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --run-id qwen-qwen3-5-0-8b-bfcl-pilot-$(date +%Y%m%d-%H%M%S)
```

### Qwen/Qwen3.5-2B

- Lane: `mac-runtime-proof`
- Coverage: `blocked`
- Blocker: blocked by empty/no-content generation under the strict prompt

```bash
source scripts/env.sh
# Acquire the smallest compatible GGUF to /Volumes/PortableSSD first, then run a bounded endpoint pilot.
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \
  --model qwen-qwen3-5-2b \
  --base-url http://127.0.0.1:<port>/v1 \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --run-id qwen-qwen3-5-2b-bfcl-pilot-$(date +%Y%m%d-%H%M%S)
```

### google/gemma-4-E2B

- Lane: `mac-runtime-proof`
- Coverage: `blocked`
- Blocker: blocked until runtime artifact/load proof exists

```bash
source scripts/env.sh
./.venv/bin/python scripts/build_all_candidate_benchmark_coverage.py
```

### google/gemma-4-E2B-it

- Lane: `mac-runtime-proof`
- Coverage: `blocked`
- Blocker: blocked until runtime artifact/load proof exists

```bash
source scripts/env.sh
./.venv/bin/python scripts/build_all_candidate_benchmark_coverage.py
```

### google/gemma-4-E2B-it-qat-mobile-transformers

- Lane: `mac-runtime-proof`
- Coverage: `blocked`
- Blocker: blocked until runtime artifact/load proof exists

```bash
source scripts/env.sh
./.venv/bin/python scripts/build_all_candidate_benchmark_coverage.py
```

### mkadrlik/hermes-Qwen3.5-0.8B-SFT-v7-fresh

- Lane: `mac-runtime-proof`
- Coverage: `blocked`
- Blocker: blocked until runtime artifact/load proof exists

```bash
source scripts/env.sh
./.venv/bin/python scripts/build_all_candidate_benchmark_coverage.py
```

### mkadrlik/hermes-Qwen3.5-2B-SFT-v7

- Lane: `mac-runtime-proof`
- Coverage: `blocked`
- Blocker: blocked until runtime artifact/load proof exists

```bash
source scripts/env.sh
./.venv/bin/python scripts/build_all_candidate_benchmark_coverage.py
```

### mlx-community/gemma-4-e2b-it-4bit

- Lane: `mac-runtime-proof`
- Coverage: `blocked`
- Blocker: blocked by current local runtime support

```bash
source scripts/env.sh
# Acquire the MLX model to the SSD Hugging Face cache first.
./.venv/bin/python scripts/run_local_pilot_benchmark.py \
  --model mlx-community/gemma-4-e2b-it-4bit \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --run-id mlx-community-gemma-4-e2b-it-4bit-local-bfcl-pilot-$(date +%Y%m%d-%H%M%S)
```

### openbmb/MiniCPM-V-4.6-BNB

- Lane: `mac-runtime-proof`
- Coverage: `blocked`
- Blocker: blocked until runtime artifact/load proof exists

```bash
source scripts/env.sh
./.venv/bin/python scripts/build_all_candidate_benchmark_coverage.py
```

### openbmb/MiniCPM5-1B-GGUF

- Lane: `mac-runtime-proof`
- Coverage: `blocked`
- Blocker: blocked until runtime artifact/load proof exists

```bash
source scripts/env.sh
# Acquire the smallest compatible GGUF to /Volumes/PortableSSD first, then run a bounded endpoint pilot.
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \
  --model openbmb-minicpm5-1b-gguf \
  --base-url http://127.0.0.1:<port>/v1 \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --run-id openbmb-minicpm5-1b-gguf-bfcl-pilot-$(date +%Y%m%d-%H%M%S)
```

### openbmb/MiniCPM5-1B-MLX

- Lane: `mac-runtime-proof`
- Coverage: `blocked`
- Blocker: blocked by empty/no-content generation under the strict prompt

```bash
source scripts/env.sh
# Acquire the MLX model to the SSD Hugging Face cache first.
./.venv/bin/python scripts/run_local_pilot_benchmark.py \
  --model openbmb/MiniCPM5-1B-MLX \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --run-id openbmb-minicpm5-1b-mlx-local-bfcl-pilot-$(date +%Y%m%d-%H%M%S)
```

### CohereLabs/North-Mini-Code-1.0

- Lane: `mac-runtime-proof`
- Coverage: `blocked`
- Blocker: blocked by current local runtime support

```bash
source scripts/env.sh
# Acquire the smallest compatible GGUF to /Volumes/PortableSSD first, then run a bounded endpoint pilot.
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \
  --model coherelabs-north-mini-code-1-0 \
  --base-url http://127.0.0.1:<port>/v1 \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --run-id coherelabs-north-mini-code-1-0-bfcl-pilot-$(date +%Y%m%d-%H%M%S)
```

## Policy

- Run local Mac proofs before cloud proofs when the artifact is small enough and a supported runtime exists.
- Use cloud only for teacher/frontier candidates or when local runtime proof is structurally unavailable.
- Route embedders, rerankers, ASR/TTS, and VLM helpers through role-specific support-model proofs rather than Hermes BFCL chat pilots.
- Do not promote from smoke evidence. Promotion still requires strict tool-call, local pilot, selected official benchmark, latency, and rollback evidence.
- Keep model downloads, caches, evals, and exports on `/Volumes/PortableSSD` through `scripts/env.sh`.
