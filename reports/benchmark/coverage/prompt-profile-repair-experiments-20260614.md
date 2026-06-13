# Prompt/Profile Repair Experiments

Run ID: `prompt-profile-repair-experiments-20260614`
Created: `2026-06-14T00:00:00+00:00`

Purpose: turn the prompt/profile repair queue into concrete, no-download experiment commands using existing local runners.

## Matrix

| Candidate | Variant | Runner | Raw-output promotion allowed | Goal |
|---|---|---|---|---|
| `LGAI-EXAONE/EXAONE-4.0-1.2B` | `strict-suffix-copy-exact` | `endpoint` | yes | tighten raw Hermes tool-call formatting and exact argument copying |
| `LiquidAI/LFM2.5-8B-A1B-GGUF` | `strict-suffix-copy-exact` | `endpoint` | yes | tighten raw Hermes tool-call formatting and exact argument copying |
| `ManiacLabs/Qwen3.6-35B-A3B-2bit` | `strict-suffix-copy-exact` | `endpoint` | yes | tighten raw Hermes tool-call formatting and exact argument copying |
| `ManiacLabs/Qwen3.6-35B-A3B-2bit` | `empty-output-retry` | `endpoint` | yes | test whether a direct non-empty tool-call instruction clears strict-prompt blank output |
| `ManiacLabs/Qwen3.6-35B-A3B-2bit` | `qwen-no-think-prefill` | `endpoint` | yes | test Qwen no-think controls while preserving strict no-extra-tool-text scoring |
| `Mungert/Nanbeige4.1-3B-GGUF` | `strict-suffix-copy-exact` | `endpoint` | yes | tighten raw Hermes tool-call formatting and exact argument copying |
| `Mungert/Nanbeige4.1-3B-GGUF` | `empty-output-retry` | `endpoint` | yes | test whether a direct non-empty tool-call instruction clears strict-prompt blank output |
| `Nanbeige/Nanbeige4.1-3B` | `strict-suffix-copy-exact` | `local` | yes | tighten raw Hermes tool-call formatting and exact argument copying |
| `Qwen/Qwen3.5-0.8B` | `strict-suffix-copy-exact` | `local` | yes | tighten raw Hermes tool-call formatting and exact argument copying |
| `Qwen/Qwen3.5-0.8B` | `empty-output-retry` | `local` | yes | test whether a direct non-empty tool-call instruction clears strict-prompt blank output |
| `Qwen/Qwen3.5-0.8B` | `qwen-no-think-prefill` | `local` | yes | test Qwen no-think controls while preserving strict no-extra-tool-text scoring |
| `Qwen/Qwen3.5-2B` | `strict-suffix-copy-exact` | `local` | yes | tighten raw Hermes tool-call formatting and exact argument copying |
| `Qwen/Qwen3.5-2B` | `empty-output-retry` | `local` | yes | test whether a direct non-empty tool-call instruction clears strict-prompt blank output |
| `Qwen/Qwen3.5-2B` | `qwen-no-think-prefill` | `local` | yes | test Qwen no-think controls while preserving strict no-extra-tool-text scoring |
| `Qwen/Qwen3.6-35B-A3B` | `strict-suffix-copy-exact` | `local` | yes | tighten raw Hermes tool-call formatting and exact argument copying |
| `Qwen/Qwen3.6-35B-A3B` | `qwen-no-think-prefill` | `local` | yes | test Qwen no-think controls while preserving strict no-extra-tool-text scoring |
| `google/gemma-4-E2B-it-qat-q4_0-gguf` | `strict-suffix-copy-exact` | `endpoint` | yes | tighten raw Hermes tool-call formatting and exact argument copying |
| `ibm-granite/granite-4.1-3b` | `strict-suffix-copy-exact` | `local` | yes | tighten raw Hermes tool-call formatting and exact argument copying |
| `ibm-granite/granite-4.1-3b` | `granite-native-normalizer-analysis` | `local` | no; analysis only | measure score-only Granite native tool-call normalization and exact-copy repair |
| `mkadrlik/Hermes-Qwen3.5-4B-SFT-v7` | `strict-suffix-copy-exact` | `endpoint` | yes | tighten raw Hermes tool-call formatting and exact argument copying |
| `mkadrlik/Hermes-Qwen3.5-4B-SFT-v7` | `qwen-no-think-prefill` | `endpoint` | yes | test Qwen no-think controls while preserving strict no-extra-tool-text scoring |
| `mkadrlik/Hermes-Qwen3.5-9B-SFT-v7` | `strict-suffix-copy-exact` | `endpoint` | yes | tighten raw Hermes tool-call formatting and exact argument copying |
| `mkadrlik/Hermes-Qwen3.5-9B-SFT-v7` | `qwen-no-think-prefill` | `endpoint` | yes | test Qwen no-think controls while preserving strict no-extra-tool-text scoring |
| `mkadrlik/hermes-Qwen3.5-0.8B-SFT-v7-fresh` | `strict-suffix-copy-exact` | `endpoint` | yes | tighten raw Hermes tool-call formatting and exact argument copying |
| `mkadrlik/hermes-Qwen3.5-0.8B-SFT-v7-fresh` | `empty-output-retry` | `endpoint` | yes | test whether a direct non-empty tool-call instruction clears strict-prompt blank output |
| `mkadrlik/hermes-Qwen3.5-0.8B-SFT-v7-fresh` | `qwen-no-think-prefill` | `endpoint` | yes | test Qwen no-think controls while preserving strict no-extra-tool-text scoring |
| `mlx-community/NVIDIA-Nemotron-3-Nano-4B-OptiQ-4bit` | `strict-suffix-copy-exact` | `local` | yes | tighten raw Hermes tool-call formatting and exact argument copying |
| `mlx-community/gemma-4-E4B-it-qat-4bit` | `strict-suffix-copy-exact` | `local` | yes | tighten raw Hermes tool-call formatting and exact argument copying |
| `mlx-community/gemma-4-E4B-it-qat-4bit` | `gemma-native-normalizer-analysis` | `local` | no; analysis only | measure score-only Gemma native tool-fragment normalization without changing raw-output promotion rules |
| `nvidia/NVIDIA-Nemotron-3-Nano-4B-GGUF` | `strict-suffix-copy-exact` | `endpoint` | yes | tighten raw Hermes tool-call formatting and exact argument copying |
| `openbmb/MiniCPM5-1B-GGUF` | `strict-suffix-copy-exact` | `endpoint` | yes | tighten raw Hermes tool-call formatting and exact argument copying |
| `openbmb/MiniCPM5-1B-GGUF` | `minicpm-empty-tag-repair` | `endpoint` | yes | test a concise tool-tag envelope for MiniCPM helper candidates before any promotion claim |
| `openbmb/MiniCPM5-1B-MLX` | `strict-suffix-copy-exact` | `local` | yes | tighten raw Hermes tool-call formatting and exact argument copying |
| `openbmb/MiniCPM5-1B-MLX` | `empty-output-retry` | `local` | yes | test whether a direct non-empty tool-call instruction clears strict-prompt blank output |
| `openbmb/MiniCPM5-1B-MLX` | `minicpm-empty-tag-repair` | `local` | yes | test a concise tool-tag envelope for MiniCPM helper candidates before any promotion claim |

## Command Templates

### LGAI-EXAONE/EXAONE-4.0-1.2B / strict-suffix-copy-exact

- Goal: tighten raw Hermes tool-call formatting and exact argument copying
- Boundary: A repair experiment can only promote after raw strict outputs pass held-out tool-call, local pilots, official benchmark coverage, latency, and rollback checks.

```bash
source scripts/env.sh
# No download here: run only against the existing SSD-backed artifact or local endpoint.
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py --model lgai-exaone-exaone-4-0-1-2b --base-url 'http://127.0.0.1:<port>/v1' --suite benchmarks/endpoint_pilots/bfcl_pilot.json --max-tokens 512 --require-no-extra-tool-text --run-id 'lgai-exaone-exaone-4-0-1-2b-strict-suffix-copy-exact-$(date +%Y%m%d-%H%M%S)' --system-suffix ' Return only valid Hermes <tool_call> blocks when a listed tool satisfies the request. If no listed tool can satisfy the request, reply exactly: I cannot perform the action because the requested tool is not available. Copy argument values exactly from the user request; do not expand, summarize, or paraphrase string arguments.'
```

### LiquidAI/LFM2.5-8B-A1B-GGUF / strict-suffix-copy-exact

- Goal: tighten raw Hermes tool-call formatting and exact argument copying
- Boundary: A repair experiment can only promote after raw strict outputs pass held-out tool-call, local pilots, official benchmark coverage, latency, and rollback checks.

```bash
source scripts/env.sh
# No download here: run only against the existing SSD-backed artifact or local endpoint.
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py --model liquidai-lfm2-5-8b-a1b-gguf --base-url 'http://127.0.0.1:<port>/v1' --suite benchmarks/endpoint_pilots/bfcl_pilot.json --max-tokens 512 --require-no-extra-tool-text --run-id 'liquidai-lfm2-5-8b-a1b-gguf-strict-suffix-copy-exact-$(date +%Y%m%d-%H%M%S)' --system-suffix ' Return only valid Hermes <tool_call> blocks when a listed tool satisfies the request. If no listed tool can satisfy the request, reply exactly: I cannot perform the action because the requested tool is not available. Copy argument values exactly from the user request; do not expand, summarize, or paraphrase string arguments.'
```

### ManiacLabs/Qwen3.6-35B-A3B-2bit / strict-suffix-copy-exact

- Goal: tighten raw Hermes tool-call formatting and exact argument copying
- Boundary: A repair experiment can only promote after raw strict outputs pass held-out tool-call, local pilots, official benchmark coverage, latency, and rollback checks.

```bash
source scripts/env.sh
# No download here: run only against the existing SSD-backed artifact or local endpoint.
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py --model maniaclabs-qwen3-6-35b-a3b-2bit --base-url 'http://127.0.0.1:<port>/v1' --suite benchmarks/endpoint_pilots/bfcl_pilot.json --max-tokens 512 --require-no-extra-tool-text --run-id 'maniaclabs-qwen3-6-35b-a3b-2bit-strict-suffix-copy-exact-$(date +%Y%m%d-%H%M%S)' --system-suffix ' Return only valid Hermes <tool_call> blocks when a listed tool satisfies the request. If no listed tool can satisfy the request, reply exactly: I cannot perform the action because the requested tool is not available. Copy argument values exactly from the user request; do not expand, summarize, or paraphrase string arguments.'
```

### ManiacLabs/Qwen3.6-35B-A3B-2bit / empty-output-retry

- Goal: test whether a direct non-empty tool-call instruction clears strict-prompt blank output
- Boundary: A repair experiment can only promote after raw strict outputs pass held-out tool-call, local pilots, official benchmark coverage, latency, and rollback checks.

```bash
source scripts/env.sh
# No download here: run only against the existing SSD-backed artifact or local endpoint.
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py --model maniaclabs-qwen3-6-35b-a3b-2bit --base-url 'http://127.0.0.1:<port>/v1' --suite benchmarks/endpoint_pilots/bfcl_pilot.json --max-tokens 512 --require-no-extra-tool-text --run-id 'maniaclabs-qwen3-6-35b-a3b-2bit-empty-output-retry-$(date +%Y%m%d-%H%M%S)' --system-suffix ' Return only valid Hermes <tool_call> blocks when a listed tool satisfies the request. If no listed tool can satisfy the request, reply exactly: I cannot perform the action because the requested tool is not available. If a listed tool can satisfy the request, emit the tool call instead of an empty answer.'
```

### ManiacLabs/Qwen3.6-35B-A3B-2bit / qwen-no-think-prefill

- Goal: test Qwen no-think controls while preserving strict no-extra-tool-text scoring
- Boundary: A repair experiment can only promote after raw strict outputs pass held-out tool-call, local pilots, official benchmark coverage, latency, and rollback checks.

```bash
source scripts/env.sh
# No download here: run only against the existing SSD-backed artifact or local endpoint.
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py --model maniaclabs-qwen3-6-35b-a3b-2bit --base-url 'http://127.0.0.1:<port>/v1' --suite benchmarks/endpoint_pilots/bfcl_pilot.json --max-tokens 512 --require-no-extra-tool-text --run-id 'maniaclabs-qwen3-6-35b-a3b-2bit-qwen-no-think-prefill-$(date +%Y%m%d-%H%M%S)' --system-suffix ' Return only valid Hermes <tool_call> blocks when a listed tool satisfies the request. If no listed tool can satisfy the request, reply exactly: I cannot perform the action because the requested tool is not available. Copy argument values exactly from the user request; do not expand, summarize, or paraphrase string arguments.' --user-prefix /no_think --assistant-prefill '<think>

</think>

'
```

### Mungert/Nanbeige4.1-3B-GGUF / strict-suffix-copy-exact

- Goal: tighten raw Hermes tool-call formatting and exact argument copying
- Boundary: A repair experiment can only promote after raw strict outputs pass held-out tool-call, local pilots, official benchmark coverage, latency, and rollback checks.

```bash
source scripts/env.sh
# No download here: run only against the existing SSD-backed artifact or local endpoint.
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py --model mungert-nanbeige4-1-3b-gguf --base-url 'http://127.0.0.1:<port>/v1' --suite benchmarks/endpoint_pilots/bfcl_pilot.json --max-tokens 512 --require-no-extra-tool-text --run-id 'mungert-nanbeige4-1-3b-gguf-strict-suffix-copy-exact-$(date +%Y%m%d-%H%M%S)' --system-suffix ' Return only valid Hermes <tool_call> blocks when a listed tool satisfies the request. If no listed tool can satisfy the request, reply exactly: I cannot perform the action because the requested tool is not available. Copy argument values exactly from the user request; do not expand, summarize, or paraphrase string arguments.'
```

### Mungert/Nanbeige4.1-3B-GGUF / empty-output-retry

- Goal: test whether a direct non-empty tool-call instruction clears strict-prompt blank output
- Boundary: A repair experiment can only promote after raw strict outputs pass held-out tool-call, local pilots, official benchmark coverage, latency, and rollback checks.

```bash
source scripts/env.sh
# No download here: run only against the existing SSD-backed artifact or local endpoint.
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py --model mungert-nanbeige4-1-3b-gguf --base-url 'http://127.0.0.1:<port>/v1' --suite benchmarks/endpoint_pilots/bfcl_pilot.json --max-tokens 512 --require-no-extra-tool-text --run-id 'mungert-nanbeige4-1-3b-gguf-empty-output-retry-$(date +%Y%m%d-%H%M%S)' --system-suffix ' Return only valid Hermes <tool_call> blocks when a listed tool satisfies the request. If no listed tool can satisfy the request, reply exactly: I cannot perform the action because the requested tool is not available. If a listed tool can satisfy the request, emit the tool call instead of an empty answer.'
```

### Nanbeige/Nanbeige4.1-3B / strict-suffix-copy-exact

- Goal: tighten raw Hermes tool-call formatting and exact argument copying
- Boundary: A repair experiment can only promote after raw strict outputs pass held-out tool-call, local pilots, official benchmark coverage, latency, and rollback checks.

```bash
source scripts/env.sh
# No download here: run only against the existing SSD-backed artifact or local endpoint.
./.venv/bin/python scripts/run_local_pilot_benchmark.py --model Nanbeige/Nanbeige4.1-3B --suite benchmarks/endpoint_pilots/bfcl_pilot.json --max-tokens 512 --require-no-extra-tool-text --run-id 'nanbeige-nanbeige4-1-3b-strict-suffix-copy-exact-$(date +%Y%m%d-%H%M%S)' --system-suffix ' Return only valid Hermes <tool_call> blocks when a listed tool satisfies the request. If no listed tool can satisfy the request, reply exactly: I cannot perform the action because the requested tool is not available. Copy argument values exactly from the user request; do not expand, summarize, or paraphrase string arguments.'
```

### Qwen/Qwen3.5-0.8B / strict-suffix-copy-exact

- Goal: tighten raw Hermes tool-call formatting and exact argument copying
- Boundary: A repair experiment can only promote after raw strict outputs pass held-out tool-call, local pilots, official benchmark coverage, latency, and rollback checks.

```bash
source scripts/env.sh
# No download here: run only against the existing SSD-backed artifact or local endpoint.
./.venv/bin/python scripts/run_local_pilot_benchmark.py --model Qwen/Qwen3.5-0.8B --suite benchmarks/endpoint_pilots/bfcl_pilot.json --max-tokens 512 --require-no-extra-tool-text --run-id 'qwen-qwen3-5-0-8b-strict-suffix-copy-exact-$(date +%Y%m%d-%H%M%S)' --system-suffix ' Return only valid Hermes <tool_call> blocks when a listed tool satisfies the request. If no listed tool can satisfy the request, reply exactly: I cannot perform the action because the requested tool is not available. Copy argument values exactly from the user request; do not expand, summarize, or paraphrase string arguments.'
```

### Qwen/Qwen3.5-0.8B / empty-output-retry

- Goal: test whether a direct non-empty tool-call instruction clears strict-prompt blank output
- Boundary: A repair experiment can only promote after raw strict outputs pass held-out tool-call, local pilots, official benchmark coverage, latency, and rollback checks.

```bash
source scripts/env.sh
# No download here: run only against the existing SSD-backed artifact or local endpoint.
./.venv/bin/python scripts/run_local_pilot_benchmark.py --model Qwen/Qwen3.5-0.8B --suite benchmarks/endpoint_pilots/bfcl_pilot.json --max-tokens 512 --require-no-extra-tool-text --run-id 'qwen-qwen3-5-0-8b-empty-output-retry-$(date +%Y%m%d-%H%M%S)' --system-suffix ' Return only valid Hermes <tool_call> blocks when a listed tool satisfies the request. If no listed tool can satisfy the request, reply exactly: I cannot perform the action because the requested tool is not available. If a listed tool can satisfy the request, emit the tool call instead of an empty answer.'
```

### Qwen/Qwen3.5-0.8B / qwen-no-think-prefill

- Goal: test Qwen no-think controls while preserving strict no-extra-tool-text scoring
- Boundary: A repair experiment can only promote after raw strict outputs pass held-out tool-call, local pilots, official benchmark coverage, latency, and rollback checks.

```bash
source scripts/env.sh
# No download here: run only against the existing SSD-backed artifact or local endpoint.
./.venv/bin/python scripts/run_local_pilot_benchmark.py --model Qwen/Qwen3.5-0.8B --suite benchmarks/endpoint_pilots/bfcl_pilot.json --max-tokens 512 --require-no-extra-tool-text --run-id 'qwen-qwen3-5-0-8b-qwen-no-think-prefill-$(date +%Y%m%d-%H%M%S)' --system-suffix ' Return only valid Hermes <tool_call> blocks when a listed tool satisfies the request. If no listed tool can satisfy the request, reply exactly: I cannot perform the action because the requested tool is not available. Copy argument values exactly from the user request; do not expand, summarize, or paraphrase string arguments.' --user-prefix /no_think --assistant-prefill '<think>

</think>

'
```

### Qwen/Qwen3.5-2B / strict-suffix-copy-exact

- Goal: tighten raw Hermes tool-call formatting and exact argument copying
- Boundary: A repair experiment can only promote after raw strict outputs pass held-out tool-call, local pilots, official benchmark coverage, latency, and rollback checks.

```bash
source scripts/env.sh
# No download here: run only against the existing SSD-backed artifact or local endpoint.
./.venv/bin/python scripts/run_local_pilot_benchmark.py --model Qwen/Qwen3.5-2B --suite benchmarks/endpoint_pilots/bfcl_pilot.json --max-tokens 512 --require-no-extra-tool-text --run-id 'qwen-qwen3-5-2b-strict-suffix-copy-exact-$(date +%Y%m%d-%H%M%S)' --system-suffix ' Return only valid Hermes <tool_call> blocks when a listed tool satisfies the request. If no listed tool can satisfy the request, reply exactly: I cannot perform the action because the requested tool is not available. Copy argument values exactly from the user request; do not expand, summarize, or paraphrase string arguments.'
```

### Qwen/Qwen3.5-2B / empty-output-retry

- Goal: test whether a direct non-empty tool-call instruction clears strict-prompt blank output
- Boundary: A repair experiment can only promote after raw strict outputs pass held-out tool-call, local pilots, official benchmark coverage, latency, and rollback checks.

```bash
source scripts/env.sh
# No download here: run only against the existing SSD-backed artifact or local endpoint.
./.venv/bin/python scripts/run_local_pilot_benchmark.py --model Qwen/Qwen3.5-2B --suite benchmarks/endpoint_pilots/bfcl_pilot.json --max-tokens 512 --require-no-extra-tool-text --run-id 'qwen-qwen3-5-2b-empty-output-retry-$(date +%Y%m%d-%H%M%S)' --system-suffix ' Return only valid Hermes <tool_call> blocks when a listed tool satisfies the request. If no listed tool can satisfy the request, reply exactly: I cannot perform the action because the requested tool is not available. If a listed tool can satisfy the request, emit the tool call instead of an empty answer.'
```

### Qwen/Qwen3.5-2B / qwen-no-think-prefill

- Goal: test Qwen no-think controls while preserving strict no-extra-tool-text scoring
- Boundary: A repair experiment can only promote after raw strict outputs pass held-out tool-call, local pilots, official benchmark coverage, latency, and rollback checks.

```bash
source scripts/env.sh
# No download here: run only against the existing SSD-backed artifact or local endpoint.
./.venv/bin/python scripts/run_local_pilot_benchmark.py --model Qwen/Qwen3.5-2B --suite benchmarks/endpoint_pilots/bfcl_pilot.json --max-tokens 512 --require-no-extra-tool-text --run-id 'qwen-qwen3-5-2b-qwen-no-think-prefill-$(date +%Y%m%d-%H%M%S)' --system-suffix ' Return only valid Hermes <tool_call> blocks when a listed tool satisfies the request. If no listed tool can satisfy the request, reply exactly: I cannot perform the action because the requested tool is not available. Copy argument values exactly from the user request; do not expand, summarize, or paraphrase string arguments.' --user-prefix /no_think --assistant-prefill '<think>

</think>

'
```

### Qwen/Qwen3.6-35B-A3B / strict-suffix-copy-exact

- Goal: tighten raw Hermes tool-call formatting and exact argument copying
- Boundary: A repair experiment can only promote after raw strict outputs pass held-out tool-call, local pilots, official benchmark coverage, latency, and rollback checks.

```bash
source scripts/env.sh
# No download here: run only against the existing SSD-backed artifact or local endpoint.
./.venv/bin/python scripts/run_local_pilot_benchmark.py --model Qwen/Qwen3.6-35B-A3B --suite benchmarks/endpoint_pilots/bfcl_pilot.json --max-tokens 512 --require-no-extra-tool-text --run-id 'qwen-qwen3-6-35b-a3b-strict-suffix-copy-exact-$(date +%Y%m%d-%H%M%S)' --system-suffix ' Return only valid Hermes <tool_call> blocks when a listed tool satisfies the request. If no listed tool can satisfy the request, reply exactly: I cannot perform the action because the requested tool is not available. Copy argument values exactly from the user request; do not expand, summarize, or paraphrase string arguments.'
```

### Qwen/Qwen3.6-35B-A3B / qwen-no-think-prefill

- Goal: test Qwen no-think controls while preserving strict no-extra-tool-text scoring
- Boundary: A repair experiment can only promote after raw strict outputs pass held-out tool-call, local pilots, official benchmark coverage, latency, and rollback checks.

```bash
source scripts/env.sh
# No download here: run only against the existing SSD-backed artifact or local endpoint.
./.venv/bin/python scripts/run_local_pilot_benchmark.py --model Qwen/Qwen3.6-35B-A3B --suite benchmarks/endpoint_pilots/bfcl_pilot.json --max-tokens 512 --require-no-extra-tool-text --run-id 'qwen-qwen3-6-35b-a3b-qwen-no-think-prefill-$(date +%Y%m%d-%H%M%S)' --system-suffix ' Return only valid Hermes <tool_call> blocks when a listed tool satisfies the request. If no listed tool can satisfy the request, reply exactly: I cannot perform the action because the requested tool is not available. Copy argument values exactly from the user request; do not expand, summarize, or paraphrase string arguments.' --user-prefix /no_think --assistant-prefill '<think>

</think>

'
```

### google/gemma-4-E2B-it-qat-q4_0-gguf / strict-suffix-copy-exact

- Goal: tighten raw Hermes tool-call formatting and exact argument copying
- Boundary: A repair experiment can only promote after raw strict outputs pass held-out tool-call, local pilots, official benchmark coverage, latency, and rollback checks.

```bash
source scripts/env.sh
# No download here: run only against the existing SSD-backed artifact or local endpoint.
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py --model google-gemma-4-e2b-it-qat-q4-0-gguf --base-url 'http://127.0.0.1:<port>/v1' --suite benchmarks/endpoint_pilots/bfcl_pilot.json --max-tokens 512 --require-no-extra-tool-text --run-id 'google-gemma-4-e2b-it-qat-q4-0-gguf-strict-suffix-copy-exact-$(date +%Y%m%d-%H%M%S)' --system-suffix ' Return only valid Hermes <tool_call> blocks when a listed tool satisfies the request. If no listed tool can satisfy the request, reply exactly: I cannot perform the action because the requested tool is not available. Copy argument values exactly from the user request; do not expand, summarize, or paraphrase string arguments.'
```

### ibm-granite/granite-4.1-3b / strict-suffix-copy-exact

- Goal: tighten raw Hermes tool-call formatting and exact argument copying
- Boundary: A repair experiment can only promote after raw strict outputs pass held-out tool-call, local pilots, official benchmark coverage, latency, and rollback checks.

```bash
source scripts/env.sh
# No download here: run only against the existing SSD-backed artifact or local endpoint.
./.venv/bin/python scripts/run_local_pilot_benchmark.py --model ibm-granite/granite-4.1-3b --suite benchmarks/endpoint_pilots/bfcl_pilot.json --max-tokens 512 --require-no-extra-tool-text --run-id 'ibm-granite-granite-4-1-3b-strict-suffix-copy-exact-$(date +%Y%m%d-%H%M%S)' --system-suffix ' Return only valid Hermes <tool_call> blocks when a listed tool satisfies the request. If no listed tool can satisfy the request, reply exactly: I cannot perform the action because the requested tool is not available. Copy argument values exactly from the user request; do not expand, summarize, or paraphrase string arguments.'
```

### ibm-granite/granite-4.1-3b / granite-native-normalizer-analysis

- Goal: measure score-only Granite native tool-call normalization and exact-copy repair
- Boundary: A repair experiment can only promote after raw strict outputs pass held-out tool-call, local pilots, official benchmark coverage, latency, and rollback checks.

```bash
source scripts/env.sh
# No download here: run only against the existing SSD-backed artifact or local endpoint.
./.venv/bin/python scripts/run_local_pilot_benchmark.py --model ibm-granite/granite-4.1-3b --suite benchmarks/endpoint_pilots/bfcl_pilot.json --max-tokens 512 --require-no-extra-tool-text --run-id 'ibm-granite-granite-4-1-3b-granite-native-normalizer-analysis-$(date +%Y%m%d-%H%M%S)' --system-suffix ' Return only valid Hermes <tool_call> blocks when a listed tool satisfies the request. If no listed tool can satisfy the request, reply exactly: I cannot perform the action because the requested tool is not available. Copy argument values exactly from the user request; do not expand, summarize, or paraphrase string arguments.' --score-normalizer granite-native-tool-call
```

### mkadrlik/Hermes-Qwen3.5-4B-SFT-v7 / strict-suffix-copy-exact

- Goal: tighten raw Hermes tool-call formatting and exact argument copying
- Boundary: A repair experiment can only promote after raw strict outputs pass held-out tool-call, local pilots, official benchmark coverage, latency, and rollback checks.

```bash
source scripts/env.sh
# No download here: run only against the existing SSD-backed artifact or local endpoint.
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py --model mkadrlik-hermes-qwen3-5-4b-sft-v7 --base-url 'http://127.0.0.1:<port>/v1' --suite benchmarks/endpoint_pilots/bfcl_pilot.json --max-tokens 512 --require-no-extra-tool-text --run-id 'mkadrlik-hermes-qwen3-5-4b-sft-v7-strict-suffix-copy-exact-$(date +%Y%m%d-%H%M%S)' --system-suffix ' Return only valid Hermes <tool_call> blocks when a listed tool satisfies the request. If no listed tool can satisfy the request, reply exactly: I cannot perform the action because the requested tool is not available. Copy argument values exactly from the user request; do not expand, summarize, or paraphrase string arguments.'
```

### mkadrlik/Hermes-Qwen3.5-4B-SFT-v7 / qwen-no-think-prefill

- Goal: test Qwen no-think controls while preserving strict no-extra-tool-text scoring
- Boundary: A repair experiment can only promote after raw strict outputs pass held-out tool-call, local pilots, official benchmark coverage, latency, and rollback checks.

```bash
source scripts/env.sh
# No download here: run only against the existing SSD-backed artifact or local endpoint.
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py --model mkadrlik-hermes-qwen3-5-4b-sft-v7 --base-url 'http://127.0.0.1:<port>/v1' --suite benchmarks/endpoint_pilots/bfcl_pilot.json --max-tokens 512 --require-no-extra-tool-text --run-id 'mkadrlik-hermes-qwen3-5-4b-sft-v7-qwen-no-think-prefill-$(date +%Y%m%d-%H%M%S)' --system-suffix ' Return only valid Hermes <tool_call> blocks when a listed tool satisfies the request. If no listed tool can satisfy the request, reply exactly: I cannot perform the action because the requested tool is not available. Copy argument values exactly from the user request; do not expand, summarize, or paraphrase string arguments.' --user-prefix /no_think --assistant-prefill '<think>

</think>

'
```

### mkadrlik/Hermes-Qwen3.5-9B-SFT-v7 / strict-suffix-copy-exact

- Goal: tighten raw Hermes tool-call formatting and exact argument copying
- Boundary: A repair experiment can only promote after raw strict outputs pass held-out tool-call, local pilots, official benchmark coverage, latency, and rollback checks.

```bash
source scripts/env.sh
# No download here: run only against the existing SSD-backed artifact or local endpoint.
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py --model mkadrlik-hermes-qwen3-5-9b-sft-v7 --base-url 'http://127.0.0.1:<port>/v1' --suite benchmarks/endpoint_pilots/bfcl_pilot.json --max-tokens 512 --require-no-extra-tool-text --run-id 'mkadrlik-hermes-qwen3-5-9b-sft-v7-strict-suffix-copy-exact-$(date +%Y%m%d-%H%M%S)' --system-suffix ' Return only valid Hermes <tool_call> blocks when a listed tool satisfies the request. If no listed tool can satisfy the request, reply exactly: I cannot perform the action because the requested tool is not available. Copy argument values exactly from the user request; do not expand, summarize, or paraphrase string arguments.'
```

### mkadrlik/Hermes-Qwen3.5-9B-SFT-v7 / qwen-no-think-prefill

- Goal: test Qwen no-think controls while preserving strict no-extra-tool-text scoring
- Boundary: A repair experiment can only promote after raw strict outputs pass held-out tool-call, local pilots, official benchmark coverage, latency, and rollback checks.

```bash
source scripts/env.sh
# No download here: run only against the existing SSD-backed artifact or local endpoint.
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py --model mkadrlik-hermes-qwen3-5-9b-sft-v7 --base-url 'http://127.0.0.1:<port>/v1' --suite benchmarks/endpoint_pilots/bfcl_pilot.json --max-tokens 512 --require-no-extra-tool-text --run-id 'mkadrlik-hermes-qwen3-5-9b-sft-v7-qwen-no-think-prefill-$(date +%Y%m%d-%H%M%S)' --system-suffix ' Return only valid Hermes <tool_call> blocks when a listed tool satisfies the request. If no listed tool can satisfy the request, reply exactly: I cannot perform the action because the requested tool is not available. Copy argument values exactly from the user request; do not expand, summarize, or paraphrase string arguments.' --user-prefix /no_think --assistant-prefill '<think>

</think>

'
```

### mkadrlik/hermes-Qwen3.5-0.8B-SFT-v7-fresh / strict-suffix-copy-exact

- Goal: tighten raw Hermes tool-call formatting and exact argument copying
- Boundary: A repair experiment can only promote after raw strict outputs pass held-out tool-call, local pilots, official benchmark coverage, latency, and rollback checks.

```bash
source scripts/env.sh
# No download here: run only against the existing SSD-backed artifact or local endpoint.
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py --model mkadrlik-hermes-qwen3-5-0-8b-sft-v7-fresh --base-url 'http://127.0.0.1:<port>/v1' --suite benchmarks/endpoint_pilots/bfcl_pilot.json --max-tokens 512 --require-no-extra-tool-text --run-id 'mkadrlik-hermes-qwen3-5-0-8b-sft-v7-fresh-strict-suffix-copy-exact-$(date +%Y%m%d-%H%M%S)' --system-suffix ' Return only valid Hermes <tool_call> blocks when a listed tool satisfies the request. If no listed tool can satisfy the request, reply exactly: I cannot perform the action because the requested tool is not available. Copy argument values exactly from the user request; do not expand, summarize, or paraphrase string arguments.'
```

## Policy

- Do not redownload models from these commands.
- Keep score-only normalizer variants out of raw-output promotion decisions.
- Every command keeps `--require-no-extra-tool-text` enabled.
- Treat endpoint `<port>` placeholders as operator-supplied local runtime state, not a default service assumption.
