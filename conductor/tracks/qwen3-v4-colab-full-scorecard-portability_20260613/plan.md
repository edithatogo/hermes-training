# Plan: Qwen3 V4 Colab Full Scorecard Portability

## Phase 1 - Probe Script

- [x] Task: Add a Colab-safe portability probe for the public MLX adapter.
- [x] Task: Keep the probe read-only with respect to Hugging Face and benchmark datasets.

## Phase 2 - Colab Execution

- [x] Task: Run the probe on the T4 Colab lane.
- [x] Task: Capture the tracked Colab report and raw SSD log path.

## Phase 3 - Reconcile Route

- [x] Task: If MLX is usable on Colab, create the next full-scorecard execution track.
  - [x] Not applicable: MLX import is blocked on the T4 Linux CUDA runtime.
- [x] Task: If MLX is blocked on Colab, record the required portable artifact route.
- [x] Task: Run focused validation and publish the route decision.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.7 / 10
- Evidence: `reports/colab/qwen3-v4-colab-mlx-portability-20260613.md` records a live T4 Colab probe: CUDA was visible, `mlx-lm` installed, but `mlx` and `mlx_lm` imports failed with `ModuleNotFoundError: No module named 'mlx'`.
- Gaps: no exact-adapter Colab scorecard route exists until a PEFT/Transformers adapter export or equivalent portable artifact exists.
- Decision: Complete. Do not run the full Qwen3 v4 adapter scorecard on Colab with the current MLX LoRA artifact.
