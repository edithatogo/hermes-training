# Endpoint Tool-Call Benchmark: Qwen3 4B Q4_K_M via LM Studio

Date: 2026-05-24

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_endpoint_tool_call_benchmark.py \
  --model qwen3-4b-hermes-smoke-q4_K_M \
  --suite benchmarks/tool_call_local/heldout_suite.json \
  --base-url http://127.0.0.1:1234/v1 \
  --user-prefix /no_think \
  --run-id qwen3-q4km-lmstudio-heldout-20260524 \
  --output-dir /Volumes/PortableSSD/hermes-evals/endpoint-tool-call-benchmark/qwen3-q4km-lmstudio-heldout-20260524
```

## Result

| Metric | Score |
|---|---:|
| Strict pass rate | 0.500 |
| JSON validity rate | 0.333 |
| Argument accuracy rate | 0.333 |
| Runtime-normalized pass rate | 0.500 |
| Empty-think prefix cases | 0 |
| Invalid-tool handling rate | 1.000 |
| Multi-turn repair rate | 1.000 |

Raw output:

- `/Volumes/PortableSSD/hermes-evals/endpoint-tool-call-benchmark/qwen3-q4km-lmstudio-heldout-20260524/summary.md`
- `/Volumes/PortableSSD/hermes-evals/endpoint-tool-call-benchmark/qwen3-q4km-lmstudio-heldout-20260524/results.jsonl`

## Decision

This is now the strongest local endpoint result recorded for the current Qwen3 artifact. It is still not publication-ready because JSON validity and argument correctness remain below the strict Hermes agent gate.
