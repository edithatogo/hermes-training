# Endpoint Tool-Call Benchmark: Qwen3 4B Q4_K_M via llama.cpp

Date: 2026-05-24

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_endpoint_tool_call_benchmark.py \
  --model qwen3-4b-hermes-smoke-q4_K_M \
  --suite benchmarks/tool_call_local/heldout_suite.json \
  --base-url http://127.0.0.1:8091/v1 \
  --user-prefix /no_think \
  --run-id qwen3-q4km-llamacpp-heldout-20260524 \
  --output-dir /Volumes/PortableSSD/hermes-evals/endpoint-tool-call-benchmark/qwen3-q4km-llamacpp-heldout-20260524
```

Runtime command:

```bash
/Volumes/PortableSSD/GitHub/llama.cpp/build/bin/llama-server \
  -m /Volumes/PortableSSD/hermes-exports/ollama/qwen3-4b-hermes-smoke/qwen3-4b-hermes-smoke-q4_K_M.gguf \
  --host 127.0.0.1 \
  --port 8091 \
  --alias qwen3-4b-hermes-smoke-q4_K_M \
  -c 4096 \
  -ngl auto
```

## Result

| Metric | Score |
|---|---:|
| Strict pass rate | 0.375 |
| JSON validity rate | 0.333 |
| Argument accuracy rate | 0.333 |
| Runtime-normalized pass rate | 0.375 |
| Empty-think prefix cases | 0 |
| Invalid-tool handling rate | 0.500 |
| Multi-turn repair rate | 1.000 |

Raw output:

- `/Volumes/PortableSSD/hermes-evals/endpoint-tool-call-benchmark/qwen3-q4km-llamacpp-heldout-20260524/summary.md`
- `/Volumes/PortableSSD/hermes-evals/endpoint-tool-call-benchmark/qwen3-q4km-llamacpp-heldout-20260524/results.jsonl`

## Decision

This is the strongest local endpoint proof currently recorded, but it is still not publication-ready. It improves over the Ollama baselines on strict pass rate and invalid-tool handling, while failing the JSON validity and argument correctness categories.
