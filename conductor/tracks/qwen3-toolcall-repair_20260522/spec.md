# Spec: Qwen3 Tool-Call Repair Proof and Runtime Normalization Gate

## Overview

Implement a local Qwen3 4B tool-call repair proof that turns the failed strict benchmark into concrete evidence for the next Hermes runtime and dataset work.

## Requirements

- Keep all training artifacts and benchmark outputs on `/Volumes/PortableSSD`.
- Add a reproducible strict tool-call seed build path.
- Run a short MLX LoRA repair training pass on Mac.
- Run the strict local tool-call benchmark with `/no_think`.
- Record both strict pass/fail and a diagnostic empty-think-stripped score without weakening the strict publication gate.
- Document whether the result is enough training and whether it is publishable.
- Keep Hugging Face publication blocked until a strict held-out tool-call benchmark passes.

## Acceptance Criteria

- Training config exists for the repair proof.
- Training completes and saves an adapter under ignored experiment storage.
- Benchmark raw outputs and summaries are written under `$HERMES_EVAL_ROOT`.
- A run card records tokens, loss, memory, wall time, command, strict score, diagnostic score, and publication decision.
- The benchmark runner reports diagnostic empty-think-stripped metrics separately from strict pass metrics.
- The track remains health >= 9.5 because the next blocker is explicit and evidenced.

## Out of Scope

- Publishing the adapter to Hugging Face.
- Claiming model-quality improvement.
- Treating benchmark-overlapping training as a valid release result.
- Downloading additional frontier models.
