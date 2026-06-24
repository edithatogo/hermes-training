# Plan: Qwen3 BFCL + Safety Blocker Resolution

## Phase 1 - Track Creation + Evidence Lock

- [x] Task: Create umbrella track artifacts.
    - [x] Add `metadata.json`, `spec.md`, `plan.md`, and `index.md`.
    - [x] Link the track from `conductor/tracks.md`.
    - [x] Confirm the BFCL and v9 safety/refusal source tracks remain active.
- [x] Task: Run syntax checks for new track artifacts.
- [x] Task: Conductor - User Manual Verification 'Phase 1 - Track Creation + Evidence Lock' (Protocol in workflow.md)

## Phase 2 - BFCL Clean Regeneration

- [x] Task: Finalize and validate BFCL zero-score failure analysis.
    - [x] Record that the current selected-slice artifact has `796` upstream errors, `4` blank outputs, and `800/800` contaminated rows.
    - [x] Validate `scripts/validate_bfcl_zero_score_failure_analysis.py`.
- [x] Task: Run clean selected-slice BFCL regeneration attempt.
    - [x] Use fresh root `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-peft-official-bfcl-clean-rerun-20260624`.
    - [x] Serve v4 adapter through `mlx_lm.server` on `127.0.0.1:8097`.
    - [x] Serve `scripts/openai_normalizing_proxy.py` on `127.0.0.1:8098` with `--model-override Qwen/Qwen3-4B-MLX-4bit`.
    - [x] Launch BFCL selected categories with `--num-threads 1`, `--skip-server-setup`, and `--include-input-log`.
    - [x] Stop after the first gated batch because the clean endpoint produced `10/10` blank outputs.
    - [x] Evaluate with `--partial-eval`.
- [x] Task: Add clean-rerun report and validation.
    - [x] Gate on `upstream_error_rows == 0`.
    - [x] Gate on `blank_output_rows == 0`.
    - [x] Keep selected-slice evidence separate from full BFCL claims.
    - [x] Report: `reports/benchmark/official-candidates/qwen3-v4-bfcl-clean-rerun-20260624.md`.
    - [x] Validator: `scripts/validate_bfcl_clean_rerun_report.py`.
- [x] Task: Conductor - User Manual Verification 'Phase 2 - BFCL Clean Regeneration' (Protocol in workflow.md)
    - [x] Remaining blocker: endpoint cleanliness gate passed, but blank-output gate failed.

## Phase 3 - v9 Safety/Refusal Train + Rerun

- [x] Task: Validate v9 repair data and config.
    - [x] Run `scripts/validate_qwen3_v9_repair_dataset.py`.
    - [x] Run focused v9 and safety/refusal dataset tests.
- [x] Task: Train bounded v9 repair adapter.
    - [x] Use `gemma4/scripts/train_config.qwen3-4b.strict-toolcall-v9-runtime-profile-refusal-marker-repair.yaml`.
    - [x] Write training logs under `/Volumes/PortableSSD/hermes-evals/training/qwen3-v9-runtime-profile-refusal-marker-repair-20260624`.
    - [x] Checkpoint sweep showed the bounded run was not promotable.
    - [x] Run a full-budget v9 follow-up with 140 iterations under `/Volumes/PortableSSD/hermes-evals/training/qwen3-v9-full140-runtime-profile-refusal-marker-repair-20260624`.
- [x] Task: Rerun pinned safety/refusal suite with assistant prefill.
    - [x] Use model `Qwen/Qwen3-4B-MLX-4bit`.
    - [x] Use adapter `gemma4/experiments/qwen3-4b-strict-toolcall-v9-runtime-profile-refusal-marker-repair/lora_adapter`.
    - [x] Use user prefix `/no_think\n`.
    - [x] Use assistant prefill `<think>\n\n</think>\n\n`.
    - [x] Write outputs to `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/safety/qwen3-v9-runtime-profile-refusal-marker-repair-20260624`.
    - [x] Best full-budget output root: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/safety/qwen3-v9-full140-runtime-profile-prefill-only-20260624`.
- [x] Task: Add v9 run report, validator, and tests.
    - [x] Record best strict pass rate `0.875`, JSON validity `1.000`, argument accuracy `1.000`, empty-think prefix cases `0`, residual failures `1`, refusal-marker echo count `1`, and text-mode tool-call rows `0`.
    - [x] Gate on strict pass `1.000`, empty-think prefix cases `0`, residual strict failures `0`, no marker echoes, and no text-mode tool calls.
    - [x] Report: `reports/benchmark/official-candidates/qwen3-v9-runtime-profile-refusal-marker-repair-run-20260624.md`.
    - [x] Validator: `scripts/validate_qwen3_v9_repair_run_report.py`.
- [x] Task: Conductor - User Manual Verification 'Phase 3 - v9 Safety/Refusal Train + Rerun' (Protocol in workflow.md)
    - [x] Remaining blocker: wrapper/tool-call gates passed, but strict pass remains blocked by one customer-delete marker echo.

## Phase 4 - Evidence Publication + Push

- [ ] Task: Update source and umbrella track plans.
    - [x] Update BFCL source track status/health.
    - [x] Update v9 safety/refusal source track status/health.
    - [x] Update umbrella status/health.
- [ ] Task: Run focused validators and readiness.
    - [x] Run BFCL failure/clean-rerun validators.
    - [x] Run v9 dataset/run validators.
    - [x] Run `scripts/validate_official_candidate_execution_matrix.py`.
    - [x] Run `scripts/validate_readiness.py` after focused checks passed.
- [ ] Task: Commit and push.
    - [ ] Commit/push nested `gemma4` first.
    - [ ] Commit/push hub root after nested repo state is reproducible.
- [ ] Task: Upload private HF evidence-only artifact.
    - [ ] Include reports/log manifests.
    - [ ] Exclude weights unless a separate publication review approves.
- [ ] Task: Conductor - User Manual Verification 'Phase 4 - Evidence Publication + Push' (Protocol in workflow.md)

## Health Check

- Target: >= 9.5 / 10.
- Current estimate: 8.4 / 10.
- Evidence: umbrella track is linked, BFCL failure analysis validates, BFCL
  clean-rerun reporting validates, v9 dataset/config validate, the v9 adapter
  trained, checkpoint/full-budget variants were tested, and the best pinned v9
  suite rerun is reported.
- Gaps: BFCL blank-output gate failed (`10/10` blank rows in the clean attempt);
  v9 full-budget improved to `0.875` strict pass but still fails on one
  `safety-refusal-delete-customer-record` marker echo.
- Decision: keep the umbrella active as failed-gate evidence coordination; do
  not publish weights or model-quality claims.
