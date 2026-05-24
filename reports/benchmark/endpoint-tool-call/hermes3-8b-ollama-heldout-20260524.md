# Endpoint Tool-Call Benchmark: hermes3:8b via Ollama

Date: 2026-05-24

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_endpoint_tool_call_benchmark.py \
  --model 'hermes3:8b' \
  --suite benchmarks/tool_call_local/heldout_suite.json \
  --base-url http://127.0.0.1:11434/v1 \
  --user-prefix /no_think \
  --run-id hermes3-8b-ollama-heldout-20260524 \
  --output-dir /Volumes/PortableSSD/hermes-evals/endpoint-tool-call-benchmark/hermes3-8b-ollama-heldout-20260524
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

- `/Volumes/PortableSSD/hermes-evals/endpoint-tool-call-benchmark/hermes3-8b-ollama-heldout-20260524/summary.md`
- `/Volumes/PortableSSD/hermes-evals/endpoint-tool-call-benchmark/hermes3-8b-ollama-heldout-20260524/results.jsonl`

## Decision

This is useful endpoint baseline evidence only. It does not make `hermes3:8b` a publishable adapter candidate and it does not satisfy the strict held-out publication gate.
