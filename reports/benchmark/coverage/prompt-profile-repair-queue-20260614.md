# Prompt/Profile Repair Queue

Run ID: `prompt-profile-repair-queue-20260614`
Created: `2026-06-13T16:12:47.976648+00:00`

Purpose: isolate runtime-proven or partially proven Hermes candidates whose next local work is prompt/profile repair, not training or remote execution.

## Queue

| Priority | Candidate | Params | Environment | Blocker | Repair hypothesis |
|---:|---|---|---|---|---|
| 1 | `LGAI-EXAONE/EXAONE-4.0-1.2B` | 1.2B | `mac-mlx` | blocked by strict Hermes tool-call formatting failure | test strict JSON envelope prompting on the existing GGUF endpoint; keep MLX blocked until loader support changes |
| 2 | `google/gemma-4-E2B-it-qat-q4_0-gguf` | E2B | `mac-lmstudio` | blocked by strict Hermes tool-call formatting failure | test Gemma native tool-fragment normalization or a stricter system suffix without changing raw outputs |
| 3 | `mkadrlik/hermes-Qwen3.5-0.8B-SFT-v7-fresh` | 0.8B | `mac-lmstudio` | blocked by empty/no-content generation under the strict prompt | retry only after a prompt profile changes prefill, stop tokens, or thinking/no-thinking controls |
| 4 | `LiquidAI/LFM2.5-8B-A1B-GGUF` | 8B total / 1B active | `mac-lmstudio` | blocked by strict Hermes tool-call formatting failure | test refusal wording and strict JSON/tool envelope profile on the existing GGUF endpoint |
| 5 | `openbmb/MiniCPM5-1B-GGUF` | 1B | `mac-lmstudio` | blocked by strict Hermes tool-call formatting failure | test MiniCPM tool-tag extraction only as score-only analysis before any helper promotion |
| 6 | `openbmb/MiniCPM5-1B-MLX` | 1B | `mac-mlx` | blocked by empty/no-content generation under the strict prompt | retry only after a prompt profile changes prefill, stop tokens, or thinking/no-thinking controls |
| 7 | `Qwen/Qwen3.5-0.8B` | 0.9B | `mac-mlx` | blocked by empty/no-content generation under the strict prompt | retry only after a prompt profile changes prefill, stop tokens, or thinking/no-thinking controls |
| 8 | `Qwen/Qwen3.5-2B` | 2B | `mac-mlx` | blocked by empty/no-content generation under the strict prompt | retry only after a prompt profile changes prefill, stop tokens, or thinking/no-thinking controls |
| 9 | `mlx-community/gemma-4-E4B-it-qat-4bit` | E4B | `mac-mlx` | blocked by strict Hermes tool-call formatting failure | test Gemma native tool-fragment normalization or a stricter system suffix without changing raw outputs |
| 10 | `ibm-granite/granite-4.1-3b` | 3B | `mac-mlx` | blocked by strict Hermes tool-call formatting failure | test Granite native tool-call normalization and copy-exact argument constraints |
| 11 | `mkadrlik/Hermes-Qwen3.5-4B-SFT-v7` | 4B | `mac-lmstudio` | blocked by strict Hermes tool-call formatting failure | test Qwen-style no-think/prefill controls and strict forbidden-tool wording |
| 12 | `Mungert/Nanbeige4.1-3B-GGUF` | 3B | `mac-lmstudio` | blocked by empty/no-content generation under the strict prompt | retry only after a prompt profile changes prefill, stop tokens, or thinking/no-thinking controls |
| 13 | `Nanbeige/Nanbeige4.1-3B` | 3B | `hf-transformers` | blocked by strict Hermes tool-call formatting failure | design a model-family-specific runtime profile, then rerun the strict BFCL pilot with no-extra-tool-text scoring |
| 14 | `mlx-community/NVIDIA-Nemotron-3-Nano-4B-OptiQ-4bit` | 4B | `mac-mlx` | blocked by strict Hermes tool-call formatting failure | design a model-family-specific runtime profile, then rerun the strict BFCL pilot with no-extra-tool-text scoring |
| 15 | `nvidia/NVIDIA-Nemotron-3-Nano-4B-GGUF` | 4B | `mac-lmstudio` | blocked by strict Hermes tool-call formatting failure | design a model-family-specific runtime profile, then rerun the strict BFCL pilot with no-extra-tool-text scoring |
| 16 | `ManiacLabs/Qwen3.6-35B-A3B-2bit` | 35B total / 3B active | `mac-lmstudio` | blocked by empty/no-content generation under the strict prompt | retry only after a prompt profile changes prefill, stop tokens, or thinking/no-thinking controls |
| 17 | `Qwen/Qwen3.6-35B-A3B` | 35B total / 3B active | `azure-cuda` | blocked by strict Hermes tool-call formatting failure | test Qwen-style no-think/prefill controls and strict forbidden-tool wording |
| 18 | `mkadrlik/Hermes-Qwen3.5-9B-SFT-v7` | 9B | `mac-lmstudio` | blocked by strict Hermes tool-call formatting failure | test Qwen-style no-think/prefill controls and strict forbidden-tool wording |

## Command Templates

### LGAI-EXAONE/EXAONE-4.0-1.2B

- Evidence: `reports/benchmark/endpoint-pilots/exaone4-12b-strict-suffix-copy-exact-repair-20260614.md`, `reports/benchmark/local-pilots/exaone4-12b-q4km-llamacpp-strict-bfcl-pilot-20260613.md`, `reports/runtime/exaone4-12b-q4km-llamacpp-smoke-20260612.md`
- Boundary: Prompt/profile repair is runtime analysis only; promotion still requires strict held-out tool-call, local pilots, official benchmark coverage, latency, and rollback evidence.

```bash
source scripts/env.sh
# No download here: start the existing local endpoint for this artifact, then rerun after a prompt/profile change.
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \
  --model lgai-exaone-exaone-4-0-1-2b \
  --base-url http://127.0.0.1:<port>/v1 \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --require-no-extra-tool-text \
  --run-id lgai-exaone-exaone-4-0-1-2b-prompt-profile-repair-$(date +%Y%m%d-%H%M%S)
```

### google/gemma-4-E2B-it-qat-q4_0-gguf

- Evidence: `reports/benchmark/local-pilots/gemma4-e2b-q4-llamacpp-strict-bfcl-pilot-20260613.md`, `reports/model-radar/gemma4-e2b-it-packaging-refresh-current-release-scan-20260612.md`, `reports/runtime/gemma4-e2b-q4-llamacpp-smoke-20260612.md`
- Boundary: Prompt/profile repair is runtime analysis only; promotion still requires strict held-out tool-call, local pilots, official benchmark coverage, latency, and rollback evidence.

```bash
source scripts/env.sh
# No download here: start the existing local endpoint for this artifact, then rerun after a prompt/profile change.
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \
  --model google-gemma-4-e2b-it-qat-q4-0-gguf \
  --base-url http://127.0.0.1:<port>/v1 \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --require-no-extra-tool-text \
  --run-id google-gemma-4-e2b-it-qat-q4-0-gguf-prompt-profile-repair-$(date +%Y%m%d-%H%M%S)
```

### mkadrlik/hermes-Qwen3.5-0.8B-SFT-v7-fresh

- Evidence: `reports/benchmark/local-pilots/hermes-qwen35-08b-sft-v7-q4km-llamacpp-strict-bfcl-pilot-20260613.md`
- Boundary: Prompt/profile repair is runtime analysis only; promotion still requires strict held-out tool-call, local pilots, official benchmark coverage, latency, and rollback evidence.

```bash
source scripts/env.sh
# No download here: start the existing local endpoint for this artifact, then rerun after a prompt/profile change.
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \
  --model mkadrlik-hermes-qwen3-5-0-8b-sft-v7-fresh \
  --base-url http://127.0.0.1:<port>/v1 \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --require-no-extra-tool-text \
  --run-id mkadrlik-hermes-qwen3-5-0-8b-sft-v7-fresh-prompt-profile-repair-$(date +%Y%m%d-%H%M%S)
```

### LiquidAI/LFM2.5-8B-A1B-GGUF

- Evidence: `reports/benchmark/local-pilots/lfm25-8b-a1b-q4km-llamacpp-strict-bfcl-pilot-20260613.md`, `reports/runtime/lfm25-8b-a1b-q4km-llamacpp-smoke-20260612.md`
- Boundary: Prompt/profile repair is runtime analysis only; promotion still requires strict held-out tool-call, local pilots, official benchmark coverage, latency, and rollback evidence.

```bash
source scripts/env.sh
# No download here: start the existing local endpoint for this artifact, then rerun after a prompt/profile change.
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \
  --model liquidai-lfm2-5-8b-a1b-gguf \
  --base-url http://127.0.0.1:<port>/v1 \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --require-no-extra-tool-text \
  --run-id liquidai-lfm2-5-8b-a1b-gguf-prompt-profile-repair-$(date +%Y%m%d-%H%M%S)
```

### openbmb/MiniCPM5-1B-GGUF

- Evidence: `reports/benchmark/local-pilots/minicpm5-1b-q4km-llamacpp-strict-bfcl-pilot-20260613.md`
- Boundary: Prompt/profile repair is runtime analysis only; promotion still requires strict held-out tool-call, local pilots, official benchmark coverage, latency, and rollback evidence.

```bash
source scripts/env.sh
# No download here: start the existing local endpoint for this artifact, then rerun after a prompt/profile change.
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \
  --model openbmb-minicpm5-1b-gguf \
  --base-url http://127.0.0.1:<port>/v1 \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --require-no-extra-tool-text \
  --run-id openbmb-minicpm5-1b-gguf-prompt-profile-repair-$(date +%Y%m%d-%H%M%S)
```

### openbmb/MiniCPM5-1B-MLX

- Evidence: `reports/benchmark/local-pilots/minicpm5-1b-mlx-empty-output-retry-repair-20260614.md`, `reports/benchmark/local-pilots/minicpm5-1b-mlx-empty-tag-repair-20260614.md`, `reports/benchmark/local-pilots/minicpm5-1b-mlx-local-bfcl-pilot-20260612.md`, `reports/benchmark/local-pilots/minicpm5-1b-mlx-strict-bfcl-pilot-20260613.md`, `reports/benchmark/local-pilots/minicpm5-1b-mlx-strict-suffix-copy-exact-repair-20260614.md`, `reports/benchmark/mlx-loglikelihood/minicpm5-1b-mlx-loglikelihood-smoke-20260612.md`
- Boundary: Prompt/profile repair is runtime analysis only; promotion still requires strict held-out tool-call, local pilots, official benchmark coverage, latency, and rollback evidence.

```bash
source scripts/env.sh
# No download here: use the SSD cache/local artifact already proven for this candidate.
./.venv/bin/python scripts/run_local_pilot_benchmark.py \
  --model openbmb/MiniCPM5-1B-MLX \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --require-no-extra-tool-text \
  --run-id openbmb-minicpm5-1b-mlx-prompt-profile-repair-$(date +%Y%m%d-%H%M%S)
```

### Qwen/Qwen3.5-0.8B

- Evidence: `reports/benchmark/local-pilots/qwen3-5-0-8b-local-bfcl-pilot-20260613.md`
- Boundary: Prompt/profile repair is runtime analysis only; promotion still requires strict held-out tool-call, local pilots, official benchmark coverage, latency, and rollback evidence.

```bash
source scripts/env.sh
# No download here: use the SSD cache/local artifact already proven for this candidate.
./.venv/bin/python scripts/run_local_pilot_benchmark.py \
  --model Qwen/Qwen3.5-0.8B \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --require-no-extra-tool-text \
  --run-id qwen-qwen3-5-0-8b-prompt-profile-repair-$(date +%Y%m%d-%H%M%S)
```

### Qwen/Qwen3.5-2B

- Evidence: `reports/benchmark/local-pilots/qwen3-5-2b-local-bfcl-pilot-20260613.md`
- Boundary: Prompt/profile repair is runtime analysis only; promotion still requires strict held-out tool-call, local pilots, official benchmark coverage, latency, and rollback evidence.

```bash
source scripts/env.sh
# No download here: use the SSD cache/local artifact already proven for this candidate.
./.venv/bin/python scripts/run_local_pilot_benchmark.py \
  --model Qwen/Qwen3.5-2B \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --require-no-extra-tool-text \
  --run-id qwen-qwen3-5-2b-prompt-profile-repair-$(date +%Y%m%d-%H%M%S)
```

### mlx-community/gemma-4-E4B-it-qat-4bit

- Evidence: `reports/benchmark/local-pilots/gemma4-e4b-native-normalized-pilot-20260612.md`, `reports/benchmark/local-pilots/gemma4-e4b-native-normalizer-analysis-repair-20260614.md`, `reports/benchmark/local-pilots/gemma4-e4b-strict-profile-no-extra-pilot-20260612.md`, `reports/benchmark/local-pilots/gemma4-e4b-strict-suffix-copy-exact-repair-20260614.md`, `reports/benchmark/mlx-loglikelihood/gemma4-e4b-mlx-loglikelihood-smoke-20260612.md`
- Boundary: Prompt/profile repair is runtime analysis only; promotion still requires strict held-out tool-call, local pilots, official benchmark coverage, latency, and rollback evidence.

```bash
source scripts/env.sh
# No download here: use the SSD cache/local artifact already proven for this candidate.
./.venv/bin/python scripts/run_local_pilot_benchmark.py \
  --model mlx-community/gemma-4-E4B-it-qat-4bit \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --require-no-extra-tool-text \
  --run-id mlx-community-gemma-4-e4b-it-qat-4bit-prompt-profile-repair-$(date +%Y%m%d-%H%M%S)
```

### ibm-granite/granite-4.1-3b

- Evidence: `reports/benchmark/local-pilots/granite41-3b-transformers-mps-fp16-strict-bfcl-pilot-20260613.md`
- Boundary: Prompt/profile repair is runtime analysis only; promotion still requires strict held-out tool-call, local pilots, official benchmark coverage, latency, and rollback evidence.

```bash
source scripts/env.sh
# No download here: use the SSD cache/local artifact already proven for this candidate.
./.venv/bin/python scripts/run_local_pilot_benchmark.py \
  --model ibm-granite/granite-4.1-3b \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --require-no-extra-tool-text \
  --run-id ibm-granite-granite-4-1-3b-prompt-profile-repair-$(date +%Y%m%d-%H%M%S)
```

### mkadrlik/Hermes-Qwen3.5-4B-SFT-v7

- Evidence: `reports/benchmark/local-pilots/hermes-qwen35-4b-sft-v7-q8-llamacpp-strict-bfcl-pilot-20260613.md`
- Boundary: Prompt/profile repair is runtime analysis only; promotion still requires strict held-out tool-call, local pilots, official benchmark coverage, latency, and rollback evidence.

```bash
source scripts/env.sh
# No download here: start the existing local endpoint for this artifact, then rerun after a prompt/profile change.
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \
  --model mkadrlik-hermes-qwen3-5-4b-sft-v7 \
  --base-url http://127.0.0.1:<port>/v1 \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --require-no-extra-tool-text \
  --run-id mkadrlik-hermes-qwen3-5-4b-sft-v7-prompt-profile-repair-$(date +%Y%m%d-%H%M%S)
```

### Mungert/Nanbeige4.1-3B-GGUF

- Evidence: `reports/benchmark/local-pilots/nanbeige41-3b-q4km-llamacpp-strict-bfcl-pilot-20260613.md`
- Boundary: Prompt/profile repair is runtime analysis only; promotion still requires strict held-out tool-call, local pilots, official benchmark coverage, latency, and rollback evidence.

```bash
source scripts/env.sh
# No download here: start the existing local endpoint for this artifact, then rerun after a prompt/profile change.
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \
  --model mungert-nanbeige4-1-3b-gguf \
  --base-url http://127.0.0.1:<port>/v1 \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --require-no-extra-tool-text \
  --run-id mungert-nanbeige4-1-3b-gguf-prompt-profile-repair-$(date +%Y%m%d-%H%M%S)
```

## Policy

- Do not redownload models for this queue; use existing SSD-backed artifacts or endpoints.
- Do not treat score-only normalizers as promotion evidence.
- Keep raw responses and normalized-for-score responses distinct in future reports.
- Keep strict `--require-no-extra-tool-text` scoring for Hermes tool-call claims.
