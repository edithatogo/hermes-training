# Standard Benchmark Manifest

Date: 2026-05-24

This manifest defines future benchmark execution without running expensive suites.

## Artifact Root

All generated benchmark artifacts must live under:

```text
/Volumes/PortableSSD/hermes-evals/standard-benchmarks/
```

## Suites

| Suite | Purpose | First Tier | Output Root | Run Gate |
|---|---|---|---|---|
| Local held-out strict tool-call | Hermes agent formatting gate | required for every agent model | `tool-call/<run-id>` | candidate runtime exists |
| BFCL subset | Function/tool calling comparability | pilot | `bfcl/<run-id>` | local strict gate no worse than baseline |
| IFEval | Instruction following | pilot | `ifeval/<run-id>` | candidate runtime exists |
| HumanEval/MBPP | Coding sanity | pilot | `coding/<run-id>` | candidate claims coding utility |
| lm-eval selected tasks | General comparability | candidate | `lm-eval/<run-id>` | runtime is stable and artifact roots are ready |
| Retrieval/MTEB-style | Memory/RAG quality | retrieval candidate | `retrieval/<run-id>` | retriever candidate exists |

## Required Run Record

Each future run card must include:

- model ID and revision
- adapter path and revision, if any
- runtime and endpoint
- prompt template and sampling settings
- suite name and version
- exact command
- repo commit
- environment summary
- raw output path
- normalized score path
- failure examples
- publish/no-publish decision

## No-Run Guardrail

This setup pass did not run BFCL, IFEval, coding, lm-eval, MTEB, paid Azure jobs, or new large model downloads.

## Command Manifests

- `reports/benchmark/manifests/local-tool-call-heldout-command-20260524.md`
- `reports/benchmark/manifests/bfcl-pilot-command-20260524.md`
- `reports/benchmark/manifests/ifeval-pilot-command-20260524.md`
- `reports/benchmark/manifests/coding-pilot-command-20260524.md`
- `reports/benchmark/manifests/lm-eval-smoke-command-20260524.md`
- `reports/benchmark/manifests/lm-eval-candidate-command-20260524.md`
- `reports/benchmark/manifests/retrieval-smoke-command-20260524.md`

## Endpoint Baselines

The endpoint harness ran against installed Ollama model `hermes3:8b` on 2026-05-24:

- Report: `reports/benchmark/endpoint-tool-call/hermes3-8b-ollama-heldout-20260524.md`
- Raw output root: `/Volumes/PortableSSD/hermes-evals/endpoint-tool-call-benchmark/hermes3-8b-ollama-heldout-20260524`
- Strict held-out pass: `0.250`
- Decision: baseline evidence only, not publishable.

The same endpoint harness also ran against installed Ollama model `sam860/LFM2:2.6b` on 2026-05-24:

- Report: `reports/benchmark/endpoint-tool-call/lfm2-2-6b-ollama-heldout-20260524.md`
- Raw output root: `/Volumes/PortableSSD/hermes-evals/endpoint-tool-call-benchmark/lfm2-2-6b-ollama-heldout-20260524`
- Strict held-out pass: `0.250`
- Decision: Liquid/LFM baseline evidence only, not publishable.

The current strongest local endpoint proof is the SSD-backed Qwen3 4B Q4_K_M GGUF served through llama.cpp:

- Report: `reports/benchmark/endpoint-tool-call/qwen3-q4km-llamacpp-heldout-20260524.md`
- Raw output root: `/Volumes/PortableSSD/hermes-evals/endpoint-tool-call-benchmark/qwen3-q4km-llamacpp-heldout-20260524`
- Strict held-out pass: `0.375`
- Decision: strongest local evidence so far, but still below the publication gate.
