# Cross-Runtime Proof Matrix Execution

## Overview

Create and execute a cross-runtime proof matrix so every candidate in the Hermes, helper, mem0, embedding, and support lanes has a clear path through local and cloud execution backends.

## Scope

- Cover local runtime paths:
  - MLX and MLX-LM for Mac/Metal-first candidates
  - llama.cpp for GGUF candidates
  - Ollama for local operational packaging
  - LM Studio for OpenAI-compatible local use
  - Transformers or ONNX/CoreML where appropriate
- Cover offload and scale-out routes:
  - Colab CLI first for dynamic benchmark jobs
  - Azure only after login, subscription, quota, and region preflight
  - NVIDIA/NGC only after API-key, entitlement, and container/model preflight
  - Kaggle only if CLI/auth becomes available and the task is license-safe
- Record runtime state in proof queues and candidate metadata.

## Out of Scope

- Runtime-specific one-off hacks that cannot be reproduced from the repo.
- Downloading gated models without license acceptance.
- Cloud jobs that require private fixtures or secrets in notebooks.
- Treating a single backend success as universal runtime proof.

## Acceptance Criteria

- Each active candidate has at least one explicit runtime route and a documented desired secondary route.
- Runtime blockers identify missing packaging, missing auth, missing quota, hardware insufficiency, or license restrictions.
- Colab, Azure, and NGC preflight commands are documented with current observed state.
- Mac/Metal-specific routes are preferred for local day-to-day candidates.
- Runtime proof artifacts remain bounded and reproducible.

## Health Target

This track should not be marked complete below health 9.5. Completion requires an operator to know exactly which backend to use for the next proof job and why.
