# Runtime Proof Action Queue

Run ID: `runtime-proof-action-queue-20260613`
Created: `2026-06-14T12:31:41.273003+00:00`

Purpose: convert the broad Hermes candidate radar into an executable queue. This file does not promote models; it identifies the next proof needed before spending local SSD space, Colab quota, or Azure hours.

## Immediate Local Queue

| Priority | Candidate | Lane | Params | Environment | Coverage | Next proof |
|---:|---|---|---|---|---|---|
| 1 | `google/gemma-4-E4B-it-qat-mobile-transformers` | `mac-runtime-proof` | 3B | `hf-transformers` | `blocked` | blocked until runtime artifact/load proof exists |
| 2 | `unsloth/NVIDIA-Nemotron-3-Nano-4B-GGUF` | `mac-runtime-proof` | 4B | `mac-lmstudio` | `blocked` | blocked until runtime artifact acquisition succeeds |
| 3 | `DJLougen/Harmonic-9B` | `mac-runtime-proof` | 9B | `hf-transformers` | `blocked` | blocked from local Mac benchmark by model size; route to quantized sibling or cloud |
| 4 | `DJLougen/Harmonic-Hermes-9B-GGUF` | `mac-runtime-proof` | 9B | `mac-lmstudio` | `blocked` | blocked until runtime artifact acquisition succeeds |
| 5 | `Qwen/Qwen3.5-9B` | `mac-runtime-proof` | 9B | `hf-transformers` | `blocked` | blocked from local Mac benchmark by model size; route to quantized sibling or cloud |
| 6 | `mradermacher/Harmonic-Hermes-9B-i1-GGUF` | `mac-runtime-proof` | 9B | `mac-lmstudio` | `blocked` | blocked until runtime artifact acquisition succeeds |
| 7 | `nex-agi/Nex-N2-mini` | `mac-runtime-proof` | 9B | `mac-mlx` | `blocked` | blocked from local Mac benchmark by model size; route to quantized sibling or cloud |
| 8 | `openbmb/AgentCPM-Report-GGUF` | `mac-runtime-proof` | 8B | `mac-lmstudio` | `blocked` | blocked until runtime artifact acquisition succeeds |
| 9 | `openbmb/MiniCPM-V-4.6-GPTQ` | `mac-runtime-proof` | 9B | `mac-lmstudio` | `blocked` | blocked until runtime artifact acquisition succeeds |
| 10 | `openbmb/MiniCPM-o-4_5-gguf` | `mac-runtime-proof` | 9B | `mac-lmstudio` | `blocked` | blocked until runtime artifact acquisition succeeds |
| 11 | `DuoNeural/OpenYourMind-Gemma4-12B-IT-Abliterated-GGUF` | `mac-runtime-proof` | 12B | `mac-lmstudio` | `blocked` | blocked until runtime artifact acquisition succeeds |
| 12 | `batiai/gemma-4-12B-it-GGUF` | `mac-runtime-proof` | 12B | `mac-lmstudio` | `blocked` | blocked until runtime artifact acquisition succeeds |
| 13 | `google/gemma-4-12B` | `mac-runtime-proof` | 12B | `hf-transformers` | `blocked` | blocked from local Mac benchmark by model size; route to quantized sibling or cloud |
| 14 | `google/gemma-4-12B-it` | `mac-runtime-proof` | 12B | `hf-transformers` | `blocked` | blocked from local Mac benchmark by model size; route to quantized sibling or cloud |
| 15 | `unsloth/gemma-4-12B-it-qat-GGUF` | `mac-runtime-proof` | 12B | `mac-lmstudio` | `blocked` | blocked until runtime artifact acquisition succeeds |
| 16 | `unsloth/gemma-4-12b-it-GGUF` | `mac-runtime-proof` | 12B | `mac-lmstudio` | `blocked` | blocked until runtime artifact acquisition succeeds |
| 17 | `bartowski/google_gemma-4-31B-it-GGUF` | `mac-runtime-proof` | 31B | `mac-lmstudio` | `blocked` | blocked until runtime artifact acquisition succeeds |
| 18 | `ggml-org/gemma-4-31B-it-GGUF` | `mac-runtime-proof` | 31B | `mac-lmstudio` | `blocked` | blocked from local Mac benchmark by model size; route to quantized sibling or cloud |
| 19 | `google/gemma-4-31B-it-qat-q4_0-gguf` | `mac-runtime-proof` | 31B | `mac-lmstudio` | `blocked` | blocked from local Mac benchmark by model size; route to quantized sibling or cloud |
| 20 | `lmstudio-community/gemma-4-31B-it-GGUF` | `mac-runtime-proof` | 31B | `mac-lmstudio` | `blocked` | blocked from local Mac benchmark by model size; route to quantized sibling or cloud |
| 21 | `unsloth/Qwen3.6-27B-GGUF` | `mac-runtime-proof` | 27B | `mac-lmstudio` | `blocked` | blocked until runtime artifact/load proof exists |
| 22 | `unsloth/Qwen3.6-27B-MTP-GGUF` | `mac-runtime-proof` | 27B | `mac-lmstudio` | `blocked` | blocked until runtime artifact/load proof exists |
| 23 | `unsloth/Qwen3.6-27B-UD-MLX-4bit` | `mac-runtime-proof` | 27B | `mac-mlx` | `blocked` | blocked until runtime artifact/load proof exists |
| 24 | `unsloth/gemma-4-31B-it-GGUF` | `mac-runtime-proof` | 31B | `mac-lmstudio` | `blocked` | blocked until runtime artifact/load proof exists |
| 25 | `Qwen/Qwen3-Coder-Next` | `mac-runtime-proof` | 80B total / 3B active | `hf-transformers` | `blocked` | blocked until runtime artifact/load proof exists |

## Lane Counts

| Lane | Count |
|---|---:|
| `cloud-teacher-proof` | 12 |
| `mac-runtime-proof` | 39 |
| `prompt-profile-repair` | 17 |
| `runtime-support-upgrade` | 9 |
| `specialist-runtime-proof` | 9 |
| `support-model-proof` | 68 |
| `watchlist` | 6 |

## Command Templates

### google/gemma-4-E4B-it-qat-mobile-transformers

- Lane: `mac-runtime-proof`
- Coverage: `blocked`
- Blocker: blocked until runtime artifact/load proof exists

```bash
source scripts/env.sh
# Uses SSD-backed Hugging Face cache from scripts/env.sh; add --local-files-only after acquisition.
./.venv/bin/python scripts/run_transformers_pilot_benchmark.py \
  --model google/gemma-4-E4B-it-qat-mobile-transformers \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --device auto \
  --dtype float16 \
  --require-no-extra-tool-text \
  --run-id google-gemma-4-e4b-it-qat-mobile-transformers-transformers-bfcl-pilot-$(date +%Y%m%d-%H%M%S)
```

### unsloth/NVIDIA-Nemotron-3-Nano-4B-GGUF

- Lane: `mac-runtime-proof`
- Coverage: `blocked`
- Blocker: blocked until runtime artifact acquisition succeeds

```bash
source scripts/env.sh
# Acquire the smallest compatible GGUF to /Volumes/PortableSSD first, then run a bounded endpoint pilot.
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \
  --model unsloth-nvidia-nemotron-3-nano-4b-gguf \
  --base-url http://127.0.0.1:<port>/v1 \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --require-no-extra-tool-text \
  --run-id unsloth-nvidia-nemotron-3-nano-4b-gguf-bfcl-pilot-$(date +%Y%m%d-%H%M%S)
```

### DJLougen/Harmonic-9B

- Lane: `mac-runtime-proof`
- Coverage: `blocked`
- Blocker: blocked from local Mac benchmark by model size; route to quantized sibling or cloud

```bash
source scripts/env.sh
# Uses SSD-backed Hugging Face cache from scripts/env.sh; add --local-files-only after acquisition.
./.venv/bin/python scripts/run_transformers_pilot_benchmark.py \
  --model DJLougen/Harmonic-9B \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --device auto \
  --dtype float16 \
  --require-no-extra-tool-text \
  --run-id djlougen-harmonic-9b-transformers-bfcl-pilot-$(date +%Y%m%d-%H%M%S)
```

### DJLougen/Harmonic-Hermes-9B-GGUF

- Lane: `mac-runtime-proof`
- Coverage: `blocked`
- Blocker: blocked until runtime artifact acquisition succeeds

```bash
source scripts/env.sh
# Acquire the smallest compatible GGUF to /Volumes/PortableSSD first, then run a bounded endpoint pilot.
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \
  --model djlougen-harmonic-hermes-9b-gguf \
  --base-url http://127.0.0.1:<port>/v1 \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --require-no-extra-tool-text \
  --run-id djlougen-harmonic-hermes-9b-gguf-bfcl-pilot-$(date +%Y%m%d-%H%M%S)
```

### Qwen/Qwen3.5-9B

- Lane: `mac-runtime-proof`
- Coverage: `blocked`
- Blocker: blocked from local Mac benchmark by model size; route to quantized sibling or cloud

```bash
source scripts/env.sh
# Uses SSD-backed Hugging Face cache from scripts/env.sh; add --local-files-only after acquisition.
./.venv/bin/python scripts/run_transformers_pilot_benchmark.py \
  --model Qwen/Qwen3.5-9B \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --device auto \
  --dtype float16 \
  --require-no-extra-tool-text \
  --run-id qwen-qwen3-5-9b-transformers-bfcl-pilot-$(date +%Y%m%d-%H%M%S)
```

### mradermacher/Harmonic-Hermes-9B-i1-GGUF

- Lane: `mac-runtime-proof`
- Coverage: `blocked`
- Blocker: blocked until runtime artifact acquisition succeeds

```bash
source scripts/env.sh
# Acquire the smallest compatible GGUF to /Volumes/PortableSSD first, then run a bounded endpoint pilot.
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \
  --model mradermacher-harmonic-hermes-9b-i1-gguf \
  --base-url http://127.0.0.1:<port>/v1 \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --require-no-extra-tool-text \
  --run-id mradermacher-harmonic-hermes-9b-i1-gguf-bfcl-pilot-$(date +%Y%m%d-%H%M%S)
```

### nex-agi/Nex-N2-mini

- Lane: `mac-runtime-proof`
- Coverage: `blocked`
- Blocker: blocked from local Mac benchmark by model size; route to quantized sibling or cloud

```bash
source scripts/env.sh
# Acquire the MLX model to the SSD Hugging Face cache first.
./.venv/bin/python scripts/run_local_pilot_benchmark.py \
  --model nex-agi/Nex-N2-mini \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --require-no-extra-tool-text \
  --run-id nex-agi-nex-n2-mini-local-bfcl-pilot-$(date +%Y%m%d-%H%M%S)
```

### openbmb/AgentCPM-Report-GGUF

- Lane: `mac-runtime-proof`
- Coverage: `blocked`
- Blocker: blocked until runtime artifact acquisition succeeds

```bash
source scripts/env.sh
# Acquire the smallest compatible GGUF to /Volumes/PortableSSD first, then run a bounded endpoint pilot.
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \
  --model openbmb-agentcpm-report-gguf \
  --base-url http://127.0.0.1:<port>/v1 \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --require-no-extra-tool-text \
  --run-id openbmb-agentcpm-report-gguf-bfcl-pilot-$(date +%Y%m%d-%H%M%S)
```

### openbmb/MiniCPM-V-4.6-GPTQ

- Lane: `mac-runtime-proof`
- Coverage: `blocked`
- Blocker: blocked until runtime artifact acquisition succeeds

```bash
source scripts/env.sh
# Acquire the smallest compatible local artifact to /Volumes/PortableSSD first, then expose it through a bounded OpenAI-compatible endpoint pilot.
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \
  --model openbmb-minicpm-v-4-6-gptq \
  --base-url http://127.0.0.1:<port>/v1 \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --require-no-extra-tool-text \
  --run-id openbmb-minicpm-v-4-6-gptq-bfcl-pilot-$(date +%Y%m%d-%H%M%S)
```

### openbmb/MiniCPM-o-4_5-gguf

- Lane: `mac-runtime-proof`
- Coverage: `blocked`
- Blocker: blocked until runtime artifact acquisition succeeds

```bash
source scripts/env.sh
# Acquire the smallest compatible GGUF to /Volumes/PortableSSD first, then run a bounded endpoint pilot.
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \
  --model openbmb-minicpm-o-4-5-gguf \
  --base-url http://127.0.0.1:<port>/v1 \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --require-no-extra-tool-text \
  --run-id openbmb-minicpm-o-4-5-gguf-bfcl-pilot-$(date +%Y%m%d-%H%M%S)
```

### DuoNeural/OpenYourMind-Gemma4-12B-IT-Abliterated-GGUF

- Lane: `mac-runtime-proof`
- Coverage: `blocked`
- Blocker: blocked until runtime artifact acquisition succeeds

```bash
source scripts/env.sh
# Acquire the smallest compatible GGUF to /Volumes/PortableSSD first, then run a bounded endpoint pilot.
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \
  --model duoneural-openyourmind-gemma4-12b-it-abliterated-gguf \
  --base-url http://127.0.0.1:<port>/v1 \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --require-no-extra-tool-text \
  --run-id duoneural-openyourmind-gemma4-12b-it-abliterated-gguf-bfcl-pilot-$(date +%Y%m%d-%H%M%S)
```

### batiai/gemma-4-12B-it-GGUF

- Lane: `mac-runtime-proof`
- Coverage: `blocked`
- Blocker: blocked until runtime artifact acquisition succeeds

```bash
source scripts/env.sh
# Acquire the smallest compatible GGUF to /Volumes/PortableSSD first, then run a bounded endpoint pilot.
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \
  --model batiai-gemma-4-12b-it-gguf \
  --base-url http://127.0.0.1:<port>/v1 \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --require-no-extra-tool-text \
  --run-id batiai-gemma-4-12b-it-gguf-bfcl-pilot-$(date +%Y%m%d-%H%M%S)
```

## Policy

- Run local Mac proofs before cloud proofs when the artifact is small enough and a supported runtime exists.
- Do not rerun `runtime-support-upgrade` candidates until the underlying runtime/converter has changed.
- Use cloud only for teacher/frontier candidates or when local runtime proof is structurally unavailable.
- Route embedders, rerankers, ASR/TTS, and VLM helpers through role-specific support-model proofs rather than Hermes BFCL chat pilots.
- Do not promote from smoke evidence. Promotion still requires strict tool-call, local pilot, selected official benchmark, latency, and rollback evidence.
- Keep model downloads, caches, evals, and exports on `/Volumes/PortableSSD` through `scripts/env.sh`.
