# Plan: Qwen3.5 0.8B Strict-Suffix Repair Result

## Phase 1 - Result Capture

- [x] Task: Record the existing local repair run.
  - [x] Add a repo report summarizing the source eval output.
  - [x] Add a result registry entry with status `completed-no-promotion`.

## Phase 2 - Template Fix

- [x] Task: Fix generated experiment run ids.
  - [x] Add `RUN_STAMP=$(date +%Y%m%d-%H%M%S)` to generated commands.
  - [x] Use `${RUN_STAMP}` in `--run-id`.
  - [x] Validate that quoted literal date expressions are rejected.

## Phase 3 - Ledger And Validation

- [x] Task: Regenerate the experiment matrix, ledger, and selection report.
- [x] Task: Add result validation to full readiness.
- [x] Task: Update handoff and Conductor registry.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.8 / 10
- Evidence: The failed repair is explicitly recorded and cannot be mistaken for
  promotion evidence; future generated commands have expandable run stamps.
- Validation: Focused tests, prompt/profile validators, Conductor consistency,
  and full readiness are required before commit.
- Gaps: Grammar/envelope-constrained repair remains unrun.
- Decision: Complete. Do not rerun prompt-only Qwen3.5 0.8B repair variants;
  all queued local prompt-only variants have now failed strict promotion.
