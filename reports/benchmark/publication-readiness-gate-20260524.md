# Benchmark Publication Readiness Gate

Date: 2026-05-24
Updated: 2026-05-25

## Status

Publication status: **partially cleared**

The `qwen3-4b-strict-toolcall-v4-targeted` adapter now satisfies the local strict held-out Hermes-agent gate at `1.000` when evaluated with the required Qwen runtime condition. Public adapter publication is approved as an experimental strict Hermes tool-call LoRA with pilot-only benchmark positioning. Public dataset and merged-weight publication remain separate and blocked.

## Required Evidence Pack

Every publish candidate must have:

- model/runtime identity and revision
- adapter path and revision, if applicable
- training/data card, if any training occurred
- exact benchmark commands
- raw output paths under `/Volumes/PortableSSD`
- normalized score summary
- failure examples and parser diagnostics
- environment capture and repo commit
- license and redistribution review
- model card or report draft
- explicit user approval

## Current Local Evidence

| Runtime | Strict Held-Out | BFCL-Style Pilot | IFEval-Style Pilot | Coding Pilot | Decision |
|---|---:|---:|---:|---:|---|
| Qwen3 4B MLX LoRA v4 targeted with `/no_think` plus assistant prefill | `1.000` | `0.667` | `0.667` | `1.000` | Local strict gate passed; pilot failures still limit broad benchmark claims. |
| Qwen3 4B Q4_K_M via LM Studio | `0.500` | `0.000` | `0.667` | `1.000` | Best local strict endpoint so far; not publishable. |
| Qwen3 4B Q4_K_M via llama.cpp | `0.375` | `0.333` | `0.667` | `1.000` | Useful baseline; not publishable. |
| Hermes 4 14B Q4_K_M via llama.cpp | `0.250` | `0.000` | `0.667` | `1.000` | Runtime proof and baseline only. |
| LFM2 24B-A2B Q4_K_M via llama.cpp | `0.375` | `0.333` | `1.000` | `1.000` | Frontier LFM runtime proof and comparison lane only. |
| Hermes3 8B via Ollama | `0.250` | not run | not run | not run | Baseline only. |
| LFM2 2.6B via Ollama | `0.250` | not run | not run | not run | Baseline only. |

## Full Benchmark Gate

Before public Hugging Face publication:

1. Local held-out strict tool-call suite must pass at `1.000` for any model positioned as a Hermes agent. This is now satisfied by `qwen3-4b-strict-toolcall-v4-targeted` under the recorded runtime condition.
2. BFCL/IFEval/coding/lm-eval runs must be either complete or explicitly excluded in the model card.
3. Limited-sample pilot scores must be labeled as pilot-only and must not be presented as full benchmark scores.
4. Azure results, if used, must be synced back to `/Volumes/PortableSSD` with job logs and artifact paths.
5. Generated artifacts must stay out of Git unless deliberately lightweight and reviewed.

The current machine-readable coverage report is
`reports/benchmark/standard-coverage/qwen3-v4-targeted-standard-coverage-20260526.md`.
It records the v4 adapter as local-gate ready with pilot-only benchmark support.
Full official BFCL, coding, safety, and RULER candidate suites remain missing
for broad benchmark claims. The selected lm-eval smoke was attempted and is
blocked on a loglikelihood-compatible MLX/local runtime, so it must not be
reported as a score.

## Report Template

Each publishable benchmark report should use this structure:

```text
Title
Model/runtime identity
Artifact and adapter provenance
Hardware and runtime
Benchmark suites and dataset versions
Prompt template and sampling settings
Exact commands
Raw artifact paths
Normalized metrics
Failure examples
Known limitations
License/provenance notes
Publish/no-publish decision
Reviewer and date
```

## Release Decision

Publish the strict-gate evidence and benchmark harness changes to GitHub. Do not publish Hugging Face model weights, adapters, or model cards until the remaining release gates are complete and explicitly approved.
