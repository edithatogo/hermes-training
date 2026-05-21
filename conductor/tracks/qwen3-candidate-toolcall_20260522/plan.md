# Plan: Qwen3 Candidate Training and Tool-Call Gate

## Phase 1: Candidate Training

- [x] Add `gemma4/scripts/train_config.qwen3-4b.candidate.yaml`.
- [x] Dry-run the config under SSD-backed `scripts/env.sh`.
- [x] Run the 60-step local MLX candidate pass.
- [x] Record training tokens, validation loss, elapsed time, and peak memory.

## Phase 2: Evaluation Gates

- [x] Run 100-prompt Hermes-local evaluation.
- [x] Run response-collapse gate.
- [x] Add local tool-call benchmark runner and checked-in suite.
- [x] Run base and candidate tool-call benchmark with `/no_think`.
- [x] Record negative tool-call result as a blocker to publication.

## Phase 3: Runtime And Publication Notes

- [x] Add LM Studio smoke helper for SSD-backed GGUF validation.
- [x] Update runtime docs with the Qwen3 GGUF path and pending LM Studio endpoint check.
- [x] Add Qwen3 candidate run card.
- [x] Confirm frontier runtime candidate metadata for Qwen3.6 and Hermes 4 with read-only Hugging Face checks.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.7 / 10
- Evidence: candidate training completed at 25,094 tokens and 3.962 GB peak memory; response gate passed on 100 prompts; tool-call benchmark runner exists and was executed; failed tool-call result is documented; LM Studio helper is wired but endpoint execution remains pending because LM Studio is not installed/running here.
- Decision: track is complete as an implementation pass, but the adapter is not publishable until strict tool-call data improves the benchmark score.
