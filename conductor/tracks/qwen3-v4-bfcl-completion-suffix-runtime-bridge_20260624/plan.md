# Plan: Qwen3 v4 BFCL Completion-Suffix Runtime Bridge

## Phase 1 - Runtime Hook

- [x] Task: Add configurable completion prompt suffix support to the OpenAI normalizing proxy.
    - [x] Apply only to `/v1/completions` prompts.
    - [x] Preserve chat-completions behavior.
    - [x] Expose `X-Hermes-Completion-Prompt-Suffix-Count` for request auditing.
- [x] Task: Add focused proxy tests and self-test coverage.
- [x] Task: Conductor - User Manual Verification 'Phase 1 - Runtime Hook' (Protocol in workflow.md)

## Phase 2 - Diagnostic Report

- [x] Task: Build BFCL completion-suffix diagnostic report.
    - [x] Record clean rerun blank gate: `10/10` blank rows.
    - [x] Record serial partial without suffix: still blank-heavy and no tool-like rows.
    - [x] Record next suffix: `<tool_call>`.
- [x] Task: Add validator and readiness wiring.
- [x] Task: Run focused validators and readiness.
    - [x] Proxy unit tests passed.
    - [x] Proxy self-test passed.
    - [x] Diagnostic validator passed.
    - [x] Full `scripts/validate_readiness.py` passed.
- [x] Task: Commit and push.
- [x] Task: Conductor - User Manual Verification 'Phase 2 - Diagnostic Report' (Protocol in workflow.md)

## Phase 3 - Future Bounded Rerun Gate

- [ ] Task: Run a new 10-case BFCL gated rerun through the proxy with `--completion-prompt-suffix '<tool_call>'`.
- [ ] Task: Stop before expansion unless upstream-error rows are `0`, blank-output rows are `0`, and tool-like rows are `>0`.
- [ ] Task: Evaluate with partial scoring only after the blank gate passes.

## Health Check

- Target: >= 9.5 / 10.
- Current estimate: 8.7 / 10.
- Current blocker: runtime bridge is implemented and diagnostic evidence is
  recorded, but no completion-suffix BFCL rerun has passed the blank-output
  gate yet.
