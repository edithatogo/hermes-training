# Spec: Future Models Proof Reconciliation

## Problem

Recent runtime and benchmark work produced new evidence for MiniCPM5 1B MLX,
Qwen3.5 tiny MLX role-gates, BitNet native runtime, and North Mini Code GGUF.
Some project-level guidance still described these as unstarted or listed them in
the wrong next-action bucket. That creates a risk of rerunning stale proof work
or overstating Hermes readiness.

## Scope

- Register the recent completed proof tracks in the hub Conductor registry.
- Update `FUTURE_MODELS.md` so proof status distinguishes runtime load evidence
  from Hermes strict tool-call readiness.
- Update `HANDOFF.md` so storage status and next actions match the current SSD
  and proof state.
- Preserve fail-closed promotion language for models that loaded but failed
  strict Hermes/BFCL-style gates.

## Out Of Scope

- No new model download, training run, benchmark run, or public push.
- No promotion of MiniCPM, BitNet, North Mini Code, or Qwen3.5 tiny models to
  default Hermes runtime status.
- No changes to checked large artifacts.

## Acceptance Criteria

- The hub registry lists the completed proof tracks.
- BitNet no longer appears as merely needing first runtime proof; it is runtime
  proven but prompt-compliance blocked.
- MiniCPM5 no longer appears as an unproven local runtime proof; it is
  MLX-load/loglikelihood proven but strict tool-call blocked.
- The handoff next-action queue prioritizes LFM2.5 8B, Gemma 4 QAT, prompt
  repair/helper comparison, and specialist runtime gaps.
- Standard repo validations pass.
