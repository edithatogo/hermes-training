# Endpoint Pilot Benchmarks: Qwen3 4B Q4_K_M via llama.cpp

Date: 2026-05-24

## Scope

These are repo-native pilot checks for BFCL-style function calling, IFEval-style instruction following, and coding sanity. They are not full standardized benchmark replacements.

External packages were not available in the active environment:

- `lm_eval`: not installed
- `bfcl_eval`: not installed
- `openai`: not installed
- `evaluate`: not installed

The pilots ran through the same OpenAI-compatible llama.cpp endpoint used for the held-out tool-call benchmark.

## Runtime

```bash
/Volumes/PortableSSD/GitHub/llama.cpp/build/bin/llama-server \
  -m /Volumes/PortableSSD/hermes-exports/ollama/qwen3-4b-hermes-smoke/qwen3-4b-hermes-smoke-q4_K_M.gguf \
  --host 127.0.0.1 \
  --port 8091 \
  --alias qwen3-4b-hermes-smoke-q4_K_M \
  -c 4096 \
  -ngl auto
```

All final pilot runs used `--user-prefix /no_think` because the initial no-prefix pilot pass failed strict formatting due reasoning text.

## Results

| Pilot | Suite | Pass rate | Raw output |
|---|---|---:|---|
| BFCL-style | `benchmarks/endpoint_pilots/bfcl_pilot.json` | 0.333 | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/qwen3-q4km-llamacpp-bfcl-pilot-nothink-20260524` |
| IFEval-style | `benchmarks/endpoint_pilots/ifeval_pilot.json` | 0.667 | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/qwen3-q4km-llamacpp-ifeval-pilot-nothink-20260524` |
| Coding sanity | `benchmarks/endpoint_pilots/coding_pilot.json` | 1.000 | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/qwen3-q4km-llamacpp-coding-pilot-nothink-20260524` |

## Interpretation

The model is usable for simple coding-format tasks under `/no_think`, but it is not yet reliable enough for Hermes agent publication. The BFCL-style failures are schema-shape failures: the model emits `function` / `parameters` forms instead of the strict `name` / `arguments` contract.

The next training/data improvement should target schema-faithful tool calls, not more generic coding examples.
