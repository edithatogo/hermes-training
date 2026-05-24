# Endpoint Tool-Call Benchmark: Hermes 4 14B Q4 via llama.cpp

Date: 2026-05-24

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_endpoint_tool_call_benchmark.py \
  --model hermes-4-14b-q4 \
  --suite benchmarks/tool_call_local/heldout_suite.json \
  --base-url http://127.0.0.1:8092/v1 \
  --user-prefix /no_think \
  --run-id hermes4-14b-q4-llamacpp-heldout-20260524 \
  --output-dir /Volumes/PortableSSD/hermes-evals/endpoint-tool-call-benchmark/hermes4-14b-q4-llamacpp-heldout-20260524
```

## Result

| Metric | Score |
|---|---:|
| Strict pass rate | 0.250 |
| JSON validity rate | 0.333 |
| Argument accuracy rate | 0.333 |
| Runtime-normalized pass rate | 0.250 |
| Empty-think prefix cases | 0 |
| Invalid-tool handling rate | 0.000 |
| Multi-turn repair rate | 1.000 |

Raw output:

- `/Volumes/PortableSSD/hermes-evals/endpoint-tool-call-benchmark/hermes4-14b-q4-llamacpp-heldout-20260524/summary.md`
- `/Volumes/PortableSSD/hermes-evals/endpoint-tool-call-benchmark/hermes4-14b-q4-llamacpp-heldout-20260524/results.jsonl`

## Decision

Hermes 4 14B is locally runnable and useful as a baseline, but this endpoint result is not publication-ready for a strict Hermes agent model. The failure shape matches the other local runtimes: exact tool-call JSON schema and invalid-tool refusal behavior need targeted data/training.
