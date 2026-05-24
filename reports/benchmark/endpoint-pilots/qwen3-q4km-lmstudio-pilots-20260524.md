# Endpoint Pilot Benchmarks: Qwen3 4B Q4_K_M via LM Studio

Date: 2026-05-24

## Scope

These are repo-native pilot checks through LM Studio's OpenAI-compatible endpoint. They use the same suites as the llama.cpp pilot report and are engineering evidence only, not full BFCL/IFEval/lm-eval replacements.

Runtime:

- App: `/Applications/LM Studio.app`
- CLI: `/opt/homebrew/bin/lms`
- Endpoint: `http://127.0.0.1:1234/v1`
- Model: `qwen3-4b-hermes-smoke`
- Artifact storage: LM Studio symlink to `/Volumes/PortableSSD/hermes-exports/ollama/qwen3-4b-hermes-smoke/qwen3-4b-hermes-smoke-q4_K_M.gguf`

All runs used `--user-prefix /no_think`.

## Results

| Pilot | Suite | Pass rate | Raw output |
|---|---|---:|---|
| BFCL-style | `benchmarks/endpoint_pilots/bfcl_pilot.json` | 0.000 | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/qwen3-q4km-lmstudio-bfcl-pilot-nothink-20260524` |
| IFEval-style | `benchmarks/endpoint_pilots/ifeval_pilot.json` | 0.667 | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/qwen3-q4km-lmstudio-ifeval-pilot-nothink-20260524` |
| Coding sanity | `benchmarks/endpoint_pilots/coding_pilot.json` | 1.000 | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/qwen3-q4km-lmstudio-coding-pilot-nothink-20260524` |

## Interpretation

LM Studio is currently the strongest strict held-out endpoint for the Qwen3 artifact, but the pilot BFCL-style score is worse than llama.cpp because the invalid-tool case leaked an excluded token. Both runtimes still show that the next training pass should target exact `name` / `arguments` tool-call schema behavior.
