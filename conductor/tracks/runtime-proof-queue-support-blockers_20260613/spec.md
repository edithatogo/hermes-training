# Specification: Runtime Proof Queue Support Blockers

## Overview

The runtime proof action queue previously mixed two different states:

- candidates missing runtime/load evidence that should be run next, and
- candidates already proven blocked by the current local runtime or converter.

This made the top queue noisy because known unsupported architectures could be
recommended for repeat execution even though no new evidence would be produced
until the underlying runtime changed.

## Goals

- Add a distinct `runtime-support-upgrade` lane for candidates blocked by current local runtime support.
- Keep immediate `mac-runtime-proof` priorities focused on candidates that can plausibly produce new runtime evidence.
- Preserve support-model, prompt-profile, cloud-teacher, specialist-runtime, and watchlist behavior.
- Regenerate the runtime proof queue with the new lane visible in JSON and Markdown reports.

## Acceptance Criteria

- `scripts/build_runtime_proof_action_queue.py` classifies current-runtime-support blockers into `runtime-support-upgrade`.
- Runtime-support candidates get an upgrade-verification command instead of rerunning the same proof command.
- The rendered queue policy says not to rerun those candidates until the runtime/converter changes.
- Unit coverage verifies lane classification, command wording, and priority order.
- `scripts/validate_runtime_proof_action_queue.py` and hub readiness validation pass.

## Out Of Scope

- Updating llama.cpp, MLX, LM Studio, Transformers, or specialist runtimes.
- Redownloading model artifacts.
- Running new candidate runtime proofs.
- Promoting any runtime-blocked candidate.
