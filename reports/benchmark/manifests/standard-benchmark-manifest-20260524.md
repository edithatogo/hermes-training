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
| mem0 memory | Local memory add/search and recency quality | required for mem0 defaults | `mem0-memory-benchmark/<run-id>` | candidate mem0 config or reranker exists |
| mem0 embedding | Direct embedding retrieval quality | required for embedder swaps | `embedding-benchmark/<run-id>` | embedding endpoint exists |
| mem0 extraction | Memory-writing quality | required for extractor swaps | `mem0-extraction-benchmark/<run-id>` | extractor endpoint exists |

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

## Publication Gate

Benchmark publication remains blocked until a candidate satisfies the full evidence pack and Hermes-agent strict tool-call gate. The current gate record is:

`reports/benchmark/publication-readiness-gate-20260524.md`

## Command Manifests

- `reports/benchmark/manifests/local-tool-call-heldout-command-20260524.md`
- `reports/benchmark/manifests/bfcl-pilot-command-20260524.md`
- `reports/benchmark/manifests/ifeval-pilot-command-20260524.md`
- `reports/benchmark/manifests/coding-pilot-command-20260524.md`
- `reports/benchmark/manifests/lm-eval-smoke-command-20260524.md`
- `reports/benchmark/manifests/lm-eval-candidate-command-20260524.md`
- `reports/benchmark/manifests/retrieval-smoke-command-20260524.md`
- `reports/benchmark/manifests/mem0-benchmark-manifest-20260524.md`

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

The same SSD-backed Qwen3 4B Q4_K_M GGUF now also runs through LM Studio:

- Report: `reports/benchmark/endpoint-tool-call/qwen3-q4km-lmstudio-heldout-20260524.md`
- Raw output root: `/Volumes/PortableSSD/hermes-evals/endpoint-tool-call-benchmark/qwen3-q4km-lmstudio-heldout-20260524`
- Strict held-out pass: `0.500`
- Decision: strongest local endpoint evidence so far, but still below the publication gate.

## Endpoint Pilot Results

Repo-native endpoint pilots ran against the same Qwen3 4B Q4_K_M llama.cpp endpoint with `/no_think`:

- Report: `reports/benchmark/endpoint-pilots/qwen3-q4km-llamacpp-pilots-20260524.md`
- BFCL-style pilot: `0.333`
- IFEval-style pilot: `0.667`
- Coding sanity pilot: `1.000`
- Decision: useful engineering evidence only. Full BFCL/IFEval/lm-eval remain blocked until their harnesses are installed and validated.

The same repo-native endpoint pilots also ran against LM Studio with the SSD-backed Qwen3 4B Q4_K_M artifact:

- Report: `reports/benchmark/endpoint-pilots/qwen3-q4km-lmstudio-pilots-20260524.md`
- BFCL-style pilot: `0.000`
- IFEval-style pilot: `0.667`
- Coding sanity pilot: `1.000`
- Decision: LM Studio remains the stronger held-out strict tool-call runtime, but the pilot BFCL-style result reinforces that exact tool-call schema training is still required.

Hermes 4 14B Q4_K_M is now acquired, loaded, and benchmarked through llama.cpp:

- Runtime report: `reports/runtime/hermes4-14b-q4-llamacpp-smoke-20260524.md`
- Held-out report: `reports/benchmark/endpoint-tool-call/hermes4-14b-q4-llamacpp-heldout-20260524.md`
- Endpoint pilot report: `reports/benchmark/endpoint-pilots/hermes4-14b-q4-llamacpp-pilots-20260524.md`
- Strict held-out pass: `0.250`
- BFCL-style pilot: `0.000`
- IFEval-style pilot: `0.667`
- Coding sanity pilot: `1.000`
- Decision: local Hermes 4 baseline proof is complete, but it does not meet the strict Hermes agent publication gate.

## mem0 Baselines

The mem0 benchmark index is:

- `reports/benchmark/mem0/index.md`

Current baseline pattern:

- direct `nomic-embed-text:latest` embedding retrieval has top-1 `0.667` and Recall@3 `1.000`
- live mem0 recency suite has raw pass `0.400`
- inline `score_plus_created_at_rank` reranking improves that same recency suite to `1.000`
- installed extractor candidates are weak on the first extraction smoke: both `sam860/LFM2:2.6b` and `hermes3:8b` scored `0.333`
