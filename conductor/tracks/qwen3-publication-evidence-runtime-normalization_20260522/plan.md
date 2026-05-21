# Plan: Qwen3 Publication Evidence And Runtime Normalization

## Phase 1 - Dataset Evidence

- [x] Task: Extend token audit tooling with JSON output.
- [x] Task: Run offline token audit against `Qwen/Qwen3-4B-MLX-4bit`.
- [x] Task: Record token audit output in the publication folder.

## Phase 2 - Publication Evidence

- [x] Task: Add dataset-card draft for the expanded strict tool-call lane.
- [x] Task: Add license and redistribution review.
- [x] Task: Update the run card and checklist to reference the new evidence.
- [x] Task: Keep Hugging Face publication blocked because held-out strict pass is `0.250`.

## Phase 3 - Runtime Normalization

- [x] Task: Add a self-test to `scripts/normalize_tool_response.py`.
- [x] Task: Document runtime-only empty-think normalization.
- [x] Task: Preserve strict benchmark scoring and publication gate semantics.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.7 / 10
- Evidence: token audit JSON, dataset-card draft, license review, runtime normalization contract, and self-tests are recorded.
- Decision: implemented. GitHub evidence is publishable; Hugging Face publication remains blocked by quality and redistribution scope.
