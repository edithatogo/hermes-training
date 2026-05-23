# Specification: Runtime Proof Completion

## Overview

Complete the remaining Hermes runtime proof work without downloading large models. This track turns the current runtime gaps into a parallelizable validation plan for the existing Qwen3 Q4_K_M GGUF, Hermes 4 14B, Qwen3.6, the OpenAI normalizing proxy route, and the deferred Ollama retest that must wait for a runtime upgrade.

## Requirements

- Validate the existing Qwen3 4B `Q4_K_M` GGUF through LM Studio using the SSD-backed artifact already recorded in `RUNTIME_TARGETS.md`.
- Prove a Hermes 4 14B runtime path only from an already-present local artifact, active endpoint, or user-provided path. Do not download a new large Hermes 4 model as part of this track.
- Prove a Qwen3.6 runtime path only from an already-present local artifact, active endpoint, or user-provided path. Do not download a new large Qwen3.6 model as part of this track.
- Route at least one successful non-streaming runtime smoke through `scripts/openai_normalizing_proxy.py`, preserving the boundary that proxy normalization is integration evidence only and not publication benchmark evidence.
- Retest Ollama for the Qwen3 GGUF only after a concrete Ollama runtime upgrade or installation change is recorded.
- Keep all run cards, logs, summaries, and generated outputs under `/Volumes/PortableSSD`, preferably below `/Volumes/PortableSSD/hermes-evals/runtime-proof-completion/`.
- Record exact commands, endpoint URLs, model IDs, artifact paths, and smoke outcomes.
- Make parallel work explicit so independent runtime checks can proceed without blocking on unrelated model availability.

## Acceptance Criteria

- The LM Studio smoke for the existing Qwen3 `Q4_K_M` GGUF has a run card with pass/fail evidence and endpoint details.
- Hermes 4 14B has either a successful runtime smoke or a documented no-download blocker with exact missing local artifact or endpoint evidence.
- Qwen3.6 has either a successful runtime smoke or a documented no-download blocker with exact missing local artifact or endpoint evidence.
- The OpenAI normalizing proxy route is exercised against at least one validated upstream runtime, with self-test status and live route evidence recorded.
- The Ollama Qwen3 retest is either completed after a recorded runtime upgrade or explicitly left blocked because no runtime upgrade occurred.
- Runtime docs or run cards preserve the SSD artifact policy and do not introduce large model files into Git.

## Out of Scope

- Downloading large Qwen3.6, Hermes 4, or replacement Qwen3 GGUF artifacts.
- Publishing adapters, datasets, merged weights, GGUFs, or benchmark claims.
- Retesting Ollama before a concrete runtime upgrade is available.
- Changing strict benchmark scoring or treating proxy-normalized output as publication-grade evidence.
