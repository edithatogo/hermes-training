# Constrained Envelope Repair Plan

Run ID: `constrained-envelope-repair-plan-20260614`
Created: `2026-06-13T16:34:19+00:00`

Rank completed prompt/profile repair failures for the next constrained-envelope or runtime-wrapper diagnostic without treating normalized or score-only behavior as promotion evidence.

## Promotion Boundary

This report is non-promotional. It may justify a constrained-envelope diagnostic, but it cannot promote a model.

## Ranked Candidates

| Candidate | Priority | Best variant | Best pass rate | Exact calls with extra text | Malformed/no calls | Action |
|---|---|---|---:|---:|---:|---|
| `Nanbeige/Nanbeige4.1-3B` | `high` | `strict-suffix-copy-exact` | 0.000 | 2 | 0 | Implement a non-promotional constrained-envelope diagnostic that strips or suppresses reasoning only when the raw response already contains exact Hermes calls, then rerun strict no-extra-text scoring before any promotion claim. |
| `Qwen/Qwen3.5-0.8B` | `medium` | `qwen-no-think-prefill` | 0.333 | 0 | 6 | Defer promotion and try a targeted prompt/runtime variant only after the high-priority envelope diagnostic is proven. |
| `Qwen/Qwen3.5-2B` | `medium` | `qwen-no-think-prefill` | 0.333 | 0 | 6 | Defer promotion and try a targeted prompt/runtime variant only after the high-priority envelope diagnostic is proven. |
| `google/gemma-4-E2B-it-qat-q4_0-gguf` | `medium` | `strict-suffix-copy-exact` | 0.333 | 0 | 2 | Defer promotion and try a targeted prompt/runtime variant only after the high-priority envelope diagnostic is proven. |
| `ibm-granite/granite-4.1-3b` | `medium` | `granite-native-normalizer-analysis` | 0.333 | 0 | 4 | Defer promotion and try a targeted prompt/runtime variant only after the high-priority envelope diagnostic is proven. |
| `LGAI-EXAONE/EXAONE-4.0-1.2B` | `low` | `strict-suffix-copy-exact` | 0.000 | 0 | 2 | Do not spend more local prompt-only cycles until runtime support or endpoint evidence changes. |
| `LiquidAI/LFM2.5-8B-A1B-GGUF` | `low` | `strict-suffix-copy-exact` | 0.000 | 0 | 2 | Do not spend more local prompt-only cycles until runtime support or endpoint evidence changes. |
| `mlx-community/NVIDIA-Nemotron-3-Nano-4B-OptiQ-4bit` | `low` | `strict-suffix-copy-exact` | 0.000 | 0 | 2 | Do not spend more local prompt-only cycles until runtime support or endpoint evidence changes. |
| `mlx-community/gemma-4-E4B-it-qat-4bit` | `low` | `gemma-native-normalizer-analysis` | 0.000 | 0 | 4 | Do not spend more local prompt-only cycles until runtime support or endpoint evidence changes. |
| `openbmb/MiniCPM5-1B-MLX` | `low` | `minicpm-empty-tag-repair` | 0.000 | 0 | 6 | Do not spend more local prompt-only cycles until runtime support or endpoint evidence changes. |

## Diagnostic Commands

### Nanbeige/Nanbeige4.1-3B

Non-promotional diagnostic only; preserve strict `--require-no-extra-tool-text` scoring.

```bash
source scripts/env.sh
RUN_STAMP=$(date +%Y%m%d-%H%M%S)
./.venv/bin/python scripts/run_local_pilot_benchmark.py --suite benchmarks/endpoint_pilots/bfcl_pilot.json --model 'Nanbeige/Nanbeige4.1-3B' --max-tokens 512 --require-no-extra-tool-text --run-id "nanbeige-nanbeige4-1-3b-constrained-envelope-diagnostic-${RUN_STAMP}" --system-suffix 'Return exactly one Hermes tool-call JSON object or JSON array and no prose, no markdown, no analysis, no hidden reasoning, and no tags.'
```

### Qwen/Qwen3.5-0.8B

Non-promotional diagnostic only; preserve strict `--require-no-extra-tool-text` scoring.

```bash
source scripts/env.sh
RUN_STAMP=$(date +%Y%m%d-%H%M%S)
./.venv/bin/python scripts/run_local_pilot_benchmark.py --suite benchmarks/endpoint_pilots/bfcl_pilot.json --model 'Qwen/Qwen3.5-0.8B' --max-tokens 512 --require-no-extra-tool-text --run-id "qwen-qwen3-5-0-8b-constrained-envelope-diagnostic-${RUN_STAMP}" --system-suffix 'Return exactly one Hermes tool-call JSON object or JSON array and no prose, no markdown, no analysis, no hidden reasoning, and no tags.'
```

### Qwen/Qwen3.5-2B

Non-promotional diagnostic only; preserve strict `--require-no-extra-tool-text` scoring.

```bash
source scripts/env.sh
RUN_STAMP=$(date +%Y%m%d-%H%M%S)
./.venv/bin/python scripts/run_local_pilot_benchmark.py --suite benchmarks/endpoint_pilots/bfcl_pilot.json --model 'Qwen/Qwen3.5-2B' --max-tokens 512 --require-no-extra-tool-text --run-id "qwen-qwen3-5-2b-constrained-envelope-diagnostic-${RUN_STAMP}" --system-suffix 'Return exactly one Hermes tool-call JSON object or JSON array and no prose, no markdown, no analysis, no hidden reasoning, and no tags.'
```

### google/gemma-4-E2B-it-qat-q4_0-gguf

Non-promotional diagnostic only; preserve strict `--require-no-extra-tool-text` scoring.

```bash
source scripts/env.sh
RUN_STAMP=$(date +%Y%m%d-%H%M%S)
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py --suite benchmarks/endpoint_pilots/bfcl_pilot.json --model 'google/gemma-4-E2B-it-qat-q4_0-gguf' --base-url 'http://127.0.0.1:<port>/v1' --max-tokens 512 --require-no-extra-tool-text --run-id "google-gemma-4-e2b-it-qat-q4-0-gguf-constrained-envelope-diagnostic-${RUN_STAMP}" --system-suffix 'Return exactly one Hermes tool-call JSON object or JSON array and no prose, no markdown, no analysis, no hidden reasoning, and no tags.'
```

### ibm-granite/granite-4.1-3b

Non-promotional diagnostic only; preserve strict `--require-no-extra-tool-text` scoring.

```bash
source scripts/env.sh
RUN_STAMP=$(date +%Y%m%d-%H%M%S)
./.venv/bin/python scripts/run_local_pilot_benchmark.py --suite benchmarks/endpoint_pilots/bfcl_pilot.json --model 'ibm-granite/granite-4.1-3b' --max-tokens 512 --require-no-extra-tool-text --run-id "ibm-granite-granite-4-1-3b-constrained-envelope-diagnostic-${RUN_STAMP}" --system-suffix 'Return exactly one Hermes tool-call JSON object or JSON array and no prose, no markdown, no analysis, no hidden reasoning, and no tags.'
```

### LGAI-EXAONE/EXAONE-4.0-1.2B

Non-promotional diagnostic only; preserve strict `--require-no-extra-tool-text` scoring.

```bash
source scripts/env.sh
RUN_STAMP=$(date +%Y%m%d-%H%M%S)
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py --suite benchmarks/endpoint_pilots/bfcl_pilot.json --model 'LGAI-EXAONE/EXAONE-4.0-1.2B' --base-url 'http://127.0.0.1:<port>/v1' --max-tokens 512 --require-no-extra-tool-text --run-id "lgai-exaone-exaone-4-0-1-2b-constrained-envelope-diagnostic-${RUN_STAMP}" --system-suffix 'Return exactly one Hermes tool-call JSON object or JSON array and no prose, no markdown, no analysis, no hidden reasoning, and no tags.'
```

### LiquidAI/LFM2.5-8B-A1B-GGUF

Non-promotional diagnostic only; preserve strict `--require-no-extra-tool-text` scoring.

```bash
source scripts/env.sh
RUN_STAMP=$(date +%Y%m%d-%H%M%S)
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py --suite benchmarks/endpoint_pilots/bfcl_pilot.json --model 'LiquidAI/LFM2.5-8B-A1B-GGUF' --base-url 'http://127.0.0.1:<port>/v1' --max-tokens 512 --require-no-extra-tool-text --run-id "liquidai-lfm2-5-8b-a1b-gguf-constrained-envelope-diagnostic-${RUN_STAMP}" --system-suffix 'Return exactly one Hermes tool-call JSON object or JSON array and no prose, no markdown, no analysis, no hidden reasoning, and no tags.'
```

### mlx-community/NVIDIA-Nemotron-3-Nano-4B-OptiQ-4bit

Non-promotional diagnostic only; preserve strict `--require-no-extra-tool-text` scoring.

```bash
source scripts/env.sh
RUN_STAMP=$(date +%Y%m%d-%H%M%S)
./.venv/bin/python scripts/run_local_pilot_benchmark.py --suite benchmarks/endpoint_pilots/bfcl_pilot.json --model 'mlx-community/NVIDIA-Nemotron-3-Nano-4B-OptiQ-4bit' --max-tokens 512 --require-no-extra-tool-text --run-id "mlx-community-nvidia-nemotron-3-nano-4b-optiq-4bit-constrained-envelope-diagnostic-${RUN_STAMP}" --system-suffix 'Return exactly one Hermes tool-call JSON object or JSON array and no prose, no markdown, no analysis, no hidden reasoning, and no tags.'
```

### mlx-community/gemma-4-E4B-it-qat-4bit

Non-promotional diagnostic only; preserve strict `--require-no-extra-tool-text` scoring.

```bash
source scripts/env.sh
RUN_STAMP=$(date +%Y%m%d-%H%M%S)
./.venv/bin/python scripts/run_local_pilot_benchmark.py --suite benchmarks/endpoint_pilots/bfcl_pilot.json --model 'mlx-community/gemma-4-E4B-it-qat-4bit' --max-tokens 512 --require-no-extra-tool-text --run-id "mlx-community-gemma-4-e4b-it-qat-4bit-constrained-envelope-diagnostic-${RUN_STAMP}" --system-suffix 'Return exactly one Hermes tool-call JSON object or JSON array and no prose, no markdown, no analysis, no hidden reasoning, and no tags.'
```

### openbmb/MiniCPM5-1B-MLX

Non-promotional diagnostic only; preserve strict `--require-no-extra-tool-text` scoring.

```bash
source scripts/env.sh
RUN_STAMP=$(date +%Y%m%d-%H%M%S)
./.venv/bin/python scripts/run_local_pilot_benchmark.py --suite benchmarks/endpoint_pilots/bfcl_pilot.json --model 'openbmb/MiniCPM5-1B-MLX' --max-tokens 512 --require-no-extra-tool-text --run-id "openbmb-minicpm5-1b-mlx-constrained-envelope-diagnostic-${RUN_STAMP}" --system-suffix 'Return exactly one Hermes tool-call JSON object or JSON array and no prose, no markdown, no analysis, no hidden reasoning, and no tags.'
```
