# Runtime Proof Action Queue

Run ID: `runtime-proof-action-queue-20260613`
Created: `2026-06-12T17:17:00.955872+00:00`

Purpose: convert the broad Hermes candidate radar into an executable queue. This file does not promote models; it identifies the next proof needed before spending local SSD space, Colab quota, or Azure hours.

## Immediate Local Queue

| Priority | Candidate | Lane | Params | Environment | Coverage | Next proof |
|---:|---|---|---|---|---|---|
| 1 | `google/gemma-4-E2B` | `mac-runtime-proof` | E2B | `hf-transformers` | `blocked` | blocked by current local runtime support |
| 2 | `google/gemma-4-E2B-it` | `mac-runtime-proof` | E2B | `hf-transformers` | `blocked` | blocked by current local runtime support |
| 3 | `google/gemma-4-E2B-it-qat-mobile-transformers` | `mac-runtime-proof` | 2B | `hf-transformers` | `blocked` | blocked by current local runtime support |
| 4 | `mlx-community/gemma-4-e2b-it-4bit` | `mac-runtime-proof` | E2B | `mac-mlx` | `blocked` | blocked by current local runtime support |
| 5 | `openbmb/MiniCPM-V-4.6-BNB` | `mac-runtime-proof` | 1B | `hf-transformers` | `blocked` | blocked by current local runtime support |
| 6 | `CohereLabs/North-Mini-Code-1.0` | `mac-runtime-proof` | 30B total / 3B active | `mac-lmstudio` | `blocked` | blocked by current local runtime support |
| 7 | `Qwen/Qwen3-Coder-Next` | `mac-runtime-proof` | 80B total / 3B active | `hf-transformers` | `blocked` | blocked until runtime artifact/load proof exists |
| 8 | `Qwen/Qwen3-Coder-Next-GGUF` | `mac-runtime-proof` | 80B total / 3B active | `mac-lmstudio` | `blocked` | blocked until runtime artifact/load proof exists |
| 9 | `baa-ai/Qwen3.6-35B-A3B-RAM-19GB-MLX` | `mac-runtime-proof` | 35B total / 3B active | `mac-mlx` | `blocked` | blocked until runtime artifact/load proof exists |
| 10 | `byteshape/Qwen3.6-35B-A3B-MTP-GGUF` | `mac-runtime-proof` | 35B total / 3B active | `mac-lmstudio` | `blocked` | blocked until runtime artifact/load proof exists |
| 11 | `deepsweet/Qwen3.6-35B-A3B-MLX-oQ4` | `mac-runtime-proof` | 35B total / 3B active | `mac-mlx` | `blocked` | blocked until runtime artifact/load proof exists |
| 12 | `google/gemma-4-E4B-it-qat-mobile-transformers` | `mac-runtime-proof` | 3B | `hf-transformers` | `blocked` | blocked until runtime artifact/load proof exists |
| 13 | `localweights/Qwen3.6-35B-A3B-MTP-IQ4_XS-GGUF` | `mac-runtime-proof` | 35B total / 3B active | `mac-lmstudio` | `blocked` | blocked until runtime artifact/load proof exists |
| 14 | `microsoft/Phi-4-mini-instruct` | `mac-runtime-proof` | 4B | `hf-transformers` | `blocked` | blocked until runtime artifact/load proof exists |
| 15 | `mlx-community/NVIDIA-Nemotron-3-Nano-4B-OptiQ-4bit` | `mac-runtime-proof` | 4B | `mac-mlx` | `blocked` | blocked until runtime artifact/load proof exists |
| 16 | `mudler/Qwen3.6-35B-A3B-APEX-MTP-GGUF` | `mac-runtime-proof` | 35B total / 3B active | `mac-lmstudio` | `blocked` | blocked until runtime artifact/load proof exists |
| 17 | `unsloth/NVIDIA-Nemotron-3-Nano-4B-GGUF` | `mac-runtime-proof` | 4B | `mac-lmstudio` | `blocked` | blocked until runtime artifact/load proof exists |
| 18 | `unsloth/North-Mini-Code-1.0-GGUF` | `mac-runtime-proof` | 30B total / 3B active | `mac-lmstudio` | `blocked` | blocked by current local runtime support |
| 19 | `unsloth/Qwen3.6-35B-A3B-MTP-GGUF` | `mac-runtime-proof` | 35B total / 3B active | `mac-lmstudio` | `blocked` | blocked until runtime artifact/load proof exists |
| 20 | `unsloth/gemma-4-26B-A4B-it-GGUF` | `mac-runtime-proof` | 26B total / 4B active | `mac-lmstudio` | `blocked` | blocked until runtime artifact/load proof exists |
| 21 | `DJLougen/Harmonic-9B` | `mac-runtime-proof` | 9B | `hf-transformers` | `blocked` | blocked until runtime artifact/load proof exists |
| 22 | `DJLougen/Harmonic-Hermes-9B-GGUF` | `mac-runtime-proof` | 9B | `mac-lmstudio` | `blocked` | blocked until runtime artifact/load proof exists |
| 23 | `LiquidAI/LFM2-8B-A1B` | `mac-runtime-proof` | 8B-ish / low active parameter count | `mac-ollama` | `blocked` | blocked until runtime artifact/load proof exists |
| 24 | `Qwen/Qwen3.5-9B` | `mac-runtime-proof` | 9B | `hf-transformers` | `blocked` | blocked until runtime artifact/load proof exists |
| 25 | `mradermacher/Harmonic-Hermes-9B-i1-GGUF` | `mac-runtime-proof` | 9B | `mac-lmstudio` | `blocked` | blocked until runtime artifact/load proof exists |

## Lane Counts

| Lane | Count |
|---|---:|
| `cloud-teacher-proof` | 12 |
| `mac-runtime-proof` | 49 |
| `prompt-profile-repair` | 16 |
| `specialist-runtime-proof` | 10 |
| `support-model-proof` | 67 |
| `watchlist` | 5 |

## Command Templates

### google/gemma-4-E2B

- Lane: `mac-runtime-proof`
- Coverage: `blocked`
- Blocker: blocked by current local runtime support

```bash
source scripts/env.sh
./.venv/bin/python scripts/build_all_candidate_benchmark_coverage.py
```

### google/gemma-4-E2B-it

- Lane: `mac-runtime-proof`
- Coverage: `blocked`
- Blocker: blocked by current local runtime support

```bash
source scripts/env.sh
./.venv/bin/python scripts/build_all_candidate_benchmark_coverage.py
```

### google/gemma-4-E2B-it-qat-mobile-transformers

- Lane: `mac-runtime-proof`
- Coverage: `blocked`
- Blocker: blocked by current local runtime support

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
- Blocker: blocked by current local runtime support

```bash
source scripts/env.sh
./.venv/bin/python scripts/build_all_candidate_benchmark_coverage.py
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

### Qwen/Qwen3-Coder-Next

- Lane: `mac-runtime-proof`
- Coverage: `blocked`
- Blocker: blocked until runtime artifact/load proof exists

```bash
source scripts/env.sh
./.venv/bin/python scripts/build_all_candidate_benchmark_coverage.py
```

### Qwen/Qwen3-Coder-Next-GGUF

- Lane: `mac-runtime-proof`
- Coverage: `blocked`
- Blocker: blocked until runtime artifact/load proof exists

```bash
source scripts/env.sh
# Acquire the smallest compatible GGUF to /Volumes/PortableSSD first, then run a bounded endpoint pilot.
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \
  --model qwen-qwen3-coder-next-gguf \
  --base-url http://127.0.0.1:<port>/v1 \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --run-id qwen-qwen3-coder-next-gguf-bfcl-pilot-$(date +%Y%m%d-%H%M%S)
```

### baa-ai/Qwen3.6-35B-A3B-RAM-19GB-MLX

- Lane: `mac-runtime-proof`
- Coverage: `blocked`
- Blocker: blocked until runtime artifact/load proof exists

```bash
source scripts/env.sh
# Acquire the MLX model to the SSD Hugging Face cache first.
./.venv/bin/python scripts/run_local_pilot_benchmark.py \
  --model baa-ai/Qwen3.6-35B-A3B-RAM-19GB-MLX \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --run-id baa-ai-qwen3-6-35b-a3b-ram-19gb-mlx-local-bfcl-pilot-$(date +%Y%m%d-%H%M%S)
```

### byteshape/Qwen3.6-35B-A3B-MTP-GGUF

- Lane: `mac-runtime-proof`
- Coverage: `blocked`
- Blocker: blocked until runtime artifact/load proof exists

```bash
source scripts/env.sh
# Acquire the smallest compatible GGUF to /Volumes/PortableSSD first, then run a bounded endpoint pilot.
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \
  --model byteshape-qwen3-6-35b-a3b-mtp-gguf \
  --base-url http://127.0.0.1:<port>/v1 \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --run-id byteshape-qwen3-6-35b-a3b-mtp-gguf-bfcl-pilot-$(date +%Y%m%d-%H%M%S)
```

### deepsweet/Qwen3.6-35B-A3B-MLX-oQ4

- Lane: `mac-runtime-proof`
- Coverage: `blocked`
- Blocker: blocked until runtime artifact/load proof exists

```bash
source scripts/env.sh
# Acquire the MLX model to the SSD Hugging Face cache first.
./.venv/bin/python scripts/run_local_pilot_benchmark.py \
  --model deepsweet/Qwen3.6-35B-A3B-MLX-oQ4 \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --run-id deepsweet-qwen3-6-35b-a3b-mlx-oq4-local-bfcl-pilot-$(date +%Y%m%d-%H%M%S)
```

### google/gemma-4-E4B-it-qat-mobile-transformers

- Lane: `mac-runtime-proof`
- Coverage: `blocked`
- Blocker: blocked until runtime artifact/load proof exists

```bash
source scripts/env.sh
./.venv/bin/python scripts/build_all_candidate_benchmark_coverage.py
```

## Policy

- Run local Mac proofs before cloud proofs when the artifact is small enough and a supported runtime exists.
- Use cloud only for teacher/frontier candidates or when local runtime proof is structurally unavailable.
- Route embedders, rerankers, ASR/TTS, and VLM helpers through role-specific support-model proofs rather than Hermes BFCL chat pilots.
- Do not promote from smoke evidence. Promotion still requires strict tool-call, local pilot, selected official benchmark, latency, and rollback evidence.
- Keep model downloads, caches, evals, and exports on `/Volumes/PortableSSD` through `scripts/env.sh`.
