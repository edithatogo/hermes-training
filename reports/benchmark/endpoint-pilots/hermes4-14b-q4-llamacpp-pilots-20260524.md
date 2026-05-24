# Endpoint Pilot Benchmarks: Hermes 4 14B Q4 via llama.cpp

Date: 2026-05-24

## Scope

These are repo-native pilot checks through the llama.cpp OpenAI-compatible endpoint. They are engineering evidence only, not full BFCL/IFEval/lm-eval replacements.

Runtime:

- Endpoint: `http://127.0.0.1:8092/v1`
- Model: `hermes-4-14b-q4`
- Artifact: `/Volumes/PortableSSD/hermes-models/frontier-gguf/hermes-4-14b-q4/Hermes-4-14B_Q4_k_m.gguf`

All runs used `--user-prefix /no_think`.

## Results

| Pilot | Suite | Pass rate | Raw output |
|---|---|---:|---|
| BFCL-style | `benchmarks/endpoint_pilots/bfcl_pilot.json` | 0.000 | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/hermes4-14b-q4-llamacpp-bfcl-pilot-nothink-20260524` |
| IFEval-style | `benchmarks/endpoint_pilots/ifeval_pilot.json` | 0.667 | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/hermes4-14b-q4-llamacpp-ifeval-pilot-nothink-20260524` |
| Coding sanity | `benchmarks/endpoint_pilots/coding_pilot.json` | 1.000 | `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/hermes4-14b-q4-llamacpp-coding-pilot-nothink-20260524` |

## Interpretation

Hermes 4 14B is strong enough for runtime comparison and coding-format smoke, but it does not pass the repo's strict tool-call schema pilots. Use it as a baseline/teacher candidate, not as evidence that the local Hermes-agent target is solved.
