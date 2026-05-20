# Plan: Qwen3 4B Smoke Training

## Phase 1: Download Reliability

- [x] Task: Configure `HF_TOKEN` or prefetch model to SSD cache.
- [x] Task: Verify no model files are written to internal disk.
- [x] Task: Dry-run Qwen3 smoke config.
- [x] Task: Blockers: note any missing HF auth, inaccessible SSD mount, or stale cache state before training.
- [x] Task: Conductor - Automated Review and Checkpoint 'Download Reliability' (Protocol in workflow.md)

## Phase 2: Smoke Training

- [x] Task: Run Qwen3 4B smoke training.
- [x] Task: Fix track-local training compatibility issues if they appear.
- [x] Task: Save adapter and run note.
- [x] Task: Conductor - Automated Review and Checkpoint 'Smoke Training' (Protocol in workflow.md)

## Phase 3: Evaluation

- [x] Task: Run Hermes-local base vs adapter smoke evaluation.
- [x] Task: Compare against LFM2.5 smoke adapter.
- [x] Task: Update docs with result and next decision.
- [x] Task: Conductor - Automated Review and Checkpoint 'Evaluation' (Protocol in workflow.md)

## Health Check

- [x] Task: Estimate track health using hub `conductor/health-score.md`.
- [ ] Task: Close or document all gaps below health 9.5.
- [ ] Task: Run hub readiness validation and attach result to the track notes.
- [ ] Task: Confirm health >= 9.5 before marking this track complete.

- Target: >= 9.5 / 10
- Current estimate: 9.7 / 10
- Evidence: SSD-backed HF login works for `edithatogo`; Qwen3 4B smoke training completed for 10 iterations / 2,889 trained tokens with final validation loss 2.386 and peak memory 3.944 GB; base and adapter evaluation completed on 100 prompts; response-collapse gate passed for both; summary recorded in `gemma4/eval/qwen3-4b-smoke-summary.md`.
- Gaps: this is still a smoke proof only, not a publishable quality claim.
- Decision: Qwen3 4B is the stronger next local MLX candidate than the collapsed LFM2.5 full-smoke adapter. Scale Qwen only with early eval checkpoints and the response gate enabled.

## Preparation Notes

- Authenticated prefetch path: source `scripts/env.sh`, export `HF_TOKEN`, then use `huggingface-cli download` or `hf download` with `HF_HOME=$HERMES_STORAGE_ROOT/huggingface` so the cache lands on the SSD-backed volume.
- SSD cache check: confirm `HF_HOME`, `HF_HUB_CACHE`, and `TMPDIR` resolve under `/Volumes/PortableSSD` when that volume is present; otherwise the fallback is `.local-storage` under the hub checkout.
- Dry run command: `source scripts/env.sh && cd gemma4 && ../.venv/bin/python scripts/train.py --config scripts/train_config.qwen3-4b.smoke.yaml --dry-run`
- Current blockers: none for smoke proof. Publication requires larger training data, standardized benchmarks, and runtime endpoint validation.
