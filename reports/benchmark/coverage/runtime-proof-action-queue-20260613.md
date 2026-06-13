# Runtime Proof Action Queue

Run ID: `runtime-proof-action-queue-20260613`
Created: `2026-06-13T04:44:15.456595+00:00`

Purpose: convert the broad Hermes candidate radar into an executable queue. This file does not promote models; it identifies the next proof needed before spending local SSD space, Colab quota, or Azure hours.

## Immediate Local Queue

| Priority | Candidate | Lane | Params | Environment | Coverage | Next proof |
|---:|---|---|---|---|---|---|
| 1 | `Qwen/Qwen3-Coder-Next` | `mac-runtime-proof` | 80B total / 3B active | `hf-transformers` | `blocked` | blocked until runtime artifact/load proof exists |
| 2 | `Qwen/Qwen3-Coder-Next-GGUF` | `mac-runtime-proof` | 80B total / 3B active | `mac-lmstudio` | `blocked` | blocked until runtime artifact/load proof exists |
| 3 | `deepsweet/Qwen3.6-35B-A3B-MLX-oQ4` | `mac-runtime-proof` | 35B total / 3B active | `mac-mlx` | `blocked` | blocked until runtime artifact/load proof exists |
| 4 | `google/gemma-4-E4B-it-qat-mobile-transformers` | `mac-runtime-proof` | 3B | `hf-transformers` | `blocked` | blocked until runtime artifact/load proof exists |
| 5 | `localweights/Qwen3.6-35B-A3B-MTP-IQ4_XS-GGUF` | `mac-runtime-proof` | 35B total / 3B active | `mac-lmstudio` | `blocked` | blocked until runtime artifact/load proof exists |
| 6 | `mudler/Qwen3.6-35B-A3B-APEX-MTP-GGUF` | `mac-runtime-proof` | 35B total / 3B active | `mac-lmstudio` | `blocked` | blocked until runtime artifact/load proof exists |
| 7 | `unsloth/NVIDIA-Nemotron-3-Nano-4B-GGUF` | `mac-runtime-proof` | 4B | `mac-lmstudio` | `blocked` | blocked until runtime artifact/load proof exists |
| 8 | `unsloth/Qwen3.6-35B-A3B-MTP-GGUF` | `mac-runtime-proof` | 35B total / 3B active | `mac-lmstudio` | `blocked` | blocked until runtime artifact/load proof exists |
| 9 | `DJLougen/Harmonic-9B` | `mac-runtime-proof` | 9B | `hf-transformers` | `blocked` | blocked until runtime artifact/load proof exists |
| 10 | `DJLougen/Harmonic-Hermes-9B-GGUF` | `mac-runtime-proof` | 9B | `mac-lmstudio` | `blocked` | blocked until runtime artifact/load proof exists |
| 11 | `Qwen/Qwen3.5-9B` | `mac-runtime-proof` | 9B | `hf-transformers` | `blocked` | blocked until runtime artifact/load proof exists |
| 12 | `mradermacher/Harmonic-Hermes-9B-i1-GGUF` | `mac-runtime-proof` | 9B | `mac-lmstudio` | `blocked` | blocked until runtime artifact/load proof exists |
| 13 | `nex-agi/Nex-N2-mini` | `mac-runtime-proof` | 9B | `mac-mlx` | `blocked` | blocked until runtime artifact/load proof exists |
| 14 | `openbmb/AgentCPM-Report-GGUF` | `mac-runtime-proof` | 8B | `mac-lmstudio` | `blocked` | blocked until runtime artifact/load proof exists |
| 15 | `openbmb/MiniCPM-V-4.6-GPTQ` | `mac-runtime-proof` | 9B | `mac-lmstudio` | `blocked` | blocked until runtime artifact/load proof exists |
| 16 | `openbmb/MiniCPM-o-4_5-gguf` | `mac-runtime-proof` | 9B | `mac-lmstudio` | `blocked` | blocked until runtime artifact/load proof exists |
| 17 | `DuoNeural/OpenYourMind-Gemma4-12B-IT-Abliterated-GGUF` | `mac-runtime-proof` | 12B | `mac-lmstudio` | `blocked` | blocked until runtime artifact/load proof exists |
| 18 | `batiai/gemma-4-12B-it-GGUF` | `mac-runtime-proof` | 12B | `mac-lmstudio` | `blocked` | blocked until runtime artifact/load proof exists |
| 19 | `google/gemma-4-12B` | `mac-runtime-proof` | 12B | `hf-transformers` | `blocked` | blocked until runtime artifact/load proof exists |
| 20 | `google/gemma-4-12B-it` | `mac-runtime-proof` | 12B | `hf-transformers` | `blocked` | blocked until runtime artifact/load proof exists |
| 21 | `unsloth/gemma-4-12B-it-qat-GGUF` | `mac-runtime-proof` | 12B | `mac-lmstudio` | `blocked` | blocked until runtime artifact/load proof exists |
| 22 | `unsloth/gemma-4-12b-it-GGUF` | `mac-runtime-proof` | 12B | `mac-lmstudio` | `blocked` | blocked until runtime artifact/load proof exists |
| 23 | `bartowski/google_gemma-4-31B-it-GGUF` | `mac-runtime-proof` | 31B | `mac-lmstudio` | `blocked` | blocked until runtime artifact/load proof exists |
| 24 | `ggml-org/gemma-4-31B-it-GGUF` | `mac-runtime-proof` | 31B | `mac-lmstudio` | `blocked` | blocked until runtime artifact/load proof exists |
| 25 | `google/gemma-4-31B-it-qat-q4_0-gguf` | `mac-runtime-proof` | 31B | `mac-lmstudio` | `blocked` | blocked until runtime artifact/load proof exists |

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

### localweights/Qwen3.6-35B-A3B-MTP-IQ4_XS-GGUF

- Lane: `mac-runtime-proof`
- Coverage: `blocked`
- Blocker: blocked until runtime artifact/load proof exists

```bash
source scripts/env.sh
# Acquire the smallest compatible GGUF to /Volumes/PortableSSD first, then run a bounded endpoint pilot.
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \
  --model localweights-qwen3-6-35b-a3b-mtp-iq4-xs-gguf \
  --base-url http://127.0.0.1:<port>/v1 \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --run-id localweights-qwen3-6-35b-a3b-mtp-iq4-xs-gguf-bfcl-pilot-$(date +%Y%m%d-%H%M%S)
```

### mudler/Qwen3.6-35B-A3B-APEX-MTP-GGUF

- Lane: `mac-runtime-proof`
- Coverage: `blocked`
- Blocker: blocked until runtime artifact/load proof exists

```bash
source scripts/env.sh
# Acquire the smallest compatible GGUF to /Volumes/PortableSSD first, then run a bounded endpoint pilot.
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \
  --model mudler-qwen3-6-35b-a3b-apex-mtp-gguf \
  --base-url http://127.0.0.1:<port>/v1 \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --run-id mudler-qwen3-6-35b-a3b-apex-mtp-gguf-bfcl-pilot-$(date +%Y%m%d-%H%M%S)
```

### unsloth/NVIDIA-Nemotron-3-Nano-4B-GGUF

- Lane: `mac-runtime-proof`
- Coverage: `blocked`
- Blocker: blocked until runtime artifact/load proof exists

```bash
source scripts/env.sh
# Acquire the smallest compatible GGUF to /Volumes/PortableSSD first, then run a bounded endpoint pilot.
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \
  --model unsloth-nvidia-nemotron-3-nano-4b-gguf \
  --base-url http://127.0.0.1:<port>/v1 \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --run-id unsloth-nvidia-nemotron-3-nano-4b-gguf-bfcl-pilot-$(date +%Y%m%d-%H%M%S)
```

### unsloth/Qwen3.6-35B-A3B-MTP-GGUF

- Lane: `mac-runtime-proof`
- Coverage: `blocked`
- Blocker: blocked until runtime artifact/load proof exists

```bash
source scripts/env.sh
# Acquire the smallest compatible GGUF to /Volumes/PortableSSD first, then run a bounded endpoint pilot.
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \
  --model unsloth-qwen3-6-35b-a3b-mtp-gguf \
  --base-url http://127.0.0.1:<port>/v1 \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --run-id unsloth-qwen3-6-35b-a3b-mtp-gguf-bfcl-pilot-$(date +%Y%m%d-%H%M%S)
```

### DJLougen/Harmonic-9B

- Lane: `mac-runtime-proof`
- Coverage: `blocked`
- Blocker: blocked until runtime artifact/load proof exists

```bash
source scripts/env.sh
# Acquire the smallest compatible GGUF to /Volumes/PortableSSD first, then run a bounded endpoint pilot.
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \
  --model djlougen-harmonic-9b \
  --base-url http://127.0.0.1:<port>/v1 \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --run-id djlougen-harmonic-9b-bfcl-pilot-$(date +%Y%m%d-%H%M%S)
```

### DJLougen/Harmonic-Hermes-9B-GGUF

- Lane: `mac-runtime-proof`
- Coverage: `blocked`
- Blocker: blocked until runtime artifact/load proof exists

```bash
source scripts/env.sh
# Acquire the smallest compatible GGUF to /Volumes/PortableSSD first, then run a bounded endpoint pilot.
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \
  --model djlougen-harmonic-hermes-9b-gguf \
  --base-url http://127.0.0.1:<port>/v1 \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --run-id djlougen-harmonic-hermes-9b-gguf-bfcl-pilot-$(date +%Y%m%d-%H%M%S)
```

### Qwen/Qwen3.5-9B

- Lane: `mac-runtime-proof`
- Coverage: `blocked`
- Blocker: blocked until runtime artifact/load proof exists

```bash
source scripts/env.sh
# Acquire the smallest compatible GGUF to /Volumes/PortableSSD first, then run a bounded endpoint pilot.
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \
  --model qwen-qwen3-5-9b \
  --base-url http://127.0.0.1:<port>/v1 \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --run-id qwen-qwen3-5-9b-bfcl-pilot-$(date +%Y%m%d-%H%M%S)
```

### mradermacher/Harmonic-Hermes-9B-i1-GGUF

- Lane: `mac-runtime-proof`
- Coverage: `blocked`
- Blocker: blocked until runtime artifact/load proof exists

```bash
source scripts/env.sh
# Acquire the smallest compatible GGUF to /Volumes/PortableSSD first, then run a bounded endpoint pilot.
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \
  --model mradermacher-harmonic-hermes-9b-i1-gguf \
  --base-url http://127.0.0.1:<port>/v1 \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --run-id mradermacher-harmonic-hermes-9b-i1-gguf-bfcl-pilot-$(date +%Y%m%d-%H%M%S)
```

## Policy

- Run local Mac proofs before cloud proofs when the artifact is small enough and a supported runtime exists.
- Do not rerun `runtime-support-upgrade` candidates until the underlying runtime/converter has changed.
- Use cloud only for teacher/frontier candidates or when local runtime proof is structurally unavailable.
- Route embedders, rerankers, ASR/TTS, and VLM helpers through role-specific support-model proofs rather than Hermes BFCL chat pilots.
- Do not promote from smoke evidence. Promotion still requires strict tool-call, local pilot, selected official benchmark, latency, and rollback evidence.
- Keep model downloads, caches, evals, and exports on `/Volumes/PortableSSD` through `scripts/env.sh`.
