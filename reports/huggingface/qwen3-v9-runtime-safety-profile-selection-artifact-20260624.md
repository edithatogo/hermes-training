# Qwen3 v9 Runtime Safety Profile Selection HF Artifact

- Dataset: `edithatogo/hermes-training-artifacts`
- Path: `qwen3-v9-runtime-safety-profile-selection-20260624`
- Revision: `d5b72c1edb993677f7cfc340a5ada270716073ec`
- URL: <https://huggingface.co/datasets/edithatogo/hermes-training-artifacts/tree/d5b72c1edb993677f7cfc340a5ada270716073ec/qwen3-v9-runtime-safety-profile-selection-20260624>

This is a private evidence-only artifact. It does not include model weights,
adapter weights, or checkpoints.

## Gate Summary

| Path | Strict pass | JSON valid | Argument accuracy | Residual failures | Decision |
| --- | ---: | ---: | ---: | ---: | --- |
| raw v9 | 0.875 | 1.000 | 1.000 | 1 | not publishable as raw weights |
| v9 runtime-normalized profile | 1.000 | 1.000 | 1.000 | 0 | selectable for Hermes runtime evidence |
| raw v10 | 0.750 | 1.000 | 0.667 | 2 | rejected |

Selected runtime profile:
`qwen3-v9-no-think-prefill-refusal-marker-normalized`.

Claim boundary: this supports Hermes runtime-profile integration evidence only.
Public/raw model-weight claims remain blocked until a raw, unnormalized run
passes the same pinned safety/refusal gate.
