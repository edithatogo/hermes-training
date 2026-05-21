# Plan: Qwen3 Strict Tool-Call Expanded Data Retrain

## Phase 1 - Expanded Strict Data Design

- [x] Task: Define the expanded strict tool-call data target for `gemma4/data/strict_tool_call`.
    - [x] Cover single-call, multi-call, invalid-tool, argument exactness, repair, and no-tool refusal cases.
    - [x] Define minimum examples per behavior bucket before retraining.
    - [x] Keep held-out prompts, expected arguments, and answer strings excluded from training data.
- [x] Task: Record the data expansion source policy.
    - [x] Identify which examples are hand-authored, synthetic, transformed, or derived from non-held-out diagnostics.
    - [x] Record license and redistribution assumptions for any non-hand-authored examples.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1 - Expanded Strict Data Design' (Protocol in workflow.md)

## Phase 2 - Dataset Expansion and Audit

- [x] Task: Expand `gemma4/data/strict_tool_call` and regenerate splits.
    - [x] Keep split files under the existing strict tool-call data path.
    - [x] Preserve deterministic split generation or record the split command and seed.
    - [x] Avoid large generated artifacts in Git.
- [x] Task: Audit the expanded dataset before training.
    - [x] Record train, validation, and test row counts.
    - [x] Record token counts and max sequence lengths.
    - [x] Record tool coverage, behavior-bucket coverage, and exact-argument coverage.
    - [x] Check likely overlap with `benchmarks/tool_call_local/heldout_suite.json`.
    - [x] Record audit output path and summary in the publication run card.
- [x] Task: Block retraining if audit finds held-out contamination or obvious coverage gaps.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Dataset Expansion and Audit' (Protocol in workflow.md)

## Phase 3 - Retrain Attempt

- [x] Task: Prepare the retrain configuration.
    - [x] Confirm base model is `Qwen/Qwen3-4B-MLX-4bit`.
    - [x] Point the config at the expanded `gemma4/data/strict_tool_call` splits.
    - [x] Confirm caches and outputs resolve to `/Volumes/PortableSSD`.
    - [x] Choose iteration and early-stop policy based on prior validation-loss behavior.
- [x] Task: Run the retrain attempt only after the user explicitly authorizes training.
    - [x] Record exact command, config path, adapter path, wall time, peak memory, trained tokens, final validation loss, and best validation loss.
    - [x] Preserve raw logs outside source control.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - Retrain Attempt' (Protocol in workflow.md)

## Phase 4 - Held-Out Gate

- [x] Task: Run the strict held-out tool-call benchmark only after retraining completes.
    - [x] Use `benchmarks/tool_call_local/heldout_suite.json`.
    - [x] Use `--user-prefix /no_think`.
    - [x] Write raw outputs under `$HERMES_EVAL_ROOT/tool-call-benchmark/<run-id>`.
- [x] Task: Record strict held-out metrics.
    - [x] Record pass rate, JSON validity, argument correctness, invalid-tool handling, and repair metrics.
    - [x] Record diagnostic empty-think-stripped metrics as informational only.
    - [x] Keep strict pass rate as the only publication gate.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 4 - Held-Out Gate' (Protocol in workflow.md)

## Phase 5 - Publication Decision

- [x] Task: Update `reports/publication/qwen3-4b-strict-toolcall-expanded/`.
    - [x] Fill the run card with data audit, retrain, benchmark, and artifact evidence.
    - [x] Update the publish-readiness checklist with exact evidence paths.
- [x] Task: Decide publication status.
    - [x] Mark publication READY only if strict held-out pass rate is `1.000`.
    - [x] Keep Hugging Face publication BLOCKED for any strict held-out pass rate below `1.000`.
    - [x] Record residual blockers and next action if blocked.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 5 - Publication Decision' (Protocol in workflow.md)

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.6 / 10
- Evidence: expanded-data generator, deterministic materialized splits, audit utility, retrain config, completed 120-iteration MLX run, mirrored and held-out benchmarks, run card, checklist, and negative publication decision are recorded.
- Decision: implemented. GitHub publication is appropriate for the reproducibility work and negative result; Hugging Face adapter publication remains blocked because strict held-out pass rate is `0.250`, below the required `1.000`.
